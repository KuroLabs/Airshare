"""Module for sending data and hosting sending servers."""


from aiohttp import web
import asyncio
import humanize
from multiprocessing import Process
import os
import pkgutil
import platform
import requests
from requests_toolbelt import MultipartEncoder
import socket
import sys


from .exception import CodeExistsError, CodeNotFoundError, IsNotReceiverError
from .utils import get_local_ip_address, get_service_info, get_zip_file, \
    qr_code, register_service


__all__ = ["send", "send_server", "send_server_proc"]


# Request handlers


async def _text_page(request):
    """Renders a text viewing page, GET handler for route '/'."""
    text = pkgutil.get_data(__name__, "static/text.html").decode()
    return web.Response(text=text, content_type="text/html")


async def _text_sender(request):
    """Returns the text being shared, GET handler for route '/text'."""
    address = ""
    peername = request.transport.get_extra_info("peername")
    if peername is not None:
        host, _ = peername
        address = " (by " + str(host) + ")"
    print("Content viewed" + address + "!")
    return web.Response(text=request.app["text"])


async def _download_page(request):
    """Renders a download page, GET handler for route '/'."""
    download = pkgutil.get_data(__name__, "static/download.html").decode()
    return web.Response(text=download, content_type="text/html")


async def _file_stream_sender(request):
    """Streams a file from the server, GET handler for route '/download'."""
    address = ""
    peername = request.transport.get_extra_info("peername")
    if peername is not None:
        host, _ = peername
        address = " (by " + str(host) + ")"
    if request.method == "GET":
        print("Content requested" + address + ", transferring!")
    elif request.method == "HEAD":
        print("Content examined" + address + "!")
    response = web.StreamResponse()
    file_path = request.app["file_path"]
    file_name = request.app["file_name"]
    file_size = str(request.app["file_size"])
    header = "attachment; filename=\"{}\"; size={}" \
             .format(file_name, file_size)
    response.headers["content-type"] = "application/octet-stream"
    response.headers["content-length"] = str(request.app["file_size"])
    response.headers["content-disposition"] = header
    response.headers["airshare-compress"] = request.app["compress"]
    await response.prepare(request)
    with open(file_path, "rb") as f:
        chunk = f.read(8192)
        while chunk:
            await response.write(chunk)
            chunk = f.read(8192)
    return response


async def _is_airshare_text_sender(request):
    """Returns 'Text Sender', GET handler for route '/airshare'."""
    return web.Response(text="Text Sender")


async def _is_airshare_file_sender(request):
    """Returns 'File Sender', GET handler for route '/airshare'."""
    return web.Response(text="File Sender")


# Sender functions


def send(*, code, file, compress=False):
    r"""Send file(s) or directories to a receiving server.

    Parameters
    ----------
    code : str
        Identifying code for the Airshare receiving server.
    file : str or list or None
        Relative path or list of paths of the files or directories to serve.
        For multiple files or directories, contents are automatically zipped.
    compress : boolean, default=False
        Flag to enable or disable compression (Zip).
        Effective when only one file is given.

    Returns
    -------
    status_code : int
        Status code of upload POST request.
    """
    info = get_service_info(code)
    if info is None:
        raise CodeNotFoundError(code)
    if type(file) is str:
        if file == "":
            file = None
        else:
            file = [file]
    elif len(file) == 0:
        file = None
    if file is None:
        raise ValueError("The parameter `file` must be non-empty!")
    if compress or len(file) > 1 or os.path.isdir(file[0]):
        compress = "true"
        print("Compressing...")
        file, name = get_zip_file(file)
        print("Compressed to `" + name + "`!")
    else:
        compress = "false"
        file, name = file[0], file[0].split(os.path.sep)[-1]
    ip = socket.inet_ntoa(info.addresses[0])
    url = "http://" + ip + ":" + str(info.port)
    airshare_type = requests.get(url + "/airshare")
    if airshare_type.text != "Upload Receiver":
        raise IsNotReceiverError(code)
    m = MultipartEncoder(fields={"field0": (name, open(file, "rb"))})
    headers = {"content-type": m.content_type, "airshare-compress": compress}
    r = requests.post(url + "/upload", data=m, headers=headers)
    print("Uploaded `" + name + "` to Airshare `" + code + "`!")
    return r.status_code


def send_server(*, code, text=None, file=None, compress=False, port=8000):
    r"""Serves a file or text and registers it as a Multicast-DNS service.

    Parameters
    ----------
    code : str
        Identifying code for the Airshare service and server.
    text : str or None
        String value to be shared.
        If both `text` and `files` are given, `text` will be shared.
        Must be given if `files` is not given.
    file : str or list or None
        Relative path or list of paths of the files or directories to serve. If
        multiple files or directories are given, the contents are automatically
        zipped. If not given or both `files` and `text` are given, `text` will
        be shared. Must be given if `text` is not given.
    compress : boolean, default=False
        Flag to enable or disable compression (Zip).
        Effective when only one file is given.
    port : int, default=8000
        Port number at which the server is hosted on the device.
    """
    info = get_service_info(code)
    if info is not None:
        raise CodeExistsError(code)
    if file is not None:
        if type(file) is str:
            if file == "":
                file = None
            else:
                file = [file]
        elif len(file) == 0:
            file = None
    content = text or file
    name = None
    if content is None:
        raise ValueError("Either `file` or `text` (keyword arguments) must be"
                         + " given and non-empty!")
    elif text is None and file is not None:
        if compress or len(file) > 1 or os.path.isdir(file[0]):
            compress = "true"
            print("Compressing...")
            content, name = get_zip_file(file)
            print("Compressed to `" + name + "`!")
        else:
            compress = "false"
            content = file[0]
    addresses = [get_local_ip_address()]
    register_service(code, addresses, port)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = web.Application()
    file_size = ""
    if text is not None:
        app["text"] = content
        app.router.add_get(path="/", handler=_text_page)
        app.router.add_get(path="/text", handler=_text_sender)
        app.router.add_get(path="/airshare", handler=_is_airshare_text_sender)
    elif file:
        app["file_path"] = os.path.realpath(content)
        app["file_name"] = name or app["file_path"].split(os.path.sep)[-1]
        app["file_size"] = os.stat(app["file_path"]).st_size
        app["compress"] = compress
        file_size = " (" + humanize.naturalsize(app["file_size"]) + ")"
        content = app["file_name"]
        app.router.add_get(path="/", handler=_download_page)
        app.router.add_get(path="/airshare", handler=_is_airshare_file_sender)
        app.router.add_get(path="/download", handler=_file_stream_sender)
    runner = web.AppRunner(app)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, "0.0.0.0", str(port))
    loop.run_until_complete(site.start())
    url_port = ""
    if port != 80:
        url_port = ":" + str(port)
    ip = socket.inet_ntoa(addresses[0]) + url_port
    quit_msg = "`, press Ctrl+C to stop sharing..."
    if platform.system() == "Windows" and sys.version_info < (3, 8):
        quit_msg = "`, press Ctrl+Break to stop sharing..."
    print("`" + content + "`" + file_size + " available at " + ip
          + " and `http://" + code + ".local" + url_port + quit_msg)
    qr_code("http://" + ip)
    loop.run_forever()


def send_server_proc(*, code, text=None, file=None, compress=False, port=8000):
    r"""Creates a process with 'send_server' as the target.

    Parameters
    ----------
    code : str
        Identifying code for the Airshare service and server.
    text : str or None
        String value to be shared.
        If both `text` and `files` are given, `text` will be shared.
        Must be given if `files` is not given.
    file : str or list or None
        Relative path or list of paths of the files or directories to serve. If
        multiple files or directories are given, the contents are automatically
        zipped. If not given or both `files` and `text` are given, `text` will
        be shared. Must be given if `text` is not given.
    compress : boolean, default=False
        Flag to enable or disable compression (Zip).
        Effective when only one file is given.
    port : int, default=8000
        Port number at which the server is hosted on the device.

    Returns
    -------
    process: multiprocessing.Process
        A multiprocessing.Process object with 'send_server' as target.
    """
    kwargs = {"code": code, "file": file, "text": text, "compress": compress,
              "port": port}
    process = Process(target=send_server, kwargs=kwargs)
    return process

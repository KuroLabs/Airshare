"""Module for receiving data and hosting receiving servers."""


from aiohttp import web
import asyncio
import humanize
from multiprocessing import Process
import os
import pkgutil
import platform
import pyqrcode
import requests
import socket
from time import sleep, strftime
from tqdm import tqdm
from zipfile import ZipFile, is_zipfile


from .exception import CodeExistsError, CodeNotFoundError, IsNotSenderError
from .utils import get_service_info, get_local_ip_address, register_service, \
    unzip_file


__all__ = ["receive", "receive_server", "receive_server_proc"]


_tqdm_position = -1


# Request handlers


async def _upload_page(request):
    """Renders an upload page. GET handler for route '/'."""
    upload = pkgutil.get_data(__name__, "static/upload.html").decode()
    return web.Response(text=upload, content_type="text/html")


async def _uploaded_file_receiver(request):
    """Receives an uploaded file. POST handler for '/upload'."""
    global _tqdm_position
    _tqdm_position += 1
    reader = await request.multipart()
    field = await reader.next()
    file_name = field.filename
    file_path = os.getcwd() + os.path.sep + file_name
    if os.path.isfile(file_path):
        file_name, file_ext = os.path.splitext(file_name)
        file_name = file_name + "-" + strftime("%Y%m%d%H%M%S") + file_ext
        file_path = os.getcwd() + os.path.sep + file_name
    desc = "Downloading `" + file_name + "`"
    bar = tqdm(desc=desc, total=0, unit="B", unit_scale=1,
               position=_tqdm_position)
    with open(file_path, "wb") as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            bar.total += len(chunk)
            f.write(chunk)
            bar.update(len(chunk))
    if is_zipfile(file_path) and request.app["decompress"] == "True":
        unzip_file(file_path)
        os.remove(file_path)
    file_name = field.filename
    file_size = humanize.naturalsize(bar.total)
    text = "{} ({}) successfully received!".format(file_name, file_size)
    return web.Response(text=text)


async def _is_airshare_upload_receiver(request):
    """Returns 'Upload Receiver'. GET handler for '/airshare'."""
    return web.Response(text="Upload Receiver")


# Receiver functions


def receive(*, code, decompress=False):
    r"""Receive file(s) from a sending server.

    Parameters
    ----------
    code : str
        Identifying code for the Airshare sending server.
    decompress : boolean, default=False
        Flag to enable or disable decompression (Zip).

    Returns
    -------
    text (or) file_path : str
        Returns the text or path of the file received, if successful.
    """
    info = get_service_info(code)
    if info is None:
        raise CodeNotFoundError(code)
    ip = socket.inet_ntoa(info.addresses[0])
    url = "http://" + ip + ":" + str(info.port)
    airshare_type = requests.get(url + "/airshare").text
    if "Sender" not in airshare_type:
        raise IsNotSenderError(code)
    print("Receiving from Airshare `" + code + ".local`...")
    sleep(2)
    if airshare_type == "Text Sender":
        text = requests.get(url + "/text").text
        print("Received: " + text)
        return text
    elif airshare_type == "File Sender":
        with requests.get(url + "/download", stream=True) as r:
            r.raise_for_status()
            header = r.headers["content-disposition"]
            file_name = header.split("; ")[1].split("=")[1]
            file_path = os.getcwd() + os.path.sep + file_name
            file_size = int(header.split("=")[-1])
            if os.path.isfile(file_path):
                file_name, file_ext = os.path.splitext(file_name)
                file_name = file_name + "-" + strftime("%Y%m%d%H%M%S") + file_ext
                file_path = os.getcwd() + os.path.sep + file_name
            with open(file_path, "wb") as f:
                desc = "Downloading `" + file_name + "`"
                bar = tqdm(desc=desc, total=file_size, unit="B", unit_scale=1)
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))
            file_path = os.path.realpath(file_path)
            if is_zipfile(file_path) and decompress:
                print("Decompressing...")
                zip_dir = unzip_file(file_path)
                print("Decompressed to `" + zip_dir + "`!")
                os.remove(file_path)
                file_path = zip_dir
            return file_path


def receive_server(*, code, decompress=False, port=80):
    r"""Serves a file receiver and registers it as a Multicast-DNS service.

    Parameters
    ----------
    code : str
        Identifying code for the Airshare service and server.
    decompress : boolean, default=False
        Flag to enable or disable decompression (Zip).
    port : int, default=80
        Port number at which the server is hosted on the device.
    """
    info = get_service_info(code)
    if info is not None:
        raise CodeExistsError(code)
    addresses = [get_local_ip_address()]
    register_service(code, addresses, port)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = web.Application()
    app["decompress"] = str(decompress)
    app.router.add_get(path="/", handler=_upload_page)
    app.router.add_get(path="/airshare", handler=_is_airshare_upload_receiver)
    app.router.add_post(path="/upload", handler=_uploaded_file_receiver)
    runner = web.AppRunner(app)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, "0.0.0.0", str(port))
    loop.run_until_complete(site.start())
    url_port = ""
    if port != 80:
        url_port = ":" + str(port)
    ip = socket.inet_ntoa(addresses[0]) + url_port
    print("Waiting for uploaded files at " + ip + " and `http://"
          + code + ".local" + url_port + "`, press CtrlC to stop receiving...")
    if platform.system() != "Windows":
        print(pyqrcode.create("http://" + ip).terminal(quiet_zone=1))
    if decompress:
        print("Note: Any Zip Archives will be decompressed!")
    loop.run_forever()


def receive_server_proc(*, code, decompress=False, port=80):
    r"""Creates a process with 'receive_server' as the target.

    Parameters
    ----------
    code : str
        Identifying code for the Airshare service and server.
    decompress : boolean, default=False
        Flag to enable or disable decompression (Zip).
    port : int, default=80
        Port number at which the server is hosted on the device.

    Returns
    -------
    process: multiprocessing.Process
        A multiprocessing.Process object with 'receive_server' as target.
    """
    kwargs = {"code": code, "decompress": decompress, "port": port}
    process = Process(target=receive_server, kwargs=kwargs)
    return process

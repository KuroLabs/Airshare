"""Module for receiving data and hosting rceeiving servers."""


from aiohttp import web
import asyncio
import humanize
from multiprocessing import Process
import os
import pyqrcode
import requests
import socket
from time import sleep, strftime
from tqdm import tqdm
from zeroconf import IPVersion, ServiceInfo, Zeroconf
from zipfile import ZipFile, is_zipfile


from .utils import file_stream_receiver, get_local_ip_address, unzip_file


__all__ = ["receive", "receive_server", "receive_server_proc"]


# Request handlers


async def _upload_page(request):
    """Renders an upload page. GET handler for route '/'."""
    return web.Response(text="""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Airshare Upload</title>
        </head>
        <body>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input name="file-input" type="file"/>
            <input type="submit" value="Upload"/>
        </form>
        </body>
        </html>
    """, content_type="text/html")


async def _uploaded_file_receiver(request):
    """Receives an uploaded file. POST handler for '/upload'."""
    reader = await request.multipart()
    field = await reader.next()
    file_name = field.filename
    file_path = os.getcwd() + os.path.sep + file_name
    file_size = 0
    if os.path.isfile(file_path):
        file_name, file_ext = os.path.splitext(file_name)
        file_name = file_name + "-" + strftime("%Y%m%d%H%M%S") + file_ext
        file_path = os.getcwd() + os.path.sep + file_name
    with open(file_path, "wb") as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            f.write(chunk)
            file_size += len(chunk)
    desc = "Downloading `" + file_name + "`"
    tqdm(desc=desc, initial=file_size, total=file_size, unit="B", unit_scale=1)
    if is_zipfile(file_path) and request.app["decompress"] == "True":
        zip_dir = unzip_file(file_path)
        print("Decompressed to `" + zip_dir + "`!")
        os.remove(file_path)
    file_name = field.filename
    file_size = humanize.naturalsize(file_size)
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
    Returns the text or path of the file received, if successful.
    Returns 1 on failure.
    """
    zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
    service = "_airshare._http._tcp.local."
    info = zeroconf.get_service_info(service, code + service)
    if info is None:
        print("The airshare `" + code + ".local` does not exist!")
        return 1
    ip = socket.inet_ntoa(info.addresses[0])
    url = "http://" + ip + ":" + str(info.port)
    airshare_type = requests.get(url + "/airshare").text
    if "Sender" not in airshare_type:
        print("The airshare `" + code + ".local` is not a sender!")
        return 1
    print("Receiving from airshare `" + code + ".local`...")
    sleep(2)
    if airshare_type == "Text Sender":
        text = requests.get(url).text
        print("Received: " + text)
        return text
    elif airshare_type == "File Sender":
        file_path = file_stream_receiver(url + "/download")
        if is_zipfile(file_path) and decompress:
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
    zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
    service = "_airshare._http._tcp.local."
    if zeroconf.get_service_info(service, code + service) is not None:
        print("`" + code + "` already exists, please use a different code!")
        return
    addresses = [get_local_ip_address()]
    info = ServiceInfo(
        service,
        code + service,
        addresses=addresses,
        port=port,
        server=code + ".local."
    )
    zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
    zeroconf.register_service(info)
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
    ip = socket.inet_ntoa(info.addresses[0])
    print("Waiting for uploaded files at " + ip + url_port + " and `http://"
          + code + ".local" + url_port + "`, press CtrlC to stop receiving...")
    print(pyqrcode.create("http://" + ip + url_port).terminal(quiet_zone=1))
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

"""Utility functions for Airshare."""


import mimetypes
import os
import pyperclip
import re
import socket
import tempfile
from time import strftime
from zipfile import ZipFile
from zeroconf import IPVersion, ServiceInfo, Zeroconf


from .qrcode import ErrorCorrectLevel, QRCode


__all__ = ["get_local_ip_address", "qr_code", "get_service_info",
           "register_service", "get_zip_file", "unzip_file",
           "get_clipboard_paths", "is_file_copyable"]


# Local IP Address


def get_local_ip_address():
    r"""Obtains the device's local network IP address.

    Returns
    -------
    ip : bytes
        Packed 32-bit representation of the device's local IP Address.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.255.255.255", 1))
    ip = s.getsockname()[0]
    s.close()
    ip = socket.inet_aton(ip)
    return ip


# QR Code Utility


def qr_code(url):
    r"""Generate QR Code from URL and print it.

    Parameters
    ----------
    url : str
        URL to create the QR Code for.
    """
    qr = QRCode.getMinimumQRCode(url, ErrorCorrectLevel.M)
    qr.setErrorCorrectLevel(ErrorCorrectLevel.M)
    qr.make()
    qr.printQr()


# Zeroconf Utilities


def get_service_info(code):
    r"""Get service information for an Airshare service.

    Parameters
    ----------
    code : str
        Identifying code for the Airshare service.

    Returns
    -------
    info : zeroconf.ServiceInfo
        Details of the Airshare service.
    """
    zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
    service = "_airshare._http._tcp.local."
    info = zeroconf.get_service_info(service, code + service)
    return info


def register_service(code, addresses, port):
    r"""Registers an Airshare Multicast-DNS service based in the local network.

    Parameters
    ----------
    code : str
        Identifying code for the Airshare service.
    addresses : list
        List of local network IP Addresses for the service.
    port : int
        Port number for the Airshare service's server.

    Returns
    -------
    info : zeroconf.ServiceInfo
        Details of the Airshare service.
    """
    zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
    service = "_airshare._http._tcp.local."
    info = ServiceInfo(
        service,
        code + service,
        addresses=addresses,
        port=port,
        server=code + ".local."
    )
    zeroconf.register_service(info)
    return info


# Zip and Unzip


def get_zip_file(files):
    r"""Creates a temporary Zip Archive of files and directories.

    Parameters
    ----------
    files : list
        List of paths of files and directories to compress.

    Returns
    -------
    zip_file_path : str
        Canonical file path of the temporary Zip Archive file.
    zip_file_name : str
        File name to be assigned to the Zip Archive (during sending).
    """
    files = [os.path.realpath(x) for x in files]
    _, zip_file_path = tempfile.mkstemp(prefix="airshare", suffix=".zip")
    zip_archive = ZipFile(zip_file_path, "w")
    num_files = len(files)
    index = -1
    if num_files == 1:
        index = 0
    for item in files:
        index += len(item.split(os.path.sep))
        if os.path.isdir(item):
            for root, _, file_list in os.walk(item):
                for file in file_list:
                    file_path = os.path.realpath(os.path.join(root, file))
                    zip_archive.write(file_path, os.path.join(
                        *tuple(root.split(os.path.sep)[index:] + [file])))
        else:
            file_path = os.path.realpath(item)
            zip_archive.write(file_path, os.path.join(
                *tuple(file_path.split(os.path.sep)[index:])))
        index = -1
    zip_archive.close()
    zip_file_path = os.path.abspath(zip_file_path)
    zip_file_name = "airshare.zip"
    if num_files == 1:
        zip_file_name = os.path.splitext(
            os.path.realpath(files[0]).split(os.path.sep)[-1])[0] + ".zip"
    return zip_file_path, zip_file_name


def unzip_file(zip_file_path):
    r"""Unzips a Zip Archive file into a new directory.

    Parameters
    ----------
    zip_file_path : str
        Path of the Zip Archive file to unzip.

    Returns
    -------
    zip_dir : str
        Canonical path of the unzipped directory.
    """
    zip_dir = zip_file_path[:-4]
    if os.path.isdir(zip_dir):
        zip_dir += "-" + strftime("%Y%m%d%H%M%S")
    os.mkdir(zip_dir)
    with ZipFile(zip_file_path, "r") as zip_archive:
        zip_archive.extractall(zip_dir)
    zip_dir = os.path.realpath(zip_dir)
    return zip_dir


# Clipboard Utilities


def get_clipboard_paths():
    r"""Extract file paths from the clipboard.

    Returns
    -------
    file_paths : list
        List of canonical paths extracted from the clipboard.
    """
    file_paths = []
    clipboard = pyperclip.paste()
    erase = ["x-special/nautilus-clipboard\ncopy\n", "file://", "\r", "'", '"']
    file_paths = re.sub("|".join(erase), "", clipboard.strip()).split("\n")
    file_paths = [os.path.realpath(str(x).strip()) for x in file_paths]
    return file_paths


def is_file_copyable(file_path):
    r"""Check if a file can be copied to the clipboard or not.

    Parameters
    ----------
    file_path : str
        Path of the file to check.

    Returns
    -------
    copyable : boolean
        True if the file can be copied to the clipboard, False otherwise.
    """
    file_type = mimetypes.guess_type(file_path)[0]
    copyable = False
    if file_type is not None:
        if (re.findall("text|json", file_type, re.IGNORECASE)):
            copyable = True
        else:
            copyable = False
    return copyable

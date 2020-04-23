"""Utility functions for Airshare."""


import magic
import os
import pyperclip
import re
import requests
import socket
import tempfile
from time import strftime
from tqdm import tqdm
from zipfile import ZipFile


__all__ = ["get_local_ip_address", "get_zip_file", "unzip_file",
           "file_stream_receiver", "get_clipboard_paths", "is_file_copyable"]


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


# Stream Receiver


def file_stream_receiver(url):
    r"""Receives content streamed by a sender.

    Parameters
    ----------
    url : str
        The URL of the sender (server) where the content is served.

    Returns
    -------
    file_path : str
        Canonical path of the file received.
    """
    with requests.get(url, stream=True) as r:
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
            format = "{l_bar} {bar}| {n_fmt}/{total_fmt}"
            bar = tqdm(desc=desc, total=file_size, unit="B", unit_scale=1,
                       bar_format=format)
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))
        return os.path.realpath(file_path)


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
    file_type = magic.Magic(mime=True).from_file(file_path)
    if (re.findall("text|json", file_type, re.IGNORECASE)):
        copyable = True
    else:
        copyable = False
    return copyable

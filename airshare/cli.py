"""Command Line Interface for Airshare."""


import click
import os
import pyperclip


from .utils import is_file_copyable, get_clipboard_paths
from .sender import send, send_server
from .receiver import receive, receive_server


@click.command(name="airshare")
@click.argument("code", nargs=1)
@click.option("-p", "--port", type=int, default=80, help="""
Specify the port number to host a sending or receiving server (defaults to 80).
""")
@click.option("-t", "--text", type=str, help="""
Send (serve) text content. For multiple words, enclose within quotes.
""")
@click.option("-u", "--upload", is_flag=True, help="""
Host a receiving server or upload file(s) to one.
""")
@click.option("-cs", "--clip-send", is_flag=True, help="""
Send (serve) clipboard contents as text.
""")
@click.option("-cr", "--clip-receive", is_flag=True, help="""
Receive served content and also copy into clipboard (if possible).
""")
@click.option("-fp", "--file-path", is_flag=True, help="""
Send files whose paths have been copied to the clipoard.
""")
@click.argument("files", nargs=-1)
@click.help_option()
@click.version_option(version=None, prog_name="Airshare")
def main(code, port, text, upload, clip_send, clip_receive, file_path, files):
    r"""Airshare - an easy way to share content in a local network.

    CODE - An identifying code for Airshare.

    FILES - File(s) or directories to send.
    """
    files = get_clipboard_paths() if file_path else files
    if text:
        try:
            send_server(code=code, text=text, port=port)
        except KeyboardInterrupt:
            exit(0)
    if clip_send:
        try:
            send_server(code=code, text=pyperclip.paste(), port=port)
        except KeyboardInterrupt:
            exit(0)
    if clip_receive:
        content = receive(code=code)
        if os.path.exists(content):
            if is_file_copyable(content):
                with open(content, "r") as f:
                    pyperclip.copy(f.read())
                print("File copied to clipboard!")
            else:
                print("This file cannot be copied to the clipboard!")
        else:
            pyperclip.copy(content)
        return
    if len(files):
        if upload:
            send(code=code, file=list(files))
            return
        else:
            try:
                send_server(code=code, file=files, port=port)
            except KeyboardInterrupt:
                exit(0)
    else:
        if upload:
            try:
                receive_server(code=code, port=port)
            except KeyboardInterrupt:
                exit(0)
        else:
            receive(code=code)


if __name__ == "__main__":
    main(prog_name="Airshare")

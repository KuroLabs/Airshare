<h1 align="center">
  <br>
  <img src="https://raw.githubusercontent.com/KuroLabs/Airshare/master/assets/Airshare.svg" alt="Airshare" width="100">
  <br>
  <br>
  <span>Airshare</span>
  <br>
  <br>
</h1>

<h4 align="center">An easy way to share content in a local network using Multicast DNS.</h4>

<p align="justify"><b>Airshare</b> is a Python-based CLI tool that lets you transfer data between two machines in a local network, P2P, using Multicast DNS. It also opens an HTTP gateway for other non-CLI external interfaces. It works completely offline! Built with aiohttp and zeroconf.</p>

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Airshare.

```bash
pip install airshare
```

## Example

Send and receive files and directories.

To send,

```bash
airshare noobmaster requirements.txt
```
To receive using the CLI,

```bash
airshare noobmaster
```

or visit `http://noobmaster.local` in the browser to download.

## CLI Tool Usage

```bash
Usage: airshare [OPTIONS] CODE [FILES]

  Airshare - an easy way to share content in a local network.

  CODE - An identifying code for Airshare.

  FILES - File(s) or directories to send.

Options:

  -p, --port INTEGER   Specify the port number to host a sending or receiving
                       server (defaults to 80).
 
  -t, --text TEXT      Send (serve) text content. For multiple words, enclose
                       within quotes.
    
  -u, --upload         Host a receiving server or upload file(s) to one.

  -cs, --clip-send     Send (serve) clipboard contents as text.

  -cr, --clip-receive  Receive served content and also copy into clipboard (if
                       possible).

  -fp, --file-path     Send files whose paths have been copied to the
                       clipoard.

  -h, --help           Show this message and exit. For more detailed
                       instructions, use `man airshare`.

```

## Flags

* The `-t` flag can be used to send text using airshare.

  ```bash
  airshare noobmaster -t "I'm still worthy!"
  ```

* The `-u` flag opens an upload endpoint to receive files from multiple users who initiate a send with the same flag. This is useful to receive files from devices without CLI support - they may simply visit the endpoint URL from any browser.

  At the receiver,

  ```bash
  airshare -u noobmaster
  ```

  At the sender,

  ```bash
  airshare -u noobmaster file.txt
  ```

* The `-fp` flag allows users to copy file or directory paths from the Finder or File Explorer and send them. Useful for selecting multiple files instead of typing file paths.

  Select required files and use the following shortcuts to copy file paths.

  For Mac,

  <kbd>Command</kbd> + <kbd>Option</kbd> + <kbd>C</kbd>

  For Windows,

  <kbd>Shift</kbd> + <img src="https://raw.githubusercontent.com/KuroLabs/Airshare/master/assets/RightClick.svg" width="20">  and select  <kbd>Copy as Path</kbd>

  For Linux,

  <kbd>Ctrl</kbd> + <kbd>C</kbd>

  To send the files,

  ```bash
  airshare -fp noobmaster
  ```

* The `-cs` flag allows users to directly send the clipboard contents as text.

  To send,

  ```bash
  airshare -cs noobmaster
  ```

* The `-cr` flag allows users to copy the data received if clipboard compatible. 

  To receive,

  ```bash
  airshare -cs noobmaster
  ```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://github.com/KuroLabs/Airshare/blob/master/LICENSE.md) - Copyright (c) 2020 [Kandavel A](http://github.com/AK5123), [Mohanasundar M](https://github.com/mohanpierce99), [Nanda H Krishna](https://github.com/nandahkrishna)

## Acknowledgements
The Airshare logo was designed by [Siddique](https://dribbble.com/thesideeq).

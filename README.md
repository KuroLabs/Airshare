<h1 align="center">
  <br>
  <img src="https://raw.githubusercontent.com/KuroLabs/Airshare/master/assets/Airshare.svg" alt="Airshare" width="100">
  <br>
  <br>
  <span>Airshare</span>
  <br>
  <br>
  <a href="https://pypi.org/project/Airshare">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/Airshare" />
  </a>
   <a href="https://pypi.org/project/Airshare">
    <img alt="PyPI" src="https://static.pepy.tech/badge/airshare" />
  </a>
  <a href="https://pypi.org/project/Airshare">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/Airshare" />
  </a>
  <a href="https://github.com/KuroLabs/Airshare/blob/master/LICENSE.md">
    <img alt="PyPI - License" src="https://img.shields.io/pypi/l/Airshare">
  </a>
  <a href="https://airshare.readthedocs.io/en/latest/?badge=latest">
    <img src="https://readthedocs.org/projects/airshare/badge/?version=latest" alt="Documentation Status" />
  </a>
</h1>

<h4 align="center">Cross-platform content sharing in a local network.</h4>

<p align="justify"><b>Airshare</b> is a Python-based CLI tool and module that lets you transfer data between two machines in a local network, P2P, using Multicast-DNS. It also opens an HTTP gateway for other non-CLI external interfaces. It works completely offline! Built with aiohttp and zeroconf. Checkout the <a href="https://www.youtube.com/watch?v=iJH6bkLRdSw">demo</a>.</p>

## Features

* Blazing fast content transfer within a local network.

* Lets you transfer plain text, send from or receive into your clipboard.

* Supports transfer of multiple files, directories and large files - content is sent chunk by chunk and never read into memory entirely.

* Lets you send files whose paths have been copied into the clipboard (more details in the docs).

* Cross-platform, works on Linux, Windows and Mac (CLI and Web Interface), and also supports mobile (Web Interface).

* Uses Multicast-DNS service registration and discovery - so you can access content with human-readable code words.

* Can be used as a module in other Python programs.

![Airshare Demo](assets/Airshare.gif)

## Important Links

Source Code: https://github.com/KuroLabs/Airshare <br>
Bug Reports: https://github.com/KuroLabs/Airshare/issues <br>
Documentation: https://airshare.rtfd.io <br>
PyPI: https://pypi.org/project/Airshare <br>

## Installation

### [pip](https://pip.pypa.io/en/stable/)

```bash
$ pip install Airshare
```

### [pipx](https://pipxproject.github.io/pipx/)

```bash
$ pipx install Airshare
```

### [Homebrew](https://brew.sh)

```bash
$ brew install airshare
```

## Example

Send and receive files and directories.

To send using the CLI,

```bash
$ airshare noobmaster requirements.txt
```
To receive using the CLI,

```bash
$ airshare noobmaster
```

or visit `http://noobmaster.local:8000` in the browser to download.

You can also `import airshare` in any Python program. Visit the documentation for detailed usage instructions.

## Known Issues

* Link-local Name Resolution (for the `.local` addresses) on non-Apple devices requires Avahi (on Linux) or Bonjour (on Windows). Chances are you already have them, but if you don't, do check the web on how to install them.

* Android browsers do not have inbuilt Multicast-DNS service discovery, and cannot resolve the `.local` addresses. For this reason, we included QR Code support, for you to visit the URLs easily.

* Windows users with Python < 3.8, use <kbd>Ctrl</kbd> + <kbd>Break</kbd> to quit, as <kbd>Ctrl</kbd> + <kbd>C</kbd> will not work. This is a known issue with `asyncio`, which has been fixed in Python 3.8. If you do not have a <kbd>Break</kbd> key, try using <kbd>Ctrl</kbd> + <kbd>Fn</kbd> + <kbd>B</kbd>, or check the web for other alternatives (depending on your PC).

## Contributing

Contributions are welcome! Read our [Contribution Guide](https://github.com/KuroLabs/Airshare/blob/master/CONTRIBUTING.md) for more details.

## License

[MIT](https://github.com/KuroLabs/Airshare/blob/master/LICENSE.md) - Copyright (c) 2020 [Kandavel A](http://github.com/AK5123), [Mohanasundar M](https://github.com/mohanpierce99), [Nanda H Krishna](https://github.com/nandahkrishna)

## Acknowledgements

The Airshare logo was designed by [Siddique](https://dribbble.com/thesideeq).

The Airshare GIF was created by [Anam Saatvik](https://github.com/kalki7).

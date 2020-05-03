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
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/Airshare" />
  </a>
  <a href="https://github.com/KuroLabs/Airshare/blob/master/LICENSE.md">
  <img alt="PyPI - License" src="https://img.shields.io/pypi/l/Airshare">
  </a>
  <a href="https://airshare.readthedocs.io/en/latest/?badge=latest">
    <img src="https://readthedocs.org/projects/airshare/badge/?version=latest" alt="Documentation Status" />
  </a>
</h1>

<h4 align="center">An easy way to share content in a local network using Multicast-DNS.</h4>

<p align="justify"><b>Airshare</b> is a Python-based CLI tool and module that lets you transfer data between two machines in a local network, P2P, using Multicast-DNS. It also opens an HTTP gateway for other non-CLI external interfaces. It works completely offline! Built with aiohttp and zeroconf.</p>

## Important Links

Source Code: https://github.com/KuroLabs/Airshare <br>
Bug Reports: https://github.com/KuroLabs/Airshare/issues <br>
Documentation: https://airshare.rtfd.io <br>
PyPI: https://pypi.org/project/Airshare <br>

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Airshare.

```bash
$ pip install Airshare
```

If you have a non-Apple device, consider installing Avahi (for Linux) or Bonjour (for Windows) if you'd like to use Link-local Name Resolution (for the `.local` addresses).

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

or visit `http://noobmaster.local` in the browser to download.

You can also `import airshare` in any Python program. Visit the documentation for detailed usage instructions.

## Known Issues

* Link-local Name Resolution (for the `.local` addresses) on non-Apple devices requires Avahi (on Linux) or Bonjour (on Windows). Chances are you already have them, but if you don't, do check the web on how to install them.

* Link-local Name Resolution does not work on Android phones. This is because Android browsers do not have inbuilt Multicast-DNS service discovery.

* Multiple progress bars for concurrent file uploads using `tqdm` may not work as intended on some terminals, refer to the `tqdm` documentation for more details.

* Using <kbd>Ctrl</kbd> + <kbd>C</kbd> on Windows, with Python < 3.8, does not terminate the `asyncio` event loop. Use <kbd>Ctrl</kbd> + <kbd>Break</kbd> instead. If you do not have a <kbd>Break</kbd> or <kbd>Pause</kbd> key, some other combinations may work including <kbd>Ctrl</kbd> + <kbd>Fn</kbd> + <kbd>B</kbd> (check the web for solutions).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://github.com/KuroLabs/Airshare/blob/master/LICENSE.md) - Copyright (c) 2020 [Kandavel A](http://github.com/AK5123), [Mohanasundar M](https://github.com/mohanpierce99), [Nanda H Krishna](https://github.com/nandahkrishna)

## Acknowledgements
The Airshare logo was designed by [Siddique](https://dribbble.com/thesideeq).

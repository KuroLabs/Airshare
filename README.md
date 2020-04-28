<h1 align="center">
  <br>
  <img src="https://raw.githubusercontent.com/KuroLabs/Airshare/master/assets/Airshare.svg" alt="Airshare" width="100">
  <br>
  <br>
  <span>Airshare</span>
  <br>
  <br>
  <img alt="PyPI" src="https://img.shields.io/pypi/v/Airshare">
  <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/Airshare">
  <img alt="PyPI - License" src="https://img.shields.io/pypi/l/Airshare">
</h1>

<h4 align="center">An easy way to share content in a local network using Multicast DNS.</h4>

<p align="justify"><b>Airshare</b> is a Python-based CLI tool and module that lets you transfer data between two machines in a local network, P2P, using Multicast DNS. It also opens an HTTP gateway for other non-CLI external interfaces. It works completely offline! Built with aiohttp and zeroconf.</p>

## Important Links

Source Code: https://github.com/KuroLabs/Airshare
Bug Reports: https://github.com/KuroLabs/Airshare/issues
Documentation: https://airshare.rtfd.io
PyPI: https://pypi.org/project/Airshare

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Airshare.

```bash
$ pip install Airshare
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

or visit `http://noobmaster.local` in the browser to download.

You can also `import airshare` in any Python program. Visit the documentation for detailed usage instructions.

## Known Issues

* The QR Code feature is not available on Windows. Terminals on Windows are unable to render QR Codes despite our extensive attempts and tests - let us know if you have a solution!

* Link-local Name Resolution, for example, `http://noobmaster.local`, does not work on Android phones. This is because Android browsers do not have inbuilt Multicast-DNS service discovery.

* Non-Apple devices may require Avahi (on Linux) or Bonjour (on Windows) for Link-local Name Resolution.

* Multiple progress bars for concurrent file uploads using `tqdm` may not work as intended on some terminals, refer to the `tqdm` documentation for more details.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://github.com/KuroLabs/Airshare/blob/master/LICENSE.md) - Copyright (c) 2020 [Kandavel A](http://github.com/AK5123), [Mohanasundar M](https://github.com/mohanpierce99), [Nanda H Krishna](https://github.com/nandahkrishna)

## Acknowledgements
The Airshare logo was designed by [Siddique](https://dribbble.com/thesideeq).

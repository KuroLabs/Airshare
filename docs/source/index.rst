.. Airshare documentation master file, created by
   sphinx-quickstart on Wed Apr 22 02:37:05 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Airshare
========

.. toctree::
   :hidden:

   Home <self>

.. raw:: html

   <br/>

.. image:: https://img.shields.io/pypi/v/Airshare
   :target: https://pypi.org/project/Airshare
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/Airshare
   :target: https://pypi.org/project/Airshare
   :alt: Python Version Support

.. image:: https://img.shields.io/pypi/l/Airshare
   :target: https://github.com/KuroLabs/Airshare/blob/master/LICENSE.md
   :alt: License

.. image:: https://readthedocs.org/projects/airshare/badge/?version=latest
   :target: https://airshare.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. raw:: html

   <br/>

.. raw:: html

   <br/>

What is Airshare?
-----------------

Airshare is a Python-based CLI tool and module that lets you transfer data
between two machines in a local network, P2P, using Multicast-DNS. It also
opens an HTTP gateway for other non-CLI external interfaces. It works
completely offline! Built with aiohttp and zeroconf.

Features
--------

* Blazing fast content transfer within a local network.
* Lets you transfer plain text, send from or receive into your clipboard.
* Supports transfer of multiple files, directories and large files - content is sent chunk by chunk and never read into memory entirely.
* Lets you send files whose paths have been copied into the clipboard (more details in the docs).
* Cross-platform, works on Linux, Windows and Mac (CLI and Web Interface), and also supports mobile (Web Interface).
* Uses Multicast-DNS service registration and discovery - so you can access content with human-readable code words.
* Can be used as a module in other Python programs.

Important Links
---------------

* Source Code: https://github.com/KuroLabs/Airshare
* Bug Reports: https://github.com/KuroLabs/Airshare/issues
* Documentation: https://airshare.rtfd.io
* PyPI: https://pypi.org/project/Airshare

Installation
------------

Use the package manager `pip <https://pip.pypa.io/en/stable/>`__ to
install Airshare.

.. code:: bash

   $ pip install Airshare

If you have a non-Apple device, consider installing Avahi (for Linux) or Bonjour (for Windows) if you'd like to use Link-local Name Resolution (for the ``.local`` addresses).

CLI Tool Reference
------------------

.. toctree::
   :maxdepth: 2

   cli

Module Reference
----------------

.. toctree::
   :maxdepth: 2

   module

Examples
--------

.. toctree::
   :maxdepth: 2

   examples

Known Issues
------------

* Link-local Name Resolution (for the ``.local`` addresses) on non-Apple devices requires Avahi (on Linux) or Bonjour (on Windows). Chances are you already have them, but if you don't, do check the web on how to install them.
* Link-local Name Resolution does not work on Android phones. This is because Android browsers do not have inbuilt Multicast-DNS service discovery. For this reason, we included QR Code support, for you to visit the URLs easily.
* You may have to open up port 80 on your system (in Firewall settings) if not already open - Airshare uses port 80 by default.
* Multiple progress bars for concurrent file uploads using ``tqdm`` may not work as intended on some terminals, refer to the ``tqdm`` documentation for more details.

Contributing
------------

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

License
-------

Airshare is licensed under the terms of the MIT License.

Airshare is the joint work of  `Kandavel A <http://github.com/AK5123>`__,
`Mohanasundar M <https://github.com/mohanpierce99>`__ and `Nanda H
Krishna <https://github.com/nandahkrishna>`__.

.. literalinclude:: ../../LICENSE.md
   :language: text

Acknowledgements
----------------

The Airshare logo was designed by
`Siddique <https://dribbble.com/thesideeq>`__.

The Airshare GIF was designed by
`Anam Saatvik <https://github.com/kalki7>`__.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

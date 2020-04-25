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

.. image:: https://img.shields.io/pypi/pyversions/Airshare

.. image:: https://img.shields.io/pypi/l/Airshare

.. raw:: html

   <br/>

.. raw:: html

   <br/>

What is Airshare?
-----------------

Airshare is a Python-based CLI tool and module that lets you transfer data
between two machines in a local network, P2P, using Multicast DNS. It also
opens an HTTP gateway for other non-CLI external interfaces. It works
completely offline! Built with aiohttp and zeroconf.

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

   pip install Airshare

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

* The QR Code feature is not available on Windows. Terminals on Windows are unable to render QR Codes despite our extensive attempts and tests - let us know if you have a solution!
* Link-local Name Resolution, for example, ``http://noobmaster.local``, does not work on Android phones. This is because Android browsers do not have inbuilt Multicast-DNS service discovery.
* Non-Apple devices may require Avahi (on Linux) or Bonjour (on Windows) for Link-local Name Resolution.
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

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

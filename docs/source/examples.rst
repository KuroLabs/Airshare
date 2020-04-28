Examples
========

CLI
---

Serving a file,

.. code:: bash

   $ airshare noobmaster file.ext

Serving multiple files or directories,

.. code:: bash

   $ airshare noobmaster file1.ext file2.ext dir1 ../dir2

Serving text,

.. code:: bash

   $ airshare noobmaster -t "Some text here."

Serving clipboard text,

.. code:: bash

   $ airshare -cs noobmaster

Serving files whose paths have been copied to the clipboard,

.. code:: bash

   $ airshare -fp noobmaster

Uploading files,

.. code:: bash

   $ airshare -u noobmaster file1.ext dir2 file2.ext

Uploading files whose paths have been copied to the clipboard,

.. code:: bash

   $ airshare -u -fp noobmaster

Receiving a file or text,

.. code:: bash

   $ airshare noobmaster

Receiving file uploads,

.. code:: bash

   $ airshare -u noobmaster

Receiving a file or text and copying content to clipboard,

.. code:: bash

   $ airshare -cr noobmaster

Module
------

.. literalinclude:: _static/module_examples.txt
   :language: python

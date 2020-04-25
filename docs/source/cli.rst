Airshare CLI Tool
=================

Usage
-----

.. literalinclude:: _static/cli_usage.txt
   :language: text

Flags
-----

* The ``-t`` flag can be used to send text using airshare, except to a receiving server.

  .. code:: bash

     airshare noobmaster -t "I'm still worthy!"

* The ``-u`` flag opens an upload endpoint to receive files from multiple users who initiate a send with the same flag. This is useful to receive files from devices without CLI support - they may simply visit the endpoint URL from any browser.

  At the receiver,

  .. code:: bash
  
     airshare -u noobmaster

  At the sender,

  .. code:: bash

     airshare -u noobmaster file.txt

* The ``-fp`` flag allows users to copy file or directory paths from the Finder or File Explorer and send them. Useful for selecting multiple files instead of typing file paths.

  Select required files and use the following shortcuts to copy file paths.

  For Mac,

  .. raw:: html

     <kbd>Command</kbd> + <kbd>Option</kbd> + <kbd>C</kbd>

  For Windows,

  .. raw:: html

     <kbd>Shift</kbd> + <img src="https://raw.githubusercontent.com/KuroLabs/Airshare/master/assets/RightClick.svg" alt="Right Click" width="20">  and select  <kbd>Copy as Path</kbd>

  For Linux,

  .. raw:: html

     <kbd>Ctrl</kbd> + <kbd>C</kbd>

  To send the files,

  .. code:: bash

     airshare -fp noobmaster

* The ``-cs`` flag allows users to directly send the clipboard contents as text.

  To send,

  .. code:: bash

     airshare -cs noobmaster

* The ``-cr`` flag allows users to copy the data received if clipboard compatible. 

  To receive,

  .. code:: bash

     airshare -cr noobmaster

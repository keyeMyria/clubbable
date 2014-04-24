clubbable
=========

A web application for managing newsletters and image galleries for a club.

Requirements
------------

Python library requirements are listed in requirements.txt.

Requirements include Pillow, which in turn will need Python headers installed
(normally available in the python-dev or python-devel package in your operating
system's software repository) and libraries for image formats you want to
support; at least JPEG, maybe PNG. e.g. ::

    $ sudo apt-get install python-dev libjpeg-dev libpng12-dev

If you want to import data from a Microsoft Access database, *clubbable*'s
importmdb.py utility requires mdbtools_. It is available from the
mdbtools_ homepage.

You might also be able to install it from your operating system's software
repository. e.g. ::

    $ sudo apt-get install mdbtools


Documentation
-------------

Further documentation can be found in the "doc" directory.


.. _mdbtools: http://mdbtools.sourceforge.net/

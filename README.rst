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


Importing from Microsoft Access
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to import data from a Microsoft Access database, you will need
mdbtools_. It is available from the mdbtools_ homepage. You might also be able
to install it from your operating system's software repository. e.g. ::

    $ sudo apt-get install mdbtools


Importing from a legacy MySQL database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*clubbable* was build to replace a legacy web application, and data needed to
be imported from the legacy database. That was done with the
Python-3-compatible mysqlclient library. It needs the libmysqlclient
development package. On Debian-like operating systems, you can use ::

    $ sudo apt-get install libmysqlclient-dev


Documentation
-------------

Further documentation can be found in the "doc" directory.


.. _mdbtools: http://mdbtools.sourceforge.net/

Documentation for Developers
============================

*clubbable* is an open source web application for managing newsletters and
image galleries for a club. It is licensed under the `GNU Affero GPL`_. You are
welcome to `fork the project on GitHub`_.


Installation
------------

Installation for production has fewer requirements than for development. For
production you just need the requirements given in requirements.txt. ::

    $ pip install -r requirements.txt

For development, you need Attest >= 0.6, which is not yet available on PyPI.
Use GitHub. And install the rest of the development requirements. ::

    $ pip install git+https://github.com/dag/attest.git
    $ pip install -r requirements_dev.txt


.. _GNU Affero GPL: http://www.gnu.org/licenses/agpl-3.0.html
.. _fork the project on GitHub: https://github.com/kaapstorm/clubbable

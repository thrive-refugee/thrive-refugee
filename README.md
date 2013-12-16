thrive-refugee
==============

A refugee management system in Django.

For Developers
==============

Requirements
------------

* Python 2.7 http://www.python.org/download/releases/2.7/#download
* GNU Make:
    * Windows: http://cygwin.com/install.html
    * Mac: https://developer.apple.com/xcode
    * Linux: http://www.gnu.org/software/make (likely already installed)
* virtualenv: https://pypi.python.org/pypi/virtualenv

Environment
-----------

Create a virtualenv:

    make

Run the server and open a web browser:

   make launch  # Ctrl+C to stop the server

Restart a stopped server:

    make run  # Ctrl+C to stop the server

Run static analysis and tests:

    make pep8
    make pylint
    make test

thrive-refugee
==============

A refugee management system in Django.

[![Build Status](http://img.shields.io/travis/thrive-refugee/thrive-refugee/master.svg)](https://travis-ci.org/thrive-refugee/thrive-refugee)
[![Coverage Status](http://img.shields.io/coveralls/thrive-refugee/thrive-refugee/master.svg)](https://coveralls.io/r/thrive-refugee/thrive-refugee)
[![Scrutinizer Code Quality](http://img.shields.io/scrutinizer/g/thrive-refugee/thrive-refugee.svg)](https://scrutinizer-ci.com/g/thrive-refugee/thrive-refugee/?branch=master)

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

    $ make env

Run the server and open a web browser:

    $ make launch  # login: admin:password, ctrl+c to stop the server

Restart a stopped server:

    $ make run  # ctrl+c to stop the server

Run static analysis and tests:

    $ make pep8
    $ make pylint
    $ make test
    $ make ci  # all targets invoked during continous integration 

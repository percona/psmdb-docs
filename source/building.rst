.. _building:

==================================
Building Pecona Server for MongoDB
==================================

To build Pecona Server for MongoDB, you will need:

* One of the following C++ compilers:
    * GCC 4.8.2 or newer
    * Clang 3.4 (or Apple XCode 5.1.1 Clang) or newer
    * Visual Studio 2013 Update 2 or newer
* Python 2.7
* SCons 2.3

MongoDB Tools
-------------

The MongoDB command-line tools (``mongodump``, ``mongorestore``, ``mongoimport``, ``mongoexport``, etc) have been rewritten in `Go <http://golang.org/>`_ and are no longer included in this repository.

The source for the tools is now available at `Github <https://github.com/mongodb/mongo-tools>`_.

SCons
-----

For detailed information about building, please see the `build manual <http://www.mongodb.org/about/contributors/tutorial/build-mongodb-from-source/>`_

If you want to build everything (mongod, mongo, tests, etc):

.. code-block:: bash

    $ scons all

If you only want to build the database:

.. code-block:: bash

    $ scons

To install:

.. code-block:: bash

    $ scons --prefix=/opt/mongo install

Please note that prebuilt binaries are available from `MongoDB Downloads <http://www.mongodb.org/downloads>`_ and may be the easiest way to get started.

SCons Targets
-------------

* mongod
* mongos
* mongo
* core (includes mongod, mongos, mongo)
* all

Windows
-------

See the `Windows build manual <http://www.mongodb.org/about/contributors/tutorial/build-mongodb-from-source/#windows-specific-instructions>`_

Build requirements:

* Visual Studio 2013 Update 2 or newer
* Python 2.7, ActiveState ActivePython 2.7.x Community Edition for Windows is recommended
* SCons

Or download a prebuilt binary for Windows from `MongoDB <www.mongodb.org>`_.

Debian/Ubuntu
-------------

To install dependencies on Debian or Ubuntu systems:

.. code-block:: bash

    # aptitude install scons build-essential
    # aptitude install libboost-filesystem-dev libboost-program-options-dev libboost-system-dev libboost-thread-dev

To run tests as well, you will need PyMongo:

.. code-block:: bash

    # aptitude install python-pymongo

Then build as usual:

.. code-block:: bash

    $ scons all

OS X
----

Using `Homebrew <http://brew.sh>`_:

.. code-block:: bash

    $ brew install mongodb

Using `MacPorts <http://www.macports.org>`_:

.. code-block:: bash

    $ sudo port install mongodb

FreeBSD
-------

Install the following ports:

  * devel/libexecinfo
  * devel/scons
  * lang/gcc
  * lang/python

Optional components if you want to use system libraries instead of the libraries included with MongoDB:

  * archivers/snappy
  * lang/v8
  * devel/boost
  * devel/pcre

OpenBSD
-------
Install the following ports:

  * devel/libexecinfo
  * devel/scons
  * lang/gcc
  * lang/python

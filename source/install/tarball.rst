.. _tarball:

================================================================================
Installing Percona Server for MongoDB from Binary Tarball
================================================================================

You can find links to the binary tarballs under the *Generic Linux* menu item on the `Percona website`_

There are two tarballs available:

- ``percona-server-mongodb-<version>-x86_64.glibc2.17.tar.gz`` is the general tarball, compatible with any `supported operating system <https://www.percona.com/services/policies/percona-software-support-lifecycle#mongodb>`_ except Ubuntu 22.04.
- ``percona-server-mongodb-<version>-x86_64.glibc2.35.tar.gz`` is the tarball for Ubuntu 22.04.  

Preconditions
=============

The following packages are required for the installation. 

.. tabs::

   .. tab:: On Debian / Ubuntu

      * ``libcurl4``
      * ``libsasl2-modules``
      * ``libsasl2-modules-gssapi-mit``
        
   .. tab:: On Red Hat Enterprise Linux and derivatives

      * ``libcurl``
      * ``cyrus-sasl-gssapi``
      * ``cyrus-sasl-plain``


Check that they are installed in your operating system. Otherwise install them.

Procedure
=========

1. Fetch and extract the correct binary tarball. For example, if you
   are running Debian 10 ("buster"):

   .. code-block:: bash

      $ wget https://downloads.percona.com/downloads/percona-server-mongodb-4.4/percona-server-mongodb-4.4.15-15/binary/tarball/percona-server-mongodb-4.4.15-15-x86_64.glibc2.17.tar.gz
      $ tar -xf percona-server-mongodb-4.4.15-15-x86_64.glibc2.17.tar.gz

#. Add the location of the binaries to the ``PATH`` variable: 

   .. code-block:: bash

      $ export PATH=~/percona-server-mongodb-4.4.15-15/bin/:$PATH

#. Create the default data directory::

   $ mkdir -p /data/db
   
#. Make sure that you have read and write permissions for the data
   directory and run |mongod|.

.. include:: ../.res/url.txt
.. include:: ../.res/replace.program.txt

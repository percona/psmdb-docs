.. _tarball:

================================================================================
Installing Percona Server for MongoDB from Binary Tarball
================================================================================

You can find links to the binary tarballs under the *Generic Linux* menu item on the `Percona website`_

Preconditions
=============

The following libraries are required for the installation. 

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


1. Fetch and extract the binary tarball. For example, if you
   are running Debian 10 ("buster"), use the following command:

   .. code-block:: bash

      $ wget https://www.percona.com/downloads/percona-server-mongodb-6.0/percona-server-mongodb-6.0.2-1/binary/tarball/percona-server-mongodb-6.0.2-1-x86_64.glibc2.17.tar.gz\
      $ wget https://www.percona.com/downloads/percona-server-mongodb-6.0/percona-server-mongodb-6.0.2-1/binary/tarball/percona-mongodb-mongosh-1.6.0-x86_64.tar.gz

#. Extract the tarballs:
   
   .. code-block:: bash 

      $ tar -xf percona-server-mongodb-6.0.2-1-x86_64.glibc2.17.tar.gz
      $ tar -xf percona-mongodb-mongosh-1.6.0-x86_64.tar.gz

#. Add the location of the binaries to the ``PATH`` variable: 

   .. code-block:: bash

      $ export PATH=~/percona-server-mongodb-6.0.2-1/bin/:~/percona-mongodb-mongosh-1.6.0/bin/:$PATH

#. Create the default data directory:
   
   .. code-block:: bash

      $ mkdir -p /data/db
   
#. Make sure that you have read and write permissions for the data
   directory and run |mongod|.

.. include:: ../.res/url.txt
.. include:: ../.res/replace.program.txt

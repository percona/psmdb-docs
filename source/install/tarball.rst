.. _tarball:

================================================================================
Installing Percona Server for MongoDB from Binary Tarball
================================================================================

You can find links to the binary tarball under the *Generic Linux* menu item on the `Percona website`_

There are two tarballs available:

- ``percona-server-mongodb-4.0.20-14-x86_64.glibc2.17.tar.gz`` is the general tarball, compatible with any operation system but for Centos 6.
- ``percona-server-mongodb-4.0.20-14-x86_64.glibc2.12.tar.gz`` is the tarball for Centos 6.  

1. Fetch and extract the correct binary tarball. For example, if you
   are running Debian 10 ("buster"):

   .. code-block:: bash

      $ wget https://www.percona.com/downloads/percona-server-mongodb-4.0/percona-server-mongodb-4.0.20-14/binary/tarball/percona-server-mongodb-4.0.20-14-x86_64.glibc2.17.tar.gz\
      $ tar -xf percona-server-mongodb-4.0.20-14-x86_64.glibc2.17.tar.gz

#. Add the location of the binaries to the ``PATH`` variable: 
   
   .. code-block:: bash
   
       export PATH=~/percona-server-mongodb-4.0.20-14/bin/:$PATH`

#. Create the default data directory: 
   
   .. code-block:: bash

      mkdir -p /data/db
      
#. Make sure that you have read and write permissions for the data
   directory and run |mongod|.

.. include:: ../.res/url.txt
.. include:: ../.res/replace.program.txt

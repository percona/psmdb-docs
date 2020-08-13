.. _tarball:

=========================================================
Installing Percona Server for MongoDB from Binary Tarball
=========================================================

You can find the link to the binary tarball under the *Generic Linux* menu item on the 
`Percona Server for MongoDB download page <https://www.percona.com/downloads/percona-server-mongodb-3.6/>`_.

1. Fetch and extract the correct binary tarball for your operating system. For example, if you are running Debian 10 ("buster"): 
   
   .. code-block:: bash

      wget https://www.percona.com/downloads/percona-server-mongodb-3.6/percona-server-mongodb-3.6.19-7.0/binary/tarball/percona-server-mongodb-3.6.19-7.0-buster-x86_64.tar.gz 
      tar -xf percona-server-mongodb-3.6.19-7.0-buster-x86_64.tar.gz

2. Add the location of the binaries to the ``PATH`` variable:

   .. code-block:: bash

      export PATH=~/percona-server-mongodb-3.6.19-7.0/bin/:$PATH

4. Create the default data directory:

   .. code-block:: bash

      mkdir -p /data/db

5. Make sure that you have read and write permissions for the data directory
   and run ``mongod``.


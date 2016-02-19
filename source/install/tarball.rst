.. _tarball:

=========================================================
Installing Percona Server for MongoDB from Binary Tarball
=========================================================

You can find links to the binary tarballs from the `Percona Server for MongoDB download page <https://www.percona.com/downloads/percona-server-for-mongodb/>`_.

1. Fetch and extract the correct binary tarball. For example, if you are running Debian 8 ("jessie"):

   .. code-block:: bash
    
      $ wget https://www.percona.com/downloads/percona-server-for-mongodb/percona-server-for-mongodb-3.0.5/binary/debian/jessie/x86_64/percona-server-mongodb-3.0.5-rel0.7rc-r42b00da-jessie-x86_64-bundle.tar
      $ tar xfz percona-server-mongodb-3.0.5-rel0.7rc-r42b00da-jessie-x86_64-bundle.tar

2. Copy the extracted binaries to the target directory:
   
   .. code-block:: bash

      $ mkdir psmdb
      $ cp -r -n percona-server-mongodb-3.0.5-rel0.7rc-r42b00da-jessie-x86_64-bundle/ psmdb

3. Add the location of the binaries to the ``PATH`` variable:
   
   .. code-block:: bash

      $ export PATH psmdb/bin:$PATH

4. Create the default data directory:

   .. code-block:: bash

      $ mkdir -p /data/db

5. Make sure that you have read and write permissions for the data directory and run ``mongod``.

   .. note:: By default, |Percona Server for MongoDB| starts with the MMAPv1 storage engine (standard engine in MongoDB). If you want to run with PerconaFT, specify the ``--storageEngine=PerconaFT`` option on the command line when running ``mongod``, or set the ``storage.engine`` option in the configuration file. For more information, see :ref:`switch-storage-engines`.


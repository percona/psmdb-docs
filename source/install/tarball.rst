.. _tarball:

================================================================================
Installing Percona Server for MongoDB from Binary Tarball
================================================================================

You can find links to the binary tarballs from the `Percona website`_

1. Fetch and extract the correct binary tarball. For example, if you
   are running Debian 8 ("jessie"):

   .. code-block:: bash

      $ wget https://www.percona.com/downloads/percona-server-mongodb-4.0/\
      percona-server-mongodb-4.0.4-1/binary/debian/jessie/x86_64/\
      percona-server-mongodb-4.0.4-1-ra1cb178-jessie-x86_64-bundle.tar
      $ tar xfz percona-server-mongodb-4.0.4-1-ra1cb178-jessie-x86_64-bundle.tar

#. Copy the extracted binaries to the target directory, for example:

   .. code-block:: bash

      mkdir ~/psmdb
      cp -r -n percona-server-mongodb-4.0.4-1-ra1cb178-jessie-x86_64-bundle/bin ~/psmdb/

#. Add the location of the binaries to the ``PATH`` variable: :bash:`export PATH ~/psmdb/bin:$PATH`
#. Create the default data directory: :bash:`mkdir -p /data/db`
#. Make sure that you have read and write permissions for the data
   directory and run |mongod|.

.. include:: ../.res/url.txt
.. include:: ../.res/replace.program.txt

.. _switch_storage_engines:

Switching Storage Engines
=========================

By default, Percona Server for MongoDB runs with WiredTiger. You can select a
storage engine using the ``--storageEngine`` command-line option when you start
``mongod``. Alternatively, you can set the ``storage.engine`` option in the
configuration file (by default, :file:`/etc/mongod.conf`).

Data created by one storage engine is not compatible with other storage
engines, because each one has its own data model. When changing the storage
engine, you have to do one of the following:

* If you simply want to temporarily test a storage engine, change to a
  different data directory with the ``--dbpath`` command-line option:

  .. code-block:: bash

    $ service mongod stop
    $ mongod --storageEngine rocksdb --dbpath <dataDirForRocksDB>

  .. note::

    Make sure that the user running ``mongod`` has read and write
    permissons for the new data directory.

* If you want to permanently switch to a different storage engine and do not
  have any valuable data in your database, clean out the default data directory
  and edit the configuration file:

  .. code-block:: bash

    $ service mongod stop
    $ rm -rf /var/lib/mongodb/*
    $ sed -i '/engine: \*rocksdb/s/#//g' /etc/mongod.conf
    $ service mongod start

* If there is data that you want to migrate and make compatible with the new
  storage engine, use the ``mongodump`` and ``mongorestore`` utilities:

  .. code-block:: bash

    $ mongodump --out <dumpDir>
    $ service mongod stop
    $ rm -rf /var/lib/mongodb/*
    $ sed -i '/engine: \*rocksdb/s/#//g' /etc/mongod.conf
    $ service mongod start
    $ mongorestore <dumpDir>

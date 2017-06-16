.. _switch_storage_engines:

Switching Storage Engines
=========================

By default, |PSMDB| runs with WiredTiger_.
There is also the original MMAPv1_ storage engine,
as well as optional :ref:`inmemory` and :ref:`mongorocks` storage engines
to choose from.
Each one is designed for specific purposes and workloads.

You can select a storage engine
using the ``--storageEngine`` command-line option when you start ``mongod``.
Alternatively, you can set the ``storage.engine`` variable
in the configuration file (by default, :file:`/etc/mongod.conf`).

Data created by one storage engine is not compatible
with other storage engines, because each one has its own data model.
When changing the storage engine, you have to do one of the following:

* If you simply want to temporarily test a storage engine,
  you can change to a different data directory
  using the ``--dbpath`` command-line option:

  .. code-block:: bash

    $ service mongod stop
    $ mongod --storageEngine rocksdb --dbpath <dataDirForRocksDB>

  .. note:: Make sure that the user running ``mongod``
     has read and write permissons for the new data directory.

* If you want to permanently switch to a different storage engine
  and do not have any valuable data in your database,
  clean out the default data directory
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

Storage Engine Configuration Templates
======================================

The default configuration file provided with |PSMDB| (:file:`/etc/mongod.conf`)
contains templates for running any of the bundled storage engine.
The suggested values do not cover all cases,
but they are a good reference point to start customizing the configuration.
The following hints may help you:

* On very high volume systems,
  you may need to increase the maximum number of concurrent transactions
  for WiredTiger_ and :ref:`inmemory` (default is 128).
  These are controlled using the following MongoDB parameters:

  * ``wiredTigerConcurrentReadTransactions``
  * ``wiredTigerConcurrentWriteTransactions``

* On systems with more than roughly 24,000 collections running MMAPv1_,
  increase the ``storage.mmapv1.nsSize`` variable.

* Also for MMAPv1_ you can set ``storage.mmapv1.smallFiles`` to ``true``
  to use a smaller default file size,
  if you have a large number of databases
  that each holds a small amount of data.

* The ``storage.rocksdb.counters`` variable must be set to ``true``
  if you are running :ref:`mongorocks`
  and want to use `Percona Monitoring and Management
  <https://www.percona.com/software/database-tools/percona-monitoring-and-management>`_.

* The default maximum internal cache size that WiredTiger_ uses
  is the larger of either:

  * 50% of RAM minus 1 GB
  * 256 MB

* The default maximum internal cache size that :ref:`mongorocks` uses
  is 30% of RAM.


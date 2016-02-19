.. _perconaft:

========================
PerconaFT Storage Engine
========================

PerconaFT is a storage engine based on the Fractal Tree Index model, which is optimized for fast disk I/O. The Fractal Tree data structure contains buffers to temporarily store insertions. When a buffer is full, it is flushed to children nodes. This ensures that an I/O operation performs a lot of useful work when messages reach leaves on disk, instead of just a small write per I/O.

The PerconaFT storage engine is available in Percona Server for MongoDB along with the standard MongoDB engines (`MMAPv1 <https://docs.mongodb.org/manual/core/mmapv1/>`_ and `WiredTiger <https://docs.mongodb.org/manual/core/wiredtiger/>`_), as well as `MongoRocks <http://rocksdb.org>`_.

.. note:: MongoRocks is currently considered experimental.

To help you decide which is better for you, the table below lists features available in various storage engines:

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * -
     - MMAPv1
     - WiredTiger
     - MongoRocks
     - PerconaFT
   * - Available in MongoDB
     - YES
     - YES
     - NO
     - NO
   * - Document-level locking
     - NO
     - YES
     - YES
     - YES
   * - High compression
     - NO
     - YES
     - YES
     - YES
   * - Fast insertions
     - NO
     - NO
     - YES
     - YES
   * - Hot Backup
     - NO
     - NO
     - :ref:`YES <toku-backup>`
     - YES

.. note:: PerconaFT is not supported on 32-bit systems.

.. warning:: Transparent huge pages is a feature in newer Linux kernel versions that causes problems for the memory usage tracking calculations in PerconaFT and can lead to memory overcommit. If you have this feature enabled, PerconaFT will not start, and you should turn it off. If you want to run with transparent huge pages on, you can set an environment variable ``TOKU_HUGE_PAGES_OK=1``, but only do this for testing, and only with a small cache size.

.. contents::
  :local:
  :depth: 1

.. _switch-storage-engines:

Switching Storage Engines
=========================

By default, Percona Server for MongoDB runs with MMAPv1. You can select a storage engine using the ``--storageEngine`` command-line option when you start ``mongod``. Alternatively, you can set the ``storage.engine`` option in the configuration file (by default, :file:`/etc/mongod.conf`).

Data created by one storage engine is not compatible with other storage engines, because each one has its own data model. When changing the storage engine, you have to do one of the following:

* If you simply want to temporarily test a storage engine, change to a different data directory with the ``--dbpath`` command-line option:

  .. code-block:: bash

     $ service mongod stop
     $ mongod --storageEngine PerconaFT --dbpath <dataDirForPerconaFT>

  .. note:: Make sure that the user running ``mongod`` has read and write permissons for the new data directory.

* If you want to permanently switch to a different storage engine and do not have any valuable data in your database, clean out the default data directory and edit the configuration file:

  .. code-block:: bash

     $ service mongod stop
     $ rm -rf /var/lib/mongodb/*
     $ sed -i '/engine: \*PerconaFT/s/#//g' /etc/mongod.conf
     $ service mongod start

* If there is data that you want to migrate and make compatible with the new storage engine, use the ``mongodump`` and ``mongorestore`` utilities:

  .. code-block:: bash

     $ mongodump --out <dumpDir>
     $ service mongod stop
     $ rm -rf /var/lib/mongodb/*
     $ sed -i '/engine: \*PerconaFT/s/#//g' /etc/mongod.conf
     $ service mongod start
     $ mongorestore <dumpDir>

PerconaFT Options
=================

When running with the PerconaFT storage engine, you can configure the following options:

.. option:: --PerconaFTCollectionCompression

   :Default: zlib
   :Values: none, zlib, lzma, quicklz

   Specify the PerconaFT collection compression method.

.. option:: --PerconaFTCollectionFanout

   :Default: 16

   Specify the PerconaFT collection fanout.

.. option:: --PerconaFTCollectionPageSize

   :Default: 4 MB

   Specify the PerconaFT collection page size in bytes.

.. option:: --PerconaFTCollectionReadPageSize

   :Default: 64 KB

   Specify the PerconaFT collection read page size in bytes.

.. option:: --PerconaFTEngineCacheSize

   :Default: 0

   Specify the PerconaFT storage engine cache size in bytes.

.. option:: --PerconaFTEngineCleanerIterations

   :Default: 5

   Specify the number of PerconaFT storage engine cleaner iterations.

.. option:: --PerconaFTEngineCleanerPeriod

   :Default: 2

   Specify the PerconaFT storage engine cleaner period in seconds.

.. option:: --PerconaFTEngineCompressBuffersBeforeEviction

   :Default: false

   Specify whether the PerconaFT storage engine should compress buffers before eviction.
 
.. option:: --PerconaFTEngineDirectio

   :Default: false

   Specify whether the PerconaFT storage engine should use Direct I/O.

.. option:: --PerconaFTEngineFsRedzone

   :Default: 5

   Specify the PerconaFT storage engine filesystem redzone.

.. option:: --PerconaFTEngineJournalCommitInterval

   :Default: 100

   Specify the PerconaFT storage engine journal commit interval in milliseconds.

.. option:: --PerconaFTEngineLockTimeout

   :Default: 100

   Specify the PerconaFT storage engine lock wait timeout in milliseconds.

.. option:: --PerconaFTEngineLocktreeMaxMemory

   :Default: 0

   Specify the PerconaFT storage engine locktree size in bytes.

.. option:: --PerconaFTEngineLogDir

   :Default: 

   Specify the directory for the PerconaFT storage engine transaction log.

.. option:: --PerconaFTEngineNumCachetableBucketMutexes

   :Default: 1 048 576

   Specify the number of PerconaFT storage engine num cachetable bucket mutexes.

.. option:: --PerconaFTIndexCompression

   :Default: zlib
   :Values: none, zlib, lzma, quicklz

   Specify the PerconaFT index compression method.

.. option:: ---PerconaFTIndexFanout

   :Default: 16

   Specify the PerconaFT index fanout.

.. option:: --PerconaFTIndexPageSize

   :Default: 4 MB

   Specify the PerconaFT index page size in bytes.

.. option:: --PerconaFTIndexReadPageSize

   :Default: 64 KB

   Specify the PerconaFT index read page size in bytes.


.. _perconaft:

========================
PerconaFT Storage Engine
========================

PerconaFT is a storage engine based on the Fractal Tree Index model,
which is optimized for fast disk I/O.
The Fractal Tree data structure contains buffers
to temporarily store insertions.
When a buffer is full, it is flushed to children nodes.
This ensures that an I/O operation performs a lot of useful work
when messages reach leaves on disk, instead of just a small write per I/O.

.. contents::
  :local:
  :depth: 1

The PerconaFT storage engine is available in Percona Server for MongoDB
along with the standard MongoDB engines
(`MMAPv1 <https://docs.mongodb.org/manual/core/mmapv1/>`_
and `WiredTiger <https://docs.mongodb.org/manual/core/wiredtiger/>`_),
as well as `MongoRocks <http://rocksdb.org>`_.

.. note:: PerconaFT has been deprecated
   and will be removed in future releases.

To help you decide which is better for you,
the table below lists features available in various storage engines:

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
     - YES
     - :ref:`YES <toku-backup>`

.. note:: PerconaFT is not supported on 32-bit systems.

.. warning:: Transparent huge pages is a feature in newer Linux kernel versions
   that causes problems for the memory usage tracking calculations
   in PerconaFT and can lead to memory overcommit.
   If you have this feature enabled, PerconaFT will not start,
   and you should turn it off.
   If you want to run with transparent huge pages on,
   you can set an environment variable ``TOKU_HUGE_PAGES_OK=1``,
   but only do this for testing, and only with a small cache size.

.. _switch-storage-engines:

Switching Storage Engines
=========================

As of version 3.2, Percona Server for MongoDB runs with WiredTiger by default.
You can select a storage engine using the ``--storageEngine``
command-line option when you start ``mongod``.
Alternatively, you can set the ``storage.engine`` option
in the configuration file (by default, :file:`/etc/mongod.conf`).

Data created by one storage engine is not compatible
with other storage engines, because each one has its own data model.
When changing the storage engine, you have to do one of the following:

* If you simply want to temporarily test a storage engine,
  change to a different data directory
  with the ``--dbpath`` command-line option:

  .. code-block:: bash

     $ service mongod stop
     $ mongod --storageEngine PerconaFT --dbpath <dataDirForPerconaFT>

  .. note:: Make sure that the user running ``mongod``
     has read and write permissons for the new data directory.

* If you want to permanently switch to a different storage engine
  and do not have any valuable data in your database,
  clean out the default data directory and edit the configuration file:

  .. code-block:: bash

     $ service mongod stop
     $ rm -rf /var/lib/mongodb/*
     $ sed -i '/engine: \*PerconaFT/s/#//g' /etc/mongod.conf
     $ service mongod start

* If there is data that you want to migrate
  and make compatible with the new storage engine,
  use the ``mongodump`` and ``mongorestore`` utilities:

  .. code-block:: bash

     $ mongodump --out <dumpDir>
     $ service mongod stop
     $ rm -rf /var/lib/mongodb/*
     $ sed -i '/engine: \*PerconaFT/s/#//g' /etc/mongod.conf
     $ service mongod start
     $ mongorestore <dumpDir>

.. _configure-perconaft:

Configuring PerconaFT
=====================

You can configure the PerconaFT storage engine
using either command-line options
or corresponding parameters in the :file:`/etc/mongod.conf` file.
The configuration file is formatted in YAML. For example:

.. code-block:: text

 storage:
   engine: PerconaFT
   PerconaFT:
     engineOptions:
       cacheSize: 53687091200
       journalCommitInterval: 100
     collectionOptions:
       compression: zlib
     indexOptions:
       compression: zlib

Setting parameters in the previous example configuration file
is the same as starting the ``mongod`` daemon with the following options:

.. code-block:: bash

 $ mongod --storageEngine PerconaFT \
   --PerconaFTEngineCacheSize 53687091200 \
   --PerconaFTEngineJournalCommitInterval 100 \
   --PerconaFTCollectionCompression zlib \
   --PerconaFTIndexCompression zlib

.. seealso::

   YAML Specification
      https://yaml.org/spec/1.2/spec.html

The following options are available
(with corresponding YAML configuration file parameters):

.. option:: --PerconaFTCollectionCompression

   :Config: ``storage.PerconaFT.collectionOptions.compression``
   :Default: ``zlib``
   :Values: ``none``, ``zlib``, ``lzma``, ``quicklz``

   Specifies the PerconaFT collection compression method.

.. option:: --PerconaFTCollectionFanout

   :Config: ``storage.PerconaFT.collectionOptions.fanout``
   :Default: ``16``

   Specifies the PerconaFT collection fanout.

.. option:: --PerconaFTCollectionPageSize

   :Config: ``storage.PerconaFT.collectionOptions.pageSize``
   :Default: ``4194304`` (4 MiB)

   Specifies the PerconaFT collection page size in bytes.

.. option:: --PerconaFTCollectionReadPageSize

   :Config: ``storage.PerconaFT.collectionOptions.readPageSize``
   :Default: ``65536`` (64 KiB)

   Specifies the PerconaFT collection read page size in bytes.

.. option:: --PerconaFTEngineCacheSize

   :Config: ``storage.PerconaFT.engineOptions.cacheSize``
   :Default: ``0``

   Specifies the PerconaFT storage engine cache size in bytes.

.. option:: --PerconaFTEngineCleanerIterations

   :Config: ``storage.PerconaFT.engineOptions.cleanerIterations``
   :Default: ``5``

   Specifies the number of PerconaFT storage engine cleaner iterations.

.. option:: --PerconaFTEngineCleanerPeriod

   :Config: ``storage.PerconaFT.engineOptions.cleanerPeriod``
   :Default: ``2``

   Specifies the PerconaFT storage engine cleaner period in seconds.

.. option:: --PerconaFTEngineCompressBuffersBeforeEviction

   :Config: ``storage.PerconaFT.engineOptions.compressBuffersBeforeEviction``
   :Default: ``false``

   Specifies whether the PerconaFT storage engine
   should compress buffers before eviction.

.. option:: --PerconaFTEngineDirectio

   :Config: ``storage.PerconaFT.engineOptions.directio``
   :Default: ``false``

   Specifies whether the PerconaFT storage engine should use Direct I/O.

.. option:: --PerconaFTEngineFsRedzone

   :Config: ``storage.PerconaFT.engineOptions.fsRedzone``
   :Default: ``5``

   Specifies the PerconaFT storage engine filesystem redzone.

.. option:: --PerconaFTEngineJournalCommitInterval

   :Config: ``storage.PerconaFT.engineOptions.journalCommitInterval``
   :Default: ``100``

   Specifies the PerconaFT storage engine
   journal commit interval in milliseconds.

.. option:: --PerconaFTEngineLockTimeout

   :Config: ``storage.PerconaFT.engineOptions.lockTimeout``
   :Default: ``100``

   Specifies the PerconaFT storage engine lock wait timeout in milliseconds.

.. option:: --PerconaFTEngineLocktreeMaxMemory

   :Config: ``storage.PerconaFT.engineOptions.locktreeMaxMemory``
   :Default: ``0``

   Specifies the PerconaFT storage engine locktree size in bytes.

.. option:: --PerconaFTEngineLogDir

   :Config: ``storage.PerconaFT.engineOptions.logDir``
   :Default:

   Specifies the directory for the PerconaFT storage engine transaction log.

.. option:: --PerconaFTEngineNumCachetableBucketMutexes

   :Config: ``storage.PerconaFT.engineOptions.numCachetableBucketMutexes``
   :Default: ``1048576``

   Specifies the number of PerconaFT storage engine
   num cachetable bucket mutexes.

.. option:: --PerconaFTIndexCompression

   :Config: ``storage.PerconaFT.indexOptions.compression``
   :Default: ``zlib``
   :Values: ``none``, ``zlib``, ``lzma``, ``quicklz``

   Specifies the PerconaFT index compression method.

.. option:: ---PerconaFTIndexFanout

   :Config: ``storage.PerconaFT.indexOptions.fanout``
   :Default: ``16``

   Specifies the PerconaFT index fanout.

.. option:: --PerconaFTIndexPageSize

   :Config: ``storage.PerconaFT.indexOptions.pageSize``
   :Default: ``4194304`` (4 MiB)

   Specifies the PerconaFT index page size in bytes.

.. option:: --PerconaFTIndexReadPageSize

   :Config: ``storage.PerconaFT.indexOptions.readPageSize``
   :Default: ``65536`` (64 KiB)

   Specifies the PerconaFT index read page size in bytes.


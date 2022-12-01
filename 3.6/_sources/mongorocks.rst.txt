.. _mongorocks:

==========
MongoRocks
==========

.. important:: **MongoRocks is deprecated in Percona Server for MongoDB 3.6.**

MongoRocks is deprecated in |PSMDB| 3.6 and it will be fully removed in the
next major version of |PSMDB|. Feature compatibility version is set to 3.4 when
using |PSMDB| 3.6 with MongoRocks, so 3.6 features, such as retryable writes
and causal consistency, cannot be used. Additionally, read concern majority may
produce unreliable results.

If you are using MongoRocks with |PSMDB| 3.4 or older, we strongly encourage
you to migrate from MongoRocks to WiredTiger before upgrading to |PSMDB| 3.6.
Instructions on how to change storage engines are located in this Percona blog
post: https://www.percona.com/blog/2017/03/07/how-to-change-mongodb-storage-engines-without-downtime/.

If you install |PSMDB| 3.6 with the RocksDB storage engine, you will receive
the following error message when trying to start mongod:

.. code-block:: text

  [ERROR] There are known issues with MongoDB 3.6 and MongoRocks. To learn about these issues and how to enable MongoRocks with Percona Server for MongoDB 3.6, please read https://www.percona.com/doc/percona-server-for-mongodb/3.6/mongorocks.html, terminating

.. note:: changing feature compatibility version to 3.6 when using MongoRocks
   will produce the following error: ``storage engine does not support
   upgrading featureCompatibilityVersion to 3.6``

To continue using |PSMDB| 3.6 with MongoRocks, use one of the following two
methods:


    Add ``--useDeprecatedMongoRocks`` to ``mongod`` startup options
    Update the config file with the following parameter:

.. code-block:: text

      storage:
      engine: rocksdb
      useDeprecatedMongoRocks: true


*MongoRocks* is a storage engine for MongoDB
based on the RocksDB_ key-value store optimized for fast storage.
It is developed by Facebook and designed to handle write-intensive workloads.

.. contents::
  :local:
  :depth: 1

The *MongoRocks* storage engine is available in |PSMDB|
along with the standard MongoDB engines
(the original `MMAPv1`_ and the default `WiredTiger`_),
as well as :ref:`inmemory`.

Using MongoRocks
================

As of version 3.2, |PSMDB| runs with `WiredTiger`_ by default.
If you still would like to use the deprecated *MongoRocks* storage
engine, please use the ``--storageEngine rocksdb`` command-line option
accompanied by ``--useDeprecatedMongoRocks`` when you start
``mongod``. Alternatively, you can set the ``storage.engine`` and
``useDeprecatedMongoRocks`` variables in the configuration file (by
default, :file:`/etc/mongod.conf`) as shown below.

Data created by one storage engine
is not compatible with other storage engines,
because each one has its own data model.
When changing the storage engine, you have to do one of the following:

* If you simply want to temporarily test *MongoRocks*,
  change to a different data directory with the ``--dbpath``
  command-line option:

  .. code-block:: bash

     $ service mongod stop
     $ mongod --storageEngine rocksdb --useDeprecatedMongoRocks --dbpath <newDataDir>

  .. note:: Make sure that the user running ``mongod``
     has read and write permissions for the new data directory.

* If you want to permanently switch to *MongoRocks*
  and do not have any valuable data in your database,
  clean out the default data directory and edit the configuration file:

  .. code-block:: bash

     $ service mongod stop
     $ rm -rf /var/lib/mongodb/*
     $ sed -i '/engine: .*rocksdb/s/#//g' /etc/mongod.conf
     $ service mongod start

* If there is data that you want to migrate
  and make compatible with *MongoRocks*,
  use the ``mongodump`` and ``mongorestore`` utilities:

  .. code-block:: bash

     $ mongodump --out <dumpDir>
     $ service mongod stop
     $ rm -rf /var/lib/mongodb/*
     $ sed -i '/engine: .*rocksdb/s/#//g' /etc/mongod.conf
     $ service mongod start
     $ mongorestore <dumpDir>

.. _`MMAPv1`: https://docs.mongodb.org/manual/core/mmapv1/
.. _`WiredTiger`: https://docs.mongodb.org/manual/core/wiredtiger/

Configuring MongoRocks
======================

You can configure *MongoRocks* using either command-line options
or corresponding parameters in the :file:`/etc/mongod.conf` file.
The configuration file is formatted in YAML.
For example, the following sample configuration is suggested
as the default for running |PSMDB| with *MongoRocks*:

.. code-block:: text

   storage:
     engine: rocksdb
     useDeprecatedMongoRocks: true
     rocksdb:
       cacheSizeGB: 1
       compression: snappy
       maxWriteMBPerSec: 1024
       crashSafeCounters: false
       counters: true
       singleDeleteIndex: false

Setting parameters in the previous example configuration file
is the same as starting the ``mongod`` daemon with the following options:

.. code-block:: bash

    mongod --storageEngine=rocksdb \
      --useDeprecatedMongoRocks \
      --rocksdbCacheSizeGB=1 \
      --rocksdbCompression=snappy \
      --rocksdbMaxWriteMBPerSec=1024 \
      --rocksdbCrashSafeCounters=false \
      --rocksdbCounters=true \
      --rocksdbSingleDeleteIndex=false

The following options are available
(with corresponding YAML configuration file parameters):

.. option:: --rocksdbCacheSizeGB

   :Variable: ``storage.rocksdb.cacheSizeGB``
   :Type: Integer
   :Default: 30% of physical memory

   Specifies the amount of memory (in gigabytes) to allocate for block cache.
   Block cache is used to store uncompressed pages.
   Compressed pages are stored in kernel's page cache.

   To configure block cache size dynamically,
   set the ``rocksdbRuntimeConfigCacheSizeGB`` parameter at runtime::

    db.adminCommand({setParameter:1, rocksdbRuntimeConfigCacheSizeGB: 10})

.. option:: --rocksdbCompression

   :Variable: ``storage.rocksdb.compression``
   :Type: String
   :Default: ``snappy``

   Specifies the block compression algorithm for data collection.
   Possible values: ``none``, ``snappy``, ``zlib``, ``lz4``, ``lz4hc``.

.. option:: --rocksdbMaxWriteMBPerSec

   :Variable: ``storage.rocksdb.maxWriteMBPerSec``
   :Type: Integer
   :Default: ``1024`` (1 GB/sec)

   Specifies the maximum speed at which *MongoRocks* writes to storage
   (in megabytes per second).
   Decrease this value to reduce read latency spikes during compactions.
   However, reducing it too much might slow down writes.

   To configure write speed dynamically,
   set the ``rocksdbRuntimeConfigMaxWriteMBPerSec`` parameter at runtime::

    db.adminCommand({setParameter:1, rocksdbRuntimeConfigMaxWriteMBPerSec:30})

.. option:: --rocksdbCrashSafeCounters

   :Variable: ``storage.rocksdb.crashSafeCounters``
   :Type: Boolean
   :Default: ``false``

   Specifies whether to correct counters after a crash.
   Enabling this can affect write performance.

.. option:: --rocksdbCounters

   :Variable: ``storage.rocksdb.counters``
   :Type: Boolean
   :Default: ``true``

   Specifies whether to use advanced counters for *MongoRocks*.
   You can disable them to improve write performance.

.. option:: --rocksdbSingleDeleteIndex

   :Variable: ``storage.rocksdb.singleDeleteIndex``
   :Type: Boolean
   :Default: ``false``

   This is an experimental feature.
   Enable it only if you know what you are doing.


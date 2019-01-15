.. _mongorocks:

==========
MongoRocks
==========

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
You can select a storage engine
using the ``--storageEngine`` command-line option when you start ``mongod``.
Alternatively, you can set the ``storage.engine`` variable
in the configuration file (by default, :file:`/etc/mongod.conf`):

Data created by one storage engine
is not compatible with other storage engines,
because each one has its own data model.
When changing the storage engine, you have to do one of the following:

* If you simply want to temporarily test *MongoRocks*,
  change to a different data directory with the ``--dbpath``
  command-line option:

  .. code-block:: bash

     $ service mongod stop
     $ mongod --storageEngine rocksdb --dbpath <newDataDir>

  .. note:: Make sure that the user running ``mongod``
     has read and write permissons for the new data directory.

* If you want to permanently switch to *MongoRocks*
  and do not have any valuable data in your database,
  clean out the default data directory and edit the configuration file:

  .. code-block:: bash

     $ service mongod stop
     $ rm -rf /var/lib/mongodb/*
     $ sed -i '/engine: \*rocksdb/s/#//g' /etc/mongod.conf
     $ service mongod start

* If there is data that you want to migrate
  and make compatible with *MongoRocks*,
  use the ``mongodump`` and ``mongorestore`` utilities:

  .. code-block:: bash

     $ mongodump --out <dumpDir>
     $ service mongod stop
     $ rm -rf /var/lib/mongodb/*
     $ sed -i '/engine: \*rocksdb/s/#//g' /etc/mongod.conf
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
      --rocksdbCacheSizeGB=1 \
      --rocksdbCompression=snappy \
      --rocksdbMaxWriteMBPerSec=1024 \
      --rocksdbCrashSafeCounters=false \
      --rocksdbCounters=true \
      --rocksdbSingleDeleteIndex=false

.. seealso::

   YAML Specification
      https://yaml.org/spec/1.2/spec.html

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


.. _perconaft:

========================
PerconaFT Storage Engine
========================

PerconaFT is a storage engine based on the Fractal Tree Index model, which is optimized for fast disk I/O. The Fractal Tree data structure contains buffers to temporarily store insertions. When a buffer is full, it is flushed to children nodes. This ensures that an I/O operation performs a lot of useful work when messages reach leaves on disk, instead of just a small write per I/O.

The PerconaFT storage engine is available in Percona Server for MongoDB along with the standard MongoDB engines (`MMAPv1 <https://docs.mongodb.org/manual/core/mmapv1/>`_) and `WiredTiger <https://docs.mongodb.org/manual/core/wiredtiger/>`_), as well as `MongoRocks <http://rocksdb.org>`_.

Using PerconaFT
===============

.. attention:: PerconaFT is not supported on 32-bit systems.

By default, Percona Server for MongoDB runs with MMAPv1. To enable PerconaFT:

1. Create a data directory for PerconaFT

   PerconaFT does not support data created with other storage engines. You need to create a separate data directory for PerconaFT and ensure that the user running Percona Server for MongoDB has read and write permissons for this directory.

2. Run ``mongod`` with PerconaFT

   Set the ``--storageEngine`` option to ``PerconaFT`` and the ``--dbpath`` option to the newly created directory for PerconaFT.

   .. code-block:: bash

      $ mongod --storageEngine PerconaFT --dbpath /data/dir/for/perconaft

.. note:: You can specify the above options in the configuration file. The default configuration file is :file:`/etc/mongod.conf`. Alternatively, you can create a configuration file and specify it using the ``--config`` option.

   .. code-block:: bash

      $ mongod --config /path/to/mongod.conf

   You can set the storage engine and data directory in the configuration file as follows:

   .. code-block:: yaml

      storage:
         dbPath: data/dir/for/perconaft
         engine: PerconaFT

.. attention:: Transparent huge pages is a feature in newer Linux kernel versions that causes problems for the memory usage tracking calculations in PerconaFT and can lead to memory overcommit. If you have this feature enabled, PerconaFT will not start, and you should turn it off. If you want to run with transparent hugepages on, you can set an environment variable ``TOKU_HUGE_PAGES_OK=1``, but only do this for testing, and only with a small cache size.

Storage Engine Comparison
=========================

|Percona Server for MongoDB| includes several storage engines, which have a different set of features and advantages over one another. To help you decide which is better for you, the table below lists features available in various storage engines:

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


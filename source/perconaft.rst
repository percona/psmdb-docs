
===============
Using PerconaFT
===============

PerconaFT is a storage engine based on the Fractal Tree Index model, which is optimized for fast disk I/O. The storage engine is available in |Percona Server for MongoDB| along with the standard MongoDB engines (MMAPv1 and WiredTiger), as well as RocksDB.

PerconaFT is supported on 64-bit CentOS, should work on other 64-bit linux distributions, and may work on OS X 10.8 and FreeBSD. PerconaFT is not supported on 32-bit systems.

To enable PerconaFT, run ``mongod`` with the ``--storageEngine=PerconaFT`` option.

.. note:: Transparent huge pages is a feature in newer Linux kernel versions that causes problems for the memory usage tracking calculations in PerconaFT and can lead to memory overcommit. If you have this feature enabled, PerconaFT will not start, and you should turn it off. If you want to run with transparent hugepages on, you can set an environment variable ``TOKU_HUGE_PAGES_OK=1``, but only do this for testing, and only with a small cache size.

Storage Engine Comparison
=========================

|Percona Server for MongoDB| includes several storage engines, which have different set of features and advantages over one another. To help you decide which is better for you, the table below lists features available in various storage engines:

.. list-table::
   :header-rows: 1

   * - Feature
     - MMAPv1
     - WiredTiger
     - RocksDB
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


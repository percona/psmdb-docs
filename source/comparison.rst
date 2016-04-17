.. _compare:

=============================================
Percona Server for MongoDB Feature Comparison
=============================================

Percona Server for MongoDB is based on MongoDB 3.2, and it is the successor to Percona TokuMX, which is based on MongoDB 2.4. The tables in this section will help you evaluate the differences.

Storage Engines
===============

Both MongoDB and Percona Server for MongoDB include a pluggable storage engine API. This enables you to select from a variety of storage engines depending on your needs. Previous MongoDB versions (before 3.0) and Percona TokuMX can run with only one default storage engine.

The following table shows which storage engines are available.

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * - 
     - PSMDB 3.2
     - MongoDB 3.2
     - PSMDB 3.0
     - MongoDB 3.0
     - TokuMX [#n-1]_
   * - `MMAPv1 <https://docs.mongodb.org/manual/core/mmapv1/>`_
     - YES
     - YES
     - YES (default)
     - YES (default)
     - NO
   * - `WiredTiger <https://docs.mongodb.org/manual/core/wiredtiger/>`_
     - YES (default)
     - YES (default)
     - YES
     - YES
     - NO
   * - `MongoRocks <http://rocksdb.org>`_ [#n-2]_
     - YES
     - NO
     - YES
     - NO
     - NO
   * - :ref:`PerconaFT <perconaft>`
     - YES
     - NO
     - YES
     - NO
     - NO

.. [#n-1] TokuMX uses a proprietary storage engine similar to :ref:`PerconaFT <perconaft>`

.. [#n-2] MongoRocks engine is currently considered experimental

Feature Comparison
==================

The table below provides a comparison of important features to help you evaluate the differences.

.. note:: It is assumed that you run Percona Server for MongoDB with the PerconaFT storage engine, and it is compared against MongoDB *community edition* running with MMAPv1. There are footnotes for cases when a feature depends on the storage engine or it is available only in the commercial enterprise edition of MongoDB. 

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * - 
     - PSMDB 3.2
     - MongoDB 3.2
     - PSMDB 3.0
     - MongoDB 3.0
     - TokuMX
   * - :ref:`Hot Backup <toku-backup>`
     - YES [#n-3]_
     - NO
     - YES [#n-3]_
     - NO
     - YES
   * - :ref:`Audit Logging <audit-log>`
     - YES
     - NO [#n-4]_
     - YES
     - NO [#n-4]_
     - YES
   * - :ref:`External SASL Authentication <ext-auth>`
     - YES
     - NO [#n-4]_
     - YES
     - NO [#n-4]_
     - NO
   * - Geospatial Indexes
     - YES
     - YES
     - YES
     - YES
     - YES
   * - Text Search
     - YES
     - YES
     - YES
     - YES
     - NO
   * - ACID and MVCC compliant
     - NO
     - NO
     - NO
     - NO
     - YES
   * - Clustering Key Support
     - NO
     - NO
     - NO
     - NO
     - YES
   * - Sharding with Clustering Keys
     - NO
     - NO
     - NO
     - NO
     - YES
   * - Point-in-time Recovery
     - NO
     - NO [#n-4]_
     - NO
     - NO [#n-4]_
     - YES

.. [#n-3] You can use :ref:`TokuBackup <toku-backup>` when running under :ref:`PerconaFT <perconaft>` or use hot backup functionality available in the MongoRocks storage engine

.. [#n-4] Available in MongoDB Enterprise Edition

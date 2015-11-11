.. Percona Server for MongoDB documentation master file, created by
   sphinx-quickstart on Sat Sep 12 09:11:52 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _dochome:

============================================
 Percona Server for MongoDB - Documentation
============================================

|Percona Server for MongoDB| is a highly scalable, zero-maintenance downtime database supporting the |MongoDB| v3.0 protocol and drivers. It extends |MongoDB| with RocksDB and PerconaFT storage engines, as well as features like external authentication and audit logging. |Percona Server for MongoDB| requires no changes to |MongoDB| applications or code.

The table below shows a comparison between |Percona Server for MongoDB|, |TokuMX|, and corresponding versions of |MongoDB| community edition. This comparison assumes that the PerconaFT storage engine is used for |Percona Server for MongoDB| and |TokuMX|, and features are compared against |MongoDB| running with MMAPv1.

.. list-table::
   :header-rows: 1

   * - 
     - PSMDB
     - MongoDB 3.0
     - TokuMX
     - MongoDB 2.4
   * - :ref:`Audit Logging <auditing>`
     - **YES**
     - *NO* [1]_
     - **YES**
     - *NO*
   * - :ref:`Hot Backup <toku-backup>`
     - **YES**
     - *NO*
     - **YES**
     - *NO*
   * - :ref:`External SASL Authentication <ext-auth>`
     - **YES**
     - *NO* [1]_
     - *NO*
     - *NO*
   * - High Compression
     - **YES**
     - *NO*
     - **YES**
     - *NO*
   * - Reduced SSD Wear
     - **YES**
     - *NO*
     - **YES**
     - *NO*
   * - Zero Maintenance Downtime
     - **YES**
     - *NO*
     - **YES**
     - *NO*
   * - Fully ACID and MVCC compliant
     - *NO*
     - *NO*
     - **YES**
     - *NO*
   * - Clustering Key Support
     - *NO*
     - *NO*
     - **YES**
     - *NO*
   * - Sharding with Clustering Keys
     - *NO*
     - *NO*
     - **YES**
     - *NO*
   * - Point-in-time Recovery
     - *NO*
     - *NO* [1]_
     - **YES**
     - *NO* [1]_
   * - Geospatial Indexes
     - **YES**
     - **YES**
     - **YES**
     - *NO*
   * - Text Search
     - **YES**
     - **YES**
     - *NO*
     - *NO*

.. [1] Available in MongoDB Enterprise Edition.

Installation
============
.. toctree::
   :maxdepth: 1
   :glob:

   installation
   upgrading_guide_mongodb_psmdb
   upgrading_guide_tokumx_psmdb

Features
========

.. toctree::
   :maxdepth: 1
   :glob:

   perconaft
   ext-auth
   auditing

Reference
=========

.. toctree::
   :maxdepth: 1
   :glob:

   release_notes/release_notes_index
   glossary
   copyright
   trademark-policy

* :ref:`genindex`


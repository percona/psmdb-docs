.. Percona Server for MongoDB documentation master file, created by
   sphinx-quickstart on Sat Sep 12 09:11:52 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _dochome:

============================================
 Percona Server for MongoDB - Documentation
============================================

|Percona Server for MongoDB| is a highly scalable, zero-maintenance downtime database supporting the |MongoDB| v3.0 protocol and drivers. It extends |MongoDB| with RocksDB and PerconaFT storage engines, as well as features like external authentication and audit logging. |Percona Server for MongoDB| requires no changes to |MongoDB| applications or code. The main benefits of |Percona Server for MongoDB| are:

 * Improved single-threaded and multi-threaded performance
 * Compression
 * Fully ACID and MVCC transaction support
 * No maintenance or scheduled downtime necessary
 * Clustering key support for query acceleration
 * Better read scaling and reduced lag on replica sets
 * Low-impact migrations and accelerated range queries with clustering shard keys
 * Fast, read-free updates
 * Hot Backup
 * Point-in-time Recovery
 * Audit Logging
 * Reduced SSD wear
 * Geospatial Indexes
 * Includes all |MongoDB| v3.0 functionality except Text Search
   
Installation
============
.. toctree::
   :maxdepth: 2
   :glob:

   installation
   upgrading_guide_mongodb_psmdb
   building

Features
========

.. toctree::
   :maxdepth: 1
   :glob:

   ext_authentication/index
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


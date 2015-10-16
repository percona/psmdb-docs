.. Percona Server for MongoDB documentation master file, created by
   sphinx-quickstart on Sat Sep 12 09:11:52 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _dochome:

============================================
 Percona Server for MongoDB - Documentation
============================================

|Percona Server for MongoDB| is a highly scalable, zero-maintenance downtime database supporting the |MongoDB| v3.0 protocol and drivers. It extends |MongoDB| with RocksDB and PerconaFT storage engines, as well as features like external authentication and audit logging. |Percona Server for MongoDB| requires no changes to |MongoDB| applications or code. The main benefits of |Percona Server for MongoDB| are:

* Audit logging
* External SASL authentication
* Compression
* No maintenance or scheduled downtime necessary
* Reduced SSD wear
* Includes all |MongoDB| v3.0 functionality
* Hot Backup (will be available in the GA release)
 
Installation
============
.. toctree::
   :maxdepth: 2
   :glob:

   installation
   upgrading_guide_mongodb_psmdb
   upgrading_guide_tokumx_psmdb
   building

Features
========

.. toctree::
   :maxdepth: 1
   :glob:

   perconaft
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


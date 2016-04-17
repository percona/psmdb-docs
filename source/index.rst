.. _dochome:

========================================
Percona Server for MongoDB Documentation
========================================

|Percona Server for MongoDB| is a free, enhanced, fully compatible, open source, drop-in replacement for MongoDB 3.2 Community Edition with enterprise-grade features. It requires no changes to MongoDB applications or code.

Percona Server for MongoDB provides:

* MongoDB's original `MMAPv1 <https://docs.mongodb.org/manual/core/mmapv1/>`_ storage engine, and the default `WiredTiger <https://docs.mongodb.org/manual/core/wiredtiger/>`_ engine
* Optional :ref:`PerconaFT <perconaft>` and `MongoRocks <http://rocksdb.org>`_ storage engines
* :ref:`Percona TokuBackup <toku-backup>` for creating dynamic backups while data remains fully accessible and writable (*hot backup*)
* :ref:`External SASL authentication <ext-auth>` using OpenLDAP or Active Directory
* :ref:`Audit logging <audit-log>` to track and query database interactions of users or applications

.. note:: MongoRocks is currently considered experimental.

-----

Introduction
============

.. toctree::
   :maxdepth: 1

   Feature Comparison <comparison>

Installation
============

.. toctree::
   :maxdepth: 2
   :includehidden:
   :titlesonly:

   install/index
   Upgrading from MongoDB Community Edition <install/upgrade_from_mongodb>
   Upgrading from Percona TokuMX <install/upgrade_from_tokumx>

Features
========

.. toctree::
   :maxdepth: 1

   perconaft
   toku-backup
   authentication
   audit-logging

Reference
=========

.. toctree::
   :maxdepth: 1

   Release Notes <release_notes/index>
   glossary
   copyright
   trademark-policy


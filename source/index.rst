.. Percona Server for MongoDB documentation master file, created by
   sphinx-quickstart on Sat Sep 12 09:11:52 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _dochome:

========================================
Percona Server for MongoDB Documentation
========================================

.. note:: Percona Server for MongoDB is currently available only as a *release candidate*.

   For more information, see the :ref:`3.0.5-rc7`.

Percona Server for MongoDB is a free, enhanced, fully compatible, open source, drop-in replacement for MongoDB 3.0 Community Edition with enterprise-grade features. It requires no changes to MongoDB applications or code.

Percona Server for MongoDB provides:

* MongoDB's original `MMAPv1 <https://docs.mongodb.org/manual/core/mmapv1/>`_ storage engine as the default, and `WiredTiger <https://docs.mongodb.org/manual/core/wiredtiger/>`_ as an alternative
* Optional `MongoRocks <http://rocksdb.org>`_ and :ref:`PerconaFT <perconaft>` storage engines
* :ref:`Percona TokuBackup <toku-backup>` for creating dynamic backups while data remains fully accessible and writable (*hot backup*)
* :ref:`External SASL authentication <ext-auth>` using OpenLDAP or Active Directory
* :ref:`Audit logging <audit-log>` to track and query database interactions of users or applications

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


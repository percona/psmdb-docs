.. _dochome:

==================================================
Percona Server for MongoDB |version| Documentation
==================================================

|PSMDB| is a free, enhanced, fully compatible, open source, drop-in replacement
for MongoDB 3.2 Community Edition with enterprise-grade features.
It requires no changes to MongoDB applications or code.

|PSMDB| provides the following features:

* MongoDB's original `MMAPv1`_ storage engine,
  and the default `WiredTiger`_ engine
* Optional :ref:`PerconaFT <perconaft>`, :ref:`inmemory`,
  and :ref:`mongorocks` storage engines
* :ref:`Percona TokuBackup <toku-backup>` for creating dynamic backups
  while data remains fully accessible and writable (*hot backup*)
* :ref:`External SASL authentication <ext-auth>`
  using OpenLDAP or Active Directory
* :ref:`Audit logging <audit-log>`
  to track and query database interactions of users or applications

.. note:: PerconaFT has been deprecated
   and will not be available in future releases.

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

   mongorocks
   inmemory
   perconaft
   toku-backup
   hot-backup
   rate-limit
   authentication
   audit-logging

Reference
=========

.. toctree::
   :maxdepth: 1

   switch_storage_engines
   Parameter Tuning <setParameter>
   Release Notes <release_notes/index>
   glossary
   copyright
   trademark-policy


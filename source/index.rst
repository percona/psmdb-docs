.. _dochome:

========================================
Percona Server for MongoDB Documentation
========================================

|PSMDB| is a free, enhanced, fully compatible, open source, drop-in replacement
for MongoDB 3.4 Community Edition with enterprise-grade features.
It requires no changes to MongoDB applications or code.

|PSMDB| provides the following features:

* MongoDB's original `MMAPv1`_ storage engine,
  and the default `WiredTiger`_ engine
* Optional :ref:`inmemory` and `MongoRocks`_ storage engines
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
   changed_in_34

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

   inmemory
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


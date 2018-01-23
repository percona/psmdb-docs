.. _dochome:

==================================================
Percona Server for MongoDB |version| Documentation
==================================================

|PSMDB| is a free, enhanced, fully compatible, open source, drop-in replacement
for MongoDB 3.6 Community Edition with enterprise-grade features.
It requires no changes to MongoDB applications or code.

|PSMDB| provides the following features:

* MongoDB's original MMAPv1_ storage engine,
  and the default WiredTiger_ engine
* Optional :ref:`inmemory` and :ref:`mongorocks` storage engines
* :ref:`External SASL authentication <ext-auth>`
  using OpenLDAP or Active Directory
* :ref:`Audit logging <audit-log>`
  to track and query database interactions of users or applications
* :ref:`hot-backup` for the default WiredTiger_
  and alternative :ref:`mongorocks` storage engine
* :ref:`rate-limit` to decrease the impact of the profiler on performance

-----

.. note::

  This version is currenlty considered *BETA* quality and it's not inteded to
  be run in production.

Introduction
============

.. toctree::
   :maxdepth: 1

   Feature Comparison <comparison>
   changed_in_36

Installation
============

.. toctree::
   :maxdepth: 2
   :includehidden:
   :titlesonly:

   install/index
   Upgrading from MongoDB Community Edition <install/upgrade_from_mongodb>
   Upgrading from Version 3.4 <install/upgrade_from_34>

Features
========

.. toctree::
   :maxdepth: 1

   inmemory
   mongorocks
   hot-backup
   rate-limit
   authentication
   audit-logging
   log-redaction
   enable-auth

Reference
=========

.. toctree::
   :maxdepth: 1

   switch_storage_engines
   Parameter Tuning <setParameter>
   contact
   Release Notes <release_notes/index>
   glossary
   copyright
   trademark-policy


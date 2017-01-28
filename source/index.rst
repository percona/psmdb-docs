.. _dochome:

========================================
Percona Server for MongoDB Documentation
========================================

|PSMDB| is a free, enhanced, fully compatible, open source, drop-in replacement
for MongoDB 3.4 Community Edition with enterprise-grade features.
It requires no changes to MongoDB applications or code.

.. note:: |PSMDB| 3.4 is currently in beta.
   For the latest stable version, see `PSMDB 3.2 documentation
   <https://www.percona.com/doc/percona-server-for-mongodb/LATEST/>`_.

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


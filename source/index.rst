.. _dochome:

================================================================================
Percona Server for MongoDB |version| Documentation
================================================================================

|PSMDB| is a free, enhanced, fully compatible, source available, drop-in replacement
for MongoDB |version| Community Edition with enterprise-grade features.
It requires no changes to MongoDB applications or code.

.. hint::

   To see which version of |PSMDB| you are using check the value of the
   ``psmdbVersion`` key in the output of the ``buildInfo`` database command. If
   this key does not exist |PSMDB| is not installed on the server.

   .. seealso::

      MongoDB Documentation: ``buildInfo`` Database Command
         https://docs.mongodb.com/manual/reference/command/buildInfo/#dbcmd.buildInfo

|PSMDB| provides the following features:

- MongoDB's original MMAPv1_ storage engine, and the default
  WiredTiger_ engine
- Optional :ref:`inmemory` storage engine
- Optional :ref:`psmdb.data-at-rest-encryption`
- :ref:`External SASL authentication <ext-auth>`
  using OpenLDAP or Active Directory
- :ref:`Audit logging <audit-log>`
  to track and query database interactions of users or applications
- :ref:`hot-backup` for the default WiredTiger_
- :ref:`rate-limit` to decrease the impact of the profiler on performance

--------------------------------------------------------------------------------

Introduction
================================================================================

.. toctree::
   :maxdepth: 1

   Feature Comparison <comparison>

Installation
================================================================================

.. toctree::
   :maxdepth: 2
   :includehidden:
   :titlesonly:

   install/index
   install/upgrade_from_mongodb
   install/upgrade_from_36

Features
================================================================================

.. toctree::
   :maxdepth: 1

   inmemory
   hot-backup
   rate-limit
   authentication
   audit-logging
   log-redaction
   enable-auth
   data_at_rest_encryption
   ngram-full-text-search

Reference
================================================================================

.. toctree::
   :maxdepth: 1

   switch_storage_engines
   Parameter Tuning <setParameter>
   contact
   Release Notes <release_notes/index>
   glossary
   copyright
   trademark-policy

.. include:: .res/replace.txt

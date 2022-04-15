.. _dochome:

================================================================================
Percona Server for MongoDB |version| Documentation
================================================================================

|PSMDB| is a free, enhanced, fully compatible, source available, drop-in replacement
for MongoDB |version| Community Edition with enterprise-grade features.
It requires no changes to MongoDB applications or code.

.. hint::

   To see which version of |PSMDB| you are using check the value of the
   ``psmdbVersion`` key in the output of the `buildInfo <https://docs.mongodb.com/manual/reference/command/buildInfo/#dbcmd.buildInfo>`_ database command. If
   this key does not exist, |PSMDB| is not installed on the server.
        
|PSMDB| provides the following features:

- MongoDB's default WiredTiger_ engine
- :ref:`inmemory` storage engine
- :ref:`psmdb.data-at-rest-encryption`
- :ref:`External authentication <ext-auth>`
  using OpenLDAP or Active Directory
- :ref:`Audit logging <audit-log>`
  to track and query database interactions of users or applications
- :ref:`hot-backup` for the default WiredTiger_
- :ref:`rate-limit` to decrease the impact of the profiler on performance

To learn more about the features, available in |PSMDB|, see :ref:`compare`

--------------------------------------------------------------------------------

About Percona Server for MongoDB
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


Features
================================================================================

.. toctree::
   :maxdepth: 2
   :includehidden:
   :titlesonly:

   inmemory
   hot-backup
   rate-limit
   authentication
   authorization
   audit-logging
   log-redaction
   data-at-rest-encryption
   ngram-full-text-search

How to
================================================================================

.. toctree::
   :maxdepth: 1

   Enable authentication <enable-auth>
   Set up LDAP authentication using SASL <sasl-auth>
   Set up LDAP authentication and authorization using NativeLDAP <ldap-setup>
   x509-ldap
   kerberos
   Tune parameters <set-parameter>
   Upgrade Percona Server for MongoDB <install/upgrade-from-mongodb>
   Perform a major upgrade of Percona Server for MongoDB from 4.0 to 4.2 <install/upgrade-from-40>
   Uninstall Percona Server for MongoDB <install/uninstall>

Release Notes
================================================================================

.. toctree::
   :maxdepth: 1

   Release notes <release_notes/index>

Reference
================================================================================

.. toctree::
   :maxdepth: 1

   contact
   glossary
   copyright
   trademark-policy

.. include:: .res/replace.txt

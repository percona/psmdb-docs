.. _compare:

================================================================================
Percona Server for MongoDB Feature Comparison
================================================================================

|PSMDB| |version| is based on `MongoDB 4.4 <https://docs.mongodb.com/manual/introduction/>`_. |PSMDB| extends MongoDB 
Community Edition to include the functionality that is otherwise only available
in MongoDB Enterprise Edition.

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * -
     - PSMDB
     - MongoDB
   * - Storage Engines
     - * WiredTiger_ (default)
       * :ref:`inmemory`
     - * WiredTiger_ (default)
       * In-Memory_ (Enterprise only)
   * - Encryption-at-Rest
     - * Key servers = :ref:`Hashicorp Vault <vault>`, :ref:`KMIP <kmip>`
       * Fully open source
     - * Key server = KMIP
       * Enterprise only
   * - Hot Backup 
     - :ref:`YES <hot-backup>` (replica set)
     - NO
   * - LDAP Authentication
     - * (legacy) :ref:`ldap-authentication-sasl`
     - * Enterprise only
   * - LDAP Authorization
     - :ref:`YES <ldap-authorization>`
     - Enterprise only
   * - Kerberos Authentication
     - :ref:`YES <kerberos-authentication>`
     - Enterprise only
   * - Audit Logging 
     - :ref:`YES <audit-log>`
     - Enterprise only
   * - Log redaction
     - :ref:`YES <log-redaction>`
     - Enterprise only
   * - SNMP Monitoring
     - NO
     - Enterprise only

Profiling Rate Limiting
-----------------------

Profiling Rate Limiting was added to |PSMDB| in v3.4 with the ``--rateLimit`` argument. Since v3.6, MongoDB Community (and Enterprise) Edition includes a similar option slowOpSampleRate_. Please see :ref:`rate-limit` for more information.

.. _slowOpSampleRate: https://docs.mongodb.com/manual/reference/program/mongod/index.html#cmdoption-mongod-slowopsamplerate

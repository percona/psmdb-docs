.. _compare:

================================================================================
Percona Server for MongoDB Feature Comparison
================================================================================

|PSMDB| |version| is based on `MongoDB 4.0 <https://docs.mongodb.com/manual/introduction/>`_. |PSMDB| extends MongoDB 
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
     - * Key server = Hashicorp Vault
       * Fully opensource
     - * Key server = KMIP
       * Enterprise only
   * - :ref:`Hot Backup <hot-backup>`
     - YES (replica set)
     - NO
   * - LDAP Authentication
     - * Simple LDAP Auth
       * (legacy) :ref:`External SASL Authentication <ext-auth>`
     - * Enterprise only
       * Enterprise only
   * - LDAP Authorization
     - YES
     - Enterprise only
   * - Kerberos Authentication
     - YES
     - Enterprise only
   * - :ref:`Audit Logging <audit-log>`
     - YES
     - Enterprise only
   * - Log redaction
     - YES
     - Enterprise only
   * - SNMP Monitoring
     - NO
     - Enterprise only

Profiling Rate Limiting
-----------------------

Profiling Rate Limiting was added to |PSMDB| in v3.4 with the ``--rateLimit`` argument. Since v3.6, MongoDB Community (and Enterprise) Edition includes a similar option slowOpSampleRate_. Please see :ref:`rate-limit` for more information.

.. _slowOpSampleRate: https://docs.mongodb.com/manual/reference/program/mongod/index.html#cmdoption-mongod-slowopsamplerate

.. include:: .res/replace.txt
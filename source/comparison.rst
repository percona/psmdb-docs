.. _compare:

================================================================================
Percona Server for MongoDB Feature Comparison
================================================================================

|PSMDB| |version| is based on MongoDB |version|. |PSMDB| extends MongoDB 
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
     - YES (replicaset)
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
     - No
     - Enterprise only

Profiling Rate Limiting
-----------------------

Profiling Rate Limiting was added to PSMDB in v3.4 with --rateLimit argument. Since v3.6 MongoDB community (and Enterprise) reproduced this feature but called the option slowOpSampleRate_. Percona Server for MongoDB v3.6+ includes both. The two options have the same effect upon profiling and the database diagnostic log but the argument value is inverted: slowOpSampleRate = (1/rateLimit).

For naming simplicity we recommend using --slowOpSampleRate argument. Eg. if you have used --rateLimit 50 please use --slowOpSampleRate 0.02 instead.

.. _slowOpSampleRate: https://docs.mongodb.com/manual/reference/program/mongod/index.html#cmdoption-mongod-slowopsamplerate

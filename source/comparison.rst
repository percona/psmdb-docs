.. _compare:

================================================================================
Percona Server for MongoDB Feature Comparison
================================================================================

|PSMDB| |version| is based on MongoDB |version|. |PSMDB| is the successor to Percona TokuMX,
which is based on MongoDB 2.4.

Both MongoDB and |PSMDB| include a pluggable storage engine API.  This enables
you to select from a variety of storage engines depending on your needs.
Previous MongoDB versions (before 3.0) could run with only
one default storage engine.  For more information about about using various
storage engines, see :ref:`switch_storage_engines`.

The following table will help you evaluate the differences.

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
   * - :ref:`Hot Backup <hot-backup>`
     - YES for WiredTiger_
     - NO
   * - :ref:`Audit Logging <audit-log>`
     - YES
     - Enterprise only
   * - :ref:`External SASL Authentication <ext-auth>`
     - YES
     - Enterprise only
   * - :ref:`rate-limit`
     - YES
     - YES [#]_
   * - Geospatial Indexes
     - YES
     - YES
   * - Text Search
     - YES
     - YES
   * - ACID and MVCC compliant
     - NO
     - NO
   * - Clustering Key Support
     - NO
     - NO
   * - Sharding with Clustering Keys
     - NO
     - NO
   * - Point-in-time Recovery
     - NO
     - Enterprise only

.. [#] via the `sampleRate <https://docs.mongodb.com/manual/reference/command/profile/#profile>`_ parameter.

.. _compare:

=============================================
Percona Server for MongoDB Feature Comparison
=============================================

|PSMDB| is based on MongoDB 3.2, and it is the successor to Percona TokuMX,
which is based on MongoDB 2.4.

Both MongoDB and |PSMDB| include a pluggable storage engine API.
This enables you to select from a variety of storage engines
depending on your needs.
Previous MongoDB versions (before 3.0) and Percona TokuMX
can run with only one default storage engine.

The following table will help you evaluate the differences.

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * -
     - PSMDB
     - MongoDB
     - TokuMX
   * - Storage Engines
     - * WiredTiger_ (default)
       * MMAPv1_
       * :ref:`inmemory`
       * :ref:`mongorocks`
       * :ref:`PerconaFT <perconaft>` (deprecated)
     - * WiredTiger_ (default)
       * MMAPv1_
       * In-Memory_ (Enterprise only)
     - Built-in storage engine based on the Fractal Tree index
   * - :ref:`Hot Backup <hot-backup>`
     - YES (for WiredTiger_ and :ref:`mongorocks`)
     - NO
     - YES
   * - :ref:`Audit Logging <audit-log>`
     - YES
     - Enterprise only
     - YES
   * - :ref:`External SASL Authentication <ext-auth>`
     - YES
     - Enterprise only
     - NO
   * - :ref:`rate-limit`
     - YES
     - NO
     - NO
   * - Geospatial Indexes
     - YES
     - YES
     - YES
   * - Text Search
     - YES
     - YES
     - NO
   * - ACID and MVCC compliant
     - NO
     - NO
     - YES
   * - Clustering Key Support
     - NO
     - NO
     - YES
   * - Sharding with Clustering Keys
     - NO
     - NO
     - YES
   * - Point-in-time Recovery
     - NO
     - Enterprise only
     - YES



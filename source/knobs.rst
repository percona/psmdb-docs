.. _knobs:

=============
Percona Knobs
=============

|PSMDB| includes several additional configuration file variables
and corresponding command-line options::

 Percona:
   cursorTimeoutMillis: <int>
   ignoreLongIndexError: <boolean>
   allowIndexIntersections: <boolean>
   ttlEnabled: <boolean>
   ttlSleepSecs: <int>

.. variable:: cursorTimeoutMillis

   :CLI Option: ``--cursorTimeoutMS``
   :Value Type: *integer*
   :Default: ``600000`` (ten minutes)

   Sets the duration of time after which idle query cursors
   are removed from memory.

.. variable:: ignoreLongIndexError

   :CLI Option: ``--failIndexKeyTooLong``
   :Value Type: *boolean*
   :Default: ``true``

   Older versions of MongoDB would insert and update documents
   even if an index key was too long.
   The documents would not be included in the index.
   Newer versions of MongoDB ignore documents with long index key.
   By setting this value to ``false``, the old behavior is enabled.

.. variable:: allowIndexIntersection

   :CLI Option: ``--internalQueryPlannerEnableIndexIntersection``
   :Value Type: *boolean*
   :Default: ``true``

   Due to changes introduced in MongoDB 2.6.4,
   some queries that reference multiple indexed fields,
   where one field matches no documents,
   may choose a non-optimal single-index plan.
   Setting this value to ``false`` will enable the old behavior
   and select the index intersection plan.

.. variable:: ttlEnabled

   :CLI Option: ``--ttlMonitorEnabled``
   :Value Type: *boolean*
   :Default: ``true``

   If this option is set to ``false``,
   the worker thread that monitors TTL Indexes and removes old documents
   will be disabled.

.. variable:: ttlSleepSecs

   :CLI Option: ``--ttlMonitorSleepSecs``
   :Value Type: *integer*
   :Default: ``60`` (one minute)

   Defines the number of seconds to wait
   between checking TTL Indexes for old documents and removing them.



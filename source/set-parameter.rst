.. _setParameter:

==============================
|PSMDB| Parameter Tuning Guide
==============================

|PSMDB| includes several parameters that can be changed
in one of the following ways:

* The ``setParameter`` admonitions in the configuration file
  for persistent changes in production::

   setParameter:
     cursorTimeoutMillis: <int>
     failIndexKeyTooLong: <boolean>
     internalQueryPlannerEnableIndexIntersection: <boolean>
     ttlMonitorEnabled: <boolean>
     ttlMonitorSleepSecs: <int>

* The ``--setParameter`` option arguments when running the ``mongod`` process
  for development or testing purposes:

  .. code-block:: bash

     $ mongod \
       --setParameter cursorTimeoutMillis=<int> \
       --setParameter failIndexKeyTooLong=<boolean> \
       --setParameter internalQueryPlannerEnableIndexIntersection=<boolean> \
       --setParameter ttlMonitorEnabled=<boolean> \
       --setParameter ttlMonitorSleepSecs=<int>

* The ``setParameter`` command on the ``admin`` database
  to make changes at runtime:

  .. code-block:: text

     > db = db.getSiblingDB('admin')
     > db.runCommand( { setParameter: 1, cursorTimeoutMillis: <int> } )
     > db.runCommand( { setParameter: 1, failIndexKeyTooLong: <boolean> } )
     > db.runCommand( { setParameter: 1, internalQueryPlannerEnableIndexIntersection: <boolean> } )
     > db.runCommand( { setParameter: 1, ttlMonitorEnabled: <int> } )
     > db.runCommand( { setParameter: 1, ttlMonitorSleepSecs: <int> } )

Parameters
==============

cursorTimeoutMillis
---------------------

:Value Type: *integer*
:Default: ``600000`` (ten minutes)

Sets the duration of time after which idle query cursors
are removed from memory.

failIndexKeyTooLong
-----------------------
:Value Type: *boolean*
:Default: ``true``

Versions of MongoDB prior to 2.6 would insert and update documents
even if an index key was too long.
The documents would not be included in the index.
Newer versions of MongoDB ignore documents with long index key.
By setting this value to ``false``, the old behavior is enabled.

internalQueryPlannerEnableIndexIntersection
----------------------------------------------

:Value Type: *boolean*
:Default: ``true``

Due to changes introduced in MongoDB 2.6.4,
some queries that reference multiple indexed fields,
where one field matches no documents,
may choose a non-optimal single-index plan.
Setting this value to ``false`` will enable the old behavior
and select the index intersection plan.

ttlMonitorEnabled
----------------------------------

:Value Type: *boolean*
:Default: ``true``

If this option is set to ``false``,
the worker thread that monitors TTL Indexes and removes old documents
will be disabled.

ttlMonitorSleepSecs
--------------------

:Value Type: *integer*
:Default: ``60`` (one minute)

Defines the number of seconds to wait
between checking TTL Indexes for old documents and removing them.


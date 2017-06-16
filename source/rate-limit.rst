.. _rate-limit:

====================
Profiling Rate Limit
====================

|PSMDB| can limit the number of queries collected by the database profiler
to decrease its impact on performance.
Rate limit is an integer between 1 and 1000
and represents the fraction of queries to be profiled.
For example, if you set it to 20, then every 20th query will be logged.
For compatibility reasons, rate limit of 0 is the same as setting it to 1,
and will effectively disable the feature
meaning that every query will be profiled.

The MongoDB database profiler can operate in one of three modes:

* ``0``: Profiling is disabled. This is the default setting.

* ``1``: The profiler collects data only for *slow* queries.
  By default, queries that take more than 100 milliseconds to execute
  are considered *slow*.

* ``2``: Collects profiling data for all database operations. 

Mode ``1`` ignores all *fast* queries,
which may be the cause of problems that you are trying to find.
Mode ``2`` provides a comprehensive picture of database performance,
but may introduce unnecessary overhead.

With rate limiting you can collect profiling data for all database operations
and reduce overhead by sampling queries.
Slow queries ignore rate limiting and are always collected by the profiler.

Enabling the Rate Limit
=======================

To enable rate limiting, set the profiler mode to ``2``
and specify the value of the rate limit.
Optionally, you can also change the default threshold for slow queries,
which will not be sampled by rate limiting.

For example, to set the rate limit to ``100``
(profile every 100th *fast* query)
and the slow query threshold to ``200``
(profile all queries slower than 200 milliseconds),
run the ``mongod`` instance as follows::

 $ mongod --profile 2 --slowms 200 --rateLimit 100

To do the same at runtime,
use the ``profile`` command.
It returns the *previous* settings
and ``"ok" : 1`` indicates that the operation was successful::

 > db.runCommand( { profile: 2, slowms: 200, ratelimit: 100 } );
 { "was" : 0, "slowms" : 100, "ratelimit" : 1, "ok" : 1 }

To check the current settings, run ``profile: -1``::

 > db.runCommand( { profile: -1 } );
 { "was" : 2, "slowms" : 200, "ratelimit" : 100, "ok" : 1 }

If you want to set or get just the rate limit value,
use the ``profilingRateLimit`` parameter on the ``admin`` database::

 > db.getSiblingDB('admin').runCommand( { setParameter: 1, "profilingRateLimit": 100 } );
 { "was" : 1, "ok" : 1 }
 > db.getSiblingDB('admin').runCommand( { getParameter: 1, "profilingRateLimit": 1 } );
 { "profilingRateLimit" : 100, "ok" : 1 }

If you want rate limiting to persist when you restart ``mongod``,
set the corresponding variables in the MongoDB configuration file
(by default, :file:`/etc/mongod.conf`)::

 operationProfiling:
   mode: all
   slowOpThresholdMs: 200
   rateLimit: 100

.. note:: The value of the ``operationProfiling.mode`` variable is a string,
   which you can set to either ``off``, ``slowOp``, or ``all``,
   corresponding to profiling modes ``0``, ``1``, and ``2``.

Profiler Collection Extension
=============================

Each document in the ``system.profile`` collection
includes an additional ``rateLimit`` field.
This field always has the value of ``1`` for *slow* queries
and the current rate limit value for *fast* queries.


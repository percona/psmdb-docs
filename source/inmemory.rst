.. _inmemory:

=====================
Percona Memory Engine
=====================

*Percona Memory Engine* is a special configuration of `WiredTiger`_
that does not store user data on disk.
Data fully resides in the main memory,
making processing much faster and smoother.
Keep in mind that you need to have enough memory to hold the data set,
and ensure that the server does not shut down.

.. contents::
  :local:
  :depth: 1

The *Percona Memory Engine* is available in |PSMDB|
along with the standard MongoDB engines
(the original `MMAPv1`_ and the default `WiredTiger`_),
as well as `MongoRocks`_ and :ref:`perconaft`.

.. note:: PerconaFT has been deprecated
   and will be removed in future releases.

Using Percona Memory Engine
===========================

As of version 3.2, |PSMDB| runs with `WiredTiger`_ by default.
You can select a storage engine
using the ``--storageEngine`` command-line option when you start ``mongod``.
Alternatively, you can set the ``storage.engine`` option
in the configuration file (by default, :file:`/etc/mongod.conf`):

Data created by one storage engine
is not compatible with other storage engines,
because each one has its own data model.
When changing the storage engine, you have to do one of the following:

* If you simply want to temporarily test a Percona Memory Engine,
  change to a different data directory with the ``--dbpath``
  command-line option:

  .. code-block:: bash

     service mongod stop
     mongod --storageEngine inMemory --dbpath <newDataDir>

  .. note:: Make sure that the user running ``mongod``
     has read and write permissons for the new data directory.

  .. note:: Although *Percona Memory Engine* stores all data in memory,
     some diagnostics and statistics are still written to disk.
     This is controlled using
     the :option:`--inMemoryStatisticsLogDelaySecs` option.

* If you want to permanently switch to Percona Memory Engine
  and do not have any valuable data in your database,
  clean out the default data directory and edit the configuration file:

  .. code-block:: bash

     service mongod stop
     rm -rf /var/lib/mongodb/*
     sed -i '/engine: \*inMemory/s/#//g' /etc/mongod.conf
     service mongod start

* If there is data that you want to migrate
  and make compatible with Percona Memory Engine,
  use the ``mongodump`` and ``mongorestore`` utilities:

  .. code-block:: bash

     mongodump --out <dumpDir>
     service mongod stop
     rm -rf /var/lib/mongodb/*
     sed -i '/engine: \*inMemory/s/#//g' /etc/mongod.conf
     service mongod start
     mongorestore <dumpDir>

.. _`MMAPv1`: https://docs.mongodb.org/manual/core/mmapv1/
.. _`WiredTiger`: https://docs.mongodb.org/manual/core/wiredtiger/
.. _`MongoRocks`: http://rocksdb.org

Configuring Percona Memory Engine
=================================

You can configure the Percona Memory Engine using either command-line options
or corresponding parameters in the :file:`/etc/mongod.conf` file.
The configuration file is formatted in YAML. For example:

.. code-block:: text

 storage:
   engine: inMemory
   inMemory:
     engineConfig:
       inMemorySizeGB: 140
       statisticsLogDelaySecs: 0

Setting parameters in the previous example configuration file
is the same as starting the ``mongod`` daemon with the following options:

.. code-block:: bash

 mongod --storageEngine=inMemory \
   --inMemorySizeGB=140 \
   --inMemoryStatisticsLogDelaySecs=0

The following options are available
(with corresponding YAML configuration file parameters):

.. option:: --inMemorySizeGB

   :Config: ``storage.inMemory.engineConfig.inMemorySizeGB``
   :Default: 60% of total memory minus 1024 MB, but not less than 256 MB

   Specifies the maximum memory in gigabytes to use for data.

.. option:: --inMemoryStatisticsLogDelaySecs

   :Config: ``storage.inMemory.engineConfig.statisticsLogDelaySecs``
   :Default: 0

   Specifies the number of seconds between writes to statistics log.
   If 0 is specified then statistics are not logged.


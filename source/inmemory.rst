.. _inmemory:

================================================================================
Percona Memory Engine
================================================================================

*Percona Memory Engine* is a special configuration of `WiredTiger`_ that does
not store user data on disk.  Data fully resides in the main memory, making
processing much faster and smoother.  Keep in mind that you need to have enough
memory to hold the data set, and ensure that the server does not shut down.

.. contents::
  :local:
  :depth: 1

The *Percona Memory Engine* is available in |PSMDB| along with the default
MongoDB engine `WiredTiger`_.

Using Percona Memory Engine
================================================================================

As of version 3.2, |PSMDB| runs with `WiredTiger`_ by default.  You can select a
storage engine using the ``--storageEngine`` command-line option when you start
``mongod``.  Alternatively, you can set the ``storage.engine`` variable in the
configuration file (by default, :file:`/etc/mongod.conf`):

.. seealso::

   |mongodb| Documentation: Configuration File Options
      - `storage.engine Options
        <https://docs.mongodb.com/manual/reference/configuration-options/#storage.engine>`_
      - `storage.wiredTiger Options
        <https://docs.mongodb.com/manual/reference/configuration-options/#storage-wiredtiger-options>`_
      - `storage.inmemory Options
        <https://docs.mongodb.com/manual/reference/configuration-options/#storage-inmemory-options>`_

Changing storage engine
-----------------------

If you have data files in your database and want to change to |inmemory|, consider the following:

* Data files created by one storage engine are not compatible with other engines, because each one has its own data model.

* When changing the storage engine, the |mongod| node requires an empty ``dbPath`` data directory when it is restarted. Though |inmemory| stores all data in memory, some metadata files, diagnostics logs and statistics metrics are still written to disk. This is controlled using the :option:`--inMemoryStatisticsLogDelaySecs` option. 

For how to change a storage engine, refer to :ref:`Switching storage engines procedure <switching-storage-procedure>`



Configuring Percona Memory Engine
================================================================================

You can configure the Percona Memory Engine using either command-line options or
corresponding parameters in the :file:`/etc/mongod.conf` file.  The
configuration file is formatted in YAML. For example:

.. code-block:: yaml

   storage:
     engine: inMemory
     inMemory:
       engineConfig:
         inMemorySizeGB: 140
         statisticsLogDelaySecs: 0
  
Setting parameters in the previous example configuration file is the same as
starting the ``mongod`` daemon with the following options:

.. code-block:: bash

   $ mongod --storageEngine=inMemory \
   --inMemorySizeGB=140 \
   --inMemoryStatisticsLogDelaySecs=0

The following options are available (with corresponding YAML configuration file
parameters):

.. option:: --inMemorySizeGB

   :Config: ``storage.inMemory.engineConfig.inMemorySizeGB``
   :Default: 50% of total memory minus 1024 MB, but not less than 256 MB

   Specifies the maximum memory in gigabytes to use for data.

.. option:: --inMemoryStatisticsLogDelaySecs

   :Config: ``storage.inMemory.engineConfig.statisticsLogDelaySecs``
   :Default: 0

   Specifies the number of seconds between writes to statistics log.  If 0 is
   specified then statistics are not logged.

.. include:: .res/url.txt
.. include:: .res/replace.program.txt
.. include:: .res/replace.txt

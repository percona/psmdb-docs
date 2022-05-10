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

.. code-block:: yaml

   storage:
     dbPath: <dataDir>
     engine: inMemory


.. seealso::

   |mongodb| Documentation: Configuration File Options
      - `storage.engine Options
        <https://docs.mongodb.com/manual/reference/configuration-options/#storage.engine>`_
      - `storage.wiredTiger Options
        <https://docs.mongodb.com/manual/reference/configuration-options/#storage-wiredtiger-options>`_
      - `storage.inmemory Options
        <https://docs.mongodb.com/manual/reference/configuration-options/#storage-inmemory-options>`_

.. _switch_storage_engines:

Switching storage engines
=========================

Considerations 
-----------------------

If you have data files in your database and want to change to |inmemory|, consider the following:

* Data files created by one storage engine are not compatible with other engines, because each one has its own data model.

* When changing the storage engine, the |mongod| node requires an empty ``dbPath`` data directory when it is restarted. Though |inmemory| stores all data in memory, some metadata files, diagnostics logs and statistics metrics are still written to disk. This is controlled with the :option:`--inMemoryStatisticsLogDelaySecs` option. 

  Creating a new ``dbPath`` data directory for a different storage engine is the simplest solution. Yet when you switch between disk-using storage engines (e.g. from WiredTiger_ to :ref:`inmemory`), you may have to delete the old data if there is not enough disk space for both. Double-check that your backups are solid and/or the replica set nodes are healthy before you switch to the new storage engine.

Procedure
--------------

To change a storage engine, you have the following options:

* If you simply want to temporarily test Percona Memory Engine, set a different
  data directory for the ``dbPath`` variable in the configuration file.
  Make sure that the user running |mongod| has read and write
  permissions for the new data directory.

  .. code-block:: bash

     $ service mongod stop
     $ # In the configuration file, set the inmemory
     $ # value for the storage.engine variable
     $ # Set the <newDataDir> for the dbPath variable
     $ service mongod start

* If you want to permanently switch to |inmemory| and do not have any
  valuable data in your database, clean out the ``dbPath`` data directory
  (by default, :file:`/var/lib/mongodb`) and edit the configuration file:

  .. code-block:: bash

     $ service mongod stop
     $ rm -rf <dbpathDataDir>
     $ # Update the configuration file by setting the new
     $ # value for the storage.engine variable
     $ # set the engine-specific settings such as
     $ # storage.inMemory.engineConfig.inMemorySizeGB
     $ service mongod start
     
* If there is data that you want to migrate
  and make compatible with Percona Memory Engine,
  use the following methods:

  - for replica sets, use the "rolling restart" process. 
    Switch to the |inmemory| on the secondary node. Clean out the ``dbPath`` data directory and edit the configuration file:

    .. code-block:: bash
		    
       $ service mongod stop
       $ rm -rf <dbpathDataDir>
       $ # Update the configuration file by setting the new
       $ # value for the storage.engine variable
       $ # set the engine-specific settings such as
       $ # storage.inMemory.engineConfig.inMemorySizeGB
       $ service mongod start
    
    Wait for the node to rejoin with the other nodes and report the SECONDARY status.

    Repeat the procedure to switch the remaining nodes to |inmemory|.

  - for a standalone instance or a single-node replica set, use the ``mongodump`` and ``mongorestore`` utilities:

    .. code-block:: bash
		    
       $ mongodump --out <dumpDir>
       $ service mongod stop
       $ rm -rf <dbpathDataDir>
       $ # Update the configuration file by setting the new
       $ # value for the storage.engine variable
       $ # set the engine-specific settings such as
       $ # storage.inMemory.engineConfig.inMemorySizeGB
       $ service mongod start
       $ mongorestore <dumpDir>

Data at Rest Encryption
-----------------------

Using :ref:`psmdb.data-at-rest-encryption` means using the same ``storage.*``
configuration options as for WiredTiger_. To change from normal to :ref:`psmdb.data-at-rest-encryption`
mode or backward, you must clean up the ``dbPath`` data directory,
just as if you change the storage engine. This is because
|mongod| cannot convert the data files to an encrypted format 'in place'. It
must get the document data again either via the initial sync from another
replica set member, or from imported backup dump.

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

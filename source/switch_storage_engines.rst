
.. _switch_storage_engines:

Switching Storage Engines
=========================

By default, |PSMDB| runs with WiredTiger_.
There is also the original MMAPv1_ storage engine,
as well as optional :ref:`inmemory` and :ref:`mongorocks` storage engines
to choose from.
Each one is designed for specific purposes and workloads.

You can select a storage engine
using the ``--storageEngine`` command-line option when you start ``mongod``.
Alternatively, you can set the ``storage.engine`` variable
in the configuration file (by default, :file:`/etc/mongod.conf`).

Data created by one storage engine is not compatible
with other storage engines, because each one has its own data model.
When changing the storage engine, you have to do one of the following:

.. seealso::

   |mongodb| Documentation: Configuration File Options
      - `storage.engine Options
        <https://docs.mongodb.com/manual/reference/configuration-options/#storage.engine>`_
      - `storage.wiredTiger Options
        <https://docs.mongodb.com/manual/reference/configuration-options/#storage-wiredtiger-options>`_
      - `storage.inmemory Options
        <https://docs.mongodb.com/manual/reference/configuration-options/#storage-inmemory-options>`_

Data files created by one storage engine are not compatible with other storage
engines, because each one has its own data model.

When changing the storage engine, the |mongod| node requires an empty ``dbPath``
data directory when it is restarted even when using :ref:`inmemory`.
Though in-memory storage engine stores all data in memory,
some metadata files, diagnostics logs and statistics metrics are still
written to disk. 

Creating a new ``dbPath`` data directory for a different storage engine is the
simplest solution. Yet when you switch between disk-using storage engines (e.g.
from WiredTiger_ to :ref:`inmemory`), you may have to delete the old data if
there is not enough disk space for both. Double-check that your backups are solid
and/or the replica set nodes are healthy before you switch to the new storage
engine.

If there is data that you want to migrate and make compatible with the new
storage engine, use the following methods:

* for replica sets, use the "rolling restart" process. 

  Switch to the new storage engine on the secondary node. Clean out the
  ``dbPath`` data directory (by default , :file:`/var/lib/mongodb`) and edit
  the configuration file:

  .. code-block:: bash

     $ service mongod stop
     $ rm -rf <dbpathDataDir>
     $ # Update the configuration file by setting the new
     $ # value for the storage.engine variable
     $ # set the engine-specific settings such as
     $ # storage.inMemory.engineConfig.inMemorySizeGB
     $ service mongod start
     
  Wait for the node to rejoin with the other replica set members and report the
  SECONDARY status. 

  Repeat the procedure on the remaining nodes.
    
* for a standalone instance or a single-node replica set, use the
  ``mongodump`` and ``mongorestore`` utilities:

  .. code-block:: bash

     $ mongodump --out <dumpDir>
     $ rm -rf <dbpathDataDir>
     $ # Update the configuration file by setting the new
     $ # value for the storage.engine variable
     $ # set the engine-specific settings such as
     $ # storage.wiredTiger.engineConfig.cacheSizeGB or
     $ # storage.inMemory.engineConfig.inMemorySizeGB
     $ service mongod start
     $ mongorestore <dumpDir>
 
Data at Rest Encryption
================================================================================

Using :ref:`psmdb.data-at-rest-encryption` means using the same ``storage.*``
configuration options as for WiredTiger_. To change from normal to :ref:`psmdb.data-at-rest-encryption`
mode or backward, you must clean up the ``dbPath`` data directory,
just as if you change the storage engine. This is because
|mongod| cannot convert the data files to an encrypted format 'in place'. It
must get the document data again either via the initial sync from another
replica set member or from imported backup dump.

.. $The ``storage.rocksdb.counters`` variable must be set to ``true``
.. $if you are running :ref:`mongorocks`
.. $and want to use `Percona Monitoring and Management
.. $<https://www.percona.com/software/database-tools/percona-monitoring-and-management>`_.

.. |mongod| replace:: ``mongod`` 
   
.. include:: .res/replace.txt


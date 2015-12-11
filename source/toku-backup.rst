.. _toku-backup:

==================
Percona TokuBackup
==================

Percona TokuBackup is an integrated open-source hot backup system for |MongoDB| servers running the :ref:`PerconaFT <perconaft>` storage engine (including |Percona Server for MongoDB|). It creates a physical data backup on a running server without performance degradation or capacity planning, and provides a more recent backup than a snapshot at the file system level.

.. contents::
   :local:

Architectural Overview
----------------------

|TokuBackup| copies the data in the ``dbpath`` (and ``logDir`` if different) to a backup directory. The following subsystems are used to complete the backup:

* One component copies files directly, in the background. This component’s I/O consumption can be controlled with the ``backupThrottle`` command.

* The other component ensures consistency between the original database files and the backup copy, even while there are read and write workloads occuring in the database. This is possible because |TokuBackup| is essentially a shim between the ``mongod`` process and the operating system. It intercepts all relvant file system calls, and creates some state in the memory that mirrors the same state in the file system.

Since all writes to database files are applied to their corresponding files in the backup directory, the state of the files in the backup directory is identical to the database files at the time the backup completes. Compare this with backups performed with file system level snapshots, where the backup data is as it was at the beginning of the backup.

Another effect of mirrored writes is that the write I/O done by clients is doubled for the duration of the backup. As Fractal Tree indexes are write-optimized, this is usually not a problem, but is important to know for capacity planning.

Making a Backup
---------------

|TokuBackup| is included with |Percona Server for MongoDB|.

.. note:: |TokuBackup| is available only if you are running the :ref:`PerconaFT storage engine <perconaft>`.

To take a backup of the database files in your current ``dbpath``, you can execute the following command as an administrator on the admin database:

.. code-block:: none

 > use admin
 switched to db admin
 > db.runCommand({backupStart:"/my/backup/data/path"})
 { "ok" : 1 }

You should receive an ``{ "ok" : 1 }`` object as a return value if the backup was successful. If there was an error, you will receive an error message along with failing ``ok`` status. For example:

.. code-block:: none

 > db.runCommand({backupStart:""})
 { "ok" : 0, "errmsg" : "invalid destination directory: ''" }

Checking Backup Progress
------------------------

For long running backups, with lots of data to copy, it is helpful to see how much data the backup process has copied. To see the high level status of a backup use the following command:

.. code-block:: none

 > db.runCommand({backupStatus:1})
 {
        "inProgress" : false,
        "bytesCopied" : NumberLong(0),
        "filesCopied" : 0,
        "ok" : 1
 }

In this case, there is no backup in progress. The ``inProgress`` field will return ``true`` when there is a backup executing. The ``bytesCopied`` and the ``filesCopied`` fields will increase as data is copied from the source files to the backup destination directory.

Controlling Backup Rate
-----------------------

Throttling backups can help reduce the impact on a running server. The rate at which |TokuBackup| copies files from the source directories (like those in your ``dbpath`` setting) can be controlled using the ``backupThrottle`` command.

For example, to limit the backup rate to 128 KB/s, run the following command:

.. code-block:: none

 > db.runCommand({backupThrottle:128000})

.. note:: By default, backup rate is not limited.

Restoring From Backup
---------------------

To restore from backup, simply stop ``mongod`` and run it with ``--dbpath`` option pointing to the location of the backup.

.. note:: The server to which you are restoring must be the same MongoDB version as the one used when you created the backup.

Creating New Replicas
---------------------

A great use case for |TokuBackup| is creating new secondaries in a replica set.

The normal initial sync procedure can use normal queries that need to decompress and deserialize data on disk, and then marshall it and send it across the network, then on the secondary, it needs to be indexed, serialized, and compressed all over again. This is a slow process, and furthermore it poisons the cache of the machine being synced from with data that may be irrelevant to the application.

Instead, a hot backup can be used to initialize a replica set secondary. This is both faster and less intrusive to application queries and the sync source server’s cache.

To create a secondary using |TokuBackup|, move the backup files to the new machine, start the server with the ``--replSet`` option and additionally with ``--fastsync``, then use ``rs.add()`` on the primary to add the new secondary. After the secondary has been added, you should remove the ``--fastsync`` option for future server startups.

.. warning:: In order to find the oplog position in common between the new secondary and the existing members of the set, the oplog must be present in the backup. Therefore, when initially creating a replica set from a single server, it is necessary to run ``rs.initiate()`` first before taking a backup for the new secondary.

.. note:: To minimize impact on a running application, it is recommended to use a backup of an existing secondary to create a new secondary, rather than backing up the primary.

Sharding
--------

Since |TokuBackup| captures the state of a server at the end of the backup operation, it can be difficult to capture a time-consistent backup of multiple shards simultaneously.

The recommended procedure for taking a backup of a sharded cluster in |Percona Server for MongoDB| is to disconnect one secondary from each shard at the same time, then back up those secondaries with any backup procedure. Additionally, one configuration server must be backed up at the same time as well.

For most applications, getting a truly consistent backup of a sharded cluster requires that the application pauses all writes and the balancer, waits for one secondary on each shard to catch up fully with the primary, then disconnects one configuration server and a secondary from each shard. After this, the application can continue (and the balancer as well, once the configuration server has been backed up), and when the backup is finished, the secondaries will need to catch up again.

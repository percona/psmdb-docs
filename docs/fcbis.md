# File copy based initial sync

!!! admonition "Version added: [8.0.12-4](release_notes/8.0.12-4.md)"

When a new member joins the replica set, it receives the data from the existing replica set node via the initial sync. 

In Percona Server for MongoDB, you can choose a file copy-based initial sync (FCBIS) for a new node. You must have WiredTiger defined as the storage. Both source and target nodes must run Percona Server for MongoDB version 8.0.12-4 or higher. 
Note that if you are using v8.0.12-4, the FCBIS feature is available with Pro-Build packages or you should compile from the source to avail this feature. We recommend using the latest available version instead of an older one. See [release notes :octicons-link-external-16:](https://docs.percona.com/percona-server-for-mongodb/8.0/release_notes/8.0.12-4.html#boost-performance-during-cluster-restore-and-scaling-with-file-copy-based-initial-sync) for more details.

The file copy-based initial sync method is a physical copying of the data files from the source to the target. It is much faster than the default [logical initial sync :octicons-link-external-16:](https://www.mongodb.com/docs/manual/core/replica-set-sync/#logical-initial-sync-process) for big datasets (500GB+), which is especially beneficial in heavy write environments. Using this initial sync method speeds up cluster scaling and increases restore performance. 

File copy-based initial sync implementation is compatible with that of MongoDB Enterprise Advanced and has the same [configuration parameters](#configuration-parameters).

To select the initial sync method, specify the `initialSyncMethod` parameter in the configuration file for the target node:

```yaml
setParameter:
  initialSyncMethod: fileCopyBased
```

You can only set this server parameter at startup.

## Workflow

When you start a new node for the replica set, the workflow is the following:

1. The new node (also referred to as the target node) selects the source node for the sync. This sync source is typically the node that responded first and has the passing configuration (e.g. it has WiredTiger set as the storage and the same arrangement of files and indexes as the target node.)
2. The target node opens a backup cursor on the sync source. The backup cursor is used to retrieve the list of files to copy and the timestamp of the oplog end in the metadata file.
3. The file copy starts. During this process the target node lags behind the sync source as it remains operational and its data changes. The sync source node is periodically checked to ensure the time of the lag falls within the defined time.
4. If the lag between the sync source and the target exceeds the defined threshold, the target node executes the `$backupCursorExtend` aggregation to retrieve the changes. Depending on the file copy duration, the target node can execute `$backupCursorExtend` several times, limited by the maximum number of cycles (3 by default)
5. When the files are copied and the lag between the sync source and the target is acceptable, the target node closes the backup cursor. 
6. The target node internally moves the downloaded files to the local `dbPath`, applies oplog on top, reconstructs timestamps to ensure data consistency.

## Configuration parameters

These configuration parameters can be used to control the file copy-based initial sync flow. You can set them only at startup.

| Name | Type | Default | Description |
| --- | --- | --- | --- |
| `initialSyncMethod` | string | logical | Specifies which method of initial sync to use. Valid options are: fileCopyBased, logical. |
| `numInitialSyncAttempts` | integer | 10 | Number of attempts to make at replica set initial synchronization |
| `numInitialSyncConnectAttempts` | integer | 10 | The number of attempts to select and connect to a valid sync source |
| `fileBasedInitialSyncMaxLagSec` | integer | 300 | Specifies the max lag in seconds between the syncing node and the sync source to mark the file copy based initial sync as done successfully |
| `fileBasedInitialSyncMaxCyclesWithoutProgress` | integer | 3 | Specifies the max number of cycles to clone updates while the lag between the syncing node and the sync source is higher than `fileBasedInitialSyncMaxLagSec` |


## Limitations

Using file copy-based initial sync has the following limitations:

* Don't run backups on either sync source or syncing nodes
* Don't write to the `local` database on the syncing node
* You cannot use the same sync source for multiple target nodes simultaneously because only one backup cursor can exist at any moment.
* If you're using encrypted storage, Percona Server for MongoDB applies the encryption key from the sync source node to secure the data on the syncing node.
* You must have WiredTiger defined as the storage engine to run file copy-based initial sync. [Percona memory engine](inmemory.md) is not supported.
* Both source and target nodes must run the same Percona Server for MongoDB version. 





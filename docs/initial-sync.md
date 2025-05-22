# File copy based initial sync

!!! admonition "Version added: [](release_notes/.md)"

When a new member joins the replica set, it receives the data from the primary node via the initial sync. 

The default initial sync method is logical, during which Percona Server for MongoDB clones all databases except the `local` database, builds all collection indexes, pulls oplog records and applies the changes to the data set. Read more about [logical initial sync in MongoDB documentation](https://www.mongodb.com/docs/manual/core/replica-set-sync/#logical-initial-sync-process).

This process may be quite long for large MongoDB data sets. To reduce the time when a new member joins a replica set, you can select **file copy-based** as the initial sync method. 

File copy-based initial sync is the physical copying of the data files from source to target. This sync method is faster than logical, which is especially beneficial in heavy write environments. It enables you to:

* scale your deployment faster, for example, during sudden demand spikes
* increase restore performance, bringing the cluster to operation faster
* have more control over the infrastructure and storage paths in cloud deployments

File copy-based initial sync is included in Percona Server for MongoDB Pro packages that are available for Percona Customers. Become a Percona Customer to enjoy all Pro features. Otherwise, you can receive this feature by [building Percona Server for MongoDB from source](install/source.md).

## Workflow 

Here's how file copy-based initial sync works:

1. When you start a new node, it searches for a sync source. It queries the replica set members and picks the node that responded first and meets the following criteria:

   * Runs Percona Server for MongoDB Pro
   * Has the WiredTiger set as the storage
   * The syncing node and the sync source must have the same values for the `directoryPerDB` and `directoryForIndexes` to ensure the same arrangement  of files and indexes on both of them.

2. The `$backupCursor` is opened on the sync source. The `$backupCursor` returns the files to copy and the `oplogEnd` timestamp. This is the time to apply the oplog after the data copy
3. The syncing node starts copying data files and applies oplog on top of them up to the `oplogEnd` timestamp.
4. During the data copy, data changes can happen on the sync source node. This may result in the lag between the syncing node and the sync source. If this lag is longer than 5 minutes (default), the `$backupCursorExtended` is opened on the sync source.
5. The `$backupCursorExtended` returns the set of changed files, and these files are copied too. This step can repeat, if the lag between the source and target nodes is high. 
6. After the data files copy is complete, the `$backupCursor` and `$backupCursorExtended` are closed, the syncing node completes the sync and joins the replica set as the new member.

File copy-based initial sync implementation is compatible with the one in MongoDB Advanced. For workflow and known limitations, refer to [MongoDB documentation](https://www.mongodb.com/docs/manual/core/replica-set-sync/#file-copy-based-initial-sync).
 
## Configuration

To select the initial sync method, specify the following configuration in the configuration file for the new node:

```yaml
setParameter:
  initialSyncMethod: fileCopyBased
```

You can only set this configuration at startup.

Other configuration options are:

| Parameter               | Data type | Default value | Description |
|-------------------------|-----------|---------------|-------------|
| `numInitialSyncAttempts`| integer   | 10            | The number of attempts for a replica set initial synchronization. |
| `numInitialSyncConnectAttempts` | integer | 10  | The number of attempts to get a valid sync source. If the sync source is not received, the sync method falls back to the logical one. |
| `fileBasedInitialSyncMaxLagSec` | time    | 5 minutes | Maximum lag in seconds before marking initial sync as successful. |
| `fileBasedInitialSyncMaxCyclesWithoutProgress` | integer   | 3 times | Maximum number of cycles trying to clone updates when the lag is above the value of `fileBasedInitialSyncMaxLagSec`. |

You can set these parameters via the `setParameter` command or setting. Learn more about setting Percona Server for MongoDB parameters in the [Parameter tuning guide](set-parameter.md).








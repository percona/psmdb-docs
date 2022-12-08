# $backupCursor and $backupCursorExtend aggregation stages

`$backupCursor` and `$backupCursorExtend` aggregation stages expose the WiredTiger API which allows making consistent backups. Running these stages allows listing and freezing the files so you can copy them without the files being deleted or necessary parts within them being overwritten.


* `$backupCursor` outputs the list of files and their size to copy.

* `$backupCursorExtend` outputs the list of WiredTiger transaction log files that have been updated or newly added since the `$backupCursor` was first run. Saving these files enables restoring the database to any arbitrary time between the `$backupCursor` and `$backupCursorExtend` execution times.

They are available in Percona Server for MongoDB starting with version 4.4.6-8.

Percona provides [Percona Backup for MongoDB (PBM)](https://www.percona.com/doc/percona-backup-mongodb/index.html) – a light-weight open source solution for consistent backups and restores across sharded clusters. PBM relies on these aggregation stages for physical backups and restores. However, if you wish to develop your own backup application, this document describes the `$backupCursor` and `$backupCursorExtend` aggregation stages.

## Usage

You can run these stages in any type of MongoDB deployment. If you need to back up a single node in a replica set, first run the `$backupCursor`, then the `$backupCursorExtend` and save the output files to the backup storage.

To make a consistent backup of a sharded cluster, run both aggregation stages on one node from each shard and the config server replica set. It can be either the primary or the secondary node. Note that since the secondary node may lag in syncing the data from the primary one, you will have to wait for the exact same time before running the `$backupCursorExtend`.

Note that for standalone MongoDB node with disabled oplogs, you can only run the `$backupCursor` aggregation stage.

### Get a list of all files to copy with $backupCursor

```javascript
var bkCsr = db.getSiblingDB("admin").aggregate([{$backupCursor: {}}])
bkCsrMetadata = bkCsr.next().metadata
```

Sample output:

```json
{
  "metadata" : {
     "backupId": UUID("35c34101-0107-44cf-bdec-fad285e07534"),
     "dbpath": '/var/lib/mongodb',
     "oplogStart": { ts: Timestamp({ t: 1666631297, i: 1 }), t: Long("-1") },
     "oplogEnd": { ts: Timestamp({ t: 1666631408, i: 1 }), t: Long("1") },
     "checkpointTimestamp": Timestamp({ t: 1666631348, i: 1 })
     "disableIncrementalBackup" : false,
     "incrementalBackup" : false,
     "blockSize" : 16
  }
}
```

Store the `metadata` document somewhere, because you need to pass the `backupId` parameter from this document as the input parameter for the `$backupCursorExtend` stage. Also you need the `oplogEnd` timestamp.
Make sure that the `$backupCursor` is complete on all shards in your cluster.

!!! note 

    Note that when running `$backupCursor` in a standalone node deployment, `oplogStart`, `oplogEnd`, `checkpointTimesatmp` values may be absent. This is because standalone node deployments don’t have oplogs.

### Run `$backupCursorExtend` to retrieve the WiredTiger transaction logs

Pass the `backupId` from the metadata document as the first parameter. For the `timestamp` parameter, use the maximum (latest) value among the `oplogEnd` timestamps from all shards and config server replica set. This will be the target time to restore.

```javascript
var bkExtCsr = db.aggregate([{$backupCursorExtend: {backupId: bkCsrMetadata.backupId, timestamp: new Timestamp(1666631418, 1)}}])
```

Sample output:

```default
{ "filename" : "/data/plain_rs/n1/data/journal/WiredTigerLog.0000000042" }
{ "filename" : "/data/plain_rs/n1/data/journal/WiredTigerLog.0000000043" }
{ "filename" : "/data/plain_rs/n1/data/journal/WiredTigerLog.0000000044" }
```

### Loop the `$backupCursor`

Prevent the backup cursor from closing on timeout (default – 10 minutes). This is crucial since it prevents overwriting backup snapshot file blocks with new ones if the files take longer than 10 minutes to copy.  Use the [getMore](https://www.mongodb.com/docs/v6.0/reference/command/getMore/#getmore) command for this purpose.

### Copy the files to the storage

Now you can copy the output of both aggregation stages to your backup storage.

After the backup is copied to the storage, terminate the [getMore](https://www.mongodb.com/docs/v6.0/reference/command/getMore/#getmore) command and close the cursor.

!!! note 

    Save the timestamp that you passed for the `$backupCursorExtend` stage somewhere since you will need it for the restore.

!!! admonition ""

    This document is based on the blog post [Experimental Feature: $backupCursorExtend in Percona Server for MongoDB](https://www.percona.com/blog/2021/06/07/experimental-feature-backupcursorextend-in-percona-server-for-mongodb/) by Akira Kurogane
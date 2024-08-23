# File copy based initial sync

!!! admonition "Version added: [7.0.14-8](release_notes/7.0.14-8.md)"

When a new member joins the replica set, it receives the data from the primary node via the initial sync. 

The default initial sync method is logical, during which Percona Server for MongoDB clones all databases except the `local` database, builds all collection indexes, pulls oplog records and applies the changes to the data set. Read more about [logical initial sync in MongoDB documentation](https://www.mongodb.com/docs/manual/core/replica-set-sync/#logical-initial-sync-process).

Starting with version 7.0.12, you can select **file copy based** as the initial sync method. This is the physical copying of the data files from source to target. This sync method is faster than logical, which is especially beneficial in heavy write environments. It speeds up cluster scaling and increases restore performance.

File copy-based initial sync is implemented in the same way as in MongoDB Enterprise. For workflow and known limitations, refer to [MongoDB documentation](https://www.mongodb.com/docs/manual/core/replica-set-sync/#file-copy-based-initial-sync). 

To select the initial sync method, specify the following configuration in the configuration file for the target server:

```yaml
setParameter:
  initialSyncMethod: fileCopyBased
```

You can only set this configuration at startup.


File copy based initial sync is available in [Percona Server for MongoDB Pro out of the box](psmdb-pro.md). You can also receive this functionality by [building Percona Server for MongoDB from source code](install/source.md). 




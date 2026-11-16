# Percona Memory Engine

Percona Memory Engine is a special configuration of [WiredTiger](https://docs.mongodb.org/manual/core/wiredtiger/) that does
not store user data on disk. Data fully resides in the main memory, making
processing much faster and smoother. Keep in mind that you need to have enough
memory to hold the data set, and ensure that the server does not shut down.

The Percona Memory Engine is available in Percona Server for MongoDB, along with the default MongoDB
engine WiredTiger.

## Usage

Percona Server for MongoDB runs with WiredTiger by default. You can select a
storage engine using the `--storageEngine` command-line option when you start
`mongod`. Alternatively, you can set the `storage.engine` variable in the
configuration file (by default, `/etc/mongod.conf`):

```yaml
storage:
  dbPath: <dataDir>
  engine: inMemory
```

## Configuration

You can configure Percona Memory Engine using either command-line options or corresponding parameters in the `/etc/mongod.conf` file. 

The following options are available (with corresponding YAML configuration file parameters):

| Configuration file | {{ optionlink('storage.inMemory.engineConfig.inMemorySizeGB') }}|
|--------------------| ---------------|
| **Command line**   | `--inMemorySizeGB=<value>` |
| **Default**        | 50% of total memory minus 1024 MB, but not less than 256 MB | 
| **Description**    | Specifies the maximum memory in gigabytes to use for data |

| Configuration file | {{ optionlink('storage.inMemory.engineConfig.statisticsLogDelaySecs') }}|
|--------------------| ---------------|
| **Command line**   | `--inMemoryStatisticsLogDelaySecs=<value>` |
| **Default**        | 0 | 
| **Description**    | Specifies the number of seconds between writes to the statistics log.  A 0 value means statistics are not logged |


### Examples

The following are the configuration examples:

=== ":octicons-file-code-24: Configuration file"
    
    The configuration file is formatted in YAML

    ```yaml
    storage:
      engine: inMemory
      inMemory:
        engineConfig:
          inMemorySizeGB: 140
          statisticsLogDelaySecs: 0
    ```

=== ":material-console: Command line"

     Setting parameters in the configuration file is the same as
     starting the `mongod` daemon with the following options:

     ```sh
     mongod --storageEngine=inMemory \
     --inMemorySizeGB=140 \
     --inMemoryStatisticsLogDelaySecs=0
     ```

### How WiredTiger settings apply

When you select `storage.engine: inMemory`, Percona Memory Engine inherits WiredTiger settings, with exceptions for memory size, statistics logging, and custom configuration strings. Use the following tables when configuring the engine or migrating a configuration from MongoDB Enterprise Advanced.

The `storage.inMemory` settings take precedence over the corresponding
`storage.wiredTiger` settings. 

This also applies when you omit an InMemory setting: the engine uses its InMemory default, not the WiredTiger value.

In the following table, option names are relative to `storage`. 

For example, `inMemory.engineConfig.inMemorySizeGB` means
`storage.inMemory.engineConfig.inMemorySizeGB`.

| WiredTiger setting | Setting to use for Percona Memory Engine |
| --- | --- |
| `wiredTiger.engineConfig.cacheSizeGB` | `inMemory.engineConfig.inMemorySizeGB` |
| `wiredTiger.engineConfig.cacheSizePct` | `inMemory.engineConfig.inMemorySizeGB`; the WiredTiger percentage does not control the InMemory memory limit. |
| `wiredTiger.engineConfig.statisticsLogDelaySecs` | `inMemory.engineConfig.statisticsLogDelaySecs` |
| `wiredTiger.engineConfig.configString` | `inMemory.engineConfig.configString` |
| `wiredTiger.collectionConfig.configString` | `inMemory.collectionConfig.configString` |
| `wiredTiger.indexConfig.configString` | `inMemory.indexConfig.configString` |

The custom configuration strings in the WiredTiger section do not carry over to the InMemory section. If you use custom strings, review the settings before moving them to the corresponding `storage.inMemory` options. Percona Memory Engine enforces `cache_resident=false` for collection and index configurationm strings.

Other WiredTiger settings remain available, but some have no effect on the InMemory engine. The following table describes the settings relevant to this configuration change. Option names are relative to `storage.wiredTiger`.

| WiredTiger setting | Behavior with Percona Memory Engine |
| --- | --- |
| `engineConfig.zstdCompressionLevel` | Inherited as the compression level for the `zstd` compressor. |
| `engineConfig.directoryForIndexes` | Inherited and recorded in storage metadata. |
| `collectionConfig.blockCompressor` | Inherited as the default block compressor for collections. |
| `indexConfig.prefixCompression` | Inherited as the default prefix compression setting for indexes. |
| `engineConfig.journalCompressor` | Has no effect because the InMemory engine disables journaling. |
| `engineConfig.checkpointSizeMB` | Has no effect on the InMemory engine, which disables checkpoints. |
| `engineConfig.liveRestoreSource`, `engineConfig.liveRestoreThreads`, `engineConfig.liveRestoreReadSizeMB` | Have no effect because live restore is not enabled for the InMemory engine. |
| `engineConfig.maxCacheOverflowFileSizeGB` | Deprecated; has no effect on storage engine operation. |

The `setParameter` settings `wiredTigerSessionMax`,
`wiredTigerEvictionDirtyTargetGB`, `wiredTigerEvictionDirtyMaxGB`, and
`wiredTigerEvictionUpdatesMaxGB` also apply to Percona Memory Engine. Keep
these settings under `setParameter`, not under `storage.inMemory`.

??? example "Example with inherited settings"

    This example sets a 3 GB memory limit and enables statistics logging every two seconds. It also sets the inherited collection and index compression options.
    
    The values are illustrative. Choose a memory limit that fits your data set and available memory.

    ```yaml
    storage:
      engine: inMemory
      inMemory:
        engineConfig:
          inMemorySizeGB: 3
          statisticsLogDelaySecs: 2
      wiredTiger:
        engineConfig:
          zstdCompressionLevel: 6
        collectionConfig:
          blockCompressor: zstd
        indexConfig:
          prefixCompression: true
    ```

    When switching from another storage engine, setting these options alone does not migrate existing data. Follow the [storage engine switching procedure](#switching-storage-engines).

## Switching storage engines

### Considerations

If you have data files in your database and want to change to Percona Memory Engine, consider the following:

* Data files created by one storage engine are not compatible with other engines, because each one has its own data model.

* When changing the storage engine, the `mongod` node requires an empty `dbPath` data directory when it is restarted. Though Percona Memory Engine stores all data in memory, some metadata files, diagnostics logs, and statistics metrics are still written to disk. This is controlled with the `--inMemoryStatisticsLogDelaySecs` option.

Creating a new `dbPath` data directory for a different storage engine is the simplest solution. Yet when you switch between disk-using storage engines (e.g. from [WiredTiger](https://docs.mongodb.org/manual/core/wiredtiger/) to Percona Memory Engine), you may have to delete the old data if there is not enough disk space for both. Double-check that your backups are solid and/or the replica set nodes are healthy before you switch to the new storage engine.

* In addition to running as standalones, `mongod` instances that use Percona Memory Engine storage can run as part of a Replica Set and be part of a sharded cluster.

### Procedure

To change a storage engine, you have the following options:

#### Temporarily test Percona Memory Engine
  
Set a different data directory for the `dbPath` variable in the configuration file. Make sure that the user running `mongod` has read and write permissions for the new data directory.

1. Stop `mongod`

    ```bash
    service mongod stop
    ```

2. Edit the configuration file

    ```yaml
    storage:
      dbPath: <newDataDir>
      engine: inmemory
    ```

3. Start `mongod`

    ```bash
    service mongod start
    ```


#### Permanent switch to Percona Memory Engine without any valuable data in your database

Clean out the `dbPath` data directory (by default, `/var/lib/mongodb`) and edit the configuration file:

1. Stop `mongod`

    ```bash
    service mongod stop
    ```

2. Clean out the `dbPath` data directory

    ```bash
    sudo rm -rf <dbpathDataDir>
    ```

3. Edit the configuration file

    ```yaml
    storage:
      dbPath: <newDataDir>
      engine: inmemory
    ```

4. Start `mongod`

    ```bash
    service mongod start
    ```

#### Switch to Percona Memory Engine with data migration and compatibility

=== "Standalone or single-node Replica Set"

    For a standalone instance or a single-node replica set, use the `mongodump` and `mongorestore` utilities:

    1. Export the `dataDir` contents

        ```bash
        mongodump --out <dumpDir>
        ```

    2. Stop `mongod`

        ```bash
        service mongod stop
        ```

    3. Clean out the `dbPath` data directory

        ```bash
        sudo rm -rf <dbpathDataDir>
        ```

    4. Update the configuration file by setting the new
    value for the `storage.engine` variable. Set the engine-specific settings such as `storage.inMemory.engineConfig.inMemorySizeGB`

    5. Start `mongod`

        ```bash
        service mongod start
        ```
    
    6. Restore the database

        ```bash
        mongorestore <dumpDir>
        ```

=== "Replica Set"

    Use the “rolling restart” process.

    1. Switch to the Percona Memory Engine on the secondary node. Clean out the `dbPath` data directory and edit the configuration file:

       1. Stop `mongod`

           ```bash
           service mongod stop
           ```

       2. Clean out the `dbPath` data directory

           ```bash
           sudo rm -rf <dbpathDataDir>
           ```

       3. Edit the configuration file

           ```yaml
           storage:
             dbPath: <newDataDir>
             engine: inmemory
           ```

       4. Start `mongod`

           ```bash
           service mongod start
           ```

    2. Wait for the node to rejoin with the other nodes and report the SECONDARY status.

    3. Repeat the procedure to switch the remaining nodes to Percona Memory Engine.


## Data at rest encryption

Using [Data at Rest Encryption](data-at-rest-encryption.md) means using the same `storage.\*`
configuration options as for [WiredTiger](https://docs.mongodb.org/manual/core/wiredtiger/). To change from normal to [Data at Rest Encryption](data-at-rest-encryption.md) mode or backward, you must clean up the `dbPath` data directory, just as if you change the storage engine. This is because `mongod` cannot convert the data files to an encrypted format **in place**. It
must get the document data again, either via the initial sync from another
replica set member or from an imported backup.


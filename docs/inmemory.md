# Percona Memory Engine

Percona Memory Engine is a special configuration of [WiredTiger](https://docs.mongodb.org/manual/core/wiredtiger/) that does
not store user data on disk. Data fully resides in the main memory, making
processing much faster and smoother. Keep in mind that you need to have enough
memory to hold the data set, and ensure that the server does not shut down.

The Percona Memory Engine is available in Percona Server for MongoDB along with the default MongoDB engine [WiredTiger](https://docs.mongodb.org/manual/core/wiredtiger/).

## Usage

As of version 3.2, Percona Server for MongoDB runs with [WiredTiger](https://docs.mongodb.org/manual/core/wiredtiger/) by default. You can select a
storage engine using the `--storageEngine` command-line option when you start
`mongod`.  Alternatively, you can set the `storage.engine` variable in the
configuration file (by default, `/etc/mongod.conf`):

```yaml
storage:
  dbPath: <dataDir>
  engine: inMemory
```

## Configuration

You can configure Percona Memory Engine using either command-line options or
corresponding parameters in the `/etc/mongod.conf` file. The following are the configuration examples:

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

### Options

The following options are available (with corresponding YAML configuration file
parameters):

| Configuration file | {{ optionlink('storage.inMemory.engineConfig.inMemorySizeGB') }}|
|--------------------| ---------------|
| **Command line**   | `inMemorySizeGB()` |
| **Default**        | 50% of total memory minus 1024 MB, but not less than 256 MB | 
| **Description**    | Specifies the maximum memory in gigabytes to use for data |

| Configuration file | {{ optionlink('storage.inMemory.engineConfig.statisticsLogDelaySecs') }}|
|--------------------| ---------------|
| **Command line**   | `inMemoryStatisticsLogDelaySecs()()` |
| **Default**        | 0 | 
| **Description**    | Specifies the number of seconds between writes to statistics log.  A 0 value means statistics are not logged |


## Switching storage engines

### Considerations

If you have data files in your database and want to change to Percona Memory Engine, consider the following:


* Data files created by one storage engine are not compatible with other engines, because each one has its own data model.

* When changing the storage engine, the `mongod` node requires an empty `dbPath` data directory when it is restarted. Though Percona Memory Engine stores all data in memory, some metadata files, diagnostics logs and statistics metrics are still written to disk. This is controlled with the `--inMemoryStatisticsLogDelaySecs` option.

Creating a new `dbPath` data directory for a different storage engine is the simplest solution. Yet when you switch between disk-using storage engines (e.g. from [WiredTiger](https://docs.mongodb.org/manual/core/wiredtiger/) to Percona Memory Engine), you may have to delete the old data if there is not enough disk space for both. Double-check that your backups are solid and/or the replica set nodes are healthy before you switch to the new storage engine.

### Procedure

To change a storage engine, you have the following options:

#### Temporarily test Percona Memory Engine
  
Set a different data directory for the `dbPath` variable in the configuration file. Make sure that the user running `mongod` has read and write permissions for the new data directory.

1. Stop `mongod`

    ```{.bash data-prompt="$"}
    $ service mongod stop
    ```

2. Edit the configuration file

    ```yaml
    storage:
      dbPath: <newDataDir>
      engine: inmemory
    ```

3. Start `mongod`

    ```{.bash data-prompt="$"}
    $ service mongod start
    ```


#### Permanent switch to Percona Memory Engine without any valuable data in your database

Clean out the `dbPath` data directory (by default, `/var/lib/mongodb`) and edit the configuration file:

1. Stop `mongod`

    ```{.bash data-prompt="$"}
    $ service mongod stop
    ```

2. Clean out the `dbPath` data directory

    ```{.bash data-prompt="$"}
    $ sudo rm -rf <dbpathDataDir>
    ```

3. Edit the configuration file

    ```yaml
    storage:
      dbPath: <newDataDir>
      engine: inmemory
    ```

4. Start `mongod`

    ```{.bash data-prompt="$"}
    $ service mongod start
    ```

#### Switch to Percona Memory Engine with data migration and compatibility

=== "Standalone instance"

    For a standalone instance or a single-node replica set, use the `mongodump` and `mongorestore` utilities:

    1. Export the `dataDir` contents

        ```{.bash data-prompt="$"}
        $ mongodump --out <dumpDir>
        ```

    2. Stop `mongod`

        ```{.bash data-prompt="$"}
        $ service mongod stop
        ```

    3. Clean out the `dbPath` data directory

        ```{.bash data-prompt="$"}
        $ sudo rm -rf <dbpathDataDir>
        ```

    4. Update the configuration file by setting the new
    value for the `storage.engine` variable. Set the engine-specific settings such as `storage.inMemory.engineConfig.inMemorySizeGB`

    5. Start `mongod`

        ```{.bash data-prompt="$"}
        $ service mongod start
        ```
    
    6. Restore the database

        ```{.bash data-prompt="$"}
        $ mongorestore <dumpDir>
        ```

=== "Replica set"

    Use the “rolling restart” process.

    1. Switch to the Percona Memory Engine on the secondary node. Clean out the `dbPath` data directory and edit the configuration file:

       1. Stop `mongod`

           ```{.bash data-prompt="$"}
           $ service mongod stop
           ```

       2. Clean out the `dbPath` data directory

           ```{.bash data-prompt="$"}
           $ sudo rm -rf <dbpathDataDir>
           ```

       3. Edit the configuration file

           ```yaml
           storage:
             dbPath: <newDataDir>
             engine: inmemory
           ```

       4. Start `mongod`

           ```{.bash data-prompt="$"}
           $ service mongod start
           ```

    2. Wait for the node to rejoin with the other nodes and report the SECONDARY status.

    3. Repeat the procedure to switch the remaining nodes to Percona Memory Engine.


### Data at rest encryption

Using [Data at Rest Encryption](data-at-rest-encryption.md) means using the same `storage.\*`
configuration options as for [WiredTiger](https://docs.mongodb.org/manual/core/wiredtiger/). To change from normal to [Data at Rest Encryption](data-at-rest-encryption.md) mode or backward, you must clean up the `dbPath` data directory, just as if you change the storage engine. This is because
**mongod** cannot convert the data files to an encrypted format ‘in place’. It
must get the document data again either via the initial sync from another
replica set member, or from imported backup dump.


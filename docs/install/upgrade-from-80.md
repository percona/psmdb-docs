# Upgrading from Percona Server for MongoDB 8.0 to 8.3

## Considerations

1. To upgrade Percona Server for MongoDB to version 8.3, you must be running version 8.0. Upgrades from earlier versions are not supported.

2. Before upgrading your production Percona Server for MongoDB deployments, test all your applications
in a testing environment to make sure they are compatible with the new version.

Review the [Compatibility Changes in MongoDB 8.2 :octicons-link-external-16:](https://www.mongodb.com/docs/manual/release-notes/8.3-compatibility/){:target="_blank"} and [Compatibility Changes in MongoDB 8.3 :octicons-link-external-16:](https://www.mongodb.com/docs/manual/release-notes/8.3-compatibility/){:target="_blank"} before you begin the upgrade.

3. If you run Amazon Linux 2023, consider the following:

    --8<-- "al-compatibility.md"


## Prerequisites

Before the upgrade, do the following:

1. Make a full backup of your data and configuration files

2. In Percona Server for MongoDB 8.3, journaling is enabled by default. Both the `storage.journal.enabled` configuration option and the corresponding `--journal`, `--no-journal` command-line options are ignored. You receive the corresponding warning during the server start after the upgrade. To get rid of this warning, change your configuration to remove the journaling options. 

=== ":material-debian: Upgrade on Debian and Ubuntu"

     1. Stop the `mongod` service:

          ```bash
          sudo systemctl stop mongod
          ```

     2. Enable Percona repository for Percona Server for MongoDB 8.3:

         ```bash
         sudo percona-release enable psmdb-83
         ```

     3. Update the local cache:

         ```bash
         sudo apt update
         ```

     4. Remove the following configuration from the configuration file, if you have it:

         ```yaml
         processManagement:
            fork: true
            pidFilePath: /var/run/mongod.pid
         ```
         
     5. Install Percona Server for MongoDB 8.3 packages:

         ```bash
         sudo apt install percona-server-mongodb
         ```

     6. Start the `mongod` instance:

         ```bash
         sudo systemctl start mongod
         ```

     For more information, see [Installing Percona Server for MongoDB on Debian and Ubuntu](apt.md).

=== ":material-redhat: Upgrade on Red Hat Enterprise Linux and derivatives"

     1. Stop the `mongod` service:

          ```bash
          sudo systemctl stop mongod
          ```

     2. Enable Percona repository for Percona Server for MongoDB 8.3:

         ```bash
         sudo percona-release enable psmdb-83
         ``` 

     3. Remove the following configuration from the configuration file, if you have it:

         ```yaml
         processManagement:
            fork: true
            pidFilePath: /var/run/mongod.pid
         ```

     4. Install Percona Server for MongoDB 8.3 packages:

         ```bash
         sudo yum install percona-server-mongodb
         ```

     5. Start the `mongod` instance:

         ```bash
         sudo systemctl start mongod
         ```

After the upgrade, Percona Server for MongoDB is started with the feature set of 8.0 version. Assuming that your applications are compatible with the new version, enable 8.3 version features. Run the following command against the `admin` database:

```javascript 
db.adminCommand( { setFeatureCompatibilityVersion: "8.0", confirm: true } )
```

!!! admonition "See also"

    MongoDB Documentation:

    * [Upgrade a Standalone](https://www.mongodb.com/docs/manual/release-notes/8.3-upgrade-from-8.0-standalone/)
    * [Upgrade a Replica Set](https://www.mongodb.com/docs/manual/release-notes/8.3-upgrade-from-8.0-replica-set/)
    * [Upgrade a Sharded Cluster](https://www.mongodb.com/docs/manual/release-notes/8.3-upgrade-from-8.0-sharded-cluster/)

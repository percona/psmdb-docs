# Upgrading from Percona Server for MongoDB 7.0 to 8.0

## Considerations

To upgrade Percona Server for MongoDB to version 8.0, you must be running version
7.0. Upgrades from earlier versions are not supported.

2. Before upgrading your production Percona Server for MongoDB deployments, test all your applications
in a testing environment to make sure they are compatible with the new version.
For more information, see [Compatibility Changes in MongoDB 8.0](https://www.mongodb.com/docs/v8.0/release-notes/8.0-compatibility/)

3. If you are using data-at-rest-encryption with KMIP server, check the [upgrade considerations](../kmip.md#upgrade-considerations)

We recommend to upgrade Percona Server for MongoDB from official Percona repositories using [`percona-release` repository management tool](https://docs.percona.com/percona-software-repositories/index.html) and
the corresponding package manager for your system. 

This document describes this method for the in-place upgrade (where your existing
data and configuration files are preserved).

## Prerequisites

Before the upgrade, do the following:

1. Make a full backup of your data and configuration files

2. In Percona Server for MongoDB 8.0, journaling is enabled by default. Both the `storage.journal.enabled` configuration option and the corresponding `--journal`, `--no-journal` command-line options are ignored. You receive the corresponding warning during the server start after the upgrade. To get rid of this warning, change your configuration to remove the journaling options. 

=== ":material-debian: Upgrade on Debian and Ubuntu"

     1. Stop the `mongod` service:

          ```{.bash data-prompt="$"}
          $ sudo systemctl stop mongod
          ```

     2. Enable Percona repository for Percona Server for MongoDB 8.0:

         ```{.bash data-prompt="$"}
         $ sudo percona-release enable psmdb-80
         ```

     3. Update the local cache:

         ```{.bash data-prompt="$"}
         $ sudo apt update
         ```

     4. Install Percona Server for MongoDB 8.0 packages:

         ```{.bash data-prompt="$"}
         $ sudo apt install percona-server-mongodb
         ```

     5. Start the `mongod` instance:

         ```{.bash data-prompt="$"}
         $ sudo systemctl start mongod
         ```

     For more information, see [Installing Percona Server for MongoDB on Debian and Ubuntu](apt.md).

=== ":material-redhat: Upgrade on Red Hat Enterprise Linux and derivatives"

     1. Stop the `mongod` service:

          ```{.bash data-prompt="$"}
          $ sudo systemctl stop mongod
          ```

     2. Enable Percona repository for Percona Server for MongoDB 8.0:

         ```{.bash data-prompt="$"}
         $ sudo percona-release enable psmdb-80
         ``` 

     3. Install Percona Server for MongoDB 8.0 packages:

         ```{.bash data-prompt="$"}
         $ sudo yum install percona-server-mongodb
         ```

     4. Start the `mongod` instance:

         ```{.bash data-prompt="$"}
         $ sudo systemctl start mongod
         ```

After the upgrade, Percona Server for MongoDB is started with the feature set of 7.0 version. Assuming that your applications are compatible with the new version, enable 8.0 version features. Run the following command against the `admin` database:

```{.javascript data-prompt=">"}
> db.adminCommand( { setFeatureCompatibilityVersion: "8.0" } )
```

!!! admonition "See also"

    MongoDB Documentation:

    * [Upgrade a Standalone](https://docs.mongodb.com/manual/release-notes/8.0-upgrade-standalone/)
    * [Upgrade a Replica Set](https://docs.mongodb.com/manual/release-notes/8.0-upgrade-replica-set/)
    * [Upgrade a Sharded Cluster](https://docs.mongodb.com/manual/release-notes/8.0-upgrade-sharded-cluster/)

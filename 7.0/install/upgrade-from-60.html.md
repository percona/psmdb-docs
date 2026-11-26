> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server-for-mongodb/7.0/llms.txt).

# Upgrading from Percona Server for MongoDB 6.0 to 7.0

## Considerations

1.To upgrade Percona Server for MongoDB to version 7.0, you must be running version 6.0. Upgrades from earlier versions are not supported.

1. Before upgrading your production Percona Server for MongoDB deployments, test all your applications in a testing environment to make sure they are compatible with the new version. For more information, see [Compatibility Changes in MongoDB 7.0](https://www.mongodb.com/docs/v7.0/release-notes/7.0-compatibility/)

1. If you are using data-at-rest-encryption with KMIP server, check the [upgrade considerations](https://docs.percona.com/percona-server-for-mongodb/7.0/kmip.md#upgrade-considerations)

1. If you run Amazon Linux 2023, consider the following:

   We build and test Percona Server for MongoDB only on the latest versions of Amazon Linux 2023. Because of the way Amazon Linux updates their libraries, Percona Server for MongoDB works only on specific Amazon Linux versions.

   The following table shows Percona Server for MongoDB versions that are supported on specific versions of Amazon Linux 2023:

   | Percona Server for MongoDB version | Amazon Linux 2023 version |
   | ---------------------------------- | ------------------------- |
   | 7.0.16-10                          | 2023.6.x and earlier      |
   | 7.0.18-11                          | 2023.7.x and newer        |

   To upgrade Percona Server for MongoDB, make sure that you run a compatible version of Amazon Linux 2023. Use the [update instructions](https://docs.aws.amazon.com/linux/al2023/ug/updating.html) to update the operating system.

We recommend to upgrade Percona Server for MongoDB from official Percona repositories using [`percona-release` repository management tool](https://docs.percona.com/percona-software-repositories/index.html) and the corresponding package manager for your system.

This document describes this method for the in-place upgrade (where your existing data and configuration files are preserved).

## Prerequisites

Before the upgrade, do the following:

1. Make a full backup of your data and configuration files
1. In Percona Server for MongoDB 7.0, journaling is enabled by default. Both the `storage.journal.enabled` configuration option and the corresponding `--journal`, `--no-journal` command-line options are ignored. You receive the corresponding warning during the server start after the upgrade. To get rid of this warning, change your configuration to remove the journaling options.

**Upgrade on Debian and Ubuntu**

1. Stop the `mongod` service:

   ```bash
   sudo systemctl stop mongod
   ```

1. Enable Percona repository for Percona Server for MongoDB 7.0:

   ```bash
   sudo percona-release enable psmdb-70
   ```

1. Update the local cache:

   ```bash
   sudo apt update
   ```

1. Install Percona Server for MongoDB 7.0 packages:

   ```bash
   sudo apt install percona-server-mongodb
   ```

1. Start the `mongod` instance:

   ```bash
   sudo systemctl start mongod
   ```

For more information, see [Installing Percona Server for MongoDB on Debian and Ubuntu](https://docs.percona.com/percona-server-for-mongodb/7.0/install/apt.md).

**Upgrade on Red Hat Enterprise Linux and derivatives**

1. Stop the `mongod` service:

   ```bash
   sudo systemctl stop mongod
   ```

1. Enable Percona repository for Percona Server for MongoDB 7.0:

   ```bash
   sudo percona-release enable psmdb-70
   ```

1. Install Percona Server for MongoDB 7.0 packages:

   ```bash
   sudo yum install percona-server-mongodb
   ```

1. Start the `mongod` instance:

   ```bash
   sudo systemctl start mongod
   ```

After the upgrade, Percona Server for MongoDB is started with the feature set of 6.0 version. Assuming that your applications are compatible with the new version, enable 7.0 version features. Run the following command against the `admin` database:

```javascript
> db.adminCommand( { setFeatureCompatibilityVersion: "7.0", confirm: true } )
```

See also

MongoDB Documentation:

- [Upgrade a Standalone](https://docs.mongodb.com/manual/release-notes/7.0-upgrade-standalone/)
- [Upgrade a Replica Set](https://docs.mongodb.com/manual/release-notes/7.0-upgrade-replica-set/)
- [Upgrade a Sharded Cluster](https://docs.mongodb.com/manual/release-notes/7.0-upgrade-sharded-cluster/)

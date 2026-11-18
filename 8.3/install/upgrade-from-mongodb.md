> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server-for-mongodb/8.3/llms.txt).

# Upgrade from MongoDB Community Edition to Percona Server for MongoDB

This document provides instructions for an in-place upgrade from MongoDB Community Edition to Percona Server for MongoDB.

An in-place upgrade is done by keeping the existing data in the server and replacing the MongoDB binaries. Afterwards, you restart the `mongod` service with the same `dbpath` data directory.

An in-place upgrade is suitable for most environments except the ones that use ephemeral storage and/or host addresses.

## Procedure

Note

MongoDB creates a user that belongs to two groups, which is a potential security risk. This is fixed in Percona Server for MongoDB: the user is included only in the `mongod` group. To avoid problems with current MongoDB setups, existing user group membership is not changed when you migrate to Percona Server for MongoDB. Instead, a new `mongod` user is created during installation, and it belongs to the `mongod` group.

This procedure describes an in-place upgrade of a `mongod` instance. If you are using data at rest encryption, refer to the [Upgrading to Percona Server for MongoDB with data at rest encryption enabled](#upgrading-to-percona-server-for-mongodb-with-data-at-rest-encryption-enabled) section.

Important

Before starting the upgrade, we recommend to perform a full backup of your data.

**Upgrade on Debian and Ubuntu**

1. Save the current configuration file as the backup:

   ```
   sudo mv /etc/mongod.conf /etc/mongod.conf.bkp
   ```

1. Stop the `mongod` service:

   ```
   sudo systemctl stop mongod
   ```

1. Check for installed packages:

   ```
   sudo dpkg -l | grep mongod
   ```

   Sample output

   ```
   ii  mongodb-org                      8.3.7                       amd64        MongoDB open source document-oriented database system (metapackage)
   ii  mongodb-org-database             8.3.7                       amd64        MongoDB open source document-oriented database system (metapackage)
   ii  mongodb-org-database-tools-extra 8.3.7                       amd64        Extra MongoDB database tools
   ii  mongodb-org-mongos               8.3.7                       amd64        MongoDB sharded cluster query router
   ii  mongodb-org-server               8.3.7                       amd64        MongoDB database server
   ii  mongodb-org-shell                8.3.7                       amd64        MongoDB shell client
   ii  mongodb-org-tools                8.3.7                       amd64        MongoDB tools
   ```

1. Remove the installed packages:

   ```
   sudo apt remove \
     mongodb-org \
     mongodb-org-mongos \
     mongodb-org-server \
     mongodb-org-shell \
     mongodb-org-tools
   ```

1. [Install Percona Server for MongoDB](https://docs.percona.com/percona-server-for-mongodb/8.3/install/apt.html).

1. Verify that the configuration file includes correct options:

   - Copy the required configuration options like custom dbPath/system log path, additional security/replication or sharding options from the backup configuration file (`/etc/mongod.conf`) to the current one `/etc/mongodb.conf`.

   - Make sure that the `mongod` user has access to your custom paths. If not, provide it as follows:

     ```
     sudo chown -R mongod:mongod <custom-dbPath>
     sudo chown -R mongod:mongod <custom-systemLog.path>
     ```

   - Remove the following configuration from the configuration file if you have it:

     ```
     processManagement:
        fork: true
        pidFilePath: /var/run/mongod.pid
     ```

1. Restart the `mongod` service:

   ```
   sudo systemctl start mongod
   ```

**Upgrade on Red Hat Enterprise Linux and derivatives**

1. Stop the `mongod` service:

   ```
   sudo systemctl stop mongod
   ```

1. Check for installed packages:

   ```
   sudo rpm -qa | grep mongo
   ```

   Sample output

   ```
    mongodb-org-shell-8.3.7-1.el9.x86_64
    mongodb-org-database-8.3.7-1.el9.x86_64
    mongodb-org-8.3.7-1.el9.x86_64
    mongodb-database-tools-100.17.0-1.x86_64
    mongodb-org-server-8.3.7-1.el9.x86_64
   mongodb-org-mongos-8.3.7-1.el9.x86_64
   mongodb-org-tools-8.3.7-1.el9.x86_64
   ```

1. Remove the installed packages:

   ```
   sudo yum remove \
   mongodb-org-shell-8.3.7-1.el9.x86_64 \
   mongodb-org-database-8.3.7-1.el9.x86_64 \
   mongodb-org-8.3.7-1.el9.x86_64 \
   mongodb-database-tools-100.17.0-1.x86_64 \
   mongodb-org-server-8.3.7-1.el9.x86_64 \
   mongodb-org-mongos-8.3.7-1.el9.x86_64 \
   mongodb-org-tools-8.3.7-1.el9.x86_64
   ```

1. [Install Percona Server for MongoDB](https://docs.percona.com/percona-server-for-mongodb/8.3/install/yum.html).

1. Verify that the configuration file includes correct options:

   - When you remove old packages, your existing configuration file is saved as `/etc/mongod.conf.rpmsave`. Copy the required configuration options like custom dbPath/system log path, additional security/replication or sharding options from the backup configuration file (`/etc/mongod.conf.rpmsave`) to the current one `/etc/mongodb.conf`.

   - Make sure that the `mongod` user has access to your custom paths. If not, provide it as follows:

     ```
     sudo chown -R mongod:mongod <custom-dbPath>
     sudo chown -R mongod:mongod <custom-systemLog.path>
     ```

   - Make sure the configuration file includes the following configuration:

     ```
     processManagement:
        fork: true
        pidFilePath: /var/run/mongod.pid
     ```

     **Troubleshooting tip**: The `pidFilePath` setting in `mongod.conf` must match the `PIDFile` option in the `systemd mongod` service unit. Otherwise, the service will kill the `mongod` process after a timeout.

1. Restart the `mongod` service:

   ```
   sudo systemctl start mongod
   ```

To upgrade a replica set or a sharded cluster, use the [rolling restart](https://docs.percona.com/percona-server-for-mongodb/8.3/glossary.html#rolling-restart) method. It allows you to perform the upgrade with minimum downtime. You upgrade the nodes one by one, while the whole cluster / replica set remains operational.

See also

MongoDB Documentation:

- [Upgrade a Replica Set](https://docs.mongodb.com/manual/release-notes/8.0-upgrade-replica-set/)
- [Upgrade a Sharded Cluster](https://docs.mongodb.com/manual/release-notes/8.0-upgrade-sharded-cluster/)

## Upgrading to Percona Server for MongoDB with data at rest encryption enabled

Steps to upgrade from MongoDB 8.0 Community Edition with data encryption enabled to Percona Server for MongoDB are different. `mongod` requires an empty `dbPath` data directory because it cannot encrypt data files in place. It must receive data from other replica set members during the initial sync. Please refer to the [Switching storage engines](https://docs.percona.com/percona-server-for-mongodb/8.3/inmemory.html#switching-storage-engines) for more information on migration of encrypted data. [Contact us](https://www.percona.com/about-percona/contact#us) for working at the detailed migration steps, if further assistance is needed.

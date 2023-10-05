# Upgrade Percona Server for MongoDB

An in-place upgrade is done by keeping the existing data in the server. It involves changing out the MongoDB binaries. Generally speaking, the upgrade steps include:

1. Stopping the `mongod` service
2. Removing the old binaries
3. Installing the new server version binaries
4. Restarting the `mongod` service with the same `dbpath` data directory.

An in-place upgrade is suitable for most environments except the ones that use ephemeral storage and/or host addresses.

This document provides upgrade instructions for the following use cases:

* [Upgrading from MongoDB 7.0 Community Edition](#upgrading-from-mongodb-70-community-edition)

* [Minor upgrade of Percona Server for MongoDB](#minor-upgrade-of-percona-server-for-mongodb)

## Upgrading from MongoDB 7.0 Community Edition

!!! note 

    MongoDB creates a user that belongs to two groups, which is a potential security risk.  This is fixed in Percona Server for MongoDB: the user is included only in the `mongod` group.  To avoid problems with current MongoDB setups, existing user group membership is not changed when you migrate to Percona Server for MongoDB.  Instead, a new `mongod` user is created during installation, and it belongs to the `mongod` group.

This section describes an in-place upgrade of a `mongod` instance. If you are using data at rest encryption, refer to the [Upgrading to Percona Server for MongoDB with data at rest encryption enabled](#upgrading-to-percona-server-for-mongodb-with-data-at-rest-encryption-enabled) section.

### Prerequisites

Before you start the upgrade, update the MongoDB configuration file
(`/etc/mongod.conf`) to contain the following settings.

```yaml
processManagement:
   fork: true
   pidFilePath: /var/run/mongod.pid
```

**Troubleshooting tip**: The `pidFilePath` setting in `mongod.conf` must  match the `PIDFile` option in the `systemd mongod` service unit. Otherwise, the service will kill the `mongod` process after a timeout.

!!! warning

    Before starting the upgrade, we recommend to perform a full backup of your data.

=== "Upgrade on Debian and Ubuntu"

     1. Stop the `mongod` service:

         ```{.bash data-prompt="$"}
         $ sudo systemctl stop mongod
         ```

     2. Check for installed packages:

         ```{.bash data-prompt="$"}
         $ sudo dpkg -l | grep mongod
         ```

         Output:

         ```{.text .no-copy}
         ii  mongodb-org                      7.0.2                       amd64        MongoDB open source document-oriented database system (metapackage)
         ii  mongodb-org-database             7.0.2                       amd64        MongoDB open source document-oriented database system (metapackage)
         ii  mongodb-org-database-tools-extra 7.0.2                       amd64        Extra MongoDB database tools
         ii  mongodb-org-mongos               7.0.2                       amd64        MongoDB sharded cluster query router
         ii  mongodb-org-server               7.0.2                       amd64        MongoDB database server
         ii  mongodb-org-shell                7.0.2                       amd64        MongoDB shell client
         ii  mongodb-org-tools                7.0.2                       amd64        MongoDB tools
         ```

     3. Remove the installed packages:

         ```{.bash data-prompt="$"}
         $ sudo apt remove \
           mongodb-org \
           mongodb-org-mongos \
           mongodb-org-server \
           mongodb-org-shell \
           mongodb-org-tools
         ```

     4. Remove log files:

         ```{.bash data-prompt="$"}
         $ sudo rm -r /var/log/mongodb
         ```
     5. [Install Percona Server for MongoDB](apt.md)

     6. Verify that the configuration file includes the correct options. For example, Percona Server for MongoDB stores data files in /var/lib/mongodb by default. If you used another dbPath data directory, edit the configuration file accordingly

     7. Start the `mongod` service:

         ```{.bash data-prompt="$"}
         $ sudo systemctl start mongod
         ```

=== "Upgrade on Red Hat Enterprise Linux and derivatives"

     1. Stop the `mongod` service:

         ```{.bash data-prompt="$"}
         $ sudo systemctl stop mongod
         ```

     2. Check for installed packages:

         ```{.bash data-prompt="$"}
         $ sudo rpm -qa | grep mongo
         ```

         Output:

         ```{.text .no-copy}
         mongodb-org-shell-7.0.2-1.el9.x86_64
         mongodb-org-database-7.0.2-1.el9.x86_64
         mongodb-org-7.0.2-1.el8.x86_64
         mongodb-database-tools-100.4.1-1.x86_64
         mongodb-org-server-7.0.2-1.el9.x86_64
         mongodb-org-mongos-7.0.2-1.el9.x86_64
         mongodb-org-tools-7.0.2-1.el9.x86_64
         ```

     3. Remove the installed packages:

         ```{.bash data-prompt="$"}
         $ sudo yum remove \
         mongodb-org-shell-7.0.2-1.el9.x86_64
         mongodb-org-database-7.0.2-1.el9.x86_64
         mongodb-org-7.0.2-1.el9.x86_64
         mongodb-database-tools-100.4.1-1.x86_64
         mongodb-org-server-7.0.2-1.el8.x86_64
         mongodb-org-mongos-7.0.2-1.el8.x86_64
         mongodb-org-tools-7.0.2-1.el8.x86_64
         ```
     
     4. Remove log files:

         ```{.bash data-prompt="$"}
         $ sudo rm -r /var/log/mongodb
         ```

     5. [Install Percona Server for MongoDB](yum.md)

        !!! note

            When you remove old packages, your existing configuration file is saved as `/etc/mongod.conf.rpmsave`. If you want to use this configuration with the new version, replace the default `/etc/mongod.conf` file. For example, existing data may not be compatible with the default WiredTiger storage engine.

    6. Start the `mongod` service:

        ```{.bash data-prompt="$"}
        $ sudo systemctl start mongod
        ```

To upgrade a replica set or a sharded cluster, use the [rolling restart](../glossary.md#rolling-restart) method. It allows you to perform the upgrade with minimum downtime. You upgrade the nodes one by one, while the whole cluster / replica set remains operational.

!!! admonition "See also"

    MongoDB Documentation:

    * [Upgrade a Replica Set](https://docs.mongodb.com/manual/release-notes/7.0-upgrade-replica-set/)
    * [Upgrade a Sharded Cluster](https://docs.mongodb.com/manual/release-notes/7.0-upgrade-sharded-cluster/)

## Minor upgrade of Percona Server for MongoDB

To upgrade Percona Server for MongoDB to the latest version, follow these steps:


1. Stop the `mongod` service:

    ```{.bash data-prompt="$"}
    $ sudo systemctl stop mongod
    ```

2. [Install the latest version packages](index.md). Use the command relevant to your operating system.

3. Start the `mongod` service:

    ```{.bash data-prompt="$"}
    $ sudo systemctl start mongod
    ```

To upgrade a replica set or a sharded cluster, use the [rolling restart](../glossary.md#term-Rolling-restart) method. It allows you to perform the upgrade with minimum downtime. You upgrade the nodes one by one, while the whole cluster / replica set remains operational.

## Upgrading to Percona Server for MongoDB with data at rest encryption enabled

Steps to upgrade from MongoDB 6.0 Community Edition with data encryption enabled to Percona Server for MongoDB are different. `mongod` requires an empty `dbPath` data directory because it cannot encrypt data files in place. It must receive data from other replica set members during the initial sync. Please refer to the [Switching storage engines](../inmemory.md#switching-storage-engines) for more information on migration of encrypted data. [Contact us](https://www.percona.com/about-percona/contact#us) for working at the detailed migration steps, if further assistance is needed.


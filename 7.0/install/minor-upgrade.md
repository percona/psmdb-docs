> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server-for-mongodb/7.0/llms.txt).

# Minor upgrade of Percona Server for MongoDB

## Upgrade considerations

1. If you are using data-at-rest-encryption with KMIP server, check the [upgrade considerations](https://docs.percona.com/percona-server-for-mongodb/7.0/kmip.html#upgrade-considerations)

1. If you run Amazon Linux 2023, consider the following:

   We build and test Percona Server for MongoDB only on the latest versions of Amazon Linux 2023. Because of the way Amazon Linux updates their libraries, Percona Server for MongoDB works only on specific Amazon Linux versions.

   The following table shows Percona Server for MongoDB versions that are supported on specific versions of Amazon Linux 2023:

   | Percona Server for MongoDB version | Amazon Linux 2023 version |
   | ---------------------------------- | ------------------------- |
   | 7.0.16-10                          | 2023.6.x and earlier      |
   | 7.0.18-11                          | 2023.7.x and newer        |

   To upgrade Percona Server for MongoDB, make sure that you run a compatible version of Amazon Linux 2023. Use the [update instructions](https://docs.aws.amazon.com/linux/al2023/ug/updating.html) to update the operating system.

## Procedure

To upgrade Percona Server for MongoDB to the latest version, follow these steps:

1. Stop the `mongod` service:

   ```
   sudo systemctl stop mongod
   ```

1. [Install the latest version packages](https://docs.percona.com/percona-server-for-mongodb/7.0/install/index.html). Use the command relevant to your operating system.

1. Start the `mongod` service:

   ```
   sudo systemctl start mongod
   ```

To upgrade a replica set or a sharded cluster, use the [rolling restart](https://docs.percona.com/percona-server-for-mongodb/7.0/glossary.html#rolling-restart) method. It allows you to perform the upgrade with minimum downtime. You upgrade the nodes one by one, while the whole cluster / replica set remains operational.

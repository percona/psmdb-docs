# What's next?

Congratulations with your first hands-on experience with Percona Server for MongoDB. 

To deepen your knowledge in working with the database, see the MongoDB documentation on [aggregation](https://www.mongodb.com/docs/manual/aggregation/), [indexes](https://www.mongodb.com/docs/manual/indexes/), [data modelling](https://www.mongodb.com/docs/manual/data-modeling/), [transactions](https://www.mongodb.com/docs/manual/core/transactions/).

The following sections help you achieve your organization's goals on:

## High availability

Having multiple copies of data on different servers provides redundancy and high availability. Deploying MongoDB [replica sets](https://www.mongodb.com/docs/current/replication/) serves this purpose. Replica sets also increase data availability and provide fault tolerance against the loss of a database instance.

[Replica set deployment](https://www.mongodb.com/docs/current/administration/replica-set-deployment/){.md-button}

## Scalability

Ensure your database handles the increasing load without performance degradation as your data set grows. The [sharding](https://www.mongodb.com/docs/current/sharding/) method in MongoDB is the distribution of data across multiple servers where each server handles a subset of data. This is the horizontal scaling mechanism where you can add additional servers if needed for a lower overall cost than upgrading existing hardware. The tradeoff is in complex infrastructure management.

[Deploy a sharded cluster](https://www.mongodb.com/docs/current/tutorial/deploy-shard-cluster/){.md-button} 

## Encryption

Protecting your data from unauthorized access is crucial. Introducing data-at-rest encryption helps protect sensitive information when it is stored on storage devices, such as hard drives, solid-state drives, or other types of persistent storage. Percona Server for MongoDB is integrated with several external key managers.

[Data-at-rest encryption](data-at-rest-encryption.md){.md-button} 

## Backup and restore

Protect your database against data loss by implementing the backup strategy. You can either use the built-in [hot backup feature](hot-backup.md) or consider deploying Percona Backup for MongoDB - an open source solution for making consistent backups and restores in sharded clusters and replica sets.

[Percona Backup for MongoDB](https://docs.percona.com/percona-backup-mongodb/installation.html){.md-button}

## Monitoring

Get insights into the database health and performance using Percona Monitoring and Management (PMM) - an open-source database monitoring, management, and observability solution for MySQL, PostgreSQL, and MongoDB. It allows you to observe the health of your database systems, explore new patterns in their behavior, troubleshoot them and perform database management operations 

[Get started with PMM](https://docs.percona.com/percona-monitoring-and-management/quickstart/index.html){.md-button}

## Advanced command line tools

Perform sophisticated database management and administration tasks using Percona toolkit - the collection of advanced command-line tools developed and tested by Percona as an alternative to private or “one-off” scripts.

[Get Percona Toolkit](https://docs.percona.com/percona-toolkit/installation.html){.md-button}



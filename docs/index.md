# Percona Server for MongoDB 6.0 Documentation

Percona Server for MongoDB is a free, enhanced, fully compatible, source available, drop-in replacement
for MongoDB 6.0 Community Edition with enterprise-grade features.
It requires no changes to MongoDB applications or code.

!!! hint ""

    To see which version of Percona Server for MongoDB you are using check the value of the `psmdbVersion` key in the output of the [buildInfo](https://docs.mongodb.com/manual/reference/command/buildInfo/#dbcmd.buildInfo) database command. If this key does not exist, Percona Server for MongoDB is not installed on the server.

!!! note ""

    This is the documentation for the latest release, **Percona Server for MongoDB {{release}}** ([Release Notes](release_notes/{{release}}.md)).

## Features

Percona Server for MongoDB provides the following features:


* MongoDB’s default [WiredTiger](https://docs.mongodb.org/manual/core/wiredtiger/) engine

* [Percona Memory Engine](inmemory.md) storage engine

* [Data at Rest Encryption](data-at-rest-encryption.md)

* [External authentication](authentication.md#ext-auth)
using OpenLDAP or Active Directory

* [AWS IAM authentication](aws-iam.md) (a [technical preview feature](glosary.md#technical-preview-feature))

* [Audit logging](audit-logging.md) to track and query database interactions of users or applications

* [Hot Backup](hot-backup.md) for the default [WiredTiger](https://docs.mongodb.org/manual/core/wiredtiger/)

* [Profiling Rate Limit](rate-limit.md) to decrease the impact of the profiler on performance

To learn more about the features, available in Percona Server for MongoDB, see [Percona Server for MongoDB Feature Comparison](comparison.md)


## Get started

* [Install Percona Server for MongoDB](install/index.md)
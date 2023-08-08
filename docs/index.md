# Percona Server for MongoDB 6.0 Documentation

Percona Server for MongoDB is a free, enhanced, fully compatible, source available, drop-in replacement
for MongoDB 6.0 Community Edition with enterprise-grade features.
It requires no changes to MongoDB applications or code.

!!! hint ""

    To see which version of Percona Server for MongoDB you are using check the value of the `psmdbVersion` key in the output of the [buildInfo](https://docs.mongodb.com/manual/reference/command/buildInfo/#dbcmd.buildInfo) database command. If this key does not exist, Percona Server for MongoDB is not installed on the server.


!!! important

    **Changes to Chunk Management and Balancing**

    Several changes have been incrementally introduced within 6.0.x releases.

    * The name of a subset of data has changed from a `chunk` to a `range`. 
    * The data size has changed from 64 MB for a chunk to 128 MB for a range.

    * The balancer now distributes ranges based on the actual data size of collections. Formerly the balancer migrated and balanced data across shards based strictly on the number of chunks of data that exist for a collection across each shard. This, combined with the auto-splitter process could cause quite a heavy performance impact to heavy write environments. 

    * Ranges (formerly chunks) are no longer auto-split. They are split only when they move across shards for distribution purposes. The auto-splitter process is currently still available but it serves no purpose and does nothing active to the data. This also means that the Enable/Disable AutoSplit helpers should no longer be used. 

    The above changes are expected to lead to better performance overall going forward.

[What's new in Percona Server for MongoDB {{release}}](release_notes/{{release}}.md){ .md-button .md-button }
    
## Features

Percona Server for MongoDB provides the following features:


* MongoDB’s default [WiredTiger](https://docs.mongodb.org/manual/core/wiredtiger/) engine

* [Percona Memory Engine](inmemory.md) storage engine

* [Data at Rest Encryption](data-at-rest-encryption.md)

* [External authentication](authentication.md#ext-auth)
using OpenLDAP or Active Directory

* [AWS IAM authentication](aws-iam.md) (a [technical preview feature](glossary.md#technical-preview-feature))

* [Audit logging](audit-logging.md) to track and query database interactions of users or applications

* [Hot Backup](hot-backup.md) for the default [WiredTiger](https://docs.mongodb.org/manual/core/wiredtiger/)

* [Profiling Rate Limit](rate-limit.md) to decrease the impact of the profiler on performance

To learn more about the features, available in Percona Server for MongoDB, see [Percona Server for MongoDB Feature Comparison](comparison.md)


## Get started

Ready to try out Percona Server for MongoDB?


[Install and get started](install/index.md){ .md-button .md-button }
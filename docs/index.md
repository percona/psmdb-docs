# Percona Server for MongoDB 6.0 Documentation

Percona Server for MongoDB is a free, enhanced, fully compatible, source available, drop-in replacement
for MongoDB 6.0 Community Edition with [enterprise-grade features](comparison.md).
It requires no changes to MongoDB applications or code.

[What's new in Percona Server for MongoDB {{release}}](release_notes/{{release}}.md){ .md-button .md-button }


!!! important

    **Changes to Chunk Management and Balancing**

    Several changes have been incrementally introduced within 6.0.x releases.

    * The name of a subset of data has changed from a `chunk` to a `range`. 
    * The data size has changed from 64 MB for a chunk to 128 MB for a range.

    * The balancer now distributes ranges based on the actual data size of collections. Formerly the balancer migrated and balanced data across shards based strictly on the number of chunks of data that exist for a collection across each shard. This, combined with the auto-splitter process could cause quite a heavy performance impact to heavy write environments. 

    * Ranges (formerly chunks) are no longer auto-split. They are split only when they move across shards for distribution purposes. The auto-splitter process is currently still available but it serves no purpose and does nothing active to the data. This also means that the Enable/Disable AutoSplit helpers should no longer be used. 

    The above changes are expected to lead to better performance overall going forward.

## What's in it for you?

* Enterprise-grade security features help you ensure your data stays safe
* High-availability and scalability help you meet your enterprise application needs
* Get [visibility into user and process actions](audit-logging.md) and [redact sensitive information from log files](log-redaction.md).
* Enjoy simplified backup and observability management with the natively integrated [Percona Backup for MongoDB](https://docs.percona.com/percona-backup-mongodb/index.html) and [Percona Monitoring and Management](https://www.percona.com/doc/percona-monitoring-and-management/2.x/index.html) solutions.  

<div data-grid markdown><div data-banner markdown>

## :material-progress-download: Installation guides { .title }

Ready to try out Percona Server for MongoDB? Get started quickly with the step-by-step installation instructions.

[Quickstart guides :material-arrow-right:](install/index.md){ .md-button }

</div><div data-banner markdown>

### :fontawesome-solid-gears: Secure access to database { .title }

Define who has access to the database, ensuring only authorized users have access to resources and operations. 

[Authentication :material-arrow-right:](authentication.md){.md-button}
</div><div data-banner markdown>

### :material-backup-restore: Backup management { .title }

Create physical backups on a running server without notable performance degradation.

[Hot backup :material-arrow-right:](hot-backup.md){ .md-button }

</div>
</div>    



# Percona Server for MongoDB 6.0 Documentation

Percona Server for MongoDB is an enhanced, fully compatible, source available, drop-in replacement
for MongoDB 6.0 Community Edition with [enterprise-grade features](comparison.md).
[To migrate to Percona Server for MongoDB](install/upgrade-from-mongodb.md) requires no changes to MongoDB applications or code.

[What's new in Percona Server for MongoDB {{release}}](release_notes/{{release}}.md){ .md-button .md-button }


!!! important

    **Changes to Chunk Management and Balancing**

    Several changes have been incrementally introduced within 6.0.x releases.

    * The name of a subset of data has changed from a `chunk` to a `range`. 
    * The data size has changed from 64 MB for a chunk to 128 MB for a range.

    * The balancer now distributes ranges based on the actual data size of collections. Formerly the balancer migrated and balanced data across shards based strictly on the number of chunks of data that exist for a collection across each shard. This, combined with the auto-splitter process could cause quite a heavy performance impact to heavy write environments. 

    * Ranges (formerly chunks) are no longer auto-split. They are split only when they move across shards for distribution purposes. The auto-splitter process is currently still available but it serves no purpose and does nothing active to the data. This also means that the Enable/Disable AutoSplit helpers should no longer be used. 

    The above changes are expected to lead to better performance overall going forward.
  

<div data-grid markdown><div data-banner markdown>

## :material-progress-download: Installation guides { .title }

Ready to try out Percona Server for MongoDB? Get started quickly with the step-by-step installation instructions.

[Quickstart guides :material-arrow-right:](install/index.md){ .md-button }

</div><div data-banner markdown>

### :fontawesome-solid-gears: Control database access { .title }

Define who has access to the database and manage their permissions in a single place like LDAP server, ensuring only authorized users have access to resources and operations. 

[Authentication :material-arrow-right:](authentication.md){.md-button}
</div><div data-banner markdown>

### :material-backup-restore: Backup and restore { .title }

Make enterprise-level backups and restores with guaranteed data consistency using Percona Backup for MongoDB (PBM). Or, create physical backups on a running server using the built-in [hot backup](hot-backup.md) functionality. 

[Get started with PBM :material-arrow-right:](https://docs.percona.com/percona-backup-mongodb/installation.html){ .md-button }

</div><div data-banner markdown>

### :simple-letsencrypt: Secure access to data { .title }

Keep your sensitive data safe, ensuring users only see the data they are authorized to access. 

[Data-at-rest encryption :material-arrow-right:](data-at-rest-encryption.md){ .md-button }

</div>
</div>    



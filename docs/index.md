# Percona Server for MongoDB 8.0 Documentation

Percona Server for MongoDB is an enhanced, fully compatible, source available, drop-in replacement
for MongoDB 8.0 Community Edition with [enterprise-grade features](comparison.md).

[To migrate to Percona Server for MongoDB](install/upgrade-from-mongodb.md) requires no changes to MongoDB applications or code.

!!! hint ""

    To see which version of Percona Server for MongoDB you are using check the value of the `psmdbVersion` key in the output of the [buildInfo](https://docs.mongodb.com/manual/reference/command/buildInfo/#dbcmd.buildInfo) database command. If this key does not exist, Percona Server for MongoDB is not installed on the server.


[What's new in Percona Server for MongoDB {{release}}](release_notes/{{release}}.md){ .md-button .md-button }
    
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
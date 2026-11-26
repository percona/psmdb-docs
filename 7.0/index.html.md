> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server-for-mongodb/7.0/llms.txt).

# Percona Server for MongoDB 7.0 Documentation

Percona Server for MongoDB is an enhanced, fully compatible, source available, drop-in replacement for MongoDB 7.0 Community Edition with [enterprise-grade features](https://docs.percona.com/percona-server-for-mongodb/7.0/comparison.md).

[To migrate to Percona Server for MongoDB](https://docs.percona.com/percona-server-for-mongodb/7.0/install/upgrade-from-mongodb.md) requires no changes to MongoDB applications or code.

To see which version of Percona Server for MongoDB you are using check the value of the `psmdbVersion` key in the output of the [buildInfo](https://docs.mongodb.com/manual/reference/command/buildInfo/#dbcmd.buildInfo) database command. If this key does not exist, Percona Server for MongoDB is not installed on the server.

[What’s new in Percona Server for MongoDB 7.0.48-25](https://docs.percona.com/percona-server-for-mongodb/7.0/release_notes/7.0.48-25.md)

## Installation guides

Ready to try out Percona Server for MongoDB? Get started quickly with the step-by-step installation instructions.

[Quickstart guides](https://docs.percona.com/percona-server-for-mongodb/7.0/install/index.md)

### Control database access

Define who has access to the database and manage their permissions in a single place like LDAP server, ensuring only authorized users have access to resources and operations.

[Authentication](https://docs.percona.com/percona-server-for-mongodb/7.0/authentication.md)

### Backup and restore

Make enterprise-level backups and restores with guaranteed data consistency using Percona Backup for MongoDB (PBM). Or, create physical backups on a running server using the built-in [hot backup](https://docs.percona.com/percona-server-for-mongodb/7.0/hot-backup.md) functionality.

[Get started with PBM](https://docs.percona.com/percona-backup-mongodb/installation.html)

### Secure access to data

Keep your sensitive data safe, ensuring users only see the data they are authorized to access.

[Data-at-rest encryption](https://docs.percona.com/percona-server-for-mongodb/7.0/data-at-rest-encryption.md)

# Back up with Percona Backup for MongoDB

Percona Server for MongoDB 9.0.8-1 removes the built-in `createBackup` command.
Use [Percona Backup for MongoDB (PBM)](https://docs.percona.com/percona-backup-mongodb/latest/index.html) instead.

## Prepare your backup workflow

Before you upgrade to Percona Server for MongoDB 9.0, replace `createBackup` calls in scripts and scheduled jobs.
The removal applies to all `createBackup` destinations: local directories, archive files, and S3-compatible storage.

PBM supports consistent backups and restores for replica sets and sharded clusters.
PBM does not support standalone MongoDB instances.
For deployment requirements, see [Supported MongoDB deployments](https://docs.percona.com/percona-backup-mongodb/latest/details/deployments.html).

To prepare your PBM backup workflow:
{.power-number}

1. Check the [PBM compatibility matrix](https://docs.percona.com/percona-backup-mongodb/latest/details/versions.html) for support for your server version and backup type.

2. Follow the [PBM quickstart](https://docs.percona.com/percona-backup-mongodb/latest/installation.html) for PBM installation and configuration.

3. Choose a [backup type](https://docs.percona.com/percona-backup-mongodb/latest/features/backup-types.html) that meets your backup and restore requirements.

4. Replace `createBackup` calls with the corresponding PBM backup workflow.

5. Verify backups and restores in a test environment before you upgrade production servers.

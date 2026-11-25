# Upgrade from Percona Server for MongoDB 8.0 to {{psmdb_version}}

## Considerations


1. Upgrade Percona Server for MongoDB 8.0 deployments to {{psmdb_version}}.
   For earlier major versions, upgrade to 8.0 first.

2. Test your applications with {{psmdb_version}} before you upgrade production deployments.
   Review [MongoDB {{psmdb_version}} compatibility changes](https://www.mongodb.com/docs/v{{psmdb_version}}/release-notes/{{psmdb_version}}-compatibility/).

3. Enable Transparent Hugepages (THP) before you start Percona Server for MongoDB {{psmdb_version}}.
   See [Enable THP](https://www.mongodb.com/docs/manual/administration/tcmalloc-performance/#enable-transparent-hugepages--thp-).

4. For data-at-rest encryption with a KMIP server, check the [upgrade considerations](../kmip.md#upgrade-considerations).

5. If you run Amazon Linux 2023, consider the following:

    {{render_snippet('al-compatibility.md') | indent(4)}}


Use the official Percona repositories and your operating system package manager for the upgrade.
Manage the repositories with [`percona-release`](https://docs.percona.com/percona-software-repositories/index.html).

The package commands apply to standalone deployments.
For replica sets and sharded clusters, follow the corresponding [upstream upgrade procedure](#see-also).
Preserve your data and configuration files during the upgrade.

## Prerequisites

Before the upgrade, do the following:

1. Make a full backup of your data and configuration files

2. Verify that your deployment uses feature compatibility version (FCV) `8.0`:

    ```javascript
    db.adminCommand({ getParameter: 1, featureCompatibilityVersion: 1 })
    ```

    Resolve an incomplete 8.0 upgrade before you install {{psmdb_version}} binaries.

=== ":material-debian: Upgrade on Debian and Ubuntu"

     1. Stop the `mongod` service:

          ```bash
          sudo systemctl stop mongod
          ```

     2. Enable Percona repository for Percona Server for MongoDB {{psmdb_version}}:

         ```bash
         sudo percona-release enable psmdb-{{psmdb_version | replace(".", "")}}
         ```

     3. Update the local cache:

         ```bash
         sudo apt update
         ```

     4. Remove these `processManagement` options from your configuration file when present:

         ```yaml
         processManagement:
            fork: true
            pidFilePath: /var/run/mongod.pid
         ```

     5. Install Percona Server for MongoDB {{psmdb_version}} packages:

         ```bash
         sudo apt install percona-server-mongodb
         ```

     6. Start the `mongod` instance:

         ```bash
         sudo systemctl start mongod
         ```

     For more information, see [Installing Percona Server for MongoDB on Debian and Ubuntu](apt.md).

=== ":material-redhat: Upgrade on Red Hat Enterprise Linux and derivatives"

     1. Stop the `mongod` service:

          ```bash
          sudo systemctl stop mongod
          ```

     2. Enable Percona repository for Percona Server for MongoDB {{psmdb_version}}:

         ```bash
         sudo percona-release enable psmdb-{{psmdb_version | replace(".", "")}}
         ```

     3. Remove these `processManagement` options from your configuration file when present:

         ```yaml
         processManagement:
            fork: true
            pidFilePath: /var/run/mongod.pid
         ```

     4. Install Percona Server for MongoDB {{psmdb_version}} packages:

         ```bash
         sudo yum install percona-server-mongodb
         ```

     5. Start the `mongod` instance:

         ```bash
         sudo systemctl start mongod
         ```

Retain FCV `8.0` while you test the upgraded deployment.
To enable {{psmdb_version}} features after you finish the tests, run this command against the `admin` database:

```javascript
db.adminCommand( { setFeatureCompatibilityVersion: "{{psmdb_version}}", confirm: true } )
```

## See also

MongoDB documentation:

- [Upgrade a Standalone](https://www.mongodb.com/docs/v{{psmdb_version}}/release-notes/{{psmdb_version}}-upgrade-standalone/)

- [Upgrade a Replica Set](https://www.mongodb.com/docs/v{{psmdb_version}}/release-notes/{{psmdb_version}}-upgrade-replica-set/)

- [Upgrade a Sharded Cluster](https://www.mongodb.com/docs/v{{psmdb_version}}/release-notes/{{psmdb_version}}-upgrade-sharded-cluster/)

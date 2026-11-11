# Telemetry and data collection

Percona collects usage data to improve its software. The telemetry feature helps us identify popular features, detect problems, and plan future improvements. 

Currently, telemetry is added only to the Percona packages for both basic and Pro builds and to Docker images. 

## What information is collected

Telemetry collects the following information:

* The information about the installation environment when you install the software.
* The information about the operating system such as OS name, the architecture, the list of Percona packages. See more in the [Telemetry Agent section](#telemetry-agent).
* The metrics from the database instance. See more in the [Telemetry Subsystem section](#telemetry-subsystem).

## What is NOT collected

Percona protects your privacy and doesn't collect any personal information about you like database names, user names or credentials or any user-entered values. 

All collected data is anonymous, meaning it can't be traced back to any individual user. To learn more about how Percona handles your data, read the [Percona Privacy statement](https://www.percona.com/privacy-policy).

You control whether to share this information. Participation in this program is completely voluntary. If don't want to share anonymous data, you can [disable telemetry](#disable-telemetry).

## Why telemetry matters

Benefits for Percona:

| Advantages                  | Description                                                                                                                                                         |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| See how people use your software | Telemetry collects anonymous data on how users interact with our software. This tells developers which features are popular, which ones are confusing, and if anything is causing crashes. |
| Identify issues early       | Telemetry can catch bugs or performance problems before they become widespread. |

Benefits for users in the long run:

| Advantages                | Description                                                                                                         |
|---------------------------|---------------------------------------------------------------------------------------------------------------------|
| Faster bug fixes          | With telemetry data, developers can pinpoint issues affecting specific users and prioritize fixing them quickly.  |
| Improved features           | Telemetry helps developers understand user needs and preferences. This allows them to focus on features that will be genuinely useful and improve your overall experience. |
| Improved user experience  | By identifying and resolving issues early, telemetry helps create a more stable and reliable software experience for everyone. |

## Telemetry components

Percona collects information using the following components:

* Telemetry script that sends the information about the software and the environment where it is installed. This information is collected only once during the installation.

* The Telemetry Subsystem collects the necessary metrics directly from the database and stores them in a Metrics File.

* The Metrics File stores the metrics and is a standalone file located on the database host's file system.

* The Telemetry Agent is an independent process running on your database host's operating system and carries out the following tasks:

    * Collects OS-level metrics

    * Reads the Metrics File, adds the OS-level metrics

    * Sends the full set of metrics to the Percona Platform

    * Collects the list of installed Percona packages using the local package manager

The telemetry also uses the Percona Platform with the following components:

* Telemetry Service - offers an API endpoint for sending telemetry. The service handles incoming requests. This service saves the data into Telemetry Storage.

* Telemetry Storage - stores all telemetry data for the long term.

### Telemetry Subsystem

The Telemetry Subsystem extends the functionality of the database. It is built-in in Percona Server for MongoDB and is implemented separately for `mongod` and `mongos` instances. The Telemetry Subsystem is enabled by default during the initial database deployment.

The Telemetry Subsystem waits 24 hours before the first collection, then writes a new Metrics File daily. Before each collection, it deletes Metrics Files older than seven days.

A `mongod` instance preserves its collection schedule across restarts in the non-replicated `local.percona.telemetry` collection. A `mongos` instance starts a new 24-hour grace period on every start.

!!! note

    Restarting `mongod` does not renew the grace period. If you don't want to share usage data, [disable telemetry](#disable-telemetry) before the first scheduled collection.

The Metrics File is named `<timestamp>-<db_instance_id>.json`, where `<timestamp>` is the collection time in UNIX seconds. Files have `0660` permissions: the owner and group can read and write them, and other users have no access.

The server does not create the telemetry directory. The directory must exist and allow the server to write Metrics Files and the Telemetry Agent to read them.

### Instance identifiers

The Metrics File uses identifiers to distinguish instances and their data:

* `db_instance_id` identifies a database instance. A `mongod` instance stores it in `psmdb_telemetry.data` in its data directory (`storage.dbPath`) and reuses it across restarts. A `mongos` instance generates a new identifier on every start.
* `db_internal_id` identifies the data set on a `mongod` instance. It is stored in the non-replicated `local.percona.telemetry` collection and is not reported by `mongos`.

On the first start of a new `mongod` instance, both identifiers have the same value. They can differ after a restore or a change to the data directory or stored telemetry identifiers.

### Metrics File

The Metrics File is a JSON file with the metrics collected by the Telemetry Subsystem. 

#### Locations 

Percona stores the Metrics File in one of the following directories on the local file system. The location depends on the product.

* Telemetry root path - `/usr/local/percona/telemetry`

* Percona Server for MongoDB has two root paths since the telemetry Subsystem is enabled both for the `mongod` and `mongos` instances. The paths are the following:  

    * `mongod` root path -  `${telemetry root path}/psmdb/`
    * `mongos` root path -  `${telemetry root path}/psmdbs/`

To check the directory used by the connected `mongod` or `mongos` instance, run this command in `mongosh`:

```javascript
db.adminCommand({getParameter: 1, perconaTelemetryPath: 1})
```

For a `mongod` instance using the default path, the output is:

```json
{
    "perconaTelemetryPath": "/usr/local/percona/telemetry/psmdb",
    "ok": 1
}
```

Percona archives the telemetry history in `${telemetry root path}/history/`.

#### Metrics File format

The Metrics File uses JavaScript Object Notation (JSON). Boolean indicators and numeric metrics such as `uptime` are stored as strings. The `percona_features` field is an array, and `tde_vault_info` is an object.

The following examples illustrate the file format. Feature lists are abbreviated, and values depend on the build and configuration. Percona can add fields in future releases.

=== "`mongod` Metrics File"

    This example shows a config server replica set member with x.509 authentication, Vault encryption, and a registered Percona Backup for MongoDB agent:

    ```json
    {
        "source": "mongod",
        "pillar_version": "7.0.48-25",
        "percona_features": ["HotBackup", "LDAP", "OIDC", "TDE"],
        "db_instance_id": "65e9977d58deb2f66faa591c",
        "db_internal_id": "65e9977d58deb2f66faa591c",
        "db_cluster_id": "65e997cb58deb2f66faa5954",
        "oidc_enabled": "false",
        "ldap_enabled": "false",
        "ldap_authorization_enabled": "false",
        "ldap_sasl_authentication_enabled": "false",
        "kerberos_enabled": "false",
        "x509_enabled": "true",
        "x509_server_enabled": "true",
        "shard_svr": "false",
        "config_svr": "true",
        "uptime": "86502",
        "storage_engine": "wiredTiger",
        "db_replication_id": "65e997cb58deb2f66faa5944",
        "replication_state": "PRIMARY",
        "initial_sync_method": "logical",
        "tde_key_storage": "vault",
        "tde_vault_info": {
            "title": "HashiCorp Vault API",
            "version": "1.15.2"
        },
        "pbm_active": "2.9.0"
    }
    ```

=== "`mongos` Metrics File"

    The following is an example of the collected data generated by the `mongos` instance. 

    ```json
    {
        "source": "mongos",
        "pillar_version": "7.0.48-25",
        "percona_features": ["HotBackup", "LDAP", "OIDC", "TDE"],
        "db_instance_id": "6690fea9066216c6d9d77044",
        "oidc_enabled": "false",
        "ldap_enabled": "false",
        "ldap_authorization_enabled": "false",
        "ldap_sasl_authentication_enabled": "false",
        "kerberos_enabled": "false",
        "x509_enabled": "false",
        "x509_server_enabled": "false",
        "uptime": "86404",
        "db_cluster_id": "6690fea65d86eb061c0bd728"
    }
    ```

#### Collected metrics

The following table describes the fields in a Metrics File. Configuration-dependent fields are included only when the relevant information is available.

| Field | Instance | Description and availability |
|---|---|---|
| `source` | `mongod`, `mongos` | The instance type that generated the file. |
| `pillar_version` | `mongod`, `mongos` | The Percona Server for MongoDB version. |
| `percona_features` | `mongod`, `mongos` | Features available in the build, also listed in `perconaFeatures` in the `buildInfo` command output. This list does not indicate which features are in use. |
| `db_instance_id` | `mongod`, `mongos` | The instance identifier. See [Instance identifiers](#instance-identifiers). |
| `db_internal_id` | `mongod` | The data set identifier. See [Instance identifiers](#instance-identifiers). |
| `oidc_enabled` | `mongod`, `mongos` | Whether at least one identity provider is configured for [OpenID Connect authentication](oidc.md) through `oidcIdentityProviders`. |
| `ldap_enabled` | `mongod`, `mongos` | Whether an LDAP server is configured with `security.ldap.servers`. |
| `ldap_authorization_enabled` | `mongod`, `mongos` | Whether [LDAP authorization](ldap-setup.md) has a query configured in `security.ldap.authz.queryTemplate`. |
| `ldap_sasl_authentication_enabled` | `mongod`, `mongos` | Whether the `PLAIN` mechanism for [LDAP authentication with SASL](sasl-auth.md) is enabled in `authenticationMechanisms`. |
| `kerberos_enabled` | `mongod`, `mongos` | Whether the `GSSAPI` mechanism for [Kerberos authentication](kerberos.md) is enabled in `authenticationMechanisms`. |
| `x509_enabled` | `mongod`, `mongos` | Whether client x.509 authentication is configured. Reports `"true"` when `MONGODB-X509` is enabled in `authenticationMechanisms`, TLS is enabled, and either `tlsCAFile` or the system CA store (`tlsUseSystemCA`) is configured. Otherwise reports `"false"`. |
| `x509_server_enabled` | `mongod`, `mongos` | Whether cluster member x.509 authentication is configured. Reports `"true"` when `clusterAuthMode` is `x509` or `sendX509`, TLS is enabled, and `tlsCAFile` or `tlsClusterCAFile` is configured. Otherwise reports `"false"`. |
| `uptime` | `mongod`, `mongos` | Seconds since the instance started. |
| `storage_engine` | `mongod` | The storage engine, such as `wiredTiger` or `inMemory`. |
| `db_replication_id` | `mongod` | The replica set identifier. Present for replica set members. |
| `replication_state` | `mongod` | The replica set member state, such as `PRIMARY` or `SECONDARY`. Present for replica set members. |
| `initial_sync_method` | `mongod` | The configured [initial sync method](fcbis.md): `logical` or `fileCopyBased`. Present for replica set members. |
| `tde_key_storage` | `mongod` | The key storage for [data-at-rest encryption](data-at-rest-encryption.md): `keyfile`, `vault`, or `kmip`. Present when encryption is enabled. |
| `tde_vault_info` | `mongod` | Vault API metadata, including `title` and `version` when provided. Present when [Vault](vault.md) is used for key storage and its API metadata can be retrieved. |
| `db_cluster_id` | `mongod`, `mongos` | The sharded cluster identifier, when cluster metadata is available. |
| `shard_svr` | `mongod` | Whether the instance is a shard server. Present with sharded cluster metadata. |
| `config_svr` | `mongod` | Whether the instance is a config server. Present with sharded cluster metadata. |
| `pbm_active` | `mongod` | The version reported by a registered [Percona Backup for MongoDB :octicons-link-external-16:](https://docs.percona.com/percona-backup-mongodb/index.html){:target="_blank"} agent. Present when a version is available from `admin.pbmAgents`; it does not indicate that a backup is running. |

### Telemetry Agent

The Percona Telemetry Agent runs as a dedicated OS daemon process `percona-telemetry-agent`. It creates, reads, writes, and deletes JSON files in the [`${telemetry root path}`](#locations). You can find the agent's log file at `/var/log/percona/telemetry-agent.log`.

The agent does not send anything if there are no Percona-specific files in the target directory.

The following is an example of a Telemetry Agent payload:

```json
{
  "reports": [
    {
      "id": "B5BDC47B-B717-4EF5-AEDF-41A17C9C18BB",
      "createTime": "2023-09-01T10:56:49Z",
      "instanceId": "B5BDC47B-B717-4EF5-AEDF-41A17C9C18BA",
      "productFamily": "PRODUCT_FAMILY",
      "metrics": [
        {
          "key": "OS",
          "value": "Ubuntu"
        },
        {
          "key": "pillar_version",
          "value": "7.0.0"
        }
      ]
    }
  ]
}
```

The agent sends information about the database and metrics.

| Key | Description |
|---|---|
| "id" | A generated Universally Unique Identifier (UUID) version 4 |
| "createTime" | UNIX timestamp |
| "instanceId" | The DB Host ID. The value can be taken from the `instanceId`, the `/usr/local/percona/telemetry_uuid` or generated as a UUID version 4 if the file is absent. |
| "productFamily" | The value from the file path |
| "metrics" | An array of key:value pairs collected from the Metrics File.

The following operating system-level metrics are sent with each check:

| Key | Description |
|---|---|
| "OS" | The name of the operating system |
| "hardware_arch" | The type of process used in the environment |
| "deployment" | How the application was deployed. <br> The possible values could be "PACKAGE" or "DOCKER". |
| "installed_packages" | A list of the installed Percona packages.|

The information includes the following:

* Package name

* Package version - the same format as Red Hat Enterprise Linux or Debian

* Package repository - if possible

The package names must fit the following pattern:

* `percona-*`

* `Percona-*`

* `proxysql*`

* `pmm`

* `etcd*`

* `haproxy`

* `patroni`

* `pg*`

* `postgis`

* `wal2json`

## Disable telemetry 

Telemetry is enabled by default when you install the software. It is also included in the software packages (Telemetry Subsystem and Telemetry Agent) and enabled by default.

If you don't want to send the telemetry data, here's how: 

### Disable the telemetry collected during the installation

If you decide not to send usage data to Percona when you install the software, you can set the `PERCONA_TELEMETRY_DISABLE=1` environment variable for either the root user or in the operating system prior to the installation process.

=== "Debian-derived distribution"

    Add the environment variable before the installation process.

    ```bash
    sudo PERCONA_TELEMETRY_DISABLE=1 apt install percona-server-mongodb
    ```

=== "Red Hat-derived distribution"

    Add the environment variable before the installation process.
    
    ```bash
    sudo PERCONA_TELEMETRY_DISABLE=1 yum install percona-server-mongodb
    ```

=== "Docker"

    Add the environment variable when running a command in a new container.
    
    ```bash
    docker run -d --name psmdb --restart always \
      -e PERCONA_TELEMETRY_DISABLE=1 \
      percona/percona-server-mongodb:<TAG>
    ```

    The command does the following:

    * `docker run` - This is the command to run a Docker container.
    * `-d` - This flag specifies that the container should run in detached mode (in the background).
    * `--name psmdb` - Assigns the name “psmdb” to the container.
    * `--restart always` - Configures the container to restart automatically if it stops or crashes.
    * `-e PERCONA_TELEMETRY_DISABLE=1` - Sets an environment variable within the container. In this case, it disables telemetry for Percona Server for MongoDB.
    * `percona/percona-server-mongodb:<TAG>-multi` - Specifies the image to use for the container. For example, `{{release}}-multi`. The `multi` part of the tag serves to identify the architecture (x86_64 or ARM64) and use the respective image.

## Disable telemetry for the installed software

Percona software you installed includes the telemetry feature that collects information about how you use this software. It is enabled by default. To turn  off telemetry, you need to disable both the Telemetry Agent and the Telemetry Subsystem.

### Disable Telemetry Agent

For the grace period before the first database metrics collection, see [Telemetry Subsystem](#telemetry-subsystem).

You can either disable the Telemetry Agent temporarily or permanently.

=== "Disable temporarily"

    Turn off Telemetry Agent temporarily until the next server restart with this command:

    ```bash
    systemctl stop percona-telemetry-agent
    ```

=== "Disable permanently"

    Turn off Telemetry Agent permanently with this command:

    ```bash
    systemctl disable percona-telemetry-agent
    ```

Even after stopping the Telemetry Agent service, a different part of the software (Telemetry Subsystem) continues to create the Metrics File related to telemetry every day and saves that file for seven days.

### Telemetry Agent dependencies and removal considerations

If you decide to remove the Telemetry Agent, this also removes the database. That's because the Telemetry Agent is a mandatory dependency for Percona Server for MongoDB. 

On YUM-based systems, the system removes the Telemetry Agent package when you remove the last dependency package.

On APT-based systems, you must use the '--autoremove' option to remove all dependencies, as the system doesn't automatically remove the Telemetry Agent when you remove the database package.

The '--autoremove' option only removes unnecessary dependencies. It doesn't remove dependencies required by other packages or guarantee the removal of all package-associated dependencies.

### Disable the Telemetry Subsystem

To disable the Telemetry Subsystem, set the `perconaTelemetry` server parameter to `false`. You can do this in one of the following ways:

=== ":octicons-file-code-24: Configuration file"

    Use the `setParameter.perconaTelemetry` parameter in the configuration file
    for persistent changes:    

    ```yaml
    setParameter:
      perconaTelemetry: false
    ```

=== ":material-console: Command line"

    Use the `--setParameter` command line option arguments for both `mongod` and `mongos` processes. The server starts with the telemetry Subsystem disabled:    

    ```bash
    mongod \
      --setParameter perconaTelemetry=false
    mongos \
      --setParameter perconaTelemetry=false
    ```

=== ":simple-mongodb: `setParameter` command"    

    Use the `setParameter` command on the `admin` database
    to make changes at runtime. The changes apply until the server restart.

    ```javascript 
    db.adminCommand({setParameter: 1, "perconaTelemetry": false})
    ```

!!! tip

    If you wish to re-enable the Telemetry Subsystem, set the `perconaTelemetry` to `true` for the `setParameter` command.


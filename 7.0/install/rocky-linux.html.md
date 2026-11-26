> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server-for-mongodb/7.0/llms.txt).

# Install Percona Server for MongoDB on Rocky Linux

This guide walks you through the installation of Percona Server for MongoDB on Rocky Linux.

We gather [Telemetry data](https://docs.percona.com/percona-server-for-mongodb/7.0/telemetry.md) to understand the use of the software and improve our products.

Package contents

| Package                         | Contains                                                                                                                        |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `percona-server-mongodb`        | The `mongosh` shell, import/export tools, other client utilities, server software, default configuration, and `init.d` scripts. |
| `percona-server-mongodb-server` | The `mongod` server, default configuration files, and `init.d` scripts                                                          |
| `percona-server-mongodb-shell`  | The `mongosh` shell                                                                                                             |
| `percona-server-mongodb-mongos` | The `mongos` sharded cluster query router                                                                                       |
| `percona-server-mongodb-tools`  | Mongo tools for high-performance MongoDB fork from Percona                                                                      |
| `percona-server-mongodb-dbg`    | Debug symbols for the server                                                                                                    |

## Procedure

Before you start, check the [system requirements](https://docs.percona.com/percona-server-for-mongodb/7.0/system-requirements.md).

### Configure Percona repository

Percona provides the [`percona-release`](https://docs.percona.com/percona-software-repositories/index.html) configuration tool that simplifies operating repositories and enables to install and update both Percona Server for MongoDB packages and required dependencies smoothly.

1. Install **percona-release**:

   ```bash
   sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
   ```

   Example output

   ```bash
   Retrieving https://repo.percona.com/yum/percona-release-latest.noarch.rpm
   Preparing...                ########################################### [100%]
   1:percona-release        ########################################### [100%]
   ```

1. Enable the repository:

   ```bash
   sudo percona-release enable psmdb-70 release
   ```

### Install Percona Server for MongoDB packages

**Install the latest version**

To install the latest version of *Percona Server for MongoDB*, use the following command:

```bash
sudo yum install percona-server-mongodb
```

**Install a specific version**

To install a specific version of *Percona Server for MongoDB*, do the following:

1. List available versions:

   ```bash
   sudo yum list percona-server-mongodb --showduplicates
   ```

   Sample output:

   ```bash
       Available Packages

   percona-server-mongodb.x86_64    7.0.48-25.el9       psmdb-70-release-x86_64
   ```

1. Install a specific version packages. For example, to install *Percona Server for MongoDB* 7.0.48-25, run the following command:

   ```bash
   sudo yum install percona-server-mongodb-7.0.48-25.el9
   ```

By default, Percona Server for MongoDB stores data files in `/var/lib/mongodb/` and configuration parameters in `/etc/mongod.conf`.

## Run Percona Server for MongoDB

Note

If you use SELinux in enforcing mode, you must customize your SELinux user policies to allow access to certain `/sys` and `/proc` files for OS-level statistics. Also, you must customize directory and port access policies if you are using non-default locations.

Please refer to [Configure SELinux](https://docs.mongodb.com/v7.0/tutorial/install-mongodb-on-red-hat/#configure-selinux) section of MongoDB Documentation for policy configuration guidelines.

**Start the service**

Percona Server for MongoDB is not started automatically after installation. Start it manually using the following command:

```bash
sudo systemctl start mongod
```

**Confirm that service is running**

Check the service status using the following command:

```bash
sudo systemctl status mongod
```

**Stop the service**

Stop the service using the following command:

```bash
sudo systemctl stop mongod
```

**Restart the service**

Restart the service using the following command:

```bash
sudo systemctl restart mongod
```

### Run after reboot

The `mongod` service is not automatically started after you reboot the system.

To make it start automatically after reboot, enable it using the systemctl utility:

```bash
sudo systemctl enable mongod
```

Then start the `mongod` service:

```bash
sudo systemctl start mongod
```

## Next steps

[Connect to MongoDB](https://docs.percona.com/percona-server-for-mongodb/7.0/connect.md)

# Install Percona Server for MongoDB on Debian and Ubuntu

This document describes how to install Percona Server for MongoDB from Percona repositories on DEB-based distributions such as Debian and Ubuntu. 

We gather [Telemetry data](../telemetry.md) to understand the use of the software and improve our products.

??? admonition "Package contents"

    | Package                 | Contains                                 |
    | ----------------------- | -----------------------------------------|
    | `percona-server-mongodb`| The `mongo` shell, import/export tools, other client utilities, server software, default configuration, and `init.d` scripts. |
    | `percona-server-mongodb-server`| The mongod` server, default configuration files, and `init.d` scripts|
    | `percona-server-mongodb-shell` | The `mongo` shell |
    | `percona-server-mongodb-mongos`| The `mongos` sharded cluster query router |
    | `percona-server-mongodb-tools` | Mongo tools for high-performance MongoDB fork from Percona|
    | `percona-server-mongodb-dbg`   | Debug symbols for the server|

## Procedure

Before you start, check the [system requirements](system-requirements.md).

### Configure Percona repository

To install from Percona repositories, first you need to enable the required repository using the [`percona-release`](https://docs.percona.com/percona-software-repositories/index.html) repository management tool.
{.power-number}

1. Fetch **percona-release** packages from Percona web:
    
    ```{.bash data-prompt="$"}
    $ wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
    ```

2. Install the downloaded package with **dpkg**:

    ```{.bash data-prompt="$"}
    $ sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb
    ```

    After you install this package, you have the access to Percona repositories. You
    can check the repository setup in the `/etc/apt/sources.list.d/percona-release.list` file.


3. Enable the repository:

    ```{.bash data-prompt="$"}
    $ sudo percona-release enable psmdb-44 release
    ```

4. Remember to update the local cache:

    ```{.bash data-prompt="$"}
    $ sudo apt update
    ```

### Install Percona Server for MongoDB

=== ":material-run-fast: Install the latest version"

     Run the following command to install the latest version of Percona Server for MongoDB:

      ```{.bash data-prompt="$"}
      $ sudo apt install percona-server-mongodb
      ```

=== ":octicons-number-16: Install a specific version"

     To install a specific version of Percona Server for MongoDB, do the following:


     1. List available versions:

         ```{.bash data-prompt="$"}
         $ sudo apt-cache madison percona-server-mongodb
         ```

         ??? example "Sample output"

             ```{.text .no-copy}
             percona-server-mongodb | 4.4.17-17.jammy | http://repo.percona.com/psmdb-44/apt jammy/main amd64 Packages
             percona-server-mongodb | 4.4.16-16.jammy | http://repo.percona.com/psmdb-44/apt jammy/main amd64 Packages
             percona-server-mongodb | 4.4.15-15.jammy | http://repo.percona.com/psmdb-44/apt jammy/main amd64 Packages
             percona-server-mongodb |  4.4.17-17 | http://repo.percona.com/psmdb-44/apt jammy/main Sources
             percona-server-mongodb |  4.4.16-16 | http://repo.percona.com/psmdb-44/apt jammy/main Sources
             percona-server-mongodb |  4.4.15-15 | http://repo.percona.com/psmdb-44/apt jammy/main Sources
             ```

      2. Install a specific version packages. You must specify each package with the version number. For example, to install Percona Server for MongoDB 4.4.15-15, run the following command:

         ```{.bash data-prompt="$"}
         $ sudo apt install percona-server-mongodb=4.4.15-15.jammy percona-server-mongodb-mongos=4.4.15-15.jammy percona-server-mongodb-shell=4.4.15-15.jammy percona-server-mongodb-server=4.4.15-15.jammy percona-server-mongodb-tools=4.4.15-15.jammy
         ```

## Run Percona Server for MongoDB

By default, Percona Server for MongoDB stores data files in `/var/lib/mongodb/`
and configuration parameters in `/etc/mongod.conf`.

**Start the service**

Percona Server for MongoDB is started automatically after installation unless it encounters errors during the installation process.

You can also manually start it using the following command:

```{.bash data-prompt="$"}
$ sudo systemctl start mongod
```

**Confirm that the service is running**

Check the service status using the following command:

```{.bash data-prompt="$"}
$ sudo systemctl status mongod
```

**Stop the service**

Stop the service using the following command:

```{.bash data-prompt="$"}
$ sudo systemctl stop mongod
```

**Restart the service**

Restart the service using the following command:

```{.bash data-prompt="$"}
$ sudo systemctl restart mongod
```

Congratulations! Your Percona Server for MongoDB is up and running. 

## Next steps

[Connect to MongoDB :material-arrow-right:](../connect.md){.md-button}

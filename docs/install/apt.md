# Install {{psmdb.full_name}} on Debian and Ubuntu

This document describes how to install {{psmdb.full_name}} from Percona repositories on DEB-based distributions such as Debian and Ubuntu. 

We gather [Telemetry data](../telemetry.md) to understand the use of the software and improve our products.

!!! note

    {{psmdb.full_name}} should work on other DEB-based distributions,
    but it is tested only on platforms listed on the [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-support-lifecycle#mongodb) page.

??? admonition "Package contents"

    | Package                 | Contains                                 |
    | ----------------------- | -----------------------------------------|
    | `percona-server-mongodb`| The `mongosh` shell, import/export tools, other client utilities, server software, default configuration, and `init.d` scripts. |
    | `percona-server-mongodb-server`| The `mongod` server, default configuration files, and `init.d` scripts|
    | `percona-server-mongodb-shell` | The `mongosh` shell |
    | `percona-server-mongodb-mongos`| The `mongos` sharded cluster query router |
    | `percona-server-mongodb-tools` | Mongo tools for high-performance MongoDB fork from Percona|
    | `percona-server-mongodb-dbg`   | Debug symbols for the server|

## Procedure

Before you start, check the [system requirements](../system-requirements.md).

### Configure Percona repository

Percona provides the [`percona-release`](https://docs.percona.com/percona-software-repositories/index.html) configuration tool that simplifies operating repositories and enables to install and update both {{psmdb.full_name}} packages and required dependencies smoothly.    

1. Fetch `percona-release` packages from Percona web:
        
    ```{.bash data-prompt="$"}
    $ wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
    ```    

2. Install the downloaded package with **dpkg**:    

    ```{.bash data-prompt="$"}
    $ sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb
    ```    

    After you install this package, you have the access to Percona repositories. You can check the repository setup in the `/etc/apt/sources.list.d/percona-release.list` file.    
    
3. Enable the repository:    

    ```{.bash data-prompt="$"}
    $ sudo percona-release enable psmdb-80 release
    ```    

4. Remember to update the local cache:    

    ```{.bash data-prompt="$"}
    $ sudo apt update
    ```

### Install {{psmdb.full_name}}

=== ":material-run-fast: Install the latest version"

     Run the following command to install the latest version of {{psmdb.full_name}}:

      ```{.bash data-prompt="$"}
      $ sudo apt install percona-server-mongodb
      ```

=== ":octicons-number-16: Install a specific version"

     To install a specific version of {{psmdb.full_name}}, do the following:
     {.power-number}


     1. List available versions:

         ```{.bash data-prompt="$"}
         $ sudo apt-cache madison percona-server-mongodb
         ```

         Sample output:

         ```{.bash .no-copy}
         percona-server-mongodb | {{release}}.bullseye | http://repo.percona.com/psmdb-80/apt bullseye/main amd64 Packages
         ```

      2. Install a specific version packages. You must specify each package with the version number. For example, to install {{psmdb.full_name}} {{release}}, run the following command:

         ```{.bash data-prompt="$"}
         $ sudo apt install percona-server-mongodb={{release}}.bullseye percona-server-mongodb-mongos={{release}}.bullseye percona-server-mongodb-shell={{release}}.bullseye percona-server-mongodb-server={{release}}.bullseye percona-server-mongodb-tools={{release}}.bullseye
         ```

By default, {{psmdb.full_name}} stores data files in `/var/lib/mongodb/`
and configuration parameters in `/etc/mongod.conf`.

## Run {{psmdb.full_name}}

**Start the service**

{{psmdb.full_name}} is started automatically after installation unless it encounters errors during the installation process.

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

Congratulations! Your {{psmdb.full_name}} is up and running. 

## Next steps

[Connect to MongoDB :material-arrow-right:](../connect.md){.md-button}

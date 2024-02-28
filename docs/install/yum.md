# Install Percona Server for MongoDB on Red Hat Enterprise Linux and derivatives

This document describes how to install Percona Server for MongoDB on RPM-based distributions such as Red Hat Enterprise Linux and compatible derivatives.

We gather [Telemetry data](../telemetry.md) to understand the use of the software and improve our products.

??? admonition "Package contents"

    | Package                 | Contains                                 |
    | ----------------------- | -----------------------------------------|
    | `percona-server-mongodb`| The `mongo` shell, import/export tools, other client utilities, server software, default configuration, and `init.d` scripts. |
    | `percona-server-mongodb-server`| The mongod` server, default configuration files, and `init.d` scripts|
    | `percona-server-mongodb-shell` | The `mongo` shell |
    | `percona-server-mongodb-mongos`| The `mongos` sharded cluster query router |
    | `percona-server-mongodb-tools` | Mongo tools for high-performance MongoDB fork from Percona|
    | `percona-server-mongodb-dbg`   | Debug symbols for the server  |

## Procedure

Before you start, check the [system requirements](system-requirements.md).

### Configure Percona repository

To install from Percona repositories, first you need to enable the required repository using the [`percona-release`](https://docs.percona.com/percona-software-repositories/index.html) repository management tool.
{.power-number}

1. Install **percona-release**:

    ```{.bash data-prompt="$"}
    $ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
    ```


2. Enable the repository: 
   
    ```{.bash data-prompt="$"}
    $ sudo percona-release enable psmdb-44 release
    ```

### Install Percona Server for MongoDB packages

=== ":material-run-fast: Install the latest version"

      To install the latest version of *Percona Server for MongoDB*, use the following command:

      ```{.bash data-prompt="$"}
      $ sudo yum install percona-server-mongodb
      ```

=== ":octicons-number-16: Install a specific version"

     To install a specific version of Percona Server for MongoDB, do the following:
     {.power-number}

     1. List available versions:

         ```{.bash data-prompt="$"}
         $ sudo yum list percona-server-mongodb --showduplicates
         ```

        ??? example "Sample output"

            ```{.text .no-copy}
                Available Packages
            percona-server-mongodb.x86_64  4.4.10-11.el8  psmdb-44-release-x86_64
            percona-server-mongodb.x86_64  4.4.12-12.el8  psmdb-44-release-x86_64
            percona-server-mongodb.x86_64  4.4.13-13.el8  psmdb-44-release-x86_64
            percona-server-mongodb.x86_64  4.4.14-14.el8  psmdb-44-release-x86_64
            percona-server-mongodb.x86_64  4.4.15-15.el8  psmdb-44-release-x86_64
            percona-server-mongodb.x86_64  4.4.16-16.el8  psmdb-44-release-x86_64
            percona-server-mongodb.x86_64  4.4.17-17.el8  psmdb-44-release-x86_64
            ```

     2. Install a specific version packages. For example, to install *Percona Server for MongoDB* 4.4.15-15, run the following command:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-server-mongodb-4.4.15-15.el8
        ```

By default, Percona Server for MongoDB stores data files in /var/lib/mongodb/ and configuration parameters in /etc/mongod.conf.

## Run Percona Server for MongoDB

!!! note

    If you use SELinux in enforcing mode, you must customize your SELinux user policies to allow access to certain `/sys` and `/proc` files for OS-level statistics. Also, you must customize directory and port access policies if you are using non-default locations.

    Please refer to [Configure SELinux](https://docs.mongodb.com/v4.2/tutorial/install-mongodb-on-red-hat/#configure-selinux) section of MongoDB Documentation for policy configuration guidelines.

**Start the service**

Percona Server for MongoDB is not started automatically after installation.
Start it manually using the following command:

```{.bash data-prompt="$"}
$ sudo systemctl start mongod
```

**Confirm that service is running**

Check the service status using the following command: `service mongod status`

```{.bash data-prompt="$"}
$ sudo systemctl status mongod
```

**Stop the service**

Stop the service using the following command: `service mongod stop`

```{.bash data-prompt="$"}
$ sudo systemctl stop mongod
```

**Restart the service**

Restart the service using the following command: `service mongod restart`

```{.bash data-prompt="$"}
$ sudo systemctl restart mongod
```

### Run after reboot

The `mongod` service is not automatically started
after you reboot the system.

For RHEL or CentOS versions 5 and 6, you can use the `chkconfig` utility
to enable auto-start as follows:

```{.bash data-prompt="$"}
$ sudo chkconfig --add mongod
```

For RHEL or CentOS version 7, you can use the `systemctl` utility:

```{.bash data-prompt="$"}
$ sudo systemctl enable mongod
```


Congratulations! Your Percona Server for MongoDB is up and running. 

## Next steps

[Connect to MongoDB :material-arrow-right:](../connect.md){.md-button}

[^1]: We support only the current stable RHEL 6 and CentOS 6 releases, because there is no official (i.e. RedHat provided) method to support or download the latest OpenSSL on RHEL and CentOS versions prior to 6.5. Similarly, and also as a result thereof, there is no official Percona way to support the latest Percona Server builds on RHEL and CentOS versions prior to 6.5. Additionally, many users will need to upgrade to OpenSSL 1.0.1g or later (due to the [Heartbleed vulnerability](http://www.percona.com/resources/ceo-customer-advisory-heartbleed)), and this OpenSSL version is not available for download from any official RHEL and CentOS repositories for versions 6.4 and prior. For any officially unsupported system, src.rpm packages can be used to rebuild Percona Server for any environment. Please contact our [support service](http://www.percona.com/products/mysql-support) if you require further information on this.

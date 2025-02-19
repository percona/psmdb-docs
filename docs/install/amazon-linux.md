# Install Percona Server for MongoDB on Amazon Linux 2023

This guide walks you through the installation of Percona Server for MongoDB on Amazon Linux 2023. 

We gather [Telemetry data](../telemetry.md) to understand the use of the software and improve our products.

--8<-- "yum-install.md:1:48"

=== ":octicons-number-16: Install a specific version"

     To install a specific version of *Percona Server for MongoDB*, do the following:

     1. List available versions:

         ```{.bash data-prompt="$"}
         $ sudo yum list percona-server-mongodb --showduplicates
         ```

        Sample output:

         ```{.bash .no-copy}
             Available Packages
         
         percona-server-mongodb.aarch64    {{release}}.amzn2023       psmdb-60-release-aarch64
         ```

     2. Install a specific version packages. For example, to install *Percona Server for MongoDB* {{release}}, run the following command:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-server-mongodb-{{release}}.amzn2023
        ```

--8<-- "yum-install.md:74:140"

## Next steps

[Connect to MongoDB :material-arrow-right:](../connect.md){.md-button}

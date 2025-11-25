# Install Percona Server for MongoDB on Rocky Linux

This guide walks you through the installation of Percona Server for MongoDB on Rocky Linux. 

We gather [Telemetry data](../telemetry.md) to understand the use of the software and improve our products.

--8<-- "yum-install.md:1:48"

=== ":octicons-number-16: Install a specific version"

     To install a specific version of *Percona Server for MongoDB*, do the following:

     1. List available versions:

         ```bash
         sudo yum list percona-server-mongodb --showduplicates
         ```

        Sample output:

         ```{.bash .no-copy}
             Available Packages
         
         percona-server-mongodb.x86_64    {{release}}.el9       psmdb-80-release-x86_64
         ```

     2. Install a specific version packages. For example, to install *Percona Server for MongoDB* {{release}}, run the following command:

        ```bash
        sudo yum install percona-server-mongodb-{{release}}.el9
        ```

--8<-- "yum-install.md:75:134"

## Next steps

[Connect to MongoDB :material-arrow-right:](../connect.md){.md-button}

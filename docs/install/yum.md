# Install Percona Server for MongoDB on Red Hat Enterprise Linux and derivatives

This document describes how to install Percona Server for MongoDB on RPM-based distributions such as Red Hat Enterprise Linux and compatible derivatives. We gather [Telemetry data](../telemetry.md) to understand the use of the software and improve our products.

!!! note

    Percona Server for MongoDB should work on other RPM-based distributions (for example, Oracle Linux), but it is tested only on platforms listed on the [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mongodb) page. 


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
         
         percona-server-mongodb.x86_64    {{release}}.el9       psmdb-70-release-x86_64
         ```

     2. Install a specific version packages. For example, to install *Percona Server for MongoDB* {{release}}, run the following command:

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-server-mongodb-{{release}}.el9
        ```

--8<-- "yum-install.md:75:134"

## Next steps

[Connect to MongoDB :material-arrow-right:](../connect.md){.md-button}


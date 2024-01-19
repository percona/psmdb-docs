# Install Pro packages of Percona Server for MongoDB

This document provides guidelines how to install Percona Server for MongoDB Pro from Percona repositories. [Learn more about Percona Server for MongoDB Pro](../psmdb-pro.md).

If you already run Percona Server for MongoDB and wish to upgrade to Percona Server for MongoDB Pro, see the [upgrade guide](update-pro.md).

## Procedure

1. Request the access to the pro repository from Percona Support. You will receive the client ID and the access token.

2. Configure the repository

    === ":material-debian: Debian and Ubuntu"

        1. Create the `/etc/apt/sources.list.d/psmdb-pro.list` configuration file with the following contents

            ```ini title="/etc/apt/sources.list.d/psmdb-pro.list"
            deb http://repo.percona.com/private/[CLIENTID]-[TOKEN]/psmdb-60-pro/apt/ OPERATING_SYSTEM main
            ```

        2. Update the local cache

            ```{.bash .data-prompt="$"}
            $ sudo apt update
            ```

    === ":material-redhat: RHEL and derivatives"

        Create the `/etc/yum.repos.d/psmdb-pro.repo` configuration file with the following contents

        ```ini title="/etc/yum.repos.d/psmdb-pro.repo"
        [psmdb-6.0-pro]
        name=PSMDB_6.0_PRO
        baseurl=http://repo.percona.com/private/[CLIENTID]-[TOKEN]/psmdb-60-pro/yum/main/$releasever/RPMS/x86_64
        enabled=1
        gpgkey = https://repo.percona.com/yum/PERCONA-PACKAGING-KEY
        ```

3. Install Percona Server for MongoDB Pro packages

    === ":material-debian: Debian and Ubuntu"

        ```{.bash .data-prompt="$"}
        $ sudo apt install -y percona-server-mongodb-pro
        ```

    === ":material-redhat: RHEL and derivatives"

        ```{.bash .data-prompt="$"}
        $ sudo yum install -y percona-server-mongodb-pro
        ```

4. Start the server

    ```{.bash .data-prompt="$"}
    $ sudo systemct start mongod
    ```

## Next steps

[Connect to MongoDB :material-arrow-right:](../connect.md){.md-button}
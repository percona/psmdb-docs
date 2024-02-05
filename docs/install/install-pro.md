# Install Percona Server for MongoDB Pro

This document provides guidelines how to install Percona Server for MongoDB Pro from Percona repositories. [Learn more about Percona Server for MongoDB Pro](../psmdb-pro.md).

## Procedure {.power-number}

1. Request the access to the Pro builds repository from Percona Support. You will receive the client ID and the access token.

2. Configure the repository

    === ":material-debian: On Debian and Ubuntu"

        1. Create the `/etc/apt/sources.list.d/psmdb-pro.list` configuration file with the following contents

            ```ini title="/etc/apt/sources.list.d/psmdb-pro.list"
            deb http://repo.percona.com/private/[CLIENTID]-[TOKEN]/psmdb-70-pro/apt/ OPERATING_SYSTEM main
            ```

        2. Update the local cache

            ```{.bash .data-prompt="$"}
            $ sudo apt update
            ```

    === ":material-redhat: On RHEL and derivatives"

        Create the `/etc/yum.repos.d/psmdb-pro.repo` configuration file with the following contents

        ```ini title="/etc/yum.repos.d/psmdb-pro.repo"
        [psmdb-7.0-pro]
        name=PSMDB_7.0_PRO
        baseurl=http://repo.percona.com/private/[CLIENTID]-[TOKEN]/psmdb-70-pro/yum/main/$releasever/RPMS/x86_64
        enabled=1
        gpgkey = https://repo.percona.com/yum/PERCONA-PACKAGING-KEY
        ```

3. Install Percona Server for MongoDB Pro packages

    === ":material-debian: On Debian and Ubuntu"

        ```{.bash .data-prompt="$"}
        $ sudo apt install -y percona-server-mongodb-pro
        ```

    === ":material-redhat: On RHEL and derivatives"

        ```{.bash .data-prompt="$"}
        $ sudo yum install -y percona-server-mongodb-pro
        ```

4. Start the server

    ```{.bash .data-prompt="$"}
    $ sudo systemct start mongod
    ```
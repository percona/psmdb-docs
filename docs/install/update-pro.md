# Upgrade to Percona Server for MongoDB Pro

Are you a Percona Customer already and are you ready to enjoy all the [benefits of Percona Server for MongoDB Pro](../psmdb-pro.md)? 

This document provides instructions how you can upgrade from Percona Server for MongoDB Basic to Percona Server for MongoDB Pro.

!!! note

    You can upgrade to Percona Server for MongoDB Pro starting with version 6.0.12-9. 

## Preconditions 

Request the access to the Pro repository from Percona Support. You will receive the client ID and the access token.

## Procedure

1. Stop the `mongod` service

    ```{.bash data-prompt="$"}
    $ sudo systemctl stop mongod
    ```

2. Configure the repository

    === "On Debian and Ubuntu"

        1. Create the `/etc/apt/sources.list.d/psmdb-pro.list` configuration file with the following contents

            ```ini title="/etc/apt/sources.list.d/psmdb-pro.list"
            deb http://repo.percona.com/private/[CLIENTID]-[TOKEN]/psmdb-60-pro/apt/ OPERATING_SYSTEM main
            ```

        2. Update the local cache

            ```{.bash .data-prompt="$"}
            $ sudo apt update
            ```

    === "On RHEL and derivatives"

        Create the `/etc/yum.repos.d/psmdb-pro.repo` configuration file with the following contents

        ```ini title="/etc/yum.repos.d/psmdb-pro.repo"
        [psmdb-6.0-pro]
        name=PSMDB_6.0_PRO
        baseurl=http://repo.percona.com/private/[CLIENTID]-[TOKEN]/psmdb-60-pro/yum/main/$releasever/RPMS/x86_64
        enabled=1
        gpgkey = https://repo.percona.com/yum/PERCONA-PACKAGING-KEY
        ```

3. Install Percona Server for MongoDB packages

    === "On Debian and Ubuntu"

        ```{.bash .data-prompt="$"}
        $ sudo apt install -y percona-server-mongodb-pro
        ```

    === "On RHEL and derivatives"

        ```{.bash .data-prompt="$"}
        $ sudo yum install -y percona-server-mongodb-pro
        ```

4. Start the server

    ```{.bash .data-prompt="$"}
    $ sudo systemct start mongod
    ```
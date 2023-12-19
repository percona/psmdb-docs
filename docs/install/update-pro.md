# Upgrade to Percona Server for MongoDB Pro builds

Are you a Percona Customer already and are you ready to enjoy all the [benefits of Percona Server for MongoDB Pro builds](../psmdb-pro.md)? 

This document provides instructions how you can upgrade from Percona Server for MongoDB Basic builds to Percona Server for MongoDB Pro builds.

## Preconditions 

Request the access to the Pro builds repository from Percona Support. You will receive the client ID and the access token.

## Procedure

1. Stop the `mongod` service

    ```{.bash data-prompt="$"}
    $ sudo systemctl stop mongod
    ```

2. Configure the repository

    === "On Debian and Ubuntu"

        1. Create the `/etc/apt/sources.list.d/psmdb-pro.list` configuration file with the following contents

            ```ini title="/etc/apt/sources.list.d/psmdb-pro.list"
            deb http://repo.percona.com/private/[CLIENTID]-[TOKEN]/psmdb-70-pro/apt/ OPERATING_SYSTEM main
            ```

        2. Update the local cache

            ```{.bash .data-prompt="$"}
            $ sudo apt update
            ```

    === "On RHEL and derivatives"

        Create the `/etc/yum.repos.d/psmdb-pro.repo` configuration file with the following contents

        ```ini title="/etc/yum.repos.d/psmdb-pro.repo"
        [psmdb-7.0-pro]
        name=PSMDB_7.0_PRO
        baseurl=http://repo.percona.com/private/[CLIENTID]-[TOKEN]/psmdb-70-pro/yum/main/$releasever/RPMS/x86_64
        enabled=1
        gpgkey = https://repo.percona.com/yum/PERCONA-PACKAGING-KEY
        ```

3. Install Percona Server for MongoDB Pro build packages

    === "On Debian and Ubuntu"

        ```{.bash .data-prompt="$"}
        $ sudo apt install -y percona-server-mongodb-pro
        ```

    === "On RHEL 8+ and derivatives"

        ```{.bash .data-prompt="$"}
        $ sudo yum install -y percona-server-mongodb-pro
        ```

    === "On RHEL 7 and derivatives"

        1. Back up the `/etc/mongod.conf` configuration file
       
            ```{.bash .data-prompt="$"}
            $ sudo cp /etc/mongod.conf /etc/mongod.conf.bkp
            ```

        2. Remove Percona Server for MongoDB basic build packages

            ```{.bash .data-prompt="$"}
            $ sudo yum remove percona-server-mongodb*
            ```

        3. Install Percona Server for MongoDB Pro build packages

            ```{.bash .data-prompt="$"}
            $ sudo yum install -y percona-server-mongodb-pro
            ```

        4. Restore the configuration file from the backup

            ```{.bash .data-prompt="$"}
            $ sudo cp /etc/mongod.conf.bkp /etc/mongod.conf
            ```

4. Start the server

    ```{.bash .data-prompt="$"}
    $ sudo systemct start mongod
    ```

## Downgrade considerations

The downgrade to Percona Server for MongoDB basic build of version **7.0.4 and higher** is done automatically by [installing the basic build packages](yum.md#install-percona-server-for-mongodb-packages). 

If you wish to downgrade from Percona Server for MongoDB Pro builds to Percona Server for MongoDB basic builds of version **lower than 7.0.4**, do the following:

1. Remove the Pro packages

    ```{.bash .data-prompt="$"}
    $ sudo yum remove percona-server-mongodb-pro*
    ```

2. [Install Percona Server for MongoDB basic packages of the desired version](yum.md#install-percona-server-for-mongodb-packages)

        
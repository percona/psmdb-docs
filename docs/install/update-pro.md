# Upgrade to Percona Server for MongoDB Pro

Are you a Percona Customer already and are you ready to enjoy all the [benefits of Percona Server for MongoDB Pro](../psmdb-pro.md)? 

This document provides instructions how you can upgrade from Percona Server for MongoDB to Percona Server for MongoDB Pro.

## Preconditions 

Request the access to the Percona Server for MongoDB Pro repository from Percona Support. You will receive the client ID and the access token.

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

3. Install Percona Server for MongoDB Pro packages

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

        2. Remove basic packages of Percona Server for MongoDB 

            ```{.bash .data-prompt="$"}
            $ sudo yum remove percona-server-mongodb*
            ```

        3. Install Percona Server for MongoDB Pro packages

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

## Downgrade considerations on RHEL and derivatives

The downgrade to Percona Server for MongoDB basic of version **6.0.12 and higher** is done automatically by [installing the basic packages](yum.md#install-percona-server-for-mongodb-packages). 

If you wish to downgrade from Percona Server for MongoDB Pro to Percona Server for MongoDB basic of version **lower than 6.0.12**, do the following:

1. Remove the Pro packages

    ```{.bash .data-prompt="$"}
    $ sudo yum remove percona-server-mongodb-pro*
    ```

2. [Install Percona Server for MongoDB basic packages of the desired version](yum.md#install-percona-server-for-mongodb-packages)

        
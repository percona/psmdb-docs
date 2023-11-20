# Install Pro packages of Percona Server for MongoDB

This document provides guidelines how to install Pro packages of Percona Server for MongoDB from Percona repositories. [Learn more about PSMDB Pro :material-arrow-top-right:](../psmdb-pro.md).

## Procedure

1. Request the access the pro repository from Percona Support. You will receive the client ID and the access token.

2. Configure the repository

    === "On Debian and Ubuntu"

        1. Create the `/etc/apt/sources.list.d/psmdb-pro.list` configuration file with the following contents

            ```ini title="/etc/apt/sources.list.d/psmdb-pro"
            deb http://repo.percona.com/private/[CLIENTID]-[TOKEN]/psmdb-60/apt/ jammy main
            ```
        2. Update the local cache

            ```{.bash .data-prompt="$"}
            $ sudo apt update
            ```

    === "On RHEL and derivatives"

        Create the `/etc/yum.repos.d/psmdb-pro.repo` configuration file with the following contents

        ```ini 
        [psmdb-6.0-pro]
        name=PSMDB_6.0_PRO
        baseurl=http://repo.percona.com/private/[CLIENTID]-[TOKEN]/psmdb-60-pro/yum/testing/$releasever/RPMS/x86_64
        enabled=1
        gpgkey = https://repo.percona.com/yum/PERCONA-PACKAGING-KEY
        ```

3. Install Percona Server for MongoDB packages

    === "On Debian and Ubuntu"

        ```{.bash .data-prompt="$"}
        $ apt install -y percona-server-mongodb
        ```

    === "On RHEL and derivatives"

        ```{.bash .data-prompt="$"}
        $ yum install -y percona-server-mongodb
        ```
# Install Pro packages of Percona Server for MongoDB

This document provides guidelines how to install Percona Server for MongoDB Pro from Percona repositories and from binary tarballs. [Learn more about Percona Server for MongoDB Pro](../psmdb-pro.md).

## Preconditions

Request the access to the pro repository from Percona Support. You will receive the client ID and the access token.

## Install from Percona repository

=== "On Debian and Ubuntu"

    1. Configure the repository. Create the `/etc/apt/sources.list.d/psmdb-pro.list` configuration file with the following contents:

        ```ini title="/etc/apt/sources.list.d/psmdb-pro.list"
        deb http://repo.percona.com/private/[CLIENTID]-[TOKEN]/psmdb-60-pro/apt/ OPERATING_SYSTEM main
        ```

    2. Update the local cache

        ```{.bash .data-prompt="$"}
        $ sudo apt update
        ```

    3. Install Percona Server for MongoDB Pro packages

        ```{.bash .data-prompt="$"}
        $ sudo apt install -y percona-server-mongodb-pro
        ```

    4. Start the server

        ```{.bash .data-prompt="$"}
        $ sudo systemctl start mongod
        ```

=== "On RHEL and derivatives"

    1. Configure the repository. Create the `/etc/yum.repos.d/psmdb-pro.repo` configuration file with the following contents:

        ```ini title="/etc/yum.repos.d/psmdb-pro.repo"
        [psmdb-6.0-pro]
        name=PSMDB_6.0_PRO
        baseurl=http://repo.percona.com/private/[CLIENTID]-[TOKEN]/psmdb-60-pro/yum/main/$releasever/RPMS/x86_64
        enabled=1
        gpgkey = https://repo.percona.com/yum/PERCONA-PACKAGING-KEY
        ```

    2. Install Percona Server for MongoDB Pro packages

        ```{.bash .data-prompt="$"}
        $ sudo yum install -y percona-server-mongodb-pro
        ```

    3. Start the server

        ```{.bash .data-prompt="$"}
        $ sudo systemctl start mongod
        ```

## Install from binary tarballs

Binary tarballs are available starting with version 6.0.13-10 for the following operating systems:

* Ubuntu 22.04 (Jammy Jellyfish)
* Red Hat Enterprise Linux 9

### Preconditions

The following packages are required for the installation.

=== "On Debian and Ubuntu"
     
     * `libcurl4`

     * `libsasl2-modules`

     * `libsasl2-modules-gssapi-mit`


=== "On Red hat Enterprise Linux and derivatives"

     * `libcurl`

     * `cyrus-sasl-gssapi`

     * `cyrus-sasl-plain`

### Procedure

The steps below describe the installation on Ubuntu 22.04.

1. Download the tarballs from the pro repository 

    ```{.bash data-prompt="$"}
    $ wget https://repo.percona.com/private/ID-TOKEN/psmdb-60-pro/tarballs/percona-server-mongodb-pro-{{release}}-x86_64.jammy.tar.gz\
    $ wget https://repo.percona.com/private/ID-TOKEN/psmdb-60-pro/tarballs/percona-mongodb-mongosh-{{mongosh}}-x86_64.tar.gz
    ```
2. Extract the tarballs

    ```{.bash data-prompt='$'} 
    $ tar -xf percona-server-mongodb-{{release}}-x86_64.jammy.tar.gz
    $ tar -xf percona-mongodb-mongosh-{{mongosh}}-x86_64.tar.gz
    ```


3. Add the location of the binaries to the `PATH` variable:

    ```{.bash data-prompt="$"}
    $ export PATH=~/percona-server-mongodb-pro-{{release}}-x86_64.jammy/bin/:~/percona-mongodb-mongosh-{{mongosh}}/bin/:$PATH
    ```


4. Create the default data directory:

    ```{.bash data-prompt="$"}
    $ mkdir -p /data/db
    ```


5. Make sure that you have read and write permissions for the data
directory and run `mongod`.
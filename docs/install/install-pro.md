# Install Percona Server for MongoDB Pro

This document provides guidelines how to install Percona Server for MongoDB Pro from Percona repositories and from binary tarballs. [Learn more about Percona Server for MongoDB Pro](../psmdb-pro.md).

If you already run Percona Server for MongoDB and wish to upgrade to Percona Server for MongoDB Pro, see the [upgrade guide](update-pro.md).

--8<-- "token.md"

## Install from Percona repository

1. Install `percona-release` repository management tool.  

    === ":material-debian: Debian and Ubuntu" 

        1. Fetch `percona-release` packages from Percona web:
        
            ```{.bash data-prompt="$"}
            $ wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
            ```            

        2. Install the downloaded package with **dpkg**:            

            ```{.bash data-prompt="$"}
            $ sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb
            ```

        3. Update the local cache    

            ```{.bash .data-prompt="$"}
            $ sudo apt update
            ```

    === ":material-redhat: RHEL and derivatives"  

        Install `percona-release` using the following command:

        ```{.bash data-prompt="$"}
        $ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
        ```

2. Enable the repository. Choose your preferable method:

    === ":material-console: Command line"

        Run the following command and pass your credentials to the Pro repository:

        ```{.bash .data-prompt="$"}
        $ sudo percona-release enable psmdb-70-pro release --user_name=<Your Customer ID> --repo_token=<Your PRO repository token>
        ```

    === ":octicons-file-code-24: Configuration file"

        Create the `/root/.percona-private-repos.config` configuration file with the following content:

        ```ini title="/root/.percona-private-repos.config"
        [psmdb-70-pro]
        USER_NAME=<Your Customer ID>
        REPO_TOKEN=<Your PRO repository token>
        ```    

3. Install Percona Server for MongoDB Pro packages:

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
    $ sudo systemctl start mongod
    ```    

## Install from binary tarballs

Binary tarballs are available for the following operating systems:

Starting with version 7.0.7-4:

* Ubuntu 22.04 (Jammy Jellyfish)
* Red Hat Enterprise Linux 9
* Debian 12 (bookworm)

Starting with version 7.0.8-5:

* Red Hat Enterprise Linux 8

### Preconditions

The following packages are required for the installation.

=== ":material-debian: On Debian and Ubuntu"
     
     * `libcurl4`

     * `libsasl2-modules`

     * `libsasl2-modules-gssapi-mit`


=== ":material-redhat: On RHEL and derivatives"

     * `libcurl`

     * `cyrus-sasl-gssapi`

     * `cyrus-sasl-plain`

### Procedure

The steps below describe the installation on Ubuntu 22.04.

1. Download the tarballs from the pro repository 

    ```{.bash data-prompt="$"}
    $ wget https://repo.percona.com/private/ID-TOKEN/psmdb-70-pro/tarballs/percona-server-mongodb-pro-{{release}}-x86_64.jammy.tar.gz\
    $ wget https://repo.percona.com/private/ID-TOKEN/psmdb-70-pro/tarballs/percona-mongodb-mongosh-{{mongosh}}-x86_64.tar.gz
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

## Next steps

[Connect to MongoDB :material-arrow-right:](../connect.md){.md-button}
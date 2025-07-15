# Install Pro packages of Percona Server for MongoDB

This document provides guidelines how to install Percona Server for MongoDB Pro from Percona repositories and from binary tarballs. [Learn more about Percona Server for MongoDB Pro](../psmdb-pro.md).

If you already run Percona Server for MongoDB and wish to upgrade to Percona Server for MongoDB Pro, see the [upgrade guide](update-pro.md).

--8<-- "token.md"

## Install from Percona repository

=== ":material-debian: Debian and Ubuntu" 

    1. Install `percona-release` repository management tool. Fetch `percona-release` packages from Percona web:
        
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

    4. Enable the repository. Choose your preferable method:        

        === ":material-console: Command line"

            Run the following command and pass your credentials to the Pro repository:        

            ```{.bash .data-prompt="$"}
            $ sudo percona-release enable psmdb-60-pro release --user_name=<Your Customer ID> --repo_token=<Your PRO repository token>
            ```        

        === ":octicons-file-code-24: Configuration file"        

            1. Create the `/root/.percona-private-repos.config` configuration file with the following content:            

                ```ini title="/root/.percona-private-repos.config"
                [psmdb-60-pro]
                USER_NAME=<Your Customer ID>
                REPO_TOKEN=<Your PRO repository token>
                ```  

            2. Enable the repository

                ```{.bash .data-prompt="$"}
                $ sudo percona-release enable psmdb-60-pro release
                ```            

    5. Install Percona Server for MongoDB Pro packages:        

        ```{.bash .data-prompt="$"}
        $ sudo apt install -y percona-server-mongodb-pro
        ```            

    6. Start the server            

        ```{.bash .data-prompt="$"}
        $ sudo systemctl start mongod
        ```    

=== ":material-redhat: RHEL and derivatives"  

    1. Install `percona-release` using the following command:

        ```{.bash data-prompt="$"}
        $ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
        ```        

    2. Enable the repository. Choose your preferable method:        

        === ":material-console: Command line"

            Run the following command and pass your credentials to the Pro repository:        

            ```{.bash .data-prompt="$"}
            $ sudo percona-release enable psmdb-60-pro release --user_name=<Your Customer ID> --repo_token=<Your PRO repository token>
            ```        

        === ":octicons-file-code-24: Configuration file"        

            1. Create the `/root/.percona-private-repos.config` configuration file with the following content:            

                ```ini title="/root/.percona-private-repos.config"
                [psmdb-60-pro]
                USER_NAME=<Your Customer ID>
                REPO_TOKEN=<Your PRO repository token>
                ```  

            2. Enable the repository

                ```{.bash .data-prompt="$"}
                $ sudo percona-release enable psmdb-60-pro release
                ```

    3. Install Percona Server for MongoDB Pro packages:        

        ```{.bash .data-prompt="$"}
        $ sudo yum install -y percona-server-mongodb-pro
        ```        

    4. Start the server            

        ```{.bash .data-prompt="$"}
        $ sudo systemctl start mongod
        ```    



## Install from binary tarballs

Binary tarballs are available for the following operating systems:

Starting with version 6.0.13-10:

* Ubuntu 22.04 (Jammy Jellyfish)
* Red Hat Enterprise Linux 9

Starting with 6.0.14-11: 

* Red Hat Enterprise Linux 8 

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
    $ wget https://repo.percona.com/private/ID-TOKEN/psmdb-60-pro/tarballs/percona-server-mongodb-{{release}}/percona-server-mongodb-pro-{{release}}-x86_64.jammy.tar.gz \
    $ wget https://repo.percona.com/private/ID-TOKEN/psmdb-60-pro/tarballs/percona-mongodb-mongosh-{{mongosh}}/percona-mongodb-mongosh-{{mongosh}}-x86_64.tar.gz
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

## Run Percona Server for MongoDB Pro in Docker

You can run Percona Server for MongoDB Pro in Docker using the official image available in a private registry on [Docker Hub](https://hub.docker.com/r/percona/percona-server-mongodb-pro).

We gather [Telemetry data](../telemetry.md) to understand the use of the software and improve our products.x

To access this image, you must authenticate in DockerHub. For this you must have a valid Percona Server for MongoDB Pro subscription. 

### Authenticate in Docker Hub

1. Contact your Percona Representative to get authentication credentials for Docker Hub. You will receive a username and an access token. 
2. Authenticate in Docker Hub:

    ```{.bash data-prompt="$"}
    $ docker login --username <Username> 
    ```
    
    When prompted for a password, enter your access token.


### Run Percona Server for MongoDB Pro

To run Percona Server for MongoDB Pro in Docker, use the following command:

```{.bash data-prompt="$"}
$ docker run -d --name psmdb-pro -p 27017:27017 --restart always percona/percona-server-mongodb-pro:<TAG>
```

The command does the following:

* The `docker run` command instructs the `docker` daemon
to run a container from an image.

* The `-d` option starts the container in detached mode
(that is, in the background).

* The `--name` option assigns a custom name for the container
that you can use to reference the container within a Docker network.
In this case: `psmdb-pro`.

* The `-p` option binds the container's port `27017` to TCP port `27017` on all host network interfaces. This makes the container accessible externally.

* The `--restart` option defines the container’s restart policy.
Setting it to `always` ensures that the Docker daemon
will start the container on startup
and restart it if the container exits.

* `percona/percona-server-mongodb-pro` is the name of the image to derive the container from.

* `<TAG>` is the tag specifying the version you need. For example, `{{release}}`. Docker automatically identifies the architecture (x86_64 or ARM64) and pulls the respective image. [See the full list of tags](https://hub.docker.com/r/percona/percona-server-mongodb-pro/tags).

### Access the container shell

--8<-- "docker.md:shell"

## Next steps

[Run simple queries :material-arrow-right:](../crud.md){.md-button}

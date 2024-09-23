# Upgrade to Percona Server for MongoDB Pro

Are you a Percona Customer already and are you ready to enjoy all the [benefits of Percona Server for MongoDB Pro](../psmdb-pro.md)? 

This document provides instructions how you can upgrade from Percona Server for MongoDB to Percona Server for MongoDB Pro.

--8<-- "token.md"

## Procedure

=== ":material-debian: On Debian and Ubuntu"

    1. Stop the `mongod` service    

        ```{.bash data-prompt="$"}
        $ sudo systemctl stop mongod
        ```    

    2. [Install `percona-release` :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/installing.html#__tabbed_1_1). If you have installed it before, [upgrade :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/updating.html#__tabbed_1_1) it to the latest version

    3. Enable the repository. Choose your preferable method:            

        === ":material-console: Command line"    

            Run the following command and pass your credentials to the Pro repository:            

            ```{.bash .data-prompt="$"}
            $ sudo percona-release enable psmdb-60-pro release --user_name=<Your Customer ID> --repo_token=<Your PRO repository token>
            ```            

        === ":octicons-file-code-24: Configuration file"            

            Create the `/root/.percona-private-repos.config` configuration file with the following content:            

            ```ini title="/root/.percona-private-repos.config"
            [psmdb-60-pro]
            USER_NAME=<Your Customer ID>
            REPO_TOKEN=<Your PRO repository token>
            ```            
   
    4. Install Percona Server for MongoDB Pro packages

        ```{.bash .data-prompt="$"}
        $ sudo apt install -y percona-server-mongodb-pro
        ```

    5. Start the server            

        ```{.bash .data-prompt="$"}
        $ sudo systemctl start mongod
        ``` 

=== ":material-redhat: On RHEL and derivatives"

    1. Stop the `mongod` service    

        ```{.bash data-prompt="$"}
        $ sudo systemctl stop mongod
        ```

    2. [Install `percona-release` :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/installing.html#__tabbed_1_2). If you have installed it before, [upgrade :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/updating.html#__tabbed_1_2) it to the latest version.
    3. Enable the repository. Choose your preferable method:            

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

    4. Install Percona Server for MongoDB Pro packages

        === ":material-redhat: On RHEL 8+ and derivatives"    

            ```{.bash .data-prompt="$"}
            $ sudo yum install -y percona-server-mongodb-pro
            ```    

        === ":material-redhat: On RHEL 7 and derivatives"    

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

    5. Start the server    

        ```{.bash .data-prompt="$"}
        $ sudo systemct start mongod
        ```

## Downgrade considerations on RHEL and derivatives

The downgrade to the basic build of Percona Server for MongoDB of version **6.0.12 and higher** is done automatically by [installing the basic packages](yum.md#install-percona-server-for-mongodb-packages). 

If you wish to downgrade from Percona Server for MongoDB Pro to the basic build of Percona Server for MongoDB version **lower than 6.0.12**, do the following:

1. Remove the Pro packages

    ```{.bash .data-prompt="$"}
    $ sudo yum remove percona-server-mongodb-pro*
    ```

2. [Install Percona Server for MongoDB basic packages of the desired version](yum.md#install-percona-server-for-mongodb-packages)

        
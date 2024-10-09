# Upgrade to Percona Server for MongoDB Pro

Are you a Percona Customer already and are you ready to enjoy all the [benefits of Percona Server for MongoDB Pro](../psmdb-pro.md)? 

This document provides instructions how you can upgrade from Percona Server for MongoDB to Percona Server for MongoDB Pro .

--8<-- "token.md"

## Procedure {.power-number}

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
            $ sudo percona-release enable psmdb-80-pro release --user_name=<Your Customer ID> --repo_token=<Your PRO repository token>
            ```            

        === ":octicons-file-code-24: Configuration file"            

            1. Create the `/root/.percona-private-repos.config` configuration file with the following content:            

                ```ini title="/root/.percona-private-repos.config"
                [psmdb-80-pro]
                USER_NAME=<Your Customer ID>
                REPO_TOKEN=<Your PRO repository token>
                ```  

            2. Enable the repository

                ```{.bash .data-prompt="$"}
                $ sudo percona-release enable psmdb-80-pro release
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
            $ sudo percona-release enable psmdb-80-pro release --user_name=<Your Customer ID> --repo_token=<Your PRO repository token>
            ```             

        === ":octicons-file-code-24: Configuration file"            

            1. Create the `/root/.percona-private-repos.config` configuration file with the following content:            

                ```ini title="/root/.percona-private-repos.config"
                [psmdb-80-pro]
                USER_NAME=<Your Customer ID>
                REPO_TOKEN=<Your PRO repository token>
                ```   

            2. Enable the repository

                ```{.bash .data-prompt="$"}
                $ sudo percona-release enable psmdb-80-pro release
                ```

    4. Install Percona Server for MongoDB Pro packages


        ```{.bash .data-prompt="$"}
        $ sudo yum install -y percona-server-mongodb-pro
        ```    

    5. Start the server    

        ```{.bash .data-prompt="$"}
        $ sudo systemctl start mongod
        ```


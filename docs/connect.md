# Connect to Percona Server for MongoDB

After you have successfully installed and started Percona Server for MongoDB, let's connect to it.

By default, access control is disabled in MongoDB. We recommend enabling it so that users must verify their identity to be able to connect to the database. Percona Server for MongoDB supports several [authentication methods](authentication.md). We will use the default one, [SCRAM](authentication.md#scram), to configure authentication.

The steps are the following:
{.power-number}

1. Connect to Percona Server for MongoDB instance without authentication:

    ```{.bash data-prompt="$"}
    $ mongosh
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        Current Mongosh Log ID:	6598270a3a0c418751550ded
        Connecting to:		mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.0
        Using MongoDB:		{{release}}
        Using Mongosh:		2.0.0    

        For mongosh info see: https://docs.mongodb.com/mongodb-shell/    

        test>
        ```

2. Create the administrative user in the `admin` database:

    1. Switch to the `admin` database

        ```{.javascript data-prompt=">"}
        > use admin
        ```

        ??? example "Sample output"

            ```{.text .no-copy}
            switched to db admin
            ```

    2. Create the user:

        ```{.javascript data-prompt=">"}
        > db.createUser(
            {
              user: "admin",
              pwd: passwordPrompt(), // or cleartext password
              roles: [
                { role: "userAdminAnyDatabase", db: "admin" },
                { role: "readWriteAnyDatabase", db: "admin" }
              ]
            }
          )
        ```

3. Shutdown the `mongod` instance and exit `mongosh`

    ``` {.bash data-prompt=">"}
    > db.adminCommand( { shutdown: 1 } )
    ```

4. Enable authentication

    === ":octicons-file-code-24: Command line"

        Start the server with authentication enabled using the following command: 

        ``` {.bash data-prompt="$"}
        $ mongod --auth --port 27017 --dbpath /var/lib/mongodb --fork --syslog
        ```

    === ":material-console: Configuration file"

        1. Edit the configuration file

            ```yaml title="/etc/mongod.conf"
            security:
                authorization: enabled
            ```          

        2. Start the `mongod` service

            ``` {.bash data-prompt="$"}
            $ systemctl start mongod
            ```

5. Connect to Percona Server for MongoDB and authenticate.
    
    ``` {.bash data-prompt="$"}
    $ mongosh --port 27017  --authenticationDatabase \
    "admin" -u "admin" -p
    ```

## Next steps

[Run simple queries](crud.md){.md-button}




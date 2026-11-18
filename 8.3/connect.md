> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server-for-mongodb/8.3/llms.txt).

# Connect to Percona Server for MongoDB

After you have successfully installed and started Percona Server for MongoDB, let’s connect to it.

By default, access control is disabled in MongoDB. We recommend enabling it so that users must verify their identity to be able to connect to the database. Percona Server for MongoDB supports several [authentication methods](https://docs.percona.com/percona-server-for-mongodb/8.3/authentication.html). We will use the default one, [SCRAM](https://docs.percona.com/percona-server-for-mongodb/8.3/authentication.html#scram), to configure authentication.

The steps are the following:

1. Connect to Percona Server for MongoDB instance without authentication:

   ```
   mongosh
   ```

   Sample output

   ```
   Current Mongosh Log ID: 6598270a3a0c418751550ded
   Connecting to:      mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.0
   Using MongoDB:      8.3.17-5
   Using Mongosh:      2.0.0    

   For mongosh info see: https://docs.mongodb.com/mongodb-shell/    

   test>
   ```

1. Create the administrative user in the `admin` database:

   1. Switch to the `admin` database

      ```
      use admin
      ```

      Sample output

      ```
      switched to db admin
      ```

   1. Create the user:

      ```
      db.createUser(
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

1. Shutdown the `mongod` instance and exit `mongosh`

   ```
   db.adminCommand( { shutdown: 1 } )
   ```

1. Enable authentication

   **Command line**

   Start the server with authentication enabled using the following command:

   ```
   mongod --auth --port 27017 --dbpath /var/lib/mongodb --fork --syslog
   ```

   **Configuration file**

   1. Edit the configuration file

      /etc/mongod.conf

      ```
      security:
          authorization: enabled
      ```

   1. Start the `mongod` service

      ```
      systemctl start mongod
      ```

1. Connect to Percona Server for MongoDB and authenticate.

   ```
   mongosh --port 27017  --authenticationDatabase \
   "admin" -u "admin" -p
   ```

## Next steps

[Run simple queries](https://docs.percona.com/percona-server-for-mongodb/8.3/crud.html)

# Upgrading from Percona Server for MongoDB 4.2 to 4.4

To upgrade Percona Server for MongoDB to version 4.4, you must be running version 4.2. Upgrades from earlier versions are not supported.

Before upgrading your production Percona Server for MongoDB deployments, test all your applications in a testing environment to make sure they are compatible with the new version. For more information, see [Compatibility Changes in MongoDB 4.4](https://docs.mongodb.com/manual/release-notes/4.4-compatibility/)

We recommend to upgrade Percona Server for MongoDB from official Percona repositories using [`percona-release` repository management tool](https://www.percona.com/doc/percona-repo-config/index.html) and
the corresponding package manager for your system. 

This document describes this method for the in-place upgrade (where your existing data and configuration files are preserved).


!!! warning 

    Perform a full backup of your data and configuration files before upgrading.

=== "Upgrade on Debian and Ubuntu"

     1. Stop the `mongod` service:

          ```{.bash data-prompt="$"}
          $ sudo systemctl stop mongod
          ```

     2. Enable Percona repository for Percona Server for MongoDB 4.4:

         ```{.bash data-prompt="$"}
         $ sudo percona-release enable psmdb-44
         ```

     3. Update the local cache:

         ```{.bash data-prompt="$"}
         $ sudo apt update
         ```

     4. Install Percona Server for MongoDB 4.4 packages:

         ```{.bash data-prompt="$"}
         $ sudo apt install percona-server-mongodb
         ```

     5. Start the `mongod` instance:

         ```{.bash data-prompt="$"}
         $ sudo systemctl start mongod
         ```

     For more information, see [Installing Percona Server for MongoDB on Debian and Ubuntu](apt.md).

=== "Upgrade on Red Hat Enterprise Linux and derivatives"

     1. Stop the `mongod` service:

          ```{.bash data-prompt="$"}
          $ sudo systemctl stop mongod
          ```

     2. Enable Percona repository for Percona Server for MongoDB 4.4:

         ```{.bash data-prompt="$"}
         $ sudo percona-release enable psmdb-44
         ``` 

     3. Install Percona Server for MongoDB 4.4 packages:

         ```{.bash data-prompt="$"}
         $ sudo yum install percona-server-mongodb
         ```

     4. Start the `mongod` instance:

         ```{.bash data-prompt="$"}
         $ sudo systemctl start mongod
         ```

After the upgrade, Percona Server for MongoDB is started with the feature set of 4.2 version. Assuming that your applications are compatible with the new version, enable 4.4 version features. Run the following command against the `admin` database:

```{.javascript data-prompt=">"}
> db.adminCommand( { setFeatureCompatibilityVersion: "4.4" } )
```

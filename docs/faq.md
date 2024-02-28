# FAQ

## How to check Percona Server for MongoDB version?

To see which version of Percona Server for MongoDB you are using, check the value of the `psmdbVersion` key in the output of the [buildInfo](https://docs.mongodb.com/manual/reference/command/buildInfo/#dbcmd.buildInfo) database command. If this key does not exist, Percona Server for MongoDB is not installed on the server.

## Where is the location of the configuration and data files?

By default, Percona Server for MongoDB stores data files in `/var/lib/mongodb/`
and configuration parameters in `/etc/mongod.conf`.
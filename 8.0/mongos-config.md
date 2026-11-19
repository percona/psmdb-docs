> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server-for-mongodb/8.0/llms.txt).

# Configure a systemd unit file for `mongos`

`mongos` provides the entry point for an application to connect to a sharded cluster. To automate the `mongos` process management, you can use a system unit file. This file defines how the `mongos` service should behave when the system boots, shuts down, or encounters an issue.

This document provides a sample configuration for a `mongos` systemd unit file that you can use and/or modify to meet your specific needs. For security considerations, cluster components use a keyfile for internal authentication.

## Before you start

1. Ensure you have a working config server replica set and shards. Refer to the [deployment documentation](https://www.mongodb.com/docs/manual/tutorial/deploy-sharded-cluster-with-keyfile-access-control/#create-the-config-server-replica-set) for guidelines

1. Check that you have fulfilled all prerequisites in your system:

   - /var/log/mongo directory is created
   - If SELinux is in use, /var/run/mongos.pid is added to the policy so mongos process can create it

1. Get the shared key file from any existing member of the cluster. Refer to the [MongoDB documentation](https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-security.keyFile) for how to create keyfiles.

## Procedure

The steps are the following:

1. Create a `mongos` user and a group. This user will own the `mongos` process. Use the following command:

   ```
   groupadd mongos && sudo useradd -r -s /bin/false -g mongos mongos
   ```

1. Create the environment file at the path `/etc/sysconfig/mongos` and specify the following environment variables within:

   /etc/sysconfig/mongos

   ```
   OPTIONS="-f /etc/mongos.conf"
   STDOUT="/var/log/mongo/mongos.stdout"
   STDERR="/var/log/mongo/mongos.stderr"
   ```

1. Create a `mongos` configuration file at the path `/etc/mongos.conf`. In the following example configuration, replace the `security.keyfile` with the path to your keyfile and specify the name of the config server replica set and its members in the format `hostname:port`:

   /etc/mongos.conf

   ```
   # where to write logging data.
   systemLog:
     destination: file
     logAppend: true
     path: /var/log/mongo/mongos.log

   processManagement:
     fork: true
     pidFilePath: /var/run/mongos.pid

   # network interfaces
   net:
     port: 27017
     bindIp: 127.0.0.1

   security:
     keyFile: /etc/mongos.key

   sharding:
     configDB: configRS/cfg1.example.com:27017,cfg2.example.com:27017,cfg3.example.com:27017
   ```

1. Create the systemd unit file at the path `/usr/lib/systemd/system/mongos.service`. Specify the following configuration:

   ```
   tee /usr/lib/systemd/system/mongos.service <<EOF
   [Unit]
   Description=High-performance, schema-free document-oriented database
   After=time-sync.target network.target    

   [Service]
   Type=forking
   User=mongos
   Group=mongos
   PermissionsStartOnly=true
   LimitFSIZE=infinity
   LimitCPU=infinity
   LimitAS=infinity
   LimitNOFILE=64000
   LimitNPROC=64000
   EnvironmentFile=/etc/sysconfig/mongos
   ExecStart=/usr/bin/env bash -c "/usr/bin/mongos $OPTIONS > ${STDOUT} 2> ${STDERR}"
   PIDFile=/var/run/mongos.pid    

   [Install]
   WantedBy=multi-user.target
   EOF
   ```

1. Grant read/write access for the `mongos` user to the following directories and files:

   ```
   sudo chown -R mongos:mongos /var/log/mongo \
   /var/run/mongos.pid \
   /etc/mongos.conf \
   /etc/sysconfig/mongos \
   <path-to-keyfile>
   ```

1. Reload the systemd daemon to apply the changes:

   ```
   sudo systemctl daemon-reload
   ```

1. Start the `mongos` service:

   ```
   sudo systemctl start mongos
   ```

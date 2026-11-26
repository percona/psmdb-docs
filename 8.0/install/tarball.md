> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server-for-mongodb/8.0/llms.txt).

# Install Percona Server for MongoDB from binary tarball

You can find links to the binary tarballs under the *Generic Linux* menu item on the [Percona website](https://www.percona.com/downloads/percona-server-mongodb-6.0/)

There are the following tarballs available:

- `percona-server-mongodb-8.0.38-16-x86_64.<operating-system>.tar.gz` is the tarball for a [supported operating system](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mongodb).
- `percona-mongodb-mongosh-2.14.1-x86_64.tar.gz` is the tarball for `mongosh` shell.

Note that tarballs are available only for the x86_64 architecture.

## Tarball types

| Type     | Name                                                              | Description                                                                         |
| -------- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Full     | percona-server-mongodb-8.0.38-16-x86_64..tar.gz                   | Contains binaries and libraries                                                     |
| Minimal  | percona-server-mongodb-8.0.38-16-x86_64.-minimal.tar.gz           | Contains binaries and libraries without debug symbols                               |
| Checksum | percona-server-mongodb-8.0.38-16-x86_64.-minimal.tar.gz.sha256sum | Contains the MD5 checksum to verify the integrity of the files after the extraction |

## Preconditions

Install the following dependencies required to install Percona Server for MongoDB from tarballs.

**RHEL and derivatives**

```bash
sudo yum install openldap cyrus-sasl-gssapi curl
```

**Ubuntu**

Update the repositories and install the required packages:

```bash
sudo apt update
sudo apt install curl libsasl2-modules-gssapi-mit
```

**Debian**

Update the repositories and install the required packages:

```bash
sudo apt update
sudo apt install curl libsasl2-modules-gssapi-mit
```

## Procedure

The following steps show how to install Percona Server for MongoDB from a tarball.

**Red Hat and derivatives**

The following steps describe how to install Percona Server for MongoDB **on Oracle Linux 9.0**. They use the tarball package built for this operating system.

**If you are running a different operating system, you must download the tarball built for that OS version and replace its name and paths in the commands below.**

1. Fetch the binary tarballs:

   ```bash
   curl -O https://downloads.percona.com/downloads/percona-server-mongodb-8.0/percona-server-mongodb-8.0.38-16/binary/tarball/percona-server-mongodb-8.0.38-16-x86_64.ol9.tar.gz\
   curl -O https://downloads.percona.com/downloads/percona-server-mongodb-8.0/percona-server-mongodb-8.0.38-16/binary/tarball/percona-mongodb-mongosh-2.14.1-x86_64.tar.gz
   ```

1. Extract the tarballs

   ```bash
   tar -xf percona-server-mongodb-8.0.38-16-x86_64.ol9.tar.gz
   tar -xf percona-mongodb-mongosh-2.14.1-x86_64.tar.gz
   ```

1. Add the location of the binaries to the `PATH` variable:

   ```bash
   export PATH=~/percona-server-mongodb-8.0.38-16-x86_64.ol9/bin/:~/percona-mongodb-mongosh-2.14.1-x86_64/bin/:$PATH
   ```

1. Create the default data directory:

   ```bash
   sudo mkdir -p /data/db
   ```

1. Create a user and group for mongod

   ```bash
   sudo groupadd -r mongod
   sudo useradd -M -r -g mongod -d /var/lib/mongo -s /bin/false -c mongod mongod
   ```

1. The new TCMalloc requires [Restartable Sequences (rseq)](https://github.com/google/tcmalloc/blob/master/docs/design.md#restartable-sequences-and-per-cpu-tcmalloc) to implement [per-CPU caches](https://www.mongodb.com/docs/upcoming/reference/glossary/#std-term-per-CPU-cache) . To ensure that TCMalloc can use rseq, prevent glibc from registering an rseq structure. To do this, set the following environment variable:

   ```bash
   GLIBC_TUNABLES=glibc.pthread.rseq=0
   export GLIBC_TUNABLES
   ```

1. (Optional) Create a systemd unit file. Specify the following configuration:

   ```bash
   sudo tee /etc/systemd/system/mongod.service <<'EOF' > /dev/null
   [Unit]
   Description=MongoDB Database Server instance
   After=time-sync.target network.target

   [Service]
   User=mongod
   Group=mongod
   PermissionsStartOnly=true
   LimitFSIZE=infinity
   LimitCPU=infinity
   LimitAS=infinity
   LimitNOFILE=64000
   LimitNPROC=64000
   LimitMEMLOCK=infinity
   TasksMax=infinity
   TasksAccounting=false
   Environment="OPTIONS=-f /etc/mongod.conf"
   Environment="MONGODB_CONFIG_OVERRIDE_NOFORK=1"
   Environment="GLIBC_TUNABLES=glibc.pthread.rseq=0"
   EnvironmentFile=-/etc/sysconfig/mongod
   ExecStart=/usr/bin/mongod $OPTIONS
   RuntimeDirectory=mongodb
   ExecStartPre=/usr/bin/mkdir -p /var/run/mongodb
   ExecStartPre=/usr/bin/chown mongod:mongod /var/run/mongodb
   ExecStartPre=/usr/bin/chmod 0755 /var/run/mongodb
   PIDFile=/var/run/mongodb/mongod.pid
   ExecReload=/bin/kill -s HUP $MAINPID
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   EOF
   sudo systemctl daemon-reload
   sudo systemctl enable --now mongod
   ```

1. Make sure that you have read and write permissions for the data directory and run `mongod`.

**Debian and Ubuntu**

The following steps describe how to install Percona Server for MongoDB **on Ubuntu 22.04 (Jammy Jellyfish)**. They use the tarball package built for this operating system.

**If you are running a different operating system, you must download the tarball built for that OS version and replace its name and paths in the commands below.**

1. Fetch the binary tarballs:

   ```bash
   curl -O https://downloads.percona.com/downloads/percona-server-mongodb-8.0/percona-server-mongodb-8.0.38-16/binary/tarball/percona-server-mongodb-8.0.38-16-x86_64.jammy.tar.gz\
   curl -O https://downloads.percona.com/downloads/percona-server-mongodb-8.0/percona-server-mongodb-8.0.38-16/binary/tarball/percona-mongodb-mongosh-2.14.1-x86_64.tar.gz
   ```

1. Extract the tarballs

   ```bash
   tar -xf percona-server-mongodb-8.0.38-16-x86_64.jammy.tar.gz
   tar -xf percona-mongodb-mongosh-2.14.1-x86_64.tar.gz
   ```

1. Add the location of the binaries to the `PATH` variable:

   ```bash
   export PATH=~/percona-server-mongodb-8.0.38-16-x86_64.jammy/bin/:~/percona-mongodb-mongosh-2.14.1-x86_64/bin/:$PATH
   ```

1. Create the default data directory:

   ```bash
   mkdir -p /data/db
   ```

1. The new TCMalloc requires [Restartable Sequences (rseq)](https://github.com/google/tcmalloc/blob/master/docs/design.md#restartable-sequences-and-per-cpu-tcmalloc) to implement [per-CPU caches](https://www.mongodb.com/docs/upcoming/reference/glossary/#std-term-per-CPU-cache) . To ensure that TCMalloc can use rseq, prevent glibc from registering an rseq structure. To do this, set the following environment variable:

   ```bash
   GLIBC_TUNABLES=glibc.pthread.rseq=0
   export GLIBC_TUNABLES
   ```

1. Make sure that you have read and write permissions for the data directory and run `mongod`.

## Next steps

[Connect to MongoDB](https://docs.percona.com/percona-server-for-mongodb/8.0/connect.md)

> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server-for-mongodb/7.0/llms.txt).

# Install Percona Server for MongoDB from binary tarball

You can find links to the binary tarballs under the *Generic Linux* menu item on the [Percona website](https://www.percona.com/downloads/percona-server-mongodb-7.0/)

There are the following tarballs available:

`percona-server-mongodb-7.0.48-25-x86_64.<operating-system>.tar.gz` is the tarball for a [supported operating system](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mongodb).

- `percona-mongodb-mongosh-2.14.1-x86_64.tar.gz` is the tarball for `mongosh` shell.

Note that tarballs are available only for the x86_64 architecture.

## Tarball types

| Type     | Name                                                              | Description                                                                         |
| -------- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Full     | percona-server-mongodb-7.0.48-25-x86_64..tar.gz                   | Contains binaries and libraries                                                     |
| Minimal  | percona-server-mongodb-7.0.48-25-x86_64.-minimal.tar.gz           | Contains binaries and libraries without debug symbols                               |
| Checksum | percona-server-mongodb-7.0.48-25-x86_64.-minimal.tar.gz.sha256sum | Contains the MD5 checksum to verify the integrity of the files after the extraction |

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
   curl -O https://downloads.percona.com/downloads/percona-server-mongodb-7.0/percona-server-mongodb-7.0.48-25/binary/tarball/percona-server-mongodb-7.0.48-25-x86_64.ol9.tar.gz\
   curl -O https://downloads.percona.com/downloads/percona-server-mongodb-7.0/percona-server-mongodb-7.0.48-25/binary/tarball/percona-mongodb-mongosh-2.14.1-x86_64.tar.gz
   ```

1. Extract the tarballs

   ```bash
   tar -xf percona-server-mongodb-7.0.48-25-x86_64.ol9.tar.gz
   tar -xf percona-mongodb-mongosh-2.14.1-x86_64.tar.gz
   ```

1. Add the location of the binaries to the `PATH` variable:

   ```bash
   export PATH=~/percona-server-mongodb-7.0.48-25-x86_64.ol9/bin/:~/percona-mongodb-mongosh-2.14.1-x86_64/bin/:$PATH
   ```

1. Create the default data directory:

   ```bash
   sudo mkdir -p /data/db
   ```

1. Make sure that you have read and write permissions for the data directory and run `mongod`.

**Debian and Ubuntu**

The following steps describe how to install Percona Server for MongoDB **on Ubuntu 22.04 (Jammy Jellyfish)**. They use the tarball package built for this operating system.

**If you are running a different operating system, you must download the tarball built for that OS version and replace its name and paths in the commands below.**

1. Fetch the binary tarballs:

   ```bash
   curl -O https://downloads.percona.com/downloads/percona-server-mongodb-7.0/percona-server-mongodb-7.0.48-25/binary/tarball/percona-server-mongodb-7.0.48-25-x86_64.jammy.tar.gz\
   curl -O https://downloads.percona.com/downloads/percona-server-mongodb-7.0/percona-server-mongodb-7.0.48-25/binary/tarball/percona-mongodb-mongosh-2.14.1-x86_64.tar.gz
   ```

1. Extract the tarballs

   ```bash
   tar -xf percona-server-mongodb-7.0.48-25-x86_64.jammy.tar.gz
   tar -xf percona-mongodb-mongosh-2.14.1-x86_64.tar.gz
   ```

1. Add the location of the binaries to the `PATH` variable:

   ```bash
   export PATH=~/percona-server-mongodb-7.0.48-25-x86_64.jammy/bin/:~/percona-mongodb-mongosh-2.14.1-x86_64/bin/:$PATH
   ```

1. Create the default data directory:

   ```bash
   mkdir -p /data/db
   ```

1. Make sure that you have read and write permissions for the data directory and run `mongod`.

## Next steps

[Connect to MongoDB](https://docs.percona.com/percona-server-for-mongodb/7.0/connect.md)

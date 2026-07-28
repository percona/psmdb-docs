# Install Percona Server for MongoDB from binary tarball

You can find links to the binary tarballs under the *Generic Linux* menu item on the [Percona website](https://www.percona.com/downloads/percona-server-mongodb-6.0/)

There are the following tarballs available:

* `percona-server-mongodb-{{release}}-x86_64.<operating-system>.tar.gz` is the  tarball for a [supported operating system](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mongodb).

* `percona-mongodb-mongosh-{{mongosh}}-x86_64.tar.gz` is the tarball for `mongosh` shell.

Note that tarballs are available only for the x86_64 architecture.

## Tarball types

| Type | Name | Description |
|---|---|---|
| Full | percona-server-mongodb-{{release}}-x86_64.<operating-system>.tar.gz | Contains binaries and libraries |
| Minimal | percona-server-mongodb-{{release}}-x86_64.<operating-system>-minimal.tar.gz| Contains binaries and libraries without debug symbols|
| Checksum| percona-server-mongodb-{{release}}-x86_64.<operating-system>-minimal.tar.gz.sha256sum | Contains the MD5 checksum to verify the integrity of the files after the extraction|


## Preconditions

Install the following dependencies required to install Percona Server for MongoDB from tarballs.

=== ":material-redhat: RHEL and derivatives"

    ```bash
    sudo yum install openldap cyrus-sasl-gssapi curl
    ```

=== ":material-ubuntu: Ubuntu"

    Update the repositories and install the required packages:

    ```bash
    sudo apt update
    sudo apt install curl libsasl2-modules-gssapi-mit
    ```

=== ":material-debian: Debian"

    Update the repositories and install the required packages:

    ```bash
    sudo apt update
    sudo apt curl libsasl2-modules-gssapi-mit
    ```

## Procedure

The following steps show how to install Percona Server for MongoDB from a tarball. 
{.power-number}

=== ":material-redhat: Red Hat and derivatives"

    The following steps describe how to install Percona Server for MongoDB **on Oracle Linux 9.0**. They use the tarball package built for this operating system.

    **If you are running a different operating system, you must download the tarball built for that OS version and replace its name and paths in the commands below.**


    1. Fetch the binary tarballs:    

        ```bash
        curl -O https://downloads.percona.com/downloads/percona-server-mongodb-8.3/percona-server-mongodb-{{release}}/binary/tarball/percona-server-mongodb-{{release}}-x86_64.ol9.tar.gz
        curl -O https://downloads.percona.com/downloads/percona-server-mongodb-8.3/percona-server-mongodb-{{release}}/binary/tarball/percona-mongodb-mongosh-{{mongosh}}-x86_64.tar.gz
        ```

    2. Extract the tarballs    

        ```bash
        tar -xf percona-server-mongodb-{{release}}-x86_64.ol9.tar.gz
        tar -xf percona-mongodb-mongosh-{{mongosh}}-x86_64.tar.gz
        ```    

    3. Add the location of the binaries to the `PATH` variable:    

        ```bash
        export PATH=~/percona-server-mongodb-{{release}}-x86_64.ol9/bin/:~/percona-mongodb-mongosh-{{mongosh}}-x86_64/bin/:$PATH
        ```        

    4. Create the default data directory:    

        ```bash
        sudo mkdir -p /data/db
        ```    
    
    5. The new TCMalloc requires [Restartable Sequences (rseq) :octicons-link-external-16:](https://github.com/google/tcmalloc/blob/master/docs/design.md#restartable-sequences-and-per-cpu-tcmalloc) to implement [per-CPU caches :octicons-link-external-16:](https://www.mongodb.com/docs/upcoming/reference/glossary/#std-term-per-CPU-cache). To ensure that TCMalloc can use rseq, prevent glibc from registering an rseq structure. To do this, set the following environment variable:

    ```bash
    GLIBC_TUNABLES=glibc.pthread.rseq=0
    export GLIBC_TUNABLES

    6. Make sure that you have read and write permissions for the data
    directory and run `mongod`.

=== ":material-ubuntu: Debian and Ubuntu"

    The following steps describe how to install Percona Server for MongoDB **on Ubuntu 22.04 (Jammy Jellyfish)**. They use the tarball package built for this operating system.

    **If you are running a different operating system, you must download the tarball built for that OS version and replace its name and paths in the commands below.**

    1. Fetch the binary tarballs:    

        ```bash
        curl -O https://downloads.percona.com/downloads/percona-server-mongodb-8.3/percona-server-mongodb-{{release}}/binary/tarball/percona-server-mongodb-{{release}}-x86_64.jammy.tar.gz

        curl -O https://downloads.percona.com/downloads/percona-server-mongodb-8.3/percona-server-mongodb-{{release}}/binary/tarball/percona-mongodb-mongosh-{{mongosh}}-x86_64.tar.gz
        ```

    2. Extract the tarballs    

        ```bash
        tar -xf percona-server-mongodb-{{release}}-x86_64.jammy.tar.gz
        tar -xf percona-mongodb-mongosh-{{mongosh}}-x86_64.tar.gz
        ```    

    3. Add the location of the binaries to the `PATH` variable:    

        ```bash
        export PATH=~/percona-server-mongodb-{{release}}-x86_64.jammy/bin/:~/percona-mongodb-mongosh-{{mongosh}}-x86_64/bin/:$PATH
        ```        

    4. Create the default data directory:    

        ```bash
        mkdir -p /data/db
        ```    

    5. The new TCMalloc requires [Restartable Sequences (rseq) :octicons-link-external-16:](https://github.com/google/tcmalloc/blob/master/docs/design.md#restartable-sequences-and-per-cpu-tcmalloc) to implement [per-CPU caches :octicons-link-external-16:](https://www.mongodb.com/docs/upcoming/reference/glossary/#std-term-per-CPU-cache). To ensure that TCMalloc can use rseq, prevent glibc from registering an rseq structure. To do this, set the following environment variable:

        ```sh
        GLIBC_TUNABLES=glibc.pthread.rseq=0
        export GLIBC_TUNABLES
        ```
        
    6. Make sure that you have read and write permissions for the data
    directory and run `mongod`.

## Next steps

[Connect to MongoDB :material-arrow-right:](../connect.md){.md-button}

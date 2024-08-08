# Installing Percona Server for MongoDB from binary tarball

You can find links to the binary tarballs under the *Generic Linux* menu item on the [Percona website](https://www.percona.com/downloads/percona-server-mongodb-5.0/). The list provides a binary tarball for every [supported operating system](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mongodb).

## Tarball types

| Type | Name | Description |
|---|---|---|
| Full | percona-server-mongodb-{{release}}-x86_64.<operating-system>.tar.gz | Contains binaries and libraries |
| Minimal | percona-server-mongodb-{{release}}-x86_64.<operating-system>-minimal.tar.gz| Contains binaries and libraries without debug symbols|
| Checksum| percona-server-mongodb-{{release}}-x86_64.<operating-system>-minimal.tar.gz.sha256sum | Contains the MD5 checksum to verify the integrity of the files after the extraction|


## Preconditions

Install the following dependencies required to install Percona Server for MongoDB from tarballs.

=== ":material-redhat: RHEL and derivatives"

    ```{.bash data-prompt="$"}
    $ sudo yum install openldap cyrus-sasl-gssapi curl
    ```

=== ":material-ubuntu: Ubuntu"

    ```{.bash data-prompt="$"}
    $ sudo apt install curl libsasl2-modules-gssapi-mit
    ```

=== ":material-debian: Debian"
     
    ```{.bash data-prompt="$"}
    $ sudo apt curl libsasl2-modules-gssapi-mit
    ```

## Procedure

The following example installs Percona Server for MongoDB from a tarball on Ubuntu 22.04. Replace the link to the tarballs for your desired operating system in the following steps:
{.power-number}

1. Fetch the binary tarball:

    ```{.bash data-prompt="$"}
    $ wget https://www.percona.com/downloads/percona-server-mongodb-5.0/percona-server-mongodb-{{release}}/binary/tarball/percona-server-mongodb-{{release}}-x86_64.jammy.tar.gz\
    ```

2. Extract the tarball

    ```{.bash data-prompt='$'} 
    $ tar -xf percona-server-mongodb-{{release}}-x86_64.jammy.tar.gz
    ```

3. Add the location of the binaries to the `PATH` variable:

    ```{.bash data-prompt="$"}
    $ export PATH=~/percona-server-mongodb-{{release}}/bin/:$PATH
    ```

4. Create the default data directory:

    ```{.bash data-prompt="$"}
    $ mkdir -p /data/db
    ```

5. Make sure that you have read and write permissions for the data
directory and run `mongod`.

## Next steps

[Connect to MongoDB :material-arrow-right:](../connect.md){.md-button}

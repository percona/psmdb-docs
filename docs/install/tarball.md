# Install Percona Server for MongoDB from binary tarball

You can find links to the binary tarballs under the *Generic Linux* menu item on the [Percona website](https://www.percona.com/downloads/percona-server-mongodb-6.0/)

There are the following tarballs available:

* `percona-server-mongodb-{{release}}-x86_64.glibc2.17.tar.gz` is the general tarball, compatible with any [supported operating system](https://www.percona.com/services/policies/percona-software-support-lifecycle#mongodb) except Ubuntu 22.04.

* `percona-server-mongodb-{{release}}-x86_64.glibc2.35.tar.gz` is the tarball for Ubuntu 22.04.

* `percona-mongodb-mongosh-{{release}}-x86_64.tar.gz` is the tarball for `mongosh` shell.

## Preconditions

The following packages are required for the installation.

=== ":material-debian: Debian and Ubuntu"
     
     * `libcurl4`

     * `libsasl2-modules`

     * `libsasl2-modules-gssapi-mit`


=== ":material-redhat: Red hat Enterprise Linux and derivatives"

     * `libcurl`

     * `cyrus-sasl-gssapi`

     * `cyrus-sasl-plain`


## Procedure

The steps below describe the installation on Debian 10 (“buster”).
{.power-number}

1. Fetch and the binary tarballs:

    ```{.bash data-prompt="$"}
    $ wget https://www.percona.com/downloads/percona-server-mongodb-6.0/percona-server-mongodb-6.0.2-1/binary/tarball/percona-server-mongodb-6.0.2-1-x86_64.glibc2.17.tar.gz\
    $ wget https://www.percona.com/downloads/percona-server-mongodb-6.0/percona-server-mongodb-6.0.2-1/binary/tarball/percona-mongodb-mongosh-1.6.0-x86_64.tar.gz
    ```
2. Extract the tarballs

    ```{.bash data-prompt='$'} 
    $ tar -xf percona-server-mongodb-6.0.2-1-x86_64.glibc2.17.tar.gz
    $ tar -xf percona-mongodb-mongosh-1.6.0-x86_64.tar.gz
    ```


3. Add the location of the binaries to the `PATH` variable:

    ```{.bash data-prompt="$"}
    $ export PATH=~/percona-server-mongodb-6.0.2-1/bin/:~/percona-mongodb-mongosh-1.6.0/bin/:$PATH
    ```


4. Create the default data directory:

    ```{.bash data-prompt="$"}
    $ mkdir -p /data/db
    ```


5. Make sure that you have read and write permissions for the data
directory and run `mongod`.

## Next steps

[Connect to MongoDB :material-arrow-right:](../connect.md){.md-button}
# Installing Percona Server for MongoDB from Binary Tarball

Find links to the binary tarball under the *Generic Linux* menu item on the [Percona website](https://www.percona.com/downloads/percona-server-mongodb-4.2/)

There are two tarballs available:

* `percona-server-mongodb-<version>-x86_64.glibc2.17.tar.gz` is the general tarball, compatible with any [supported operating system](https://www.percona.com/services/policies/percona-software-support-lifecycle#mongodb) except Ubuntu 22.04.


* `percona-server-mongodb-<version>-x86_64.glibc2.35.tar.gz` is the tarball for Ubuntu 22.04.

## Procedure

The steps below describe the installation on Debian 10 (“buster”).

1. Fetch and extract the correct binary tarball:

    ```{.bash data-prompt="$"}
    $ wget https://www.percona.com/downloads/percona-server-mongodb-4.2/percona-server-mongodb-4.2.9-10/binary/tarball/percona-server-mongodb-4.2.9-10-x86_64.glibc2.17.tar.gz\
    $ tar -xf percona-server-mongodb-4.2.9-10-x86_64.glibc2.17.tar.gz
    ```


2. Add the location of the binaries to the `PATH` variable:

    ```{.bash data-prompt="$"}
    $ export PATH=~/percona-server-mongodb-4.2.9-10/bin/:$PATH
    ```


3. Create the default data directory:

    ```{.bash data-prompt="$"}
    $ mkdir -p /data/db
    ```


4. Make sure that you have read and write permissions for the data
directory and run `mongod`.

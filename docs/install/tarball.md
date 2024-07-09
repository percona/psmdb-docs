# Installing Percona Server for MongoDB from binary tarball

You can find links to the binary tarballs under the *Generic Linux* menu item on the [Percona website](https://www.percona.com/downloads/percona-server-mongodb-5.0/)

There are two tarballs available:

* `percona-server-mongodb-{{release}}-x86_64.glibc2.17.tar.gz` is the general tarball, compatible with any [supported operating system](https://www.percona.com/services/policies/percona-software-support-lifecycle#mongodb) except Ubuntu 22.04.

* `percona-server-mongodb-{{release}}-x86_64.glibc2.35.tar.gz` is the tarball for Ubuntu 22.04.

To check which `glibc` version your system is using, run the following command:

```{.bash data-prompt="$"}
$ ldd --version
```

??? example "Sample output"

    ```{.text .no-copy}
    ldd (GNU libc) 2.28
    Copyright (C) 2018 Free Software Foundation, Inc.
    This is free software; see the source for copying conditions.  There is NO
    warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    Written by Roland McGrath and Ulrich Drepper.
    ```

## What tarballs to choose

The following table helps you understand what tarball to download based on the glibc version of your operating system.

| Operating system | Tarball to download | glibc version  |
|------------------|---------------------|----------------|
| Ubuntu 22.04         | percona-server-mongodb-{{release}}-x86_64.glibc2.35.tar.gz     | glibc2.35 |
| Ubuntu 20.04         | percona-server-mongodb-{{release}}-x86_64.glibc2.17.tar.gz     | glibc2.31 |
| Debian 11            | percona-server-mongodb-{{release}}-x86_64.glibc2.17.tar.gz     | glibc2.31 |
| Debian 10            | percona-server-mongodb-{{release}}-x86_64.glibc2.17.tar.gz     | glibc2.28 |   
| Red Hat Enterprise 8 | percona-server-mongodb-{{release}}-x86_64.glibc2.17.tar.gz     | glibc2.28 |
| Red Hat Enterprise 7 | percona-server-mongodb-{{release}}-x86_64.glibc2.17.tar.gz     | glibc2.17 |

### Tarball types

| Type | Name | Description |
|---|---|---|
| Full | percona-server-mongodb-{{release}}-x86_64.<glibc-version>.tar.gz | Contains binaries and libraries |
| Minimal | percona-server-mongodb-{{release}}-x86_64.<glibc-version>-minimal.tar.gz| Contains binaries and libraries without debug symbols|
| Checksum| percona-server-mongodb-{{release}}-x86_64.<glibc-version>-minimal.tar.gz.sha256sum | Contains the MD5 checksum to verify the integrity of the files after extraction|


## Preconditions

The following packages are required for the installation.

=== ":material-debian: On Debian and Ubuntu"

     * `libcurl4`

     * `libsasl2-modules`

     * `libsasl2-modules-gssapi-mit`

=== ":material-redhat: On Red Hat Enterprise Linux and derivatives"
     
     * `libcurl`

     * `cyrus-sasl-gssapi`

     * `cyrus-sasl-plain`

Check that they are installed in your operating system. Otherwise install them.

## Procedure

The steps below describe the installation on Debian 10 (“buster”).
{.power-number}

1. Fetch and extract the binary tarball:

    ```{.bash data-prompt="$"}
    $ wget https://www.percona.com/downloads/percona-server-mongodb-5.0/percona-server-mongodb-5.0.2-1/binary/tarball/percona-server-mongodb-5.0.2-1-x86_64.glibc2.17.tar.gz\
    $ tar -xf percona-server-mongodb-5.0.2-1-x86_64.glibc2.17.tar.gz
    ```

2. Add the location of the binaries to the `PATH` variable:

    ```{.bash data-prompt="$"}
    $ export PATH=~/percona-server-mongodb-5.0.2-1/bin/:$PATH
    ```


3. Create the default data directory:

    ```{.bash data-prompt="$"}
    $ mkdir -p /data/db
    ```


4. Make sure that you have read and write permissions for the data
directory and run `mongod`.

## Next steps

[Connect to MongoDB :material-arrow-right:](../connect.md){.md-button}

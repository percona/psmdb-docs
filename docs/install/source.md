# Build from source code

You can build Percona Server for MongoDB from the source code either manually or using the build script. 

## Manual build 

To build Percona Server for MongoDB, you need the following:

- A modern C++ compiler capable of compiling C++17 like GCC 8.2 or newer 
- Amazon AWS Software Development Kit for C++ library 
- Python 3.7.x and Pip modules. 
- The set of dependencies for your operating system:


   | Linux Distribution              | Dependencies
   | --------------------------------|---------------------------
   | Debian/Ubuntu                   | python3 python3-dev python3-pip scons gcc g++ cmake curl libssl-dev libldap2-dev libkrb5-dev libcurl4-openssl-dev libsasl2-dev liblz4-dev libpcap-dev libbz2-dev libsnappy-dev zlib1g-dev libzlcore-dev libsasl2-dev liblzma-dev libext2fs-dev e2fslibs-dev bear|
   | RedHat Enterprise Linux/CentOS 8| python38 python38-devel python38-pip python3-scons gcc-toolset-9 gcc-c++ gcc-toolset-11-dwz gcc-toolset-11-elfutils cmake3 wget openssl-devel zlib-devel cyrus-sasl-devel xz-devel bzip2-devel libcurl-devel lz4-devel e2fsprogs-devel krb5-devel openldap-devel expat-devel cmake make|  

- About 13 GB of disk space for the core binaries (`mongod`, `mongos`, and `mongo`) and about 600 GB for the install-all target.

### Build steps

1. Clone Percona Server for MongoDB and the AWS Software Development Kit for C++ repositories

    ```{.bash data-prompt="$"}
    $ git clone https://github.com/percona/percona-server-mongodb.git
    $ git clone https://github.com/aws/aws-sdk-cpp.git
    ```

2. Switch to the Percona Server for MongoDB branch that you are building
   and install Python3 modules

    ```{.bash data-prompt="$"}
    $ cd percona-server-mongodb && git checkout v6.0
    $ pip3 install --user -r etc/pip/dev-requirements.txt
    ```

3. Define Percona Server for MongoDB version (6.0.6 for the time of
   writing this document)

    ```{.bash data-prompt="$"}
    $ echo '{"version": "6.0.6"}' > version.json
    ```

4. Install the dependencies for your operating system. 

    === "Debian/Ubuntu"

        The following command installs the dependencies for Ubuntu 20.04:

        ```{.bash data-prompt="$"}
        $ sudo apt install -y python3 python3-dev python3-pip scons gcc g++ cmake curl libssl-dev libldap2-dev libkrb5-dev libcurl4-openssl-dev libsasl2-dev liblz4-dev libpcap-dev libbz2-dev libsnappy-dev zlib1g-dev libzlcore-dev libsasl2-dev liblzma-dev libext2fs-dev e2fslibs-dev bear
        ```
    
    === "RHEL / CentOS"

        1. Install the dependencies. The following command installs the dependencies for CentOS 8:

            ```{.bash data-prompt="$"}
            $ sudo yum -y install centos-release-scl epel-release 
            $ sudo yum -y install python38 python38-devel python38-pip python3-scons gcc-toolset-9 gcc-c++ gcc-toolset-11-dwz gcc-toolset-11-elfutils cmake3 wget openssl-devel zlib-devel cyrus-sasl-devel xz-devel bzip2-devel libcurl-devel lz4-devel e2fsprogs-devel krb5-devel openldap-devel expat-devel cmake make
            ```

        2. Build a specific ``curl`` version

            -  Fetch the package archive  
                ```{.bash data-prompt="$"}
                $ wget https://curl.se/download/curl-7.66.0.tar.gz
                ```  
            -  Unzip the package  
                ```{.bash data-prompt="$"}
                $ tar -xvzf curl-7.66.0.tar.gz && cd curl-7.66.0
                ```  
            -  Configure and build the package  
                ```{.bash data-prompt="$"}
                $ ./configure
                $ sudo make install
                ```

5. Build the AWS Software Development Kit for C++ library

    -  Create a directory to store the AWS library 

        ```{.bash data-prompt="$"}
        $ mkdir -p /tmp/lib/aws
        ``` 

    -  Declare an environment variable ``AWS_LIBS`` for this directory 

        ```{.bash data-prompt="$"}
        $ export AWS_LIBS=/tmp/lib/aws
        ``` 

    -  Percona Server for MongoDB is built with AWS SDK CPP 1.8.187
       version. Switch to this version 

        ```{.bash data-prompt="$"}
        $ cd aws-sdk-cpp && git checkout 1.8.187
        ``` 

    -  It is recommended to keep build files outside the SDK directory.
       Create a build directory and navigate to it 

        ```{.bash data-prompt="$"}
        $ mkdir build && cd build
        ``` 

    -  Generate build files using ``cmake`` 

        ```{.bash data-prompt="$"}
        $ cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_ONLY="s3;transfer" -DBUILD_SHARED_LIBS=OFF -DMINIMIZE_SIZE=ON -DCMAKE_INSTALL_PREFIX="${AWS_LIBS}"
        ``` 

    -  Install the SDK 

        ```{.bash data-prompt="$"}
        $ make install
        ```

6. Build Percona Server for MongoDB

    -  Change directory to ``percona-server-mongodb`` 

        ```{.bash data-prompt="$"}
        $ cd percona-server-mongodb
        ``` 

    -  Build Percona Server for MongoDB from ``buildscripts/scons.py``.
        
        ```{.bash data-prompt="$"}
        $ buildscripts/scons.py -j$(nproc --all) --jlink=2 --disable-warnings-as-errors --ssl --opt=on --use-sasl-client --wiredtiger --audit --inmemory --hotbackup CPPPATH="${AWS_LIBS}/include" LIBPATH="${AWS_LIBS}/lib" install-mongod
        ``` 

       This command builds only the database. Other available targets for the
       ``scons`` command are:  

       - ``mongod`` 
       - ``mongos`` 
       - ``mongo`` 
       - ``core`` (includes ``mongod``, ``mongos``, ``mongo``) 
       - ``all``

The built binaries are in the ``percona-server-mongodb`` directory.

## Use the build script

To automate the build process, Percona provides the build script. With this script you can either build binary tarballs or DEB/RPM packages to install Percona Server for MongoDB from. 

### Prerequisites

To use the build script you need the following:

* Docker up and running on your machine
* About 200GB of disk space

### Prepare the build environment

1. Create the folder where all build actions take place. For the steps below we use the `/tmp/psmdb/test` folder.
2. Navigate to the build folder and download the build script. Replace the `<tag>` placeholder with the required version of Percona Server for MongoDB:

    ```{.bash data-prompt="$"}
    $ wget https://raw.githubusercontent.com/percona/percona-server-mongodb/psmdb-<tag>/percona-packaging/scripts/psmdb_builder.sh -O psmdb_builder.sh 
    ```

### Build steps

Use the following instructions depending on what you wish to build:

=== "Build tarballs"

    ```{.bash data-prompt="$"}
    $ docker run -ti -u root -v /tmp/psmdb:/tmp/psmdb rhel:8 sh -c '
    set -o xtrace
    cd /tmp/psmdb
    bash -x ./psmdb_builder.sh --builddir=/tmp/psmdb/test --install_deps=1
    bash -x ./psmdb_builder.sh --builddir=/tmp/psmdb/test --repo=https://github.com/percona/percona-server-mongodb.git \
    --branch=release-6.0.6-5 --psm_ver=6.0.6 --psm_release=5 --mongo_tools_tag=100.7.0 --jemalloc_tag=psmdb-3.2.11-3.1 --get_sources=1
    '
    ```

    The command does the following:

    * runs Docker daemon as the root user using the RHEL 8 image
    * mounts the build directory into the container
    * establishes the shell session inside the container
    * inside the container, navigates to the build directory and runs the build script to install dependencies 
    * runs the build script again to build the tarball for the PSMDB version 6.0.6-5

    Check that tarballs are built:

    ```{.bash data-prompt="$"}
    $ ls -la /tmp/psmdb/test/source_tarball/
    ```

    Sample output:

    ```{.text .no-copy}
    total 88292
    -rw-r--r--. 1 root root 90398894 Jul  1 10:58 percona-server-mongodb-6.0.6-5.tar.gz
    ```

=== "Build packages"

    1. Build source packages

        === "DEB"

            ```{.bash data-prompt="$"}
            $ docker run -ti -u root -v /tmp/psmdb:/tmp/psmdb ubuntu:jammy sh -c '
            set -o xtrace
            cd /tmp/psmdb
            bash -x ./psmdb_builder.sh --builddir=/tmp/psmdb/test --install_deps=1
            bash -x ./psmdb_builder.sh --builddir=/tmp/psmdb/test --repo=https://github.com/percona/percona-server-mongodb.git \
            --branch=release-6.0.6-5 --psm_ver=6.0.6--psm_release=5 --mongo_tools_tag=100.7.0 --jemalloc_tag=psmdb-3.2.11-3.1 --build_src_deb=1
            '
            ```

            Check that source packages are created

            ```{.bash data-prompt="$"}
            $ ls -la /tmp/psmdb/test/source_deb/
            ```

            Sample output:

            ```{.text .no-copy}
            rw-r--r--. 1 root root 90398894 Jul  1 11:45 percona-server-mongodb_6.0.6.orig.tar.gz
            ```
        
        === "RPM"

            ```{.bash data-prompt="$"}
            $ docker run -ti -u root -v /tmp/psmdb:/tmp/psmdb ubuntu:jammy sh -c '
            set -o xtrace
            cd /tmp/psmdb
            bash -x ./psmdb_builder.sh --builddir=/tmp/psmdb/test --install_deps=1
            bash -x ./psmdb_builder.sh --builddir=/tmp/psmdb/test --repo=https://github.com/percona/percona-server-mongodb.git \
            --branch=release-6.0.6-5 --psm_ver=6.0.6--psm_release=5 --mongo_tools_tag=100.7.0 --jemalloc_tag=psmdb-3.2.11-3.1 --build_src_rpm=1
            '
            ```

            Check that source packages are created

            ```{.bash data-prompt="$"}
            $ ls -la /tmp/psmdb/test/srpm/
            ```

            Sample output:

            ```{.text .no-copy}
            rw-r--r--. 1 root root 90398894 Jul  1 11:45 percona-server-mongodb-6.0.6-5.generic.src.rpm
            ```

    2. Build Percona Server for MongoDB packages

        === "DEB"

            ```{.bash data-prompt="$"}
            $ docker run -ti -u root -v /tmp/psmdb:/tmp/psmdb ubuntu:jammy sh -c '
            set -o xtrace
            cd /tmp/psmdb
            bash -x ./psmdb_builder.sh --builddir=/tmp/psmdb/test --install_deps=1
            bash -x ./psmdb_builder.sh --builddir=/tmp/psmdb/test --repo=https://github.com/percona/percona-server-mongodb.git \
            --branch=release-6.0.6-5 --psm_ver=6.0.6 --psm_release=5 --mongo_tools_tag=100.7.0 --jemalloc_tag=psmdb-3.2.11-3.1 --build_deb=1
            '
            ```

            Check that source packages are created

            ```{.bash data-prompt="$"}
            $ ls -la /tmp/psmdb/test/deb/
            ```

            Sample output:

            ```{.text .no-copy}
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-dbg_6.0.6-5.jammy_amd64.deb  
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-mongos_6.0.6-5.jammy_amd64.deb 
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-server_6.0.6-5.jammy_amd64.deb 
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-tools_6.0.6-5.jammy_amd64.deb  
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb_6.0.6-5.jammy_amd64.deb
            ```
        
        === "RPM"

            ```{.bash data-prompt="$"}
            $ docker run -ti -u root -v /tmp/psmdb:/tmp/psmdb ubuntu:jammy sh -c '
            set -o xtrace
            cd /tmp/psmdb
            bash -x ./psmdb_builder.sh --builddir=/tmp/psmdb/test --install_deps=1
            bash -x ./psmdb_builder.sh --builddir=/tmp/psmdb/test --repo=https://github.com/percona/percona-server-mongodb.git \
            --branch=release-6.0.6-5 --psm_ver=6.0.6 --psm_release=5 --mongo_tools_tag=100.7.0 --jemalloc_tag=psmdb-3.2.11-3.1 --build_rpm=1
            '
            ```

            Check that source packages are created

            ```{.bash data-prompt="$"}
            $ ls -la /tmp/psmdb/test/srpm/
            ```

            Sample output:

            ```{.text .no-copy}
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-6.0.6-5.el8.x86_64.rpm  
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-debugsource-6.0.6-5.el8.x86_64.rpm 
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-mongos-6.0.6-5.el8.x86_64.rpm    
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-mongos-debuginfo-6.0.6-5.el8.x86_64.rpm 
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-server-6.0.6-5.el8.x86_64.rpm    
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-server-debuginfo-6.0.6-5.el8.x86_64.rpm 
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-tools-6.0.6-5.el8.x86_64.rpm 
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-tools-debuginfo-6.0.6-5.el8.x86_64.rpm
            ```

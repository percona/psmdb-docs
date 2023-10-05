# Build from source code

You can build Percona Server for MongoDB from the source code either manually or using the build script. 

## Manual build 

To build Percona Server for MongoDB manually, you need the following:

- A modern C++ compiler capable of compiling C++17 like GCC 8.2 or newer 
- Amazon AWS Software Development Kit for C++ library 
- Python 3.7.x and Pip modules. 
- The set of dependencies for your operating system. The following table lists dependencies for Ubuntu 22.04 and Red Hat Enterprise 9 and compatible derivatives:


   | Linux Distribution              | Dependencies
   | --------------------------------|---------------------------
   | Debian/Ubuntu                   | gcc g++ cmake curl libssl-dev libldap2-dev libkrb5-dev libcurl4-openssl-dev libsasl2-dev liblz4-dev libbz2-dev libsnappy-dev zlib1g-dev libzlcore-dev liblzma-dev e2fslibs-dev|
   | RedHat Enterprise Linux/CentOS 9| gcc gcc-c++ cmake curl openssl-devel openldap-devel krb5-devel libcurl-devel cyrus-sasl-devel bzip2-devel zlib-devel lz4-devel xz-devel e2fsprogs-devel|  

- About 13 GB of disk space for the core binaries (`mongod`, `mongos`, and `mongo`) and about 600 GB for the `install-all` target.

### Build steps

#### Install Python and Python modules

1. Make sure the `python3`, `python3-dev`, `python3-pip` Python packages are installed on your machine. Otherwise, install them using the package manager of your operating system.

2. Clone Percona Server for MongoDB repository

    ```{.bash data-prompt="$"}
    $ git clone https://github.com/percona/percona-server-mongodb.git
    ```

3. Switch to the Percona Server for MongoDB branch that you are building
   and install Python3 modules

    ```{.bash data-prompt="$"}
    $ cd percona-server-mongodb && git checkout v7.0
    $ python3 -m pip install --user -r etc/pip/dev-requirements.txt
    ```

4. Define Percona Server for MongoDB version (7.0.2 for the time of
   writing this document)

    ```{.bash data-prompt="$"}
    $ echo '{"version": "7.0.2"}' > version.json
    ```

#### Install operating system dependencies

=== "Debian/Ubuntu"

    The following command installs the dependencies for Ubuntu 22.04:

    ```{.bash data-prompt="$"}
    $ sudo apt install -y gcc g++ cmake curl libssl-dev libldap2-dev libkrb5-dev libcurl4-openssl-dev libsasl2-dev liblz4-dev libbz2-dev libsnappy-dev zlib1g-dev libzlcore-dev liblzma-dev e2fslibs-dev
    ```

=== "RHEL / CentOS"

    The following command installs the dependencies for CentOS 9:

    ```{.bash data-prompt="$"}
    $ sudo yum -y install gcc gcc-c++ cmake curl openssl-devel openldap-devel krb5-devel libcurl-devel cyrus-sasl-devel bzip2-devel zlib-devel lz4-devel xz-devel e2fsprogs-devel
    ```

#### Build AWS Software Development Kit for C++ library

1. Clone the AWS Software Development Kit for C++ repository

    ```{.bash data-prompt="$"}
    $ git clone --recurse-submodules https://github.com/aws/aws-sdk-cpp.git
    ```

2. Create a directory to store the AWS library 

    ```{.bash data-prompt="$"}
    $ mkdir -p /tmp/lib/aws
    ``` 

3.  Declare an environment variable ``AWS_LIBS`` for this directory 
    ```{.bash data-prompt="$"}
    $ export AWS_LIBS=/tmp/lib/aws
    ``` 

4. Percona Server for MongoDB is built with AWS SDK CPP 1.9.379
   version. Switch to this version 

    ```{.bash data-prompt="$"}
    $ cd aws-sdk-cpp && git checkout 1.9.379
    ``` 

5. It is recommended to keep build files outside the SDK directory.
   Create a build directory and navigate to it 

    ```{.bash data-prompt="$"}
    $ mkdir build && cd build
    ``` 

6.  Generate build files using ``cmake`` 

     ```{.bash data-prompt="$"}
     $ cmake .. -DCMAKE_BUILD_TYPE=Release '-DBUILD_ONLY=s3;transfer' -DBUILD_SHARED_LIBS=OFF -DMINIMIZE_SIZE=ON -DCMAKE_INSTALL_PREFIX="${AWS_LIBS}"
     ```

7.  Install the SDK 

    ```{.bash data-prompt="$"}
    $ make install
    ```

#### Build Percona Server for MongoDB

1. Change directory to ``percona-server-mongodb`` 
   
    ```{.bash data-prompt="$"}
    $ cd percona-server-mongodb
    ``` 

2. Build Percona Server for MongoDB from ``buildscripts/scons.py``
     
    ```{.bash data-prompt="$"}
    $ buildscripts/scons.py --disable-warnings-as-errors --release --ssl --opt=on -j$(nproc --all) --use-sasl-client --wiredtiger --audit --inmemory --hotbackup CPPPATH="${AWS_LIBS}/include" LIBPATH="${AWS_LIBS}/lib ${AWS_LIBS}/lib64" install-mongod install-mongos 
    ```  

   This command builds core components of the database. Other available targets for the
   ``scons`` command are:  
  
   - `install-mongod`
   - `install-mongos`
   - `install-servers` (includes mongod and mongos)
   - `install-core` (includes mongod and mongos)
   - `install-devcore` (includes mongod, mongos, and jstestshell (formerly mongo shell))
   - `install-all`

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

    The following command builds tarballs of Percona Server for MongoDB 7.0.2-1 on Red Hat Enterprise Linux 9. Change the Docker image and the values for `--branch`, `--psm_ver`, `--psm_release` flags to build tarballs of a different version and on a different operating system.

    ```{.bash data-prompt="$"}
    $ docker run -ti -u root -v /tmp/psmdb:/tmp/psmdb rhel:9 sh -c '
    set -o xtrace
    cd /tmp/psmdb
    bash -x ./psmdb_builder.sh --builddir=/tmp/psmdb/test --install_deps=1
    bash -x ./psmdb_builder.sh --builddir=/tmp/psmdb/test --repo=https://github.com/percona/percona-server-mongodb.git \
    --branch=release-7.0.2-1 --psm_ver=7.0.2 --psm_release=1 --mongo_tools_tag=100.7.0 --jemalloc_tag=psmdb-3.2.11-3.1 --get_sources=1
    '
    ```

    The command does the following:

    * runs Docker daemon as the root user using the RHEL 9 image
    * mounts the build directory into the container
    * establishes the shell session inside the container
    * inside the container, navigates to the build directory and runs the build script to install dependencies 
    * runs the build script again to build the tarball for the PSMDB version 7.0.2-1

    Check that tarballs are built:

    ```{.bash data-prompt="$"}
    $ ls -la /tmp/psmdb/test/source_tarball/
    ```

    Sample output:

    ```{.text .no-copy}
    total 88292
    -rw-r--r--. 1 root root 90398894 Jul  1 10:58 percona-server-mongodb-7.0.2-1.tar.gz
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
            --branch=release-7.0.2-1 --psm_ver=7.0.2--psm_release=1 --mongo_tools_tag=100.7.0 --jemalloc_tag=psmdb-3.2.11-3.1 --build_src_deb=1
            '
            ```

            Check that source packages are created

            ```{.bash data-prompt="$"}
            $ ls -la /tmp/psmdb/test/source_deb/
            ```

            Sample output:

            ```{.text .no-copy}
            rw-r--r--. 1 root root 90398894 Jul  1 11:45 percona-server-mongodb_7.0.2.orig.tar.gz
            ```
        
        === "RPM"

            ```{.bash data-prompt="$"}
            $ docker run -ti -u root -v /tmp/psmdb:/tmp/psmdb ubuntu:jammy sh -c '
            set -o xtrace
            cd /tmp/psmdb
            bash -x ./psmdb_builder.sh --builddir=/tmp/psmdb/test --install_deps=1
            bash -x ./psmdb_builder.sh --builddir=/tmp/psmdb/test --repo=https://github.com/percona/percona-server-mongodb.git \
            --branch=release-7.0.2-1 --psm_ver=7.0.2--psm_release=1 --mongo_tools_tag=100.7.0 --jemalloc_tag=psmdb-3.2.11-3.1 --build_src_rpm=1
            '
            ```

            Check that source packages are created

            ```{.bash data-prompt="$"}
            $ ls -la /tmp/psmdb/test/srpm/
            ```

            Sample output:

            ```{.text .no-copy}
            rw-r--r--. 1 root root 90398894 Jul  1 11:45 percona-server-mongodb-7.0.2-1.generic.src.rpm
            ```

    2. Build Percona Server for MongoDB packages

        === "DEB"

            ```{.bash data-prompt="$"}
            $ docker run -ti -u root -v /tmp/psmdb:/tmp/psmdb ubuntu:jammy sh -c '
            set -o xtrace
            cd /tmp/psmdb
            bash -x ./psmdb_builder.sh --builddir=/tmp/psmdb/test --install_deps=1
            bash -x ./psmdb_builder.sh --builddir=/tmp/psmdb/test --repo=https://github.com/percona/percona-server-mongodb.git \
            --branch=release-7.0.2-1 --psm_ver=7.0.2--psm_release=1 --mongo_tools_tag=100.7.0 --jemalloc_tag=psmdb-3.2.11-3.1 --build_deb=1
            '
            ```

            Check that source packages are created

            ```{.bash data-prompt="$"}
            $ ls -la /tmp/psmdb/test/deb/
            ```

            Sample output:

            ```{.text .no-copy}
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-dbg_7.0.2-1.jammy_amd64.deb  
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-mongos_7.0.2-1.jammy_amd64.deb 
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-server_7.0.2-1.jammy_amd64.deb 
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-tools_7.0.2-1.jammy_amd64.deb  
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb_7.0.2-1.jammy_amd64.deb
            ```
        
        === "RPM"

            ```{.bash data-prompt="$"}
            $ docker run -ti -u root -v /tmp/psmdb:/tmp/psmdb ubuntu:jammy sh -c '
            set -o xtrace
            cd /tmp/psmdb
            bash -x ./psmdb_builder.sh --builddir=/tmp/psmdb/test --install_deps=1
            bash -x ./psmdb_builder.sh --builddir=/tmp/psmdb/test --repo=https://github.com/percona/percona-server-mongodb.git \
            --branch=release-7.0.2-1 --psm_ver=7.0.2 --psm_release=1 --mongo_tools_tag=100.7.0 --jemalloc_tag=psmdb-3.2.11-3.1 --build_rpm=1
            '
            ```

            Check that source packages are created

            ```{.bash data-prompt="$"}
            $ ls -la /tmp/psmdb/test/srpm/
            ```

            Sample output:

            ```{.text .no-copy}
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-7.0.2-1.el8.x86_64.rpm  
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-debugsource-7.0.2-1.el8.x86_64.rpm 
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-mongos-7.0.2-1.el8.x86_64.rpm    
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-mongos-debuginfo-7.0.2-1.el8.x86_64.rpm 
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-server-7.0.2-1.el8.x86_64.rpm    
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-server-debuginfo-7.0.2-1.el8.x86_64.rpm 
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-tools-7.0.2-1.el8.x86_64.rpm 
            rw-r--r--. 1 root root 90398894 Jul  1 13:16 percona-server-mongodb-tools-debuginfo-7.0.2-1.el8.x86_64.rpm
            ```

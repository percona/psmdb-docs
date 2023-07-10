# Build from source code

To build Percona Server for MongoDB, you need: 

- A modern C++ compiler capable of compiling C++17 like GCC 8.2 or newer 
- Amazon AWS Software Development Kit for C++ library 
- Python 3.6.x and Pip. 
- The set of dependencies for your operating system:


   | Linux Distribution              | Dependencies
   | --------------------------------|---------------------------
   | Debian/Ubuntu                   | python3 python3-dev python3-pip scons gcc g++ cmake curl libssl-dev libldap2-dev libkrb5-dev libcurl4-openssl-dev libsasl2-dev liblz4-dev libpcap-dev libbz2-dev libsnappy-dev zlib1g-dev libzlcore-dev libsasl2-dev liblzma-dev libext2fs-dev e2fslibs-dev bear|
   | CentOS / RedHat Enterprise Linux| centos-release-scl epel-release python3 python3-devel scons gcc gcc-c++ cmake3 openssl-devel cyrus-sasl-devel snappy-devel zlib-devel bzip2-devel libcurl-devel lz4-devel openldap-devel krb5-devel xz-devel e2fsprogs-devel expat-devel devtoolset-8-gcc devtoolset-8-gcc-c++|   
   | RedHat Enterprise Linux/CentOS 8| python36 python36-devel gcc-c++ gcc cmake3 wget openssl-devel zlib-devel cyrus-sasl-devel xz-devel bzip2-devel libcurl-devel lz4-devel e2fsprogs-devel krb5-devel openldap-devel expat-devel cmake|  

## Build steps

### Debian/Ubuntu

1. Clone this repository and the AWS Software Development Kit for C++
   repository

    ```{.bash code-prompt="$"}
    $ git clone https://github.com/percona/percona-server-mongodb.git
    $ git clone https://github.com/aws/aws-sdk-cpp.git
    ```

2. Install the dependencies for your operating system. The following
   command installs the dependencies for Ubuntu 20.04:

    ```{.bash code-prompt="$"}
    $ sudo apt install -y python3 python3-dev python3-pip scons gcc g++ cmake curl libssl-dev libldap2-dev libkrb5-dev libcurl4-openssl-dev libsasl2-dev liblz4-dev libpcap-dev libbz2-dev libsnappy-dev zlib1g-dev libzlcore-dev libsasl2-dev liblzma-dev libext2fs-dev e2fslibs-dev bear
    ```

3. Switch to the Percona Server for MongoDB branch that you are building
   and install Python3 modules

    ```{.bash code-prompt="$"}
    $ cd percona-server-mongodb && git checkout v5.0
    $ pip3 install --user -r etc/pip/dev-requirements.txt
    ```

4. Define Percona Server for MongoDB version (5.0.2 for the time of
   writing this document)

    ```{.bash code-prompt="$"}
    $ echo '{"version": "5.0.2"}' > version.json
    ```

5. Build the AWS Software Development Kit for C++ library

    -  Create a directory to store the AWS library 

        ```{.bash code-prompt="$"}
        $ mkdir -p /tmp/lib/aws
        ``` 

    -  Declare an environment variable ``AWS_LIBS`` for this directory 

        ```{.bash code-prompt="$"}
        $ export AWS_LIBS=/tmp/lib/aws
        ``` 

    -  Percona Server for MongoDB is built with AWS SDK CPP 1.8.187
       version. Switch to this version 

        ```{.bash code-prompt="$"}
        $ cd aws-sdk-cpp && git checkout 1.8.187
        ``` 

    -  It is recommended to keep build files outside the SDK directory.
       Create a build directory and navigate to it 

        ```{.bash code-prompt="$"}
        $ mkdir build && cd build
        ``` 

    -  Generate build files using ``cmake`` 

        ```{.bash code-prompt="$"}
        $ cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_ONLY="s3;transfer" -DBUILD_SHARED_LIBS=OFF -DMINIMIZE_SIZE=ON -DCMAKE_INSTALL_PREFIX="${AWS_LIBS}"
        ``` 

    -  Install the SDK 

        ```{.bash code-prompt="$"}
        $ make install
        ```

6. Build Percona Server for MongoDB

    -  Change directory to ``percona-server-mongodb`` 

        ```{.bash code-prompt="$"}
        $ cd percona-server-mongodb
        ``` 

    -  Build Percona Server for MongoDB from ``buildscripts/scons.py``.
        
        ```{.bash code-prompt="$"}
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

### Red Hat Enterprise Linux/CentOS

1. Clone this repository and the AWS Software Development Kit for C++
   repository

    ```{.bash code-prompt="$"}
    $ git clone https://github.com/percona/percona-server-mongodb.git
    $ git clone https://github.com/aws/aws-sdk-cpp.git
    ```

2. Install the dependencies for your operating system. The following
   command installs the dependencies for CentOS 7:

    ```{.bash code-prompt="$"}
    $ sudo yum -y install centos-release-scl epel-release 
    $ sudo yum -y install python3 python3-devel scons gcc gcc-c++ cmake3 openssl-devel cyrus-sasl-devel snappy-devel zlib-devel bzip2-devel libcurl-devel lz4-devel openldap-devel krb5-devel xz-devel e2fsprogs-devel expat-devel devtoolset-8-gcc devtoolset-8-gcc-c++
    ```

3. Switch to the Percona Server for MongoDB branch that you are building
   and install Python3 modules

    ```{.bash code-prompt="$"}
    $ cd percona-server-mongodb && git checkout v5.0
    $ python3 -m pip install --user -r etc/pip/dev-requirements.txt
    ```

4. Define Percona Server for MongoDB version (5.0.2 for the time of
   writing this document)

    ```{.bash code-prompt="$"}
    $ echo '{"version": "5.0.2"}' > version.json
    ```

5. Build a specific ``curl`` version

    -  Fetch the package archive 

        ```{.bash code-prompt="$"}
        $ wget https://curl.se/download/curl-7.66.0.tar.gz
        ``` 

    -  Unzip the package 

        ```{.bash code-prompt="$"}
        $ tar -xvzf curl-7.66.0.tar.gz && cd curl-7.66.0
        ``` 

    -  Configure and build the package 

        ```{.bash code-prompt="$"}
        $ ./configure
        $ sudo make install
        ```

6. Build the AWS Software Development Kit for C++ library

    -  Create a directory to store the AWS library 

        ```{.bash code-prompt="$"}
        $ mkdir -p /tmp/lib/aws
        ``` 

    -  Declare an environment variable ``AWS_LIBS`` for this directory 

        ```{.bash code-prompt="$"}
        $ export AWS_LIBS=/tmp/lib/aws
        ``` 

    -  Percona Server for MongoDB is built with AWS SDK CPP 1.8.187
       version. Switch to this version 

        ```{.bash code-prompt="$"}
        $ cd aws-sdk-cpp && git checkout 1.8.187
        ``` 

    -  It is recommended to keep build files outside of the SDK
       directory. Create a build directory and navigate to it 

        ```{.bash code-prompt="$"}
        $ mkdir build && cd build
        ``` 

    -  Generate build files using ``cmake`` 

        === "On RedHat Enterprise Linux / CentOS 7" 

            ```{.bash code-prompt="$"}
            $ cmake3 .. -DCMAKE_C_COMPILER=/opt/rh/devtoolset-8/root/usr/bin/gcc  -DCMAKE_CXX_COMPILER=/opt/rh/devtoolset-8/root/usr/bin/g++ -DCMAKE_BUILD_TYPE=Release -DBUILD_ONLY="s3;transfer" -DBUILD_SHARED_LIBS=OFF -DMINIMIZE_SIZE=ON -DCMAKE_INSTALL_PREFIX="${AWS_LIBS}"
            ```  

        === "On RedHat Enterprise Linux / CentOS 8"  

            ```{.bash code-prompt="$"}
            $ cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_ONLY="s3;transfer" -DBUILD_SHARED_LIBS=OFF -DMINIMIZE_SIZE=ON -DCMAKE_INSTALL_PREFIX="${AWS_LIBS}"
            ``` 

    -  Install the SDK 

        ```{.bash code-prompt="$"}
        $ make install
        ```

7. Build Percona Server for MongoDB

    -  Change directory to ``percona-server-mongodb`` 

        ```{.bash code-prompt="$"}
        $ cd percona-server-mongodb
        ``` 

    -  Build Percona Server for MongoDB from ``buildscripts/scons.py``.
       
        === "On RedHat Enterprise Linux / CentOS 7" 

            ```{.bash code-prompt="$"}
            $ python3 buildscripts/scons.py CC=/opt/rh/devtoolset-8/root/usr/bin/gcc CXX=/opt/rh/devtoolset-8/root/usr/bin/g++ -j$(nproc --all) --jlink=2 --install-mode=legacy --disable-warnings-as-errors --ssl --opt=on --use-sasl-client --wiredtiger --audit --inmemory --hotbackup CPPPATH="${AWS_LIBS}/include" LIBPATH="${AWS_LIBS}/lib"  mongod
            ``` 

        === "On RedHat Enterprise Linux / CentOS 8" 

            ```{.bash code-prompt="$"}
            $ buildscripts/scons.py -j$(nproc --all) --jlink=2 --install-mode=legacy --disable-warnings-as-errors --ssl --opt=on --use-sasl-client --wiredtiger --audit --inmemory --hotbackup CPPPATH="${AWS_LIBS}/include" LIBPATH="${AWS_LIBS}/lib64" mongod
            ``` 

       This command builds only the database. Other available targets for the
       ``scons`` command are:        

       - ``mongod`` 
       - ``mongos`` 
       - ``mongo``  
       - ``core`` (includes ``mongod``, ``mongos``, ``mongo``) 
       - ``all``

The built binaries are in the ``percona-server-mongodb`` directory.
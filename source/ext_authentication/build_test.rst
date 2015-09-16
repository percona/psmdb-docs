.. _build-test:

====================
Building and Testing
====================

This guide describes how to build Percona Server for MongoDB and test external authentication on Ubuntu 14.x docker image or bare bones machine.

.. contents::
   :local:

Build and Test Requirements
===========================

* A bare bones Ubuntu 14.x or Debian 7.x installation
* Minimum 3 GB RAM
* Minimum 20 GB free space
* An internet connection to download tools and source code

Transparent Huge Pages
======================

Percona Server for MongoDB comes with the Percona Fractal Tree storage engine. This engine requires the transparent huge page feature of modern Linux kernels to be disabled. Before running the server with the Percona Fractal Tree, it is important to disable this feature on the machine. If you are building and testing under Docker, you will need to set these in the host machine's kernel before running the container.

.. code-block:: bash

  $ sudo /bin/bash -c 'echo never > /sys/kernel/mm/transparent_hugepage/enabled'
  $ sudo /bin/bash -c 'echo never > /sys/kernel/mm/transparent_hugepage/defrag'

Using Docker
============

Most default Docker installations do not provide enough free space to build and test external authentication. You may need to use the ``--volume`` option to map a host directory to the Docker container.

.. code-block:: bash

  $ mkdir $HOME/percona-server-mongodb
  $ docker run -ti --name='percona-server-mongodb' --volume=$HOME/percona-server-mongodb:/root docker.io/ubuntu:14.10 /bin/bash

Download the source
===================

Execute the following as root:

.. code-block:: bash

  $ apt-get update -y
  $ apt-get install -y git
  $ mkdir -p ~/git
  $ cd ~/git
  $ git clone https://github.com/Percona/percona-server-mongodb.git

Deploying OpenLDAP Server and Cyrus SASL
========================================

Execute the following as root:

.. code-block:: bash

  $ cd ~/git/percona-server-mongodb/support-files/ldap-sasl
  $ ./deploy_ldap_and_sasl.sh

After the script runs you should see ``0: OK "Success."`` reported at the end. To run a test of the OpenLDAP/Cyrus SASL installation you can run the ``check_saslauthd.sh`` script.

This will ensure all the proper LDAP authentication for all of the accounts used in the external authentication test suite.

Build
=====

The following script will install the tool chain, download all of the sources, compile and package the result into a tarball.

.. code-block:: bash

  $ cd ~/git/percona-server-mongodb/scripts
  $ ./build_ubuntu14.sh

.. note:: The script builds the binaries without debug symbols by default. You may edit the value at the top of :file:`scripts/build_ubuntu14.sh` to build the Debug version.

Install
=======

The packages will be built in the :file:`~/git/mongo` repository location.

Execute the following as root:

.. code-block:: bash

  $ cd ~
  $ tar xzvf ~/git/percona-server-mongodb/......tar.gz

Run Tests
=========

Once the executables have been compiled and installed, and OpenLDAP and Cyrus SASL are running, you can run the external authentication test suite:

.. code-block:: bash

  $ cd ~/git/percona-server-mongodb/jstests/external_auth
  $ export MONGODB_HOME=$HOME/tokumx-2.0.1-linux-x86_64
  $ ./run.sh

The output should resemble the following:

.. code-block:: none

 mongod startup (opts: )                                                   [OK]
 Database Setup Script                                                     [OK]
 mongod shutdown                                                           [OK]
 mongod startup (opts: --auth)                                             [OK]
 Add Local Users                                                           [OK]
 Add External Users                                                        [OK]
 Test invalid account names and passwords                                  [OK]
 External user with read (only) access to 'test'                           [OK]
 External user with readWrite access to 'test'                             [OK]
 Local user with read (only) access to 'test'                              [OK]
 Local user with readWrite access to 'test'                                [OK]
 External user with read (only) access to 'other'                          [OK]
 External user with readWrite access to 'other'                            [OK]
 Local user with read (only) access to 'other'                             [OK]
 Local user with readWrite access to 'other'                               [OK]
 External user with read (only) access to both 'test' and 'other'          [OK]
 External user with readWrite access to both 'test' and 'other'            [OK]
 External user with read (only) on 'test' and readWrite on 'other'         [OK]
 External user with readWrite on 'test' and read (only) on 'other'         [OK]
 mongod shutdown                                                           [OK]
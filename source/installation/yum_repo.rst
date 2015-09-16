.. _yum_repo:

===============================================================================
 Installing |Percona Server for MongoDB| on Red Hat Enterprise Linux and CentOS
===============================================================================

Ready-to-use packages are available from the |Percona| software repositories and the `download page <http://www.percona.com/downloads/Percona-Server-for-MongoDB/>`_. The |Percona| :program:`yum` repository supports popular *RPM*-based operating systems, including the *Amazon Linux AMI*.

The easiest way to install the *Percona Yum* repository is to install an *RPM* that configures :program:`yum` and installs the `Percona GPG key <https://www.percona.com/downloads/RPM-GPG-KEY-percona>`_.

Supported Releases:


 * *CentOS* 5 and *RHEL* 5

 * *CentOS* 6 and *RHEL* 6 (Current Stable) [#f1]_

 * *CentOS* 7 and *RHEL* 7

The *CentOS* repositories should work well with *Red Hat Enterprise Linux* too, provided that :program:`yum` is installed on the server.

Supported Platforms:

 * x86_64 (also known as ``amd64``)

What's in each RPM package?
===========================

Each of the |Percona Server for MongoDB| RPM packages have a particular purpose.

The ``Percona-Server-MongoDB`` meta package will install the ``mongo`` shell, import/export tools, other client utilities, server software, default configuration, and init.d scripts.

The ``Percona-Server-MongoDB-debuginfo`` package contains debug symbols and information for the server package. 

The ``Percona-Server-MongoDB-server`` package contains Percona Server for MongoDB server software, default configuration files and service management scripts.

The ``Percona-Server-MongoDB-shell`` package contains the Percona Server for MongoDB shell. 

The ``Percona-Server-MongoDB-mongos`` package contains ``mongos`` - the Percona Server for MongoDB sharded cluster query router.

The ``Percona-Server-MongoDB-tools`` package contains Mongo tools for high-performance MongoDB fork from Percona.

Installing |Percona Server for MongoDB| from Percona ``yum`` repository
=======================================================================

1. Install the Percona repository 
   
   You can install Percona yum repository by running the following command as a ``root`` user or with sudo:

   .. code-block:: bash

     yum install http://www.percona.com/downloads/percona-release/redhat/0.1-3/percona-release-0.1-3.noarch.rpm

   You should see some output such as the following: 

   .. code-block:: bash

     Retrieving http://www.percona.com/downloads/percona-release/redhat/0.1-3/percona-release-0.1-3.noarch.rpm
     Preparing...                ########################################### [100%]
        1:percona-release        ########################################### [100%]

.. note:: 

  *RHEL*/*Centos* 5 doesn't support installing the packages directly from the remote location so you'll need to download the package first and install it manually with :program:`rpm`:

    .. code-block:: bash

      wget http://www.percona.com/downloads/percona-release/redhat/0.1-3/percona-release-0.1-3.noarch.rpm
      rpm -ivH percona-release-0.1-3.noarch.rpm


2. Testing the repository
   
   Make sure packages are now available from the repository, by executing the following command: 

   .. code-block:: bash

     yum list | grep percona

   You should see output similar to the following:

   .. code-block:: bash

     ...
     Percona-Server-MongoDB.x86_64               3.0.5-rel0.7rc.el6           percona-release-x86_64
     Percona-Server-MongoDB-debuginfo.x86_64     3.0.5-rel0.7rc.el6           percona-release-x86_64
     Percona-Server-MongoDB-mongos.x86_64        3.0.5-rel0.7rc.el6           percona-release-x86_64
     Percona-Server-MongoDB-server.x86_64        3.0.5-rel0.7rc.el6           percona-release-x86_64
     Percona-Server-MongoDB-shell.x86_64         3.0.5-rel0.7rc.el6           percona-release-x86_64
     Percona-Server-MongoDB-tools.x86_64         3.0.5-rel0.7rc.el6           percona-release-x86_64
     ...

3. Install the packages

   You can now install |Percona Server| by running:

   .. code-block:: bash

     yum install Percona-Server-MongoDB

Percona `yum` Testing repository
--------------------------------

Percona offers pre-release builds from our testing repository. To subscribe to the testing repository, you'll need to enable the testing repository in :file:`/etc/yum.repos.d/percona-release.repo`. To do so, set both ``percona-testing-$basearch`` and ``percona-testing-noarch`` to ``enabled = 1`` (Note that there are 3 sections in this file: release, testing and experimental - in this case it is the second section that requires updating). **NOTE:** You'll need to install the Percona repository first (ref above) if this hasn't been done already.


Running |Percona Server| for MongoDB
====================================

|Percona Server| for MongoDB stores the data files in :file:`/var/lib/mongodb/` by default. You can find the configuration file that is used to manage |Percona Server| in :file:`/etc/mongod.cnf`. 

1. Starting the service

   |Percona Server| for MongoDB isn't started automatically on *RHEL* and *CentOS* after it gets installed. You should start it by running:

   .. code-block:: bash

     service mongod start

2. Confirming that service is running

   You can check the service status by running:

   .. code-block:: bash

     service mongod status

3. Stopping the service

   You can stop the service by running:

   .. code-block:: bash

     service mongod stop

4. Restarting the service

   You can restart the service by running:

   .. code-block:: bash

     service mongod restart

.. note::

  *RHEL* 7 and *CentOS* 7 come with `systemd <http://freedesktop.org/wiki/Software/systemd/>`_ as the default system and service manager so you can invoke all the above commands with ``sytemctl`` instead of ``service``. Currently both are supported.

Uninstalling |Percona Server| for MongoDB
=========================================

To completely uninstall |Percona Server| for MongoDB you'll need to remove all the installed packages and data files.

1.  Stop the |Percona Server| for MongDB service

    .. code-block:: bash

     service mongod stop

2. Remove the packages 

   .. code-block:: bash

    yum remove Percona-Server-MongoDB*

3. Remove the data and configuration files

   .. code-block:: bash

     rm -rf /var/lib/mongodb
     rm -f /etc/mongod.cnf

.. warning:: 

  This will remove all the packages and delete all the data files (databases, tables, logs, etc.), you might want to take a backup before doing this in case you need the data.

.. rubric:: Footnotes

.. [#f1] "Current Stable": We support only the current stable RHEL6/CentOS6 release, because there is no official (i.e. RedHat provided) method to support or download the latest OpenSSL on RHEL/CentOS versions prior to 6.5. Similarly, and also as a result thereof, there is no official Percona way to support the latest Percona Server builds on RHEL/CentOS versions prior to 6.5. Additionally, many users will need to upgrade to OpenSSL 1.0.1g or later (due to the `Heartbleed vulnerability <http://www.percona.com/resources/ceo-customer-advisory-heartbleed>`_), and this OpenSSL version is not available for download from any official RHEL/Centos repository for versions 6.4 and prior. For any officially unsupported system, src.rpm packages may be used to rebuild Percona Server for any environment. Please contact our `support service <http://www.percona.com/products/mysql-support>`_ if you require further information on this.

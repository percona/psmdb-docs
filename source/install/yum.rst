.. _yum:

============================================================================
Installing Percona Server for MongoDB on Red Hat Enterprise Linux and CentOS
============================================================================

.. note:: |PSMDB| should work on other RPM-based distributions
   (for example, Amazon Linux AMI and Oracle Linux),
   but it is tested only on platforms listed on the `Percona Software and Platform Lifecycle <https://www.percona.com/services/policies/percona-software-platform-lifecycle#mongodb>`_ page. [#f1]_.

.. contents::
   :local:

Package Contents
================

:``Percona-Server-MongoDB-36``:
 Installs the ``mongo`` shell, import/export tools, other client utilities,
 server software, default configuration, and init.d scripts.

:``Percona-Server-MongoDB-36-server``:
 Contains the ``mongod`` server, default configuration files,
 and init.d scripts.

:``Percona-Server-MongoDB-36-shell``:
 Contains the ``mongo`` shell.

:``Percona-Server-MongoDB-36-mongos``:
 Contains the ``mongos`` sharded cluster query router.

:``Percona-Server-MongoDB-36-tools``:
 Contains Mongo tools for high-performance MongoDB fork from Percona.

:``Percona-Server-MongoDB-36-debuginfo``:
 Contains debug symbols for the server.

Installing from Percona Repositories
====================================

It is recommended to install |PSMDB| from official Percona repositories

Configure Percona repositories as described in `Percona Software Repositories Documentation <https://www.percona.com/doc/percona-repo-config/index.html>`_.

Install the latest version
---------------------------------------------

Starting from |PSMDB| 3.6.19-7.0, the packages are located in the ``psmdb-36`` repository. To install the latest version of |PSMDB|, do the following:

1. Enable the repository.
   
   .. code-block:: bash
   
      $ sudo percona-release enable psmdb-36 

#. Install the required |PSMDB| package using :command:`yum`.
   For example, to install the full package, run the following:

   .. code-block:: bash

      $ sudo yum install Percona-Server-MongoDB-36

Install a specific version
-----------------------------------------------------

Earlier versions of |PSMDB| are located in the ``original`` repository. To install a specific version:

1. Enable the `original` repository: 

   .. code-block:: bash
   
      $ sudo percona-release enable original

#. List available packages: 
   
   .. code-block:: bash
   
      $ sudo yum list Percona-Server-MongoDB-36 --showduplicates

   .. admonition:: Sample output 
   
      .. include:: ../.res/yum-repo-list.txt    

#. Install a specific version packages. For example, to install |PSMDB| 3.6.17-4.0, use the following command: 

   .. code-block:: bash
   
      $ sudo yum install Percona-Server-MongoDB-36-3.6.17-4.0.el8
   
Using Percona Server for MongoDB
================================

.. warning:: If you have SELinux security module installed,
   it will conflict with Percona Server for MongoDB.
   There are several options to deal with this:

   * Remove the SELinux packages.
     This is not recommended, because it may violate security.

   * Disable SELinux by setting ``SELINUX``
     in :file:`/etc/selinux/config` to ``disabled``.
     This change takes effect after you reboot.

   * Run SELinux in permissive mode by setting ``SELINUX``
     in :file:`/etc/selinux/config` to ``permissive``.
     This change takes effect after you reboot.

     You can also enforce permissive mode at runtime
     using the ``setenforce 0`` command.
     However, this will not affect the configuration after a reboot.

|PSMDB| stores data files in :file:`/var/lib/mongodb/` by default.
The configuration file is :file:`/etc/mongod.conf`.

* **Starting the service**

  |PSMDB| is not started automatically after installation.
  Start it manually using the following command:

  .. code-block:: bash

     $ sudo systemctl start mongod

* **Confirming that service is running**

  Check the service status using the following command:

  .. code-block:: bash

     $ sudo systemctl status mongod

* **Stopping the service**

  Stop the service using the following command:

  .. code-block:: bash

     $ sudo systemctl stop mongod

* **Restarting the service**

  Restart the service using the following command:

  .. code-block:: bash

     $ sudo systemctl restart mongod 

Running after reboot
--------------------

The ``mongod`` service is not automatically started
after you reboot the system.

For RHEL or CentOS versions 5 and 6, you can use the ``chkconfig`` utility
to enable auto-start as follows:

.. code-block:: bash

   $ chkconfig --add mongod

For RHEL or CentOS version 7, you can use the ``systemctl`` utility as follows:

.. code-block:: bash

   $ systemctl enable mongod

Uninstalling Percona Server for MongoDB
=======================================

To completely uninstall Percona Server for MongoDB
you'll need to remove all the installed packages and data files:

1. Stop the Percona Server for MongoDB service:

   .. code-block:: bash

      $ sudo systemctl stop mongod

#. Remove the packages:

   .. code-block:: bash

      $ sudo yum remove Percona-Server-MongoDB*

#. Remove the data and configuration files:

   .. code-block:: bash

      $ rm -rf /var/lib/mongodb
      $ rm -f /etc/mongod.cnf

.. warning:: This will remove all the packages
   and delete all the data files (databases, tables, logs, etc.).
   You might want to back up your data before doing this
   in case you need the data later.

.. rubric:: Footnotes

.. [#f1] We support only the current stable RHEL 6 and CentOS 6 releases,
   because there is no official (i.e. RedHat provided) method to support
   or download the latest OpenSSL on RHEL and CentOS versions prior to 6.5.
   Similarly, and also as a result thereof,
   there is no official Percona way to support the latest Percona Server builds
   on RHEL and CentOS versions prior to 6.5.
   Additionally, many users will need to upgrade to OpenSSL 1.0.1g or later
   (due to the `Heartbleed vulnerability
   <http://www.percona.com/resources/ceo-customer-advisory-heartbleed>`_),
   and this OpenSSL version is not available for download
   from any official RHEL and CentOS repositories for versions 6.4 and prior.
   For any officially unsupported system, :file:`src.rpm` packages can be used
   to rebuild Percona Server for any environment.
   Please contact our `support service
   <http://www.percona.com/products/mysql-support>`_
   if you require further information on this.


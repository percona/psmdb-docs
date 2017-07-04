.. _yum:

============================================================================
Installing Percona Server for MongoDB on Red Hat Enterprise Linux and CentOS
============================================================================

Percona provides :file:`.rpm` packages for 64-bit versions
of the following distributions:

* Red Hat Enterprise Linux / CentOS 5
* Red Hat Enterprise Linux / CentOS 6 [#f1]_
* Red Hat Enterprise Linux / CentOS 7

.. note:: |PSMDB| should work on other RPM-based distributions
   (for example, Amazon Linux AMI and Oracle Linux),
   but it is tested only on platforms listed above.

.. contents::
   :local:

Package Contents
================

:``Percona-Server-MongoDB``:
 Installs the ``mongo`` shell, import/export tools, other client utilities,
 server software, default configuration, and init.d scripts.

:``Percona-Server-MongoDB-server``:
 Contains the ``mongod`` server, default configuration files,
 and init.d scripts.

:``Percona-Server-MongoDB-shell``:
 Contains the ``mongo`` shell.

:``Percona-Server-MongoDB-mongos``:
 Contains the ``mongos`` sharded cluster query router.

:``Percona-Server-MongoDB-tools``:
 Contains Mongo tools for high-performance MongoDB fork from Percona.

:``Percona-Server-MongoDB-debuginfo``:
 Contains debug symbols for the server.

Installing from Percona Repository
==================================

It is recommended to intall |PSMDB| from official Percona repositories:

1. Configure Percona repositories as described in
   `Percona Software Repositories Documentation
   <https://www.percona.com/doc/percona-repo-config/index.html>`_.

#. Install the required |PSMDB| package using :command:`yum`.
   For example, to install the full package, run the following:

   .. code-block:: bash

      $ sudo yum install Percona-Server-MongoDB

Using Percona Server for MongoDB
================================

.. warning:: If you have SELinux security module installed,
   it will conflict with Percona Server for MongoDB.
   There are several options to deal with this:

   * Remove the SELinux packages or not install them at all.
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
It runs as a service named ``mongod``.

* **Starting the service**

  |PSMDB| is not started automatically after installation.
  Start it manually using the following command:

  .. code-block:: bash

     $ sudo service mongod start

* **Confirming that service is running**

  Check the service status using the following command:

  .. code-block:: bash

     $ sudo service mongod status

* **Stopping the service**

  Stop the service using the following command:

  .. code-block:: bash

     $ sudo service mongod stop

* **Restarting the service**

  Restart the service using the following command:

  .. code-block:: bash

     $ sudo service mongod restart

.. note:: On Red Hat Enterprise Linux and CentOS 7
   you can also invoke all the above commands with ``sytemctl``
   instead of ``service``.

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

      $ sudo service mongod stop

2. Remove the packages:

   .. code-block:: bash

      $ sudo yum remove Percona-Server-MongoDB*

3. Remove the data and configuration files:

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


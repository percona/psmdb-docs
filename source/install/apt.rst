.. _apt:

==========================================================
Installing Percona Server for MongoDB on Debian and Ubuntu
==========================================================

Percona provides :file:`.deb` packages for 64-bit versions
of the following distributions:

* Debian 8 ("jessie")
* Debian 9 ("stretch")
* Ubuntu 14.04 LTS (Trusty Tahr)
* Ubuntu 16.04 LTS (Xenial Xerus)
* Ubuntu 16.10 (Yakkety Yak)
* Ubuntu 17.04 (Zesty Zapus)
* Ubuntu 17.10 (Artful Aardvark)
* Ubuntu 18.04 LTS (Bionic Beaver)

.. note:: |PSMDB| should work on other DEB-based distributions,
   but it is tested only on platforms listed above.

.. contents::
   :local:

Package Contents
================

:``percona-server-mongodb-36``:
 Installs the ``mongo`` shell, import/export tools, other client utilities,
 server software, default configuration, and init.d scripts.

:``percona-server-mongodb-36-server``:
 Contains the ``mongod`` server, default configuration files,
 and init.d scripts.

:``percona-server-mongodb-36-shell``:
 Contains the ``mongo`` shell.

:``percona-server-mongodb-36-mongos``:
 Contains the ``mongos`` sharded cluster query router.

:``percona-server-mongodb-36-tools``:
 Contains Mongo tools for high-performance MongoDB fork from Percona.

:``percona-server-mongodb-36-dbg``:
 Contains debug symbols for the server.

Installing from Percona Repositories
====================================

It is recommended to install |PSMDB| from official Percona repositories:

1. Configure Percona repositories as described in
   `Percona Software Repositories Documentation
   <https://www.percona.com/doc/percona-repo-config/index.html>`_.

#. Install the required |PSMDB| package using :command:`apt-get`.
   For example, to install the full package, run the following:

   .. code-block:: bash

      $ sudo apt-get install percona-server-mongodb-34

Using Percona Server for MongoDB
================================

By default, |PSMDB| stores data files in :file:`/var/lib/mongodb/`
and configuration parameters in :file:`/etc/mongod.conf`.

* **Starting the service**

  |PSMDB| is started automatically after installation
  unless it encounters errors during the installation process.
  You can also manually start it using the following command:

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

.. note:: On Debian 8, Ubuntu 16.04 and later versions
   you can also invoke all the above commands with ``sytemctl``
   instead of ``service``.

Uninstalling Percona Server for MongoDB
=======================================

To uninstall |PSMDB|, remove all the installed packages.
Removing packages with :command:`apt-get remove`
will leave the configuration and data files.
Removing the packages with :command:`apt-get purge`
will remove all the packages with configuration files and data.
Depending on your needs you can choose which command better suits you.

1. Stop the server:

   .. code-block:: bash

      $ sudo service mongod stop

#. Remove the packages.

   * If you want to leave configuration and data files:

     .. code-block:: bash

        $ sudo apt-get remove percona-server-mongodb*

   * If you want to delete configuration and data files
     as well as the packages:

     .. code-block:: bash

        $ sudo apt-get purge percona-server-mongodb*


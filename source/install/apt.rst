.. _apt:

==========================================================
Installing Percona Server for MongoDB on Debian and Ubuntu
==========================================================

.. note:: |PSMDB| should work on other DEB-based distributions,
   but it is tested only on platforms listed above on the `Percona Software and Platform Lifecycle <https://www.percona.com/services/policies/percona-software-platform-lifecycle#mongodb>`_ page.

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

It is recommended to install |PSMDB| from official Percona repositories.  

Configure Percona repositories as described in `Percona Software Repositories Documentation <https://www.percona.com/doc/percona-repo-config/index.html>`_.

Install the latest version
---------------------------------------------

Starting from |PSMDB| 3.6.19-7.0, the packages are located in the ``psmdb-36`` repository. To install the latest version of |PSMDB|, do the following:

1. Enable the repository.
   
   .. code-block:: bash
   
      $ sudo percona-release enable psmdb-36 

#. Install the required |PSMDB| package using :command:`apt-get`.
   For example, to install the full package, run the following:

   .. code-block:: bash

      $ sudo apt-get install percona-server-mongodb-36

Install a specific version
---------------------------------------------

|PSMDB| versions earlier than 3.6.19-7.0 are available for download on the `Percona website <https://www.percona.com/downloads/percona-server-mongodb-3.6/>`_.

1.  Select the desired version and your operating system from the drop-down menus. 
#.  Download the package bundle. The permalink for download is generated for  you based on your selections in the format ``https://www.percona.com/downloads/percona-server-mongodb-3.6/<release_version>/binary/<OS>/<OS_version>/x86_64/<package_name>``. 

    For example, to download |PSMDB| 3.6.14-3.4 for Debian Buster, use the following URL:

    .. code-block:: bash
    
       $ wget https://www.percona.com/downloads/percona-server-mongodb-3.6/percona-server-mongodb-3.6.14-3.4/binary/debian/buster/x86_64/percona-server-mongodb-3.6.14-3.4-r0985495-buster-x86_64-bundle.tar

#. Unpack the archive


   .. code-block:: bash
   
      $ tar xfv percona-server-mongodb-3.6.14-3.4-r0985495-buster-x86_64-bundle.tar

#. Install the packages
   
   .. code-block:: bash
   
      $ sudo dpkg -i percona-server-mongodb-36_3.6.14-3.4.buster_amd64.deb \
        percona-server-mongodb-36-dbg_3.6.14-3.4.buster_amd64.deb \
        percona-server-mongodb-36-mongos_3.6.14-3.4.buster_amd64.deb \
        percona-server-mongodb-36-server_3.6.14-3.4.buster_amd64.deb \
        percona-server-mongodb-36-shell_3.6.14-3.4.buster_amd64.deb \
        percona-server-mongodb-36-tools_3.6.14-3.4.buster_amd64.deb

   .. note::

      If ``dpkg`` fails at this step due to missing dependencies, run ``apt`` as follows:

      .. code-block:: bash

         $ sudo apt-get install --fix-broken

Using Percona Server for MongoDB
================================

By default, |PSMDB| stores data files in :file:`/var/lib/mongodb/`
and configuration parameters in :file:`/etc/mongod.conf`.

* **Starting the service**

  |PSMDB| is started automatically after installation
  unless it encounters errors during the installation process.
  You can also manually start it using the following command:

  .. code-block:: bash

     $ sudo systemctl start mongod

* **Confirming that the service is running**

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

      $ sudo systemctl stop mongod

#. Remove the packages.

   * If you want to leave configuration and data files:

     .. code-block:: bash

        $ sudo apt-get remove percona-server-mongodb*

   * If you want to delete configuration and data files
     as well as the packages:

     .. code-block:: bash

        $ sudo apt-get purge percona-server-mongodb*


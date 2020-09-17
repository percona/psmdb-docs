.. _apt:

==========================================================
Installing Percona Server for MongoDB on Debian and Ubuntu
==========================================================


.. note:: |PSMDB| should work on other DEB-based distributions,
   but it is tested only on platforms listed on the `Percona Software and Platform Lifecycle <https://www.percona.com/services/policies/percona-software-platform-lifecycle#mongodb>`_ page.

.. contents::
   :local:

Package Contents
================================================================================

.. list-table::
   :widths: 25 75

   * - Package
     - Contains
   * - percona-server-mongodb
     - The ``mongo`` shell, import/export tools, other client
       utilities, server software, default configuration, and init.d scripts.
   * - percona-server-mongodb-server
     - The :program:`mongod` server, default configuration files, and :dir:`init.d`
       scripts
   * - percona-server-mongodb-shell
     - The ``mongo`` shell
   * - percona-server-mongodb-mongos
     - The ``mongos`` sharded cluster query router
   * - percona-server-mongodb-tools
     - Mongo tools for high-performance MongoDB fork from Percona
   * - percona-server-mongodb-dbg
     - Debug symbols for the server

Installing from Percona Repositories
================================================================================

It is recommended to install |PSMDB| from official Percona repositories using
the |percona-release| utility:

|tip.run-all.root|

1. Fetch the repository packages from Percona web:

   .. code-block:: bash

      $ wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb

#. Install the downloaded package with :program:`dpkg`:

   .. code-block:: bash

      $ dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb

   Once you install this package the |Percona| repositories should be added. You
   can check the repository setup in the
   :file:`/etc/apt/sources.list.d/percona-release.list` file.

#. Enable the repository: :bash:`percona-release enable psmdb-42 release`
#. Remember to update the local cache: |apt.update|
   
Install the latest version 
--------------------------------------------------------------

Run the following command to install the latest version of |PSMDB|: 

.. code-block:: bash

   $ sudo apt-get install percona-server-mongodb

Install a specific version
--------------------------------------------------------------

1. List available versions:
 
   .. code-block:: bash
   
      $ sudo apt-cache madison percona-server-mongodb

   .. admonition:: Sample Output

      .. include:: ../.res/text/apt-versions-list.txt

2. Install a specific version packages. You must specify each package with the version number. For example, to install |PSMDB| 4.2.5-5, run the following command:
   
   .. code-block:: bash
   
      $ sudo apt-get install percona-server-mongodb=4.2.5-5.buster percona-server-mongodb-mongos=4.2.5-5.buster percona-server-mongodb-shell=4.2.5-5.buster percona-server-mongodb-server=4.2.5-5.buster percona-server-mongodb-tools=4.2.5-5.buster

Using Percona Server for MongoDB
================================================================================

By default, |PSMDB| stores data files in :file:`/var/lib/mongodb/`
and configuration parameters in :file:`/etc/mongod.conf`.

|tip.run-all.root|

Starting the service
  |PSMDB| is started automatically after installation
  unless it encounters errors during the installation process.
  You can also manually start it using the following command:
  |service.mongod.start|

Confirming that service is running**
  Check the service status using the following command:
  |service.mongod.status|

Stopping the service
  Stop the service using the following command: |service.mongod.stop|

Restarting the service
  Restart the service using the following command: |service.mongod.restart|

.. note::

   On Debian 8, Ubuntu 16.04 and later versions you can also invoke all the
   above commands with ``systemctl`` instead of ``service``.

Uninstalling Percona Server for MongoDB
================================================================================

To uninstall |PSMDB|, remove all the installed packages. Removing packages with
|apt.remove| will leave the configuration and data files. Removing the packages
with |apt.purge| will remove all the packages with configuration files and data.
Depending on your needs you can choose which command better suits you.

|tip.run-all.root|

1. Stop the |mongod| server: |service.mongod.stop|
#. Remove the packages. There are two options. To keep the configuration and
   data files, run |apt.remove.percona-server-mongodb|. If you want to delete
   the configuration and data files as well as the packages, use |apt.purge|:
   |apt.purge.percona-server-mongodb|

.. include:: ../.res/replace.txt
.. include:: ../.res/replace.program.txt

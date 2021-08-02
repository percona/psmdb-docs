.. _apt:

==========================================================
Installing Percona Server for MongoDB on Debian and Ubuntu
==========================================================

Use this document to install |PSMDB| from Percona repositories on DEB-based distributions such as Debian and Ubuntu.

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
       utilities, server software, default configuration, and :dir:`init.d` scripts.
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

Installing from Percona repositories
================================================================================

It is recommended to install |PSMDB| from official Percona repositories using
the |percona-release| utility.

Configure Percona repository
----------------------------

|tip.run-all.root|

1. Fetch |percona-release| packages from Percona web:

   .. code-block:: bash

      $ wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb

#. Install the downloaded package with :program:`dpkg`:

   .. code-block:: bash

      $ dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb

   Once you install ``percona-release``, the |Percona| repositories should be available. You
   can check the repository setup in the
   :file:`/etc/apt/sources.list.d/percona-release.list` file.

#. Enable the repository: :bash:`percona-release enable psmdb-50 release`
#. Remember to update the local cache: |apt.update|
   
Install the latest version 
--------------------------------------------------------------

Run the following command to install the latest version of |PSMDB|: 

.. code-block:: bash

   $ sudo apt-get install percona-server-mongodb

Install a specific version
--------------------------------------------------------------

To install a specific version of |PSMDB|, do the following:

1. List available versions:
 
   .. code-block:: bash
   
      $ sudo apt-cache madison percona-server-mongodb

   .. admonition:: Sample Output

      .. include:: ../.res/text/apt-versions-list.txt

2. Install a specific version packages. You must specify each package with the version number. For example, to install |PSMDB| 5.0.1-1, run the following command:
   
   .. code-block:: bash
   
      $ sudo apt-get install percona-server-mongodb=5.0.1-1.buster percona-server-mongodb-mongos=5.0.1-1.buster percona-server-mongodb-shell=5.0.1-1.buster percona-server-mongodb-server=5.0.1-1.buster percona-server-mongodb-tools=5.0.1-1.buster

Running Percona Server for MongoDB
================================================================================

By default, |PSMDB| stores data files in :file:`/var/lib/mongodb/`
and configuration parameters in :file:`/etc/mongod.conf`.

|tip.run-all.root|

**Starting the service**

|PSMDB| is started automatically after installation unless it encounters errors during the installation process.

You can also manually start it using the following command:

.. code-block:: bash
  
   $ sudo systemctl start mongod

**Confirming that the service is running**

Check the service status using the following command:

.. code-block:: bash
  
   $ sudo systemctl status mongod

**Stopping the service**

Stop the service using the following command: 

.. code-block:: bash
  
   $ sudo systemctl stop mongod

**Restarting the service**

Restart the service using the following command: 

.. code-block:: bash
  
   $ sudo systemctl restart mongod

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

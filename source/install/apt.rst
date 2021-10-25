.. _apt:

==========================================================
Installing Percona Server for MongoDB on Debian and Ubuntu
==========================================================

Use this document to install |PSMDB| from Percona repositories on DEB-based distributions.

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

Installing from Percona repositories
================================================================================

It is recommended to install |PSMDB| from official Percona repositories using
the |percona-release| utility.

Configure Percona repository
-------------------------------------------------------------------

1. Fetch |percona-release| packages from Percona web:

   .. code-block:: bash

      $ wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb

#. Install the downloaded package with :program:`dpkg`:

   .. code-block:: bash

      $ sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb

   Once you install this package the |Percona| repositories should be added. You can check the repository setup in the
   :file:`/etc/apt/sources.list.d/percona-release.list` file.

#. Enable the repository: 
   
   .. code-block:: bash
   
      $ sudo percona-release enable psmdb-40 release

#. Remember to update the local cache: 
   
   .. code-block:: bash

      $ sudo apt update
   
Install the latest version 
--------------------------------------------------------------

Run the following command to install the latest version of |PSMDB|: 

.. code-block:: bash

   $ sudo apt install percona-server-mongodb

Install a specific version
--------------------------------------------------------------

To install a specific version of |PSMDB|, do the following:

1. List available versions:
 
   .. code-block:: bash
   
      $ sudo apt-cache madison percona-server-mongodb

   .. admonition:: Sample Output

     .. include:: ../.res/text/apt-versions-list.txt

2. Install a specific version packages. You must specify each package with the version number. For example, to install |PSMDB| 4.0.16-9, run the following command:
   
   .. code-block:: bash
   
      $ sudo apt install percona-server-mongodb=4.0.16-9.buster percona-server-mongodb-mongos=4.0.16-9.buster percona-server-mongodb-shell=4.0.16-9.buster percona-server-mongodb-server=4.0.16-9.buster percona-server-mongodb-tools=4.0.16-9.buster

Running Percona Server for MongoDB
================================================================================

By default, |PSMDB| stores data files in :file:`/var/lib/mongodb/`
and configuration parameters in :file:`/etc/mongod.conf`.

**Starting the service**

|PSMDB| is started automatically after installation
unless it encounters errors during the installation process.
You can also manually start it using the following command:

.. code-block:: bash
  
   $ sudo systemctl start mongod

**Confirming that service is running**

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

.. include:: ../.res/replace.txt
.. include:: ../.res/replace.program.txt

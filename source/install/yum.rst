.. _yum:

=============================================================================================
Installing Percona Server for MongoDB on Red Hat Enterprise Linux and derivatives
=============================================================================================

Use this document to install |psmdb| on RPM-based distributions such as Red Hat Enterprise Linux and derivatives from Percona repositories. 

.. note:: |PSMDB| should work on other RPM-based distributions
   (for example, Amazon Linux AMI and Oracle Linux),
   but it is tested only on platforms listed on the `Percona Software and Platform Lifecycle <https://www.percona.com/services/policies/percona-software-platform-lifecycle#mongodb>`_ page. 

Package Contents
================================================================================

.. list-table::
   :widths: 25 75

   * - Package
     - Contains
   * - percona-server-mongodb
     - The ``mongosh`` shell, import/export tools, other client
       utilities, server software, default configuration, and :dir:`init.d` scripts.
   * - percona-server-mongodb-server
     - The :program:`mongod` server, default configuration files, and :dir:`init.d` scripts
   * - percona-server-mongodb-shell
     - The ``mongosh`` shell
   * - percona-server-mongodb-mongos
     - The ``mongos`` sharded cluster query router
   * - percona-server-mongodb-tools
     - Mongo tools for high-performance MongoDB fork from Percona
   * - percona-server-mongodb-debugsource
     - Debug sources for the server

Installing from Percona repositories
================================================================================

Percona repositories are managed using the |percona-release| tool. So in order to install |PSMDB|, install |percona-release| first.

Configure Percona repository
----------------------------
                                          
1. Install |percona-release|:

   .. code-block:: bash

      $ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm

   .. admonition:: Example of output

      .. code-block:: bash

	 Retrieving https://repo.percona.com/yum/percona-release-latest.noarch.rpm
	 Preparing...                ########################################### [100%]
         1:percona-release        ########################################### [100%]

#. Enable the repository: 

   .. code-block:: bash

      $ sudo percona-release enable psmdb-60 release


.. seealso::

   More information about how to use the ``percona-release`` tool
      https://www.percona.com/doc/percona-repo-config/index.html


Install the latest version
-------------------------------------------------------------------

To install the latest version of |PSMDB|, use the following command:

.. code-block:: bash

    $ sudo yum install percona-server-mongodb

Install a specific version 
-------------------------------------------------------------------

To install a specific version of |PSMDB|, do the following:

1. List available versions:
   
   .. code-block:: bash 
   
      $ sudo yum list percona-server-mongodb --showduplicates

   .. admonition:: Sample Output   

      .. code-block:: text

             Available Packages
         percona-server-mongodb.x86_64    6.0.2-1.el8       psmdb-60-release-x86_64



#. Install a specific version packages. For example, to install |PSMDB| 6.0.1-1, run the following command:
   
   .. code-block:: bash 
   
      $ sudo yum install percona-server-mongodb-6.0.2-1.el8
      
Running Percona Server for MongoDB
================================================================================

.. note::  

   If you are using SELinux in enforcing mode, you must customize your SELinux user policies to allow access to certain ``/sys`` and ``/proc`` files for OS-level statistics. Also, you must customize directory and port access policies if you are using non-default locations.

   Please refer to `Configure SELinux <https://docs.mongodb.com/v5.0/tutorial/install-mongodb-on-red-hat/#configure-selinux>`_ section of MongoDB Documentation for policy configuration guidelines. 

|PSMDB| stores data files in :dir:`/var/lib/mongodb/` by default.
The configuration file is :file:`/etc/mongod.conf`.

**Starting the service**

|PSMDB| is not started automatically after installation. Start it manually using the following command: 

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

Running after reboot
--------------------------------------------------------------------------------

The ``mongod`` service is not automatically started
after you reboot the system. To make it start automatically after reboot, enable it using the ``systemctl`` utility: 

.. code-block:: bash

   $ sudo systemctl enable mongod

Then start the ``mongod`` service

.. code-block:: bash
  
   $ sudo systemctl start mongod

.. include:: ../.res/replace.txt
.. include:: ../.res/replace.program.txt

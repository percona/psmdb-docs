.. _yum:

============================================================================
Installing Percona Server for MongoDB on Red Hat Enterprise Linux and CentOS
============================================================================

Use this document to install |psmdb| on RPM-based distributions from Percona repositories. 

.. note:: |PSMDB| should work on other RPM-based distributions
   (for example, Amazon Linux AMI and Oracle Linux),
   but it is tested only on platforms listed on the `Percona Software and Platform Lifecycle <https://www.percona.com/services/policies/percona-software-platform-lifecycle#mongodb>`_ page. [#f1]_

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

The preferable way to install |PSMDB| is from Percona repositories. Percona repositories are managed using the |percona-release| tool. 

Configure Percona repository
----------------------------

                                                      
1. Install |percona-release|:

   .. code-block:: bash

      $ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm

   .. admonition:: Example of Output

      .. code-block:: bash

	 Retrieving https://repo.percona.com/yum/percona-release-latest.noarch.rpm
	 Preparing...                ########################################### [100%]
         1:percona-release        ########################################### [100%]

#. Enable the repository: :bash:`percona-release enable psmdb-44 release`


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

      .. include:: ../.res/text/yum-versions-list.txt

#. Install a specific version packages. For example, to install |PSMDB| 4.4.0-1, run the following command:
   
   .. code-block:: bash 
   
      $ sudo yum install percona-server-mongodb-4.4.0-1.el8
      
Running Percona Server for MongoDB
================================================================================

.. note:: 

   If you are using SELinux in enforcing mode, you must customize your SELinux user policies to allow access to certain ``/sys`` and ``/proc`` files for OS-level statistics. Also, you must customize directory and port access policies if you are using non-default locations.

   Please refer to `Configure SELinux <https://docs.mongodb.com/v4.4/tutorial/install-mongodb-on-red-hat/#configure-selinux>`_ section of MongoDB Documentation for policy configuration guidelines. 


|PSMDB| stores data files in :dir:`/var/lib/mongodb/` by default.
The configuration file is :file:`/etc/mongod.conf`.

**Starting the service**

|PSMDB| is not started automatically after installation. Start it manually using the following command: 

.. code-block:: bash
  
   $ sudo systemctl start mongod

**Confirming that service is running**

Check the service status using the following command: |service.mongod.status|

.. code-block:: bash
  
   $ sudo systemctl status mongod

**Stopping the service**

Stop the service using the following command: |service.mongod.stop|

.. code-block:: bash
  
   $ sudo systemctl stop mongod

**Restarting the service**

Restart the service using the following command: |service.mongod.restart|

.. code-block:: bash
  
   $ sudo systemctl restart mongod

Running after reboot
--------------------------------------------------------------------------------

The ``mongod`` service is not automatically started
after you reboot the system.

For RHEL or CentOS versions 5 and 6, you can use the ``chkconfig`` utility
to enable auto-start as follows:

.. code-block:: bash

   $ sudo chkconfig --add mongod

For RHEL or CentOS version 7, you can use the ``systemctl`` utility: 

.. code-block:: bash

   $ sudo systemctl enable mongod

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


.. include:: ../.res/replace.txt
.. include:: ../.res/replace.program.txt

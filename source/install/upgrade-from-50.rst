.. _upgrade_from_50:

Upgrading from |PSMDB| |prev-version| to |version|
================================================================================

To upgrade |PSMDB| to version |version|, you must be running version
|prev-version|. Upgrades from earlier versions are not supported.

Before upgrading your production |PSMDB| deployments, test all your applications
in a testing environment to make sure they are compatible with the new version.
For more information, see `Compatibility Changes in MongoDB 6.0 <https://www.mongodb.com/docs/v6.0/release-notes/6.0-compatibility/>`_
       
The general procedure for performing an in-place upgrade (where your existing
data and configuration files are preserved) includes the following steps:

1. Stop the ``mongod`` instance
#. Enable |percona| repository for |PSMDB| |version|
#. Install new packages. Old packages are considered obsolete and automatically removed
#. Start the ``mongod`` instance

Similar to :ref:`installing Percona Server for MongoDB <install>` , we recommend upgrading it from official Percona repositories using the ``percona-release`` tool. `Install percona-release <https://docs.percona.com/percona-software-repositories/installing.html>`_ or `update <https://docs.percona.com/percona-software-repositories/updating.html>`_ it to the latest version.

.. warning::

   Perform a full backup of your data and configuration files before upgrading.

.. tabs::

   .. tab:: Upgrading on Debian or Ubuntu

      1. Stop the ``mongod`` instance: 

         .. code-block:: bash

            $ sudo systemctl stop mongod

      #. Enable |percona| repository for |PSMDB| |version|: 

         .. code-block:: bash

            $ sudo percona-release enable psmdb-60

      #. Update the local cache: 
         
         .. code-block:: bash

            $ sudo apt update

      #. Install |PSMDB| |version| packages: 

         .. code-block:: bash

            $ sudo apt install percona-server-mongodb

      #. Start the ``mongod`` instance: 

         .. code-block:: bash

            $ sudo systemctl start mongod

      For more information, see :ref:`apt`.

   .. tab:: Upgrading on RHEL and CentOS

      
      1. Stop the ``mongod`` instance: 

         .. code-block:: bash

            $ sudo systemctl stop mongod

      #. Enable |percona| repository for |PSMDB| |version|: 

         .. code-block:: bash

            $ sudo percona-release enable psmdb-60

      #. Install |PSMDB| |version| packages: 
          
         .. code-block::bash

            $ sudo yum install percona-server-mongodb

      #. Start the ``mongod`` instance: 

         .. code-block:: bash

            $ sudo systemctl start mongod

      For more information, see :ref:`yum`.

.. include:: ../.res/text/enable_features.txt   


.. include:: ../.res/replace.txt
.. include:: ../.res/replace.program.txt

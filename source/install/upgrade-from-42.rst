.. _upgrade_from_42:

Upgrading from |PSMDB| |prev-version| to |version|
================================================================================

To upgrade |PSMDB| to version |version|, you must be running version
|prev-version|. Upgrades from earlier versions are not supported.

Before upgrading your production |PSMDB| deployments, test all your applications
in a testing environment to make sure they are compatible with the new version.
For more information, see `Compatibility Changes in MongoDB 4.4 <https://docs.mongodb.com/manual/release-notes/4.4-compatibility/>`_
       
The general procedure for performing an in-place upgrade (where your existing
data and configuration files are preserved) includes the following steps:

1. Stop the ``mongod`` instance
#. Enable |percona| repository for |PSMDB| |version|
#. Install new packages. Old packages are considered obsolete and automatically removed
#. Start the ``mongod`` instance

It is recommended to upgrade |PSMDB| from official |percona| repositories using
the corresponding package manager for your system.  For more information, see
:ref:`install`.

.. warning::

   Perform a full backup of your data and configuration files before upgrading.

.. tabs::

   .. tab:: Upgrading on Debian or Ubuntu

      1. Stop the ``mongod`` instance: 

         .. code-block:: bash

            $ sudo systemctl stop mongod

      #. Enable |percona| repository for |PSMDB| |version|: 

         .. code-block:: bash

            $ sudo percona-release enable psmdb-44

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

            $ sudo percona-release enable psmdb-44

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

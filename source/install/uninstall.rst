.. _uninstall:

Uninstalling |PSMDB|
********************

To completely remove |PSMDB| you need to remove all the installed packages, data and configuration files. If you need the data, consider making a backup before uninstalling Percona Server for MongoDB.

Follow the instructions, relevant to your operating system:

.. _apt-uninstall:

.. tabs:: 

   .. tab:: Uninstall on Debian and Ubuntu

      You can remove |PSMDB| packages with one of the following commands:

      * |apt.remove| will only remove the packages and leave the configuration and data files. 
      * |apt.purge| will remove all the packages with configuration files and data.

      Choose which command better suits you depending on your needs.

      1. Stop the |mongod| server: 
         
         .. code-block:: bash 

            $ sudo systemctl stop mongod

      #. Remove the packages. There are two options. 
         
         * To keep the configuration and data files, run:

           .. code-block:: bash

              $ sudo apt remove percona-server-mongodb* 

         * To delete both the configuration and data files and the packages, run:
            
           .. code-block:: bash

              $ sudo apt purge percona-server-mongodb*


   .. tab:: Uninstall on RHEL and CentOS

      
      1. Stop the Percona Server for MongoDB service: 

         .. code-block:: bash

            $ sudo systemctl stop mongod

      #. Remove the packages: 
         
         .. code-block:: bash
         
            $ sudo yum remove percona-server-mongodb* 

      #. Remove the data and configuration files:

         .. code-block:: bash

            $ sudo rm -rf /var/lib/mongodb
            $ sudo rm -f /etc/mongod.conf

      .. warning::

         This will remove all the packages and delete all the data files (databases, tables, logs, etc.).  You might want to back up your data before doing this in case you need the data later.

.. include:: ../.res/replace.txt
.. include:: ../.res/replace.program.txt
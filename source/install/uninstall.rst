.. _uninstall:

Uninstalling |PSMDB|
********************

To completely remove |PSMDB| you need to remove all the installed packages, data and configuration files. If you need the data, consider making a backup before uninstalling Percona Server for MongoDB.

Follow the instructions, relevant to your operating system:

* :ref:`Uninstall on Debian and Ubuntu <apt-uninstall>`
* :ref:`Uninstall on Red Hat Enterprise Linux and CentOS <yum-uninstall>`

.. _apt-uninstall:

Uninstall on Debian and Ubuntu
==============================

You can remove |PSMDB| packages with one of the following commands:

* |apt.remove| will only remove the packages and leave the configuration and data files. 
* |apt.purge| will remove all the packages with configuration files and data.

Choose which command better suits you depending on your needs.

|tip.run-all.root|

1. Stop the |mongod| server: |service.mongod.stop|
#. Remove the packages. There are two options. To keep the configuration and
   data files, run |apt.remove.percona-server-mongodb|. If you want to delete
   the configuration and data files as well as the packages, run
   |apt.purge.percona-server-mongodb|

.. _yum-uninstall:

Uninstall on Red Hat Enterprise Linux and CentOS
============================================================

|tip.run-all.root|

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

   This will remove all the packages and delete all the data files (databases,
   tables, logs, etc.).  You might want to back up your data before doing this
   in case you need the data later.

.. include:: ../.res/replace.txt
.. include:: ../.res/replace.program.txt
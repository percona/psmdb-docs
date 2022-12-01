.. _upgrade_from_34:

=================================
Upgrading from |PSMDB| 3.4 to 3.6
=================================

.. important:: **MongoRocks is deprecated in Percona Server for MongoDB 3.6.**
   If you are using |PSMDB| 3.4 with MongoRocks, and you wish to upgrade to
   version 3.6, please read the note at the top of the MongoRocks page before
   upgrading:
   https://www.percona.com/doc/percona-server-for-mongodb/3.6/mongorocks.html

To upgrade |PSMDB| to version 3.6, you must be running version 3.4.
Upgrades from earlier versions are not supported.

Before upgrading your production |PSMDB| deployments,
test all your applications in a testing environment
to make sure they are compatible with the new version.

The general procedure for performing an in-place upgrade
(where your existing data and configuration files are preserved)
includes the following steps:

1. Stop the ``mongod`` instance.

#. Remove old packages.

#. Install new packages.

#. Start the ``mongod`` instance.

It is recommended to upgrade |PSMDB| from official Percona repositories
using the corresponding package manager for your system.
For more information, see :ref:`install`.

.. warning:: Perform a full backup of your data and configuration files
   before upgrading.

Upgrading on Debian or Ubuntu
=============================

1. Stop the ``mongod`` instance::

    sudo service mongod stop

#. Remove |PSMDB| 3.4 packages::

    sudo apt-get remove percona-server-mongodb-34*

#. Install |PSMDB| 3.6 packages::

    sudo apt-get install percona-server-mongodb-36

#. If you modified the configuration file and wish to use it with the new version, verify that the :file:`/etc/mongod.conf` file includes the correct options.  

#. Start the ``mongod`` instance::

    sudo service mongod start

For more information, see :ref:`apt`.

Upgrading on RHEL and CentOS
============================

1. Stop the ``mongod`` instance::

    sudo service mongod stop

#. Remove |PSMDB| 3.4 packages::

    sudo yum remove Percona-Server-MongoDB-34*

#. Install |PSMDB| 3.6 packages::

    sudo yum install Percona-Server-MongoDB-36

#. Start the ``mongod`` instance::

    sudo service mongod start

.. note::

   When you remove old packages on Centos / RHEL, your modified configuration file is placed to :file:`/etc/mongod.conf.rpmsave`. To use your configuration with the new version, do the following before you start the ``mongod`` service:
   
   - Replace the default :file:`/etc/mongod.conf` file,
   - Check the permissions for the ``mongod`` user to custom paths for database and/or log files.
   - Restore the permissions, if needed::
       
      chown -R mongod:mongod <dpPathDir> <logDir>
   
For more information, see :ref:`yum`.


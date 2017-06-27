.. _upgrade_from_32:

=================================
Upgrading from |PSMDB| 3.2 to 3.4
=================================

To upgrade |PSMDB| to version 3.4, you must be running version 3.2.
Upgrades from earlier versions are not supported.

For information about changes in |PSMDB| 3.4 compared to 3.2,
see :ref:`changed_in_34`.

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

#. Remove |PSMDB| 3.2 packages::

    sudo apt-get remove percona-server-mongodb-32*

#. Install |PSMDB| 3.4 packages::

    sudo apt-get install percona-server-mongodb-34

#. Start the ``mongod`` instance::

    sudo service mongod start

For more information, see :ref:`apt`.

Upgrading on RHEL and CentOS
============================

1. Stop the ``mongod`` instance::

    sudo service mongod stop

#. Remove |PSMDB| 3.2 packages::

    sudo yum remove Percona-Server-MongoDB-32*

#. Install |PSMDB| 3.4 packages::

    sudo yum install Percona-Server-MongoDB-34

#. Start the ``mongod`` instance::

    sudo service mongod start

For more information, see :ref:`yum`.


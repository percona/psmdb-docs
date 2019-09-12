.. _upgrade_from_40:

================================================================================
Upgrading from |PSMDB| |prev-version| to |version|
================================================================================

:Availability: MongoRocks has been removed from |PSMDB| |version|

To upgrade |PSMDB| to version |version|, you must be running version
|prev-version| Upgrades from earlier versions are not supported.

Before upgrading your production |PSMDB| deployments, test all your applications
in a testing environment to make sure they are compatible with the new version.

The general procedure for performing an in-place upgrade (where your existing
data and configuration files are preserved) includes the following steps:

1. Stop the :program:`mongod` instance
#. Remove old packages
#. Install new packages
#. Start the :program`mongod` instance

It is recommended to upgrade |PSMDB| from official Percona repositories using
the corresponding package manager for your system.  For more information, see
:ref:`install`.

.. warning::

   Perform a full backup of your data and configuration files before upgrading.

Upgrading on Debian or Ubuntu
================================================================================

|tip.run-all.root|

1. Stop the ``mongod`` instance: :bash:`service mongod stop`
#. Remove |PSMDB| |prev-version| packages: :bash:`apt-get remove percona-server-mongodb*`
#. Install |PSMDB| |version| packages: :bash:`apt-get install percona-server-mongodb`
#. Start the ``mongod`` instance: :bash:`service mongod start`

For more information, see :ref:`apt`.

Upgrading on RHEL and CentOS
================================================================================

|tip.run-all.root|

1. Stop the ``mongod`` instance: :bash:`service mongod stop`
#. Remove |PSMDB| |prev-version| packages: :bash:`yum remove percona-server-mongodb*`
#. Install |PSMDB| |version| packages: :bash:`yum install percona-server-mongodb`
#. Start the ``mongod`` instance:: :bash:`service mongod start`

For more information, see :ref:`yum`.

.. include:: ../.res/replace.txt

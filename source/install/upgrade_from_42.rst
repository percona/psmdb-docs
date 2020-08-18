.. _upgrade_from_42:

================================================================================
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

Upgrading on Debian or Ubuntu
================================================================================

|tip.run-all.root|

1. Stop the ``mongod`` instance: |service.mongod.stop|
#. Enable |percona| repository for |PSMDB| |version|: :bash:`percona-release enable psmdb-44`
#. Update the local cache: :bash:`apt-get update`
#. Install |PSMDB| |version| packages: :bash:`apt-get install percona-server-mongodb`     
#. Start the ``mongod`` instance: |service.mongod.start|

For more information, see :ref:`apt`.

.. include:: ../.res/text/enable_features.txt   

Upgrading on RHEL and CentOS
================================================================================

|tip.run-all.root|

1. Stop the ``mongod`` instance: |service.mongod.stop|
#. Enable |percona| repository for |PSMDB| |version|: :bash:`percona-release enable psmdb-44`
#. Install |PSMDB| |version| packages: :bash:`yum install percona-server-mongodb`
#. Start the ``mongod`` instance: |service.mongod.start|

For more information, see :ref:`yum`.

.. include:: ../.res/text/enable_features.txt   

.. include:: ../.res/replace.txt
.. include:: ../.res/replace.program.txt

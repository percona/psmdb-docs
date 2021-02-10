.. _upgrade_from_mongodb:

================================================================================
Upgrading from |mongodb-ce| to |PSMDB|
================================================================================

An in-place upgrade is done with existing data in the server.  Generally
speaking, this is stopping the ``mongod`` service, removing the old packages, installing the
new server and starting it with the same db data directory. An in-place upgrade
is suitable for most environments, except the ones that use ephemeral storage and/or host addresses.

.. note::

   MongoDB creates a user that belongs to two groups, which is a potential
   security risk.  This is fixed in |PSMDB|: user is included only in the
   ``mongod`` group.  To avoid problems with current MongoDB setups, existing
   user group membership is not changed when you migrate to |PSMDB|.  Instead, a
   new ``mongod`` user is created during installation, and it belongs to the
   ``mongod`` group.

This document describes an in-place upgrade of a ``mongod`` instance. If you are using data at rest encryption, refer to the :ref:`upgrade_encryption` section. 

.. contents::
   :local:

Prerequisites
=================

Before you start the upgrade, update the |mongodb| configuration file
(:file:`/etc/mongod.conf`) to contain the following settings.  

.. code-block:: yaml

   processManagement:
      fork: true
      pidFilePath: /var/run/mongod.pid

Troubleshooting tip: The ``pidFilePath`` setting in :file:`mongod.conf` must  match the ``PIDFile`` option in the ``systemd mongod`` service unit. Otherwise, the service will kill the ``mongod`` process after a timeout.

.. warning::

   Before starting the upgrade, we recommend to perform a full
   backup of your data.  

Upgrading on Debian or Ubuntu
=======================================================

1. Stop the ``mongod`` service: 
   
   .. code-block:: bash
   
      $ sudo systemctl stop mongod

2. Check for installed packages:

   .. code-block:: bash

      $ dpkg -l | grep mongod

      ii  mongodb-org                    3.6.2                              amd64        MongoDB open source document-oriented database system (metapackage)
      ii  mongodb-org-mongos             3.6.2                              amd64        MongoDB sharded cluster query router
      ii  mongodb-org-server             3.6.2                              amd64        MongoDB database server
      ii  mongodb-org-shell              3.6.2                              amd64        MongoDB shell client
      ii  mongodb-org-tools              3.6.2                              amd64        MongoDB tools

3. Remove installed packages:

   .. code-block:: bash

      $ sudo apt-get remove \
      mongodb-org \
      mongodb-org-mongos \
      mongodb-org-server \
      mongodb-org-shell \
      mongodb-org-tools

#. Remove log files: 
  
   .. code-block:: bash
  
      $ sudo rm -r /var/log/mongodb

#. Install |PSMDB| :ref:`using apt <apt>`
#. Verify that the configuration file includes the correct options. For example, |PSMDB| stores data files in :file:`/var/lib/mongodb` by default. If you used another ``dbPath`` data directory, edit the configuration file accordingly
   
#. Start the ``mongod`` service: 
   
   .. code-block:: bash
   
      $ sudo systemctl start mongod

Upgrading on Red Hat Enterprise Linux or CentOS
=======================================================

1. Stop the ``mongod`` service: 

   .. code-block:: bash

      $ sudo systemctl stop mongod

#. Check for installed packages:

   .. code-block:: bash

      $ rpm -qa | grep mongo

      mongodb-org-mongos-3.6.2-1.el6.x86_64
      mongodb-org-shell-3.6.2-1.el6.x86_64
      mongodb-org-server-3.6.2-1.el6.x86_64
      mongodb-org-tools-3.6.2-1.el6.x86_64
      mongodb-org-3.6.2-1.el6.x86_64

3. Remove the installed packages:

   .. code-block:: bash

      $ sudo yum remove \
      mongodb-org-mongos-3.6.2-1.el6.x86_64 mongodb-org-shell-3.6.2-1.el6.x86_64 \
      mongodb-org-server-3.6.2-1.el6.x86_64 mongodb-org-tools-3.6.2-1.el6.x86_64 \
      mongodb-org-3.6.2-1.el6.x86_64

#. Remove log files: 
   
   .. code-block:: bash
   
      $ sudo rm -r /var/log/mongodb

#. Install Percona Server for MongoDB :ref:`using yum <yum>`.
#. Start the ``mongod`` service: 

   .. code-block:: bash
   
      $ sudo systemctl start mongod

.. note:: When you remove old packages,
   your existing configuration file is saved
   as :file:`/etc/mongod.conf.rpmsave`.
   If you want to use this configuration with the new version,
   replace the default :file:`/etc/mongod.conf` file.
   For example, existing data may not be compatible
   with the default WiredTiger storage engine.

To upgrade a replica set or a sharded cluster, use the :term:`rolling restart <Rolling restart>` method. It allows you to perform the upgrade with minimum downtime. You upgrade the nodes one by one, while the whole cluster / replica set remains operational.

.. seealso::

   |mongodb| Documentation: 
      - `Upgrade a Replica Set <https://docs.mongodb.com/manual/release-notes/4.0-upgrade-replica-set/>`_
      - `Upgrade a Sharded Cluster <https://docs.mongodb.com/manual/release-notes/4.0-upgrade-sharded-cluster/>`_ 

.. _upgrade_encryption:

Upgrading to |PSMDB| with data at rest encryption enabled
=========================================================

Steps to upgrade from |mongodb-ce| with data encryption enabled to |PSMDB| are different. ``mongod`` requires an empty ``dbPath`` data directory because it cannot encrypt data files in place. It must receive data from other replica set members during the initial sync. Please refer to the :ref:`switch_storage_engines` for more information on migration of encrypted data. `Contact us <https://www.percona.com/about-percona/contact#us>`_ for working at the detailed migration steps, if further assistance is needed.

.. include:: ../.res/replace.txt



.. _upgrade_from_mongodb:

================================================================================
Upgrading from |mongodb-ce|
================================================================================

An in-place upgrade is done with existing data in the server.  Generally
speaking, this is stopping the server, removing the old packages, installing the
new server and starting it with the same data files.  While an in-place upgrade
may not be suitable for high-complexity environments, it should work in most
cases.

.. note::

   MongoDB creates a user that belongs to two groups, which is a potential
   security risk.  This is fixed in |PSMDB|: the user is included only in the
   ``mongod`` group.  To avoid problems with current MongoDB setups, existing
   user group membership is not changed when you migrate to |PSMDB|.  Instead, a
   new ``mongod`` user is created during installation, and it belongs to the
   ``mongod`` group.

This document describes an in-place upgrade of a ``mongod`` instance. If you are using data at rest encryption, refer to the :ref:`upgrade_encryption"` section. 

.. contents::
   :local: 

Prerequisites
==================

Before you start the upgrade, update the |mongodb| configuration file
(:file:`/etc/mongod.conf`) to contain the following settings.  Otherwise the
|mongod| service will not be able to start.

.. code-block:: yaml

   processManagement:
      fork: true
      pidFilePath: /var/run/mongod.pid

.. warning::

   Before starting the upgrade procedure, we recommend to perform a full
   backup of your data.  

Upgrading on Debian or Ubuntu
=========================================

|tip.run-all.root|

1. Stop the ``mongod`` service: |service.mongod.stop|

#. Check for installed packages: :bash:`dpkg -l | grep mongod`

   .. admonition:: Output

      .. code-block:: guess

	 ii  mongodb-org            4.4.0    amd64      MongoDB open source document-oriented database system (metapackage)
	 ii  mongodb-org-mongos     4.4.0    amd64      MongoDB sharded cluster query router
	 ii  mongodb-org-server     4.4.0    amd64      MongoDB database server
	 ii  mongodb-org-shell      4.4.0    amd64      MongoDB shell client
	 ii  mongodb-org-tools      4.4.0    amd64      MongoDB tools

#. Remove the installed packages:

   .. code-block:: bash

      $ apt-get remove mongodb-org mongodb-org-mongos mongodb-org-server \
      $ mongodb-org-shell mongodb-org-tools

#. Remove log files: :bash:`rm -r /var/log/mongodb`

#. Install |PSMDB| :ref:`using apt <apt>`
   
#. Verify that the configuration file includes the correct options. For example, |PSMDB| stores data files in :file:`/var/lib/mongodb` by default. If you used another ``dbPath`` data directory, edit the configuration file accordingly
   
#. Start the ``mongod`` service: |service.mongod.start|

Upgrading on Red Hat Enterprise Linux or CentOS
====================================================

|tip.run-all.root|

1. Stop the ``mongod`` service: |service.mongod.stop| 
#. Check for installed packages: :bash:`rpm -qa | grep mongo`

   .. admonition:: Output

      .. code-block:: guess

	 mongodb-org-mongos-4.4.0-1.el6.x86_64
	 mongodb-org-shell-4.4.0-1.el6.x86_64
	 mongodb-org-server-4.4.0-1.el6.x86_64
	 mongodb-org-tools-4.4.0-1.el6.x86_64
	 mongodb-org-4.4.0-1.el6.x86_64

#. Remove the installed packages:

   .. code-block:: bash

      $ yum remove \
      mongodb-org-mongos-4.4.0-1.el6.x86_64 \
      mongodb-org-shell-4.4.0-1.el6.x86_64 \
      mongodb-org-server-4.4.0-1.el6.x86_64 \
      mongodb-org-tools-4.4.0-1.el6.x86_64 \
      mongodb-org-4.4.0-1.el6.x86_64

#. Remove log files: :bash:`rm -r /var/log/mongodb`
#. Install |PSMDB| :ref:`using yum <yum>`.

.. note::

   When you remove old packages, your existing configuration file is saved as
   :file:`/etc/mongod.conf.rpmsave`.  If you want to use this configuration with
   the new version, replace the default :file:`/etc/mongod.conf` file.  For
   example, existing data may not be compatible with the default WiredTiger
   storage engine.

To upgrade a replica set or a sharded cluster, use the :term:`rolling restart <Rolling restart>` method. It allows you to perform the upgrade with minimum downtime. You upgrade the nodes one by one, while the whole cluster / replica set remains operational. 

.. seealso::

   |mongodb| Documentation: 
      - `Upgrade a Replica Set <https://docs.mongodb.com/manual/release-notes/4.4-upgrade-replica-set/>`_
      - `Upgrade a Sharded Cluster <https://docs.mongodb.com/manual/release-notes/4.4-upgrade-sharded-cluster/>`_

Upgrading to |PSMDB| with data at rest encryption enabled
=========================================================

Steps to upgrade from |mongodb-ce| with data encryption enabled to |PSMDB| are different. ``mongod`` requires an empty ``dbPath`` data directory because it cannot encrypt data files in place. It must receive data from other replica set members during the initial sync. Please refer to the :ref:`switch_storage_engines` for more information on migration of encrypted data. `Contact us <https://www.percona.com/about-percona/contact#us>`_ for working at the detailed migration steps, if further assistance is needed.


.. include:: ../.res/replace.txt
.. include:: ../.res/replace.program.txt

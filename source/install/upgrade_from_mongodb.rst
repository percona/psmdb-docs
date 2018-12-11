.. _upgrade_from_mongodb:

================================================================================
Upgrading from |mongodb-ce|
================================================================================

.. note::

   MongoDB creates a user that belongs to two groups, which is a potential
   security risk.  This is fixed in |PSMDB|: user is included only in the
   ``mongod`` group.  To avoid problems with current MongoDB setups, existing
   user group membership is not changed when you migrate to |PSMDB|.  Instead, a
   new ``mongod`` user is created during installation, and it belongs to the
   ``mongod`` group.

An in-place upgrade is done with existing data in the server.  Generally
speaking, this is stopping the server, removing the old packages, installing the
new server and starting it with the same data files.  While an in-place upgrade
may not be suitable for high-complexity environments, it should work in most
cases.

.. warning::

   Before starting the upgrade process it is recommended to perform a full
   backup of your data.

The upgrade process depends on the distribution you are using:

.. contents::
   :local:

Upgrading on Debian or Ubuntu
================================================================================

|tip.run-all.root|

1. Stop the mongod process: |service.mongod.stop|

2. Check for installed packages: :bash:`dpkg -l | grep mongod`

   .. admonition:: Output

      .. code-block:: guess

	 ii  mongodb-org            4.0.4    amd64      MongoDB open source document-oriented database system (metapackage)
	 ii  mongodb-org-mongos     4.0.4    amd64      MongoDB sharded cluster query router
	 ii  mongodb-org-server     4.0.4    amd64      MongoDB database server
	 ii  mongodb-org-shell      4.0.4    amd64      MongoDB shell client
	 ii  mongodb-org-tools      4.0.4    amd64      MongoDB tools

3. Remove the installed packages:

   .. code-block:: bash

      $ apt-get remove mongodb-org mongodb-org-mongos mongodb-org-server \
      $ mongodb-org-shell mongodb-org-tools

4. Install |PSMDB| :ref:`using apt <apt>`.

Upgrading on Red Hat Enterprise Linux or CentOS
================================================================================

|tip.run-all.root|

1. Stop the mongod process: |service.mongod.stop|
#. Check for installed packages: :bash:`rpm -qa | grep mongo`

   .. admonition:: Output

      .. code-block:: guess

	 mongodb-org-mongos-4.0.4-1.el6.x86_64
	 mongodb-org-shell-4.0.4-1.el6.x86_64
	 mongodb-org-server-4.0.4-1.el6.x86_64
	 mongodb-org-tools-4.0.4-1.el6.x86_64
	 mongodb-org-4.0.4-1.el6.x86_64

3. Remove the installed packages:

   .. code-block:: bash

      $ yum remove \
      mongodb-org-mongos-4.0.4-1.el6.x86_64 \
      mongodb-org-shell-4.0.4-1.el6.x86_64 \
      mongodb-org-server-4.0.4-1.el6.x86_64 \
      mongodb-org-tools-4.0.4-1.el6.x86_64 \
      mongodb-org-4.0.4-1.el6.x86_64

4. Install Percona Server for MongoDB :ref:`using yum <yum>`.

.. note::

   When you remove old packages, your existing configuration file is saved as
   :file:`/etc/mongod.conf.rpmsave`.  If you want to use this configuration with
   the new version, replace the default :file:`/etc/mongod.conf` file.  For
   example, existing data may not be compatible with the default WiredTiger
   storage engine.

.. include:: ../.res/replace.txt
.. include:: ../.res/replace.program.txt

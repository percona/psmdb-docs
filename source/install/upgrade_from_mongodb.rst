.. _upgrade_from_mongodb:

======================================================================
Upgrading from MongoDB Community Edition to Percona Server for MongoDB
======================================================================

.. note:: MongoDB creates a user that belongs to two groups,
   which is a potential security risk.
   This is fixed in |PSMDB|: user is included only in the ``mongod`` group.
   To avoid problems with current MongoDB setups,
   existing user group membership is not changed
   when you migrate to |PSMDB|.
   Instead, a new ``mongod`` user is created during installation,
   and it belongs to the ``mongod`` group.

An in-place upgrade is done with existing data in the server.
Generally speaking, this is stopping the server, removing the old packages,
installing the new server and starting it with the same data files.
While an in-place upgrade may not be suitable for high-complexity environments,
it should work in most cases.

Upgrading from an earlier version of Percona Server for MongoDB
(for example, from 3.0) is the same as upgrading from MongoDB 3.0 or 3.2.

.. warning:: Before starting the upgrade process
   it is recommended to perform a full backup of your data.

The upgrade process depends on the distribution you are using:

.. contents::
   :local:

Upgrading on Debian or Ubuntu
=============================

1. Stop the mongod process:

   .. prompt:: bash

      service mongod stop

2. Check for installed packages:

   .. code-block:: bash

      $ dpkg -l | grep mongod

      ii  mongodb-org                              3.0.6                         amd64        MongoDB open source document-oriented database system (metapackage)
      ii  mongodb-org-mongos                       3.0.6                         amd64        MongoDB sharded cluster query router
      ii  mongodb-org-server                       3.0.6                         amd64        MongoDB database server
      ii  mongodb-org-shell                        3.0.6                         amd64        MongoDB shell client
      ii  mongodb-org-tools                        3.0.6                         amd64        MongoDB tools

3. Remove installed packages:

   .. prompt:: bash

      apt-get remove mongodb-org mongodb-org-mongos mongodb-org-server \ 
      mongodb-org-shell mongodb-org-tools

4. Install Percona Server for MongoDB :ref:`using apt <apt>`.

Upgrading on Red Hat Enterprise Linux or CentOS
===============================================

1. Stop the mongod process:

   .. prompt:: bash 

      service mongod stop

2. Check for installed packages: 

   .. code-block:: bash

      $ rpm -qa | grep mongo

      mongodb-org-3.0.6-1.el6.x86_64
      mongodb-org-server-3.0.6-1.el6.x86_64 
      mongodb-org-shell-3.0.6-1.el6.x86_64
      mongodb-org-mongos-3.0.6-1.el6.x86_64
      mongodb-org-tools-3.0.6-1.el6.x86_64

3. Remove installed packages:

   .. prompt:: bash

      $ yum remove \
      mongodb-org-3.0.6-1.el6.x86_64 mongodb-org-server-3.0.6-1.el6.x86_64 \
      mongodb-org-shell-3.0.6-1.el6.x86_64 mongodb-org-mongos-3.0.6-1.el6.x86_64 \
      mongodb-org-tools-3.0.6-1.el6.x86_64

4. Install Percona Server for MongoDB :ref:`using yum <yum>`.


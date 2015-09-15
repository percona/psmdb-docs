.. _upgrading_guide_mongodb_psmdb:

=================================================
Replacing MongoDB with Percona Server for MongoDB
=================================================

In-place upgrades are those which are done using the existing data in the server. Generally speaking, this is stopping the server, removing the old packages, installing the new server and starting it with the same data files. While they may not be suitable for high-complexity environments, they may be adequate for many scenarios.

.. warning:: 

  Before starting the upgrade process it's recommended that you perform a full backup (if you don't have one already). 


Replacing MongoDB on CentOS/RHEL
================================

1) Stop the mongod process:

.. code-block:: bash 

   $ service mongod stop

2) Check for the installed packages: 

.. code-block:: bash

   $ rpm -qa | grep mongo

   mongodb-org-3.0.6-1.el6.x86_64
   mongodb-org-server-3.0.6-1.el6.x86_64 
   mongodb-org-shell-3.0.6-1.el6.x86_64                                                 
   mongodb-org-mongos-3.0.6-1.el6.x86_64 
   mongodb-org-tools-3.0.6-1.el6.x86_64

3) Remove the installed packages:

.. code-block:: bash

   $ yum remove mongodb-org-3.0.6-1.el6.x86_64 mongodb-org-server-3.0.6-1.el6.x86_64 \
   mongodb-org-shell-3.0.6-1.el6.x86_64 mongodb-org-mongos-3.0.6-1.el6.x86_64 \
   mongodb-org-tools-3.0.6-1.el6.x86_64

4) You can now proceed with steps described in :ref:`yum_repo`.

Replacing MongoDB on Debian/Ubuntu
==================================

1) Stop the mongod process:

.. code-block:: bash

   $ service mongod stop

2) Check for the installed packages:

.. code-block:: bash

   $ dpkg -l | grep mongod

   ii  mongodb-org                              3.0.6                         amd64        MongoDB open source document-oriented database system (metapackage)
   ii  mongodb-org-mongos                       3.0.6                         amd64        MongoDB sharded cluster query router
   ii  mongodb-org-server                       3.0.6                         amd64        MongoDB database server
   ii  mongodb-org-shell                        3.0.6                         amd64        MongoDB shell client
   ii  mongodb-org-tools                        3.0.6                         amd64        MongoDB tools

3) Remove the installed packages:

.. code-block:: bash

   $ apt-get remove ongodb-org mongodb-org-mongos mongodb-org-server \ 
   mongodb-org-shell mongodb-org-tools

4) You can now proceed with steps described in :ref:`apt_repo`.

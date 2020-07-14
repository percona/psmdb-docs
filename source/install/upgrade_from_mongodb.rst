.. _upgrade_from_mongodb:

================================================================================
Upgrading from |mongodb| |prev-version| Community Edition 
================================================================================


.. note::

   MongoDB creates a user that belongs to two groups, which is a potential
   security risk.  This is fixed in |PSMDB|: the user is included only in the
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

   Before starting the upgrade procedure, we recommend to perform a full
   backup of your data.

The sections below describe an in-place upgrade of a standalone instance and a replica set without encryption. 

.. contents::
   :local:

.. _upgrade_standalone:   

Upgrading a standalone instance or a single-node replica set 
================================================================================

The upgrade procedure depends on the distribution you are using:

Upgrading on Debian or Ubuntu
--------------------------------------------------------------------------------

|tip.run-all.root|

.. include:: ../.res/text/important.mongod-conf.txt
.. Is this warning still actual?

1. Stop the ``mongod`` service: :bash:`systemctl stop mongod`

#. Check for installed packages: :bash:`dpkg -l | grep mongod`

   .. admonition:: Output

      .. code-block:: guess

	 ii  mongodb-org            4.2.7    amd64      MongoDB open source document-oriented database system (metapackage)
	 ii  mongodb-org-mongos     4.2.7    amd64      MongoDB sharded cluster query router
	 ii  mongodb-org-server     4.2.7    amd64      MongoDB database server
	 ii  mongodb-org-shell      4.2.7    amd64      MongoDB shell client
	 ii  mongodb-org-tools      4.2.7    amd64      MongoDB tools

#. Remove the installed packages:

   .. code-block:: bash

      $ apt-get remove mongodb-org mongodb-org-mongos mongodb-org-server \
      $ mongodb-org-shell mongodb-org-tools

#. Remove log files: :bash:`rm -r /var/log/mongodb`

#. Install |PSMDB| :ref:`using apt <apt>`
   
#. Verify that the configuration file includes the correct options. For example, |PSMDB| stores data files in :file:`/var/lib/mongodb` by default. If you used another ``dbPath`` data directory, edit the configuration file accordingly
   
#. Start the ``mongod`` service: :bash:`systemctl start mongod`

Upgrading on Red Hat Enterprise Linux or CentOS
--------------------------------------------------------------------------------

|tip.run-all.root|

.. include:: ../.res/text/important.mongod-conf.txt
.. Is this warning still actual?

1. Stop the ``mongod`` service: :bash:`systemctl stop mongod` 
#. Check for installed packages: :bash:`rpm -qa | grep mongo`

   .. admonition:: Output

      .. code-block:: guess

	 mongodb-org-mongos-4.2.7-1.el6.x86_64
	 mongodb-org-shell-4.2.7-1.el6.x86_64
	 mongodb-org-server-4.2.7-1.el6.x86_64
	 mongodb-org-tools-4.2.7-1.el6.x86_64
	 mongodb-org-4.2.7-1.el6.x86_64

#. Remove the installed packages:

   .. code-block:: bash

      $ yum remove \
      mongodb-org-mongos-4.2.7-1.el6.x86_64 \
      mongodb-org-shell-4.2.7-1.el6.x86_64 \
      mongodb-org-server-4.2.7-1.el6.x86_64 \
      mongodb-org-tools-4.2.7-1.el6.x86_64 \
      mongodb-org-4.2.7-1.el6.x86_64

#. Remove log files: :bash:`rm -r /var/log/mongodb`
#. Install |PSMDB| :ref:`using yum <yum>`.

.. note::

   When you remove old packages, your existing configuration file is saved as
   :file:`/etc/mongod.conf.rpmsave`.  If you want to use this configuration with
   the new version, replace the default :file:`/etc/mongod.conf` file.  For
   example, existing data may not be compatible with the default WiredTiger
   storage engine.

Upgrading a replica set
================================================================================

The :term:`rolling restart <Rolling restart>` method allows upgrading a replica set from |mongodb-ce| to |PSMDB| with minimum downtime. You upgrade the nodes one by one while the whole cluster remains operational.   

Upgrade some but not all replica set nodes  
--------------------------------------------------------------------------------

1. Upgrade a node in a replica set as described in :ref:`upgrade_standalone`. Use the instructions relevant to your operating system. 

.. note::

   It is better to upgrade the secondary node to avoid an extra election of the primary one. If you upgrade the primary node, run the :command:`rs.stepDown()` command before shutting it down.

#. Wait for the node to rejoin with the replica set members, resync and report that it is in the SECONDARY status. 
#. Optional: repeat the upgrade procedure on other (but not on all) nodes.

Test the |PSMDB| node in the primary role before all nodes are upgraded
--------------------------------------------------------------------------------

This step is optional. Its purpose is to run a testing stage with the |PSMDB| node as primary whilst at least one of nodes still runs the old version. This will make rolling back a little quicker if you choose to do so.

1. Use :command:`rs.stepDown()` on the current primary node to start an election of a new primary among nodes with |PSMDB| installed. If you have multiple nodes of the previous version, use :command:`rs.freeze()` on them to make sure one of |PSMDB| nodes becomes primary.
 
Upgrade the last node(s)
--------------------------------------------------------------------------------

1. If any of the previous version nodes is the current primary node, step it down: :command:`rs.stepDown()`.
2. Wait for the remaining nodes to elect a new primary. Run :command:`rs.status()` to verify that the former primary node reports as SECONDARY.
#. Upgrade the node as described in :ref:`upgrade_standalone`.
   
.. seealso::

   |mongodb| Documentation: Upgrade a Replica Set
       https://docs.mongodb.com/manual/release-notes/4.2-upgrade-replica-set/

.. note::

   Steps to upgrade from |mongodb-ce| with data encryption enabled to |PSMDB| are different. ``mongod`` requires an empty ``dbPath`` data directory because it cannot encrypt data files in place. It must receive data from other replica set members during the initial sync. Please refer to the :ref:`switch_storage_engines` for more information on migration of encrypted data. `Contact us <https://www.percona.com/about-percona/contact#us>`_ for working at the detailed migration steps, if further assistance is needed.


.. include:: ../.res/replace.txt
.. include:: ../.res/replace.program.txt

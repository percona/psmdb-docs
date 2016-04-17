.. _upgrade_from_tokumx:

===========================================================
Upgrading from Percona TokuMX to Percona Server for MongoDB
===========================================================

This guide describes how to upgrade existing |TokuMX| instance to |Percona Server for MongoDB|. The same process should work when upgrading from MongoDB prior to version 3.0 (such as, 2.4 and 2.6).

The following JavaScript files are required to perform the upgrade:

* :file:`allDbStats.js`
* :file:`tokumx_dump_indexes.js`
* :file:`psmdb_restore_indexes.js`

You can download those files from `GitHub <https://github.com/dbpercona/tokumx2_to_psmdb3_migration>`_.

.. warning:: Before starting the upgrade process, it is recommended that you perform a full backup.

To performa the upgrade:

1. Restart the TokuMX server without the ``--auth`` parameter:

  .. code-block:: bash

     $ service tokumx stop
     $ sed -i'' s/^auth/#auth/ /etc/tokumx.conf
     $ service tokumx start

2. Run the :file:`allDbStats.js` script to record database state before migration:

  .. code-block:: bash

     $ mongo ./allDbStats.js > ~/allDbStats.before.out

3. Perform a dump of the database:

  .. code-block:: bash

     $ mongodump --out /your/dump/path

4. Perform a dump of the indexes:

  .. code-block:: bash

     $ ./tokumx_dump_indexes.js > /your/dump/path/tokumxIndexes.json

5. Stop the TokuMX server:

  .. code-block:: bash

     $ service tokumx stop

6. Move the data directory and copy the configuration for safekeeping.

  .. code-block:: bash

     $ mv /var/lib/tokumx /var/lib/tokumx.bak
     $ cp /etc/tokumx.conf /etc/tokumx.conf.bak

7. Uninstall all TokuMX packages.

  If you are using a Debian or Ubuntu based distribution:

  .. code-block:: bash

     $ dpkg -P --force-all `dpkg -l | grep tokumx | awk '{print $2}'`

  If you are using a Red Hat or CentOS based distribution:
 
  .. code-block:: bash

     $ yum remove -y tokumx-enterprise-common-2.0.2-1.el6.x86_64 \
         tokumx-enterprise-server-2.0.2-1.el6.x86_64 \ 
         tokumx-enterprise-2.0.2-1.el6.x86_64

8. Install |Percona Server for MongoDB| as described in the :ref:`Installation Guide <install>`.

9. Stop the ``mongod`` service, configure the ``storage.engine`` parameter to run PerconaFT and disable ``--auth`` in :file:`/etc/mongod.conf`:

  .. code-block:: bash

     $ service mongod stop
     $ sed -i '/engine: \*PerconaFT/s/#//g' /etc/mongod.conf
     $ sed -i'' s/^auth/#auth/ /etc/mongod.conf

  For more information about configuring the storage engine, see :ref:`switch-storage-engines`.

10. Start the ``mongod`` server:

  .. code-block:: bash

     $ service mongod start

11. Restore the collections without indexes:

  .. code-block:: bash

     $ mongorestore --noIndexRestore /your/dump/path

12. Restore the indexes (this may take a while). This step will remove clustering options to the collections before inserting.

  .. code-block:: bash

     $ ./psmdb_restore_indexes.js --eval " data='/your/dump/path/tokumxIndexes.json' "

13. Run the :file:`allDbStats.js` script to record database state after migration:

  .. code-block:: bash

     $ mongo ./allDbStats.js > ~/allDbStats.after.out

14. Restart the ``mongod`` server with authentication:

  .. code-block:: bash

     $ service mongod stop
     $ sed -i'' s/^i#auth/auth/ /etc/mongod.conf
     $ service mongod start

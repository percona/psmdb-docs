.. _hot-backup:

==========
Hot Backup
==========

|PSMDB| includes an integrated open-source hot backup system
for the default WiredTiger_ and alternative :ref:`mongorocks` storage engine.
It creates a physical data backup on a running server
without notable performance and operating degradation.

To take a hot backup of the database in your current ``dbpath``,
run the ``createBackup`` command as administrator on the ``admin`` database
and specify the backup directory.

.. code-block:: text

   > use admin
   switched to db admin
   > db.runCommand({createBackup: 1, backupDir: "/my/backup/data/path"})
   { "ok" : 1 }

If the backup was successful, you should receive an ``{ "ok" : 1 }`` object.
If there was an error, you will receive a failing ``ok`` status
with the error message, for example:

.. code-block:: text

   > db.runCommand({createBackup: 1, backupDir: ""})
   { "ok" : 0, "errmsg" : "Destination path must be absolute" }


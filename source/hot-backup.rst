.. _hot-backup:

================================================================================
Hot Backup
================================================================================

|PSMDB| includes an integrated open-source hot backup system for the default
WiredTiger_ storage engine.  It creates a physical data backup on a running
server without notable performance and operating degradation.

.. contents::
   :local:  

Making a backup
===============

To take a hot backup of the database in your current ``dbpath``, do the following:

- Make sure to provide access to the backup directory for the ``mongod`` user.

  .. code-block:: bash

     chown mongod:mongod <backupDir>

- Run the ``createBackup`` command as administrator on the ``admin`` database and specify the backup directory. 

  .. code-block:: text

     > use admin
     switched to db admin
     > db.runCommand({createBackup: 1, backupDir: <backup_data_path})
     { "ok" : 1 }

If the backup was successful, you should receive an ``{ "ok" : 1 }`` object.
If there was an error, you will receive a failing ``ok`` status
with the error message, for example:

.. code-block:: text

   > db.runCommand({createBackup: 1, backupDir: ""})
   { "ok" : 0, "errmsg" : "Destination path must be absolute" }

Saving a Backup to a TAR Archive
---------------------------------------------------------------------

.. admonition:: Implementation details

   This feature was implemented in |PSMDB| 4.0.12-6.

To save a backup in the format of *tar* archive, use the *archive* field to
specify the destination path:

.. code-block:: text

   > use admin
   ...
   > db.runCommand({createBackup: 1, archive: <path_to_archive>.tar })

.. _psmdb-hot-backup-remote-destination:

Streaming Hot Backups to a Remote Destination
---------------------------------------------------------------------

Starting from version 4.0.12-6, |PSMDB| enables uploading hot backups
to an `Amazon S3 <https://aws.amazon.com/s3/>`_ or a compatible storage service,
such as `MinIO <https://min.io/>`_.

This method requires that you provide the *bucket* field in the *s3* object:

.. code-block:: text

   > use admin
   ...
   > db.runCommand({createBackup: 1, s3: {bucket: "backup20190510", path: <some-optional-path>} })

In addition to the mandatory *bucket* field, the *s3* object may contain the following fields:

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - Field
     - Type
     - Description
   * - bucket
     - string
     - The only mandatory field. Names are subject to restrictions described in 
       the `Bucket Restrictions and Limitations section of Amazon S3 documentation <https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html>`_
   * - path
     - string
     - The virtual path inside the specified bucket where the backup will be
       created. If the *path* is not specified then the backup is created in the root
       of the bucket. If there are any objects under the specified path, the backup
       will not be created and an error will be reported.
   * - endpoint
     - string
     - The endpoint address and port - mainly for AWS S3 compatible servers such
       as the *MinIO* server. For a local MinIO server, this can be
       "127.0.0.1:9000". For AWS S3 this field can be omitted.
   * - scheme
     - string
     - "HTTP" or "HTTPS" (default). For a local MinIO server started
       with the *minio server* command this should field should contain *HTTP*.
   * - useVirtualAddressing
     - bool
     - The style of addressing buckets in the URL. By default 'true'. For MinIO
       servers, set this field to **false**. For more information, see `Virtual
       Hosting of Buckets
       <https://docs.aws.amazon.com/AmazonS3/latest/dev/VirtualHosting.html>`_
       in the Amazon S3 documentation.
   * - region
     - string
     - The name of an AWS region. The default region is **US_EAST_1**. For more
       information see `AWS Service Endpoints
       <https://docs.aws.amazon.com/general/latest/gr/rande.html>`_ in the
       Amazon S3 documentation.
   * - profile
     - string
     - The name of a credentials profile in the *credentials* configuration file. If
       not specified, the profile named **default** is used.
   * - accessKeyId
     - string
     - The access key id
   * - secretAccessKey
     - string
     - The secret access key

.. rubric:: Credentials

If the user provides the *access key id* and the *secret access key* parameters,
these are used as credentials.

If the *access key id* parameter is not specified then the credentials are loaded from
the credentials configuration file. By default, it is :file:`~/.aws/credentials`.

.. admonition:: An example of the credentials file

   .. code-block:: text

      [default]
      aws_access_key_id = ABC123XYZ456QQQAAAFFF
      aws_secret_access_key = zuf+secretkey0secretkey1secretkey2
      [localminio]
      aws_access_key_id = ABCABCABCABC55566678
      aws_secret_access_key = secretaccesskey1secretaccesskey2secretaccesskey3

.. rubric:: Examples

**Backup in root of bucket on local instance of MinIO server**

.. code-block:: text

   > db.runCommand({createBackup: 1,  s3: {bucket: "backup20190901500", 
   scheme: "HTTP",
   endpoint: "127.0.0.1:9000",
   useVirtualAddressing: false,
   profile: "localminio"}})

**Backup on MinIO testing server with the default credentials profile**

The following command creates a backup under the virtual path  "year2019/day42" in the *backup* bucket:

.. code-block:: text

   > db.runCommand({createBackup: 1,  s3: {bucket: "backup",
   path: "year2019/day42",
   endpoint: "sandbox.min.io:9000",
   useVirtualAddressing: false}})

**Backup on AWS S3 service using default settings**

.. code-block:: text

   > db.runCommand({createBackup: 1,  s3: {bucket: "backup", path: "year2019/day42"}})

.. seealso::

   AWS Documentation: Providing AWS Credentials
      https://docs.aws.amazon.com/sdk-for-cpp/v1/developer-guide/credentials.html

Restoring data from backup
===============================

.. rubric:: Restoring from backup on a standalone server

To restore your database on a standalone server, stop the ``mongod`` service, clean out the data directory and copy files from the backup directory to the data directory. The ``mongod`` user requires access to those files to start the service. Therefore, make the ``mongod`` user the owner of the data directory and all files and subdirectories under it, and restart the ``mongod`` service.

.. code-block:: bash

   #Stop the mongod service
   $ systemctl stop mongod
   #Clean out the data directory
   $ rm -rf /var/lib/mongodb/*
   # Copy backup files
   $ cp -RT <backup_data_path> /var/lib/mongodb/
   #Grant permissions to data files for the mongod user
   $ chown -R mongod:mongod /var/lib/mongodb/
   #Start the mongod service
   $ systemctl start mongod


.. rubric:: Restoring from backup in a replica set

The recommended way to restore the replica set from a backup is to restore it into a standalone node and then initiate it as the first member of a new replica set. 

.. note:: 

   If you try to restore the node into the existing replica set and there is more recent data, the restored node detects that it is out of date with the other replica set members, deletes the data and makes an initial sync.


The restore steps are the following:

1.  Stop the ``mongod`` service:
    
    .. code-block:: bash
    
       $ systemctl stop mongod

2.  Clean the data directory and then copy the files from the backup directory to your data directory. Assuming that the data directory is :file:`/var/lib/mongodb/`, use the following commands:
    
    .. code-block:: bash
    
       $ rm -rf /var/lib/mongodb/*
       $ cp -RT <backup_data_path> /var/lib/mongodb/

#.  Grant permissions to the data files for the ``mongod`` user

    .. code-block:: bash
    
       $ chown -R mongod:mongod /var/lib/mongodb/

#.  Make sure the replication is disabled in the config file and start the ``mongod`` service. 
    
    .. code-block:: bash
    
       $ systemctl start mongod

#.  Connect to your standalone node via the ``mongo`` shell and drop the local database
    
    .. code-block:: bash
    
       $ mongo
       $ use local
       $ db.dropDatabase()

#.  Restart the node with the replication enabled
    
    * Shut down the node. 
    
      .. code-block:: bash
       
         systemctl stop mongod

    * Edit the configuration file and specify the ``replication.replSetname`` option
    * Start the ``mongod`` node:
      
      .. code-block:: bash
       
         systemctl start mongod

#.  Initiate a new replica set
    
    .. code-block:: bash
    
       # Start the mongo shell
       $ mongo
       # Initiate a new replica set
       $ rs.initiate()

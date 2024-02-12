# Hot backup

Percona Server for MongoDB includes an integrated open source hot backup system for the default
[WiredTiger](https://docs.mongodb.org/manual/core/wiredtiger/) storage engine.  It creates a physical data backup on a running
server without notable performance and operating degradation.

!!! note

    Hot backups are done on `mongod` servers independently, without synchronizing them across replica set members and shards in a cluster. To ensure data consistency during backups and restores, we recommend using [Percona Backup for MongoDB](https://docs.percona.com/percona-backup-mongodb/index.html).

## Make a backup

To take a hot backup of the database in your current `dbpath`, do the following:
{.power-number}

1. Provide access to the backup directory for the `mongod` user:

    ```{.bash data-prompt="$"}
    $ sudo chown mongod:mongod <backupDir>
    ```

2. Run the `createBackup` command as administrator on the `admin` database and specify the backup directory.
    
    ```javascript
    > use admin
    switched to db admin
    > db.runCommand({createBackup: 1, backupDir: "<backup_data_path>"})
    { "ok" : 1 }
    ```

The backup taken is the snapshot of the `mongod` server’s `dataDir` at the moment of the `createBackup` command start.

If the backup was successful, you should receive an `{ "ok" : 1 }` object.
If there was an error, you will receive a failing `ok` status
with the error message, for example:

```javascript
> db.runCommand({createBackup: 1, backupDir: ""})
{ "ok" : 0, "errmsg" : "Destination path must be absolute" }
```

## Save a backup to a TAR archive

To save a backup as a *tar* archive, use the `archive` field to
specify the destination path:

```javascript
> use admin
...
> db.runCommand({createBackup: 1, archive: <path_to_archive>.tar })
```


## Streaming hot backups to a remote destination

Percona Server for MongoDB enables uploading hot backups to an [Amazon S3](https://aws.amazon.com/s3/) or a compatible storage service, such
as [MinIO](https://min.io/).

This method requires that you provide the *bucket* field in the *s3* object:

```javascript
> use admin
...
> db.runCommand({createBackup: 1, s3: {bucket: "backup20190510", path: <some_optional_path>} })
```

In addition to the mandatory `bucket` field, the `s3` object may contain the following fields:

| Field                   | Type     | Description              |
| ----------------------- | -------- | ------------------------ |  
| bucket                  | string   | The only mandatory field. Names are subject to restrictions described in the [Bucket Restrictions and Limitations section of Amazon S3 documentation](https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html) |
| path                    | string   | The virtual path inside the specified bucket where the backup will be created. If the `path` is not specified, then the backup is created in the root of the bucket. If there are any objects under the specified path, the backup will not be created and an error will be reported.|
| endpoint                | string   | The endpoint address and port - mainly for AWS S3 compatible servers such as the *MinIO* server. For a local MinIO server, this can be "127.0.0.1:9000". For AWS S3 this field can be omitted.|
| scheme                  | string   | “HTTP” or “HTTPS” (default). For a local MinIO server started with the *minio server* command this should field should contain *HTTP*.|
| useVirtualAddressing    | bool     | The style of addressing buckets in the URL. By default ‘true’. For MinIO servers, set this field to **false**. For more information, see [Virtual Hosting of Buckets](https://docs.aws.amazon.com/AmazonS3/latest/dev/VirtualHosting.html) in the Amazon S3 documentation.    |
| region                  | string   | The name of an AWS region. The default region is **US_EAST_1**. For more information see [AWS Service Endpoints](https://docs.aws.amazon.com/general/latest/gr/rande.html) in the Amazon S3 documentation. |
| profile                 | string    | The name of a credentials profile in the *credentials* configuration file. If not specified, the profile named **default** is used.  |
| accessKeyId             | string    | The access key id  |
| secretAccessKey         | string    | The secret access key |

### Credentials

If the user provides the *access key id* and the *secret access key* parameters,
these are used as credentials.

If the *access key id* parameter is not specified then the credentials are loaded from
the credentials configuration file. By default, it is `~/.aws/credentials`.

#### Example credentials file

```title="~/.aws/credentials"
[default]
aws_access_key_id = ABC123XYZ456QQQAAAFFF
aws_secret_access_key = zuf+secretkey0secretkey1secretkey2
[localminio]
aws_access_key_id = ABCABCABCABC55566678
aws_secret_access_key = secretaccesskey1secretaccesskey2secretaccesskey3
```

### Examples

**Backup in root of bucket on local instance of MinIO server**

```javascript
> db.runCommand({createBackup: 1,  s3: {bucket: "backup20190901500",
scheme: "HTTP",
endpoint: "127.0.0.1:9000",
useVirtualAddressing: false,
profile: "localminio"}})
```

**Backup on MinIO testing server with the default credentials profile**

The following command creates a backup under the virtual path  “year2019/day42” in the `backup` bucket:

```javascript
> db.runCommand({createBackup: 1,  s3: {bucket: "backup",
path: "year2019/day42",
endpoint: "sandbox.min.io:9000",
useVirtualAddressing: false}})
```

**Backup on AWS S3 service using default settings**

```javascript
> db.runCommand({createBackup: 1,  s3: {bucket: "backup", path: "year2019/day42"}})
```

!!! admonition "See also"
 
    AWS Documentation: [Providing AWS Credentials](https://docs.aws.amazon.com/sdk-for-cpp/v1/developer-guide/credentials.html)

## Restore data from backup

### Restore on a standalone server

To restore your database on a standalone server, stop the `mongod` service, clean out the data directory and copy files from the backup directory to the data directory. The `mongod` user requires access to those files to start the service. Therefore, make the `mongod` user the owner of the data directory and all files and subdirectories under it, and restart the `mongod` service.

!!! note

    If you try to restore the node into the existing replica set and there is more recent data, the restored node detects that it is out of date with the other replica set members, deletes the data and makes an initial sync.

Run the following commands as root or by using the `sudo` command

1. Stop the `mongod` service

    ```{.bash data-prompt="$"}
    $ systemctl stop mongod
    ```

2. Clean out the data directory
   
    ```{.bash data-prompt="$"}
    $ rm -rf /var/lib/mongodb/*
    ``` 

3. Copy backup files

    ```{.bash data-prompt="$"}
    $ cp -RT <backup_data_path> /var/lib/mongodb/
    ```

4. Grant permissions to data files for the `mongod` user

    ```{.bash data-prompt="$"}
    $ chown -R mongod:mongod /var/lib/mongodb/
    ```

5. Start the `mongod` service

    ```{.bash data-prompt="$"}
    $ systemctl start mongod
    ```

### Restore in a replica set

The recommended way to restore the replica set from a backup is to restore it into a standalone node and then initiate it as the first member of a new replica set.

!!! note

    If you try to restore the node into the existing replica set and there is more recent data, the restored node detects that it is out of date with the other replica set members, deletes the data and makes an initial sync.

Run the following commands as root or by using the **sudo** command

1. Stop the `mongod` service:

    ```{.bash data-prompt="$"}
    $ systemctl stop mongod
    ```

2. Clean the data directory and then copy the files from the backup directory to your data directory. Assuming that the data directory is `/var/lib/mongodb/`, use the following commands:

    ```{.bash data-prompt="$"}
    $ rm -rf /var/lib/mongodb/*
    $ cp -RT <backup_data_path> /var/lib/mongodb/
    ```


3. Grant permissions to the data files for the `mongod` user

    ```{.bash data-prompt="$"}
    $ chown -R mongod:mongod /var/lib/mongodb/
    ```


4. Make sure the replication is disabled in the config file and start the `mongod` service.

    ```{.bash data-prompt="$"}
    $ systemctl start mongod
    ```


5. Connect to your standalone node via the `mongo` shell and drop the local database

    ```javascript
    > mongo
    > use local
    > db.dropDatabase()
    ```


6. Restart the node with the replication enabled

    * Shut down the node.

        ```{.bash data-prompt="$"}
        $ systemctl stop mongod
        ```

    * Edit the configuration file and specify the `replication.replSetname` option


    * Start the `mongod` node:

        ```{.bash data-prompt="$"}
        $ systemctl start mongod
        ```


7. Initiate a new replica set

    * Start the mongo shell
 
       ```javascript
       > mongo
       ```
          
    * Initiate a new replica set
     
       ```javascript
       > rs.initiate()
       ```
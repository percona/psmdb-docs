# Local key management using a keyfile

The key file must contain a 32 character string encoded in base64. You can generate a random
key and save it to a file by using the `openssl` command:

```{.bash data-prompt="$"}
$ openssl rand -base64 32 > mongodb-keyfile
```

Then, as the owner of the `mongod` process, update the file permissions: only
the owner should be able to read and modify this file. The effective permissions
specified with the `chmod` command can be:

* **600** - only the owner may read and modify the file
* **400** - only the owner may read the file.

```{.bash data-prompt="$"}
$ chmod 600 mongodb-keyfile
```

Enable the data encryption at rest in Percona Server for MongoDB by setting these options:

* `--enableEncryption` to enable data at rest encryption

* `--encryptionKeyFile` to specify the path to a file that contains the encryption key

```{.bash data-prompt="$"}
$ mongod ... --enableEncryption --encryptionKeyFile <fileName>
```

By default, Percona Server for MongoDB uses the `AES256-CBC` cipher mode. If you want to use the `AES256-GCM` cipher mode, then use the `--encryptionCipherMode` parameter to change it.

If `mongod` is started with the `--relaxPermChecks` option and the key file
is owned by `root`, then `mongod` can read the file based on the
group bit set accordingly. The effective key file permissions in this
case are:

* **440** - both the owner and the group can only read the file, or
* **640** - only the owner can read and the change the file, the group can only read the file.

All these options can be specified in the configuration file:

```yaml
security:
   enableEncryption: <boolean>
   encryptionCipherMode: <string>
   encryptionKeyFile: <string>
   relaxPermChecks: <boolean>
```

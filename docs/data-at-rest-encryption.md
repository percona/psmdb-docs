# Data at Rest encryption

Data at rest encryption for the WiredTiger storage engine in MongoDB was
introduced in MongoDB Enterprise version 3.2 to ensure that encrypted data
files can be decrypted and read by parties with the decryption key.

## Differences from upstream

The data encryption at rest in Percona Server for MongoDB is introduced in version 3.6 to be compatible with data encryption at rest interface in MongoDB. In the current release of Percona Server for MongoDB, the data encryption at rest does not include support for Amazon AWS key management service. Instead, Percona Server for MongoDB is [integrated with HashiCorp Vault](vault.md). 

Starting with release 4.2.19-19, Percona Server for MongoDB supports the secure transfer of keys using [Key Management Interoperability Protocol (KMIP)](kmip.md). This allows users to store encryption keys in their favorite KMIP-compatible key manager when they set up encryption at rest.

Two types of keys are used for data at rest encryption:

* Database keys to encrypt data. They are stored internally, near the data that they encrypt.

* The master key to encrypt database keys. It is kept separately from the data and database keys and requires external management.

To manage the master key, use one of the supported key management options:

* Integration with an external key server (recommended). Percona Server for MongoDB is [integrated with HashiCorp Vault](vault.md) for this purpose and supports the secure transfer of keys using [Key Management Interoperability Protocol (KMIP)](kmip.md).

* [Local key management using a keyfile](keyfile.md).

Note that you can use only one of the key management options at a time. However, you can switch from one management option to another (e.g. from a keyfile to HashiCorp Vault). Refer to [Migrating from Key File Encryption to HashiCorp Vault Encryption](encryption-mode-switch.md) section for details.

!!! important

    You can only enable data at rest encryption and provide all encryption settings on an empty database, when you start the mongod instance for the first time. You cannot enable or disable encryption while the Percona Server for MongoDB server is already running and / or has some data. Nor can you change the effective encryption mode by simply restarting the server. Every time you restart the server, the encryption settings must be the same.

## Important Configuration Options

Percona Server for MongoDB supports the `encryptionCipherMode` option where you choose one of the following cipher modes:

* AES256-CBC

* AES256-GCM

By default, the `AES256-CBC` cipher mode is applied. The following example
demonstrates how to apply the AES256-GCM cipher mode when starting the
`mongod` service:

```{.bash data-prompt="$"}
$ mongod ... --encryptionCipherMode AES256-GCM
```

!!! admonition "See also"

    MongoDB Documentation: [encryptionCipherMode Option](https://docs.mongodb.com/manual/reference/program/mongod/#cmdoption-mongod-encryptionciphermode)

## Encrypting Rollback Files

Starting from version 3.6, Percona Server for MongoDB also encrypts rollback files when data at rest encryption is enabled. To inspect the contents of these files, use **perconadecrypt**. This is a tool that you run from the command line as follows:

```{.bash data-prompt="$"}
$ perconadecrypt --encryptionKeyFile FILE  --inputPath FILE --outputPath FILE [--encryptionCipherMode MODE]
```

When decrypting, the cipher mode must match the cipher mode which was used for
the encryption. By default, the `--encryptionCipherMode` option uses the
`AES256-CBC` mode.

### Parameters of `perconadecrypt`

| Option                   | Purpose                        |
| ------------------------ | -------------------------------|
| `–-encryptionKeyFile`    | The path to the encryption key file
| `--encryptionCipherMode` | The cipher mode for decryption. The supported values are `AES256-CBC` or `AES256-GCM` | 
| `--inputPath`            | The path to the encrypted rollback file | 
| `--outputPath`           | The path to save the decrypted rollback file | 



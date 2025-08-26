# Encryption at Rest

Encryption at rest should be used with data in transit encryption and policies that protect accounts, passwords, and encryption keys. When implemented well, the encryption at rest helps organizations to comply with security and privacy standards like HIPAA, PCI-DSS, GDPR, and FIPS, ensuring sensitive data is protected both when it's being transmitted and when it's stored.

Data encryption at rest was introduced in Percona Server for MongoDB 3.6 and is fully compatible with MongoDB's encryption interface. Percona Server for MongoDB supports the following Key Management System (KMS) integrations:

* [HashiCorp Vault](vault.md)
* [Key Management Interoperability Protocol (KMIP) Servers](kmip.md)

## Workflow

!!! important

    You can only enable data at rest encryption and provide all encryption settings on an empty database, when you start the mongod instance for the first time. You cannot enable or disable encryption while the Percona Server for MongoDB server is already running and / or has some data. Nor can you change the effective encryption mode by simply restarting the server. Every time you restart the server, the encryption settings must be the same.

Each node of Percona Server for MongoDB generates a random, individual key for every database. It encrypts every database with an individual key and puts those keys into the special, so-called key database. Then each node of Percona Server for MongoDB randomly generates a unique master encryption key and encrypts the key database with this key. 

Thus, two types of keys are used for data at rest encryption:

* Database keys to encrypt data. They are stored internally, near the data that they encrypt.

* The master key to encrypt database keys. It is kept separately from the data and database keys and requires external management.

To manage the master encryption key, use one of the supported key management options:

* Integration with an external key server (recommended). Percona Server for MongoDB is [integrated with HashiCorp Vault](vault.md) for this purpose and supports the secure transfer of keys using [Key Management Interoperability Protocol (KMIP)](kmip.md).

* [Local key management using a keyfile](keyfile.md).

Note that you can use only one of the key management options at a time. However, you can switch from one management option to another (e.g. from a keyfile to HashiCorp Vault). Refer to [Migrating from Key File Encryption to HashiCorp Vault Encryption](encryption-mode-switch.md) section for details.

## Important configuration options

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

## Encryption of rollback files 

Percona Server for MongoDB encrypts rollback files when data at rest encryption is enabled. To inspect the contents of these files, use **perconadecrypt**. This is a tool that you run from the command line as follows:

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


--8<-- "encryption-status.md"

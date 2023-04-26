# Using the Key Management Interoperability Protocol (KMIP)

!!! admonition "Version added: 5.0.7-6"

Percona Server for MongoDB adds support for secure transfer of keys using the [OASIS Key Management Interoperability Protocol (KMIP)](https://docs.oasis-open.org/kmip/kmip-spec/v2.0/os/kmip-spec-v2.0-os.html). The KMIP implementation was tested with the [PyKMIP server](https://pykmip.readthedocs.io/en/latest/server.html) and the [HashiCorp Vault Enterprise KMIP Secrets Engine](https://www.vaultproject.io/docs/secrets/kmip).

KMIP enables the communication between key management systems and the database server. KMIP provides the following benefits:

* Streamlines encryption key management
* Eliminates redundant key management processes

Starting with version 5.0.9-8, you can specify multiple KMIP servers for failover. On startup, Percona Server for MongoDB connects to the servers in the order listed and selects the one with which the connection is successful.

Starting with version 5.0.11-10, the `kmipKeyIdentifier` option is no longer mandatory. When left blank, the database server creates a key on the KMIP server and uses that for encryption. When you specify the identifier, the key with such an ID must exist on the key storage.

!!! note

    Starting with version 5.0.17-14, the master key is stored in a raw-byte format. If you set up Percona Server for MongoDB 5.0.17-14 with data-at-rest encryption using KMIP and wish to downgrade to some previous version, this downgrade is not possible via binary replacement. Consider using the [logical backup and restore via Percona Backup for MongoDB](https://docs.percona.com/percona-backup-mongodb/usage/start-backup.html) for this purpose.

## KMIP parameters

| Option            | Type    | Description    |
| ----------------- | ------- | -------------- |
|`--kmipServerName` | string  | The hostname or IP address of the KMIP server. As of version 4.2.21-21, multiple KMIP servers are supported as the comma-separated list, e.g. `kmip1.example.com,kmip2.example.com`|
| `--kmipPort`      | number  | The port used to communicate with the KMIP server. When undefined, the default port `5696` will be used|
| `--kmipServerCAFile`| string| The path to the CA certificate file. CA file is used to validate secure client connection to the KMIP server|
| `--kmipClientCertificateFile`| string| The path to the PEM file with the KMIP client private key and the certificate chain. The database server uses this PEM file to authenticate the KMIP server|
| `--kmipKeyIdentifier`| string| Optional starting with version 5.0.11-10. The identifier of the KMIP key. If the key does not exist, the database server creates a key on the KMIP server with the specified identifier. When you specify the identifier, the key with such an ID must exist on the key storage. You can only use this setting for the first time you enable encryption.|
| `--kmipRotateMasterKey`| boolean| Controls master keys rotation. When enabled, generates the new master key version and re-encrypts the keystore. Available as of version 5.0.8-7. Requires the unique `--kmipKeyIdentifier` for every `mongod` node. |
| `--kmipClientCertificatePassword`| string| The password for the KMIP client private key or certificate. Use this parameter only if the KMIP client private key or certificate is encrypted. Available starting with version 5.0.9-8.|

# Key rotation

Starting with release 5.0.8-7, the support for [master key rotation](https://www.mongodb.com/docs/manual/tutorial/rotate-encryption-key/#kmip-master-key-rotation) is added. This enables users to comply with data security regulations when using KMIP.

# Configuration

### Considerations

Make sure you have obtained the root certificate, and the keypair for the KMIP server and the `mongod` client. For testing purposes you can use the [OpenSSL](https://www.openssl.org/) to issue self-signed certificates. For production use we recommend you use the valid certificates issued by the key management appliance.

To enable data-at-rest encryption in Percona Server for MongoDB using KMIP, edit the `/etc/mongod.conf` configuration file as follows:

```yaml
security:
  enableEncryption: true
  kmip:
    serverName: <kmip_server_name>
    port: <kmip_port>
    clientCertificateFile: </path/client_certificate.pem>
    clientKeyFile: </path/client_key.pem>
    serverCAFile: </path/ca.pem>
    keyIdentifier: <key_name>
```

Alternatively, you can start Percona Server for MongoDB using the command line as follows:

```{.bash data-prompt="$"}
$ mongod --enableEncryption \
  --kmipServerName <kmip_servername> \
  --kmipPort <kmip_port> \
  --kmipServerCAFile <path_to_ca_file> \
  --kmipClientCertificateFile <path_to_client_certificate> \
  --kmipClientKeyFile <path_to_client_private_key> \
  --kmipKeyIdentifier <kmip_identifier>
```

# Minor upgrade of Percona Server for MongoDB to version 5.0.11-10 and higher

With the `kmipKeyIdentifier` option becoming optional in version 5.0.11-10, the standard upgrade procedure doesn’t work if you are upgrading from version 5.0.10-9 and earlier.

For Percona Server for MongoDB 5.0.13-11 and higher, follow the standard [upgrade procedure](install/upgrade-from-mongodb.md)

This section provides upgrade instructions from Percona Server for MongoDB 5.0.10-9 or lower to Percona Server for MongoDB version 5.0.11-10 and higher.

For a single-node deployment, use the `mongodump` / `mongorestore` tools to make a backup before the update and to restore from it after binaries are updated.

For replica sets, data must be re-encrypted with the **new** key during the upgrade. Go through the [encrypting existing data steps](https://www.mongodb.com/docs/v5.0/tutorial/configure-encryption/#std-label-encrypt-existing-data)  but perform the [minor upgrade](install/upgrade-from-mongodb.md#minor-upgrade) between steps 1 and 2 to replace the `mongod` binary.

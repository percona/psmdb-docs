# Using the Key Management Interoperability Protocol (KMIP)

Percona Server for MongoDB adds support for secure transfer of keys using the [OASIS Key Management Interoperability Protocol (KMIP)](https://docs.oasis-open.org/kmip/kmip-spec/v2.0/os/kmip-spec-v2.0-os.html). The KMIP implementation was tested with the [PyKMIP server](https://pykmip.readthedocs.io/en/latest/server.html) and the [HashiCorp Vault Enterprise KMIP Secrets Engine](https://www.vaultproject.io/docs/secrets/kmip).

KMIP enables the communication between key management systems and the database server. KMIP provides the following benefits:

* Streamlines encryption key management
* Eliminates redundant key management processes

Starting with version 4.2.21-21, you can specify multiple KMIP servers for failover. On startup, Percona Server for MongoDB connects to the servers in the order listed and selects the one with which the connection is successful.

Starting with version 4.2.22-22, the `kmipKeyIdentifier` option is no longer mandatory. When left blank, the database server creates a key on the KMIP server and uses that for encryption. When you specify the identifier, the key with such an ID must exist on the key storage.

## KMIP parameters

| Command line     | Configuration file       | Type  | Description    |
| ---------------- | ------------------------ | ----- | ---------------|
| kmipServerName   | security.kmip.<br>serverName | string | The hostname or IP address of the KMIP server. As of version 4.2.21-21, multiple KMIP servers are supported as the comma-separated list, e.g. `kmip1.example.com,kmip2.example.com`|
| kmipPort         | security.kmip.port  | number  | The port used to communicate with the KMIP server. When undefined, the default port `5696` will be used|
| kmipServerCAFile | security.kmip.<br>serverCAFile | string | The path to the certificate of the root authority that issued the certificate for the KMIP server. Required only if the root certificate is not trusted by default on the machine the database server works on.|
| kmipClientCertificateFile | security.kmip.<br>clientCertificateFile | string| The path to the PEM file with the KMIP client private key and the certificate chain. The database server uses this PEM file to authenticate the KMIP server|
| kmipKeyIdentifier | security.kmip.<br>keyIdentifier | string| Optional starting with version 4.2.22-22. The identifier of the KMIP key. If not specified, the database server creates a key on the KMIP server and saves its identifier internally for future use. When you specify the identifier, the key with such an ID must exist on the key storage. You can only use this setting for the first time you enable encryption|
| kmipRotateMasterKey | security.kmip.<br>rotateMasterKey | boolean| Controls master keys rotation. When enabled, generates the new master key version and re-encrypts the keystore. Available as of version 4.2.20-20. Requires the unique `--kmipKeyIdentifier` for every `mongod` node |
| kmipClientCertificatePassword | security.kmip.<br>clientCertificatePassword | string| The password for the KMIP client private key or certificate. Use this parameter only if the KMIP client private key or certificate is encrypted. Available starting with version 4.2.21-21.|

## Key rotation

Starting with version 4.2.20-20, the support for [master key rotation](https://www.mongodb.com/docs/manual/tutorial/rotate-encryption-key/#kmip-master-key-rotation) is added. This enables users to comply with data security regulations when using KMIP.

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
  --kmipKeyIdentifier <kmip_identifier>
```

# Minor upgrade of Percona Server for MongoDB from 4.2.21-21 and earlier to version 4.2.22-22 and higher

With the `kmipKeyIdentifier` option becoming optional in version 4.2.22-22, the standard upgrade procedure doesn’t work if you are upgrading from version 4.2.21-21 and earlier.

For Percona Server for MongoDB 4.2.23 and higher, follow the standard [upgrade procedure](install/upgrade-from-mongodb.md).

This section provides upgrade instructions from Percona Server for MongoDB 4.2.21-21 or lower to Percona Server for MongoDB to version 4.2.22-22 and higher.

For a single-node deployment, use the `mongodump` / `mongorestore` tools to make a backup before the update and to restore from it after binaries are updated.

For replica sets, data must be re-encrypted with the **new** key during the upgrade. Go through the [encrypting existing data steps](https://www.mongodb.com/docs/v4.4/tutorial/configure-encryption/#std-label-encrypt-existing-data)  but perform the [minor upgrade](install/upgrade-from-mongodb.md#minor-upgrade) between steps 1 and 2 to replace the `mongod` binary.

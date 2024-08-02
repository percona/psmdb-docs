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

| Configuration file | {{ optionlink('security.kmip.serverName') }}|
|--------------------| ---------------|
| **Command line**       | `kmipServerName` |
| **Type**               | string | 
| **Description**        | The hostname or IP address of the KMIP server. As of version 4.2.21-21, multiple KMIP servers are supported as the comma-separated list, e.g. `kmip1.example.com,kmip2.example.com` | 

| Configuration file | {{ optionlink('security.kmip.port')}}  |
|--------------------| --------------------|
| **Command line**        | `kmipPort`      |
| **Type**               | number | 
| **Description**        | The port used to communicate with the KMIP server. When undefined, the default port `5696` is used|

| Configuration file  | {{ optionlink('security.kmip.serverCAFile')}} | 
|--------------------| --------------------|
| **Command line**        | `kmipServerCAFile`      |
| **Type**               | string |
| **Description**        | The path to the certificate of the root authority that issued the certificate for the KMIP server. Required only if the root certificate is not trusted by default on the machine the database server works on.|

| Configuration file  | {{ optionlink('security.kmip.clientCertificateFile')}} |
|--------------------| --------------------|
| **Command line**        | `kmipClientCertificateFile`      | 
| **Type**                | string |
| **Description**         | The path to the PEM file with the KMIP client private key and the certificate chain. The database server uses this PEM file to authenticate the KMIP server|

| Configuration file  | {{ optionlink('security.kmip.keyIdentifier')}} |
|-------------------- | --------------------|
| **Command line**    | `kmipKeyIdentifier` |
| **Type**                | string |
| **Description**         | Optional starting with version 5.0.11-10. The identifier of the KMIP key. If not specified, the database server creates a key on the KMIP server and saves its identifier internally for future use. When you specify the identifier, the key with such an ID must exist on the key storage. You can only use this setting for the first time you enable encryption.|

| Configuration file  | {{ optionlink('security.kmip.rotateMasterKey')}} |
|-------------------- | --------------------|
| **Command line**    | `kmipRotateMasterKey` | 
| **Type**            | boolean | 
| **Description**     | Controls master keys rotation. When enabled, generates the new master key version and re-encrypts the keystore. Available as of version 5.0.8-7. |

| Configuration file  | {{ optionlink('security.kmip.clientCertificatePassword')}}| 
|-------------------- | --------------------|
| **Command line**    | `kmipClientCertificatePassword` |
| **Type**            | string|
| **Description**     | The password for the KMIP client private key or certificate. Use this parameter only if the KMIP client private key or certificate is encrypted. Available starting with version 5.0.9-8.|

| Configuration file  | {{ optionlink('security.kmip.connectRetries')}}|
|-------------------- | --------------------|
| **Command line**    | `kmipConnectRetries` | 
| **Type**            | int | 
| **Description**     | Defines how many times to retry the initial connection to the KMIP server. The max number of connection attempts equals to `connectRetries + 1`. Default: 0. The option accepts values greater than zero. <br><br>Use it together with the `connectTimeoutMS` parameter to control how long `mongod` waits for the response before making the next retry.|

| Configuration file  | {{optionlink('security.kmip.connectTimeoutMS')}}|
|-------------------- | --------------------|
| **Command line**    | `kmipConnectTimeoutMS`|
| **Type**            | int|
| **Description**     | The time to wait for the response from the KMIP server. Min value: 1000. Default: 5000. <br><br>If the `connectRetries` setting is specified, the `mongod` waits up to the value specified with `connectTimeoutMS` for each retry.|

| Configuration file  | {{optionlink('security.kmip.activateKeys')}}|
|-------------------- | --------------------|
| **Command line**    | `kmipActivateKeys`|
| **Type**            | boolean|
| **Description**     | Determines the transition of the newly created master key to the Active state. Enabled by default. Available starting with version 5.0.28-24.|

| Configuration file  | {{optionlink('security.kmip.keyStatePollingSeconds')}}|
|-------------------- | --------------------|
| **Command line**    | `kmipKeyStatePollingSeconds`|
| **Type**            | int|
| **Description**     | Sets the period in seconds to check the state of the master encryption key. Default: 900. If the master encryption key for a node is not in the Active state, the node logs the error and shuts down. Available starting with version 5.0.28-24.|


## Key rotation

Starting with version 5.0.8-7, the support for [master key rotation](https://www.mongodb.com/docs/manual/tutorial/rotate-encryption-key/#kmip-master-key-rotation) is added. This enables users to comply with data security regulations when using KMIP.

## Key state polling

When a Percona Server for MongoDB node generates a new master encryption key, it automatically registers the key on the KMIP server with the `Pre-Active` state. Starting with version 5.0.28-24, Percona Server for MongoDB automatically activates the master encryption key and checks (polls) its state within a defined period. If a master encryption key for a node is not in the `Active` state, the node reports an error and shuts down. This process helps security engineers identify the nodes that require out-of-schedule master key rotation.

The `security.kmip.activateKeys` configuration file option determines the transition of the master encryption key to the `Active` state at startup. This option is enabled by default. The `security.kmip.keyStatePollingSeconds` configuration file option sets the period, in seconds, to poll the master key state. 

Percona Server for MongoDB 5.0.28 and subsequent versions tolerate already existing `Pre-Active` master keys as follows: if at startup Percona Server for MongoDB detects that the data directory is encrypted with an existing master key in the `Pre-Active` state, it logs a warning and continues to operate as usual. In that case, Percona Server for MongoDB does not do periodic key state polling regardless the value specified for the `kmipKeyStatePollingSeconds` option. 

An active master encryption key is mandatory since Percona Server for MongoDB 8.0.0. To get an active master encryption key, you can either rotate it or activate it manually by setting the `security.kmip.activateKeys` to true. 

The master key state polling functionality is particularly useful in cluster deployments with hundreds of nodes. If some master keys are compromised, security engineers change their state from `Active` so that the nodes encrypted with these keys identify themselves. This approach allows the security engineers to rotate master keys only on the affected nodes instead of the entire cluster, thus reducing the mean time to resolve (MTTR) compromised encryption key incidents.

!!! admonition "See also"

    Percona Blog: [Improve the Security of a Percona Server for MongoDB Deployment with KMIP Key State Polling]() by Konstantin Trushin.


## Configuration

### Considerations

Make sure you have obtained the root certificate, and the keypair for the KMIP server and the `mongod` client. For testing purposes you can use the [OpenSSL](https://www.openssl.org/) to issue self-signed certificates. For production use we recommend you use the valid certificates issued by the key management appliance.

### Procedure

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
    activateKeys: true
    keyStatePollingSeconds: 900
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
  --kmipActivateKeys true \
  --kmipKeyStatePollingSeconds 900
```

# Minor upgrade of Percona Server for MongoDB to version 5.0.11-10 and higher

With the `kmipKeyIdentifier` option becoming optional in version 5.0.11-10, the standard upgrade procedure doesn’t work if you are upgrading from version 5.0.10-9 and earlier.

For Percona Server for MongoDB 5.0.13-11 and higher, follow the standard [upgrade procedure](install/upgrade-from-mongodb.md)

This section provides upgrade instructions from Percona Server for MongoDB 5.0.10-9 or lower to Percona Server for MongoDB version 5.0.11-10 and higher.

For a single-node deployment, use the `mongodump` / `mongorestore` tools to make a backup before the update and to restore from it after binaries are updated.

For replica sets, data must be re-encrypted with the **new** key during the upgrade. Go through the [encrypting existing data steps](https://www.mongodb.com/docs/v5.0/tutorial/configure-encryption/#std-label-encrypt-existing-data)  but perform the [minor upgrade](install/upgrade-from-mongodb.md#minor-upgrade) between steps 1 and 2 to replace the `mongod` binary.

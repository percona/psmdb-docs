# Using the Key Management Interoperability Protocol (KMIP)

Percona Server for MongoDB adds support for secure transfer of keys using the [OASIS Key Management Interoperability Protocol (KMIP)](https://docs.oasis-open.org/kmip/kmip-spec/v2.0/os/kmip-spec-v2.0-os.html). The KMIP implementation was tested with the [PyKMIP server](https://pykmip.readthedocs.io/en/latest/server.html) and the [HashiCorp Vault Enterprise KMIP Secrets Engine](https://www.vaultproject.io/docs/secrets/kmip).

KMIP enables the communication between key management systems and the database server. KMIP provides the following benefits:

* Streamlines encryption key management
* Eliminates redundant key management processes

You can specify multiple KMIP servers for failover. On startup, Percona Server for MongoDB connects to the servers in the order listed and selects the one with which the connection is successful.

The `kmipKeyIdentifier` option is optional and when left blank, the database server creates a key on the KMIP server and uses that for encryption. When you specify the identifier, the key with such an ID must exist on the key storage.


## KMIP parameters

| Configuration file | {{ optionlink('security.kmip.serverName') }}|
|--------------------| ---------------|
| **Command line**       | `kmipServerName` |
| **Type**               | string | 
| **Description**        | The hostname or IP address of the KMIP server. Multiple KMIP servers are supported as the comma-separated list, e.g. `kmip1.example.com,kmip2.example.com` | 

| Configuration file | {{ optionlink('security.kmip.port')}}  |
|--------------------| --------------------|
| **Command line**        | `kmipPort`      |
| **Type**               | number | 
| **Description**        | The port used to communicate with the KMIP server. When undefined, the default port `5696` is used | 

| Configuration file  | {{ optionlink('security.kmip.serverCAFile')}} | 
|--------------------| --------------------|
| **Command line**        | `kmipServerCAFile`      |
| **Type**               | string |
| **Description**        |  The path to the certificate of the root authority that issued the certificate for the KMIP server. Required only if the root certificate is not trusted by default on the machine the database server works on.|

| Configuration file  | {{ optionlink('security.kmip.clientCertificateFile')}} |
|--------------------| --------------------|
| **Command line**        | `kmipClientCertificateFile`      | 
| **Type**                | string |
| **Description**         | The path to the PEM file with the KMIP client private key and the certificate chain. The database server uses this PEM file to authenticate the KMIP server|

| Configuration file  | {{optionlink('security.kmip.keyIdentifier')}}  |
|--------------------| --------------------|
| **Command line**        | `kmipKeyIdentifier`      |
| **Type**                | string |
| **Description**         | Optional. The identifier of the KMIP key. If not specified, the database server creates a key on the KMIP server and saves its identifier internally for future use. When you specify the identifier, the key with such an ID must exist on the key storage. You can only use this setting for the first time you enable encryption.|

| Configuration file  | {{ optionlink('security.kmip.rotateMasterKey')}} |
|--------------------| --------------------|
| **Command line**        | kmipRotateMasterKey      |
| **Type**                | boolean |
| **Description**         | Controls master keys rotation. When enabled, generates the new master key and re-encrypts the keystore.|

| Configuration file  | {{ optionlink('security.kmip.clientCertificatePassword')}} |
|--------------------| --------------------|
| **Command line**        | kmipClientCertificatePassword |
| **Type**                | string |
| **Description**         | The password for the KMIP client private key or certificate. Use this parameter only if the KMIP client private key or certificate is encrypted. |

| Configuration file  | {{ optionlink('security.kmip.connectRetries')}}|
|--------------------| --------------------|
| **Command line**        | kmipConnectRetries      |
| **Type**               | int | 
| **Description**        | Defines how many times to retry the initial connection to the KMIP server. The max number of connection attempts equals to `connectRetries + 1`. Default: 0. The option accepts values greater than zero. <br><br>Use it together with the `connectTimeoutMS` parameter to control how long `mongod` waits for the response before making the next retry.|

| Configuration file  | {{ optionlink('security.kmip.connectTimeoutMS')}} | 
|--------------------| --------------------|
| **Command line**        | kmipConnectTimeoutMS      |
| **Type**               | int | 
| **Description**        | The time to wait for the response from the KMIP server. Min value: 1000. Default: 5000. <br><br>If the `connectRetries` setting is specified, the `mongod` waits up to the value specified with `connectTimeoutMS` for each retry.|
 
## Key rotation

Percona Server for MongoDB supports the [master key rotation](https://www.mongodb.com/docs/manual/tutorial/rotate-encryption-key/#kmip-master-key-rotation). This enables users to comply with data security regulations when using KMIP.

## Configuration

### Considerations

Make sure you have obtained the root certificate, and the keypair for the KMIP server and the `mongod` client. For testing purposes you can use the [OpenSSL](https://www.openssl.org/) to issue self-signed certificates. For production use we recommend you use the valid certificates issued by the key management appliance.

To enable data-at-rest encryption in Percona Server for MongoDB using KMIP, the options are:

=== "Configuration file"

    Edit the `/etc/mongod.conf` configuration file as follows:    

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

=== "Command line" 

    Start Percona Server for MongoDB using the command line as follows:    

    ```{.bash data-prompt="$"}
    $ mongod --enableEncryption \
      --kmipServerName <kmip_servername> \
      --kmipPort <kmip_port> \
      --kmipServerCAFile <path_to_ca_file> \
      --kmipClientCertificateFile <path_to_client_certificate> \
      --kmipKeyIdentifier <kmip_identifier>
    ```


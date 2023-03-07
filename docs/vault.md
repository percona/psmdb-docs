# HashiCorp Vault integration

Percona Server for MongoDB is integrated with HashiCorp Vault. HashiCorp Vault supports different secrets engines. Percona Server for MongoDB only supports the HashiCorp Vault
back end with KV Secrets Engine - Version 2 (API)
with versioning enabled.

!!! admonition "See also"

    Percona Blog: [Using Vault to Store the Master Key for Data at Rest Encryption on Percona Server for MongoDB](https://www.percona.com/blog/2020/04/21/using-vault-to-store-the-master-key-for-data-at-rest-encryption-on-percona-server-for-mongodb/)

    HashiCorp Vault Documentation: [How to configure the KV Engine](https://www.vaultproject.io/api/secret/kv/kv-v2.html)

## HashiCorp Vault Parameters

| Command line         | Configuration file        | Type   | Description  |
| -------------------- | ------------------------- | ------ | ------------ |
| vaultServerName      | security.vault.serverName | string | The IP address of the Vault server|
| vaultPort            | security.vault.port       | int    | The port on the Vault server|
| vaultTokenFile       | security.vault.tokenFile  | string | The path to the vault token file. The token file is used by MongoDB to access HashiCorp Vault. The vault token file consists of the raw vault token and does not include any additional strings or parameters. <br> <br> Example of a vault token file: <br> <br> `s.uTrHtzsZnEE7KyHeA797CkWA`|
| vaultSecret          | security.vault.secret     | string | The path to the Vault secret. The Vault secret path format must be ```<secrets_engine_mount_path>/data/<custom_path>``` <br> <br> where: <br> - ``<secrets_engine_mount_path>`` is the path to the Key/Value Secrets Engine v2; <br> - ``data`` is the mandatory path prefix required by Version 2 API; <br> - ``<custom_path>`` is the path to the specific secret. <br> <br> Example: `secret_v2/data/psmdb-test/rs1-27017` <br><br> Starting with version [6.0.5-4](release_notes/6.0.5-4.md), a distinct Vault secret path for every replica set member is no longer mandatory. In earlier versions, it is recommended to use different secret paths for every database node in the entire deployment to avoid issues during the master key rotation.|
| vaultSecretVersion | security.vault.<br>secretVersion | unsigned long | (Optional) The version of the Vault secret to use | 
| vaultRotateMasterKey | security.vault.<br>rotateMasterKey| switch | When enabled, rotates the master key and exits |
| vaultServerCAFile    | security.vault.<br>serverCAFile | string | The path to the TLS certificate file |
| vaultDisableTLSForTesting | security.vault.<br>disableTLSForTesting | switch | Disables secure connection to Vault using SSL/TLS client certificates|

**Config file example**

```yaml
security:
  enableEncryption: true
  vault:
    serverName: 127.0.0.1
    port: 8200
    tokenFile: /home/user/path/token
    secret: secret/data/hello
```

During the first run of the Percona Server for MongoDB, the process generates a secure key and writes the key to the vault.

During the subsequent start, the server tries to read the master key from the vault. If the configured secret does not exist, vault responds with HTTP 404 error.

## Namespaces

Namespaces are isolated environments in Vault that allow for separate secret key and policy management.

You can use Vault namespaces with Percona Server for MongoDB. Specify the namespace(s) for the `security.vault.secret` option value as follows:

```{.bash data-prompt="$"}
<namespace>/secret/data/<secret_path>
```

For example, the path to secret keys for namespace `test` on  the secrets engine `secret` will be `test/secret/<my_secret_path>`.

### Targeting a namespace in Vault configuration

You have the following options of how to target a particular namespace when configuring Vault:

1. Set the VAULT_NAMESPACE environment variable so that all subsequent commands are executed against that namespace. Use the following command to set the environment variable for the namespace `test`:

   ```{.bash data-prompt="$"}
   $ export VAULT_NAMESPACE=test
   ```
2. Provide the namespace with the `-namespace` flag in commands

!!! admonition "See also"

    HashiCorp Vault Documentation:

    * [Namespaces](https://www.vaultproject.io/docs/enterprise/namespaces)

    * [Secure Multi-Tenancy with Namespaces](https://learn.hashicorp.com/tutorials/vault/namespaces)

## Key rotation

Key rotation is replacing the old master key with a new one. This process helps to comply with regulatory requirements.

To rotate the keys for a single `mongod` instance, do the following:

1. Stop the `mongod` process

2. Add `--vaultRotateMasterKey` option via the command line or `security.vault.rotateMasterKey` to the config file.

3. Run the `mongod` process with the selected option, the process will perform the key rotation and exit.

4. Remove the selected option from the startup command or the config file.

5. Start `mongod` again.

Rotating the master key process also re-encrypts the keystore using the new master key. The new master key is stored in the vault. The entire dataset is not re-encrypted.

### Key rotation in replica sets

Starting with version [6.0.5-4](release_notes/6.0.5-4.md), you can store the master key at the same path on every replica set member in your entire deployment. Vault assigns different versions to the master keys stored at the same path. The path and the version serve as the unique identifier of a master key. The `mongod` server stores that identifier and uses it to retrieve the correct master key from the Vault server during the restart.  

In versions 6.0.4-3 and earlier, every `mongod` node in a replica set in your entire deployment must have a distinct path to the master keys on a Vault server. 

The key rotation steps are the following:

1. Rotate the master key for the secondary nodes one by one.
2. Step down the primary and wait for another primary to be elected.
3. Rotate the master key for the previous primary node.


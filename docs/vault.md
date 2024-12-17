# HashiCorp Vault integration

Percona Server for MongoDB is integrated with HashiCorp Vault. HashiCorp Vault supports different secrets engines. Percona Server for MongoDB only supports the HashiCorp Vault
back end with KV Secrets Engine - Version 2 (API)
with versioning enabled.

!!! admonition "See also"

    Percona Blog: [Using Vault to Store the Master Key for Data at Rest Encryption on Percona Server for MongoDB](https://www.percona.com/blog/2020/04/21/using-vault-to-store-the-master-key-for-data-at-rest-encryption-on-percona-server-for-mongodb/)

    HashiCorp Vault Documentation: [How to configure the KV Engine](https://www.vaultproject.io/api/secret/kv/kv-v2.html)



## HashiCorp Vault parameters

| Command line         | Configuration file        | Type   | Description  |
| -------------------- | ------------------------- | ------ | ------------ |
| vaultServerName      | security.vault.serverName | string | The IP address of the Vault server|
| vaultPort            | security.vault.port       | int    | The port on the Vault server|
| vaultTokenFile       | security.vault.tokenFile  | string | The path to the vault token file. The token file is used by MongoDB to access HashiCorp Vault. The vault token file consists of the raw Vault token and does not include any additional strings or parameters. <br> <br> Example of a Vault token file: <br> <br> `s.uTrHtzsZnEE7KyHeA797CkWA`|
| vaultSecret          | security.vault.secret     | string | The path to the Vault secret. The Vault secret path format must be ```<secrets_engine_mount_path>/data/<custom_path>``` <br> <br> where: <br> - ``<secrets_engine_mount_path>`` is the path to the Key/Value Secrets Engine v2; <br> - ``data`` is the mandatory path prefix required by Version 2 API; <br> - ``<custom_path>`` is the path to the specific secret. <br> <br> Example: `secret_v2/data/psmdb-test/rs1-27017` <br><br> A distinct Vault secret path for every replica set member is not mandatory. In previous versions, it is recommended to use different secret paths for every database node in the entire deployment to avoid issues during the master key rotation.|
| vaultSecretVersion | security.vault.<br>secretVersion | unsigned long | (Optional) The version of the Vault secret to use | 
| vaultRotateMasterKey | security.vault.<br>rotateMasterKey| switch | When enabled, rotates the master key and exits |
| vaultServerCAFile    | security.vault.<br>serverCAFile | string | The path to the TLS certificate file |
| vaultDisableTLSForTesting | security.vault.<br>disableTLSForTesting | switch | Disables secure connection to Vault using SSL/TLS client certificates|
| vaultCheckMaxVersions  | security.vault.<br>checkMaxVersions| boolean | Verifies that the current number of secret versions has not reached the maximum, defined by the `max_versions` parameter for the secret or the secrets engine on the Vault server. If the number of versions has reached the maximum, the server logs an error and exits. Enabled by default. Available starting with version 8.0.1-1.|


### Config file example

```yaml
security:
  enableEncryption: true
  vault:
    serverName: 127.0.0.1
    port: 8200
    tokenFile: /home/user/path/token
    secret: secret/data/hello
```

#### Vault access policy configuration

Percona Server for MongoDB checks the number of the secrets on the Vault server before adding a new one thus [preventing the loss of the old master key](#master-key-loss-prevention). For these checks, Percona Server for MongoDB requires read permissions for the secret’s metadata and the secrets engine configuration. You configure these permissions within the access policy on the Vault server.

Find the sample policy configuration below:

```json
path "secret/data/*" {
  capabilities = ["create","read","update","delete"]
}
path "secret/metadata/*" {
  capabilities = ["read"]
}
path "secret/config" {
  capabilities = ["read"]
}
```

During the first run of the Percona Server for MongoDB, the process generates a new random master encryption key. Then, it wraps it into a secret and puts the latter on a Vault server at the configured path. Vault increments the value of the `current_version`, associates the resulting value with a new secret, and returns the version. Percona Server for MongoDB then saves the full path and the version in the metadata and uses them later to get the key from the Vault server.

During the subsequent start, the server tries to read the master key from the Vault. If the configured secret does not exist, Vault responds with the HTTP 404 error.

## Namespaces

Namespaces are isolated environments in Vault that allow for separate secret key and policy management.

You can use Vault namespaces with Percona Server for MongoDB. Specify the namespace(s) for the `security.vault.secret` option value as follows:

```{.bash data-prompt="$"}
<namespace>/secret/data/<secret_path>
```

For example, the path to secret keys for namespace `test` on  the secrets engine `secret` will be `test/secret/<my_secret_path>`.

### Targeting a namespace in Vault configuration

You have the following options of how to target a particular namespace when configuring Vault:

1. Set the `VAULT_NAMESPACE` environment variable so that all subsequent commands are executed against that namespace. Use the following command to set the environment variable for the namespace `test`:

   ```{.bash data-prompt="$"}
   $ export VAULT_NAMESPACE=test
   ```
2. Provide the namespace with the `--namespace` flag in commands

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

Rotating the master key process also re-encrypts the keystore using the new master key. The new master key is stored in the Vault. The entire dataset is not re-encrypted.

### Key rotation in replica sets

Starting with version [6.0.5-4](https://docs.percona.com/percona-server-for-mongodb/6.0/release_notes/6.0.5-4.md), you can store the master key at the same path on every replica set member in your entire deployment. Vault assigns different versions to the master keys stored at the same path. The path and the version serve as the unique identifier of a master key. The `mongod` server stores that identifier and uses it to retrieve the correct master key from the Vault server during the restart.

The key rotation steps are the following:

1. Rotate the master key for the secondary nodes one by one.
2. Step down the primary and wait for another primary to be elected.
3. Rotate the master key for the previous primary node.

### Master key loss prevention

Percona Server for MongoDB checks if the number of secret versions has reached the maximum (10 by default) before adding a new master key to the Vault server as a versioned secret. You configure this number using the `max_versions` parameter on the Vault server.

If the number of secrets reaches the maximum, Percona Server for MongoDB logs an error and exits. This prevents the Vault server from dropping the oldest secret version and the encryption key it stores.

To continue, increase the maximum versions for the secret or the entire secrets engine on the Vault server, then restart Percona Server for MongoDB. To check the number of secrets on the Vault server, ensure Percona Server for MongoDB has [read permissions for the secret’s metadata and the secrets engine configuration](#vault-access-policy-configuration).

## Upgrade considerations

If you upgraded to Percona Server for MongoDB 8.0.x from version 7.0.14-9 or earlier, where there is no check for the number of secrets versions on the Vault server, configure the read permissions for Percona Server for MongoDB within the access policy on the Vault server after the upgrade. 

See [the policy configuration example](#vault-access-policy-configuration).
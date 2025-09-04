# Use OpenBao for data-at-rest encryption

[OpenBao](https://openbao.org/) is an open-source alternative to HashiCorp Vault. Percona Server for MongoDB is integrated with OpenBao for encryption key management and supports only OpenBao back end with KV Secrets Engine - Version 2 (API) with versioning enabled. 

## Assumptions

1. We assume that you have OpenBao up and running. Refer to [OpenBao](https://openbao.org/docs/install/) documentation for installation instructions. 
2. For secure communication with OpenBao, [it's recommended to use TLS](https://openbao.org/docs/configuration/ui/#note-on-tls). 
3. You have an empty Percona Server for MongoDB deployment. 

## OpenBao setup

OpenBao setup is similar to that of HashiCorp Vault. It consists of the following steps:

1. Initialize OpenBao server. As a result, OpenBao generates the root token and the unseal key.

    ```{.bash data-prompt="$"}
    $ bao operator init
    ```

2. OpenBao is started in a sealed state. In this state OpenBao can access the storage but it cannot decrypt data. In order to use OpenBao, you need to unseal it using the unseal key.

    ```{.bash data-prompt="$"}
    $ bao operator unseal <your-unseal-key>
    ```

3. Next, authenticate in OpenBao using the root token.

    ```{.bash data-prompt="$"}
    $ bao login <root-token>
    ```

4. Enable the KV Secrets Engine – Version 2. By default, the secrets engine is enabled at the `secrets/` path. You can specify your own path using the `-path` flag

    ```{.bash data-prompt="$"}
    $ bao secrets enable --version=2 -path=secret kv
    ```

5. Create the access policy and grant Percona Server for MongoDB read permissions for the secret's metadata and the secrets engine configuration. Percona Server needs it to check the number of secrets on the OpenBao before it generates a new key. 

   * Create an access policy file:

     ```{.bash data-prompt="$"}
     $ cat <<EOF > psmdb-access.hcl
     path "secret/data/*" {
       capabilities = ["create","read","update","delete"]
     }
     path "secret/metadata/*" {
       capabilities = ["read"]
     }
     path "secret/config" {
       capabilities = ["read"]
     }
     EOF
     ```

   * Upload the access policy to OpenBao:

      ```{.bash data-prompt="$"}
      $ bao policy write psmdb-policy psmdb-access.hcl
      ```

6. Create an access token that Percona Server for MongoDB will use. You need to create an access token for every instance of Percona Server for MongoDB in your deployment.

    ```{.bash data-prompt="$"}
    $ bao token create -policy=psmdb-policy
    ```

7. Export an access token to a file and restrict access to it for `mongod` user:

    * Create a directory where you will store the token and SSL certificates if you [configured OpenBao with TLS](https://openbao.org/docs/auth/cert/#configuration)

       ```{.bash data-prompt="$"}
       $ sudo mkdir -p /etc/openbao
       ```

    * Export the token into the token file. For TLS communication, copy the `.crt` file from OpenBao.

       ```{.bash data-prompt="$"}
       $ echo "your-access-token-here" > /etc/openbao/token
       ```

    * Restrict access to the token and certificate files for the `mongod` user:
       
       ```{.bash data-prompt="$"}
       $ sudo chmod 400 -p /etc/openbao/token
       $ sudo chown mongod:mongod /etc/openbao/token
       ```

!!! admonition "See also"

    To learn more about OpenBao configuration, see the following resources:

    * [How to configure KV secrets engine - version 2](https://openbao.org/docs/secrets/kv/kv-v2/)
    * [Master key loss prevention](vault.md#master-key-loss-prevention)

## Percona Server for MongoDB configuration

Percona Server for MongoDB configuration for OpenBao is the same as for HashCorp Vault. Refer to the [HashiCorp Vault parameters](vault.md#hashicorp-vault-parameters) for the description of available configuration options.

To enable data-at-rest encryption in Percona Server for MongoDB, you need the following information:

* OpenBao URL and port 
* OpenBao secrets engine mount path
* Path to the access token

=== ":octicons-file-code-24: Configuration file"    

    1. Edit the `/etc/mongod.conf` configuration file and specify the following configuration:    

        ```yaml
        security:
          enableEncryption: true
          vault:
            serverName: 127.0.0.1
            port: 8200
            tokenFile: /etc/openbao/token
            secret: secret/data/
        ```

    2. Start Percona Server for MongoDB:

        ```{.bash data-prompt="$"}
        $ sudo systemctl start
        ```

=== ":material-console: Command line"

    Start Percona Server for MongoDB with the following parameters:

    ```{.bash data-prompt="$"}
    $ mongod --enableEncryption --vaultServerName 127.0.0.1 --vaultPort 8200 --vaultTokenFile /etc/openbao/token --vaultSecret secret/data/ --vaultDisableTLSForTesting
    ```
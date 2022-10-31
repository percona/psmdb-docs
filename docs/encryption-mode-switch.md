# Migrating from Key File Encryption to HashiCorp Vault Encryption

The steps below describe how to migrate from the key file encryption to using  HashiCorp Vault.

!!! note 

    This is a simple guideline and it should be used for testing purposes only. We recommend to use Percona Consulting Services to assist you with migration in production environment.

### Assumptions

We assume that you have installed and configured the vault server and enabled the KV Secrets Engine as the secrets storage for it.


1. Stop `mongod`.

```{.bash data-prompt="$"}
$ sudo systemctl stop mongod
```

2. Insert the key from keyfile into the HashiCorp Vault server to the desired secret path.

   * Retrieve the key value from the keyfile

       ```{.bash data-prompt="$"}
       $ sudo cat /data/key/mongodb.key
       d0JTFcePmvROyLXwCbAH8fmiP/ZRm0nYbeJDMGaI7Zw=
       ```

   * Insert the key into vault

      ```{.bash data-prompt="$"}
      $ vault kv put secret/dc/psmongodb1 value=d0JTFcePmvROyLXwCbAH8fmiP/ZRm0nYbeJDMGaI7Zw=
      ```

!!! note 

    Vault KV Secrets Engine uses different read and write secrets paths. To insert data to vault, specify the secret path without the `data/` prefix.


3. Edit the configuration file to provision the HashiCorp Vault configuration options instead of the key file encryption options.

    ```yaml
    security:
       enableEncryption: true
       vault:
          serverName: 10.0.2.15
          port: 8200
          secret: secret/data/dc/psmongodb1
          tokenFile: /etc/mongodb/token
          serverCAFile: /etc/mongodb/vault.crt
    ```


4. Start the `mongod` service

    ```{.bash data-prompt="$"}
    $ sudo systemctl start mongod
    ```

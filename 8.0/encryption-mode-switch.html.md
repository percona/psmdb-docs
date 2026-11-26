> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server-for-mongodb/8.0/llms.txt).

# Migrate from key file encryption to HashiCorp Vault / OpenBao encryption

The steps below describe how to migrate from the key file encryption to using HashiCorp Vault. This guide also applies to migration to [OpenBao](https://openbao.org/) - an open-source alternative to HashiCorp Vault.

Note

This is a sample guideline and it should be used for testing purposes only. We recommend to contact [Percona Consulting Services](https://www.percona.com/services/consulting) to assist you with migration in production environment.

### Assumptions

We assume that you have installed and configured the vault server and enabled the KV Secrets Engine as the secrets storage for it.

1. Stop `mongod`.

   ```bash
   sudo systemctl stop mongod
   ```

1. Insert the key from keyfile into the HashiCorp Vault server to the desired secret path.

   - Retrieve the key value from the keyfile

   ```bash
   sudo cat /data/key/mongodb.key
   d0JTFcePmvROyLXwCbAH8fmiP/ZRm0nYbeJDMGaI7Zw=
   ```

   - Insert the key into vault

   ```bash
   vault kv put secret/dc/psmongodb1 value=d0JTFcePmvROyLXwCbAH8fmiP/ZRm0nYbeJDMGaI7Zw=
   ```

   Note

   Vault KV Secrets Engine uses different read and write secrets paths. To insert data to Vault, specify the secret path without the `data/` prefix.

1. Edit the configuration file to provision the HashiCorp Vault configuration options instead of the key file encryption options.

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

1. Start the `mongod` service

   ```bash
   sudo systemctl start mongod
   ```

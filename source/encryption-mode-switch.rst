.. _psmdb.encryption-mode-switch:

Migrating from Key File Encryption to |vault| Encryption
========================================================

The steps below describe how to migrate from the key file encryption to using  |vault|.

.. note::

   This is a simple guideline and it should be used for testing purposes only. We recommend to use Percona Consulting Services to assist you with migration in production environment.

.. rubric:: Assumptions

We assume that you have installed and configured the vault server and enabled the KV Secrets Engine as the secrets storage for it. 

#. Stop ``mongod``.
   
   .. code-block:: bash
  
      $ sudo systemctl stop mongod

#. Insert the key from keyfile into the |vault| server to the desired secret
   path.

   .. code-block:: bash
   
      # Retrieve the key value from the keyfile
      $ sudo cat /data/key/mongodb.key
      d0JTFcePmvROyLXwCbAH8fmiP/ZRm0nYbeJDMGaI7Zw=
      # Insert the key into vault
      $ vault kv put secret/dc/psmongodb1 value=d0JTFcePmvROyLXwCbAH8fmiP/ZRm0nYbeJDMGaI7Zw=

   .. note::
  
      Vault KV Secrets Engine uses different read and write secrets paths. To insert data to vault, specify the secret path without the ``data/`` prefix. 

#. Edit the configuration file to provision the |vault| configuration options instead of the key file encryption options.
   
   .. code-block:: yaml
   
      security:
         enableEncryption: true
         vault:
            serverName: 10.0.2.15
            port: 8200
            secret: secret/data/dc/psmongodb1
            tokenFile: /etc/mongodb/token
            serverCAFile: /etc/mongodb/vault.crt

#. Start the ``mongod`` service

   .. code-block:: bash
   
      $ sudo systemctl start mongod


.. |vault| replace:: HashiCorp Vault

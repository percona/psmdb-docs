.. _psmdb.data-at-rest-encryption:

================================================================================
Data at Rest Encryption
================================================================================

Data at rest encryption for the WiredTiger storage engine in |mongodb| was
introduced in |mongodb-enterprise| version 3.2. to ensure that encrypted data
files can be decrypted and read by parties with the decryption key.

.. seealso::

   |mongodb| Documentation: Encryption at Rest
       https://docs.mongodb.com/manual/core/security-encryption-at-rest/#encryption-at-rest

.. rubric:: Differences from Upstream

The |feature| in |PSMDB| is introduced in version 3.6 to be compatible with
|feature| in |mongodb|. In the current release of |PSMDB|, the |feature| does
not include support for |abbr.kmip|, or |amazon-aws| key management
services.

Two types of keys are used for data at rest encryption:

* Database keys to encrypt data. They are stored internally, near the data that they encrypt. 
* The master key to encrypt database keys. It is kept separately from the data and database keys and requires external management.

To manage the master key, use one of the supported key management options:

- Integration with an external key server (recommended). |PSMDB| is integrated with |vault| for this purpose. 
- Local key management using a keyfile.

Note that you can use only one of the key management options at a time. However, you can switch from one management option to another (e.g. from a keyfile to |vault|). Refer to :ref:`psmdb.encryption-mode-switch` section for details.

.. important::

   You can only enable data at rest encryption and provide all encryption settings on an empty database, when you start the ``mongod`` instance for the first time. You cannot enable or disable encryption while the |PSMDB| server is already running and / or has some data. Nor can you change the effective encryption mode by simply restarting the server. Every time you restart the server, the encryption settings must be the same.

.. contents::
   :local:

.. rubric:: Important Configuration Options

|PSMDB| supports the ``encryptionCipherMode`` option where you choose one of the following cipher modes:

- |mode.cbc|
- |mode.gcm|

By default, the |mode.cbc| cipher mode is applied. The following example
demonstrates how to apply the |mode.gcm| cipher mode when starting the
:program:`mongod` service:

.. code-block:: bash

   $ mongod ... --encryptionCipherMode AES256-GCM

.. seealso::

   |mongodb| Documentation: encryptionCipherMode Option
      https://docs.mongodb.com/manual/reference/program/mongod/#cmdoption-mongod-encryptionciphermode

|vault| Integration
=================================================================

Starting from version 3.6.13-3.3, |PSMDB| provides |vault| integration. |vault| supports different secrets engines. |PSMDB| only supports the |vault|
back end with KV Secrets Engine - Version 2 (API)
with versioning enabled.

.. seealso::

   Percona Blog: Using Vault to Store the Master Key for Data at Rest Encryption on |PSMDB|
      https://www.percona.com/blog/2020/04/21/using-vault-to-store-the-master-key-for-data-at-rest-encryption-on-percona-server-for-mongodb/

   How to configure the KV Engine:
      https://www.vaultproject.io/api/secret/kv/kv-v2.html

.. admonition:: |vault| Parameters

   .. list-table::
      :widths: 25 25 15 35
      :header-rows: 1
   
      * - Command line
        - Config file
        - Type
        - Description
      * - vaultServerName
        - security.vault.serverName
        - string
        - The IP address of the Vault server
      * - vaultPort
        - security.vault.port
        - int
        - The port on the Vault server
      * - vaultTokenFile
        - security.vault.tokenFile
        - string
        - The path to the vault token file. The token file is used by |mongodb| to access |vault|. The vault token file consists of the raw vault token and does not include any additional strings or parameters.
             
          Example of a vault token file:

          .. code-block:: text

             s.uTrHtzsZnEE7KyHeA797CkWA

      * - vaultSecret
        - security.vault.secret
        - string
        - The path to the vault secret. Note that vault secrets path format must be:

          .. code-block:: text

             <vault_secret_mount>/data/<custom_path>

          where:

          * ``<vault_secret_mount>`` is your Vault KV Secrets Engine;
          * ``data`` is the mandatory path prefix required by Version 2 API;
          * ``<custom_path>`` is your secrets path

          Example:

          .. code-block:: text

             secret_v2/data/psmdb-test/rs1-27017

          .. note::

             It is recommended to use different secret paths for every database node.
           
      * - vaultRotateMasterKey
        - security.vault.rotateMasterKey
        - switch
        - Enables master key rotation
      * - vaultServerCAFile
        - security.vault.serverCAFile
        - string
        - The path to the TLS certificate file
      * - vaultDisableTLSForTesting
        - security.vault.disableTLSForTesting
        - switch
        - Disables secure connection to |vault| using SSL/TLS client certificates

.. admonition:: Config file example

   .. code-block:: yaml

      security:
        enableEncryption: true
        vault:
          serverName: 127.0.0.1
          port: 8200
          tokenFile: /home/user/path/token
          secret: secret/data/hello

 During the first run of the |PSMDB|, the process generates a secure key and writes the key to the vault. 

 During the subsequent start, the server tries to read the master key from the vault. If the configured secret does not exist, vault responds with HTTP 404 error.

.. rubric:: Key Rotation

Key rotation is replacing the old master key with a new one. This process helps to comply with regulatory requirements.

To rotate the keys for a single ``mongod`` instance, do the following:

1. Stop the ``mongod`` process
#. Add ``--vaultRotateMasterKey`` option via the command line or ``security.vault.rotateMasterKey`` to the config file.
#. Run the ``mongod`` process with the selected option, the process will perform the key rotation and exit.
#. Remove the selected option from the startup command or the config file.
#. Start ``mongod`` again.

Rotating the master key process also re-encrypts the keystore using the new master key. The new master key is stored in the vault. The entire dataset is not re-encrypted.

For a replica set, the steps are the following:

1. Rotate the master key for the secondary nodes one by one.
2. Step down the primary and wait for another primary to be elected.
3. Rotate the master key for the previous primary node.

Local key management using a keyfile
====================================

The key file must contain a 32 character string encoded in base64. You can generate a random
key and save it to a file by using the |openssl| command:

.. code-block:: bash

   $ openssl rand -base64 32 > mongodb-keyfile

Then, as the owner of the ``mongod`` process, update the file permissions: only
the owner should be able to read and modify this file. The effective permissions specified with the ``chmod`` command can be:

* **600** - only the owner may read and modify the file
* **400** - only the owner may read the file.

.. code-block:: bash

   $ chmod 600 mongodb-keyfile

Enable the |feature| in |PSMDB| by setting these options:

- ``--enableEncryption`` to enable data at rest encryption
- ``--encryptionKeyFile`` to specify the path to a file that contains the encryption key

.. code-block:: bash

   $ mongod ... --enableEncryption --encryptionKeyFile <fileName>

By default, |PSMDB| uses the ``AES256-CBC`` cipher mode. If you want to use the ``AES256-GCM`` cipher mode, then use the ``encryptionCipherMode`` parameter to change it. 

If ``mongod`` is started with the ``--relaxPermChecks`` option and the key file
is owned by ``root`` then ``mongod`` can read the file based on the
group bit set accordingly. The effective key file permissions in this
case are:

- **440** - both the owner and the group can only read the file, or
- **640** - only the owner can read and the change the file, the group can only read the file.

.. seealso::

   |mongodb| Documentation: Configure Encryption
      https://docs.mongodb.com/manual/tutorial/configure-encryption/#local-key-management

   |Percona| Blog: WiredTiger Encryption at Rest with Percona Server for MongoDB
      https://www.percona.com/blog/2018/11/01/wiredtiger-encryption-at-rest-percona-server-for-mongodb/
 
All these options can be specified in the configuration file:

.. code-block:: yaml

   security:
      enableEncryption: <boolean>
      encryptionCipherMode: <string>
      encryptionKeyFile: <string>
      relaxPermChecks: <boolean>

.. seealso::

   |mongodb| Documentation: How to set options in a configuration file
      https://docs.mongodb.com/manual/reference/configuration-options/index.html#configuration-file

Encrypting Rollback Files
============================================================================

Starting from version 3.6, |PSMDB| also encrypts rollback files when data at
rest encryption is enabled. To inspect the contents of these files, use
|perconadecrypt|. This is a tool that you run from the command line as follows:

.. code-block:: bash

   $ perconadecrypt --encryptionKeyFile FILE  --inputPath FILE --outputPath FILE [--encryptionCipherMode MODE]

When decrypting, the cipher mode must match the cipher mode which was used for
the encryption. By default, the |opt.encryption-cipher-mode| option uses the
|mode.cbc| mode.

.. admonition:: Parameters of |perconadecrypt|

   ========================  ==================================================================================
   Option                    Purpose
   ========================  ==================================================================================
   --encryptionKeyFile       The path to the encryption key file
   --encryptionCipherMode    The cipher mode for decryption. The supported values are |mode.cbc| or |mode.gcm|
   --inputPath               The path to the encrypted rollback file
   --outputPath              The path to save the decrypted rollback file
   ========================  ==================================================================================

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

.. |openssl| replace:: :program:`openssl`
.. |mongodb-enterprise| replace:: MongoDB Enterprise
.. |mongodb| replace:: MongoDB
.. |feature| replace:: data encryption at rest
.. |abbr.kmip| replace:: :abbr:`KMIP (Key Management Interoperability Protocol)`
.. |vault| replace:: HashiCorp Vault
.. |amazon-aws| replace:: Amazon AWS
.. |mode.cbc| replace:: AES256-CBC
.. |mode.gcm| replace:: AES256-GCM
.. |perconadecrypt| replace:: :program:`perconadecrypt`
.. |opt.encryption-cipher-mode| replace:: ``--encryptionCipherMode``

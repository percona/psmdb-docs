.. _psmdb.data-at-rest-encryption:

================================================================================
Data at Rest Encryption
================================================================================

.. contents::
   :local:

Data at rest encryption for the WiredTiger storage engine in |mongodb| was
introduced in |mongodb-enterprise| version 3.2 to ensure that encrypted data
files can be decrypted and read by parties with the decryption key.

.. rubric:: Differences from Upstream

The |feature| in |PSMDB| is introduced in version 3.6 to be compatible with
|feature| interface in |mongodb|. In the current release of |PSMDB|, the |feature| does not include support for |amazon-aws| key management service. Instead, |PSMDB| is :ref:`integrated with HashiCorp Vault <vault>`. Starting with release 4.2.19-19, |PSMDB| supports the secure transfer of keys using :ref:`Key Management Interoperability Protocol (KMIP) <kmip>`. This allows users to store encryption keys in their favorite KMIP-compatible key manager. when they set up encryption at rest.

Two types of keys are used for data at rest encryption:

* Database keys to encrypt data. They are stored internally, near the data that they encrypt. 
* The master key to encrypt database keys. It is kept separately from the data and database keys and requires external management.

To manage the master key, use one of the supported key management options:

- Integration with an external key server (recommended). |PSMDB| is :ref:`integrated with HashiCorp Vault <vault>` for this purpose and supports the secure transfer of keys using :ref:`Key Management Interoperability Protocol (KMIP) <kmip>`. 
- :ref:`Local key management using a keyfile <keyfile>`.

Note that you can use only one of the key management options at a time. However, you can switch from one management option to another (e.g. from a keyfile to |vault|). Refer to :ref:`psmdb.encryption-mode-switch` section for details.

.. important::

   You can only enable data at rest encryption and provide all encryption settings on an empty database, when you start the ``mongod`` instance for the first time. You cannot enable or disable encryption while the |PSMDB| server is already running and / or has some data. Nor can you change the effective encryption mode by simply restarting the server. Every time you restart the server, the encryption settings must be the same.

.. toctree::
   :hidden:

   vault
   keyfile
   encryption-mode-switch
   kmip

.. rubric:: Important Configuration Options

|PSMDB| supports the ``encryptionCipherMode`` option where you choose one of the
following cipher modes:

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



.. |openssl| replace:: :program:`openssl`
.. |mongodb-enterprise| replace:: MongoDB Enterprise
.. |feature| replace:: data encryption at rest
.. |abbr.kmip| replace:: :abbr:`KMIP (Key Management Interoperability Protocol)`
.. |vault| replace:: HashiCorp Vault
.. |amazon-aws| replace:: Amazon AWS
.. |mode.cbc| replace:: AES256-CBC
.. |mode.gcm| replace:: AES256-GCM
.. |perconadecrypt| replace:: :program:`perconadecrypt`
.. |opt.encryption-cipher-mode| replace:: ``--encryptionCipherMode``

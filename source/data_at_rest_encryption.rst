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
|feature| in |mongodb| with the following differences:

- The |feature| in |PSMDB| will not include support for |abbr.kmip|.
- There are new configuration options to support |vault| and |amazon-aws| key
  management service.

|abbr.kmip| is not supported because there is no open source solution for
|abbr.kmip| so far.

.. rubric:: Configuration options

In addition to the configuration options provided by the
upstream solution, |PSMDB| supports the encryptionCipherMode option where you
choose one of the following cipher modes:

- |mode.cbc|
- |mode.gcm|

By default, the |mode.cbc| cipher mode is applied. The following example
demonstrates how to apply the |mode.gcm| cipher mode when starting the
:program:`mongod` service:

.. code-block:: bash

   $ mongod --encryptCipherMode AES256-GCM

|PSMDB| also supports the options exposed by the upstream solution: 

- ``--enableEncryption`` to enable data at rest encryption
- ``--encryptionKeyFile`` to specify the path to a file that contains the encryption key

.. code-block:: bash

   $ mongod --enableEncryption --encryptionKeyFile <fileName>
  
The key file must contain 32 bytes; each byte encoded in base64. You can generate a random
key and save it to a file by usiing the |openssl| command:

.. code-block:: bash

   $ openssl rand -base64 32 > mongodb-keyfile

.. seealso::

   |mongodb| Documentation: Configure Encryption
      https://docs.mongodb.com/manual/tutorial/configure-encryption/#local-key-management

All these options can be specified in the configuration file:

.. code-block:: yaml
		
   security:
      enableEncryption: <boolean>
      encryptionCipherMode: <string>
      encryptionKeyFile: <string>

.. seealso::

   |mongodb| Documentation: How to set options in a configuration file
      https://docs.mongodb.com/manual/reference/configuration-options/index.html#configuration-file
  
.. |openssl| replace:: :program:`openssl`
.. |mongodb-enterprise| replace:: MongoDB Enterprise
.. |mongodb| replace:: MongoDB
.. |feature| replace:: data encryption at rest
.. |abbr.kmip| replace:: :abbr:`KMIP (Key Management Interoperability Protocol`
.. |vault| replace:: HashiCorp Vault
.. |amazon-aws| replace:: Amazon AWS
.. |mode.cbc| replace:: AES256-CBC
.. |mode.gcm| replace:: AES256-GCM

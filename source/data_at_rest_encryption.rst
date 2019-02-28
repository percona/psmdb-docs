.. _psmdb.data-at-rest-encryption:

================================================================================
Data at Rest Encryption
================================================================================

Data at rest encryption for the WiredTiger storage engine in |mongodb| was
introduced in |mongodb-enterprise| version 3.2 to ensure that encrypted data
files can be decrypted and read by parties with the decryption key.

.. important:: Limitations

   |feature| in |PSMDB| will not encrypt data backups created by
   ``mongodump`` or ``mongoexport`` utilities, AuditLog, general log
   and diagnostic data.  :ref:`Hot backups <hot-backup>`, however, are
   encrypted.


.. seealso::

   |mongodb| Documentation: Encryption at Rest
       https://docs.mongodb.com/manual/core/security-encryption-at-rest/#encryption-at-rest

.. rubric:: Differences from Upstream

Although the |feature| in |PSMDB| accepts similar options as
|mongodb-enterprise| with |feature|, the |PSMDB| binary is not a drop-in
replacement of |mongod| from |mongodb-enterprise|. In the current release of
|PSMDB|, the |feature| does not include support for |abbr.kmip|, |vault| or
|amazon-aws| key management services.


.. rubric:: Encrypting Rollback Files

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

|PSMDB| also supports the options exposed by the upstream solution: 

- ``--enableEncryption`` to enable data at rest encryption
- ``--encryptionKeyFile`` to specify the path to a file that contains the encryption key

.. code-block:: bash

   $ mongod ... --enableEncryption --encryptionKeyFile <fileName>
  
The key file must contain a 32 character string encoded in base64. You can generate a random
key and save it to a file by using the |openssl| command:

.. code-block:: bash

   $ openssl rand -base64 32 > mongodb-keyfile

Then, as the owner of the ``mongod`` process, update the file permissions: only
the owner should be able to read and modify this file. The effective permissions
specified with the ``chmod`` command can either be **600** (only the owner may
read and modify the file) or **400** (only the owner may read the file.)

.. code-block:: bash

   $ chmod 600 mongodb-keyfile

If ``mongod`` is started with the ``--relaxPermChecks`` option and the key file
is owned by ``root`` then ``mongod`` can read the file based on the
group bit set accordingly. The effective key file permissions in this
case are either **440** (both the owner and the group can only read the file) or
**640** (only the owner can read and the change the file, the group can only
read the file).

.. seealso::

   |mongodb| Documentation: Configure Encryption
      https://docs.mongodb.com/manual/tutorial/configure-encryption/#local-key-management

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


  
.. |openssl| replace:: :program:`openssl`
.. |mongodb-enterprise| replace:: MongoDB Enterprise
.. |mongodb| replace:: MongoDB
.. |feature| replace:: data encryption at rest
.. |abbr.kmip| replace:: :abbr:`KMIP (Key Management Interoperability Protocol)`
.. |vault| replace:: HashiCorp Vault
.. |amazon-aws| replace:: Amazon AWS
.. |mode.cbc| replace:: AES256-CBC
.. |mode.gcm| replace:: AES256-GCM
.. |perconadecrypt| replace:: ``perconadecrypt``
.. |opt.encryption-cipher-mode| replace:: :option:`--encryptionCipherMode`

.. include:: .res/replace.program.txt


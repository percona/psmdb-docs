.. _kmip:

Using the Key Management Interoperability Protocol (KMIP) 
============================================================

This feature is in **technical preview** stage.

|PSMDB| adds support for secure transfer of keys using the `OASIS Key Management Interoperability Protocol (KMIP) <https://docs.oasis-open.org/kmip/kmip-spec/v2.0/os/kmip-spec-v2.0-os.html>`__. The KMIP implementation was tested with the `PyKMIP server <https://pykmip.readthedocs.io/en/latest/server.html>`__ and the `HashiCorp Vault Enterprise KMIP Secrets Engine <https://www.vaultproject.io/docs/secrets/kmip>`__.

KMIP enables the communication between key management systems and the database server. KMIP provides the following benefits:

* Streamline encryption key management
* Eliminate redundant key management processes

.. admonition:: KMIP parameters

   .. list-table::
      :widths: auto
      :header-rows: 1
   
      * - Option
        - Type
        - Description
      * - --kmipServerName
        - string
        - The hostname or IP address of the KMIP server.
      * - --kmipPort
        - number
        - The port used to communicate with the KMIP server. 
      * - --kmipServerCAFile
        - string
        - The path to the CA certificate file. CA file is used to validate secure client connection to the KMIP server.
      * - --kmipClientCertificateFile
        - string
        - The path to the client certificate file. The database server uses the client certificate file to authenticate the KMIP server.
      * - --kmipClientKeyFile
        - string
        - The path to the KMIP client private key.
      * - --kmipKeyIdentifier
        - string
        - The name of the KMIP key. If the key does not exist, the database server will create a key on the KMIP server with the specified identifier.
      * - --kmipRotateMasterKey
        - boolean
        - Controls master keys rotation. When enabled, generates the new master key version and re-encrypts the keystore. Available as of version 4.2.20-20. Requires the unique ``--kmipKeyIdentifier`` for every ``mongod`` node.
 
Key rotation
============

Starting with release 4.2.20-20, the support for master key rotation is added. This enables users to comply with data security regulations when using KMIP.

.. note:: 

   To make KMIP master key rotation, make sure that every ``mongod`` has a unique ``--kmipKeyIdentifier`` value.

.. admonition:: Config file example

   .. code-block:: yaml

      security:
        enableEncryption: true
        kmip:
          serverName: 128.0.0.2
          port: 5696
          clientCertificateFile: /path/client_certificate.pem
          clientKeyFile: /path/client_key.pem
          serverCAFile: /path/ca.pem
          keyIdentifier: key_name
          
.. _kmip:

Using the Key Management Interoperability Protocol (KMIP) 
============================================================

|PSMDB| adds support for the secure transfer of keys using the `OASIS Key Management Interoperability Protocol (KMIP) <https://docs.oasis-open.org/kmip/kmip-spec/v2.0/os/kmip-spec-v2.0-os.html>`__. The KMIP implementation was tested with the `PyKMIP server <https://pykmip.readthedocs.io/en/latest/server.html>`__ and the `HashiCorp Vault Enterprise KMIP Secrets Engine <https://www.vaultproject.io/docs/secrets/kmip>`__.

KMIP enables the communication between a key management system and the database server. KMIP provides the following benefits:

* Streamlines encryption key management
* Eliminates redundant key management processes

You can specify multiple KMIP servers for failover. On startup, |PSMDB| connects to the servers in the order listed and selects the one with which the connection is successful.

.. admonition:: KMIP parameters

   .. list-table::
      :widths: auto
      :header-rows: 1
   
      * - Option
        - Type
        - Description
      * - ``--kmipServerName``
        - string
        - The hostname or IP address of the KMIP server. Multiple KMIP servers are supported as the comma-separated list, e.g. ``kmip1.example.com,kmip2.example.com``
      * - ``--kmipPort``
        - number
        - The port used to communicate with the KMIP server. When undefined, the default port ``5696`` will be used.
      * - ``--kmipServerCAFile``
        - string
        - The path to the TLS certificate file. CA file is used to validate secure client connection to the KMIP server.
      * - ``--kmipClientCertificateFile``
        - string
        - The path to the PEM file with the KMIP client private key and the certificate chain. The database server uses this PEM file to authenticate the KMIP server.
      * - ``--kmipKeyIdentifier``
        - string
        - The identifier of the KMIP key. If the key does not exist, the database server creates a key on the KMIP server with the specified identifier. When you specify the identifier, the key with such an ID must exist on the key storage. You can only use this setting for the first time you enable encryption.
      * - ``--kmipRotateMasterKey``
        - boolean
        - Controls master keys rotation. When enabled, generates the new master key version and re-encrypts the keystore. Requires the unique ``--kmipKeyIdentifier`` for every ``mongod`` node.
      * - ``--kmipClientCertificatePassword``
        - string
        - The password for the KMIP client private key or certificate. Use this parameter only if the KMIP client private key or certificate is encrypted. 

Key rotation
================

|PSMDB| supports the `master key rotation <https://www.mongodb.com/docs/manual/tutorial/rotate-encryption-key/#kmip-master-key-rotation>`_ to enable users to comply with data security regulations when using KMIP.


Configuration
=============

.. rubric:: Considerations

Make sure you have obtained the root certificate, and the keypair for the KMIP server and the ``mongod`` client. For testing purposes you can use the `OpenSSL <https://www.openssl.org/>`_ to issue self-signed certificates. For production use we recommend you use the valid certificates issued by the key management appliance.


To enable data-at-rest encryption in |PSMDB| using KMIP, edit the ``/etc/mongod.conf`` configuration file as follows:

.. code-block:: yaml

   security:
     enableEncryption: true
     kmip:
       serverName: <kmip_server_name>
       port: <kmip_port>
       clientCertificateFile: </path/client_certificate.pem>
       clientKeyFile: </path/client_key.pem>
       serverCAFile: </path/ca.pem>
       keyIdentifier: <key_name>


Alternatively, you can start |PSMDB| using the command line as follows:

.. code-block:: bash

   $ mongod --enableEncryption \
     --kmipServerName <kmip_servername> \
     --kmipPort <kmip_port> \
     --kmipServerCAFile <path_to_ca_file> \
     --kmipClientCertificateFile <path_to_client_certificate> \
     --kmipClientKeyFile <path_to_client_private_key> \
     --kmipKeyIdentifier <kmip_identifier>


          
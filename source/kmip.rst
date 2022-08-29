.. _kmip:

Using the Key Management Interoperability Protocol (KMIP) 
============================================================

This feature is **technical preview** quality.

|PSMDB| adds support for the secure transfer of keys using the `OASIS Key Management Interoperability Protocol (KMIP) <https://docs.oasis-open.org/kmip/kmip-spec/v2.0/os/kmip-spec-v2.0-os.html>`__. The KMIP implementation was tested with the `PyKMIP server <https://pykmip.readthedocs.io/en/latest/server.html>`__ and the `HashiCorp Vault Enterprise KMIP Secrets Engine <https://www.vaultproject.io/docs/secrets/kmip>`__.

KMIP enables the communication between a key management system and the database server. KMIP provides the following benefits:

* Streamlines encryption key management
* Eliminates redundant key management processes

Starting with version 5.0.9-8, you can specify multiple KMIP servers for failover. On startup, |PSMDB| connects to the servers in the order listed and selects the one with which the connection is successful.

.. admonition:: KMIP parameters

   .. list-table::
      :widths: auto
      :header-rows: 1
   
      * - Option
        - Type
        - Description
      * - --kmipServerName
        - string
        - The hostname or IP address of the KMIP server. As of version 5.0.9-8, multiple KMIP servers are supported as the comma-separated list, e.g. ``kmip1.@example.com,kmip2.example.com``
      * - --kmipPort
        - number
        - The port used to communicate with the KMIP server. When undefined, the default port ``5696`` will be used.
      * - --kmipServerCAFile
        - string
        - The path to the TLS certificate file. CA file is used to validate secure client connection to the KMIP server.
      * - --kmipClientCertificateFile
        - string
        - The path to the PEM file with the KMIP client private key and the certificate chain. The database server uses this PEM file to authenticate the KMIP server.
      * - --kmipKeyIdentifier
        - string
        - Mandatory. The name of the KMIP key. If the key does not exist, the database server creates a key on the KMIP server with the specified identifier.
      * - --kmipRotateMasterKey
        - boolean
        - Controls master keys rotation. When enabled, generates the new master key version and re-encrypts the keystore. Available as of version 5.0.8-7. Requires the unique ``--kmipKeyIdentifier`` for every ``mongod`` node.
      * - --kmipClientCertificatePassword
        - string
        - The password for the KMIP client private key or certificate. Use this parameter only if the KMIP client private key or certificate is encrypted. Available starting with version 5.0.9-8.

Key rotation
================

Starting with release 5.0.8-7, the support for `master key rotation <https://www.mongodb.com/docs/manual/tutorial/rotate-encryption-key/#kmip-master-key-rotation>`_ is added. This enables users to comply with data security regulations when using KMIP.

.. note::

   To make KMIP master key rotation, make sure that every ``mongod`` has a unique ``--kmipKeyIdentifier`` value.

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

.. _upgrade-kmip:

Minor upgrade of |PSMDB| to version 5.0.11-10 and higher
========================================================

While the data-at-rest encryption using the KMIP Protocol is in the tech preview stage, we recommend using it only for technical purposes as breaking changes can be introduced. With the ``kmipKeyIdentifier`` option becoming optional in version 5.0.11, the standard upgrade procedure doesn’t work. 

If you are running |PSMDB| 5.0.10 or lower and do need to upgrade |PSMDB| to version 5.0.11-10 and higher, this section provides the upgrade steps.

For a single-node deployment, use the ``mongodump`` / ``mongorestore`` tools to make a backup before the update and to restore from it after binaries are updated.

For replica sets, data must be re-encrypted with the **new** key during the upgrade. Go through the `encrypting existing data steps <https://www.mongodb.com/docs/v5.0/tutorial/configure-encryption/#std-label-encrypt-existing-data>`_  but perform the :ref:`minor upgrade <minor_upgrade>` between steps 1 and 2 to replace the `mongod` binary.


          
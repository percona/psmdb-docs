.. _ldap-x509:

*******************************************************
Set up x.509 authentication and LDAP authorization     
*******************************************************

:ref:`x509` is one of the supported authentication mechanisms in |PSMDB|. It is compatible with :ref:`ldap-authorization` to enable you to control user access and operations in your database environment. 

This document provides the steps on how to configure and use x.509 certificates for authentication in |PSMDB| and authorize users in the LDAP server. 

Considerations
==============

1. For testing purposes, in this tutorial we use `OpenSSL <https://www.openssl.org/>`_ to issue self-signed certificates. For production use, we recommend using certificates issued and signed by the :abbr:`CA (Certified Authority)` in |PSMDB|. Client certificates must meet the `client certificate requirements <https://docs.mongodb.com/manual/core/security-x.509/#client-certificate-requirements>`_.
2. The setup of the LDAP server and the configuration of the LDAP schema is out of scope of this document. We assume that you have the LDAP server up and running and accessible to |PSMDB|. 

Setup procedure
===============

Issue certificates
--------------------------

1. Create a directory to store the certificates. For example, :dir:`/var/lib/mongocerts`.

   .. code-block:: bash

      $ sudo mkdir -p /var/lib/mongocerts

#. Grant access to the ``mongod`` user to this directory:

   .. code-block:: bash

      $ sudo chown mongod:mongod /var/lib/mongocerts

Generate the root Certificate Authority certificate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The root Certificate Authority certificate will be used to sign the SSL certificates. 
   
Run the following command and in the ``-subj`` flag, provide the details about your organization:
   
* C - Country Name (2 letter code);
* ST - State or Province Name (full name);
* L - Locality Name (city);
* O - Organization Name (company);
* CN - Common Name (your name or your server's hostname) .

.. code-block:: bash

   $ cd /var/lib/mongocerts
   $ sudo openssl req -nodes -x509 -newkey rsa:4096 -keyout ca.key -out ca.crt -subj "/C=US/ST=California/L=SanFrancisco/O=Percona/OU=root/CN=localhost"

Generate server certificate
^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Create the server certificate request and key. In the ``-subj`` flag, provide the details about your organization:
   
   * C - Country Name (2 letter code);
   * ST - State or Province Name (full name);
   * L - Locality Name (city);
   * O - Organization Name (company);
   * CN - Common Name (your name or your server's hostname) .
   
   .. code-block:: bash

      $ sudo openssl req -nodes -newkey rsa:4096 -keyout server.key -out server.csr -subj "/C=US/ST=California/L=SanFrancisco/O=Percona/OU=server/CN=localhost" 

#. Sign the server certificate request with the root CA certificate:
   
   .. code-block:: bash

      $ sudo openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out server.crt

#. Combine the server certificate and key to create a certificate key file. Run this command as the ``root`` user:
   
   .. code-block:: bash

      $ cat server.key server.crt > server.pem

Generate client certificates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Generate client certificate request and key. In the ``-subj`` flag, specify the information about clients in the :abbr:`DN (Distinguished Name)` format.
   
   .. code-block:: bash

      $ openssl req -nodes -newkey rsa:4096 -keyout client.key -out client.csr -subj "/DC=com/DC=percona/CN=John Doe"

#. Sign the client certificate request with the root CA certificate.
   
   .. code-block:: bash

      $ openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -set_serial 02 -out client.crt

#. Combine the client certificate and key to create a certificate key file.
   
   .. code-block:: bash

      $ cat client.key client.crt > client.pem

Set up the LDAP server
-------------------------

The setup of the LDAP server is out of scope of this document. Please work with your LDAP administrators to set up the LDAP server and configure the LDAP schema. 

Configure ``mongod`` server
-----------------------------

The configuration consists of the following steps:

* Creating a role that matches the user group on the LDAP server
* Editing the configuration file to enable the x.509 authentication
  
.. note::

   When you use x.509 authentication with LDAP authorization, you don't need to create users in the ``$external`` database.  User management is done on the LDAP server so when a client connects to the database, they are authenticated and authorized through the LDAP server. 


Create roles 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At this step, create the roles in the ``admin`` database with the names that exactly match the names of the user groups on the LDAP server. These roles are used for user :ref:`ldap-authorization` in |PSMDB|. 

In our example, we create the role `cn=otherusers,dc=percona,dc=com` that has the corresponding LDAP group.

.. code-block:: javascript

   var admin = db.getSiblingDB("admin")
   db.createRole(
      {
        role: "cn=otherusers,dc=percona,dc=com", 
        privileges: [], 
        roles: [ 
              "userAdminAnyDatabase", 
              "clusterMonitor", 
              "clusterManager", 
              "clusterAdmin"
               ]
      }
   )


Output:

.. code-block:: json

   {
   	"role" : "cn=otherusers,dc=percona,dc=com",
   	"privileges" : [ ],
   	"roles" : [
   		"userAdminAnyDatabase",
   		"clusterMonitor",
   		"clusterManager",
   		"clusterAdmin"
   	]
   }


Enable x.509 authentication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Stop the ``mongod`` service
   
   .. code-block:: bash

      $ sudo systemctl stop mongod

#. Edit the :file:`/etc/mongod.conf` configuration file.
   
   .. code-block:: yaml

      net:
        port: 27017
        bindIp: 127.0.0.1
        tls:
          mode: requireTLS
          certificateKeyFile: /var/lib/mongocerts/server.pem
          CAFile: /var/lib/mongocerts/ca.crt

      security:
        authorization: enabled
        ldap:
          servers: "ldap.example.com"
          transportSecurity: none
          authz:
            queryTemplate: "dc=percona,dc=com??sub?(&(objectClass=groupOfNames)(member={USER}))"

      setParameter:
        authenticationMechanisms: PLAIN,MONGODB-X509

   Replace ``ldap.example.com`` with the hostname of your LDAP server. In the LDAP query template, replace the domain controllers ``percona`` and ``com`` with those relevant to your organization.

#. Start the ``mongod`` service
   
   .. code-block:: bash

      $ sudo systemctl start mongod

Authenticate with the x.509 certificate
--------------------------------------------------------

To test the authentication, connect to |PSMDB| using the following command:

.. code-block:: bash

   $ mongo --host localhost --tls --tlsCAFile /var/lib/mongocerts/ca.crt --tlsCertificateKeyFile <path_to_client_certificate>/client.pem  --authenticationMechanism MONGODB-X509 --authenticationDatabase='$external'

The result should look like the following: 

.. code-block:: javascript

   > db.runCommand({connectionStatus : 1})
   {
   	"authInfo" : {
   		"authenticatedUsers" : [
   			{
   				"user" : "CN=John Doe,DC=percona,DC=com",
   				"db" : "$external"
   			}
   		],
   		"authenticatedUserRoles" : [
   			{
   				"role" : "cn=otherreaders,dc=percona,dc=com",
   				"db" : "admin"
   			},
   			{
   				"role" : "clusterAdmin",
   				"db" : "admin"
   			},
   			{
   				"role" : "userAdminAnyDatabase",
   				"db" : "admin"
   			},
   			{
   				"role" : "clusterManager",
   				"db" : "admin"
   			},
   			{
   				"role" : "clusterMonitor",
   				"db" : "admin"
   			}
   		]
   	},
   	"ok" : 1
   }


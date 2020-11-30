
.. _ext-auth:

=======================
External Authentication
=======================

Normally, a client needs to authenticate themselves
against the MongoDB server user database before doing any work
or reading any data from a ``mongod`` or ``mongos`` instance.
External authentication allows the MongoDB server
to verify the client's user name and password against a separate service,
such as OpenLDAP or Active Directory. This allows users accessing the database
with the same credentials they use for their emails or workstations.

|PSMDB| supports the following external authentication mechanisms:

-  :ref:`ldap-authentication-sasl`
-  :ref:`ldap-authorization`   
-  :ref:`kerberos-authentication`

.. _ldap-authentication-sasl:
   
LDAP Authentication Using SASL
=====================================

.. contents::
   :local:
   :depth: 1

Overview
========

The following components are necessary for external authentication to work:

* **LDAP Server**: Remotely stores all user credentials
  (i.e. user name and associated password).
* **SASL Daemon**: Used as a MongoDB server-local proxy
  for the remote LDAP service.
* **SASL Library**: Used by the MongoDB client and server
  to create data necessary for the authentication mechanism.

The following image illustrates this architecture:

.. image:: psmdb-ext-auth.png
   :align: center

An authentication session uses the following sequence:

1. A ``mongo`` client connects to a running ``mongod`` instance.
#. The client creates a ``PLAIN`` authentication request
   using the |SASL| library.
#. The client then sends this SASL request to the server
   as a special Mongo command.
#. The ``mongod`` server receives this SASL Message,
   with its authentication request payload.
#. The server then creates a SASL session scoped to this client,
   using its own reference to the SASL library.
#. Then the server passes the authentication payload to the SASL library,
   which in turn passes it on to the ``saslauthd`` daemon.
#. The ``saslauthd`` daemon passes the payload on to the LDAP service
   to get a YES or NO authentication response
   (in other words, does this user exist and is the password correct).
#. The YES/NO response moves back from ``saslauthd``,
   through the SASL library, to ``mongod``.
#. The ``mongod`` server uses this YES/NO response
   to authenticate the client or reject the request.
#. If successful, the client has authenticated and can proceed.
   
Environment Setup and Configuration
===================================

This section describes an example configuration
suitable only to test out the external authentication functionality
in a non-production environment.
Use common sense to adapt these guidelines to your production.

The following components are required:

* ``slapd``: OpenLDAP server.
* ``libsasl2`` version 2.1.25 or later.
* ``saslauthd``: |SASL| Authentication Daemon (distinct from ``libsasl2``).

The following steps will help you configure your environment:

.. contents::
   :local:	  

.. rubric:: Assumptions

Before we move on to the configuration steps, we assume the following:

1. You have the LDAP server up and running. The LDAP server is accessible to the server with the |PSMDB| installed.
#. You must place these two servers behind a firewall as the communications between them will be in plain text. This is because the SASL mechanism of PLAIN can only be used when authenticating and credentials will be sent in plain text.
#. You have ``sudo`` privilege to the server with the |PSMDB| installed.

Configuring ``saslauthd``
---------------------------------
1. Install the SASL packages. Depending on your OS, use the following command:

   For *RedHat and CentOS*:

   .. code-block:: bash

     sudo yum install -y cyrus-sasl cyrus-sasl-plain
 
   For *Debian and Ubuntu*:

   .. code-block:: bash

     sudo apt-get install -y sasl2-bin
		
#. Configure SASL to use ``ldap`` as the  authentication mechanism.

   .. note:: Back up the original configuration file before making changes.
   

   For *RedHat/CentOS*, specify the ``ldap`` value for the :option:`--MECH` option using the following command:

   .. code-block:: bash

     sudo sed -i -e s/^MECH=pam/MECH=ldap/g /etc/sysconfig/saslauthd		

   Alternatively, you can edit the :file:`/etc/sysconfig/saslauthd` configuration file:

   .. code-block:: yaml

     MECH=ldap		

   For *Debian/Ubuntu*, use the following commands to enable the ``saslauthd`` to auto-run on startup and to set the ``ldap`` value for the :option:`--MECHANISMS` option:

   .. code-block:: bash

     sudo sed -i -e s/^MECH=pam/MECH=ldap/g /etc/sysconfig/saslauthdsudo sed -i -e s/^MECHANISMS="pam"/MECHANISMS="ldap"/g /etc/default/saslauthd 
     sudo sed -i -e s/^START=no/START=yes/g /etc/default/saslauthd		

   Alternatively, you can edit the :file:`/etc/default/sysconfig/saslauthd` configuration file:

   .. code-block:: yaml

     START=yes		
     MECHANISMS="ldap"
  

#. Create the :file:`/etc/saslauthd.conf` configuration file and specify these settings required for ``saslauthd``
   to connect to a local OpenLDAP service
   (the server address MUST match the OpenLDAP installation):

   .. code-block:: text

     ldap_servers: ldap://localhost
     ldap_mech: PLAIN
     ldap_search_base: dc=example,dc=com
     ldap_filter: (cn=%u)
     ldap_bind_dn: cn=admin,dc=example,dc=com
     ldap_password: secret

   Note the LDAP password and bind domain name.
   This allows the ``saslauthd`` service to connect to the LDAP service as root.
   In production, this would not be the case; users should not store administrative passwords in unencrypted files.

Microsoft Windows Active Directory
**********************************

In order for LDAP operations to be performed
against a Windows Active Directory server,
a user record must be created to perform the lookups.

The following example shows configuration parameters for ``saslauthd``
to communicate with an Active Directory server:

.. code-block:: text

  ldap_servers: ldap://localhost
  ldap_mech: PLAIN
  ldap_search_base: CN=Users,DC=example,DC=com
  ldap_filter: (sAMAccountName=%ucn=%u)
  ldap_bind_dn: CN=ldapmgr,CN=Users,DC=<AD Domain>,DC=<AD TLD>
  ldap_password: ld@pmgr_Pa55word

In order to determine and test the correct search base
and filter for your Active Directory installation,
the Microsoft `LDP GUI Tool
<https://technet.microsoft.com/en-us/library/Cc772839%28v=WS.10%29.aspx>`_
can be used to bind and search the LDAP-compatible directory.


#. Give write permissions to the :file:`/run/saslauthd` folder for the ``mongod``. Either change permissions to the  :file:`/run/saslauthd` folder:

   .. code-block:: bash

     sudo chmod 755 /run/saslauthd

   Or add the ``mongod`` user to the ``sasl`` group:

   .. code-block:: bash

     sudo usermod -a -G sasl mongod

Sanity Check
------------

Verify that the ``saslauthd`` service can authenticate
against the users created in the LDAP service:

.. code-block:: bash

   $ testsaslauthd -u christian -p secret  -f /var/run/saslauthd/mux

This should return ``0:OK "Success"``.
If it doesn't, then either the user name and password
are not in the LDAP service, or ``sasaluthd`` is not configured properly.

Configuring libsasl2
--------------------

The ``mongod`` also uses the SASL library for communications. To configure the SASL library, create a configuration file. 

The configuration file **must** be named ``mongodb.conf`` and placed in a directory
where ``libsasl2`` can find and read it.
``libsasl2`` is hard-coded to look in certain directories at build time.
This location may be different depending on the installation method.

In the configuration file, specify the following:

.. code-block:: text

  pwcheck_method: saslauthd
  saslauthd_path: /var/run/saslauthd/mux
  log_level: 5
  mech_list: plain

The first two entries (``pwcheck_method`` and ``saslauthd_path``)
are required for ``mongod`` to successfully use the ``saslauthd`` service.
The ``log_level`` is optional but may help determine configuration errors.

.. seealso::

   `SASL documentation: <https://www.cyrusimap.org/sasl/index.html>`_
  
Configuring ``mongod`` Server
-----------------------------

To enable external authentication, you must create a user with the **root** privileges in the ``admin`` database. If you have already created this user, skip this step. Otherwise, run the following command to create the admin user:

.. code-block:: text

   > use admin
   switched to db admin
   > db.createUser({"user": "admin", "pwd": "$3cr3tP4ssw0rd", "roles": ["root"]})
   Successfully added user: { "user" : "admin", "roles" : [ "root" ] }


Edit the :file:`etc/mongod.conf` configuration file to enable the external authentication:

.. code-block:: yaml

  security:
    authorization: enabled

  setParameter:
    authenticationMechanisms: PLAIN,SCRAM-SHA-1

Restart the ``mongod`` service:

.. code-block:: bash

  systemctl restart mongod

When everything is configured properly, you can use the :ref:`commands`.

.. _commands:

External Authentication Commands
================================

Use the following command to add an external user to the ``mongod`` server:

.. code-block:: text

   > db.getSiblingDB("$external").createUser( {user : "christian", roles: [ {role: "read", db: "test"} ]} );

The previous example assumes that you have set up the server-wide
admin user/role and have successfully authenticated as that user locally.

.. note:: External users cannot have roles assigned in the admin database.

When running the ``mongo`` client, a user can authenticate
against a given database using the following command:

.. code-block:: text

  > db.getSiblingDB("$external").auth({ mechanism:"PLAIN", user:"christian", pwd:"secret", digestPassword:false})


.. admonition:: Based on the material from **Percona Database Performance Blog**
		
   This section is based on the blog post *Percona Server for MongoDB Authentication Using Active Directory* by *Doug Duncan*:
      https://www.percona.com/blog/2018/12/21/percona-server-for-mongodb-authentication-using-active-directory/
  

.. _ldap-authorization:

Authentication and Authorization with Direct Binding to LDAP
============================================================
  
This feature has been supported in MongoDB Enterprise since its version 3.4.
  
Note the following limitations of |ldap-authorization| in |psmdb|:
  
- The `ldapTimeoutMS <https://docs.mongodb.com/manual/reference/program/mongoldap/#cmdoption-mongoldap-ldaptimeoutms>`_ parameter is ignored.
- The `--ldapServers <https://docs.mongodb.com/manual/reference/program/mongoldap/#cmdoption-mongoldap-ldapservers>`_ option may only contain a single server (|mongodb-e| accepts a comma-separated list).
 
As of version 4.4.2-4, |psmdb| supports LDAP referrals. For security reasons, LDAP referrals are disabled by default. Double-check that using referrals is safe before enabling them.

To enable LDAP referrals, set the ``ldapFollowReferrals`` server parameter to ``true`` either using the ``setParameter`` command or editing the configuration file.

.. code-block:: yaml

   setParameter:
      ldapFollowReferrals: true

.. rubric:: Connection pool

As of version 4.4.2-4, |PSMDB| always uses a connection pool to LDAP server to process authentication requests. The connection pool is enabled by default. The default connection pool size is 2 connections. 

You can change the connection pool size either at the server startup or dynamically by specifying the value for the ``ldapConnectionPoolSizePerHost`` server parameter. 

For example, to set the number of connections in the pool to 5, use the ``setParameter`` command: 

.. code-block:: json

   $ db.adminCommand( { setParameter: 1, ldapConnectionPoolSizePerHost: 5  } )

Alternatively, edit the configuration file:

.. code-block:: yaml

   setParameter:
     ldapConnectionPoolSizePerHost: 5

.. seealso::
  
   |mongodb| Documentation:
       - `LDAP Authorization <https://docs.mongodb.com/manual/core/security-ldap-external/>`_	    
       - `Authenticate and Authorize Users Using Active Directory via Native LDAP <https://docs.mongodb.com/manual/tutorial/authenticate-nativeldap-activedirectory/>`_

.. _kerberos-authentication:

Kerberos Authentication
==============================

|PSMDB| supports Kerberos authentication starting from release 4.2.6-6. It is implemented the same way as in |mongodb| Enterprise.

.. seealso::

   |mongodb| Documentation:
         - `Kerberos Authentication <https://docs.mongodb.com/manual/core/kerberos/>`_	 
   

	   
.. |SASL| replace:: :abbr:`SASL (Simple Authentication and Security Layer)`

.. include:: .res/replace.txt

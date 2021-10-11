.. _sasl:

================================================================================
Setting up LDAP authentication with SASL 
================================================================================

This document describes an example configuration
suitable only to test out the external authentication functionality
in a non-production environment.
Use common sense to adapt these guidelines to your production environment.

To learn more about how the authentication works, see :ref:`ldap-authentication-sasl`. 

Environment setup and configuration
===================================

The following components are required:

* ``slapd``: OpenLDAP server.
* ``libsasl2`` version 2.1.25 or later.
* ``saslauthd``: |SASL| Authentication Daemon (distinct from ``libsasl2``).

The following steps will help you configure your environment:

.. contents::
   :local:	  

.. rubric:: Assumptions

Before we move on to the configuration steps, we assume the following:

1. You have the LDAP server up and running. The LDAP server is accessible to the server with |PSMDB| installed. This document focuses on OpenLDAP server. If you use Microsoft Windows Active Directory, refer to the :ref:`windows-ad` section for ``saslauthd`` configuration. 
#. You must place these two servers behind a firewall as the communications between them will be in plain text. This is because the SASL mechanism of PLAIN can only be used when authenticating and credentials will be sent in plain text.
#. You have ``sudo`` privilege to the server with the |PSMDB| installed.

Configuring ``saslauthd``
---------------------------------
1. Install the SASL packages. Depending on your OS, use the following command:

   For *RedHat and CentOS*:

   .. code-block:: bash

      $ sudo yum install -y cyrus-sasl 

   .. note::

      For |PSMDB| versions earlier than 4.0.26-21,  4.4.8-9, 4.2.16-17, also install the ``cyrus-sasl-plain`` package.
 
   For *Debian and Ubuntu*:

   .. code-block:: bash

      $ sudo apt-get install -y sasl2-bin
		
#. Configure SASL to use ``ldap`` as the  authentication mechanism.

   .. note:: Back up the original configuration file before making changes.
   
   For *RedHat/CentOS*, specify the ``ldap`` value for the ``--MECH`` option using the following command:

   .. code-block:: bash

      $ sudo sed -i -e s/^MECH=pam/MECH=ldap/g /etc/sysconfig/saslauthd		

   Alternatively, you can edit the :file:`/etc/sysconfig/saslauthd` configuration file:

   .. code-block:: yaml

      MECH=ldap		

   For *Debian/Ubuntu*, use the following commands to enable the ``saslauthd`` to auto-run on startup and to set the ``ldap`` value for the ``--MECHANISMS`` option:

   .. code-block:: bash

      $ sudo sed -i -e s/^MECH=pam/MECH=ldap/g /etc/sysconfig/saslauthdsudo sed -i -e s/^MECHANISMS="pam"/MECHANISMS="ldap"/g /etc/default/saslauthd 
      $ sudo sed -i -e s/^START=no/START=yes/g /etc/default/saslauthd		

   Alternatively, you can edit the :file:`/etc/default/sysconfig/saslauthd` configuration file:

   .. code-block:: yaml

      START=yes		
      MECHANISMS="ldap"
  
#. Create the :file:`/etc/saslauthd.conf` configuration file and specify the settings that ``saslauthd`` requires to connect to a local LDAP service:

OpenLDAP server
**********************************

The following is the example configuration file. Note that the server address **MUST** match the OpenLDAP installation:

.. code-block:: text

   ldap_servers: ldap://localhost
   ldap_mech: PLAIN
   ldap_search_base: dc=example,dc=com
   ldap_filter: (cn=%u)
   ldap_bind_dn: cn=admin,dc=example,dc=com
   ldap_password: secret

Note the LDAP password (``ldap_password``) and bind domain name (``ldap_bind_dn``).
This allows the ``saslauthd`` service to connect to the LDAP service as admin.
In production, this would not be the case; users should not store administrative passwords in unencrypted files.

.. _windows-ad:

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


4. Start the ``saslauthd`` process and set it to run at restart:
   
   .. code-block:: bash

      $ sudo systemctl start saslauthd
      $ sudo systemctl enable saslauthd

5. Give write permissions to the :dir:`/run/saslauthd` folder for the ``mongod``. Either change permissions to the  :dir:`/run/saslauthd` folder:

   .. code-block:: bash

      $ sudo chmod 755 /run/saslauthd

   Or add the ``mongod`` user to the ``sasl`` group:

   .. code-block:: bash

      $ sudo usermod -a -G sasl mongod

Sanity check
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

The configuration consists of the following steps:

* Creating a user with the **root** privileges. This user is required to log in to |PSMDB| after the external authentication is enabled.
* Editing the configuration file to enable the external authentication

Create a root user
**********************************

Create a user with the **root** privileges in the ``admin`` database. If you have already created this user, skip this step. Otherwise, run the following command to create the admin user:

.. code-block:: javascript

   > use admin
   switched to db admin
   > db.createUser({"user": "admin", "pwd": "$3cr3tP4ssw0rd", "roles": ["root"]})
   Successfully added user: { "user" : "admin", "roles" : [ "root" ] }

Enable external authentication
**********************************

Edit the :file:`etc/mongod.conf` configuration file to enable the external authentication:

.. code-block:: yaml

   security:
     authorization: enabled

   setParameter:
     authenticationMechanisms: PLAIN,SCRAM-SHA-1

Restart the ``mongod`` service:

.. code-block:: bash

   $ sudo systemctl restart mongod

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
  


.. |SASL| replace:: :abbr:`SASL (Simple Authentication and Security Layer)`

.. include:: .res/replace.txt
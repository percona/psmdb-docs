
.. _configure:

=======================
Client and Server Setup
=======================

This document describes how to configure ``saslauthd``, ``libsasl2``, ``mongo``, and ``mongod/mongos`` to use external authentication. It assumes that those binaries have been installed in the proper locations and an LDAP service has been setup, is reachable, and has users and credentials installed.

.. contents::
   :local:

Configure saslauthd
===================

First, we have to make sure ``saslauthd`` is configured correctly. Like other systems in this project, ``saslauthd`` relies on a configuration file.

OpenLDAP
--------

These are the typical settings required for ``saslauthd`` to connect to a local OpenLDAP service (the server address MUST match the OpenLDAP installation):

.. code-block:: none

  ldap_servers: ldap://127.0.0.1:9009
  ldap_search_base: dc=example,dc=com
  ldap_filter: (cn=%u)
  ldap_bind_dn: cn=openldapper,dc=example,dc=com
  ldap_password: secret

Note the LDAP password and bind domain name. This allows the ``saslauthd`` service to connect to the LDAP service as root. In production, this would not be the case; users should not store administrative passwords in unecrypted files. This is a temporary setup for testing.

Microsoft Windows Active Directory
----------------------------------

In order for LDAP operations to be performed against a Windows Active Directory server, a user record must be created to perform the lookups.

For ``saslauthd`` to successfully communicate with an Active Directory server, it must use the following configuration parameters:

.. code-block:: none

  ldap_servers: <ldap uri>
  ldap_mech: PLAIN
  ldap_search_base: CN=Users,DC=<AD Domain>,DC=<AD TLD>
  ldap_filter: (sAMAccountName=%u)
  ldap_bind_dn: CN=<AD LDAP lookup user name>,CN=Users,DC=<AD Domain>,DC=<AD TLD>
 ldap_password: <AD LDAP lookup password>


For example:

.. code-block:: none

  ldap_servers: ldap://198.51.100.10
  ldap_mech: PLAIN
  ldap_search_base: CN=Users,DC=example,DC=com
  ldap_filter: (sAMAccountName=%u)
  ldap_bind_dn: CN=ldapmgr,CN=Users,DC=<AD Domain>,DC=<AD TLD>
  ldap_password: ld@pmgr_Pa55word

In order to determine and test the correct search base and filter for your Active Directory installation, the Microsoft `LDP GUI Tool <https://technet.microsoft.com/en-us/library/Cc772839%28v=WS.10%29.aspx>`_ can be used to bind and search the LDAP-compatible directory.

Sanity Check
------------

Verify that the ``saslauthd`` service can authenticate against the users created in the LDAP service:

.. code-block:: bash

  $ testsaslauthd -u christian -p secret  -f /var/run/saslauthd/mux

This should return ``0:OK "Success"``. If it doesn't, then either the user name and password are not in the LDAP service, or ``sasaluthd`` is not configured properly.

Configure libsasl2
==================

The SASL library used by ``mongod/mongos`` must also be configured properly via a configuration file.

.. code-block:: none

  pwcheck_method: saslauthd
  saslauthd_path: /var/run/saslauthd/mux
  log_level: 5
  mech_list: plain

The first two entries (``pwcheck_method`` and ``saslauthd_path``) are required for ``mongod/mongos`` to successfully use the ``saslauthd`` service.  The ``log_level`` is optional but may help determine configuration errors.

The file **must** be named ``mongodb.conf`` and placed in a directory where ``libsasl2`` can find and read it.  ``libsasl2`` is hard-coded to look in certain directories at build time. This location may be different depending on the installation method.

Configure mongod/mongos Server
==============================

External authentication is enabled the same way as local authentication.  Simply start the server with the ``--auth`` option:

.. code-block:: bash

  $ ./mongod --dbpath=/data/db --auth

This assumes that ``libsasl2`` has been installed in the system as a dynamic library (``libsasl2.so``). You may see an error on the command line or in the logs if that library is missing from your server's environment.

Adding external users
=====================

Use the following command to add an external user to the ``mongod`` server:

.. code-block:: bash

  $ db.getSiblingDB("$external").createUser( {user : christian, roles: [ {role: "read", db: "test"} ]} );

The previous example assumes that you have set up the server-wide admin user/role and have successfully authenticated as that user locally.

.. note:: External users cannot have roles assigned in the *admin* database.

Client Authentication
=====================

When running the ``mongo`` client, a user can authenticate against a given database using the following command:

.. code-block:: bash

  $ db.auth({ mechanism:"PLAIN", user:"christian", pwd:"secret", digestPassword:false})

MongoDB drivers need to support the command interface for authenticating externally. This means they must:

* Be compiled/run with SASL authentication support. Should include usage of the ``libsasl2`` library.
* Allow users to specify a BSON argument for ``auth()`` calls.
* Allow users to specify the authentication ``mechanism`` field in the BSON argument.
* Allow users to specify the ``digestPassword`` field.


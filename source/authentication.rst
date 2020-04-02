
.. _ext-auth:

=======================
External Authentication
=======================

Normally, a client needs to authenticate themselves
against the MongoDB server user database before doing any work
or reading any data from a ``mongod`` or ``mongos`` instance.
External authentication allows the MongoDB server
to verify the client's user name and password against a separate service,
such as OpenLDAP or Active Directory.

.. admonition:: Support for |ldap-authorization|

   Starting from release 4.2.5-5, |psmdb| supports |ldap-authorization|. This
   feature has been supported in |mongodb-e| since its version 3.4.

   Note that the following limitations of |ldap-authorization| in |psmdb|:

   - The |abbr.ldap| `connection pool and all related parameters are not
     supported
     <https://docs.mongodb.com/manual/core/security-ldap-external/#connection-pool>`_.
   - The `ldapTimeoutMS
     <https://docs.mongodb.com/manual/reference/program/mongoldap/#cmdoption-mongoldap-ldaptimeoutms>`_
     parameter is ignored.
   - The `ldapUserCacheInvalidationInterval
     <https://docs.mongodb.com/manual/reference/parameters/#param.ldapUserCacheInvalidationInterval>`_
     parameter is ignored.
   - The `--ldapServers
     <https://docs.mongodb.com/manual/reference/program/mongoldap/#cmdoption-mongoldap-ldapservers>`_
     option may only contain a single server (|mongodb-e| accepts a
     comma-separated list).

   .. seealso::

      |mongodb| Documentation:
         - `LDAP Authorization
           <https://docs.mongodb.com/manual/core/security-ldap-external/>`_
	 - `Authenticate and Authorize Users Using Active Directory via Native LDAP
	   <https://docs.mongodb.com/manual/tutorial/authenticate-nativeldap-activedirectory/>`_

.. contents::
   :local:
   :depth: 1

Overview
================================================================================

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
   using the SASL library.
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

.. _commands:

External Authentication Commands
================================

Use the following command to add an external user to the ``mongod`` server:

.. code-block:: text

  > db.getSiblingDB("$external").createUser( {user : christian, roles: [ {role: "read", db: "test"} ]} );

The previous example assumes that you have set up the server-wide
admin user/role and have successfully authenticated as that user locally.

.. note:: External users cannot have roles assigned in the admin database.

When running the ``mongo`` client, a user can authenticate
against a given database using the following command:

.. code-block:: text

  > db.getSiblingDB("$external").auth({ mechanism:"PLAIN", user:"christian", pwd:"secret", digestPassword:false})

Environment Setup and Configuration
===================================

This section describes an example configuration
suitable only to test out the external authentication functionality
in a non-production environment.
Use common sense to adapt these guidelines to your production.

The following components are required:

* ``slapd``: OpenLDAP server.
* ``libsasl2`` version 2.1.25 or later.
* ``saslauthd``: SASL Authentication Daemon (distinct from ``libsasl2``).

The following steps will help you configure your environment:

.. contents::
   :local:

Running the LDAP service
------------------------

Start the LDAP server.
Note the given URL and configuration file.
Also note the username: *openldapper*.
It is important that the user starting the service,
and adding entries to the LDAP database, has permissions to do so.

.. code-block:: bash

   $ slapd -h ldap://127.0.0.1:9009/ -u openldapper -f /etc/openldap/slapd.conf

The URL argument will be used for entering data into the LDAP database,
verifying entries, and as an endpoint for ``saslauthd`` to authenticate
against during MongoDB external authentication.

A simple LDAP configuration file can have the following contents:

.. code-block:: text

  database        mdb
  suffix          "dc=example,dc=com"
  rootdn          "cn=openldapper,dc=example,dc=com"
  rootpw          secret
  directory       /home/openldapper/ldap/tests/openldap/install/var/openldap-data

There are other entries in the :file:`slapd.conf` file
that are important for successfully starting the LDAP service.
OpenLDAP installations have a sample :file:`slapd.conf` file
that has the above and other required entries,
such as ``include``, ``pidfile``, and ``argsfile``.

Adding Users to LDAP
--------------------

OpenLDAP comes with a few programs to communicate with the LDAP daemon/service.
For example, to add new users to the LDAP database,
you can use ``ldapadd`` or ``ldapmodify``, with an associated ``.ldif`` file.

Configuring saslauthd
---------------------

These are the typical settings required for ``saslauthd``
to connect to a local OpenLDAP service
(the server address MUST match the OpenLDAP installation):

.. code-block:: text

  ldap_servers: ldap://127.0.0.1:9009
  ldap_search_base: dc=example,dc=com
  ldap_filter: (cn=%u)
  ldap_bind_dn: cn=openldapper,dc=example,dc=com
  ldap_password: secret

Note the LDAP password and bind domain name.
This allows the ``saslauthd`` service to connect to the LDAP service as root.
In production, this would not be the case;
users should not store administrative passwords in unecrypted files.

Microsoft Windows Active Directory
**********************************

In order for LDAP operations to be performed
against a Windows Active Directory server,
a user record must be created to perform the lookups.

The following example shows configuration parameters for ``saslauthd``
to communicate with an Active Directory server:

.. code-block:: text

  ldap_servers: ldap://198.51.100.10
  ldap_mech: PLAIN
  ldap_search_base: CN=Users,DC=example,DC=com
  ldap_filter: (sAMAccountName=%u)
  ldap_bind_dn: CN=ldapmgr,CN=Users,DC=<AD Domain>,DC=<AD TLD>
  ldap_password: ld@pmgr_Pa55word

In order to determine and test the correct search base
and filter for your Active Directory installation,
the Microsoft `LDP GUI Tool
<https://technet.microsoft.com/en-us/library/Cc772839%28v=WS.10%29.aspx>`_
can be used to bind and search the LDAP-compatible directory.

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

The SASL library used by ``mongod`` must also be configured properly
via a configuration file:

.. code-block:: text

  pwcheck_method: saslauthd
  saslauthd_path: /var/run/saslauthd/mux
  log_level: 5
  mech_list: plain

The first two entries (``pwcheck_method`` and ``saslauthd_path``)
are required for ``mongod`` to successfully use the ``saslauthd`` service.
The ``log_level`` is optional but may help determine configuration errors.

The file **must** be named ``mongodb.conf`` and placed in a directory
where ``libsasl2`` can find and read it.
``libsasl2`` is hard-coded to look in certain directories at build time.
This location may be different depending on the installation method.

Configuring mongod Server
-------------------------

External authentication is enabled the same way as local authentication.
Simply start the server with the ``--auth`` option:

.. code-block:: bash

  $ ./mongod --dbpath=/data/db --auth

This assumes that ``libsasl2`` has been installed in the system
as a dynamic library (``libsasl2.so``).
You may see an error on the command line or in the logs
if that library is missing from your server's environment.

When everything is configured properly, you can use the :ref:`commands`.

.. seealso::

   SASL documentation
      https://www.cyrusimap.org/sasl/
   |mongodb| Documentation:
      - `LDAP Authorization
	<https://docs.mongodb.com/manual/core/security-ldap-external/>`_
      - `Authenticate and Authorize Users Using Active Directory via Native LDAP
	<https://docs.mongodb.com/manual/tutorial/authenticate-nativeldap-activedirectory/>`_

.. include:: .res/replace.txt

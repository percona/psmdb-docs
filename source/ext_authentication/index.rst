.. _ext-auth:

=======================
External Authentication
=======================

This section describes how to create a one-machine installation of all the components necessary for testing LDAP authentication in MongoDB.

.. todtree::
   :maxdepth: 1
   :glob:

   environment
   configuration
   build_test

Overview
========

Normally, a client needs to authenticate themselves against the MongoDB server user database before doing any work or reading any data from a mongod or mongos instance. External authentication allows the MongoDB server to verify the client's user name and password against a separate service, such as OpenLDAP or Active Directory.

The following components are necessary for external authentication to work:

* LDAP Server: Remotely stores all user credentials (i.e. user name and associated password).
* SASL Daemon: Used as a MongoDB server-local proxy for the remote LDAP service.
* SASL Library: Used by the MongoDB client and server to create authentication mechanism-specific data.

Authentication Sequence
-----------------------

An authentication session in this environment moves from component to component in the following way:

1. A ``mongo`` client connects to a running ``mongod`` instance.
2. The client creates a special authentication request using the SASL library and a selected authentication mechanism (in this case ``PLAIN``).
3. The client then sends this SASL request to the server as a special Mongo ``Command``.
4. The ``mongod`` server receives this SASL Message, with its authentication request payload.
5. The server then creates a SASL session scoped to this client, using its own reference to the SASL library.
6. Then the server passes the authentication payload to the SASL library, which in turn passes it on to the ``saslauthd`` daemon.
7. The ``saslauthd`` daemon passes the payload on to the LDAP service to get a YES or NO authentication response (in other words, does this user exist and is the password correct).
8. The YES/NO response moves back from ``saslauthd``, through the SASL library, to ``mongod``.
9. The ``mongod`` server uses this YES/NO response to authenticate the client or reject the request.
10. If successful, the client has authenticated and can proceed.

Client Authentication
=====================

Use the following command to add an external user to the ``mongod`` server:

.. code-block:: bash

  $ db.getSiblingDB("$external").createUser( {user : christian, roles: [ {role: "read", db: "test"} ]} );

When running the ``mongo`` client, a user can authenticate against a given database using the following command:

.. code-block:: bash

  $ db.getSiblingDB("$external").auth({ mechanism:"PLAIN", user:"christian", pwd:"secret", digestPassword:false})

.. see-also::

  * SASL documentation: `http://cyrusimap.web.cmu.edu/docs/cyrus-sasl/2.1.25/`_
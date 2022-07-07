.. _ldap-authorization:

************************************************************************
LDAP authorization
************************************************************************

LDAP authorization allows you to control user access and operations in your database environment using the centralized user management storage – an LDAP server. You create and manage user credentials and permission information in the LDAP server. In addition, you create roles in the ``admin`` database with the names that exactly match the LDAP group Distinguished Name. These roles define what privileges the users who belong to the corresponding LDAP group. 


.. _auth-mech:

Supported authentication mechanisms
=====================================

LDAP authorization is compatible with the following authentication mechanisms:

-  :ref:`x509`
-  :ref:`kerberos-authentication`
-  :ref:`native-ldap`  


.. _native-ldap:

Authentication and authorization with direct binding to LDAP
============================================================

Starting with release 4.2.5-5, you can configure |PSMDB| to communicate with the LDAP server directly to authenticate and also authorize users. 

The advantage of using this mechanism is that it is easy to setup and does not require pre-creating users  in the dummy ``$external`` db. Nevertheless, the ``--authenticationDatabase`` connection argument will still need to be specified as ``$external``.

The following example illustrates the connection to |PSMDB| from the ``mongo`` shell:

.. code-block:: text

   mongosh -u "CN=alice,CN=Users,DC=engineering,DC=example,DC=com" -p --authenticationDatabase '$external' --authenticationMechanism PLAIN

The following diagram illustrates the authentication and authorization flow:

.. image:: _static/images/NativeLDAP-auth.png

1. A user connects to the db providing their credentials
#. If required, |PSMDB| :ref:`transforms the username <usertoDNmapping>` to match the :abbr:`DN (Distinguished Name)` in the LDAP server according to the mapping rules specified for the ``--ldapUserToDNMapping`` parameter.
#. |PSMDB| queries the LDAP server for the user identity and /or the LDAP groups this user belongs to.
#. The LDAP server evaluates the query and if a user exists, returns their LDAP groups. 
#. |PSMDB| authorizes the user by mapping the DN of the returned groups against the roles assigned to the user in the ``admin`` database.  If a user belongs to several groups they receive permissions associated with every group.

.. _usertoDNmapping:

Username transformation
-----------------------

If clients connect to |PSMDB| with usernames that are not LDAP :abbr:`DN (Distinguished Name)`, these usernames must be converted to the format acceptable by LDAP.  

To achieve this,  the ``--ldapUserToDNMapping`` parameter is available in |PSMDB| configuration. 

The ``--ldapUserToDNMapping`` parameter is a JSON string representing an ordered array of rules expressed as JSON documents. Each document provides a regex pattern (``match`` field) to match against a provided username. If that pattern matches, there are two ways to continue:

- If there is the ``substitution`` value, then the matched pattern becomes the username of the user for further processing. 
- If there is the ``ldapQuery`` value, the matched pattern is sent to the LDAP server and the result of that LDAP query becomes the :abbr:`DN (Distinguished Name)` of the user for further processing. 
  
Both ``substitution`` and ``ldapQuery`` should contain placeholders to insert parts of the original username – those placeholders are replaced with regular expression submatches found on the ``match`` stage.

So having an array of documents, |PSMDB| tries to match each document against the provided name and if it matches, the name is replaced either with the substitution string or with the result of the LDAP query.

.. rubric:: LDAP referrals 

As of version 4.2.10-11, |psmdb| supports LDAP referrals as defined in `RFC 4511 4.1.10 <https://www.rfc-editor.org/rfc/rfc4511.txt>`_. For security reasons, referrals are disabled by default. Double-check that using referrals is safe before enabling them.

To enable LDAP referrals, set the ``ldapFollowReferrals`` server parameter to ``true`` using the :ref:`setParameter <setParameter>` command or by editing the configuration file.

.. code-block:: yaml

   setParameter:
      ldapFollowReferrals: true
      
.. rubric:: Connection pool

As of version 4.2.10-11, |PSMDB| always uses a connection pool to LDAP server to process bind requests. The connection pool is enabled by default. The default connection pool size is 2 connections. 

You can change the connection pool size either at the server startup or dynamically by specifying the value for the ``ldapConnectionPoolSizePerHost`` server parameter. 

For example, to set the number of connections in the pool to 5, use the ``setParameter`` command: 

.. tabs:: 

   .. tab:: Command line

      .. code-block:: javascript

         $ db.adminCommand( { setParameter: 1, ldapConnectionPoolSizePerHost: 5  } )

   .. tab:: Configuration file:

      .. code-block:: yaml

         setParameter:
           ldapConnectionPoolSizePerHost: 5

.. rubric:: Support for multiple LDAP servers

As of version 4.2.12-13, you can specify multiple LDAP servers for failover. |PSMDB| sends bind requests to the first server defined in the list. When this server is down or unavailable, it sends requests to the next server  and so on. Note that |PSMDB| keeps sending requests to this server even after the unavailable server recovers.

Specify the LDAP servers as a comma-separated list in the format ``<host>:<port>`` for the `--ldapServers <https://docs.mongodb.com/manual/reference/program/mongod/index.html#cmdoption-mongod-ldapservers>`_ option. 

You can define the option value at the server startup by editing the configuration file.

.. code-block:: yaml

   security:
     authorization: "enabled"
     ldap:
       servers: "ldap1.example.net,ldap2.example.net"

You can change ``ldapServers`` dynamically at runtime using the :ref:`setParameter <setParameter>`.

.. code-block:: text

   $ db.adminCommand( { setParameter: 1, ldapServers:"localhost,ldap1.example.net,ldap2.example.net"} )
   { "was" : "ldap1.example.net,ldap2.example.net", "ok" : 1 }

.. seealso::
  
   |mongodb| Documentation:	    
      - `Authenticate and Authorize Users Using Active Directory via Native LDAP <https://docs.mongodb.com/manual/tutorial/authenticate-nativeldap-activedirectory/>`_
      - `LDAP referrals <https://ldapwiki.com/wiki/LDAP%20Referral>`_
      
Configuration
===============

For how to configure LDAP authorization with the native LDAP authentication, see :ref:`ldap-setup`. 
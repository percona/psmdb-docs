.. _kerberos:

**********************************
Setting up Kerberos authentication 
**********************************

This document provides configuration steps for setting up :ref:`kerberos-authentication` in |PSMDB|. 


Assumptions
====================

The setup of the Kerberos server itself is out of scope of this document. Please refer to the `Kerberos documentation <https://web.mit.edu/kerberos/krb5-latest/doc/admin/install_kdc.html>`_ for the installation and configuration steps relevant to your operation system.

We assume that you have successfully completed the following steps:

* Installed and configured the Kerberos server
* Added necessary `realms <https://web.mit.edu/kerberos/krb5-1.12/doc/admin/realm_config.html>`_
* Added service, admin and user `principals <https://web.mit.edu/kerberos/krb5-1.5/krb5-1.5.4/doc/krb5-user/What-is-a-Kerberos-Principal_003f.html#What-is-a-Kerberos-Principal_003f>`_ 
* Configured the ``A`` and ``PTR`` DNS records for every host running `mongod` instance to resolve the hostnames onto Kerberos realm.

.. seealso:: 

   MongoDB Documentation: `Kerberos Authentication <https://www.mongodb.com/docs/manual/core/kerberos/>`_

Add user principals to |PSMDB|
==================================================

To get authenticated, users must exist both in the Kerberos and |PSMDB| servers with exactly matching names.

After you defined the user principals in the Kerberos server, add them to the ``$external`` database in |PSMDB| and assigned required roles:

.. code-block:: javascript

   use $external
   db.createUser({user: "demo@PERCONATEST.COM",roles: [{role: "read", db: "admin"}]})
   
Replace ``demo@PERCONATEST.COM`` with your username and Kerberos realm.


Configure Kerberos keytab files
=================================

A keytab file stores the authentication keys for a service principal representing a ``mongod`` instance to access the Kerberos admin server. 

After you have added the service principal to the Kerberos admin server, the entry for this principal is added to the ``/etc/krb5.keytab`` keytab file. 

The ``mongod`` server must have access to the keytab file to authenticate. To keep the keytab file secure, restrict the access to it only for the user running the ``mongod`` process.

1. Stop the ``mongod`` service
   
   .. code-block:: bash 

      $ sudo systemctl stop mongod

#. `Generate the keytab file <https://web.mit.edu/kerberos/krb5-1.5/krb5-1.5.4/doc/krb5-install/The-Keytab-File.html>`_ or get a copy of it if you generated the keytab file on another host. Save the keyfile under a separate path (e.g. /etc/mongodb.keytab)
   
   .. code-block:: bash
   
      $ cp /etc/krb5.keytab /etc/mongodb.keytab

#. Change the ownership to the keytab file
   
   .. code-block:: bash

      $ sudo chown mongod:mongod /etc/mongodb.keytab

#. Set the ``KRB5_KTNAME`` variable in the environment file for the ``mongod`` process.
   
   .. tabs::

      .. tab:: On Debian and Ubuntu

         Edit the environment file at the path ``/etc/default/mongodb`` and specify the ``KRB5_KTNAME`` variable: 

         .. code-block:: text

            KRB5_KTNAME=/etc/mongodb.keytab

         If you have a different path to the keytab file, specify it accordingly.

      .. tab:: On RHEL and derivatives

         Edit the environment file at the path ``/etc/sysconfig/mongod`` and specify the ``KRB5_KTNAME`` variable: 

         .. code-block:: text

            KRB5_KTNAME=/etc/mongodb.keytab


         If you have a different path to the keytab file, specify it accordingly.
 
#. Restart the ``mongod`` service

   .. code-block:: bash 

      $ sudo systemctl start mongod

|PSMDB| configuration
================================

Enable external authentication in |PSMDB| configuration. Edit the ``etc/mongod.conf`` configuration file and specify the following configuration:

.. code-block:: yaml

      security:
        authorization: "enabled"
        
      setParameter:
        authenticationMechanisms: GSSAPI

Restart the ``mongod`` service to apply the configuration:

.. code-block:: bash 

   $ sudo systemctl start mongod

Test the access to |PSMDB|
==========================

1. Obtain the Kerberos ticket for the user using the ``kinit`` command and specify the user password:

   .. code-block:: bash

      $ kinit demo
      Password for demo@PERCONATEST.COM:
      
#. Check the user ticket:
   
   .. code-block:: bash 

      $ klist -l
      Principal name                 Cache name
      --------------                 ----------
      demo@PERCONATEST.COM           FILE:/tmp/<ticket>

#. Connect to |PSMDB|: 
   
   .. code-block:: bash

      $ mongosh --host <hostname> --authenticationMechanism=GSSAPI --authenticationDatabase='$external' --username demo@PERCONATEST.COM

The result should look like the following:

.. code-block:: javascript

   > db.runCommand({connectionStatus : 1})
   {
   	"authInfo" : {
   		"authenticatedUsers" : [
   			{
   				"user" : "demo@PERCONATEST.COM",
   				"db" : "$external"
   			}
   		],
   		"authenticatedUserRoles" : [
   			{
   				"role" : "read",
   				"db" : "admin"
   			}
   		]
   	},
   	"ok" : 1
   }


.. include:: .res/replace.txt


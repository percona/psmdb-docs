.. _enable-auth:

=======================
Enabling Authentication
=======================

By default, |PSMDB| does not restrict access to data and configuration.

Enabling authentication enforces users to identify themselves when accessing the database. This documents describes how to enable built-in authentication mechanism. |PSMDB| also supports the number of external authentication mechanisms. To learn more, refer to :ref:`ext-auth`.

You can enable authentication either automatically or manually.

Automatic setup
----------------

To enable authentication and automatically set it up,
run the :file:`/usr/bin/percona-server-mongodb-enable-auth.sh` script
as root or using ``sudo``.

This script creates the ``dba`` user with the ``root`` role.
The password is randomly generated and printed out in the output.
Then the script restarts |PSMDB| with access control enabled.
The ``dba`` user has full superuser privileges on the server.
You can add other users with various roles depending on your needs.

For usage information, run the script with the ``-h`` option.

Manual setup
------------

To enable access control manually:

1. Add the following lines to the configuration file::

    security:
      authorization: enabled

2. Run the following command on the ``admin`` database::

    > db.createUser({user: 'USER', pwd: 'PASSWORD', roles: ['root'] });

3. Restart the ``mongod`` service::

    $ service mongod restart

4. Connect to the database as the newly created user::
    
   $ mongo --port 27017 -u 'USER' -p 'PASSWORD'  --authenticationDatabase "admin"

.. seealso:: 

   |mongodb| Documentation: Enable Access Control
       https://docs.mongodb.com/v4.2/tutorial/enable-authentication/

.. include:: .res/replace.program.txt

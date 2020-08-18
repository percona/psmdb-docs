.. _enable-auth:

=======================
Enabling Authentication
=======================

By default, |PSMDB| does not restrict access to data and configuration.

To enable authentication and automatically set it up,
run the :file:`/usr/bin/percona-server-mongodb-enable-auth.sh` script
as root or using ``sudo``.
This script creates the ``dba`` user with the ``root`` role.
The password is randomly generated and printed out in the output.
Then it restarts |PSMDB| with access control enabled.
The ``dba`` user has full superuser privileges on the server.
You can add other users with various roles depending on your needs.

For usage information, run the script with the ``-h`` option.

To enable access control manually:

1. Add the following lines to the configuration file::

    security:
      authorization: enabled

2. Run the following command on the ``admin`` database::

    > db.createUser({user: 'USER', pwd: 'PASSWORD', roles: ['root'] });

3. Restart the ``mongod`` service::

    $ systemctl restart mongod

.. include:: .res/replace.program.txt
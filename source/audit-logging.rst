.. _audit-log:

========
Auditing
========

Auditing allows administrators to track
and log user activity on a MongoDB server.
With auditing enabled, the server will generate an audit log file.
This file contains information about different user events
including authentication, authorization failures, and so on.

To enable audit logging, specify where to send audit events
using the :option:`--auditDestination` option on the command line
or the ``auditLog.destination`` variable in the configuration file.

If you want to output events to a file,
also specify the format of the file
using the :option:`--auditFormat` option
or the ``auditLog.format`` variable,
and the path to the file using the :option:`--auditPath` option
or the ``auditLog.path`` variable.

To filter recorded events, use the :option:`--auditFilter` option
or the ``auditLog.filter`` variable.

For example, to log only events from a user named *tim*
and write them to a JSON file :file:`/var/log/psmdb/audit.json`,
start the server with the following parameters:

.. code-block:: bash

   mongod \
    --dbpath data/db
    --auditDestination file \
    --auditFormat JSON \
    --auditPath /var/log/psmdb/audit.json \
    --auditFilter '{ "users.user" : "tim" }'

The options in the previous example can be used as variables
in the MongoDB configuration file::

 storage:
   dbPath: data/db
 auditLog:
   destination: file
   format: JSON
   path: /var/log/psmdb/audit.json
   filter: '{ "users.user" : "tim" }'

.. note:: If you start the server with auditing enabled,
   it cannot be disabled dynamically during runtime.

Audit Options
=============

The following options control audit logging:

.. option:: --auditDestination

   :Variable: ``auditLog.destination``
   :Type: String

   Enables auditing and specifies where to send audit events:

   * ``console``: Output audit events to ``stdout``.

   * ``file``: Output audit events to a file
     specified by the :option:`--auditPath` option
     in a format specified by the :option:`--auditFormat` option.

   * ``syslog``: Output audit events to ``syslog``.

.. option:: --auditFilter

   :Variable: ``auditLog.filter``
   :Type: String

   Specifies a filter to apply to incoming audit events,
   enabling the administrator to only capture a subset of them.
   The value must be interpreted as a query object with the following syntax::

     { <field1>: <expression1>, ... }

   Audit log events that match this query will be logged.
   Events that do not match this query will be ignored.

   For more information, see :ref:`audit-filter-examples`.

.. option:: --auditFormat

   :Variable: ``auditLog.format``
   :Type: String

   Specifies the format of the audit log file,
   if you set the :option:`--auditDestination` option to ``file``.

   The default value is ``JSON``.
   Alternatively, you can set it to ``BSON``.

.. option:: --auditPath

   :Variable: ``auditLog.path``
   :Type: String

   Specifies the fully qualified path to the file
   where audit log events are written,
   if you set the :option:`--auditDestination` option to ``file``.

   If this option is not specified,
   then the :file:`auditLog.json` file is created
   in the server's configured log path.
   If log path is not configured on the server,
   then the :file:`auditLog.json` file is created in the current directory
   (from which ``mongod`` was started).

   .. note:: This file will rotate in the same manner as the system log path,
      either on server reboot or using the ``logRotate`` command.
      The time of rotation will be added to the old file’s name.

Audit Message Syntax
====================

Audit logging writes messages in JSON format with the following syntax::

 {
   atype: <String>,
   ts : { "$date": <timestamp> },
   local: { ip: <String>, port: <int> },
   remote: { ip: <String>, port: <int> },
   users : [ { user: <String>, db: <String> }, ... ],
   roles: [ { role: <String>, db: <String> }, ... ],
   param: <document>,
   result: <int>
 }

:atype: Event type

:ts: Date and UTC time of the event

:local: Local IP address and port number of the instance

:remote: Remote IP address and port number
 of the incoming connection associated with the event

:users: Users associated with the event

:roles: Roles granted to the user

:param: Details of the event associated with the specific type

:result: Exit code (``0`` for success)

.. _audit-filter-examples:

Audit Filter Examples
=====================

The following examples demostrate the flexibility of audit log filters.

.. contents::
   :local:

.. code-block:: guess

   auditLog:
      destination: file
         filter: '{atype: {$in: [
            "authenticate", "authCheck", 
            "renameCollection", "dropCollection", "dropDatabase", 
            "createUser", "dropUser", "dropAllUsersFromDatabase", "updateuser", 
            "grantRolesToUser", "revokeRolesFromUser", "createRole", "updateRole", 
            "dropRole", "dropAllRolesFromDatabase", "grantRolesToRole", "revokeRolesFromRole", 
            "grantPrivilegesToRole", "revokePrivilegesFromRole", 
            "replSetReconfig",
            "enableSharding", "shardCollection", "addShard", "removeShard", 
            "shutdown", 
            "applicationMessage"
         ]}}'

Standard Query Selectors
------------------------

You can use query selectors,
such as ``$eq``, ``$in``, ``$gt``, ``$lt``, ``$ne``, and others
to log multiple event types.

For example, to log only the ``dropCollection`` and ``dropDatabase`` events:

* Command line::

   --auditDestination file --auditFilter '{ atype: { $in: [ "dropCollection", "dropDatabase" ] } }'

* Config file::

   auditLog:
     destination: file
     filter: '{ atype: { $in: [ "dropCollection", "dropDatabase" ] } }'

Regular Expressions
-------------------

Another way to specify multiple event types is using regular expressions.

For example, to filter all ``drop`` operations:

* Command line::

   --auditDestination file --auditFilter '{ "atype" : /^drop.*/ }'

* Config file::

   auditLog:
     destination: file
     filter: '{ "atype" : /^drop.*/ }'

Read and Write Operations
-------------------------

By default, operations with successful authorization are not logged,
so for this filter to work, enable ``auditAuthorizationSuccess`` parameter,
as described in :ref:`auditAuthorizationSuccess`.

For example, to filter read and write operations
on all the collections in the ``test`` database:

.. note:: The dot (``.``) after the database name in the regular expression
   must be escaped with two backslashes (``\\``).

* Command line::

   --setParameter auditAuthorizationSuccess=true --auditDestination file --auditFilter '{ atype: "authCheck", "param.command": { $in: [ "find", "insert", "delete", "update", "findandmodify" ] }, "param.ns": /^test\\./ } }'

* Config file::

   auditLog:
     destination: file
     filter: '{ atype: "authCheck", "param.command": { $in: [ "find", "insert", "delete", "update", "findandmodify" ] }, "param.ns": /^test\\./ } }'

   setParameter: { auditAuthorizationSuccess: true }

.. _auditAuthorizationSuccess:

Enabling Auditing of Authorization Success
==========================================

By default, only authorization failures for the ``authCheck`` action
are logged by the audit system. ``authCheck`` is for authorization by
role-based access control, it does not concern authentication at logins.

To enable logging of authorization successes,
set the ``auditAuthorizationSuccess`` parameter to ``true``. Audit events 
will then be triggered by every command, including CRUD ones.

.. warning::

   Enabling the ``auditAuthorizationSuccess`` parameter heavily impacts
   the performance compared to logging only authorization failures.

You can enable it on a running server using the following command::

 db.adminCommand( { setParameter: 1, auditAuthorizationSuccess: true } )

To enable it on the command line, use the following option
when running ``mongod`` or ``mongos`` process::

 --setParameter auditAuthorizationSuccess=true

You can also add it to the configuration file as follows::

 setParameter:
   auditAuthorizationSuccess: true

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
using the :option:`--auditDestination`` option on the command line
or the ``auditLog.destination`` variable in the configuration file.

If you output events to a file, also specify the format of the file
using the :option:`--auditFormat` option or the ``auditLog.format`` variable,
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
-------------

The following options control audit logging:

.. option:: --auditDestination

   :Variable: ``auditLog.destination``
   :Type: String

   Enables auditing and specifies where to send audit events:

   * ``console``: Output audit events to ``stdout``.

   * ``file``: Output audit events to a file
     specified by the :option:`--auditPath`` option
     in a format specified by the :option:``--auditFormat`` option.

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


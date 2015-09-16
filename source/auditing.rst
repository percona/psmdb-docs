.. _auditing:

========
Auditing
========

This document describes how to build, enable, configure and test auditing in Percona Server for MongoDB. 

Auditing allows administrators to track and log user activity on a server.  With auditing enabled, the server will generate an audit log file. This file contains information about different user events including authentication, authorization failures, and so on.

.. contents::
   :local:

Building
========

By default, when building Percona Server for MongoDB from source, audit functionality is neither compiled with, nor linked into, the final binary executable. To enable auditing, execute SCons with the ``--audit`` option:

.. code-block:: bash

  $ scons <other options> --audit <targets>

Activation and Configuration
============================

The following server parameters control auditing. They are entered at the command line when starting a server instance.

``--auditDestination``

  By default, even when auditing functionality is compiled into the server executable, audit logging is disabled. Auditing and audit log generation are activated when this parameter is present on the command line at server startup.

  The argument to this parameter is the type of audit log the server will create when storing events. In Percona Server for MongoDB, this can only be set to ``file``.

  .. code-block:: bash

    $ mongod --auditDestination=file

  .. note:: Auditing remains active until shutdown, it cannot be disabled dynamically at runtime.

``--auditFormat``

  This is the format of each audit event stored in the audit log. In Percona Server for MongoDB, this can only be set to ``JSON``.  The default value for this parameter is also ``JSON``, thus this parameter is optional and is only provided for application and driver compatibility.

  .. code-block:: bash

    $ mongod --auditDestination=file --auditFormat=JSON

``--auditPath``

  This is the fully qualified path to the file you want the server to create. If this parameter is not specified then :file:`auditLog.json` file will be created in server's configured log path.

  .. code-block:: bash

    $ mongod --auditDestination=file --auditPath /var/log/tokumx/audit.json

  If log path is not configured then :file:`auditLog.json` will be created in the current directory.

  .. note:: This file will rotate in the same manner as the system log path, either on server reboot or using the ``logRotate`` command. The time of the rotation will be added to the old file’s name.

``--auditFilter``

  This parameter specifies a filter to apply to incoming audit events, enabling the administrator to only capture a subset of all possible audit events.  

  This filter should be a JSON string that can be interpreted as a query object. Each audit log event that matches this query will be logged. Events which do not match this query will be ignored. If this parameter is not specified then all audit events are stored in the audit log.

  For example, to log only events from a user named *tim*, start the server with the following parameters:

  .. code-block:: bash

    $ mongod                                \
    --auditDestination file                 \
    --auditFormat JSON                      \
    --auditPath /var/log/tokumx/audit.json  \
    --auditFilter '{ "users.user" : "tim" }'

Testing
=======

There are dedicated audit JavaScript tests under the :file:`jstests/audit` directory. To execute all of them, run the following:

.. code-block:: bash

   $ python buildscripts/resmoke.py --audit

.. note:: the ``mongoimport`` utility is required to run the audit tests. It must be placed in the same directory from which :file:`resmoke.py` is run. Typically this location is the top level MongoDB :file:`build/source` directory.

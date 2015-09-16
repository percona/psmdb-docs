.. _environment:

=========================
Environment Prerequisites
=========================

This guides describes how to set up a suitable environment for testing the implementation of LDAP authentication for MongoDB.  The setup steps should be performed on a given Linux distribution, and certain open-source components must be installed and then specially configured.

.. contents::
   :local:

Component Installation
======================

The following components are required:

* ``libsasl2`` version 2.1.25: C library used in client and server code.
* ``saslauthd``: SASL Authentication Daemon.  This is distinct from ``libsasl2``.
* ``slapd``: OpenLDAP Server.

.. note:: We have been sandboxing the ``slapd`` daemon on our test machines.  This means we just download the OpenLDAP source code, build it locally, and install it in an arbitrary test directory local to the current working directory.

Installing SASL
---------------

There are two SASL components that need to be installed. First is the SASL library itself, ``libsasl2``, along with it's development header ``sasl.h``.  Second is ``saslauthd``, the authentication daemon.

Both SASL components can be downloaded, built and installed from source.

On Ubuntu, the following packages should be installed:

* libsasl2-2
* libsasl2-dev
* libsasl2-modules
* sasl2-bin
* ldap-utils

Optional packages:

* cyrus-sasl2-dbg
* cyrus-sasl2-doc

Environment Configuration
=========================

Running the LDAP service
------------------------

Start the LDAP server in the background or in a dedicated ``tmux`` pane for testing.  Note the given URL and configuration file.  Also note the username: *openldapper*.  It is important that the user starting the service, and adding entries to the LDAP database, has permissions to do so.

.. code-block:: bash

  $ slapd -h ldap://127.0.0.1:9009/ -u openldapper -f /etc/openldap/slapd.conf -d 1


The URL argument will be used for both entering data into the LDAP database, verifying entries, and as an endpoint for ``saslauthd`` to authenticate against during MongoDB external authentication.  The ``-d`` option is for helpful debugging information to help track incoming LDAP requests and responses.

An LDAP configuration file, with simple settings suitable for testing, would have contents like this:

.. code-block:: none

  database        mdb
  suffix          "dc=example,dc=com"
  rootdn          "cn=openldapper,dc=example,dc=com"
  rootpw          secret
  directory       /home/openldapper/ldap/tests/openldap/install/var/openldap-data

There are other entries in the :file:`slapd.conf` file that are important for successfully starting the LDAP service.  OpenLDAP installations have a sample :file:`slapd.conf` file that has the above and other required entries, such as ``include``, ``pidfile``, and ``argsfile``.

.. note:: We use the ``mdb`` database here because we don't want to add a dependency on a Berkeley DB installation.  The MDB database is an in-memory database compiled as part of the OpenLDAP installation.

Enter users into LDAP service
-----------------------------

OpenLDAP comes with a few programs to communicate with the LDAP daemon/service.  For example, to enter new entries into the LDAP database, you could use ``ldapadd`` or ``ldapmodify``, with an associated ``.ldif`` file.

Building MongoDB
================

To connect to these services, MongoDB must be built with extra information.

Adding SASL support
-------------------

Both client and server components (``mongo`` and ``mongod/mongos``), must be specially compiled to enable external authentication.

To set up the initial build environment, you need to follow the basic build instructions: :ref:`building`.

Both the client and server must be linked with ``libsasl2.so``.  This just means that an extra flag ``--use-sasl-client`` must be passed to SCons at build configuration time. A quick build would look like this:

.. code-block:: bash

  $ cd percona-server-mongodb
  $ git checkout v3.0
  $ scons --use-sasl-client -j8 mongo mongod

Once configured, the ``mongo`` binaries can be built, installed, and packaged as usual.  Note that ``libsasl2`` is NOT statically linked, so any user planning on running either the client or server binaries will need the SASL library installed in the same place it was installed at build time.

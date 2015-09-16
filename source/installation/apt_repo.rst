.. _apt_repo:

================================================================
Installing |Percona Server for MongoDB| on *Debian* and *Ubuntu*
================================================================

Ready-to-use packages are available from the |Percona Server for MongoDB| software repositories and the `download page <http://www.percona.com/downloads/Percona-Server-for-MongoDB/LATEST/>`_.

Supported Releases:

* Debian:

 * 8.0 (jessie)

* Ubuntu:

 * 12.04LTS (precise)
 * 14.04LTS (trusty)
 * 14.10 (utopic)
 * 15.04 (vivid)

Supported Platforms:

 * x86_64 (also known as ``amd64``)

What's in each DEB package?
===========================

The ``percona-server-mongodb`` package will install the ``mongo`` shell, import/export tools, other client utilities, server software, default configuration, and init.d scripts.

The ``percona-server-mongodb-server`` package contains the Percona Server for MongoDB server software, default configuration files and init.d scripts. 

The ``percona-server-mongodb-shell`` package contains the Percona Server for MongoDB shell

The ``percona-server-mongodb-mongos`` package contains ``mongos`` - the Percona Server for MongoDB sharded cluster query router.

The ``percona-server-mongodb-tools`` package contains Mongo tools for high-performance MongoDB fork from Percona.

The ``percona-server-mongodb-dbg`` package contains debug symbols for the server.

                   
Installing |Percona Server for MongoDB| from Percona ``apt`` repository
=======================================================================

1. Import the public key for the package management system

  *Debian* and *Ubuntu* packages from *Percona* are signed with the Percona's GPG key. Before using the repository, you should add the key to :program:`apt`. To do that, run the following commands as root or with sudo:

  .. code-block:: bash

    $ sudo apt-key adv --keyserver keys.gnupg.net --recv-keys 1C4CBDCDCD2EFD2A

  .. note::

    In case you're getting timeouts when using ``keys.gnupg.net`` as an alternative you can fetch the key from ``keyserver.ubuntu.com``. 

2. Create the :program:`apt` source list for Percona's repository:

   You can create the source list and add the percona repository by running: 

   .. code-block:: bash

     $ echo "deb http://repo.percona.com/apt "$(lsb_release -sc)" main" | sudo tee /etc/apt/sources.list.d/percona.list

   Additionally you can enable the source package repository by running: 

   .. code-block:: bash 

     $ echo "deb-src http://repo.percona.com/apt "$(lsb_release -sc)" main" | sudo tee -a /etc/apt/sources.list.d/percona.list

3. Remember to update the local cache:

   .. code-block:: bash

     $ sudo apt-get update

4. After that you can install the server package:

   .. code-block:: bash

     $ sudo apt-get install percona-server-mongodb


Percona ``apt`` Testing repository
----------------------------------

Percona offers pre-release builds from the testing repository. To enable it add the just add the ``testing`` word at the end of the Percona repository definition in your repository file (default :file:`/etc/apt/sources.list.d/percona.list`). It should looks like this (in this example ``VERSION`` is the name of your distribution): :: 

  deb http://repo.percona.com/apt VERSION main testing
  deb-src http://repo.percona.com/apt VERSION main testing

Apt-Pinning the packages
------------------------

In some cases you might need to "pin" the selected packages to avoid the upgrades from the distribution repositories. You'll need to make a new file :file:`/etc/apt/preferences.d/00percona.pref` and add the following lines in it: :: 

  Package: *
  Pin: release o=Percona Development Team
  Pin-Priority: 1001

For more information about the pinning you can check the official `debian wiki <http://wiki.debian.org/AptPreferences>`_.


Running |Percona Server for MongoDB|
====================================

|Percona Server for MongoDB| stores the data files in :file:`/var/lib/mongodb/` by default. You can find the configuration file that is used to manage |Percona Server for MongoDB| in :file:`/etc/mongod.conf`. 

1. Starting the service

   |Percona Server for MongoDB| is started automatically after it gets installed unless it encounters errors during the installation process. You can also manually start it by running: 

   .. code-block:: bash

     $ sudo service mongod start

2. Confirming that service is running 

   You can check the service status by running:  

   .. code-block:: bash

     $ service mongod status

3. Stopping the service

   You can stop the service by running:

   .. code-block:: bash

     $ sudo service mongod stop

4. Restarting the service 

   You can restart the service by running: 

   .. code-block:: bash

     $ sudo service mongod restart

.. note:: 

  *Debian* 8.0 (jessie) and *Ubuntu* 15.04 (vivid) come with `systemd <http://freedesktop.org/wiki/Software/systemd/>`_ as the default system and service manager so you can invoke all the above commands with ``sytemctl`` instead of ``service``. Currently both are supported.
     
Uninstalling |Percona Server for MongoDB|
=========================================

To uninstall |Percona Server for MongoDB| you'll need to remove all the installed packages. Removing packages with :command:`apt-get remove` will leave the configuration and data files. Removing the packages with :command:`apt-get purge` will remove all the packages with configuration files and data files (all the databases). Depending on your needs you can choose which command better suits you.

1. Stop the |Percona Server for MongoDB| service

   .. code-block:: bash

     $ sudo service mongod stop 

2. Remove the packages
   
   a) Remove the packages. This will leave the data files (databases, tables, logs, configuration, etc.) behind. In case you don't need them you'll need to remove them manually.

   .. code-block:: bash

     $ sudo apt-get remove percona-server-mongodb*

   b) Purge the packages. **NOTE**: This will remove all the packages and delete all the data files (databases, tables, logs, etc.)

   .. code-block:: bash

     $ sudo apt-get purge percona-server-mongodb*



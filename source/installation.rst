.. _installation:

===========================================
Installing |Percona Server for MongoDB| 3.0
===========================================

This page provides the information on how to you can install |Percona Server| for MongoDB. Following options are available: 

* :ref:`installing_from_binaries` 
* :ref:`installing_from_tarball`

Before installing, you might want to read the :ref:`release_notes_index`.

.. note:: If you want to use |Percona Server for MongoDB| in a Docker container, refer to the following example procedure for building a Docker image with MongoDB: https://docs.docker.com/examples/mongodb/.

.. _installing_from_binaries:

Installing |Percona Server for MongoDB| from Repositories
=========================================================

|Percona| provides repositories for :program:`yum` (``RPM`` packages for *Red Hat*, *CentOS* and *Amazon Linux AMI*) and :program:`apt` (:file:`.deb` packages for *Ubuntu* and *Debian*) for software such as |Percona Server|, |Percona XtraBackup|, and *Percona Toolkit*. This makes it easy to install and update your software and its dependencies through your operating system's package manager. This is the recommend way of installing where possible.

Following guides describe the installation process for using the official Percona repositories for :file:`.deb` and :file:`.rpm` packages.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   installation/apt_repo 
   installation/yum_repo 

.. note:: MongoDB creates a user that belongs to two groups, which is a potential security risk. This is fixed in |Percona Server for MongoDB|: user is included only in the ``mongod`` group. To avoid problems with current MongoDB setups, existing user group membership is not changed when you migrate to |Percona Server for MongoDB|. Instead, a new ``mongod`` user is created during installation, and it belongs to the ``mongod`` group.

.. note:: By default, |Percona Server for MongoDB| starts with the MMAPv1 storage engine (standard engine in MongoDB). If you want to leverage the PerconaFT storage engine, start ``mongod`` with the ``--storageEngine=PerconaFT`` option. For more information, see :ref:`perconaft`.

.. _installing_from_tarball:

Installing |Percona Server for MongoDB| from Binary Tarballs
============================================================

You can download the binary tarballs from the `Percona Server for MongoDB download page <https://www.percona.com/downloads/percona-server-for-mongodb/>`_.

1. Fetch and extract the correct binary tarball. For example, for Debian Jessie:

  .. code-block:: bash
    
    $ wget https://www.percona.com/downloads/percona-server-for-mongodb/percona-server-for-mongodb-3.0.5/binary/debian/jessie/x86_64/percona-server-mongodb-3.0.5-rel0.7rc-r42b00da-jessie-x86_64-bundle.tar
    $ tar xfz percona-server-mongodb-3.0.5-rel0.7rc-r42b00da-jessie-x86_64-bundle.tar

2. Copy the extracted binaries to the target directory:
   
   .. code-block:: bash

     $ mkdir psmdb
     $ cp -r -n percona-server-mongodb-3.0.5-rel0.7rc-r42b00da-jessie-x86_64-bundle/ psmdb

3. Add the location of the binaries to the ``PATH`` variable:
   
   .. code-block:: bash

     $ export PATH psmdb/bin:$PATH

4. Create the default data directory:

   .. code-block:: bash

     $ mkdir -p /data/db

By default, |Percona Server for MongoDB| starts with the MMAPv1 storage engine (standard engine in MongoDB). If you want to leverage the PerconaFT storage engine, start ``mongod`` with the ``--storageEngine=PerconaFT`` option. For more information, see :ref:`perconaft`.

.. _installation:

===========================================
Installing |Percona Server for MongoDB| 5.6
===========================================

This page provides the information on how to you can install |Percona Server| for MongoDB. Following options are available: 

* :ref:`installing_from_binaries` 
* :ref:`installing_from_tarball`

Before installing, you might want to read the :ref:`release_notes_index`.

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

.. _installing_from_tarball:

Installing |Percona Server for MongoDB| from Binary Tarballs
============================================================

You can download the binary tarballs from the **Linux - Generic** `section <https://www.percona.com/downloads/percona-server-for-mongodb/>`_ on the download page.

Fetch and extract the correct binary tarball. For example for Debian Jessie:

.. code-block:: bash

  $ wget https://www.percona.com/downloads/percona-server-for-mongodb/percona-server-for-mongodb-3.0.5/binary/debian/jessie/x86_64/percona-server-mongodb-3.0.5-rel0.7rc-r42b00da-jessie-x86_64-bundle.tar
  $ tar xfz percona-server-mongodb-3.0.5-rel0.7rc-jessie-x86_64.tar.gz




.. _installation:

===========================================
Installing |Percona Server for MongoDB| 5.6
===========================================

This page provides the information on how to you can install |Percona Server|. Following options are available: 

* :ref:`installing_from_binaries` (recommended)
* Installing |Percona Server| from Downloaded `:ref:`rpm <standalone_rpm>` or :ref:`apt <standalone_deb>` Packages

Before installing, you might want to read the :ref:`release_notes_index`.

.. _installing_from_binaries:

Installing |Percona Server| from Repositories
=============================================

|Percona| provides repositories for :program:`yum` (``RPM`` packages for *Red Hat*, *CentOS* and *Amazon Linux AMI*) and :program:`apt` (:file:`.deb` packages for *Ubuntu* and *Debian*) for software such as |Percona Server|, |Percona XtraBackup|, and *Percona Toolkit*. This makes it easy to install and update your software and its dependencies through your operating system's package manager. This is the recommend way of installing where possible.

Following guides describe the installation process for using the official Percona repositories for :file:`.deb` and :file:`.rpm` packages.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   installation/apt_repo 
   installation/yum_repo 

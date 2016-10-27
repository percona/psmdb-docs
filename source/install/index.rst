.. _install:

=====================================
Installing Percona Server for MongoDB
=====================================

|PSMDB| supports most 64-bit Linux distributions.
Percona provides packages for popular DEB-based and RPM-based distributions:

* Debian 8 ("jessie")
* Ubuntu 14.04 LTS (Trusty Tahr)
* Ubuntu 15.10 (Wily Werewolf)
* Ubuntu 16.04 LTS (Xenial Xerus)
* Red Hat Enterprise Linux / CentOS 5
* Red Hat Enterprise Linux / CentOS 6
* Red Hat Enterprise Linux / CentOS 7

It is recommended to install |PSMDB| from official Percona repositories
using the corresponding tool for your system:

* :ref:`Install using apt <apt>` if you are running Debian or Ubuntu
* :ref:`Install using yum <yum>` if you are running Red Hat Enterprise Linux
  or CentOS

.. note:: You can also `download packages
   <https://www.percona.com/downloads/percona-server-mongodb/LATEST/>`_
   from the Percona website and install them manually
   using :command:`dpkg` or :command:`rpm`.

If you want more control, you can
:ref:`install Percona Server for MongoDB from binary tarballs <tarball>`.

If you are currently using MongoDB 3.0 or 3.2,
see :ref:`Upgrading from MongoDB <upgrade_from_mongodb>`.

If you are currently using Percona TokuMX,
see :ref:`Upgrading from Percona TokuMX <upgrade_from_tokumx>`.

.. note:: If you want to use |PSMDB| in a Docker container,
   refer to the following example procedure for building a Docker image
   with MongoDB: https://docs.docker.com/examples/mongodb/

.. toctree::
   :hidden:

   Install Using apt <apt>
   Install Using yum <yum>
   Install from Binary Tarbal <tarball>


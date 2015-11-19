.. _install:

=====================================
Installing Percona Server for MongoDB 
=====================================

.. note:: Percona Server for MongoDB is currently available only as a *release candidate*.

   For more information, see the :ref:`release notes <3.0.5-rc7>`.

|Percona Server for MongoDB| supports most 64-bit Linux distributions. Percona provides packages for popular DEB-based and RPM-based distributions:

* Debian 8 ("jessie")
* Ubuntu 14.04 LTS (Trusty Tahr)
* Ubuntu 14.10 (Utopic Unicorn)
* Ubuntu 15.04 (Vivid Vervet)
* Red Hat Enterprise Linux / CentOS 5
* Red Hat Enterprise Linux / CentOS 6
* Red Hat Enterprise Linux / CentOS 7

It is recommended to install |Percona Server for MongoDB| from official Percona repositories using the corresponding tool for your system:

* :ref:`Install using apt <apt>` if you are running Debian or Ubuntu
* :ref:`Install using yum <yum>` if you are running Red Hat Enterprise Linux or CentOS

.. note:: You can also `download packages <https://www.percona.com/downloads/percona-server-mongodb/LATEST/>`_ from the Percona website and install them using :command:`dpkg`, :command:`rpm`, or any other package manager.

If you want more control, Percona provides binary tarballs for all supported distributions. For more information, see :ref:`tarball`.

If you are currently using MongoDB 3.0, see :ref:`upgrade_from_mongodb`.

If you are currently using Percona TokuMX, see :ref:`upgrade_from_tokumx`.

.. note:: If you want to use |Percona Server for MongoDB| in a Docker container, refer to the following example procedure for building a Docker image with MongoDB: https://docs.docker.com/examples/mongodb/.

.. toctree::
   :hidden:

   Install Using apt <apt>
   Install Using yum <yum>
   Install from Binary Tarbal <tarball>


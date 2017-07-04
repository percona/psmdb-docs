.. _install:

=====================================
Installing Percona Server for MongoDB
=====================================

|PSMDB| supports most 64-bit Linux distributions.
Percona provides packages for the following systems:

.. list-table:: Linux distributions supported by |PSMDB|
   :widths: 70 30
   :header-rows: 1

   * - Supported Distributions
     - Instructions
   * - * Debian 8 ("jessie")
       * Ubuntu 14.04 LTS (Trusty Tahr)
       * Ubuntu 16.04 LTS (Xenial Xerus)
       * Ubuntu 16.10 (Yakkety Yak)
       * Ubuntu 17.04 (Zesty Zapus)
     - :ref:`Install on Debian or Ubuntu <apt>`
   * - * Red Hat Enterprise Linux / CentOS 5
       * Red Hat Enterprise Linux / CentOS 6
       * Red Hat Enterprise Linux / CentOS 7
     - :ref:`Install on RHEL or CentOS <yum>`

.. note:: |PSMDB| should work on other Linux distributions
   (for example, Amazon Linux AMI and Oracle Linux),
   but it is tested only on platforms listed in the previous table.

Alternative Install Instructions
================================

You can also `download packages from the Percona website
<https://www.percona.com/downloads/percona-server-mongodb-3.2/>`_
and install them manually using :command:`dpkg` or :command:`rpm`.

.. note:: In this case, you will have to manually make sure
   that all dependencies are satisfied.

If you want more control over the installation, you can
:ref:`install Percona Server for MongoDB from binary tarballs <tarball>`.

.. note:: This method is for advanced users with specific needs
   that are not addressed by DEB and RPM packages.

If you want to run |PSMDB| in a Docker container, see :ref:`docker`.

Upgrade Instructions
====================

If you are currently using MongoDB,
see :ref:`Upgrading from MongoDB <upgrade_from_mongodb>`.

.. toctree::
   :hidden:

   Install on Debian or Ubuntu <apt>
   Install on RHEL or CentOS <yum>
   Install from Binary Tarball <tarball>
   Run in a Docker Container <docker>

If you are currently using Percona TokuMX,
see :ref:`Upgrading from Percona TokuMX <upgrade_from_tokumx>`.



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
       * Debian 9 ("stretch")
       * Ubuntu 14.04 LTS (Trusty Tahr)
       * Ubuntu 16.04 (Xenial Xerus)
       * Ubuntu 18.04 LTS (Bionic Beaver)
       * Ubuntu 18.10 (Cosmic Cuttlefish)
     - :ref:`Install on Debian or Ubuntu <apt>`
   * - * Red Hat Enterprise Linux / CentOS 6
       * Red Hat Enterprise Linux / CentOS 7
     - :ref:`Install on RHEL or CentOS <yum>`

.. note:: |PSMDB| should work on other Linus distributions
   (for example, Amazon Linux AMI and Oracle Linux),
   but it is tested only on platforms listed in the previous table.

Alternative Install Instructions
================================================================================

You can also download packages from the `Percona website`_ and install them
manually using :command:`dpkg` or :command:`rpm`.

.. note::

   In this case, you will have to make sure that all dependencies are satisfied.

If you want more control over the installation, you can :ref:`install Percona
Server for MongoDB from binary tarballs <tarball>`.

.. note::

   This method is for advanced users with specific needs that are not addressed
   by DEB and RPM packages.

If you want to run |PSMDB| in a Docker container, see :ref:`docker`.

Upgrade Instructions
================================================================================

If you are currently using MongoDB, see :ref:`Upgrading from MongoDB
<upgrade_from_mongodb>`.

If you are running an earlier version of |PSMDB|, see :ref:`Upgrading from Version 3.6 <upgrade_from_36>`.

.. toctree::
   :hidden:

   Install on Debian or Ubuntu <apt>
   Install on RHEL or CentOS <yum>
   Install from Binary Tarball <tarball>
   Run in a Docker Container <docker>

.. include:: ../.res/url.txt

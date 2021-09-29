.. _install:

=====================================
Installing Percona Server for MongoDB
=====================================

Percona provides installation packages of |PSMDB| for the most 64-bit Linux distributions. Find the full list of supported platforms on the `Percona Software and Platform Lifecycle <https://www.percona.com/services/policies/percona-software-platform-lifecycle#mongodb>`_ page.

The recommended installation method is from |percona| repositories. Follow the links below for the installation instructions for your operating system.

- :ref:`Install on Debian or Ubuntu <apt>`
- :ref:`Install on RHEL or CentOS <yum>`

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

Uninstall Instructions
================================================================================

To uninstall |PSMDB|, see :ref:`uninstall`.

.. toctree::
   :hidden:

   Install on Debian or Ubuntu <apt>
   Install on RHEL or CentOS <yum>
   Install from Binary Tarball <tarball>
   Run in a Docker Container <docker>

.. include:: ../.res/url.txt

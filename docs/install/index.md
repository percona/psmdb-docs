Percona Server for MongoDB is an enhanced, fully compatible, source available, drop-in replacement
for MongoDB {{version}} Community Edition with [enterprise-grade features](../comparison.md).

Find the full list of supported platforms for Percona Server for MongoDB on the [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mongodb) page.

## Install Percona Server for MongoDB basic

You can use any of the easy-install guides. We recommend to use **the package manager of your operating system** for a convenient and quick way to install the software for production use. **Use Docker** to try the software first.

=== ":simple-windowsterminal: Package manager" 

    Use the package manager of your operating system to install Percona Server for MongoDB:

    [on Debian and Ubuntu :material-arrow-right:](apt.md){ .md-button }
    [on RHEL and derivatives :material-arrow-right:](yum.md){ .md-button }

    We gather [Telemetry data](../telemetry.md) in Percona packages.


=== ":simple-docker: Docker"

     Get our Docker image and spin up Percona Server for MongoDB for a quick evaluation. 

     Check the Docker guide for step-by-step guidelines.

     [Run in Docker :material-arrow-right:](docker.md){.md-button}

     We gather [Telemetry data](../telemetry.md) in Docker images.

=== ":simple-kubernetes: Kubernetes"

    **Percona Operator for Kubernetes** is a controller introduced to simplify complex deployments that require meticulous and secure database expertise. 

    Check the Quickstart guides how to deploy and run Percona Server for MongoDB on Kubernetes with Percona Operator for MongoDB.

    [Deploy in Kubernetes Quickstart :material-arrow-right:](https://docs.percona.com/percona-operator-for-mongodb/quickstart.html){.md-button}

=== ":octicons-file-code-16: Build from source"

    Have a full control over the installation by building Percona Server for MongoDB from source code.

    Check the guide below for step-by-step instructions.

    [Build from source :material-arrow-right:](source.md){.md-button}

=== ":octicons-download-16: Manual download"

    If you need to install Percona Server for MongoDB offline or prefer a specific version of it, check out the link below for a step-by-step guide and get access to the downloads directory.

    Note that for this scenario you must make sure that all dependencies are satisfied.

    [Install from tarballs :material-arrow-right:](tarball.md){.md-button}

## Install Percona Server for MongoDB Pro

[Percona Server for MongoDB Pro](../psmdb-pro.md) is available only from Percona repositories. 

[Install Percona Server for MongoDB Pro :material-arrow-right:](install-pro.md){.md-button}

## Upgrade instructions

If you are already using MongoDB, see [Upgrading from MongoDB](upgrade-from-mongodb.md).

If you are running an earlier version of Percona Server for MongoDB, see [Upgrading from Version 6.0](upgrade-from-60.md).

If you wish to upgrade to Percona Server for MongoDB Pro, see [Upgrade to Percona Server for MongoDB Pro](update-pro.md) guide. 


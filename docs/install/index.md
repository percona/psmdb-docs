# Installing Percona Server for MongoDB

Percona provides installation packages of Percona Server for MongoDB for the most 64-bit Linux distributions. Find the full list of supported platforms on the [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mongodb) page.


## System requirements

Percona Server for MongoDB has the same [system requirements](https://www.mongodb.com/docs/v5.0/administration/production-notes/#x86_64) as the MongoDB Community Edition.

Starting in MongoDB 5.0, `mongod`, `mongos`, and the legacy `mongo` shell are supported on x86_64 platforms that must meet these minimum micro-architecture requirements:

* Only Oracle Linux running the Red Hat Compatible Kernel (RHCK) is supported. MongoDB does not support the Unbreakable Enterprise Kernel (UEK).

* MongoDB 5.0 and above requires use of the AVX instruction set, available on 
[select Intel and AMD processors](https://en.wikipedia.org/wiki/Advanced_Vector_Extensions#CPUs_with_AVX). 


### ARM64

Percona Server for MongoDB requires the ARMv8.2-A or later microarchitecture. 

Currently, only [Docker images](https://hub.docker.com/r/percona/percona-server-mongodb/) are available.

## Installation instructions

Choose how you wish to install Percona Server for MongoDB:

* From Percona repositories (recommended):
    
    * [On Debian or Ubuntu](apt.md)
    * [On RHEL or CentOS](yum.md)

* [build from source code](source.md)
* [from binary tarballs](tarball.md)
* Manually from [Percona website](https://www.percona.com/downloads/percona-server-mongodb-4.4/)

   *NOTE*: Make sure that all dependencies are satisfied.

* [Run in a Docker](docker.md).

## Upgrade instructions

If you are currently using MongoDB, see [Upgrading from MongoDB](upgrade-from-mongodb.md#upgrade-from-mongodb).

If you are running an earlier version of Percona Server for MongoDB, see [Upgrading from Version 4.2](upgrade-from-42.md#upgrade-from-42).


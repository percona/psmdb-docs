# System requirements

## x86_64    

Percona Server for MongoDB has the same [system requirements](https://www.mongodb.com/docs/v6.0/administration/production-notes/#x86_64) as the MongoDB Community Edition.     

Starting in MongoDB 5.0, `mongod`, `mongos`, and the legacy `mongo` shell are supported on x86_64 platforms that must meet these minimum micro-architecture requirements:     

* Only Oracle Linux running the Red Hat Compatible Kernel (RHCK) is supported. MongoDB does not support the Unbreakable Enterprise Kernel (UEK).     

* MongoDB 5.0 and above requires use of the AVX instruction set, available on [select Intel and AMD processors](https://en.wikipedia.org/wiki/Advanced_Vector_Extensions#CPUs_with_AVX). 

## ARM64

Percona Server for MongoDB requires the ARMv8.2-A or later microarchitecture. 

Currently, only [Docker images](https://hub.docker.com/r/percona/percona-server-mongodb/) are available.


# System requirements

## x86_64

Percona Server for MongoDB requires the following minimum x86_64 microarchitectures:

* For Intel x86_64, it requires one of the following:
  
   * a *Sandy Bridge* or later Core processor, or
   * a *Tiger Lake* or later Celeron or Pentium processor.

* For AMD x86_64, it requires a *Bulldozer* or later processor.

`mongod` and `mongos` instances are supported on x86_64 platforms that must meet these minimum microarchitecture requirements:     

* Only Oracle Linux running the Red Hat Compatible Kernel (RHCK) is supported. MongoDB does not support the Unbreakable Enterprise Kernel (UEK).     

* MongoDB 5.0 and above require the AVX instruction set, which is available on [select Intel and AMD processors](https://en.wikipedia.org/wiki/Advanced_Vector_Extensions#CPUs_with_AVX). 

## ARM64

Percona Server for MongoDB requires the ARMv8.2-A or later microarchitectures. Support for ARM64 (AARch64) includes [AWS Graviton2 or newer processors](https://aws.amazon.com/ec2/graviton/).﻿

## Ubuntu 26.04

Percona Server for MongoDB 9.0.4-1 **testing packages** are available for Ubuntu 26.04 LTS (Resolute Raccoon) on AMD64 and ARM64. The CPU requirements in the [x86_64](#x86_64) and [ARM64](#arm64) sections also apply.

The packages are in the [Percona Server for MongoDB 9.0 testing
repository](https://repo.percona.com/psmdb-90/apt/pool/testing/p/percona-server-mongodb/).
Select packages whose names contain `9.0.4-1.resolute` and the architecture for your system: `amd64` or `arm64`.

!!! warning
   These are testing packages. Their availability does not indicate a general availability release. See the [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-support-lifecycle#mongodb) for supported production platforms.

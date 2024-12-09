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

# System requirements and compatibility

Before deploying Vector Search in Percona Server for MongoDB (PSMDB), ensure that your environment meets the software, hardware, and deployment requirements for `mongot`.

!!! info "Important"
    The requirements listed below provide the minimum supported configuration. Production environments that handle large collections or high search traffic typically require additional CPU, memory, and storage resources.

## Version compatibility

`mongot` requires Percona Server for MongoDB (PSMDB) version 8.3 or later. Ensure that the `mongot` build you deploy is compatible with the PSMDB version in your environment.

## Operating system support

`mongot` is supported on Linux systems running one of the following processor architectures:

- x86_64 (64-bit x86)
- ARM64 (AArch64)

Verify that your operating system and architecture are supported by the current release of Percona Server for MongoDB before deployment.

## Memory requirements

A minimum of 4 GB of RAM is required to run `mongot`.

Search indexes are maintained in memory whenever possible to improve query performance. Deployments with large collections, high-dimensional vectors, or multiple search indexes may require significantly more memory than the minimum requirement.

## Storage recommendations

Although `mongot` can run on any supported storage device, solid-state drives (SSDs) are strongly recommended for production deployments.

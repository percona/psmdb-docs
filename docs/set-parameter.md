# Percona Server for MongoDB parameter tuning guide

## Disable FTDC metric groups

## Overview

FTDC collects diagnostic samples such as `serverStatus`, `replSetGetStatus`, and Operating System level `systemMetrics`. By default, `systemMetrics` are collected in all environments. This can create significant noise and overhead, as disk and mount statistics are gathered from every available mount point.

When using FUSE, autofs, or NFS, reading disk stats from an unresponsive mount may cause the FTDC thread to enter an **uninterruptible sleep (D-state)**, halting all FTDC sampling until the node is restarted. To prevent this issue, you can disable specific subsections of `systemMetrics` while still collecting all other essential metrics.

## Parameters

Two new server parameters control the collection of disks and mounts subsections within `systemMetrics` in FTDC:

- **diagnosticDataCollectionEnableSystemMetricsDisks**
  - Enables or disables collection of disk level statistics.
  - Type: Boolean (`true`/`false`)
  - Default: `true` (enabled)
  - Scope: Startup; runtime configurable via `setParameter`

- **diagnosticDataCollectionEnableSystemMetricsMounts**
  - Enables or disables collection of mount level statistics.
  - Type: Boolean (`true`/`false`)
  - Default: `true` (enabled)
  - Scope: Startup; runtime configurable via `setParameter`


!!! note
    These parameter applies only to group level targets (e.g.,` systemMetrics`), not to individual keys.


## Configuration Methods

Percona Server for MongoDB includes several parameters that can be changed in one of the following ways:

=== ":octicons-file-code-24: Configuration file"

    Use the `setParameter` admonitions in the configuration file
    for persistent changes in production:    

    ```yaml
    setParameter:
      <parameter>: <value>
    ```
      
    ??? example "Example: diagnosticDataCollectionEnableSystemMetricsDisks set to true"
        ```yaml
        setParameter:
          diagnosticDataCollectionEnableSystemMetricsDisks: true   
        ```


=== ":material-console: Command line"

    use the `--setParameter` command line option arguments when running the `mongod` process
    for development or testing purposes:    

    ```bash
    mongod \
      --setParameter <parameter>=<value>\
    ```

    ??? example "Example: ftdcMetricGroupsDisabled"
        ```bash
        mongod \
          --setParameter                  ftdcMetricGroupsDisabled="systemMetrics,serverStatus.connections"
        ```

=== ":simple-mongodb: `setParameter` command"    

    Use the `setParameter` command on the `admin` database
    to make changes at runtime:    

    ```javascript
    db = db.getSiblingDB('admin')
    db.runCommand( { setParameter: 1, <parameter>: <value> } )
    ```

    ??? example "Example: ftdcMetricGroupsDisabled"
        ```javascript
        db = db.getSiblingDB('admin')
        db.runCommand({ setParameter: 1, ftdcMetricGroupsDisabled: "systemMetrics" } )
        ```

See what parameters you can define in the [parameters list](https://www.mongodb.com/docs/v8.0/reference/parameters/#parameters).


## Comparison: Default vs. tuned FTDC behavior

| Mode                          | Metrics Collected                                                                 | Risks / Overhead                                                                 |
|------------------------------|------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| **Default (no tuning)**      | `systemMetrics`, `serverStatus.connections`, `replSetGetStatus`, plus all other FTDC groups | Full visibility, but it may lead to increased noise and can become unresponsive in FUSE, autofs, or NFS environments. |
| **Tuned (disable `systemMetrics`)** | All FTDC groups except `systemMetrics`                                            | Avoids scanning unstable mount points, reduces risk of diagnostic interruptions |
| **Tuned (disable connections)**   | All FTDC groups except `serverStatus.connections`                                 | Reduces sampling overhead in high throughput environments, external monitoring required for connection details |
| **Tuned (disable `replSetGetStatus`)** | All FTDC groups except `replSetGetStatus`                                     | Useful if replication is monitored elsewhere, may reduce visibility into replica set and cluster health |

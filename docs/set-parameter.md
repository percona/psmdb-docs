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

    ??? example "Example: diagnosticDataCollectionEnableSystemMetricsMounts set to false"
        ```yaml
        setParameter:
          diagnosticDataCollectionEnableSystemMetricsMounts: false   
        ```

=== ":material-console: Command line"

    use the `--setParameter` command line option arguments when running the `mongod` process
    for development or testing purposes:    

    ```bash
    mongod \
      --setParameter <parameter>=<value>\
    ```

    ??? example "Example: diagnosticDataCollectionEnableSystemMetricsDisks set to false"
        ```bash
        mongod \
          --setParameter diagnosticDataCollectionEnableSystemMetricsDisks=false
        ```

           ??? example "Example: diagnosticDataCollectionEnableSystemMetricsMounts set to true"
        ```bash
        mongod \
          --setParameter diagnosticDataCollectionEnableSystemMetricsMounts=true
        ```

=== ":simple-mongodb: `setParameter` command"    

    Use the `setParameter` command on the `admin` database
    to make changes at runtime:    

    ```javascript
    db = db.getSiblingDB('admin')
    db.runCommand( { setParameter: 1, <parameter>: <value> } )
    ```

    ??? example "Example: diagnosticDataCollectionEnableSystemMetricsDisks set to true"
        ```javascript
        db.adminCommand({setParameter: 1, diagnosticDataCollectionEnableSystemMetricsDisks: true})
        ```

    ??? example "Example: diagnosticDataCollectionEnableSystemMetricsMounts set to false"
        ```javascript
        db.adminCommand({setParameter: 1, diagnosticDataCollectionEnableSystemMetricsMounts: false})
        ```

See what parameters you can define in the [parameters list](https://www.mongodb.com/docs/v8.0/reference/parameters/#parameters).


## Comparison: Default vs. tuned FTDC behavior

| Mode                          | Metrics Collected                                                                 | Risks / Overhead                                                                 |
|------------------------------|------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| **Default (no tuning)**      | `systemMetrics` (disks and mounts), `serverStatus.connections`, `replSetGetStatus`, plus all other FTDC groups | Full visibility, but it may lead to increased noise and can become unresponsive in FUSE, autofs, or NFS environments. |
| **Disable disks only** | All FTDC groups except `systemMetrics`  excluding disk-level stats | Reduces overhead while retaining mount level visibility.|
| **Disable mounts only**   | All FTDC groups, with `systemMetrics` excluding mount level stats| Prevents hangs caused by unresponsive mounts, keeps disk level stats.|


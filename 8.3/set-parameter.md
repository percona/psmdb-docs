> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server-for-mongodb/8.3/llms.txt).

# Percona Server for MongoDB parameter tuning guide

## Disable FTDC metric groups

### Overview

FTDC collects diagnostic samples such as `serverStatus`, `replSetGetStatus`, and Operating System level `systemMetrics`. By default, `systemMetrics` are collected in all environments. This can create significant noise and overhead, as disk and mount statistics are gathered from every available mount point.

When using FUSE, autofs, or NFS, reading disk stats from an unresponsive mount may cause the FTDC thread to enter an **uninterruptible sleep (D-state)**, halting all FTDC sampling until the node is restarted. To prevent this issue, you can disable specific subsections of `systemMetrics` while still collecting all other essential metrics.

### Parameters

Two new server parameters control the collection of disks and mounts subsections within `systemMetrics` in FTDC:

- **diagnosticDataCollectionEnableSystemMetricsDisks**

  - Enables or disables collection of disk-level statistics.
  - Type: Boolean (`true`/`false`)
  - Default: `true` (enabled)
  - Scope: Startup; runtime configurable via `setParameter`

- **diagnosticDataCollectionEnableSystemMetricsMounts**

  - Enables or disables collection of mount-level statistics.
  - Type: Boolean (`true`/`false`)
  - Default: `true` (enabled)
  - Scope: Startup; runtime configurable via `setParameter`

## Configuration methods

You can modify parameters in Percona Server for MongoDB using the following methods:

**Configuration file**

Use the `setParameter` admonitions in the configuration file for persistent changes in production:

```
setParameter:
  <parameter>: <value>
```

Example: diagnosticDataCollectionEnableSystemMetricsDisks set to true

```
setParameter:
  diagnosticDataCollectionEnableSystemMetricsDisks: true
```

Example: diagnosticDataCollectionEnableSystemMetricsMounts set to false

```
setParameter:
  diagnosticDataCollectionEnableSystemMetricsMounts: false
```

**Command line**

Use the `--setParameter` command line option arguments when running the `mongod` process for development or testing purposes:

```
mongod \
  --setParameter <parameter>=<value>\
```

Example: diagnosticDataCollectionEnableSystemMetricsDisks set to false

```
mongod \
  --setParameter diagnosticDataCollectionEnableSystemMetricsDisks=false
```

Example: diagnosticDataCollectionEnableSystemMetricsMounts set to true

```
mongod \
  --setParameter diagnosticDataCollectionEnableSystemMetricsMounts=true
```

**setParameter command**

Use the `setParameter` command on the `admin` database to make changes at runtime:

```
db.adminCommand( { setParameter: 1, <parameter>: <value> } )
```

Example: diagnosticDataCollectionEnableSystemMetricsDisks set to true

```
db.adminCommand({setParameter: 1, diagnosticDataCollectionEnableSystemMetricsDisks: true})
```

Example: diagnosticDataCollectionEnableSystemMetricsMounts set to false

```
db.adminCommand({setParameter: 1, diagnosticDataCollectionEnableSystemMetricsMounts: false})
```

See what parameters you can define in the [parameters list](https://www.mongodb.com/docs/v8.0/reference/parameters/#parameters).

## Comparison: Default vs. tuned FTDC behavior

| Mode                    | Metrics Collected                                                                                              | Risks / Overhead                                                                                                                           |
| ----------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Default (no tuning)** | `systemMetrics` (disks and mounts), `serverStatus.connections`, `replSetGetStatus`, plus all other FTDC groups | Provides full visibility, but may lead to increased noise and overhead. FTDC can become unresponsive in FUSE, autofs, or NFS environments. |
| **Disable disks only**  | All FTDC groups, with `systemMetrics` excluding **disk-level stats**                                           | Reduces overhead while retaining mount-level visibility.                                                                                   |
| **Disable mounts only** | All FTDC groups, with `systemMetrics` excluding **mount-level stats**                                          | Avoids interruptions from unresponsive mounts while continuing retaining disk-level visibility.                                            |

# Percona Server for MongoDB parameter tuning guide

## Disable FTDC Metric Groups

FTDC collects diagnostic samples such as `serverStatus`, `replSetGetStatus`, and OS-level `systemMetrics`. In containerized or cloud environments, `systemMetrics` may scan all mount points, creating significant noise and overhead.

When using FUSE, autofs, or NFS, reading disk stats from an unresponsive mount can put the FTDC thread into an uninterruptible sleep (D-state), stopping all FTDC sampling until the node is restarted. Use `ftdcMetricGroupsDisabled` to skip problematic metric groups so FTDC continues collecting all other data.

`ftdcMetricGroupsDisabled`

Disables one or more high-level FTDC groups.

**Type**: Comma-separated string (or list)

**Scope**: Startup; runtime configurable via setParameter (where supported)

Supported targets:

`systemMetrics` (recommended)

`serverStatus.connections`

`replSetGetStatus` (optional)

!!! note
    This parameter applies to group level targets (e.g., `systemMetrics`) only, not individual keys.

Percona Server for MongoDB includes several parameters that can be changed in one of the following ways:

=== ":octicons-file-code-24: Configuration file"

    Use the `setParameter` admonitions in the configuration file
    for persistent changes in production:    

    ```yaml
    setParameter:
      <parameter>: <value>
    ```
      
    For `ftdcMetricGroupsDisabled`


    ```yaml
    setParameter:
    ftdcMetricGroupsDisabled:   
    "systemMetrics,serverStatus.connections"
    ```


=== ":material-console: Command line"

    use the `--setParameter` command line option arguments when running the `mongod` process
    for development or testing purposes:    

    ```bash
    mongod \
      --setParameter <parameter>=<value>\
    ```

    For `ftdcMetricGroupsDisabled`

    ```bash
    mongod \
    --setParameter  ftdcMetricGroupsDisabled="systemMetrics,serverStatus.connections"
    ```



=== ":simple-mongodb: `setParameter` command"    

    Use the `setParameter` command on the `admin` database
    to make changes at runtime:    

    ```javascript
    db = db.getSiblingDB('admin')
    db.runCommand( { setParameter: 1, <parameter>: <value> } )
    ```


    For `ftdcMetricGroupsDisabled`

    ```javascript
    db = db.getSiblingDB('admin')
    db.runCommand( { setParameter: 1, ftdcMetricGroupsDisabled:     "systemMetrics" } )
    ```

See what parameters you can define in the [parameters list](https://www.mongodb.com/docs/v8.0/reference/parameters/#parameters).


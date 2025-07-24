# Log rotation in Percona Server for MongoDB

When you start Percona Server for MongoDB with a `--logpath` or `systemLog.path` setting, it writes logs to a file instead of standard output. These logs include detailed activity and operation information. 

Percona Server for MongoDB has server and [audit logs](audit-logging.md). To maintain system performance, manage disk space, and meet audit and compliance requirements, you must effectively manage these logs. 

Percona Server for MongoDB provides multiple log rotation mechanisms to help you achieve this goal. You can:

- Send a SIGUSR1 signal to the `mongod` or `mongos` process.

- Run the `logRotate` command on `mongosh`. Note that you must connect to each replica set member and start log rotation for it.

- Use the Linux/Unix `logrotate` utility with proper configuration.

## Log rotation considerations

Percona Server for MongoDB does not rotate logs automatically. You must trigger log rotation manually or integrate with external tools like the Linux/Unix `logrotate` utility. Log rotation is not propagated across replica set members; you must rotate logs on each node independently.

## Rotation behavior configuration

Percona Server for MongoDB supports two log rotation strategies:

* `rename` (default): Renames the current log file by appending a UTC timestamp to the file name. This log file is closed. Percona Server for MongoDB creates a new log file and writes all new log entries to this file.
* `reopen`: Closes and reopens the log file, expecting an external process (e.g., `logrotate`) to rename the file beforehand.

You can configure a log rotation behavior using either the `--logRotate` command-line option or the `systemLog.logRotate` setting in the configuration file. 

## Rotation methods

### Manual log rotation with `logRotate`

To rotate log files, do the following:

1. Connect to the `admin` database on each replica set node except the arbiter node and run:

    ```{.javascript data-prompt="<"}
    db.adminCommand({ logRotate: "server" })
    ```       

    Supported options:

    * `server` — rotates only the server log.
    * `audit` — rotates only the audit log.
    * `1` — rotates both server and audit logs.       
    
2. Check log files:

    ```{.bash data-prompt="$"}
    $ ls /var/log/mongodb/server1.log*
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        /var/log/mongodb/server1.log
        /var/log/mongodb/server1.log.<timestamp>
        ```

### Integration with `logrotate`

You can automate log rotation by integrating Percona Server for MongoDB with the Linux/Unix `logrotate` functionality.

Here's how to do it:

1. Create a `logrotate` configuration file at `/etc/logrotate.d/mongod`.

    ```ini
    /var/log/mongo/mongod.log {
       daily
       rotate 7
       compress
       missingok
       notifempty
       create 600 mongod mongod
       postrotate
        /bin/kill -SIGUSR1 $(pidof mongod)
       endscript
}
    }
   ```

2. Configure Percona Server for MongoDB:

    ```yaml
    systemLog:
      destination: file
      path: /var/log/percona/mongod.log
      logAppend: true
      logRotate: reopen
    ```

This setup ensures that Percona Server for MongoDB works seamlessly with logrotate, allowing external rotation and compression of log files.

### Signal-Based Rotation (Unix Systems)

On Unix-based systems, you can trigger log rotation by sending a SIGUSR1 signal to the running `mongod` process:

```{.bash data-prompt="$"}
$ kill -SIGUSR1 <PID>
```

Replace `<PID>` with the process ID of the Percona Server for MongoDB instance.


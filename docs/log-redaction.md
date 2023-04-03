# Log redaction

Percona Server for MongoDB can prevent writing sensitive data to the diagnostic log by redacting messages of events before they are logged.
To enable log redaction, run `mongod` with the `--redactClientLogData` option.

!!! note 

    Metadata such as error or operation codes, line numbers, and source file names remain visible in the logs.

Log redaction is important for complying with security requirements,
but it can make troubleshooting and diagnostics more difficult
due to the lack of data related to the log event.
For this reason, debug messages are not redacted
even when log redaction is enabled.
Keep this in mind when switching between log levels.

You can permanently enable log redaction
by adding the following to the configuration file:

```yaml
security:
  redactClientLogData: true
```

To enable log redaction at runtime,
use the `setParameter` command as follows:

```javascript
db.adminCommand(
  { setParameter: 1, redactClientLogData : true }
)
```
# Percona Server for MongoDB feature comparison

Percona Server for MongoDB 7.0 is based on [MongoDB Community Edition 7.0](https://docs.mongodb.com/manual/introduction/) and extends it with the functionality, that is otherwise only available in MongoDB Enterprise Edition.

|                        | PSMDB  | MongoDB  |
|------------------------| ------ | -------- |
| **Storage Engines**    | - [WiredTiger](https://docs.mongodb.org/manual/core/wiredtiger/) (default) <br> - [Percona Memory Engine](inmemory.md) | - [WiredTiger](https://docs.mongodb.org/manual/core/wiredtiger/) (default) <br>- [In-Memory](https://docs.mongodb.com/v6.0/core/inmemory/) (Enterprise only)|
| **Encryption-at-Rest** | - Key servers = [Hashicorp Vault](vault.md), [KMIP](kmip.md) <br> - Fully open source | - Key server = KMIP <br> - Enterprise only |
| **Hot Backup**         | [YES](hot-backup.md) (replica set) | NO  |
| **LDAP Authentication**| (legacy) [LDAP authentication with SASL](authentication.md) | Enterprise only |
| **LDAP Authorization** | [YES](authorization.md)| Enterprise only |
| **Kerberos Authentication** | [YES](authentication.md)| Enterprise only |
| **AWS IAM authentication** | [YES](aws-iam.md)   | MongoDB Atlas|
| **Audit Logging**      | [YES](audit-logging.md) | Enterprise only |
| **Log redaction**      | [YES](log-redaction.md) | Enterprise only |
| **SNMP Monitoring**    | NO                      | Enterprise only |
| **Database profiler**  | [YES](rate-limit.md) with the [`--rateLimit`](#profiling-rate-limiting) argument | YES

## Profiling Rate Limiting

Profiling Rate Limiting was added to *Percona Server for MongoDB* in v3.4 with the `--rateLimit` argument. Since v3.6, MongoDB Community (and Enterprise) Edition includes a similar option [slowOpSampleRate](https://www.mongodb.com/docs/manual/reference/configuration-options/#mongodb-setting-operationProfiling.slowOpSampleRate). Please see [Profiling Rate Limit](rate-limit.md#rate-limit) for more information.
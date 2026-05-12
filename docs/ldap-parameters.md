# LDAP configuration parameters

Percona Server for MongoDB provides a set of configuration parameters to enable and fine-tune LDAP authentication and authorization.


## User-to-DN cache parameters

To reduce the number of round trips to the LDAP server during authentication and authorization, Percona Server for MongoDB caches the results of LDAP user-to-DN mapping configured by `security.ldap.userToDNMapping` (exposed as `--ldapUserToDNMapping` at startup and `ldapUserToDNMapping` at runtime).

For more details on configuring user-to-DN mapping, see [LDAP authorization](authorization.md#username-transformation) and [Set up LDAP authentication and authorization using NativeLDAP](ldap-setup.md).

The cache is controlled by the following server parameters:

| **Parameter**  | **Required**    | **Description** |
|------------|-------------|-------------| 
| `ldapUserToDNCacheTTLSeconds`   | No         | Specifies how long (in seconds) a cache entry remains valid. Default: `30`. Set to `0` to disable caching. |
| `ldapUserToDNCacheSize`   | No         | Defines the maximum number of entries stored in the cache. Default: `10000`. Set to `0` to disable caching.|


!!! note
    Both parameters can be set at startup and at runtime using `setParameter`.

**Cache invalidation parameters**

The cache is automatically invalidated when any of the following parameters change at runtime:

| **Parameter**                  | **Required** | **Description**                                                |
|-----------------------------|----------|------------------------------------------------------------|
| `ldapUserToDNMapping`       | Yes      | Rules for mapping usernames to LDAP DNs.                   |
| `ldapUserToDNCacheTTLSeconds` | No       | Changing the TTL value clears the cache.                   |
| `ldapUserToDNCacheSize`     | No       | Changing the cache size clears the cache.                  |
| `ldapServers`               | Yes      | Comma-separated list of LDAP servers to connect to.         |
| `ldapQueryUser`             | optional      | Distinguished Name (DN) of the user used to perform LDAP queries. |
| `ldapQueryPassword`         | optional      | Password for the query user.                               |

## Connection pool management parameters

These parameters control how MongoDB maintains its pool of connections to the LDAP server.


| Parameter                                               | Required | Description                                                                                                                  |
| ------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `ldapUseConnectionPool`                                 | No       | Enables/disables connection pooling. Default is OS dependent: `true` on Windows and specific Linux builds using `libldap_r`. |
| `ldapConnectionPoolHostRefreshIntervalMillis`           | No       | Frequency (in ms) of health checks for pooled connections. Default: `60000`. *(This parameter can be applied only when PSMDB starts.)*                                |
| `ldapConnectionPoolIdleHostTimeoutSecs`                 | No       | Seconds a pooled connection can remain idle before being closed. Default: `300`. *(This parameter can be applied only when PSMDB starts.)*                            |
| `ldapConnectionPoolMinimumConnectionsPerHost`           | No       | Minimum number of connections to maintain per LDAP host. Default: `1`. *(This parameter can be applied only when PSMDB starts.)*                                      |
| `ldapConnectionPoolMaximumConnectionsPerHost`           | No       | Maximum number of open connections per LDAP host. Default: `2147483647`. *(This parameter can be applied only when PSMDB starts.)*                                    |
| `ldapConnectionPoolMaximumConnectionsInProgressPerHost` | No       | Limits concurrent “in-progress” connection attempts per host to prevent spikes. Default: `2`. *(This parameter can be applied only when PSMDB starts.)*               |
| `ldapConnectionPoolUseLatencyForHostPriority`           | No       | When `true`, the pool prioritizes connections to hosts with the lowest latency. Default: `TRUE`. *(This parameter can be applied only when PSMDB starts.)*            |

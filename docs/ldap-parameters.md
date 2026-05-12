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

## Connection pool parameters

These parameters control how Percona Server for MongoDB maintains its pool of connections to the LDAP server.


!!! info "Important"
    All Connection Pool parameters except `ldapUseConnectionPool` can be set at **startup only**. They must be defined in the configuration file or via `--setParameter` at launch and cannot be changed via `db.adminCommand()` while the instance is running.


| Parameter                                               | Required | Description                                                                                                                  |
| ------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `ldapUseConnectionPool`                                 | No       | Enables/disables connection pooling. Default is OS dependent: `true` on Windows and specific Linux builds using `libldap_r`. |
| `ldapConnectionPoolHostRefreshIntervalMillis`           | No       | Frequency (in ms) of health checks for pooled connections. Default: `60000`.                                |
| `ldapConnectionPoolIdleHostTimeoutSecs`                 | No       | Seconds a pooled connection can remain idle before being closed. Default: `300`.                           |
| `ldapConnectionPoolMinimumConnectionsPerHost`           | No       | Minimum number of connections to maintain per LDAP host. Default: `1`.                                      |
| `ldapConnectionPoolMaximumConnectionsPerHost`           | No       | Maximum number of open connections per LDAP host. Default: `2147483647`.                                  |
| `ldapConnectionPoolMaximumConnectionsInProgressPerHost` | No       | Limits concurrent **in-progress** connection attempts per host to prevent spikes. Default: `2`.                |
| `ldapConnectionPoolUseLatencyForHostPriority`           | No       | When `true`, the pool prioritizes connections to hosts with the lowest latency. Default: `TRUE`.            |

??? example "MongoDB configuration file (LDAP section)"
    ```sh
    security:
      authorization: enabled
      ldap:
        mode: authzAndAuthn
      # --- Connection Pool Settings (Startup Only) ---
      ldapUseConnectionPool: true
      ldapForceMultiThreadMode: true
      ldapConnectionPoolMinimumConnectionsPerHost: 5
      ldapConnectionPoolMaximumConnectionsPerHost: 100
      ldapConnectionPoolIdleHostTimeoutSecs: 600
    ```

## LDAP cache refresh parameters

As of **version 8.0.20-8**, Percona Server for MongoDB introduced parameters to optimize authentication performance and reduce unnecessary load on the LDAP server. These settings control how cached user information is refreshed, allowing administrators to fine-tune the balance between maintaining up-to-date user data and minimizing LDAP query overhead—especially in high-scale environments with many concurrent users.


| **Parameter**                       | **Required** | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ----------------------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ldapUserCacheRefreshInterval`      | No           | Defines how often (in seconds) the server refreshes cached user information from LDAP when interval-based refresh is enabled through `ldapShouldRefreshUserCacheEntries=true`. If not explicitly configured, Percona Server for MongoDB uses the built-in default for the server version. Can be configured at startup and runtime.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `ldapShouldRefreshUserCacheEntries` | No           | Selects the LDAP user cache refresh strategy. <br><br> - When set to `true`, each cached `$external` user is periodically re-fetched from the LDAP server at the interval defined by `ldapUserCacheRefreshInterval`. The cache is updated only if the user’s roles have changed; otherwise, existing entries remain untouched, ensuring no disruption. If a user no longer exists in LDAP, their cache entry is invalidated individually. <br><br> - When set to `false`, all `$external` users are evicted from the cache at intervals defined by `ldapUserCacheInvalidationInterval`. This preserves the behavior that existed prior to the introduction of `ldapUserCacheRefreshInterval` and `ldapShouldRefreshUserCacheEntries`. <br><br> Default: `false` (expiration-based invalidation using `ldapUserCacheInvalidationInterval`) to maintain backward-compatible behavior unless interval-based refreshing is explicitly enabled. The default value will change to `true` in all major versions released after March 1, 2026. <br><br> This parameter can be configured at startup only.|
| `ldapUserCacheInvalidationInterval` | No           | Defines the interval between total external user cache flushes. Cached LDAP user entries are evicted after this interval and are re-acquired from LDAP on the next operation. Default: `30s`. This parameter can be configured at startup and runtime.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `ldapUserCacheStalenessInterval`    | No           | Defines how long `mongod` retains cached LDAP user information after a failed refresh attempt before invalidating the cache entry. Maximum allowed value: `86400s`. Default: `30s`. This parameter can be configured at startup and runtime. |

??? example "Interval-based refresh: `ldapShouldRefreshUserCacheEntries: true` "

    === "Runtime (setParameter)"

        ```{.javascript data-prompt=">"}
        > db.adminCommand({
        ...   setParameter: 1,
        ...   ldapUserCacheRefreshInterval: 300
        ... })
        ```

    === "Command line"

        ```bash
        mongod --setParameter "ldapUserCacheRefreshInterval=300" \
                --setParameter "ldapShouldRefreshUserCacheEntries=true"
        ```

    === "Configuration file"

        ```yaml
        setParameter:
        ldapUserCacheRefreshInterval: 300
        ldapShouldRefreshUserCacheEntries: true
        ```

??? example "Expiration-based invalidation: `ldapShouldRefreshUserCacheEntries: false`"


    === "Runtime (setParameter)"

        ```{.javascript data-prompt=">"}
        > db.adminCommand({
        ...   setParameter: 1,
        ...   ldapUserCacheInvalidationInterval: 30
        ... })
        ```

    === "Command line"

        ```bash
        mongod --setParameter "ldapUserCacheInvalidationInterval=30" \
                --setParameter "ldapShouldRefreshUserCacheEntries=false"
        ```

    === "Configuration file"

        ```yaml
        setParameter:
        ldapUserCacheInvalidationInterval: 30
        ldapShouldRefreshUserCacheEntries: false
        ```


## Security and concurrency parameters

These parameters are used for LDAP server authentication, secure connection handling, and ensuring thread-safe operations during concurrent access.

| **Parameter**              | **Required** | **Description**                                                                                                                              |
| -------------------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `ldapQueryUser`            | No           | Specifies the DN (Distinguished Name) of the user that binds to the LDAP server. Default: `N/A`.                                             |
| `ldapQueryPassword`        | No           | Specifies the password for `ldapQueryUser`. Default: `N/A`.                                                                                  |
| `ldapForceMultiThreadMode` | No           | Enables concurrent LDAP operations. Required for connection pooling. Use only with a thread-safe `libldap` implementation. Default: `FALSE`. |
| `ldapRetryCount`           | No           | Specifies the number of times the server retries an LDAP operation after a network error. Default: `0`.                                      |


??? example "MongoDB configuration file: Performance and retries"

    ```sh
    security:
      authorization: enabled
      ldap:
        mode: authzAndAuthn
      # --- Performance & Retries ---
      ldapRetryCount: 3
    ```




# LDAP configuration parameters

Percona Server for MongoDB provides a set of configuration parameters to enable and fine-tune LDAP authentication and authorization.


## userToDN cache parameters

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

| **Parameter** | **Required** | **Description** |
|--------------|----------|---------------------|
| `ldapUserToDNMapping`       | Yes      | Rules for mapping usernames to LDAP DNs.                   |
| `ldapUserToDNCacheTTLSeconds` | No       | Changing the TTL value clears the cache.                   |
| `ldapUserToDNCacheSize`     | No       | Changing the cache size clears the cache.                  |
| `ldapServers`               | Yes      | Comma-separated list of LDAP servers to connect to.         |
| `ldapQueryUser`             | No      | Distinguished Name (DN) of the user used to perform LDAP queries. |
| `ldapQueryPassword`         | No      | Password for the query user. |


## Monitor userToDNCache

Percona Server for MongoDB exposes LDAP userToDN cache statistics in the `db.serverStatus()` output when the server is configured to use LDAP authentication with `--ldapServers`.

The `ldap.userToDNCache` document reports the status and performance of the in-memory Least Recently Used (LRU) cache that maps LDAP usernames to Distinguished Names (DNs). You can use this information to verify whether the cache is enabled, monitor cache usage, and identify whether LDAP lookups are being served from cache or sent to the LDAP server.

### View LDAP userToDN cache statistics

Run the following command:

```javascript
db.serverStatus().ldap.userToDNCache
```

??? example "Output"
    ```{.json .no-copy}
    {
      "enabled": true,
      "maxSize": 10000,
      "currentSize": 42,
      "ttlSeconds": 30,
      "hits": 1847,
      "misses": 63,
      "invalidations": 2
    }
    ```

The following table describes the fields returned in the `ldap.userToDNCache` document.

| **Field** | **Description** |
|-------|-------------|
| `enabled` | Indicates whether the LDAP user-to-DN cache is active.<br><br>The cache is disabled when either `ldapUserToDNCacheTTLSeconds` or `ldapUserToDNCacheSize` is set to `0`.<br><br>When disabled, all user-to-DN lookups are sent directly to the LDAP server. |
| `maxSize` | The maximum number of `username-to-DN mappings` that can be stored in the cache.<br><br>Corresponds to the `ldapUserToDNCacheSize` server parameter.<br><br>When the cache reaches this limit, the least recently used entry is evicted.|
| `currentSize` | The current number of `username-to-DN` mappings stored in the cache. |
| `ttlSeconds` | The time-to-live (TTL) for cache entries, in seconds.<br><br>Corresponds to the `ldapUserToDNCacheTTLSeconds` server parameter.<br><br>Entries older than this value are treated as expired and are not served from the cache. |
| `hits` | The number of `mapUserToDN` lookups served from the cache since the last cache invalidation.|
| `misses` | The number of `mapUserToDN` lookups not served from the cache since the last cache invalidation.<br><br>A miss occurs when an entry is missing or has expired.|
| `invalidations` | The total number of cache invalidations since server startup.<br><br>Unlike `hits` and `misses`, this counter does not reset. |

!!! note
    The `hits` and `misses` counters reset to `0` on each cache invalidation. `invalidations` never resets.

### Calculate the cache hit rate

You can calculate the hit rate for the current cache generation using the following command:

```javascript
var c = db.serverStatus().ldap.userToDNCache;
var total = c.hits + c.misses;
var hitRate = total > 0 ? c.hits / total : null;
```

A higher hit rate means more LDAP `userToDN` lookups are served from cache, reducing requests to the LDAP server.

!!! note
    If `hits` and `misses` drop sharply and `invalidations` increases, an LDAP-related runtime parameter was likely changed. This does not necessarily indicate degraded cache performance.






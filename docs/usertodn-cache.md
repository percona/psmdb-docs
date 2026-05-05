# LDAP UserToDN cache

To reduce the number of round-trip requests to the LDAP server during authentication and authorization, Percona Server for MongoDB caches the results of LDAP user-to-DN mapping. The mapping is configured using one of the following, depending on the context:

| Context | Name |
|---|---|
| Configuration file (`mongod.conf`) | `security.ldap.userToDNMapping` |
| Command-line option (startup) | `--ldapUserToDNMapping` |
| Runtime (`setParameter`) | `ldapUserToDNMapping` |

For more details on configuring user-to-DN mapping, see [LDAP authorization](authorization.md#username-transformation) and [Set up LDAP authentication and authorization using NativeLDAP](ldap-setup.md).

The cache is controlled by the following server parameters:

- `ldapUserToDNCacheTTLSeconds`: Specifies how long (in seconds) a cache entry remains valid.
    - Default: `30`
    - Set to `0` to disable TTL-based expiration. In this case, entries remain in the cache until it reaches its size limit or is explicitly invalidated.

- `ldapUserToDNCacheSize`: Defines the maximum number of entries stored in the cache.
    - Default: `10000`
    - Set to `0` to disable the cache entirely regardless of the TTL setting.

!!! note
    Caching is disabled when `ldapUserToDNCacheSize` is `0`. If only `ldapUserToDNCacheTTLSeconds` is `0`, the cache remains active but entries do not expire based on time. Both parameters can be set at startup and at runtime using `setParameter`.

## Cache invalidation

The cache is automatically invalidated when any of the following parameters change at runtime:

- `ldapUserToDNMapping`

- `ldapUserToDNCacheTTLSeconds`

- `ldapUserToDNCacheSize`

- `ldapServers`

- `ldapQueryUser`

- `ldapQueryPassword`

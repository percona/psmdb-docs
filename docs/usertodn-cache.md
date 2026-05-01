# LDAP UserToDN cache

To reduce the number of round trips to the LDAP server during authentication and authorization, Percona Server for MongoDB caches the results of LDAP user-to-DN mapping configured by `security.ldap.userToDNMapping` (exposed as `--ldapUserToDNMapping` at startup and `ldapUserToDNMapping` at runtime).

The cache is controlled by the following server parameters:

- `ldapUserToDNCacheTTLSeconds`: Specifies how long (in seconds) a cache entry remains valid.
    - Default: `30`
    - Set to `0` to disable caching.

- `ldapUserToDNCacheSize`: Defines the maximum number of entries stored in the cache.
    - Default: `10000`
    - Set to `0` to disable caching.

!!! note
    Both parameters can be set at startup and at runtime using `setParameter`.

## Cache invalidation

The cache is automatically invalidated when any of the following parameters change at runtime:

- `ldapUserToDNMapping`

- `ldapUserToDNCacheTTLSeconds`

- `ldapUserToDNCacheSize`

- `ldapServers`

- `ldapQueryUser`

- `ldapQueryPassword`

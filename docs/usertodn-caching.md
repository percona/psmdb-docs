# LDAP UserToDN cache

To reduce the number of round trips to the LDAP server during authentication and authorization, Percona Server for MongoDB caches the results of `LDAPManagerImpl::mapUserToDN()`.

Cache is controlled by the following server parameters:

- `ldapUserToDNCacheTTLSeconds`: Specifies how long (in seconds) a cache entry remains valid.

    - Default: `30`
    - Set to `0` to disable caching.

- `ldapUserToDNCacheSize`: Defines the maximum number of entries stored in the cache.
    - Default: `10000`
    - Set to `0` to disable caching.

!!! note
    Both the parameters can be set at startup and at runtime using `setParameter`.

## Synchronization

The cache uses two synchronization mechanisms:

- `synchronized_value`: Protects the cache configuration snapshot, minimizing blocking during configuration changes.

- Inner Mutex: Serializes concurrent cache access from `mapUserToDN()` calls.

## Cache invalidation

The cache is automatically invalidated when any of the following parameters change at runtime:

- `ldapUserToDNMapping`

- `ldapUserToDNCacheTTLSeconds`

- `ldapUserToDNCacheSize`

- `ldapServers`

- `ldapQueryUser`

- `ldapQueryPassword`







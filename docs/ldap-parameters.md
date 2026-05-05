# LDAP configuration parameters

Percona Server for MongoDB provides a set of configuration parameters to enable and fine‑tune LDAP authentication and authorization.


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

### Cache invalidation parameters

The cache is automatically invalidated when any of the following parameters change at runtime:

| Parameter                  | Required    | Description                                                |
|-----------------------------|-------------|------------------------------------------------------------|
| `ldapUserToDNMapping`       | Yes         | Rules for mapping usernames to LDAP DNs.                   |
| `ldapUserToDNCacheTTLSeconds` | No          | Changing the TTL value clears the cache.                   |
| `ldapUserToDNCacheSize`     | No          | Changing the cache size clears the cache.                  |
| `ldapServers`               | Yes         | Comma-separated list of LDAP servers to connect to.        |
| `ldapQueryUser`             | Conditional | DN of the user used to perform LDAP queries when anonymous binds are disabled; corresponds to `security.ldap.bind.queryUser` in the configuration file. |
| `ldapQueryPassword`         | Conditional | Password for the query user when anonymous binds are disabled; corresponds to `security.ldap.bind.queryPassword` in the configuration file. |


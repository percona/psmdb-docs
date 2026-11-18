# LDAP configuration parameters

Use these parameters to tune LDAP authentication and authorization in Percona
Server for MongoDB. Configure LDAP first with the
[NativeLDAP configuration guide](ldap-setup.md).

The server parameters on this page apply to `mongod` and `mongos` with LDAP
configured. Unless a section specifies another version, the parameters are
available throughout the Percona Server for MongoDB 8.0 series.

For startup settings, use the configuration file or command-line options.
For runtime changes, use the [`setParameter` command](set-parameter.md).
Runtime changes affect only the instance that receives the command.
Add persistent settings to each instance's configuration file.

## userToDN cache parameters

The userToDN cache requires Percona Server for MongoDB 8.0.21-9 or later.
The cache stores username-to-distinguished-name (DN) results to reduce LDAP
queries during authentication and authorization.

Configure transformation rules through `security.ldap.userToDNMapping`.
For rule syntax, see [Username transformation](authorization.md#username-transformation).

These optional integer parameters control the cache at startup and runtime:

| Parameter | Default | Accepted values and effect |
| --- | --- | --- |
| `ldapUserToDNCacheTTLSeconds` | `30` | Seconds that a cache entry remains valid. Range: `0`–`86400`. Set `0` to disable the cache. |
| `ldapUserToDNCacheSize` | `10000` | Maximum number of cached entries. Range: `0`–`1000000`. Set `0` to disable the cache. |

For example, add these settings to your LDAP-enabled instance's configuration file:

```yaml
setParameter:
  ldapUserToDNCacheTTLSeconds: 60
  ldapUserToDNCacheSize: 20000
```

## userToDN cache invalidation

The server clears the userToDN cache when you change any of these parameters at runtime:

| Parameter | Effect of the change |
| --- | --- |
| `ldapUserToDNMapping` | Replaces the username transformation rules. |
| `ldapUserToDNCacheTTLSeconds` | Changes the cache entry lifetime. |
| `ldapUserToDNCacheSize` | Changes the cache capacity. |
| `ldapServers` | Changes the LDAP server list and invalidates LDAP connections. |
| `ldapQueryUser` | Changes the bind user and invalidates LDAP connections. |
| `ldapQueryPassword` | Changes the bind password and invalidates LDAP connections. |

## Connection pool parameters

Percona Server for MongoDB always uses a connection pool for LDAP bind requests.
The default pool size is two connections.
The `ldapUseConnectionPool` setting does not disable Percona Server for MongoDB's
connection pool.

Use this optional parameter to change the pool size at startup or runtime:

| Parameter | Type | Default | Accepted values and effect |
| --- | --- | --- | --- |
| `ldapConnectionPoolSizePerHost` | Integer | `2` | Positive integer that controls the LDAP connection pool size. |

For example, set the pool size to five connections:

=== "Runtime"

    ```javascript
    db.adminCommand({setParameter: 1, ldapConnectionPoolSizePerHost: 5})
    ```

=== "Configuration file"

    ```yaml
    setParameter:
      ldapConnectionPoolSizePerHost: 5
    ```

## LDAP cache refresh parameters

The LDAP user cache stores user authorization information.
The userToDN cache stores username-to-DN results.
The server periodically invalidates cached `$external` users by default.
Subsequent operations retrieve the user information again.

Percona Server for MongoDB 8.0.20-8 or later also supports periodic refresh.
Set `ldapShouldRefreshUserCacheEntries` to `true` at startup to select refresh
instead of periodic invalidation.
The server checks cached `$external` users at each refresh interval.
The server replaces entries when their roles change.
The server invalidates entries for users that no longer exist.
If the refresh fails, the server invalidates all cached `$external` users.

These optional parameters control the strategy and its interval:

| Parameter | Type | Default | Availability | Accepted values and effect |
| --- | --- | --- | --- | --- |
| `ldapShouldRefreshUserCacheEntries` | Boolean | `false` | 8.0.20-8 or later; startup only | `true` selects periodic refresh. `false` selects periodic invalidation. |
| `ldapUserCacheRefreshInterval` | Integer | `30` | 8.0.20-8 or later; startup and runtime | Refresh interval in seconds when `ldapShouldRefreshUserCacheEntries` is `true`. Range: `1`–`86400`. |
| `ldapUserCacheInvalidationInterval` | Integer | `30` | Throughout the 8.0 series; startup and runtime | Invalidation interval in seconds when `ldapShouldRefreshUserCacheEntries` is `false`. For version 8.0.20-8 or later, the accepted range is `1`–`86400`. |

Shorter intervals increase LDAP query frequency.
Longer intervals can delay updates to cached authorization information.

### Periodic refresh

To enable periodic refresh, add these settings to your configuration file before
you start the instance:

```yaml
setParameter:
  ldapShouldRefreshUserCacheEntries: true
  ldapUserCacheRefreshInterval: 300
```

For an instance that uses periodic refresh, change the interval at runtime with this command:

```javascript
db.adminCommand({
  setParameter: 1,
  ldapUserCacheRefreshInterval: 300
})
```

The runtime command changes only the interval.
The startup setting controls the refresh strategy.

### Periodic invalidation

To retain periodic invalidation, use these startup settings:

```yaml
setParameter:
  ldapShouldRefreshUserCacheEntries: false
  ldapUserCacheInvalidationInterval: 30
```

For an instance that uses periodic invalidation, change the interval at runtime
with this command:

```javascript
db.adminCommand({
  setParameter: 1,
  ldapUserCacheInvalidationInterval: 60
})
```

## LDAP server and bind parameters

These parameters control LDAP server selection, credentials, and username
transformation. Use their `security.ldap` configuration options at startup.
Use the server parameter names with `setParameter` at runtime.
Do not place these runtime-only parameter names under `setParameter` in a startup
configuration file.

| Runtime parameter | Startup configuration option | Type and default | Purpose |
| --- | --- | --- | --- |
| `ldapServers` | `security.ldap.servers` | String; empty by default | Comma-separated LDAP server addresses in `host:port` format. Configure the servers for your LDAP deployment. |
| `ldapQueryUser` | `security.ldap.bind.queryUser` | String; empty by default | Bind account used for LDAP queries, such as a DN for simple binds. |
| `ldapQueryPassword` | `security.ldap.bind.queryPassword` | String; empty by default | Password for the bind account. |
| `ldapUserToDNMapping` | `security.ldap.userToDNMapping` | String that contains a JSON array; default `[{match: "(.+)", substitution: "{0}"}]` | Rules that transform usernames into DNs. The default leaves the username unchanged. |
| `ldapTimeoutMS` | `security.ldap.timeoutMS` | Integer; default `10000` | Timeout in milliseconds for LDAP responses. |

For bind configuration and credentials, follow the
[NativeLDAP configuration guide](ldap-setup.md).
For TLS settings, see [Transport security](ldap-setup.md#configure-tlsssl-connection-for-percona-server-for-mongodb).

The following optional parameters support startup and runtime changes through
`setParameter`:

| Parameter | Type | Default | Effect |
| --- | --- | --- | --- |
| `ldapFollowReferrals` | Boolean | `false` | Allows LDAP referrals with the same bind credentials when `true`. See [LDAP referrals](authorization.md#ldap-referrals). |
| `ldapDebug` | Boolean | `false` | Enables LDAP connection debug information when `true`. |

*[DN]: Distinguished Name

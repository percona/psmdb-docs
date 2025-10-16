# Setting up OIDC authentication and LDAP authorization

You can use OIDC authentication and LDAP authorization together. For example, in hybrid environments where modern applications are integrated with some legacy systems. Or, if your organization has strict user access management requirements.

You can also use both solutions in parallel. For example, to have a pool of users to both authenticate and authorize in the LDAP server, while the remaining ones pass OIDC authentication and are then authorized in the LDAP server. What flow to use is determined by the authentication mechanism in Percona Server for MongoDB configuration and in the MongoDB connection string URL. 

This document primarily focuses on configuring OIDC to authenticate users and using LDAP server for their authorization. 

## Prerequisites

1. Percona Server for MongoDB 8.0.12-4 or the Regular builds with the OIDC feature enabled. 
2. Access to an IdP administrative console
3. LDAP server up and running and it's accessible to the servers with Percona Server for MongoDB installed.

## Procedure 

To configure OIDC authentication and LDAP authorization, complete the following steps:

1. Configure an IdP provider. Refer to the [OIDC Configuration](oidc.md#configuration) section and then use the corresponding tutorial for the IdP of your choice.
2. Set up LDAP server and define users and roles there. 
    
    !!! note 

        The LDAP server setup is out of scope of this document. We assume that you are familiar with the LDAP server schema.

3. [Configure TLS/SSL connection for Percona Server for MongoDB](ldap-setup.md#configure-tlsssl-connection-for-percona-server-for-mongodb)
4. Create roles for LDAP groups in Percona Server for MongoDB
5. Configure Percona Server for MongoDB 
6. Authenticate and authorize users in Percona Server for MongoDB

--8<-- "ldap-setup.md:roles"

### Percona Server for MongoDB configuration

If your users connect to Percona Server for MongoDB with usernames that are not LDAP Distinguished Names (DN), you must transform the usernames so that LDAP server accepts them. Also, you must [escape special characters](ldap-setup.md#escaping-special-characters) if usernames contain them.

To transform usernames into LDAP DN, use the `userToDNMapping` configuration option. Specify the match pattern as a regexp to capture the name. Next, specify how to transform it - either to use a substitution value or to query the LDAP server for a username.

If you don't know what the Substitution or LDAP query string should be, please consult with the LDAP administrators to figure this out.

For this configuration example, we assume the following:

* Users authenticate with usernames matching their email addresses. 
* The LDAP server stores user entries under the organizational unit `ou=people,dc=perconatest,dc=com`, with each user identified by a `cn` equal to the local part of their email (i.e., the portion before `@perconatest.com`).
* The username is transformed using a substitution value

1. Edit the `etc/mongod.conf` configuration file and specify both the OIDC and LDAP configuration:

    ```yaml
    security:
      authorization: enabled
      ldap:
        transportSecurity: tls
        servers: "ldap.example.com"
        userToDNMapping: '[{match: "^[^/]+/([^@]+)@perconatest.com$", substitution: "cn={0},ou=people,dc=perconatest,dc=com"}]'
        authz:
          queryTemplate: 'dc=perconatest,dc=com??sub?(&(objectClass=groupOfNames)(member={USER}))'
    setParameter:
       authenticationMechanisms: SCRAM-SHA-1,MONGODB-OIDC, PLAIN
       oidcIdentityProviders: '[{
          "issuer": "https://myokta.oktapreview.com/oauth2/0oatxj71cmQfzQ9Us697",
          "authNamePrefix": "okta",
          "audience": "audience",
          "clientId": "0oatxj71cmQfzQ9Us697",
          "useAuthorizationClaim": false,
          "matchPattern": "@perconatest.com$",
          "authorizationClaim": "psmdb_test_claim",
          "supportsHumanFlows": true}]'
    ```

2. Restart Percona Server for MongoDB to apply the changes.

	```{.bash data-prompt="$"}
    $ sudo systemctl restart mongod
	```

In this configuration, Percona Server for MongoDB receives the usernames in the format `authNamePrefix/email` (e.g. `okta/testuser@perconatest.com`). The `userToDNMapping` option contains a regular expression to match usernames, extract the local part of the email and substitute the `cn` part of the LDAP DN with it. Then the transformed username is added to the LDAP query to retrieve groups where the `testuser` is listed as a member. These groups are mapped to roles you created in Percona Server for MongoDB at the previous step.


### Authenticate and authorize users

The `authenticationMechanisms` parameter contains authentication mechanisms to use when authenticating users. Then, depending on which authentication mechanism is specified in the MongoDB connection string URL, users are authenticated either with OIDC (`MONGODB-OIDC`) or with LDAP (`PLAIN`).

1. To authenticate users with OIDC, run the following command:

    ```{.bash data-prompt="$"}
    $ mongosh -u "testuser@perconatest.com" --authenticationMechanism MONGODB-OIDC
    ```

2. Pass authentication

3. Upon successful authentication, check connection status:

    ```{.javascript data-prompt="test>"}
    test> db.runCommand({connectionStatus : 1})
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        {
          authInfo: {
            authenticatedUsers: [
              { user: 'okta/testuser@perconatest.com', db: '$external' }
            ],
            authenticatedUserRoles: [
              {
                role: 'cn=testreaders,ou=groups,dc=perconatest,dc=com',
                db: 'admin'
              },
              { role: 'read', db: 'admin' }
            ]
          },
          ok: 1
        }
        ```

To authenticate users in the LDAP server, run the following command:

```{.bash data-prompt="$"}
$ mongosh -u "testuser@perconatest.com" --authenticationMechanism PLAIN
```



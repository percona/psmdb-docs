# Configure OIDC authentication with Keycloak

This document focuses on configuring OIDC authentication for Percona Server for MongoDB deployment using [Keycloak :octicons-link-external-16:](https://www.keycloak.org/) as the identity provider.

The setup process consists of three main stages:

1. IdP setup:

    * Create a new realm in KeyCloak
    * Create and configure an OIDC client
    * Create users and groups

2. Configure Percona Server for MongoDB to use OIDC as authentication method
3. Connect to Percona Server for MongoDB using OIDC authentication

## Prerequisites

1. Percona Server for MongoDB 8.0.12-4 or later.
2. Keycloak server up and running. Use any installation method you prefer, such as Docker, Kubernetes, or a standalone server. Check [Keycloak Get started documentation :octicons-link-external-16:](https://www.keycloak.org/guides#getting-started) for installation guidelines. 
3. Keycloak and Percona Server for MongoDB must be able to communicate with each other over the network. Refer to the [Configuring Keycloak for production :octicons-link-external-16:](https://www.keycloak.org/server/configuration-production) guide for more information

    In the following commands we use a Keycloak server running at `https://my.keycloak.org`.

## Identity provider setup

### Create a new realm in Keycloak

1. Open the Keycloak admin console at `https://my.keycloak.org:8080/admin/master/console` and log in with your admin credentials
2. In the left navigation pane, click on **Manage Realms**.
3. Click **Create Realm**.
4. Fill in the realm details:

    * Specify the name for your realm. For example, `mongodb`.
    * Check **Enabled**.
    * Click **Create** to create the realm.

### Create an OIDC client

1. In the left navigation pane, click on **Clients**.
2. Click **Create Client**.
3. Fill in the client details on the **General Settings** tab:

	* **Client type**: Select **OpenID Connect**.
	* **Client Id**: Specify the client identifier. For example, `mongodb-client`.
	* Click **Next**.

4. In **Capability config** tab, select the following options for the **Authentication flow**:
    
    * **Standard flow** for Authorization Code flow
    * **OAuth 2.0 Device Authorization Grant** for Device authorization flow
    * Click **Next**.

5. In **Login Settings**, for **Valid redirect URIs** specify `http://localhost:27097/redirect`.
6. Click **Save**.

### Configure the OIDC client

1. While on the client settings page, go to **Client scopes**.
2. Click `mongodb-client-dedicated`
3. On the **Mappers** tab, click **Add mapper** > **By configuration**
4. Fill in the mapper details:

	* **Mapper Type**: Select **Group Membership**.
	* **Name**: Set it to `group-membership-mapper`.
	* **Token Claim Name**: Set it to `MyClaim`. Setting a Token Claim Name is required; without this field the claim will not appear in the access token.
	* **Add to access token**: Set it to **On**.
	* Click **Save**.

5. Add a mapper for the audience. Click **Add mapper** > **By configuration**.
6. Fill in the mapper details:

	* **Mapper Type**: Select **Audience**.
	* **Name**: Provide a descriptive name for the mapper.
	* **Included Client Audience**: Select your client (`mongodb-client` in our example)
	* **Add to access token**: Set it to **On**.
	* Click **Save**.

### Add users and groups

Groups define user access rights to resources. Identity provider groups are then mapped to roles in Percona Server for MongoDB to authorize users to access the database.

1. Create groups as described in the [Groups :octicons-link-external-16:](https://www.keycloak.org/docs/latest/server_admin/index.html#proc-managing-groups_server_administration_guide) section of the Keycloak documentation. 
2. Create users as described in the [Creating users :octicons-link-external-16:](https://www.keycloak.org/docs/latest/server_admin/index.html#creating-user_server_administration_guide) section of the Keycloak documentation. 

	When creating users, ensure you:

	* Set **Email Verified** to `On`.
	* Use an email address as the username.
	* Assign the user to the group you created earlier.

## Configure Percona Server for MongoDB to use OIDC

Now you need to configure authentication in Percona Server for MongoDB. Specify the external identity provider configuration for the `oidcIdentityProviders` server parameter either via the configuration file or the command line. 

The following table maps the Keycloak configuration parameters to the Percona Server for MongoDB configuration:

| Keycloak Parameter        | Percona Server for MongoDB Parameter |
| ------------------------- | ------------------------------------ |
| `Client Id`               | `clientID`, <br> `audience`          |
| `Token Claim Name`        | `authorizationClaim`                 |

The `issuer` URL has the format `https://hostname:8443/realms/realm-name`. So if you created a realm named `mongodb`, the URL will be `https://my.keycloak.org:8443/realms/mongodb.`

=== "Configuration file"

    1. Edit the `/etc/mongod.conf` configuration file:

        ```yaml
        security:
           authorization: enabled
        setParameter:
           authenticationMechanisms: MONGODB-OIDC
           oidcIdentityProviders: '[ {
              "issuer": "https://my.keycloak.org:8443/realms/mongodb",
              "audience": "mongodb-client",
              "authNamePrefix": "keycloak",
              "clientId": "mongodb-client",
              "useAuthorizationClaim": true,
              "supportsHumanFlows": true,
              "authorizationClaim": "MyClaim"
           } ]'
        ```
    
    2. Start or restart Percona Server for MongoDB:

        ```bash
        sudo systemctl start mongod
        ```

=== "Command line"

    ```bash
    mongod --auth --setParameter authenticationMechanisms=MONGODB-OIDC --setParameter \
    'oidcIdentityProviders=[ {
       "issuer": "https://my.keycloak.org:8443/realms/mongodb",
       "audience": "mongodb-client",
       "authNamePrefix": "keycloak",
       "clientId": "mongodb-client",
       "useAuthorizationClaim": true,
       "supportsHumanFlows": true,
       "authorizationClaim": "MyClaim"
    } ]'
    ```

The `useAuthorizationClaim` configuration option defines how your users are authorized.

* When set to `true`, users are authorized using identity provider groups. Users are created and stored on the IdP side.
* When set to `false`, users are authorized by their usernames in the `$external` database in Percona Server for MongoDB. When using `useAuthorizationClaim: false`, **do not** specify `authorizationClaim`.

## Create user roles 

To enable users to access Percona Server for MongoDB, you must create roles and define privileges for them. 

The role name must match the identity provider group name and must have the prefix that matches the `authNamePrefix` in Percona Server for MongoDB configuration.

For example, to create a role for the default group `Everyone` in Keycloak and with the `authNamePrefix` set to `keycloak`, use the following command:

```javascript
db.getSiblingDB("admin").createRole({
  role: "keycloak/Everyone",
  privileges: [ ],
  roles: [ "readWriteAnyDatabase" ]
})
```

Create roles for all groups you have defined in Keycloak.

## Create users 

**Complete this step if you set `useAuthorizationClaim` to `false`**

Create users in the `$external` database. The username must consist of the `authNamePrefix` and the email that you specified when you created users in Keycloak. The username format is:

```
authNamePrefix/email
```

If you set the `authNamePrefix` to `keycloak`, then the command to create a user is the following:

```javascript
db.getSiblingDB("$external").createUser({
  user: "keycloak/john.doe@example.com",
  roles: [
    { role: "keycloak/Everyone", db: "admin" } 
  ]
})
```

## Authenticate in Percona Server for MongoDB

### Authorization Code flow

1. Connect to Percona Server for MongoDB:

    ```bash
    mongosh  --authenticationMechanism MONGODB-OIDC --oidcFlows auth-code
    ```

2. You will be redirected to the Keycloak login page in your web browser. 
3. Log in with your credentials.
4. Upon successful authentication, you will see a confirmation message. In your MongoDB client, you should see the output as follows:

    ```{.text .no-copy}
    Using MongoDB:      {{release}}
    Using Mongosh:      {{mongosh}}

    For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/

    test>
    ```

### Device Authorization flow

1. Connect to Percona Server for MongoDB:

    ```bash
    mongosh  --authenticationMechanism MONGODB-OIDC --oidcFlows device-auth
    ```

    ??? example "Sample output"

        ```
        Visit the following URL to complete authentication: https://my.keycloak.org:8443/realms/mongodb/device
        Enter the following code on that page: CSXP-ZTSJ
        Waiting...
        ```

2. Open the URL in your web browser and enter the code displayed in the terminal.
3. Approve the sign in request.
4. Upon successful authentication, you will see a confirmation message. In your MongoDB client, you should see the output as follows:

    ```{.text .no-copy}
    Using MongoDB:      {{release}}
    Using Mongosh:      {{mongosh}}

    For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/

    test>
    ```

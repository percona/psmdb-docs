> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server-for-mongodb/8.3/llms.txt).

# Configure OIDC authentication and authorization with Microsoft Entra ID

This document provides step-by-step instructions how to configure OIDC authentication and authorization the Percona Server for MongoDB using [Microsoft Entra](https://www.microsoft.com/en-gb/security/business/microsoft-entra) as an external identity provider.

The setup process consists of three main stages:

1. IdP setup:

   - Create and configure an OIDC application with Microsoft Entra
   - Create users and groups

1. Configure Percona Server for MongoDB to use OIDC as authentication method

1. Connect to Percona Server for MongoDB using OIDC authentication

## Prerequisites

Before you start, ensure you have the following:

1. Percona Server for MongoDB 8.0.12-4 and higher
1. Microsoft Entra tenant with admin access

## Identity provider setup

### Create and configure an OIDC application with Microsoft Entra

1. Sign in to the [Microsoft Entra admin center](https://entra.microsoft.com/).

1. In the left navigation pane, select **App Registrations**.

1. Click on **New registration**.

1. Fill in the registration form:

1. **Name**: Enter a name for your application.

1. **Supported account types**: Choose **Accounts in this organizational directory only**

1. **Redirect URI**: Set the redirect URI to `http://localhost:27097/redirect`.

1. Click **Register** to create the application. The application page opens.

1. Add group claims. In your application’s left-hand menu, select **Token configuration**.

1. Click on **Add group claim**.

1. In the **Group claims** dialog, select the following options:

   - **Select group types to include in Access, ID, and SAML tokens.**: Select **Security groups**
   - **Customize token properties by type**: Ensure **Group IP** is selected for every property type.

1. Click **Save** to add a groups claim.

### Configure the access token

To authorize users, you need to ensure the access tokens are generated as JWT formatted. To make this happen:

- Change the token version from null to 2.

- Expose the application’s API to define a unique set of permissions, called scopes, for your application.

- Add a custom scope for your application. This tells Entra ID that your application is a distinct resource that can be protected. When a client application requests one of these custom scopes, Entra ID issues a JSON Web Token (JWT) access token specifically for your API, which the API can then validate.

- Change the token version. In your application’s left-hand menu, select **Manifest**.

- Locate the `requestedAccessTokenVersion` property and set it from `null` to `2`. This ensures tokens are generated as JWT and not Opague:

- Click **Save**.

- Expose the application’s API. In your application’s left-hand menu, select **Expose an API**.

- Click **Add** next to **Application ID URI**. The URI defaults to \`api://<application-client-id>\`\`. The App ID URI acts as the prefix for the scopes you’ll reference in your API’s code, and it must be globally unique. Select **Save**.

- Add a custom scope. Click on **Add a scope**.

- Fill in the **Add a scope** form:

  - **Scope name**: Enter a name for your scope (e.g., `psmdb-access`).
  - **Who can consent?**: Select **Admins and users**.
  - **Admin consent display name**: Enter a display name for admin consent.
  - **Admin consent description**: Enter a description for admin consent.
  - **State**: Set to **Enabled**.
  - Click **Add scope** to create the scope.

### Configure users and groups

Groups define user access rights to resources. Identity provider groups are then mapped to roles in Percona Server for MongoDB to authorize users to access the database.

1. Create groups in Microsoft Entra ID. Check the [Create a basic group and add members](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-manage-groups) for exact steps.
1. Add users. Specify the user email as the username. Check the [Create a new user](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-create-delete-users#create-a-new-user) for exact steps.
1. Assign the groups you created earlier to your users on the **Assignments** tab of the user profile.

### Collect the information required for Percona Server for MongoDB configuration

1. Open the application’s **Overview** page.
1. Copy the **Application (client) ID** and save it for later use. You will use this value for the `clientID` and `audience` fields in Percona Server for MongoDB configuration.
1. Copy the issuer URL. From the top navigation, click **Endpoints** and copy the **OpenID Connect metadata document** URL up to `/.well-known/openid-configuration`. It should look like this:

```text
https://login.microsoftonline.com/{tenant-id}/v2.0
```

1. Copy the Application ID URI you defined earlier. It should look like this:

```text
api://<application-client-id>
```

1. Copy the groups’ Object IDs you created earlier.

## Configure Percona Server for MongoDB

Now you need to configure authentication in Percona Server for MongoDB. Specify the external identity provider configuration for the `oidcIdentityProviders` server parameter either via the configuration file or the command line.

The following table maps the Microsoft Entra ID configuration parameters to the Percona Server for MongoDB configuration:

| Microsoft Entra ID Parameter       | Percona Server for MongoDB Parameter                                                |
| ---------------------------------- | ----------------------------------------------------------------------------------- |
| `OpenID Connect metadata document` | `issuer`                                                                            |
| `Application (client) ID`          | `clientId` `audience`                                                               |
| `Application ID URI`               | `requestScopes` value consists of the Application ID URI and the custom scope name. |

To authorize users by identity provider groups, specify `authorizationClaim` value as `groups`.

**Configuration file**

1. Edit the `/etc/mongod.conf` configuration file:

   ```yaml
   security:
      authorization: enabled
   setParameter:
      authenticationMechanisms: MONGODB-OIDC
      oidcIdentityProviders: '[ {
         "issuer": "https://login.microsoftonline.com/{tenant-id}/v2.0",
         "clientId": "3ef1b836-6f12-4858-876b-35245110f6bc",
         "audience": "3ef1b836-6f12-4858-876b-35245110f6bc",
         "authNamePrefix": "entra",
         "useAuthorizationClaim": true,
         "authorizationClaim": "groups",
         "requestScopes": [ "api://3ef1b836-6f12-4858-876b-35245110f6bc/psmdb-access" ],
         "supportsHumanFlows": true           
      } ]'
   ```

1. Start or restart Percona Server for MongoDB:

   ```bash
   sudo systemctl start mongod
   ```

**Command line**

```bash
mongod --auth --setParameter authenticationMechanisms=MONGODB-OIDC --setParameter \
'oidcIdentityProviders=[ {
   "issuer": "https://login.microsoftonline.com/{tenant-id}/v2.0",
   "clientId": "3ef1b836-6f12-4858-876b-35245110f6bc",
   "audience": "3ef1b836-6f12-4858-876b-35245110f6bc",
   "authNamePrefix": "entra",
   "useAuthorizationClaim": true,
   "authorizationClaim": "groups",
   "requestScopes": [ "api://3ef1b836-6f12-4858-876b-35245110f6bc/psmdb-access" ],
   "supportsHumanFlows": true
} ]'
```

## Create user roles

To enable users to access Percona Server for MongoDB, you must create roles and define privileges for them.

The role name must have the format

```text
<authNamePrefix>/<Group-ObjectID>
```

where `<authNamePrefix>` is the prefix you specified in the `oidcIdentityProviders` configuration, and `<Group-ObjectID>` is the Object ID of the group in Microsoft Entra ID.

For example, if the `authNamePrefix` is set to `entra` and the group Object ID is `a3f2c1d4-8b9e-4f7a-a2c3-19d8e6f0b7a1`, the command to create a role is the following:

```javascript
db.getSiblingDB("admin").createRole({
  role: "entra/a3f2c1d4-8b9e-4f7a-a2c3-19d8e6f0b7a1",
  privileges: [],
  roles: ["readWriteAnyDatabase"]
})
```

Create role for all groups you have defined in Microsoft Entra ID. You can also create roles with different privileges for different groups.

## Connect to Percona Server for MongoDB using OIDC authentication

### Authorization code flow

To connect to Percona Server for MongoDB using OIDC authentication, you can use the `mongo` shell or any MongoDB client that supports OIDC.

1. Connect to Percona Server for MongoDB:

   ```bash
   mongosh  --authenticationMechanism MONGODB-OIDC --oidcFlows auth-code
   ```

1. The browser opens. Pass your credentials and click Next.

1. Confirm sign in.

1. Upon successful authentication, your `mongosh` session is established, and you can start executing commands.

### Device authentication flow

1. Connect to Percona Server for MongoDB:

   ```bash
   mongosh  --authenticationMechanism MONGODB-OIDC --oidcFlows device-auth
   ```

   Sample output

   ```text
   Visit the following URL to complete authentication: https://microsoft.com/devicelogin
   Enter the following code on that page: EKYE77DQZ
   Waiting....
   ```

1. Copy the link and open it on another device that has a browser

1. Enter the code you see in the terminal into the browser.

1. Pass your credentials and click Next.

1. Confirm sign in.

1. Upon successful authentication, your `mongosh` session is established, and you can start executing commands.

> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server-for-mongodb/8.3/llms.txt).

# Configure OIDC authentication and authorization with Ping Identity

This document provides step-by-step instructions how to configure OIDC authentication and authorization the Percona Server for MongoDB using [Ping Identity](https://www.pingidentity.com/en.html) as an external identity provider.

The setup process consists of three main stages:

1. IdP setup:

   - Create a new environment with Ping Identity
   - Configure an OIDC application
   - Create users and groups

1. Configure Percona Server for MongoDB to use OIDC as authentication method

1. Connect to Percona Server for MongoDB using OIDC authentication

## Prerequisites

Before you start, ensure you have the following:

1. Percona Server for MongoDB 8.0.12-4 and higher
1. Ping Identity account with the active subscription

## Identity provider setup

### Create an environment

An environment is the way to organize your Ping Identity resources. It contains applications, users, and groups. Each environment has its own settings and configurations.

To create a new environment in Ping Identity, follow these steps:

1. Log in to the [Ping Identity Admin Console](https://console.pingone.eu/).

1. On the home page, click **Create Environment**

1. Select the **Workforce solution** and click **Next**.

1. Click **Next**

1. Fill in the new environment details:

   - **Environment name**: Enter a name for your environment.
   - **Environment type**: Select **Production** or **Sandbox** depending on your needs.
   - **Region**: Select the region closest to your users.
   - **License**: Select the license to use for this environment.

1. Click **Finish** to create the environment.

### Configure an OIDC application

1. Select the created environment from the Environments list at the bottom of the Home page.

1. On the Environment overview page, click **Manage environment**. The environment dashboard opens.

1. In the left navigation pane, select **Applications** > **Applications**.

1. Click on **Getting Started Application**.

1. On the **Overview** tab, copy and save the following configuration information:

   - **Client ID** on the **General** section
   - An **issuer ID** on the Connection details section, it should look like `https://auth.pingone.eu/<environment-id>/as`.

1. Click **Connections** tab and click **Edit** icon.

1. Configure your application:

   - **Response Type**: select **Code**.
   - **Grant Type**:
   - Check **Authorization Code** for user applications that have a web browser
   - Check **Device Authorization** for user applications that don’t have a web browser
   - Check **Refresh Token** for better user experience. This allows users to refresh their access tokens without needing to re-authenticate.
   - **PKCE Enforcement** under the **Authorization Code** option: select **OPTIONAL** from the list.
   - Under the **Device Authorization** option, configure the device authorization lifetime
   - Under the **Refresh Token** option, configure the refresh token duration.
   - **Redirect URI**: enter `http://localhost:27097/redirect`.
   - **Token Endpoint Authentication Method**: select **None**.

1. Click **Save** to save the changes.

1. Go the **Attribute Mappings** tab.

1. Click the **Edit** icon next to the **Custom Attributes** section.

1. Click **Add**.

1. Fill in the **Add Custom Attribute** form:

   - **Attributes**: Enter `auth_claims`.
   - **PingOne Mappings**: Select `Group Names`.
   - Click **Save** to save the changes.

### Create users and groups

Groups define user access rights to resources. Identity provider groups are then mapped to roles in Percona Server for MongoDB to authorize users to access the database.

1. Create groups as described in the [Creating a group](https://docs.pingidentity.com/pingone/directory/p1_managing_groups.html#creating-a-group) guide.
1. Add users. Follow the steps in the [Adding a user](https://docs.pingidentity.com/pingone/directory/p1_adduser.html) guide to add users. Specify the user email as the username.
1. Assign groups you created earlier to the users.

## Configure Percona Server for MongoDB

Now you need to configure authentication in Percona Server for MongoDB. Specify the external identity provider configuration for the `oidcIdentityProviders` server parameter either via the configuration file or the command line.

The following table maps the Ping Identity configuration parameters to the Percona Server for MongoDB configuration:

| Ping Identity Parameter | Percona Server for MongoDB Parameter | | ======================= | ==================================== | | `Issuer ID` | `issuer` | | `Client ID` | `clientID`\
`audience` | | Attribute in Attribute Mappings | `authorizationClaim` |

**Configuration file**

1. Edit the `/etc/mongod.conf` configuration file:

   ```yaml
   security:
      authorization: enabled
   setParameter:
      authenticationMechanisms: MONGODB-OIDC
      oidcIdentityProviders: '[ {
         "issuer": "https://auth.pingone.eu/9f1b3e82-7c45-4a1e-bd62-cc38f7a4e918/as",
         "audience": "01660c90-f988-4220-ad9d-32b60370d32c",
         "authNamePrefix": "ping",
         "useAuthorizationClaim": true,
         "authorizationClaim": "auth_claims",
         "clientId": "01660c90-f988-4220-ad9d-32b60370d32c"
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
   "issuer": "https://auth.pingone.eu/9f1b3e82-7c45-4a1e-bd62-cc38f7a4e918/as",
   "audience": "01660c90-f988-4220-ad9d-32b60370d32c",
   "authNamePrefix": "ping",
   "useAuthorizationClaim": true,
   "authorizationClaim": "auth_claims",
   "clientId": "01660c90-f988-4220-ad9d-32b60370d32c"
} ]'
```

The `useAuthorizationClaim` configuration option defines how your users are authorized.

- When set to `true`, users are authorized using identity provider groups. Users are created and stored on the IdP side.
- When set to `false`, users are authorized by their usernames in the `$external` database in Percona Server for MongoDB. When using `useAuthorizationClaim: false`, **do not** specify `authorizationClaim`.

## Create user roles

To enable users to access Percona Server for MongoDB, you must create roles and define privileges for them.

The role name must match the identity provider group name and must have the prefix that matches the `authNamePrefix` in Percona Server for MongoDB configuration.

For example, to create a role for the group named `admin` in Ping and with the `authNamePrefix` set to `ping`, use the following command:

```javascript
db.getSiblingDB("admin").createRole({
  role: "ping/admin",
  privileges: [ ],
  roles: [ "readWriteAnyDatabase" ]
})
```

### Create users

**Complete this step if you set `useAuthorizationClaim` to `false`**

Create users in the `$external` database. The username must consist of the `authNamePrefix` and the email that you specified when you created users in Ping Identity. The username format is:

```text
authNamePrefix/email
```

If you set the `authNamePrefix` to `ping`, then the command to create a user is the following:

```javascript
db.getSiblingDB("$external").createUser({
  user: "ping/john.doe@example.com",
  roles: [
    { role: "ping/admin", db: "admin" } 
  ]
})
```

## Authenticate in Percona Server for MongoDB

### Authorization Code flow

1. Connect to Percona Server for MongoDB:

   ```bash
   mongosh  --authenticationMechanism MONGODB-OIDC --oidcIdTokenAsAccessToken
   ```

1. You will be redirected to the Ping Identity login page in your web browser.

1. Log in with your credentials.

1. Approve the sign in request.

1. Upon successful authentication, you will see a confirmation message. In your MongoDB client, you should see the output as follows:

   ```text
   Using MongoDB:      8.3.17-5
   Using Mongosh:      2.14.1

   For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/

   test>
   ```

### Device Authorization flow

1. Connect to Percona Server for MongoDB:

   ```bash
   mongosh  --authenticationMechanism MONGODB-OIDC --oidcIdTokenAsAccessToken --oidcFlows device-auth
   ```

   Sample output

   ```text
   Visit the following URL to complete authentication: https://auth.pingone.eu/9f1b3e82-7c45-4a1e-bd62-cc38f7a4e918/device
   Enter the following code on that page: ZDSC-KH7V
   Waiting...
   ```

1. Open the URL in your web browser and enter the code displayed in the terminal.

1. Approve the sign in request.

1. Upon successful authentication, you will see a confirmation message. In your MongoDB client, you should see the output as follows:

   ```text
   Using MongoDB:      8.3.17-5
   Using Mongosh:      2.14.1

   For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/

   test>
   ```

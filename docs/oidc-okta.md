# Configure OIDC authentication and authorization with Okta

This document focuses on configuring OIDC authentication for Percona Server for MongoDB deployment using [Okta :octicons-link-external-16:](https://www.okta.com/) as the identity provider.

The setup process consists of three main stages:

1. IdP setup:

    * Create and configure an OIDC application with Okta
    * Configure authorization server
    * Create users and groups

2. Configure Percona Server for MongoDB to use OIDC as authentication method
3. Connect to Percona Server for MongoDB using OIDC authentication

## Prerequisites

1. [ProBuild](psmdb-pro.md) of Percona Server for MongoDB 8.0.12-4 or higher
2. Access to Okta Admin console

## Identity provider setup

### Create and configure an OIDC application with Okta

1. Log in to your Okta Admin console.
2. Navigate to **Applications** > **Applications** from the side menu.
3. Click **Create App Integration**.
4. In the dialog that appears select:

    * Sign-in method: Select **OIDC - OpenID Connect**.    
    * Application type: **Select Native Application**. A command-line tool like the `mongo` shell is considered a "native" application.
    * Click **Next**.

5. Configure the Native App Integration:

    * Specify a descriptive name in the **App integration** name field.    
    * In the **Grant Types**, enable the following grant types:

        * **Authorization Code** 
        * **Device Authorization**
        * **Refresh Token** (optional, but recommended for better user experience. This allows users to refresh their access tokens without needing to re-authenticate.)

    * Set the Sign-in redirect URIs to http://localhost:17017. The port can be customized if needed, but this is a common default.
    * In the **Assignments** section, find the **Controlled access** and enable **Allow everyone in your organization to access**.
    * In the **Enable immediate access** section, ensure the **Enable immediate access with Federation Broker Mode** option is enabled.
    * Click **Save**.

6. After saving, you will be redirected to the application details page. On the **General** tab, copy the **Client ID** to clipboard and ensure the **Proof Key for Code Exchange (PKCE)** option is enabled.

### Configure an authorization server

1. Go to **Security** > **API** from the side menu, then click on the **Authorization Servers** tab.
2. Click **Add Authorization Server**.
3. In the dialog that appears, fill in the following fields:

	* **Name**: Provide a descriptive name for your authorization server.
	* **Audience**: Paste the Client ID value here.
	* **Description**: Optionally, add a description for your authorization server.
	* Click **Save**. You will be automatically redirected to the server's page.

4. Find the issuer URL. Go to the **Settings** tab and copy the **Issuer Metadata URI** value up to the `/.well-known/oauth-authorization-server`. The URL must be in the following format:

    ```
    https://<your-okta-domain>/oauth2/ausu08lpq4VQRntUz697
    ```

5. Configure **Groups claim**.

	* Go to the **Claims** tab.
	* Click **Add Claim**.
	* In the dialog that appears, fill in the following fields:

		* **Name**: Enter a name
		* **Include in token type**: Select **Access token**
		* **Value type**: Select `Groups`
		* **Filter**: Select **Matches regexp** and specify `.*` next to the drop-down.
		* **Disable claim**: Leave unchecked.
		* **Include in**: Check **Any scope**.
		* Click **Create**.

	For more information, see [Create API access claims :octicons-link-external-16:](https://help.okta.com/oie/en-us/content/topics/security/api-config-claims.htm?cshid=create-claims)

6. Configure the access policy

    * Go to the **Access Policies** tab and click **Add Policy**.
    * Specify an access policy name and description.
    * **Assign to**: Select **All clients**.
    * Click **Create Policy**. The Access Policy screen opens.

7. Create rules for the access policy. 

    On the **Access Policy** screen, click **Add rule** and fill in the rule details

    * Specify a name in the **Rule name** field.
    * Select the grant types that you want to use this rule. In the **IF Grant type is**, select the following: 

       * **Client Credentials** if a client acts on its own behalf
       *  **Authorization Code** and **Device Authorization** options if a client acts on behalf of a user.

    * Configure the rule based on your organization's security policy. This is the default rule configuration:

       * **AND User is**: Check **Any user assigned the app**
       * **AND Scopes requested**: Check **Any scopes**
       * **THEN Use this inline hook**: Leave unchecked
       * **AND Access token lifetime is**: Set `1` Hours
       * **AND Refresh token lifetime is**: Set `90` Days
       * **but will expire if not used every**: Set `7` Days.

    * Click **Create Rule**.

    See [Create access policies :octicons-link-external-16:](https://help.okta.com/oie/en-us/content/topics/security/api-config-access-policies.htm?cshid=create-access-policies) for more information about access policies and rules configuration.

### Create users and groups

Groups define user access rights to resources. Identity provider groups are then mapped to roles in Percona Server for MongoDB to authorize users to access the database.

1. Follow the steps described in the [Groups :octicons-link-external-16:](https://help.okta.com/okta_help.htm?type=oie&locale=en&id=Directory_Groups) documentation to create required groups

2. Create users. Specify the user email as the username. Follow the steps in the [Add users manually :octicons-link-external-16:](https://help.okta.com/oie/en-us/content/topics/users-groups-profiles/usgp-add-users.htm) documentation to create users.

3. Assign the groups you created to users.

## Configure Percona Server for MongoDB

Now you need to configure authentication in Percona Server for MongoDB. Specify the external identity provider configuration for the `oidcIdentityProviders` server parameter either via the configuration file or the command line. 

=== "Configuration file"

    1. Edit the `/etc/mongod.conf` configuration file:

        ```yaml
        security:
           authorization: enabled
        setParameter:
           authenticationMechanisms: MONGODB-OIDC
           oidcIdentityProviders: '[ {
              "issuer": "https://my-okta.okta.com/oauth2/austxj66qrgAVPlAj697",
              "audience": "example@my-company.com",
              "authNamePrefix": "okta",
              "useAuthorizationClaim": true,
              "authorizationClaim": "oidc-test",
              "clientId": "0oatxj71cmQfzQ9Us697"
           } ]'
        ```
    
    2. Start or restart Percona Server for MongoDB:

        ```{.bash data-prompt="$"}
        $ sudo systemctl start mongod
        ```

=== "Command line"

    ```{.bash data-prompt="$"}
    $ mongod --auth --setParameter authenticationMechanisms=MONGODB-OIDC --setParameter \
    'oidcIdentityProviders=[ {
       "issuer": "https://my-okta.okta.com/oauth2/austxj66qrgAVPlAj697",
       "audience": "example@mongodb.com",
       "authNamePrefix": "okta",
       "useAuthorizationClaim": true,
       "authorizationClaim": "oidc-test",
       "clientId": "0oatxj71cmQfzQ9Us697"
    } ]'
    ```

The `useAuthorizationClaim` configuration option defines how your users are authorized.

* When set to `true`, users are authorized using identity provider groups. Users are created and stored on the IdP side.
* When set to `false`, users are authorized by their usernames in the `$external` database in Percona Server for MongoDB. When using `useAuthorizationClaim: false`, **do not** specify `authorizationClaim`.

## Create user roles 

To enable users to access Percona Server for MongoDB, you must create roles and define privileges for them. 

The role name must match the identity provider group name and must have the prefix that matches the `authNamePrefix` in Percona Server for MongoDB configuration.

For example, to create a role for the default group `Everyone` in Okta and with the `authNamePrefix` set to `okta`, use the following command:

```javascript
db.getSiblingDB("admin").createRole({
  role: "okta/Everyone",
  privileges: [ ],
  roles: [ "readWriteAnyDatabase" ]
})
```

Create roles for all groups you have defined in Okta.

## Create users 

**Complete this step if you set `useAuthorizationClaim` to `false`**

Create users in the `$external` database. The username must consist of the `authNamePrefix` and the email that you specified when you created users in Okta. The username format is:

```
authNamePrefix/email
```

If you set the `authNamePrefix` to `okta`, then the command to create a user is the following:

```javascript
db.getSiblingDB("$external").createUser({
  user: "okta/john.doe@example.com",
  roles: [
    { role: "okta/Everyone", db: "admin" } 
  ]
})
```

## Authenticate in Percona Server for MongoDB

### Authorization code flow

1. Connect to Percona Server for MongoDB:

    ```{.bash data-prompt="$"}
    $ mongosh  --authenticationMechanism MONGODB-OIDC --oidcFlows auth-code 
    ```

2. In the Okta login portal in your browser, specify the credentials of one of the users you defined in Okta and click Sign in.

3. Upon successful log in you must see the **Login successful** screen. In your `mongo` client, you should see the output as follows:

    ```{.text .no-copy}
    Using MongoDB:		{{release}}
    Using Mongosh:		{{mongosh}}

    For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/

    test>
    ```

### Device authentication flow

1. Connect to Percona Server for MongoDB:

    ```{.bash data-prompt="$"}
    $ mongosh  --authenticationMechanism MONGODB-OIDC --oidcFlows device-auth 
    ```

    ??? example "Sample output"

        ```
        Visit the following URL to complete authentication: https://my-okta.okta.com/activate
        Enter the following code on that page: LRVCRLXP
        ```

2. Open the URL on another device that has the web browser.
3. Enter the code in the **Activation Code** field and click **Next**
4. You should see the **Device Activated** message on the screen. In your `mongo` client, you should see the output as follows:

    ```{.text .no-copy}
    Using MongoDB:		{{release}}
    Using Mongosh:		{{mongosh}}

    For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/

    test>
    ```




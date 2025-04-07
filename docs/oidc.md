# OIDC authentication

OpenID Connect (OIDC) is an identity authentication protocol built on top of the OAuth 2.0 framework. OIDC is designed to verify user identities and provide authentication, ensuring that users are who they claim to be. OAuth 2.0 is used for user authorization to access resources. 

With the OIDC / OAuth 2.0 support in Percona Server for MongoDB, users can authenticate and authorize in your infrastructure without sharing their credentials. To make this happen, you enable a single sign-on (SSO) for Percona Server for MongoDB using an external identity provider (IdP). 

The IdP is a centralized place to authenticate and authorize humans and applications to access multiple resources in your infrastructure. User credentials, access policies and roles are stored centralized on the IdP side. You can configure different access policies and tailor permissions for a group of users of a specific user. 

Currently, Percona Server for MongoDB supports [Okta :octicons-link-external-16:](https://www.okta.com/) external identity provider. We plan to extend the list of supported external identity providers in future releases.

## Authentication workflow

Percona Server for MongoDB supports two authentication workflows with OIDC:

* **Authorization code with Proof Key for Code Exchange (PKCE)**: a MongoDB client (for example, `mongosh` or Compass) opens a browser and redirects a user to the login portal of an external identity provider to pass authentication. This is the default authentication workflow.

* **Device authentication**: instead of redirecting a user to authenticate on a login portal directly, a `mongo` client receives the URL of the login portal and the authentication code. The user follows the URL and enters the  authentication code. The example use case for such a workflow is when both a `mongo` client and Percona Server for MongoDB run in a cloud environment and the client needs to authenticate in Percona Server for MongoDB without managing long-term credentials like passwords. 
 

The following diagram illustrates the authentication flow.

![image](_images/OIDC-flow.png)

1. A user connects to Percona Server for MongoDB using a `mongo` client. The client must support OIDC.
2. The `mongo` client requests authentication from the IdP.
3. The IdP generates the authorization code. A user is redirected to the login portal of an external identity provider (IdP).
4.	The user is requested to authenticate. For example, using two-factor authentication or by entering an authentication code.
5. A user is redirected back to the `mongo` client with single-use authorization code. 
6.	The IdP verifies the authorization code, user's client ID and credentials.
5.	Upon success, the IdP returns the access and ID tokens to the `mongo` client.
6.	The `mongo` client uses the access token to access Percona Server for MongoDB.

## Benefits

The use of OIDC and OAuth 2.0 provides the following benefits:

* streamlines authentication and authorization flow, 
* simplifies user management and configuration: everything is done in a single place
* enables you to use modern authentication techniques like 2FA, MFA and others supported by IdP
* improves security as credentials are not sent to nor stored in Percona Server for MongoDB. 
* Reduces cross-application risk - access tokens are granted for specific resources using audience claims. If a token is compromised, the token has a limited lifetime and scope to limit access.

## Configuration 

[Configure OIDC / OAuth 2.0 authentication and authorization](oidc-setup.md) in Percona Server for MongoDB.


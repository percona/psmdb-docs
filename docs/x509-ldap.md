# Set up x.509 authentication and LDAP authorization

[x.509 certificate authentication](authentication.md#x509) is one of the supported authentication mechanisms in Percona Server for MongoDB. It is compatible with [LDAP authorization](authorization.md) to enable you to control user access and operations in your database environment.

This document provides the steps on how to configure and use x.509 certificates for authentication in Percona Server for MongoDB and authorize users in the LDAP server.

## Considerations


1. For testing purposes, in this tutorial we use [OpenSSL](https://www.openssl.org/) to issue self-signed certificates. For production use, we recommend using certificates issued and signed by the CA in Percona Server for MongoDB. Client certificates must meet the [client certificate requirements](https://docs.mongodb.com/manual/core/security-x.509/#client-certificate-requirements).

2. The setup of the LDAP server and the configuration of the LDAP schema is out of scope of this document. We assume that you have the LDAP server up and running and accessible to Percona Server for MongoDB.

## Setup procedure

### Issue certificates


1. Create a directory to store the certificates. For example, `/var/lib/mongocerts`.

    ```{.bash data-prompt="$"}
    $ sudo mkdir -p /var/lib/mongocerts
    ```


2. Grant access to the `mongod` user to this directory:

    ```{.bash data-prompt="$"}
    $ sudo chown mongod:mongod /var/lib/mongocerts
    ```

#### Generate the root Certificate Authority certificate

The root Certificate Authority certificate will be used to sign the SSL certificates.

Run the following command and in the `-subj` flag, provide the details about your organization:

* C - Country Name (2 letter code);
* ST - State or Province Name (full name);
* L - Locality Name (city);
* O - Organization Name (company);
* CN - Common Name (your name or your server’s hostname) .

```{.bash data-prompt="$"}
$ cd /var/lib/mongocerts
$ sudo openssl req -nodes -x509 -newkey rsa:4096 -keyout ca.key -out ca.crt -subj "/C=US/ST=California/L=SanFrancisco/O=Percona/OU=root/CN=localhost"
```

#### Generate server certificate

1. Create the server certificate request and key. In the `-subj` flag, provide the details about your organization:


    * C - Country Name (2 letter code);


    * ST - State or Province Name (full name);


    * L - Locality Name (city);


    * O - Organization Name (company);


    * CN - Common Name (your name or your server’s hostname) .

    ```{.bash data-prompt="$"}
    $ sudo openssl req -nodes -newkey rsa:4096 -keyout server.key -out server.csr -subj "/C=US/ST=California/L=SanFrancisco/O=Percona/OU=server/CN=localhost"
    ```

2. Sign the server certificate request with the root CA certificate:

    ```{.bash data-prompt="$"}
    $ sudo openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out server.crt
    ```

3. Combine the server certificate and key to create a certificate key file. Run this command as the `root` user:

    ```{.bash data-prompt="$"}
    $ cat server.key server.crt > server.pem
    ```

#### Generate client certificates

1. Generate client certificate request and key. In the `-subj` flag, specify the information about clients in the  format.

    ```{.bash data-prompt="$"}
    $ openssl req -nodes -newkey rsa:4096 -keyout client.key -out client.csr -subj "/DC=com/DC=percona/CN=John Doe"
    ```

2. Sign the client certificate request with the root CA certificate.

    ```{.bash data-prompt="$"}
    $ openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -set_serial 02 -out client.crt
    ```

3. Combine the client certificate and key to create a certificate key file.

    ```{.bash data-prompt="$"}
    $ cat client.key client.crt > client.pem
    ```

### Set up the LDAP server

The setup of the LDAP server is out of scope of this document. Please work with your LDAP administrators to set up the LDAP server and configure the LDAP schema.

### Configure the `mongod` server

The configuration consists of the following steps:


* Creating a role that matches the user group on the LDAP server
* Editing the configuration file to enable the x.509 authentication

!!! note 

    When you use x.509 authentication with LDAP authorization, you don’t need to create users in the `$external` database.  User management is done on the LDAP server so when a client connects to the database, they are authenticated and authorized through the LDAP server.

#### Create roles

At this step, create the roles in the `admin` database with the names that exactly match the names of the user groups on the LDAP server. These roles are used for user [LDAP authorization](authorization.md) in Percona Server for MongoDB.

In our example, we create the role `cn=otherusers,dc=percona,dc=com` that has the corresponding LDAP group.

```javascript
var admin = db.getSiblingDB("admin")
db.createRole(
   {
     role: "cn=otherusers,dc=percona,dc=com",
     privileges: [],
     roles: [
           "userAdminAnyDatabase",
           "clusterMonitor",
           "clusterManager",
           "clusterAdmin"
            ]
   }
)
```

Output:

```json
{
     "role" : "cn=otherusers,dc=percona,dc=com",
     "privileges" : [ ],
     "roles" : [
             "userAdminAnyDatabase",
             "clusterMonitor",
             "clusterManager",
             "clusterAdmin"
     ]
}
```

#### Enable x.509 authentication


1. Stop the `mongod` service

    ```{.bash data-prompt="$"}
    $ sudo systemctl stop mongod
    ```

2. Edit the `/etc/mongod.conf` configuration file.

    ```yaml
    net:
      port: 27017
      bindIp: 127.0.0.1
      tls:
        mode: requireTLS
        certificateKeyFile: /var/lib/mongocerts/server.pem
        CAFile: /var/lib/mongocerts/ca.crt

    security:
      authorization: enabled
      ldap:
        servers: "ldap.example.com"
        transportSecurity: none
        authz:
          queryTemplate: "dc=percona,dc=com??sub?(&(objectClass=groupOfNames)(member={USER}))"

    setParameter:
      authenticationMechanisms: PLAIN,MONGODB-X509
    ```

    Replace `ldap.example.com` with the hostname of your LDAP server. In the LDAP query template, replace the domain controllers `percona` and `com` with those relevant to your organization.


3. Start the `mongod` service

    ```{.bash data-prompt="$"}
    $ sudo systemctl start mongod
    ```

### Authenticate with the x.509 certificate

To test the authentication, connect to *Percona Server for MongoDB* using the following command:

```{.bash data-prompt="$"}
$ mongosh --host localhost --tls --tlsCAFile /var/lib/mongocerts/ca.crt --tlsCertificateKeyFile <path_to_client_certificate>/client.pem  --authenticationMechanism MONGODB-X509 --authenticationDatabase='$external'
```

The result should look like the following:

```javascript
> db.runCommand({connectionStatus : 1})
{
     "authInfo" : {
             "authenticatedUsers" : [
                     {
                             "user" : "CN=John Doe,DC=percona,DC=com",
                             "db" : "$external"
                     }
             ],
             "authenticatedUserRoles" : [
                     {
                             "role" : "cn=otherreaders,dc=percona,dc=com",
                             "db" : "admin"
                     },
                     {
                             "role" : "clusterAdmin",
                             "db" : "admin"
                     },
                     {
                             "role" : "userAdminAnyDatabase",
                             "db" : "admin"
                     },
                     {
                             "role" : "clusterManager",
                             "db" : "admin"
                     },
                     {
                             "role" : "clusterMonitor",
                             "db" : "admin"
                     }
             ]
     },
     "ok" : 1
}
```

*[CA]: Certificate Authority



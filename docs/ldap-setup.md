# Set up LDAP authentication and authorization using NativeLDAP

This document describes an example configuration of LDAP authentication and authorization using direct binding to an LDAP server (Native LDAP). We recommend testing this setup in a non-production environment first, before applying it in production.

## Assumptions

* The setup of an LDAP server is out of scope of this document. We assume that you are familiar with the LDAP server schema.
* If usernames contain special characters, they must be escaped as described in [RFC4514](https://www.ietf.org/rfc/rfc4514.txt), [RFC4515](https://tools.ietf.org/html/rfc4515), [RFC4516](https://tools.ietf.org/html/rfc4516). The usage of particular escaping rules depends on  the part of the LDAP query which will contain the substituted value. An explanation of escaping rules or LDAP queries is out of scope of this setup. Please review the RFC directly or use your preferred LDAP resource.
* You have the LDAP server up and running and it's accessible to the servers with Percona Server for MongoDB installed.
* This document primarily focuses on OpenLDAP used as the LDAP server and the examples are given based on the OpenLDAP format. If you are using Active Directory, refer to the [Active Directory configuration](#active-directory-configuration) section.
* In examples below, we use anonymous binds to the LDAP server and the following OpenLDAP groups:

   ```text
   dn: cn=testusers,dc=percona,dc=com
   objectClass: groupOfNames
   cn: testusers
   member: cn=alice,dc=percona,dc=com   

   dn: cn=otherusers,dc=percona,dc=com
   objectClass: groupOfNames
   cn: otherusers
   member: cn=bob,dc=percona,dc=com
   ```

## Prerequisites 

- To configure LDAP, you must have the `sudo` privilege to the server with the Percona Server for MongoDB installed.

- If your LDAP server disallows anonymous binds, create the user that Percona Server for MongoDB will use to connect to and query the LDAP server. Afterwards, set that username and password using the `security.ldap.bind.queryUser` and `security.ldap.bind.queryPassword` parameters in the `mongod.conf` configuration file. If the username or any part of it ends up substituted as distinguished name, it must be escaped according to [RFC 4514](https://tools.ietf.org/html/rfc4514). It may happen when: 

    - A username is a fully distinguished name and can be substituted directly into the LDAP query without using any transformation. The LDAP query is defined within the `security.ldap.authz.queryTemplate` configuration parameter.
    - A username represents an email address or a full name and requires transformation to LDAP DN. The transformation rules are defined via the `security.ldap.userToDNMapping` configuration parameter. After the transformation, some parts of the username may become part of distinguished name substituted into the `security.ldap.authz.queryTemplate` parameter.


## Setup procedure

### Configure TLS/SSL connection for Percona Server for MongoDB

By default, Percona Server for MongoDB establishes the TLS connection when binding to the LDAP server and thus, it requires access to the LDAP  certificates. To make Percona Server for MongoDB aware of the certificates, do the following:

1. Place the certificate in the `certs` directory. The path to the `certs` directory is:

    * On RHEL / derivatives: `/etc/openldap/certs/`

    * On Debian / Ubuntu: `/etc/ssl/certs/`

2. Specify the path to the certificates in the `ldap.conf` file:

    === "Debian / Ubuntu"

         ```
         tee -a /etc/openldap/ldap.conf <<EOF
         TLS_CACERT /etc/ssl/certs/my_CA.crt
         EOF
         ```

    === "RHEL and derivatives"

         ```
         tee -a /etc/openldap/ldap.conf <<EOF
         TLS_CACERT /etc/openldap/certs/my_CA.crt
         EOF
         ```

--8<-- [start:roles]

### Create roles for LDAP groups in Percona Server for MongoDB

Percona Server for MongoDB authorizes users based on LDAP group membership. For every group, you must create the role in the `admin` database with the name that exactly matches the  of the LDAP group.

Percona Server for MongoDB maps the user’s LDAP group to the roles and determines what role is assigned to the user. Percona Server for MongoDB then grants privileges defined by this role.

To create the roles, use the following command:

```javascript
var admin = db.getSiblingDB("admin")
admin.createRole(
   {
     role: "cn=testusers,dc=percona,dc=com",
     privileges: [],
     roles: [ "readWrite"]
   }
)

admin.createRole(
   {
     role: "cn=otherusers,dc=percona,dc=com",
     privileges: [],
     roles: [ "read"]
   }
)
```

--8<-- [end:roles]

### Percona Server for MongoDB configuration

#### Access without username transformation

This section assumes that users connect to Percona Server for MongoDB by providing their LDAP DN as the username and the LDAP DNs don't contain special characters. Otherwise, you must escape them according to [RFC 4514 | LDAP: Distinguished Names](https://datatracker.ietf.org/doc/html/rfc4514).

1. Edit the Percona Server for MongoDB configuration file (by default, `/etc/mongod.conf`) and specify the following configuration:

    ```yaml
    security:
      authorization: "enabled"
      ldap:
        servers: "ldap.example.com"
        transportSecurity: tls
        authz:
           queryTemplate: "dc=percona,dc=com??sub?(&(objectClass=groupOfNames)(member={PROVIDED_USER}))"

    setParameter:
      authenticationMechanisms: "PLAIN"
    ```

    The `{PROVIDED_USER}` variable substitutes the provided username before authentication or username transformation takes place.

    Replace `ldap.example.com` with the hostname of your LDAP server. In the LDAP query template, replace the domain controllers `percona` and `com` with those relevant to your organization.


2. Restart the `mongod` service:

    ```bash
    sudo systemctl restart mongod
    ```


3. Test the access to Percona Server for MongoDB:

    ```bash
    mongosh -u "cn=alice,dc=percona,dc=com" -p "secretpwd" --authenticationDatabase '$external' --authenticationMechanism 'PLAIN'
    ```

#### Access with username transformation

If users connect to Percona Server for MongoDB with usernames that are not LDAP, you need to transform these usernames to be accepted by the LDAP server. If usernames contain special characters, these [characters must be escaped](#escaping-special-characters). 

Using the `--ldapUserToDNMapping` configuration parameter allows you to do this. You specify the match pattern as a regexp to capture a username. Next, specify how to transform it - either to use a substitution value or to query the LDAP server for a username.

If you don’t know what the Substitution or LDAP query string should be, please consult with the LDAP administrators to figure this out.

Note that you can use only the `LDAPquery` or the `Substitution` stage, and you cannot combine the two.

=== "Substitution"

     1. Edit the Percona Server for MongoDB configuration file (by default, `/etc/mongod.conf`) and specify the `userToDNMapping` parameter:

         ```yaml
         security:
           authorization: "enabled"
           ldap:
             servers: "ldap.example.com"
             transportSecurity: tls
             authz:
                queryTemplate: "dc=percona,dc=com??sub?(&(objectClass=groupOfNames)(member={USER}))"
             userToDNMapping: >-
                   [
                     {
                       match: "([^@]+)@percona\\.com",
                       substitution: "CN={0},DC=percona,DC=com"
                     }
                   ]

         setParameter:
           authenticationMechanisms: "PLAIN"
         ```

         The `{USER}` variable substitutes the username transformed during the `userToDNMapping` stage.

         Modify the given example configuration to match your deployment.

     2. Restart the `mongod` service:

         ```bash
         sudo systemctl restart mongod
         ```  
     3. Test the access to Percona Server for MongoDB:

         ```bash
         mongosh -u "alice@percona.com" -p "secretpwd" --authenticationDatabase '$external' --authenticationMechanism 'PLAIN'
         ```

=== "LDAP query"
    
     1. Edit the Percona Server for MongoDB configuration file (by default, `/etc/mongod.conf`) and specify the `userToDNMapping` parameter:

         ```yaml
         security:
           authorization: "enabled"
           ldap:
             servers: "ldap.example.com"
             transportSecurity: tls
             authz:
                queryTemplate: "dc=percona,dc=com??sub?(&(objectClass=groupOfNames)(member={USER}))"
             userToDNMapping: >-
                   [
                     {
                       match: "([^@]+)@percona\\.com",
                       ldapQuery: "dc=percona,dc=com??sub?(&(objectClass=organizationalPerson)(cn={0}))"
                     }
                   ]

         setParameter:
           authenticationMechanisms: "PLAIN"
         ```
        
         The `{USER}` variable substitutes the username transformed during the userToDNMapping stage.

         Modify the given example configuration to match your deployment, For example, replace `ldap.example.com` with the hostname of your LDAP server. Replace the domain controllers (DC) `percona` and `com` with those relevant to your organization. Depending on your LDAP schema, further modifications of the LDAP query may be required.

     2. Restart the `mongod` service:

         ```bash
         sudo systemctl restart mongod
         ```  

     3. Test the access to Percona Server for MongoDB:

         ```bash
         mongosh -u "alice" -p "secretpwd" --authenticationDatabase '$external' --authenticationMechanism 'PLAIN'
         ```

#### Escaping special characters

The **`substitution` parameter**

The result of the substitution becomes the value of the `{USER}` placeholder, which is a `{USER}` value in the `security.ldap.authz.queryTemplate` parameter. Escaping requirements depend on the part of the query template that will be substituted. For example, the result of the substitution can be a full distinguished name or a part of it. In this case, according to [RFC4514](https://www.ietf.org/rfc/rfc4514.txt), you must escape special characters in the `substitution` parameter. Using other escaping mechanisms in this parameter is unnecessary because {{ product.psmdb_full_name }} applies the necessary escaping as outlined in [RFC4515](https://tools.ietf.org/html/rfc4515) and [RFC4516](https://tools.ietf.org/html/rfc4516) while substituting the `security.ldap.authz.queryTemplate` parameter.

The **`ldapQuery` and `queryTemplate` parameters**

To properly escape special characters, follow these steps:

1. Escape special characters in full or partially distinguished names in the query according to [RFC 4514](https://www.ietf.org/rfc/rfc4514.txt).
2. Next, escape special characters within the LDAP search filter portion of the query, as outlined in [RFC 4515](https://www.ietf.org/rfc/rfc4515.txt).
3. Then, escape special characters in the query according to [RFC 4516](https://www.ietf.org/rfc/rfc4516.txt). Note that you do not need to escape question marks if they are being used to separate parts of the query.<br />
4. Finally, if you plan to use the result in a YAML configuration file, you may need to escape characters according to the [YAML specification](https://yaml.org/spec/)

### Active Directory configuration

Microsoft Active Directory uses a different schema for user and group definition. To illustrate Percona Server for MongoDB configuration, we will use the following AD users:

```text
dn:CN=alice,CN=Users,DC=testusers,DC=percona,DC=com
userPrincipalName: alice@testusers.percona.com
memberOf: CN=testusers,CN=Users,DC=percona,DC=com

dn:CN=bob,CN=Users,DC=otherusers,DC=percona,DC=com
userPrincipalName: bob@otherusers.percona.com
memberOf: CN=otherusers,CN=Users,DC=percona,DC=com
```

The following are respective  groups:

```text
dn:CN=testusers,CN=Users,DC=percona,DC=com
member:CN=alice,CN=Users,DC=testusers,DC=example,DC=com

dn:CN=otherusers,CN=Users,DC=percona,DC=com
member:CN=bob,CN=Users,DC=otherusers,DC=example,DC=com
```

Use one of the given Percona Server for MongoDB configurations for user authentication and authorization in Active Directory. Read about [escaping special characters in usernames](#escaping-special-characters) to modify the configuration accordingly.

=== "No username transformation"

     1. Edit the `/etc/mongod.conf` configuration file:

         ```yaml
         ldap:
           servers: "ldap.example.com"
           authz:
             queryTemplate: "DC=percona,DC=com??sub?(&(objectClass=group)(member:1.2.840.113556.1.4.1941:={PROVIDED_USER}))"

           setParameter:
             authenticationMechanisms: "PLAIN"
         ```

     2. Restart the `mongod` service:

         ```bash
         sudo systemctl restart mongod
         ```  

     3. Test the access to Percona Server for MongoDB:

         ```bash
         mongosh -u "CN=alice,CN=Users,DC=testusers,DC=percona,DC=com" -p "secretpwd" --authenticationDatabase '$external' --authenticationMechanism 'PLAIN'
         ```

=== "Username substitution"

     1. Edit the `/etc/mongod.conf` configuration file:

         ```yaml
         ldap:
           servers: "ldap.example.com"
           authz:
             queryTemplate: "DC=percona,DC=com??sub?(&(objectClass=group)(member:1.2.840.113556.1.4.1941:={USER}))"
           userToDNMapping: >-
                 [
                   {
                     match: "([^@]+)@([^\\.]+)\\.percona\\.com",
                     substitution: "CN={0},CN=Users,DC={1},DC=percona,DC=com"
                   }
                 ]

           setParameter:
             authenticationMechanisms: "PLAIN"
         ```

     2. Restart the `mongod` service:

         ```bash
         sudo systemctl restart mongod
         ```  

     3. Test the access to Percona Server for MongoDB:

         ```bash
         mongosh -u "alice@percona.com" -p "secretpwd" --authenticationDatabase '$external' --authenticationMechanism 'PLAIN'
         ```

=== "LDAP query"

     1. Edit the `/etc/mongod.conf` configuration file:

         ```yaml
         ldap:
           servers: "ldap.example.com"
           authz:
             queryTemplate: "DC=percona,DC=com??sub?(&(objectClass=group)(member:1.2.840.113556.1.4.1941:={USER}))"
           userToDNMapping: >-
                 [
                   {
                     match: "(.+)",
                     ldapQuery: "dc=example,dc=com??sub?(&(objectClass=organizationalPerson)(userPrincipalName={0}))"
                   }
                 ]

           setParameter:
             authenticationMechanisms: "PLAIN"
         ```

     2. Restart the `mongod` service:

         ```bash
         sudo systemctl restart mongod
         ```  

     3. Test the access to Percona Server for MongoDB:

         ```bash
         mongosh -u "alice" -p "secretpwd" --authenticationDatabase '$external' --authenticationMechanism 'PLAIN'
         ```

Modify one of this example configuration to match your deployment.

!!! admonition ""
    
    This document is based on the following posts from Percona Database Performance Blog:

    * [Percona Server for MongoDB LDAP Enhancements: User-to-DN Mapping](https://www.percona.com/blog/2020/04/24/percona-server-for-mongodb-ldap-enhancements-user-to-dn-mapping/) by Igor Solodovnikov
    * [Authenticate Percona Server for MongoDB Users via Native LDAP](https://www.percona.com/blog/2021/07/08/authenticate-percona-server-for-mongodb-users-via-native-ldap/) by Ivan Groenewold

*[DN]: Distinguished Name
*[AD]: Active Directory


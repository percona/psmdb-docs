# Setting up LDAP authentication with SASL

This document describes an example configuration
suitable only to test out the external authentication functionality
in a non-production environment.
Use common sense to adapt these guidelines to your production environment.

To learn more about how the authentication works, see [LDAP authentication with SASL](authentication.md#ldap-authentication-sasl).

## Environment setup and configuration

The following components are required:

* `slapd`: OpenLDAP server.

* `libsasl2` version 2.1.25 or later.

* `saslauthd`:  Authentication Daemon (distinct from `libsasl2`).

The following steps will help you configure your environment:

### Assumptions

Before we move on to the configuration steps, we assume the following:


1. You have the LDAP server up and running and have configured users on it. The LDAP server is accessible to the server with *Percona Server for MongoDB* installed. This document focuses on OpenLDAP server. If you use Microsoft Windows Active Directory, refer to the [Microsoft Windows Active Directory](https://docs.percona.com/percona-server-for-mongodb/4.2/sasl-auth.html#windows-ad) section for `saslauthd` configuration.

2. You must place these two servers behind a firewall as the communications between them will be in plain text. This is because the SASL mechanism of PLAIN can only be used when authenticating and credentials will be sent in plain text.

3. You have `sudo` privilege to the server with the *Percona Server for MongoDB* installed.

### Configuring `saslauthd`


1. Install the SASL packages. Depending on your OS, use the following command:

    === "Debian and Ubuntu"

         ```{.bash data-prompt="$"}
         $ sudo  apt install -y sasl2-bin
         ```

    === "RHEL and derivatives"

         ```{.bash data-prompt="$"}
         $ sudo  yum install -y cyrus-sasl
         ```

         **NOTE**: For Percona Server for MongoDB versions earlier than 4.0.26-21, 4.4.8-9, 4.2.16-17, also install the `cyrus-sasl-plain` package.

2. Configure SASL to use `ldap` as the  authentication mechanism.

    !!! note

        Back up the original configuration file before making changes.

    === "Debian and Ubuntu"

         Use the following commands to enable the `saslauthd` to auto-run on startup and to set the `ldap` value for the `--MECHANISMS` option:

         ```{.bash data-prompt="$"}
         $ sudo sed -i -e s/^MECH=pam/MECH=ldap/g /etc/sysconfig/saslauthdsudo sed -i -e s/^MECHANISMS="pam"/MECHANISMS="ldap"/g /etc/default/saslauthd
         $ sudo sed -i -e s/^START=no/START=yes/g /etc/default/saslauthd
         ```

         Alternatively, you can edit the `/etc/default/sysconfig/saslauthd` configuration file:

         ```init
         START=yes
         MECHANISMS="ldap
         ```

    === "RHEL and derivatives"

         Specify the `ldap` value for the `--MECH` option using the following command:

         ```{.bash data-prompt="$"}
         $ sudo sed -i -e s/^MECH=pam/MECH=ldap/g /etc/sysconfig/saslauthd
         ```

         Alternatively, you can edit the /etc/sysconfig/saslauthd configuration file:

         ```init
         MECH=ldap
         ```

3. Create the `/etc/saslauthd.conf` configuration file and specify the settings that `saslauthd` requires to connect to a local LDAP service:

    === "OpenLDAP server"

         The following is the example configuration file. Note that the server address **MUST** match the OpenLDAP installation:

         ```text
         ldap_servers: ldap://localhost
         ldap_mech: PLAIN
         ldap_search_base: dc=example,dc=com
         ldap_filter: (cn=%u)
         ldap_bind_dn: cn=admin,dc=example,dc=com
         ldap_password: secret
         ```

         Note the LDAP password (`ldap_password`) and bind domain name (`ldap_bind_dn`).
         This allows the `saslauthd` service to connect to the LDAP service as admin.
         In production, this would not be the case; users should not store administrative passwords in unencrypted files.

    === "Microsoft Windows Active Directory"

         In order for LDAP operations to be performed
         against a Windows Active Directory server,
         a user record must be created to perform the lookups.

         The following example shows configuration parameters for `saslauthd`
         to communicate with an Active Directory server:

         ```text
         ldap_servers: ldap://localhost
         ldap_mech: PLAIN
         ldap_search_base: CN=Users,DC=example,DC=com
         ldap_filter: (sAMAccountName=%u)
         ldap_bind_dn: CN=ldapmgr,CN=Users,DC=<AD Domain>,DC=<AD TLD>
         ldap_password: ld@pmgr_Pa55word
         ```

         In order to determine and test the correct search base
         and filter for your Active Directory installation,
         the Microsoft [LDP GUI Tool](https://technet.microsoft.com/en-us/library/Cc772839%28v=WS.10%29.aspx)
         can be used to bind and search the LDAP-compatible directory.


4. Start the `saslauthd` process and set it to run at restart:

    ```{.bash data-prompt="$"}
    $ sudo systemctl start saslauthd
    $ sudo systemctl enable saslauthd
    ```


5. Give write permissions to the `/run/saslauthd` folder for the `mongod`. Either change permissions to the  `/run/saslauthd` folder:

    ```{.bash data-prompt="$"}
    $ sudo chmod 755 /run/saslauthd
    ```

    Or add the `mongod` user to the `sasl` group:

    ```{.bash data-prompt="$"}
    $ sudo usermod -a -G sasl mongod
    ```

### Sanity check

Verify that the `saslauthd` service can authenticate
against the users created in the LDAP service:

```{.bash data-prompt="$"}
$ testsaslauthd -u christian -p secret  -f /var/run/saslauthd/mux
```

This should return `0:OK "Success"`.
If it doesn’t, then either the user name and password
are not in the LDAP service, or `sasaluthd` is not configured properly.

### Configuring libsasl2

The `mongod` also uses the SASL library for communications. To configure the SASL library, create a configuration file.

The configuration file **must** be named `mongodb.conf` and placed in a directory
where `libsasl2` can find and read it.
`libsasl2` is hard-coded to look in certain directories at build time.
This location may be different depending on the installation method.

In the configuration file, specify the following:

```text
pwcheck_method: saslauthd
saslauthd_path: /var/run/saslauthd/mux
log_level: 5
mech_list: plain
```

The first two entries (`pwcheck_method` and `saslauthd_path`)
are required for `mongod` to successfully use the `saslauthd` service.
The `log_level` is optional but may help determine configuration errors.

!!! admonition "See also"

    [SASL documentation](https://www.cyrusimap.org/sasl/index.html)

### Configuring `mongod` server

The configuration consists of the following steps:


* Creating a user with the **root** privileges. This user is required to log in to *Percona Server for MongoDB* after the external authentication is enabled.


* Editing the configuration file to enable the external authentication

#### Create a root user

Create a user with the **root** privileges in the `admin` database. If you have already created this user, skip this step. Otherwise, run the following command to create the admin user:

```javascript
> use admin
switched to db admin
> db.createUser({"user": "admin", "pwd": "$3cr3tP4ssw0rd", "roles": ["root"]})
Successfully added user: { "user" : "admin", "roles" : [ "root" ] }
```

#### Enable external authentication

Edit the `etc/mongod.conf` configuration file to enable the external authentication:

```yaml
security:
  authorization: enabled

setParameter:
  authenticationMechanisms: PLAIN,SCRAM-SHA-1
```

Restart the `mongod` service:

```{.bash data-prompt="$"}
$ sudo systemctl restart mongod
```

#### Add an external user to Percona Server for MongoDB

User authentication is done by mapping a user object on the LDAP server against a user created in the `$external` database. Thus, at this step, you create the user in the `$external` database and they inherit the roles and privileges. Note that the username must exactly match the name of the user object on the LDAP server.

Connect to Percona Server for MongoDB and authenticate as the root user.

```{.bash data-prompt="$"}
$ mongo --host localhost --port 27017 -u admin -p '$3cr3tP4ssw0rd' --authenticationDatabase 'admin'
```

Use the following command to add an external user to Percona Server for MongoDB:

```javascript
> db.getSiblingDB("$external").createUser( {user : "christian", roles: [ {role: "read", db: "test"} ]} );
```

## Authenticate as an external user in Percona Server for MongoDB

When running the `mongo` client, a user can authenticate
against a given database using the following command:

```javascript
> db.getSiblingDB("$external").auth({ mechanism:"PLAIN", user:"christian", pwd:"secret", digestPassword:false})
```

Alternatively, a user can authenticate while connecting to *Percona Server for MongoDB*:

```{.bash data-prompt="$"}
$ mongo --host localhost --port 27017 --authenticationMechanism PLAIN --authenticationDatabase \$external -u christian -p
```

!!! admonition ""

    This section is based on the blog post [Percona Server for MongoDB Authentication Using Active Directory](https://www.percona.com/blog/2018/12/21/percona-server-for-mongodb-authentication-using-active-directory/) by *Doug Duncan*:

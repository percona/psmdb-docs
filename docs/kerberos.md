# Setting up Kerberos authentication

This document provides configuration steps for setting up [Kerberos Authentication](authentication.md#kerberos-authentication) in Percona Server for MongoDB.

## Assumptions

The setup of the Kerberos server itself is out of scope of this document. Please refer to the [Kerberos documentation](https://web.mit.edu/kerberos/krb5-latest/doc/admin/install_kdc.html) for the installation and configuration steps relevant to your operation system.

We assume that you have successfully completed the following steps:

* Installed and configured the Kerberos server

* Added necessary [realms](https://web.mit.edu/kerberos/krb5-1.12/doc/admin/realm_config.html)

* Added service, admin and user [principals](https://web.mit.edu/kerberos/krb5-1.5/krb5-1.5.4/doc/krb5-user/What-is-a-Kerberos-Principal_003f.html#What-is-a-Kerberos-Principal_003f)

* Configured the `A` and `PTR` DNS records for every host running `mongod` instance to resolve the hostnames onto Kerberos realm.

## Add user principals to Percona Server for MongoDB

To get authenticated, users must exist both in the Kerberos and Percona Server for MongoDB servers with exactly matching names.

After you defined the user principals in the Kerberos server, add them to the `$external` database in Percona Server for MongoDB and assign required roles:

```javascript
> use $external
> db.createUser({user: "demo@PERCONATEST.COM",roles: [{role: "read", db: "admin"}]})
```

Replace `demo@PERCONATEST.COM` with your username and Kerberos realm.

## Configure Kerberos keytab files

A keytab file stores the authentication keys for a service principal representing a `mongod` instance to access the Kerberos admin server.

After you have added the service principal to the Kerberos admin server, the entry for this principal is added to the `/etc/krb5.keytab` keytab file.

The `mongod` server must have access to the keytab file to authenticate. To keep the keytab file secure, restrict the access to it only for the user running the `mongod` process.


1. Stop the `mongod` service

    ```{.bash data-prompt="$"}
    $ sudo systemctl stop mongod
    ```

2. [Generate the keytab file](https://web.mit.edu/kerberos/krb5-1.5/krb5-1.5.4/doc/krb5-install/The-Keytab-File.html) or get a copy of it if you generated the keytab file on another host. Save the keyfile under a separate path (e.g. `/etc/mongodb.keytab`)

    ```{.bash data-prompt="$"}
    $ cp /etc/krb5.keytab /etc/mongodb.keytab
    ```

3. Change the ownership to the keytab file

    ```{.bash data-prompt="$"}
    $ sudo chown mongod:mongod /etc/mongodb.keytab
    ```

4. Set the `KRB5_KTNAME` variable in the environment file for the `mongod` process.

    === "Debian and Ubuntu"

         Edit the environment file at the path `/etc/default/mongod` and specify the `KRB5_KTNAME` variable:

         ```init
         KRB5_KTNAME=/etc/mongodb.keytab
         ```

         If you have a different path to the keytab file, specify it accordingly.

    === "RHEL and derivatives"

         Edit the environment file at the path `/etc/sysconfig/mongod` and specify the `KRB5_KTNAME` variable:

         ```
         KRB5_KTNAME=/etc/mongodb.keytab
         ```

         If you have a different path to the keytab file, specify it accordingly.

5. Restart the `mongod` service

    ```{.bash data-prompt="$"}
    $ sudo systemctl start mongod
    ```

## Percona Server for MongoDB configuration

Enable external authentication in Percona Server for MongoDB configuration. Edit the `etc/mongod.conf` configuration file and specify the following configuration:

```yaml
security:
  authorization: "enabled"

setParameter:
  authenticationMechanisms: GSSAPI
```

Restart the `mongod` service to apply the configuration:

```{.bash data-prompt="$"}
$ sudo systemctl start mongod
```

## Test the access to Percona Server for MongoDB


1. Obtain the Kerberos ticket for the user using the `kinit` command and specify the user password:

    ```{.bash data-prompt="$"}
    $ kinit demo
    Password for demo@PERCONATEST.COM:
    ```

2. Check the user ticket:
    
    ```{.bash data-prompt="$"}
    $ klist -l
    ```

    Output:

    ```{.text .no-copy}
    Principal name                 Cache name
    --------------                 ----------
    demo@PERCONATEST.COM           FILE:/tmp/<ticket>
    ```


3. Connect to Percona Server for MongoDB:

    ```{.bash data-prompt="$"}
    $ mongo --host <hostname> --authenticationMechanism=GSSAPI --authenticationDatabase='$external' --username demo@PERCONATEST.COM
    ```

    The result should look like the following:

    ```{.javascript .no-copy}
    > db.runCommand({connectionStatus : 1})
    {
         "authInfo" : {
                 "authenticatedUsers" : [
                         {
                                 "user" : "demo@PERCONATEST.COM",
                                 "db" : "$external"
                         }
                 ],
                 "authenticatedUserRoles" : [
                         {
                                 "role" : "read",
                                 "db" : "admin"
                         }
                 ]
         },
         "ok" : 1
    }
    ```

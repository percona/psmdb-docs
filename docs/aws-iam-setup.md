# Setting up AWS IAM authentication

This document provides guidelines how to configure Percona Server for MongoDB to use AWS IAM authentication. The use of this authentication method enables you to natively integrate Percona Server for MongoDB with AWS services, increase security of your infrastructure by setting up password-less authentication and offload your DBAs from managing different sets of secrets. To learn more, see [AWS IAM authentication](aws-iam.md)

To configure AWS IAM authentication means to set up your AWS environment and configure Percona Server for MongoDB. The AWS environment setup is out of scope of this document. Consult the AWS documentation to perform the following setup steps: 

1.	[Configure the AWS resource to work with IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html). 
2.	For user authentication: 
      
      * [Create the IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html) and copy its ARN (Amazon Resource Name)

    For role authentication:

      * [Create the IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html)
      * Attach the IAM role to the AWS resource.
      * Copy the ARN of the IAM role. 

## Configure Percona Server for MongoDB

The steps are the following:

1. Create users in the `$external` database with the username as the IAM user/role ARN
2. Enable authentication and specify the authentication mechanism as `MONGODB-AWS`.

### Create users in `$external` database

During the authentication, Percona Server for MongoDB matches the ARN of the IAM user or role retrieved from AWS STS against the user created in the `$external` database. Thus, the username for this user must include their ARN  and have the following format:

=== "User authentication"

     ```
     arn:aws:iam::<ARN>:user/<user_name>
     ```

=== "Role authentication"

     ```
     arn:aws:iam::<ARN>:role/<role_name>
     ```

Create a user and assign the required roles to them. Specify the ARN and names in the following example commands:

=== "User authentication"

     ```{.javascript data-prompt=">"}
     > use $external
     > db.createUser(
     	{
     		user: "arn:aws:iam::000000000000:user/myUser",
     		roles: [{role: "read", db: "admin"}]
     	}
     )
     ```

=== "Role authentication"

     ```{.javascript data-prompt=">"}
     > use $external
     > db.createUser(
     	{
     		user: "arn:aws:iam::111111111111:role/myRole",
     		roles: [{role: "read", db: "admin"}]
     	}
     )
     ```

### Enable authentication

Run the following commands as root or via `sudo`

1. Stop the `mongod` service

    ```{.bash data-prompt="$"}
    $ sudo systemctl stop mongod
    ```

2. Edit the `/etc/mongod.conf` configuration file

    ```yaml
    security:
      authorization: enabled

    setParameter:
      authenticationMechanisms: MONGODB-AWS
    ```

3. Start the `mongod` service

    ```{.bash data-prompt="$"}
    $ sudo systemctl start mongod
    ```

## Authenticate in Percona Server for MongoDB using AWS IAM

To test the authentication, use either of the following methods:

=== "MongoDB connection string" 

     Replace `<aws_access_key_id>`, `<aws_secret_access_key>` and `psmdb.example.com` with actual values in the following command:

     ```{.bash data-prompt="$"}
     $ mongosh 'mongodb://<aws_access_key_id>:<aws_secret_access_key>:@psmdb.example.com/admin?authSource=$external&authMechanism=MONGODB-AWS'
     ```
 
     To pass temporary credentials and AWS token, replace `<aws_access_key_id>`, `<aws_secret_access_key>`, `<aws_session_token>` and `psmdb.example.com` in the following command:

     ```{.bash data-prompt="$"}
     $ mongosh 'mongodb://<aws_access_key_id>:<aws_secret_access_key>:@psmdb.example.com/admin?authSource=$external&authMechanism=MONGODB-AWS&authMechanismProperties=AWS_SESSION_TOKEN:<aws_session_token>'
     ```

=== "Environment variables"

     Set AWS environment variables:

     ```bash
     export AWS_ACCESS_KEY_ID='<aws_access_key_id>'
     export AWS_SECRET_ACCESS_KEY='<aws_secret_access_key>'
     export AWS_SESSION_TOKEN='<aws_session_token>'
     ```

     Connect to Percona Server for MongoDB:

     ```{.bash data-prompt="$"}
     $ mongosh 'mongodb://psmdb.example.com/testdb?authSource=$external&authMechanism=MONGODB-AWS'
     ```

=== "AWS resource metadata"
     
     If your application is running on the AWS resource, it receives the credentials from the resource metadata. To connect to Percona Server for MongoDB, run the command as follows:

     ```{.bash data-prompt="$"}
     $ mongosh --authenticationMechanism=MONGODB-AWS --authenticationDatabase='$external'
     ```

Upon successful authentication, the result should look like the following: 

``` {.javascript .no-copy}          
> db.runCommand( { connectionStatus: 1 })
{
  authInfo: {
    authenticatedUsers: [
      {
        user: 'arn:aws:iam::00000000000:user/myUser',
        db: '$external'
      }
    ],
    authenticatedUserRoles: [ { role: 'read', db: 'admin' } ]
  },
  ok: 1
}
```

*[AWS]: Amazon Web Service
*[IAM]: Identity Access Management
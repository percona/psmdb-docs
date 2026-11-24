We build and test Percona Server for MongoDB only on the latest versions of Amazon Linux 2023. Because of the way Amazon Linux updates their libraries, Percona Server for MongoDB works only on specific Amazon Linux versions. 

The following table records compatibility for earlier 8.0 releases.
Do not use these rows to select an Amazon Linux version for a 9.0 deployment.
Check the [supported platforms](https://www.percona.com/services/policies/percona-software-platform-lifecycle) before you install or upgrade.

| Percona Server for MongoDB version | Amazon Linux 2023 version |
|------------------------------------|---------------------------|
| 8.0.4-2                            | 2023.6.x and older        |
| 8.0.8-3                            | 2023.7.x and newer        |

To upgrade Percona Server for MongoDB, make sure that you run a compatible version of Amazon Linux 2023. Use the [update instructions :octicons-link-external-16:](https://docs.aws.amazon.com/linux/al2023/ug/updating.html) to update the operating system.
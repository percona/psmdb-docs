# Percona Server for MongoDB Pro

Percona Server for MongoDB Pro is a build of Percona Server for MongoDB that contains purpose-built enterprise [features](#features). It is wrapped in packages created and tested by Percona and is available exclusively for Percona customers.

Percona Server for MongoDB Pro is available starting with version [7.0.4-2](release_notes/7.0.4-2.md).

[Become a Percona Customer](https://www.percona.com/about/contact){.md-button}

Non-paying Percona software users can also benefit from Percona Pro Builds, but they’ll have to [build them from the source code](install/source.md) provided by Percona and available to everyone.

## Features

Find the list of solutions available in Percona Server for MongoDB Pro builds:

| Name                                | Version added | Description  | 
| ----------------------------------- | ------------- | -------------
| [FIPS support ](fips.md)| [7.0.4-2](release_notes/7.0.4-2.md) | FIPS mode provides a way to use FIPS-compliant encryption and run the Percona Server for MongoDB with the FIPS-140 certified library for OpenSSL. This helps customers meet minimum security requirements for cryptographic modules and testing in both hardware and software. |
| [File copy-based initial sync](initial-sync.md) | [7.0.21-12](release_notes/7.0.21-12.md) | File copy based initial sync is an additional method of doing an initial sync for a new node in a replica set. For big data sets, this method is faster than the logical sync as it copies physical files rather than cloning data. |
| Binaries with debug symbols | [7.0.18-11](release_notes/7.0.18-11.md) | By including debug symbols in the binary, Percona Server for MongoDB enables deeper integration with monitoring agent-based solutions. These agents can instrument the binary at runtime, providing more detailed telemetry data, such as performance metrics, error tracking, and function-level diagnostics. This enhanced observability allows for better monitoring of system health, faster identification of issues, and more granular insights into how the application performs in production environments.<br> Including this information empowers teams to respond proactively to performance bottlenecks, optimize resource allocation, and improve the overall stability of the application with real-time insights. 

## Benefits

* Save on deploying and maintaining build infrastructure as we do the build and testing for you 
* Longer support for older versions of operating systems.  

[Install Percona Server for MongoDB Pro](install/install-pro.md){.md-button}

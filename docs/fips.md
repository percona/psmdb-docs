# FIPS compliance

!!! note "Version added: [6.0.9-7](release_notes/6.0.9-7.md)"

FIPS (Federal Information Processing Standard) is the US government computer security standard for cryptography modules that include both hardware and software components. Percona Server for MongoDB supports FIPS certified module for OpenSSL, enabling US organizations to introduce FIPS-compliant encryption and thus meet the requirements towards data security.  

The FIPS compliance in Percona Server for MongoDB is implemented in the same way, as in MongoDB Enterprise Advanced. 

## Platform support

You can run Percona Server for MongoDB in FIPS mode on all [supported operating systems](https://www.percona.com/services/policies/percona-software-support-lifecycle#mongodb). To use FIPS mode for Percona Server for MongoDB, your Linux system must be configured with the OpenSSL FIPS certified module.

Note, that FIPS modules on Ubuntu 24.04 are not available yet as they are awaiting final certification by CMVP.

See [Configure MongoDB for FIPS](https://www.mongodb.com/docs/v6.0/tutorial/configure-fips/) in MongoDB documentation for configuration guidelines. 

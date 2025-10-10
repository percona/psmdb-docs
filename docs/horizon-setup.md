# Configure horizons in Percona Server for MongoDB

This document focuses on configuring horizons in Percona Server for MongoDB deployed in Docker. 

For using horizons in Kubernetes environment with Percona Operator for MongoDB, see the [Expose replica set with split-horizon DNS](https://docs.percona.com/percona-operator-for-mongodb/expose.html#exposing-replica-set-with-split-horizon-dns) chapter in Percona Operator for MongoDB documentation.

## Requirements

To use horizons in Percona Server for MongoDB, you must be aware of and meet these requirements enforced by the database:

* **You must use TLS in your deployment**. Horizons rely entirely on the Server Name Indication (SNI) during the TLS handshake. Connections without TLS will not allow the server to determine the correct identity via SNI, and horizons will not function.

* **TLS certificates** must be Multi-SAN (Subject Alternative Name) certificates that cover both the internal hostname (e.g., `mongo1`) and the external hostname (e.g., `external.domain.com`).

* **Use only hostnames or domain names in horizon definition**. SNI requires a hostname or a resolvable domain name to match against. Percona Server for MongoDB will reject horizon configuration that uses raw IPs.

* **Avoid duplicate hostnames.** Each horizon hostname and port must be unique across the replica set. You can’t reuse the same external name for multiple members. Percona Server for MongoDB needs to clearly map each horizon to one node.

* **All-or-nothing configuration**. If one member defines a horizon, all other members must define one too. You cannot mix members with and without horizons.

## Configuration

In this configuration, we focus on using the Docker Compose, as it simplifies the control of your entire application stack and makes it easy to manage services, networks, and volumes in a single YAML configuration file.

For testing purposes, we will expose `localhost` as the external hostname as we will be accessing the replica set from the MongoDB client running locally, to emulate the access from the outside network. In production, you must use valid domain names.

### Preconditions

Before you start, ensure you have the following:

1. Docker Engine and Docker Compose running on your machine. Refer to [Docker documentation :octicons-link-external-16:](https://docs.docker.com/compose/install/) for how to get Docker Compose.
2. `cfssl` and `cfssljson` tools installed on your machine.
3. Your user has the `root` or `sudo` privileges. 

### Generate Multi-SAN TLS certificates

At this step you need to create CA and certificates where each server cert is valid for both its internal container hostname (e.g., `mongo1`) and the external access hostname (`localhost` in this example).

1. Create a directory to store your TLS certificates. 

    ```{.bash data-prompt="$"}
    $ mkdir certs && cd certs
    ```

2. Create the Certificate Authority (CA) signing request file:

    ```{.bash data-prompt="$"}
    $ tee ca-csr.json <<EOF
    {
      "CN": "MyTestCA",
      "key": { "algo": "rsa", "size": 2048 },
      "names": [{ "C": "US", "ST": "CA", "L": "SF", "O": "Acme", "OU": "MongoDB CA" }]
    }
    EOF
    ```

    This command creates a `ca-csr.json` file describing the CA.

3. Generate the self-signed CA certificate and key:

    ```{.bash data-prompt="$"}
    $ cfssl gencert -initca ca-csr.json | cfssljson -bare ca
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        2025/10/10 14:08:35 [INFO] generating a new CA key and certificate from CSR
        2025/10/10 14:08:35 [INFO] generate received request
        2025/10/10 14:08:35 [INFO] received CSR
        2025/10/10 14:08:35 [INFO] generating key: rsa-2048
        2025/10/10 14:08:35 [INFO] encoded CSR
        2025/10/10 14:08:35 [INFO] signed certificate with serial number 314115126271842123131863341190609880955557607219
        ```

    This produces:

    - `ca.pem` — CA certificate
    - `ca-key.pem` — CA private key

4. Now, create server certificate requests for each MongoDB server (mongo1, mongo2, mongo3), including both internal and external names in the "hosts" array:

    ```{.bash data-prompt="$"}
    $ for i in 1 2 3; do
        name="mongo$i"
        tee "${name}-csr.json" <<EOF
    {
      "CN": "${name}",
      "hosts": ["${name}", "${name}.internal", "localhost", "127.0.0.1"],
      "key": { "algo": "rsa", "size": 2048 },
      "names": [
        { "O": "MongoDB", "OU": "Database", "L": "Internal", "ST": "DC", "C": "US" }
      ]
    }
    EOF
    done
    ```

    This loop creates a request for each server certificate containing the correct Subject Alternative Names for both Docker internal and external access.

    The resulting files are: `mongo1-csr.json`,  `mongo2-csr.json`,  `mongo3-csr.json`.

5. Generate and combine server certificates

    ```{.bash data-prompt="$"}
    for i in 1 2 3; do
        name="mongo$i"

        cat > "${name}-config.json" <<EOF
    {
      "signing": {
        "default": {
          "expiry": "8760h",
          "usages": [
            "signing",
            "key encipherment",
            "server auth",
            "client auth"
          ]
        }
      }
    }
    EOF

        cfssl gencert \
          -ca=ca.pem -ca-key=ca-key.pem \
          -config="${name}-config.json" \
          "${name}-csr.json" | cfssljson -bare "${name}"

        cat "${name}.pem" "${name}-key.pem" > "${name}-combined.pem"
    done
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        2025/10/10 14:11:44 [INFO] generate received request
        2025/10/10 14:11:44 [INFO] received CSR
        2025/10/10 14:11:44 [INFO] generating key: rsa-2048
        2025/10/10 14:11:45 [INFO] encoded CSR
        2025/10/10 14:11:45 [INFO] signed certificate with serial number     583125517108194834444624157976948904278489390606
        ....
        ```

    This loop creates the certificate and private key for each mongo node, then combines them into a single file as required by mongod (`--tlsCertificateKeyFile`).

    After running these commands, the `certs` directory will contain:

    - `mongo1.pem`, `mongo2.pem`, `mongo3.pem` — certificates for each server
    - `mongo1-key.pem`, `mongo2-key.pem`, `mongo3-key.pem` — corresponding private keys
    - `mongo1-combined.pem`, `mongo2-combined.pem`, `mongo3-combined.pem` — certificate and key combined in one file
    - `ca.pem` — certificate authority to be used by all members

### Deploy Percona Server for MongoDB in Docker

1. To simplify deploying Percona Server for MondoDB in Docker, create a Docker compose file with all required configuration. For each container, we map an internal MongoDB port `27017` to external ports `27017`, `27018` and `27019`:

    ```{.bash data-prompt="$"}
    $ tee test-horizons.yml <<EOF
    name: horizons
    services:
        mongo1:
            container_name: mongo1
            image: percona/percona-server-mongodb:latest
            volumes:
                - ./certs:/certs
            ports:
                - "27017:27017"
            command: >
                mongod --replSet rs0 --bind_ip_all
                       --tlsMode requireTLS
                       --tlsCertificateKeyFile /certs/mongo1-combined.pem
                       --tlsCAFile /certs/ca.pem
        mongo2:
            container_name: mongo2
            image: percona/percona-server-mongodb:latest
            volumes:
                - ./certs:/certs
            ports:
                - "27018:27017"
            command: >
                mongod --replSet rs0 --bind_ip_all
                       --tlsMode requireTLS
                       --tlsCertificateKeyFile /certs/mongo2-combined.pem
                       --tlsCAFile /certs/ca.pem
        mongo3:
            container_name: mongo3
            image: percona/percona-server-mongodb:latest
            volumes:
                - ./certs:/certs
            ports:
                - "27019:27017"
            command: >
                mongod --replSet rs0 --bind_ip_all
                       --tlsMode requireTLS
                       --tlsCertificateKeyFile /certs/mongo3-combined.pem
                       --tlsCAFile /certs/ca.pem
    networks:
        default:
            driver: bridge
    EOF
    ```

2. Start Percona Server for MongoDB using this file:

    ```{.bash data-prompt="$"}
    $ docker-compose -f test-horizons.yml up -d
    ```
    
    The command does the following:

    * reads the configuration file
    * starts Percona Server for MongoDB containers with defined certificates in a detached mode

### Initiate the replica set with horizons

With Percona Server for MongoDB up and running, initiate the replica set and specify the horizons in its configuration.

1. Connect to one of the nodes and start the `bash` session:

    ```{.bash data-prompt="$"}
    $ docker exec -it mongo1 -- /bin/bash
    ```

2. Authenticate in Percona Server for MongoDB with enabled TLS:

    ```{.bash data-prompt="$"}
    $ mongosh --tls --tlsCertificateKeyFile /certs/mongo1-combined.pem --tlsAllowInvalidCertificates
    ```

3. Initialize the replica set with horizons. Specify the internal hostname for the `host` field and the external external hostname/port in the `horizons` field for the replica set configuration:

    ```javascript
    rs.initiate({
       _id: "rs0",
       members: [
         {
           _id: 0,
           host: "mongo1:27017", // Internal address
           horizons: { external: "localhost:27017" } // External address
         },
         {
           _id: 1,
           host: "mongo2:27017",
           horizons: { external: "localhost:27018" }
         },
         {
           _id: 2,
           host: "mongo3:27017",
           horizons: { external: "localhost:27019" }
         }
       ]
    }) 
    ```

4. Check the replica set configuration:

    ```javascript
    rs.status()
    ```

### Test connection to Percona Server for MongoDB

Now let's verify that Percona Server for MongoDB is reachable from both inside and outside networks.

**Internal connection**

To check internal connection, you can spin up a new Docker container with the MongoDB client in the same network or execute into one of existing containers and connect to the replica set.

1. To spin up a new container, you must mount the certificates directory into the container when you start it:

   ```{.bash data-prompt="$"}
   $ docker run -d \
     --name mongo-test \
     --network horizons_default \
     -v <path/to/certs>:/certs \
     -p 27020:27017 \
     --restart always \
     percona/percona-server-mongodb:8.0
   ```

2. Execute in the container and connect to the replica set:

    ```{.bash data-prompt="$"}
    $ docker exec -it mongo-test mongosh \
      --host "rs0/mongo1:27017,mongo2:27017,mongo3:27017" \
      --tls \
      --tlsCertificateKeyFile /certs/mongo1-combined.pem \
      --tlsCAFile /certs/ca.pem
    ```

    ??? example "Sample output"
        
        ```{.text .no-copy}
        Current Mongosh Log ID:	68e90919857364d663248377
        Connecting to:		mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0&tls=true&tlsCertificateKeyFile=%2Fcerts%2Fmongo1-combined.pem&tlsCAFile=%2Fcerts%2Fca.pem&appName=mongosh+{{mongosh}}
        Using MongoDB:		{{release}}
        Using Mongosh:		{{mongosh}}

        rs0 [primary] test>
        ```

3. Check the replica set topology:

    ```{.javascript data-prompt="test>"}
    test> db.hello()
    ```

    ??? example "Sample output"

        ```{.text .no-edit}
        {
          topologyVersion: {
            processId: ObjectId('68e786bf0223ec7011474d9b'),
            counter: Long('40')
          },
          hosts: [ 'mongo1:27017', 'mongo2:27017', 'mongo3:27017' ],
          ...
        }
        ```

**External connection**

1. Connect to the replica set from the MongoDB client (Compass or `mongosh`) using the external hostnames you defined in horizons:

    ```{.bash data-prompt="$"}
    $ mongosh "mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0" --tls --tlsCertificateKeyFile /certs/mongo1-combined.pem --tlsCAFile /certs/ca.pem
    ```

    ??? example "Sample output"

        ```{.text .no-copy}
        Current Mongosh Log ID: 68e90919857364d663248377
        Connecting to:  mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0&tls=true&tlsCertificateKeyFile=%2Fcerts%2Fmongo1-combined.pem&tlsCAFile=%2Fcerts%2Fca.pem&appName=mongosh+{{mongosh}}
        Using MongoDB:  {{release}}
        Using Mongosh:  {{mongosh}}

        rs0 [primary] test>
        ```

2. Check the replica set topology:

    ```{.javascript data-prompt="test>"}
    test> db.hello()
    ```

    ??? example "Sample output"

        ```{.text .no-edit}
        {
          topologyVersion: {
            processId: ObjectId('68e786bf0223ec7011474d9b'),
            counter: Long('40')
          },
           hosts: [ 'localhost:27017', 'localhost:27018', 'localhost:27019' ],
          ...
        }
        ```

!!! admonition

    This setup is based on the blog post [Using replicaSetHorizons in MongoDB](https://www.percona.com/blog/using-replicasethorizons-in-mongodb/) by *Ivan Groenewold*.

# Run Percona Server for MongoDB in a Docker container

Docker images of Percona Server for MongoDB are hosted publicly on Docker Hub at
[https://hub.docker.com/r/percona/percona-server-mongodb/](https://hub.docker.com/r/percona/percona-server-mongodb/).

For more information about using Docker, see the [Docker Docs](https://docs.docker.com/).

!!! note 

    Make sure that you are using the latest version of Docker.  The ones provided via `apt` and `yum` may be outdated and cause errors.

    By default, Docker will pull the image from Docker Hub if it is not available locally.

    We gather [Telemetry data](telemetry.md) to understand the use of the software and improve our products.

To run the latest Percona Server for MongoDB 4.4 in a Docker container, run the following command as the root user or via `sudo`:

=== "On x86_64 platforms"

     ```{.bash data-prompt="$"}
     $ docker run -d --name psmdb --restart always \
     percona/percona-server-mongodb:4.4
     ```

=== "On ARM64 platforms"

    The Docker image is available starting with version 4.4.24-23.

      ```{.bash data-prompt="$"}
      $ docker run -d --name psmdb --restart always \
      percona/percona-server-mongodb:<TAG>-arm64
      ```
     
      Replace the `<TAG>` with the desired version (for example, 4.4.24-23-arm64)

The command does the following:


* The `docker run` command instructs the `docker` daemon
to run a container from an image.

* The `-d` option starts the container in detached mode
(that is, in the background).

* The `--name` option assigns a custom name for the container
that you can use to reference the container within a Docker network.
In this case: `psmdb`.

* The `--restart` option defines the container’s restart policy.
Setting it to `always` ensures that the Docker daemon
will start the container on startup
and restart it if the container exits.

* `percona/percona-server-mongodb:4.4`/`percona/percona-server-mongodb:<TAG>-arm64` is the name and version tag
of the image to derive the container from.

## Connecting from another Docker container

The Percona Server for MongoDB container exposes standard MongoDB port (27017),
which can be used for connection from an application
running in another container.

For example, to set up a replica set for testing purposes, you have the following options:

* Interconnect the `mongod` nodes in containers on a default `bridge` network. In this scenario, containers communicate with each other by their IP address.
* Create a [user-defined network](https://docs.docker.com/network/bridge/) and interconnect the `mongod` nodes on it. In this scenario, containers communicate with each other by name.
* Automate the container provisioning and the replica set setup via the [Docker Compose tool](https://docs.docker.com/compose/).

In the following example, `rs101`, `rs102`, `rs103` are the container names for Percona Server for MongoDB and `rs` is the replica set name.

=== "Bridge network"

    When you start Docker, a default `bridge` network is created and all containers are automatically attached to it unless otherwise specified. 

    1.  Start the containers and expose different ports

         ```{.bash data-prompt="$"}
         $ docker run --rm -d --name rs101 -p 27017:27017  percona/percona-server-mongodb:4.4 --port=27017 --replSet rs
         $ docker run --rm -d --name rs102 -p 28017:28017  percona/percona-server-mongodb:4.4 --port=28017 --replSet rs
         $ docker run --rm -d --name rs103 -p 29017:29017  percona/percona-server-mongodb:4.4 --port=29017 --replSet rs
         ```
    2. Check that the containers are started

        ```{.bash data-prompt="$"}
        $ docker container ls
        ```         

        Output:

        ```{.text .no-copy}
        CONTAINER ID  IMAGE                                         COMMAND               CREATED         STATUS             PORTS                     NAMES
        3a4b70cd386b  percona/percona-server-mongodb:4.4  --port=27017 --re...  3 minutes ago   Up 3 minutes ago   0.0.0.0:27017->27017/tcp  rs101
        c9b40a00e32b  percona/percona-server-mongodb:4.4  --port=28017 --re...  11 seconds ago  Up 11 seconds ago  0.0.0.0:28017->28017/tcp  rs102
        b8aebc00309e  percona/percona-server-mongodb:4.4  --port=29017 --re...  3 seconds ago   Up 3 seconds ago   0.0.0.0:29017->29017/tcp  rs103
        ```

    3. Get the IP addresses of each container

         {% raw %}
         ```{.bash data-prompt="$"}
         $ docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' rs101
         $ docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' rs102
         $ docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' rs103
         ```
         {% endraw %}

    3.  Interconnect the containers and initiate the replica set. Replace `rs101SERVER`, `rs102SERVER` and `rs103SERVER` with the IP address of each respective container.

         ```{.bash data-prompt="$"}
         $ docker exec -ti rs101 mongo --eval 'config={"_id":"rs","members":[{"_id":0,"host":"rs101SERVER:27017"},{"_id":1,"host":"rs102SERVER:28017"},{"_id":2,"host":"rs103SERVER:29017"}]};rs.initiate(config);'
         ```
    4.  Check your setup

         ```{.bash data-prompt="$"}
         $ docker exec -ti rs101 mongo --eval 'rs.status()'
         ```

=== "User-defined network"

    You can isolate desired containers in a user-defined network and provide DNS resolution across them so that they communicate with each other by hostname.

    1. Create the network:

        ```{.bash data-prompt="$"}
        $ docker network create my-network
        ```

    2. Start the containers and connect them to your network, exposing different ports

        ```{.bash data-prompt="$"}
        $ docker run --rm -d --name rs101 --net my-network -p 27017:27017  percona/percona-server-mongodb:4.4 --port=27017 --replSet rs
        $ docker run --rm -d --name rs102 --net my-network -p 28017:28017  percona/percona-server-mongodb:4.4 --port=28017 --replSet rs
        $ docker run --rm -d --name rs103 --net my-network -p 29017:29017  percona/percona-server-mongodb:4.4 --port=29017 --replSet rs
        ```

        Alternatively, you can connect the already running containers to your network:

        ```{.bash data-prompt="$"}
        $ docker network connect my-network rs101 rs102 rs103
        ```       

    3. Interconnect the containers and initiate the replica set. 

        ```{.bash data-prompt="$"}
        $ docker exec -ti rs101 mongo --eval 'config={"_id":"rs","members":[{"_id":0,"host":"rs101:27017"},{"_id":1,"host":"rs102:28017"},{"_id":2,"host":"rs103:29017"}]};rs.initiate(config);'
        ```

    4.  Check your setup

         ```{.bash data-prompt="$"}
         $ docker exec -ti rs101 mongo --eval 'rs.status()'
         ```

=== "Docker Compose"

    As the precondition, you need to have Docker Engine and Docker Compose on your machine. Refer to [Docker documentation](https://docs.docker.com/compose/install/) for how to get Docker Compose.

    1. Create a compose file and define the services in it.

        ```yaml title="docker-compose.yaml"
        version: "3"
        services:
          rs101:
            image: percona/percona-server-mongodb:4.4
            container_name: rs101
            hostname: rs101
            ports:
              - "27017:27017"
            networks:
              - my-network
            command: "--port=27017 --replSet rs"
            
          rs102:
            image: percona/percona-server-mongodb:4.4
            container_name: rs102
            hostname: rs102
            ports:
              - "28017:28017"    
            networks:
              - my-network
            command: "--port=28017 --replSet rs"
            
          rs103:
            image: percona/percona-server-mongodb:4.4
            container_name: rs103
            hostname: rs103
            ports:
              - "29017:29017"    
            networks:
              - my-network
            command: "--port=29017 --replSet rs"
            
          rs-init:
            image: percona/percona-server-mongodb:4.4
            container_name: rs-init
            restart: "no"
            networks:
              - my-network
            depends_on:
              - rs101
              - rs102
              - rs103
            command: >
              mongo --host rs101:27017 --eval 
              '
              config = {
              "_id" : "rs",
              "members" : [
                {
                  "_id" : 0,
                  "host" : "rs101:27017"
                },
                {
                  "_id" : 1,
                  "host" : "rs102:28017"
                },
                {
                  "_id" : 2,
                  "host" : "rs103:29017"
                }
              ]
              };
              rs.initiate(config);
              ' 
        networks:
          my-network:
            driver: bridge
        ```

    2. Build and run the replica set with Compose 

        ```{.bash data-prompt="$"}
        $ docker compose up -d
        ```

    3.  Check your setup

         ```{.bash data-prompt="$"}
         $ docker exec -ti rs101 mongo --eval 'rs.status()'
         ```

## Connecting with the `mongo` shell

To start another container with the `mongo` shell
that connects to your Percona Server for MongoDB container,
run the following command: 

```{.bash data-prompt="$"}
$ docker run -it --link psmdb --rm percona/percona-server-mongodb:4.4 mongo mongodb://MONGODB_SERVER:PORT/DB_NAME
```

Set `MONGODB_SERVER`, `PORT`, and `DB_NAME` with the IP address of the `psmdb` container, the port of your MongoDB server (default value is 27017), and the name of the database you want to connect to.

You can get the IP address by running this command:

{% raw %}
```{.bash data-prompt="$"}
$ docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' psmdb
```
{% endraw %}

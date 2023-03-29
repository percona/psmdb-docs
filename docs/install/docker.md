# Run Percona Server for MongoDB in a Docker container

Docker images of Percona Server for MongoDB are hosted publicly on [Docker Hub](https://hub.docker.com/r/percona/percona-server-mongodb/).

For more information about using Docker, see the [Docker Docs](https://docs.docker.com/).

!!! note 

    Make sure that you are using the latest version of Docker.  The ones provided via `apt` and `yum` may be outdated and cause errors.

    By default, Docker will pull the image from Docker Hub if it is not available locally.

To run the latest Percona Server for MongoDB 4.2 in a Docker container, run the following command as the root user or vie `sudo`:

```{.bash data-prompt="$"}
$ docker run -d --name psmdb --restart always \
percona/percona-server-mongodb:4.2
```

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

* `percona/percona-server-mongodb:4.2` is the name and version tag
of the image to derive the container from.

## Connecting from another Docker container

The Percona Server for MongoDB container exposes standard MongoDB port (27017),
which can be used for connection from an application
running in another container.

To connect the application container to the `psmdb` container, you can either use the default `bridge` network, or create your own network and attach both containers to it.

=== "Bridge network"
    
    When you start Docker, a default `bridge` network is created and all containers are attached to it unless otherwise specified. 

    To link your application container to the `psmdb` container, do the following:

    1. Get the IP address of the `psmdb` container

        {% raw %}
        ```{.bash data-prompt="$"}
        $ docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' psmdb
        ```
        {% endraw %}

        Output

        ```{.bash .no-copy}
        "172.19.0.2"
        ```

    2. Link the application container. This example shows how to link Percona Backup for MongoDB running in another container to the `psmdb` container. This example assumes that `psmdb` container is running as a single node replica set and that the PBMUSER is created there to run Percona Backup for MongoDB. 

        ```{.bash data-prompt="$"}
        $ docker run --rm  --name pbm  -e PBM_MONGODB_URI="mongodb://PBMUSER:PASSWORD@172.19.0.2:27017/?authSource=admin" -d percona/percona-backup-mongodb
        ```

=== "User-defined network"

    You can isolate desired containers in a user-defined network and provide DNS resolution across them. The containers on the same network also share environment variables which simplifies their administration. Read more about other advantages of user-defined networks in [Docker documentation](https://docs.docker.com/network/bridge/).

    To link the application container with the `psmdb` container on the user-defined network, do the following:

    1. Create the network:

        ```{.bash data-prompt="$"}
        $ docker network create my-network
        ```

    2. Start the `psmdb` container and connect it to the your network

        ```{.bash data-prompt="$"}
        $ docker run --name psmdb --net=my-network -d percona/percona-server-mongodb:4.2
        ```

        Alternatively, you can connect the already running container to your network:

        ```{.bash data-prompt="$"}
        $ docker network connect my-network psmdb
        ```       

    3. Link the application container. This example shows how to link Percona Backup for MongoDB running in another container to the `psmdb` container. This example assumes that `psmdb` container is running as a single node replica set and that the PBMUSER is created there to run Percona Backup for MongoDB. 

        ```{.bash data-prompt="$"}
        $ docker run --rm  --name pbm --net=my-network  -e PBM_MONGODB_URI="mongodb://pbmuser:secretpwd@psmdb:27017/?authSource=admin" -d percona/percona-backup-mongodb
        ```

## Connecting with the `mongo` shell

To start another container with the `mongo` shell
that connects to your Percona Server for MongoDB container,
run the following command: 

```{.bash data-prompt="$"}
$ docker run -it --link psmdb --rm percona/percona-server-mongodb:4.2 mongo mongodb://MONGODB_SERVER:PORT/DB_NAME
```

Set `MONGODB_SERVER`, `PORT`, and `DB_NAME` with the IP address of the `psmdb` container, the port of your MongoDB server (default value is 27017), and the name of the database you want to connect to.

You can get the IP address by running this command:

{% raw %}
```{.bash data-prompt="$"}
$ docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' psmdb
```
{% endraw %}

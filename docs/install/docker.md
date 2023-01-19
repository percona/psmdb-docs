# Run Percona Server for MongoDB in a Docker container

Docker images of Percona Server for MongoDB are hosted publicly on Docker Hub at
[https://hub.docker.com/r/percona/percona-server-mongodb/](https://hub.docker.com/r/percona/percona-server-mongodb/).

For more information about using Docker, see the [Docker Docs](https://docs.docker.com/).

!!! note 

    Make sure that you are using the latest version of Docker.  The ones provided via `apt` and `yum` may be outdated and cause errors.

    By default, Docker will pull the image from Docker Hub if it is not available locally.

To run the latest Percona Server for MongoDB 4.4 in a Docker container, use the following command:

```{.bash data-prompt="$"}
$ docker run -d --name psmdb --restart always \
percona/percona-server-mongodb:4.4
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

* `percona/percona-server-mongodb:4.4` is the name and version tag
of the image to derive the container from.

## Connecting from another Docker container

The Percona Server for MongoDB container exposes standard MongoDB port (27017),
which can be used for connection from an application running in another container.

To link the application container to the `psmdb` container,
use the `--link psmdb` option when running the container with your app.

## Connecting with the `mongo` shell

To start another container with the `mongo` shell
that connects to your Percona Server for MongoDB container,
run the following command: 

```{.bash data-prompt="$"}
$ docker run -it --link psmdb --rm percona/percona-server-mongodb:4.4 mongo mongodb://MONGODB_SERVER:PORT/DB_NAME
```

Set `MONGODB_SERVER`, `PORT`, and `DB_NAME` with the IP address of the `psmdb` container, the port of your MongoDB server (default value is 27017), and the name of the database you want to connect to.

You can get the IP address by running this command:

```{.bash data-prompt="$"}
$ docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' psmdb
```
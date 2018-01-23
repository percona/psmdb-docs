.. _docker:

=====================================
Running |PSMDB| in a Docker Container
=====================================

Docker images of |PSMDB| are hosted publicly on Decker Hub at
https://hub.docker.com/r/percona/percona-server-mongodb/.

For more information about using Docker, see the `Docker Docs`_.

.. _`Docker Docs`: https://docs.docker.com/

.. note:: Make sure that you are using the latest version of Docker.
   The ones provided via ``apt`` and ``yum``
   may be outdated and cause errors.

.. note:: By default, Docker will pull the image from Docker Hub
   if it is not available locally.

To run the latest |PSMDB| 3.6 in a Docker container, use the following command::

 docker run -d \
  --name psmdb \
  --restart always \
  percona/percona-server-mongodb:3.6

The previous command does the following:

* The ``docker run`` command instructs the ``docker`` daemon
  to run a container from an image.

* The ``-d`` option starts the container in detached mode
  (that is, in the background).

* The ``--name`` option assigns a custom name for the container
  that you can use to reference the container within a Docker network.
  In this case: ``psmdb``.

* The ``--restart`` option defines the container's restart policy.
  Setting it to ``always`` ensures that the Docker daemon
  will start the container on startup
  and restart it if the container exits.

* ``percona/percona-server-mongodb:3.6`` is the name and version tag
  of the image to derive the container from.

  For full list of tags,
  see https://hub.docker.com/r/percona/percona-server-mongodb/tags/

Connecting from Another Docker Container
========================================

The |PSMDB| container exposes standard MongoDB port (27017),
which can be used for connection from an application
running in another container.
To link the application container to the ``psmdb`` container,
use the ``--link psmdb`` option when running the container with your app.

Connecting with the Mongo Shell
===============================

To start another container with the ``mongo`` shell
that connects to your |PSMDB| container,
run the following comand::

 docker run -it --link psmdb --rm percona/percona-server-mongodb:mongo mongo -h psmdb


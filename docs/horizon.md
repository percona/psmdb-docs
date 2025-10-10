# Split-DNS horizons usage with Percona Server for MongoDB

This overview explains the horizons feature in Percona Server for MongoDB. If you're familiar with the concept and want to use it, switch to the [Configure horizons in Percona Server for MongoDB](horizon-setup.md).

When you deploy Percona Server for MongoDB in Docker, Kubernetes, or other containerized environments, you may come across the issue that clients within the same network can reach the replica set just fine. However, backup or monitoring tools outside your cluster can't connect. Why does this happen?

Let's have a closer look at how MongoDB discovers replica set members.

When your client connects to the replica set, it uses an IP address or hostname of a node. The hostname can be an external one, for example, `mongo1.external.mydomain.com:27017`. The MongoDB driver treats this as a starting point. It successfully connects and authenticates. Then the driver runs the `db.hello()` command to discover the full replica set topology.

MongoDB responds with the list of member hostnames you defined during `rs.initiate()`. By default, those are internal names like `mongo1` or `mongo1.default.svc.cluster.local`.



If your client is inside the same network (such as inside the same Docker bridge or Kubernetes namespace), it can resolve those names and connect to all members. However, if your client is in an outside network, running on your host machine or in another cloud, it cannot resolve those internal hostnames.

Additionally, port mismatches are common. Containers often expose MongoDB's default port `27017` internally, but map it to different external ports (such as `32768`) to avoid collisions. Thus, even though the initial connection succeeds, the driver fails when trying to reach the rest of the replica set.

To deal with these issues, use the horizons feature available in Percona Server for MongoDB and Percona Operator for MongoDB v1.16.0+.

### How horizons work

Horizons allow each replica set member to advertise alternative hostnames and ports based on the client's access context. Instead of just one identity (host in the `rs.conf`), a member can have a set of identities (horizons) for different access points.

This enables one MongoDB replica set to serve two distinct client networks:

- **Internal access**: Using internal container hostnames (`mongo1:27017`)
- **External access**: Using public DNS records, load balancer hostnames, or specific host-mapped ports (`external-host:30001`)

Horizons rely on a crucial component of the TLS handshake: Server Name Indication (SNI).

Here's how it works:

1. An external client initiates a TLS connection. As part of the handshake, it includes the hostname it is trying to connect to (for example, `external.mongodb.com`) in the SNI field of the ClientHello message.

2. Percona Server for MongoDB receives the connection and inspects the SNI hostname.

3. Percona Server for MongoDB checks its defined horizons. If the hostname presented in the SNI matches a value defined within a horizon (for example, the horizon key named `external`), the server knows the client is connecting via that external context.

4. When the driver later runs `db.hello()`, the server returns the corresponding horizon value (the external hostname/port) in the hosts list. This ensures the client discovers members using addresses it can resolve.

This mechanism makes TLS mandatory for horizons to function. The SNI field is the only way for the server to reliably determine the client's network context.

## When to use horizons

Horizons are especially useful if you:

- Run MongoDB in Kubernetes and need external access
- Use Docker with port mappings and container names
- Deploy across multiple clouds or hybrid environments
- Need to expose MongoDB to external monitoring, backup, or app clients

## Configuration

[Configure horizons in Percona Server for MongoDB](horizon-setup.md){.md-button}
# Split-DNS Horizons usage with Percona Server for MongoDB

This overview explains the Horizons feature in Percona Server for MongoDB. If you're familiar with the concept and want to use it, switch to the [Configure Horizons in Percona Server for MongoDB](horizon-setup.md).

You can deploy Percona Server for MongoDB in different environments:

* on premises with VPN networks hidden behind NAT
* on virtual servers in a public cloud such as AWS EC2 instances, Azure VMs or Google Compute Engine
* in containerized environments such as Docker or Kubernetes
* in hybrid setups where you span replica set across AWS and an on-prem data center 

Regardless of the environment you use, you may come across the issue that clients within the same network can reach the replica set just fine. However, clients running outside your cluster such as backup or monitoring tools can't connect. Why does this happen?

Let's have a closer look at how MongoDB discovers replica set members.

When your client connects to the replica set, it uses an IP address or hostname of a node. The hostname can be an external one, for example, `mongo1.external.mydomain.com:27017`. The MongoDB driver treats this as a starting point. It successfully connects and authenticates. Then the driver runs the `db.hello()` command to discover the full replica set topology.

MongoDB responds with the list of member hostnames you defined during `rs.initiate()`. By default, those are internal names like `mongo1` or `mongo1.default.svc.cluster.local`.

If your client is inside the same network, such as inside the same Docker bridge, Kubernetes namespace, or local subnet — it can resolve those names and connect to all members. But if the client is external, running on your host machine, in another cloud, or across a VPN, it likely cannot resolve those internal hostnames.

Port mismatches add another layer of complexity. Containers often expose MongoDB’s default port 27017 internally, but map it to different external ports (like 32768) to avoid conflicts. Even in non-containerized setups, NAT or firewall rules may rewrite ports, causing the driver to fail when reaching other members.

To solve these issues, use the Horizons feature available in Percona Server for MongoDB and Percona Operator for MongoDB v1.16.0+.

### How Horizons work

Horizons let each replica set member advertise different hostnames and ports depending on how the client connects — whether from inside a container, across clouds, or from a remote datacenter. This ensures reliable discovery and connectivity across diverse environments.

With Horizons configured, a single MongoDB replica set can serve two distinct client networks:

- **Internal access**: Using internal container hostnames (`mongo1:27017`)
- **External access**: Using public DNS records, load balancer hostnames, or specific host-mapped ports (`external-host:30001`)

Horizons rely on a crucial component of the TLS handshake: Server Name Indication (SNI).

Here's how it works:

1. An external client initiates a TLS connection. As part of the handshake, it includes the hostname it is trying to connect to (for example, `external.mongodb.com`) in the SNI field of the ClientHello message.

2. Percona Server for MongoDB receives the connection and inspects the SNI hostname.

3. Percona Server for MongoDB checks its defined Horizons. If the hostname presented in the SNI matches a value defined within a horizon (for example, the horizon key named `external`), the server knows the client is connecting via that external context.

4. When the driver later runs `db.hello()`, the server returns the corresponding horizon value (the external hostname/port) in the hosts list. This ensures the client discovers members using addresses it can resolve.

This mechanism makes TLS mandatory for Horizons to function. The SNI field is the only way for the server to reliably determine the client's network context.

## When to use Horizons

Horizons are especially useful if you:

- Run MongoDB in Kubernetes and need external access
- Use Docker with port mappings and container names
- Deploy across multiple clouds or hybrid environments, where internal and external DNS differ
- Use virtual machines or bare-metal servers with split DNS or custom routing rules
- Need to expose MongoDB to external monitoring, backup, or app clients

## Configuration

[Configure Horizons in Percona Server for MongoDB](horizon-setup.md){.md-button}
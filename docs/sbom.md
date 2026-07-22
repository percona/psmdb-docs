# Software Bill of Materials

A Software Bill of Materials (SBOM) is a machine-readable inventory of the components and dependencies included in a software release. It helps you understand what is included in a build and assess potential security or compliance risks.

Starting with version 8.3, every Percona Server for MongoDB (PSMDB) release includes a [CycloneDX 1.6 :octicons-link-external-16:](https://cyclonedx.org/specification/overview/){:target="_blank"} SBOM in JSON format.

## Why it matters

An SBOM helps you:

- Identify the components and dependencies included in a PBM release.
- Assess known vulnerabilities using SBOM-compatible security scanners.
- Support security reviews, compliance processes, and software supply chain requirements.
- Verify the contents of deployed software artifacts.

## Where to find the SBOM

| Distribution method | SBOM location |
|---|---|
| Binary tarball | `percona-server-mongodb/percona-server-mongodb.cdx.json` |
| RPM package | `/usr/share/doc/percona-server-mongodb-server/sbom.cdx.json` |
| DEB package | `/usr/share/doc/percona-server-mongodb-server/sbom.cdx.json` |
| Docker image | Embedded in the image and available as an attached OCI artifact. See [Docker images](#docker-images). |


## Verifying and scanning the SBOM

The examples below use [Trivy :octicons-link-external-16:](https://trivy.dev/){:target="_blank"}. You can also use other CycloneDX-compatible scanners, such as [Grype :octicons-link-external-16:](https://github.com/anchore/grype){:target="_blank"} or Snyk.

### Binary tarball

```bash
# Confirm the SBOM is bundled
tar tzf percona-server-mongodb.cdx.json | grep cdx.json

# Extract and scan
tar xzf percona-server-mongodb.cdx.json \
    -C /tmp percona-server-mongodb-{{release}}/percona-server-mongodb-{{release}}.cdx.json
trivy sbom --severity HIGH,CRITICAL --ignore-unfixed \
    /tmp/percona-server-mongodb/percona-server-mongodb.cdx.json
```

### RPM package

```bash
# Confirm the package installs the SBOM
rpm -ql percona-server-mongodb-server | grep cdx.json

# Scan it (replace 9.x with your RHEL/OL version)
trivy sbom --severity HIGH,CRITICAL --ignore-unfixed --distro redhat/9.x \
    /usr/share/doc/percona-server-mongodb-server/percona-server-mongodb-server.cdx.json
```

### DEB package

```bash
# Confirm the package installs the SBOM
dpkg -L percona-server-mongodb-server | grep cdx.json

# Scan it
trivy sbom --severity HIGH,CRITICAL --ignore-unfixed \
    /usr/share/doc/percona-server-mongodb-server/percona-server-mongodb-server.cdx.json
```

### Docker images

Each PSMDB Docker image (Docker Hub `percona/percona-server-mongodb-server`, PerconaLab `perconalab/percona-server-mongodb-server`) ships with **two** CycloneDX 1.6 SBOMs that describe overlapping scopes:

| SBOM | Scope | How to access |
|---|---|---|
| **Embedded** | PBM binary and Go modules only | Inside the image filesystem |
| **OCI-attached** | Full image — PBM and UBI9 base OS packages | Registry-side, via the OCI Referrers API |

#### Scan via OCI Referrers API (recommended)

`trivy image --sbom-sources oci` fetches the attached SBOM via the OCI Referrers API and scans it, without pulling the image:

```bash
trivy image --severity HIGH,CRITICAL --ignore-unfixed --sbom-sources oci \
    docker.io/percona-server-mongodb-server
```

#### Scan the embedded SBOM

To scan the embedded SBOM from inside the container image:

```bash
docker run --rm -it --entrypoint cat \
    docker.io/percona/percona-server-mongodb-server \
    /usr/share/doc/percona-server-mongodb-server/percona-server-mongodb-server.cdx.json \
    | trivy sbom --severity HIGH,CRITICAL --ignore-unfixed -
```

#### Advanced: Inspect OCI-attached SBOMs with ORAS

You can use the [ORAS CLI :octicons-link-external-16:](https://oras.land/){:target="_blank"} to discover and download OCI-attached SBOMs.

```bash
# Use the per-architecture tag to resolve directly to the image manifest
oras discover --format tree \
    docker.io/percona/percona-server-mongodb-server-amd64

# Pull the SBOM artifact using the digest from the discover output
oras pull docker.io/percona/percona-server-mongodb-server@sha256:<referrer-digest>
```

# Software Bill of Materials

A Software Bill of Materials (SBOM) is a machine-readable inventory of the components and dependencies included in a software release. It helps you understand what is included in a build and assess potential security or compliance risks.

Starting with version 8.3, every Percona Server for MongoDB (PSMDB) release includes a [CycloneDX :octicons-link-external-16:](https://cyclonedx.org/specification/overview/){:target="_blank"} SBOM in JSON format.

## Why it matters

An SBOM helps you:

- Identify the components and dependencies included in a PSMDB release.
- Assess known vulnerabilities using SBOM-compatible security scanners.
- Support security reviews, compliance processes, and software supply chain requirements.
- Verify the contents of deployed software artifacts.

## Where to find the SBOM

| Distribution method | SBOM location |
|---|---|
| Binary tarball | `doc/sbom.cdx.json` |
| RPM package | `/usr/share/doc/percona-server-mongodb-server/sbom.cdx.json` |
| DEB package | `/usr/share/doc/percona-server-mongodb-server/sbom.cdx.json` |
| Docker image | Embedded in the image and available as an attached OCI artifact. See [Docker images](#docker-images). |


## Verifying and scanning the SBOM

The examples below use [Grype :octicons-link-external-16:](https://github.com/anchore/grype){:target="_blank"}.

!!! note
    [Trivy :octicons-link-external-16:](https://trivy.dev/){:target="_blank"} cannot currently scan the SBOMs included with Percona Server for MongoDB DEB and RPM packages or binary tarballs. Most dependencies in these SBOMs are identified using the GitHub package type, which Trivy does not fully support in this context.

    Trivy can, however, scan the SBOMs associated with Percona Server for MongoDB Docker images.



### Binary tarball

```bash
# Confirm the SBOM is bundled
tar tzf percona-server-mongodb-{{release}}-x86_64.<operating-system>.tar.gz | grep doc/percona-server-mongodb/sbom.cdx.json

# Extract and scan
tar xzf percona-server-mongodb-{{release}}-x86_64.<operating-system>.tar.gz \
    -C /tmp doc/percona-server-mongodb/sbom.cdx.json
grype sbom:/tmp/doc/percona-server-mongodb/sbom.cdx.json
```

### RPM package

```bash
# Confirm the package installs the SBOM
rpm -ql percona-server-mongodb-server | grep sbom.cdx.json

# Scan it (replace 9.x with your RHEL/OL version)
grype sbom:/usr/share/doc/percona-server-mongodb-server/sbom.cdx.json
```

### DEB package

```bash
# Confirm the package installs the SBOM
dpkg -L percona-server-mongodb-server | grep sbom.cdx.json

# Scan it
grype sbom:/usr/share/doc/percona-server-mongodb-server/sbom.cdx.json
```

### Docker images

Each PSMDB Docker image (Docker Hub `docker.io/percona/percona-server-mongodb-server`, PerconaLab `docker.io/perconalab/percona-server-mongodb-server`) ships with **two** CycloneDX SBOMs that describe overlapping scopes:

| SBOM | Scope | CycloneDX version | How to access |
|---|---|---|---|
| **Embedded** | PSMDB packages only | 1.5 | Inside the image filesystem |
| **OCI-attached** | Full image — PSMDB and UBI9 base OS packages | 1.6 | Registry-side, via the OCI Referrers API |

#### Scan via OCI Referrers API (recommended)

`trivy image --sbom-sources oci` fetches the attached SBOM via the OCI Referrers API and scans it, without pulling the image:

```bash
trivy image --severity HIGH,CRITICAL --ignore-unfixed --sbom-sources oci \
    docker.io/percona/percona-server-mongodb-server
```

#### Scan the embedded SBOM

To scan the embedded SBOM from inside the container image: 8.3.7-1-amd64

```bash
docker run --rm -it --entrypoint cat \
    docker.io/percona/percona-server-mongodb \
    /usr/share/doc/percona-server-mongodb/sbom.cdx.json \
    | grype --from sbom
```

#### Advanced: Inspect OCI-attached SBOMs with ORAS

You can use the [ORAS CLI :octicons-link-external-16:](https://oras.land/){:target="_blank"} to discover and download OCI-attached SBOMs.

Use the per-architecture tag to resolve directly to the image manifest:
```bash
oras discover --format tree \
    docker.io/percona/percona-server-mongodb:8.3.4-1-amd64
```
Example output:
```
docker.io/percona/percona-server-mongodb@sha256:<some_fingerprint>
└── application/vnd.cyclonedx+json
    └── sha256:<another_fingerprint>
        └── [annotations]
            └── org.opencontainers.image.created: "2026-07-28T14:24:59Z"
```
Pull the SBOM artifact using the digest from the discover output and see the file locally:
```bash
oras pull docker.io/percona/percona-server-mongodb@sha256:<another_fingerprint>
ls 
```
Example output:
```
percona-server-mongodb-8.3.4-1-amd64.cdx.json
```

# Software Bill of Materials

A Software Bill of Materials (SBOM) is a machine-readable inventory of the components and dependencies included in a software release. It helps you understand what is included in a build and assess potential security or compliance risks.

Starting with version 8.0.18-12, every Percona Server for MongoDB (PSMDB) release includes a [CycloneDX :octicons-link-external-16:](https://cyclonedx.org/specification/overview/){:target="_blank"} SBOM in JSON format.

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

    Trivy can, however, scan the SBOMs attached to Percona Server for MongoDB Docker images as OCI artifacts.

### Binary tarball

```bash
# Confirm the SBOM is bundled
tar tzf percona-server-mongodb-{{release}}-x86_64.<os_codename>.tar.gz \
    | grep doc/sbom.cdx.json

# Extract and scan
tar xzf percona-server-mongodb-{{release}}-x86_64.<os_codename>.tar.gz \
    -C /tmp percona-server-mongodb-{{release}}-x86_64.<os_codename>/doc/sbom.cdx.json
grype sbom:/tmp/percona-server-mongodb-{{release}}-x86_64.<os_codename>/doc/sbom.cdx.json
```

### RPM package

```bash
# Confirm the package installs the SBOM
rpm -ql percona-server-mongodb-server | grep sbom.cdx.json

# Scan it (replace `rhel:9.8` with your `<os_name>:<os_version>`)
grype --distro rhel:9.8 sbom:/usr/share/doc/percona-server-mongodb-server/sbom.cdx.json
```

### DEB package

```bash
# Confirm the package installs the SBOM
dpkg -L percona-server-mongodb-server | grep sbom.cdx.json

# Scan it (replace `ubuntu:24.04` with your `<os_name>:<os_version>`)
grype --distro ubuntu:24.04 sbom:/usr/share/doc/percona-server-mongodb-server/sbom.cdx.json
```

### Docker images

Each PSMDB Docker image (Docker Hub `docker.io/percona/percona-server-mongodb`, PerconaLab `docker.io/perconalab/percona-server-mongodb`) ships with **two** CycloneDX SBOMs that describe overlapping scopes:

| SBOM | Scope | CycloneDX version | How to access |
|---|---|---|---|
| **Embedded** | PSMDB packages only | 1.5 | Inside the image filesystem |
| **OCI-attached** | Full image — PSMDB and UBI9 base OS packages | 1.6 | Registry-side, via the OCI Referrers API |

#### Scan via OCI Referrers API (recommended)

`trivy image --sbom-sources oci` fetches the attached SBOM via the OCI Referrers API and scans it, without pulling the image:

```bash
trivy image --severity HIGH,CRITICAL --sbom-sources oci \
    docker.io/percona/percona-server-mongodb:{{ release }}-amd64
```

#### Scan the embedded SBOM

Scan the embedded SBOM from inside the container image: `{{ release }}-amd64`:

```bash
docker run --rm -it --entrypoint cat \
    docker.io/percona/percona-server-mongodb:{{ release }}-amd64 \
    /usr/share/doc/percona-server-mongodb-server/sbom.cdx.json \
    | grype --from sbom
```

#### Advanced: Inspect OCI-attached SBOMs with ORAS

You can use the [ORAS CLI :octicons-link-external-16:](https://oras.land/){:target="_blank"} to discover and download OCI-attached SBOMs.

Follow these steps:
{.power-number}

1. Use the per-architecture tag to resolve directly to the image manifest:

    ```bash
    oras discover --format tree \
        docker.io/percona/percona-server-mongodb:{{ release }}-amd64
    ```

    ??? example "Output"

        ```text
        docker.io/percona/percona-server-mongodb@sha256:<image_manifest_digest>
        └── application/vnd.cyclonedx+json
            └── sha256:<sbom_artifact_digest>
                └── [annotations]
                    └── org.opencontainers.image.created: "2026-07-28T14:24:59Z"
        ```

        The `<image_manifest_digest>` identifies the container image. The `<sbom_artifact_digest>` identifies the CycloneDX SBOM artifact attached to that image.

2. Copy the SBOM artifact digest from the output and use it to download the SBOM to the current directory. Replace `<sbom_artifact_digest>` with the value displayed after `sha256:`:

    ```bash
    oras pull docker.io/percona/percona-server-mongodb@sha256:<sbom_artifact_digest>
    ```

3. Confirm that the SBOM file was downloaded:

    ```bash
    ls
    ```

    ??? example "Output"

        ```text
        percona-server-mongodb-{{ release }}-amd64.cdx.json
        ```

## Filtering vulnerabilities with OpenVEX

[OpenVEX :octicons-link-external-16:](https://github.com/openvex/spec){:target="_blank"} is an open, minimal format for Vulnerability Exploitability eXchange (VEX) statements. A VEX document records whether a known vulnerability (CVE) in a component actually affects a given product — for example, the vulnerable code path is unreachable, the issue is already fixed, or it's still under investigation. Scanners that support VEX use these statements to suppress vulnerabilities that don't actually apply, cutting down on noise from CVEs in bundled dependencies that PSMDB isn't actually exposed to.

Percona publishes an OpenVEX document for every PSMDB release.

The `VEX` file for version {{ release }} is available at:

`https://percona.github.io/percona-server-mongodb/vex/percona-server-mongodb-{{ release }}.openvex.json`

Pass the document to Grype's `--vex` flag along with any SBOM scan on this page. For example, when scanning the SBOM of an RPM package:

```bash
# Download the OpenVEX document for this release
curl -fsSLO https://percona.github.io/percona-server-mongodb/vex/percona-server-mongodb-{{ release }}.vex.json

# Scan the SBOM and filter out vulnerabilities addressed in the VEX document
grype --distro <os_name>:<os_version> --vex=percona-server-mongodb-{{ release }}.vex.json sbom:/usr/share/doc/percona-server-mongodb-server/sbom.cdx.json
```

!!! note
    The example above reports only [CVE-2026-6231 :octicons-link-external-16:](https://nvd.nist.gov/vuln/detail/cve-2026-6231){:target="_blank"}. This vulnerability affects Percona Server for MongoDB deployments that use [Queryable Encryption :octicons-link-external-16:](https://www.mongodb.com/docs/manual/core/queryable-encryption/about-qe-csfle/){:target="_blank"}. The vulnerability existed before version {{ release }}, but the SBOM now makes it visible. Percona plans to fix it in a future release.
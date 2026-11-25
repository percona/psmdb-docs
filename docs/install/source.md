# Build from source code

Build Percona Server for MongoDB {{psmdb_version}} from the `v{{psmdb_version}}` source branch.
For a reproducible release build, select the corresponding release tag from the
[source repository](https://github.com/percona/percona-server-mongodb/tags).

## Build options

- [Build binaries manually](#manual-build).

- [Build tarballs or packages with the build script](#use-the-build-script).

## Manual build

The {{psmdb_version}} source tree uses Bazel.
Use the [{{psmdb_version}} build requirements](https://github.com/percona/percona-server-mongodb/blob/v{{psmdb_version}}/docs/building.md)
for compiler, Python, and operating system dependencies.

### Build steps {.power-number}

1. Clone the {{psmdb_version}} source tree with submodules:

    ```bash
    git clone --branch v{{psmdb_version}} --recurse-submodules https://github.com/percona/percona-server-mongodb.git
    cd percona-server-mongodb
    ```

2. Install Bazel with the repository helper:

    ```bash
    python3 buildscripts/install_bazel.py
    export PATH="$HOME/.local/bin:$PATH"
    ```

3. Build the server binaries:

    ```bash
    bazel build --config=psmdb_opt_release install-mongod install-mongos
    ```

4. Check the built server version:

    ```bash
    bazel-bin/install-mongod/bin/mongod --version
    ```

The build creates target-specific installation directories under `bazel-bin`.
For other targets, see [Bazel targets](https://github.com/percona/percona-server-mongodb/blob/v{{psmdb_version}}/docs/building.md#bazel-targets).

## Use the build script

The [{{psmdb_version}} packaging script](https://github.com/percona/percona-server-mongodb/blob/v{{psmdb_version}}/percona-packaging/scripts/psmdb_builder.sh)
creates source archives, binary tarballs, and DEB or RPM packages.
Use a disposable build environment for the target operating system.
The dependency installation step requires root access.

The examples use version `{{release}}` as the package version.
The `v{{psmdb_version}}` branch selects branch sources, rather than an immutable release snapshot.
For release builds, use the matching release tag for both the script and `--branch`.

### Prepare the build environment {.power-number}

1. Create separate script and build directories:

    ```bash
    mkdir -p /tmp/psmdb/scripts /tmp/psmdb/build
    cd /tmp/psmdb/scripts
    ```

2. Download the script for the source branch:

    ```bash
    curl -fL https://raw.githubusercontent.com/percona/percona-server-mongodb/v{{psmdb_version}}/percona-packaging/scripts/psmdb_builder.sh -o psmdb_builder.sh
    ```

3. Install dependencies in the build environment:

    ```bash
    sudo bash ./psmdb_builder.sh --builddir=/tmp/psmdb/build --install_deps=1
    ```

### Tarballs

Build a binary tarball from the {{psmdb_version}} source branch:

```bash
bash ./psmdb_builder.sh \
  --builddir=/tmp/psmdb/build \
  --repo=https://github.com/percona/percona-server-mongodb.git \
  --branch=v{{psmdb_version}} --psm_ver={{release.split('-')[0]}} --psm_release={{release.split('-')[1]}} \
  --get_sources=1 --build_tarball=1
```

Find the generated tarballs in `/tmp/psmdb/build/tarball/`.

### Packages

Build packages in an environment that matches the target package format:

=== ":material-debian: DEB"

    ```bash
    bash ./psmdb_builder.sh \
      --builddir=/tmp/psmdb/build \
      --repo=https://github.com/percona/percona-server-mongodb.git \
      --branch=v{{psmdb_version}} --psm_ver={{release.split('-')[0]}} --psm_release={{release.split('-')[1]}} \
      --get_sources=1 --build_src_deb=1 --build_deb=1
    ```

    Find source packages in `/tmp/psmdb/build/source_deb/` and binary packages in `/tmp/psmdb/build/deb/`.

=== ":material-redhat: RPM"

    ```bash
    bash ./psmdb_builder.sh \
      --builddir=/tmp/psmdb/build \
      --repo=https://github.com/percona/percona-server-mongodb.git \
      --branch=v{{psmdb_version}} --psm_ver={{release.split('-')[0]}} --psm_release={{release.split('-')[1]}} \
      --get_sources=1 --build_src_rpm=1 --build_rpm=1
    ```

    Find source packages in `/tmp/psmdb/build/srpm/` and binary packages in `/tmp/psmdb/build/rpm/`.

## Next steps

[Connect to MongoDB :material-arrow-right:](../connect.md){.md-button}

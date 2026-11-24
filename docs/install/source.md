# Build from source code

Build Percona Server for MongoDB 9.0 from the `v9.0` source branch.
For a reproducible release build, select the corresponding release tag from the
[source repository](https://github.com/percona/percona-server-mongodb/tags).

## Build options

- [Build binaries manually](#manual-build).

- [Build tarballs or packages with the build script](#use-the-build-script).

## Manual build

The 9.0 source tree uses Bazel.
Use the [9.0 build requirements](https://github.com/percona/percona-server-mongodb/blob/v9.0/docs/building.md)
for compiler, Python, and operating system dependencies.

### Build steps {.power-number}

1. Clone the 9.0 source tree with submodules:

    ```bash
    git clone --branch v9.0 --recurse-submodules https://github.com/percona/percona-server-mongodb.git
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
For other targets, see [Bazel targets](https://github.com/percona/percona-server-mongodb/blob/v9.0/docs/building.md#bazel-targets).

## Use the build script

The [9.0 packaging script](https://github.com/percona/percona-server-mongodb/blob/v9.0/percona-packaging/scripts/psmdb_builder.sh)
creates source archives, binary tarballs, and DEB or RPM packages.
Use a disposable build environment for the target operating system.
The dependency installation step requires root access.

The examples use version `9.0.8-1` as the package version.
The `v9.0` branch selects branch sources, rather than an immutable release snapshot.
For release builds, use the matching release tag for both the script and `--branch`.

### Prepare the build environment {.power-number}

1. Create separate script and build directories:

    ```bash
    mkdir -p /tmp/psmdb/scripts /tmp/psmdb/build
    cd /tmp/psmdb/scripts
    ```

2. Download the script for the source branch:

    ```bash
    curl -fL https://raw.githubusercontent.com/percona/percona-server-mongodb/v9.0/percona-packaging/scripts/psmdb_builder.sh -o psmdb_builder.sh
    ```

3. Install dependencies in the build environment:

    ```bash
    sudo bash ./psmdb_builder.sh --builddir=/tmp/psmdb/build --install_deps=1
    ```

### Tarballs

Build a binary tarball from the 9.0 source branch:

```bash
bash ./psmdb_builder.sh \
  --builddir=/tmp/psmdb/build \
  --repo=https://github.com/percona/percona-server-mongodb.git \
  --branch=v9.0 --psm_ver=9.0.8 --psm_release=1 \
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
      --branch=v9.0 --psm_ver=9.0.8 --psm_release=1 \
      --get_sources=1 --build_src_deb=1 --build_deb=1
    ```

    Find source packages in `/tmp/psmdb/build/source_deb/` and binary packages in `/tmp/psmdb/build/deb/`.

=== ":material-redhat: RPM"

    ```bash
    bash ./psmdb_builder.sh \
      --builddir=/tmp/psmdb/build \
      --repo=https://github.com/percona/percona-server-mongodb.git \
      --branch=v9.0 --psm_ver=9.0.8 --psm_release=1 \
      --get_sources=1 --build_src_rpm=1 --build_rpm=1
    ```

    Find source packages in `/tmp/psmdb/build/srpm/` and binary packages in `/tmp/psmdb/build/rpm/`.

## Next steps

[Connect to MongoDB :material-arrow-right:](../connect.md){.md-button}

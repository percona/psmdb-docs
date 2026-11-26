> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server-for-mongodb/7.0/llms.txt).

# Uninstall Percona Server for MongoDB

To completely remove Percona Server for MongoDB you need to remove all the installed packages, data and configuration files. If you need the data, consider making a backup before uninstalling Percona Server for MongoDB.

Follow the instructions, relevant to your operating system:

**Uninstall on Debian and Ubuntu**

You can remove Percona Server for MongoDB packages with one of the following commands:

- `apt remove` will only remove the packages and leave the configuration and data files.
- `apt purge` will remove all the packages with configuration files and data.

Choose which command better suits you depending on your needs.

1. Stop the `mongod` server:

   ```bash
   sudo systemctl stop mongod
   ```

1. Remove the packages. There are two options.

   **Keep the configuration and data files**

   ```bash
   sudo apt remove percona-server-mongodb*
   ```

   **Delete configuration and data files**

   ```bash
   sudo apt purge percona-server-mongodb*
   ```

**Uninstall on Red Hat Enterprise Linux and derivatives**

1. Stop the `mongod` service:

   ```bash
   sudo systemctl stop mongod
   ```

1. Remove the packages:

   ```bash
   sudo yum remove percona-server-mongodb*
   ```

1. Remove the data and configuration files:

   ```bash
   sudo rm -rf /var/lib/mongodb
   sudo rm -f /etc/mongod.conf
   ```

   Warning

   This will remove all the packages and delete all the data files (databases, tables, logs, etc.). You might want to back up your data before doing this in case you need the data later.

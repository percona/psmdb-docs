# Minor upgrade of Percona Server for MongoDB

If you are using data-at-rest-encryption with KMIP server, check the [upgrade considerations](../kmip.md#upgrade-considerations)

To upgrade Percona Server for MongoDB to the latest version, follow these steps:


1. Stop the `mongod` service:

    ```{.bash data-prompt="$"}
    $ sudo systemctl stop mongod
    ```

2. [Install the latest version packages](index.md). Use the command relevant to your operating system.

3. Start the `mongod` service:

    ```{.bash data-prompt="$"}
    $ sudo systemctl start mongod
    ```

To upgrade a replica set or a sharded cluster, use the [rolling restart](../glossary.md#term-Rolling-restart) method. It allows you to perform the upgrade with minimum downtime. You upgrade the nodes one by one, while the whole cluster / replica set remains operational.
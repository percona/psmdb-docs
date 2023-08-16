# Percona Server for MongoDB parameter tuning guide

Percona Server for MongoDB includes several parameters that can be changed
in one of the following ways:

=== "Configuration file"

    Use the `setParameter` admonitions in the configuration file
    for persistent changes in production:    

    ```yaml
    setParameter:
      <parameter>: <value>
    ```


=== "Command line"

    use the `--setParameter` command line option arguments when running the `mongod` process
    for development or testing purposes:    

    ```{.bash data-prompt="$"}
    $ mongod \
      --setParameter <parameter>=<value>\
    ```

=== "`setParameter` command"    

    Use the `setParameter` command on the `admin` database
    to make changes at runtime:    

    ```{.javascript data-prompt=">"}
    > db = db.getSiblingDB('admin')
    > db.runCommand( { setParameter: 1, <parameter>: <value> } )
    ```

See what parameters you can define in the [parameters list](https://www.mongodb.com/docs/v7.0/reference/parameters/#parameters).


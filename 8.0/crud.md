> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server-for-mongodb/8.0/llms.txt).

# Manipulate data in Percona Server for MongoDB

After you connected to Percona Server for MongoDB, let’s insert some data and operate with it.

Note

To secure the data, you may wish to use [data-at-rest encryption](https://docs.percona.com/percona-server-for-mongodb/8.0/data-at-rest-encryption.html). Note that you can only enable it on an empty database. Otherwise you must clean up the data directory first.

See the following documentation for data-at-rest encryption:

- [Using HashiCorp Vault server](https://docs.percona.com/percona-server-for-mongodb/8.0/vault.html)
- [Using KMIP server](https://docs.percona.com/percona-server-for-mongodb/8.0/kmip.html)
- [Using a local keyfile](https://docs.percona.com/percona-server-for-mongodb/8.0/keyfile.html)

## Insert data

1. For example, let’s add an item to the `fruits` collection. Use the `insertOne()` command for this purpose:

   ```
   db.fruits.insertOne(
        {item: "apple", qty: 50}
        )
   ```

   If there is no `fruits` collection in the database, it will be created during the command execution.

   Sample output

   ```
   {
     acknowledged: true,
     insertedId: ObjectId('659c2b846252bfad93fc1578')
   }
   ```

1. Now, let’s add more fruits to the `fruits` collection using the `insertMany()` command:

   ```
   db.fruits.insertMany([
        {item: "banana", weight: "kg", qty: 10 }, 
        {item: "peach", weight: "kg", qty: 30}
        ])
   ```

   Sample output

   ```
   {
     acknowledged: true,
     insertedIds: {
       '0': ObjectId('659c2bc46252bfad93fc1579'),
       '1': ObjectId('659c2bc46252bfad93fc157a')
     }
   }
   ```

See [Insert documents](https://www.mongodb.com/docs/manual/tutorial/insert-documents/) for more information about data insertion.

## Query data

Run the following command to query data in MongoDB:

```
db.fruits.find()
```

Sample output

```
[
  { _id: ObjectId('659c2b846252bfad93fc1578'), item: 'apple', qty: 50 },
  {
    _id: ObjectId('659c2bc46252bfad93fc1579'),
    item: 'banana',
    weight: 'kg',
    qty: 10
  },
  {
    _id: ObjectId('659c2bc46252bfad93fc157a'),
    item: 'peach',
    weight: 'kg',
    qty: 30
  }
]
```

Refer to the [Query documents](https://www.mongodb.com/docs/manual/tutorial/query-documents/) documentation to for more information about reading data.

## Update data

Let’s update the `apples` entry by adding weight to it.

1. Use the `updateOne()` command for that:

   ```
   db.fruits.updateOne(
       {"item": "apple" }, 
       {$set: {"weight": "kg"}}
       )
   ```

   Sample output

   ```
   {
     acknowledged: true,
     insertedId: null,
     matchedCount: 1,
     modifiedCount: 1,
     upsertedCount: 0
   }
   ```

1. Query the collection to check the updated document:

   ```
   db.fruits.find({item: "apple"})
   ```

   Sample output

   ```
   [
     {
       _id: ObjectId('659c2b846252bfad93fc1578'),
       item: 'apple',
       qty: 50,
       weight: 'kg'
     }
   ]
   ```

See [Update methods](https://www.mongodb.com/docs/manual/reference/update-methods/) documentation for other available data update methods

## Delete data

Run the following command to delete all documents where the quantity is less than 30 kg:

```
db.fruits.deleteMany(
{"qty": {$lt: 30} }
    )
```

Sample output

```
{ acknowledged: true, deletedCount: 1 }
```

Learn more about deleting data in [Delete methods](https://www.mongodb.com/docs/manual/reference/delete-methods/) documentation.

Congratulations! You have used basic create, read, update and delete (CRUD) operations to manipulate data in Percona Server for MongoDB. See [MongoDB CRUD Concepts](https://www.mongodb.com/docs/manual/core/crud/) manual to learn more about CRUD operations.

## Next steps

[What’s next?](https://docs.percona.com/percona-server-for-mongodb/8.0/what-next.html)

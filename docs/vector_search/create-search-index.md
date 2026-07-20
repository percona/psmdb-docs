# Create Index

You can use the `createSearchIndex()` method to create a single Search or Vector Search index on a collection, or the `createSearchIndexes()` method to create multiple indexes simultaneously.

## Create single Search Index

Follow these steps to create a single search index:
{.power-number}

1. Insert test data from mongosh:

    ```javascript
    use test
    db.docs.insertMany([
    { text: "MongoDB search is powerful" },
    { text: "Vector search is the future" },
    { text: "Full text search with mongot" }
    ])

    {
    acknowledged: true,
    insertedIds: {
        '0': ObjectId('69ebae2599c54be2ea44ba89'),
        '1': ObjectId('69ebae2599c54be2ea44ba8a'),
        '2': ObjectId('69ebae2599c54be2ea44ba8b')
    }
    }
    ```

2. Create a **single Search Index**:

    ```javascript
    db.docs.createSearchIndex({
    name: "search_idx",
    definition: {
        mappings: {
        dynamic: true
        }
    }
    })

    search_idx
    ```

3. Check the status.

    ```javascript
    db.docs.getSearchIndexes()
    [
    {
        id: '69ebae2a651bce4d10f57bdc',
        name: 'search_idx',
        status: 'READY',
        queryable: true,
        latestDefinitionVersion: { version: 0, createdAt: ISODate('2026-04-24T17:53:46.000Z') },
        latestDefinition: { mappings: { dynamic: true } },
        statusDetail: [
        {
            hostname: '69eb5fc573906b6bfb8cefe7',
            status: 'READY',
            queryable: true,
            mainIndex: {
            status: 'READY',
            queryable: true,
            definitionVersion: { version: 0, createdAt: ISODate('2026-04-24T17:53:46.000Z') },
            definition: { mappings: { dynamic: true, fields: {} } }
            }
        }
        ]
    }
    ]
    ```

## Create multiple Search Indexes

The following example creates two Search indexes:

```javascript
db.docs.createSearchIndexes([
  {
    name: "search_idx",
    definition: {
      mappings: {
        dynamic: true
      }
    }
  },
  {
    name: "text_search_idx",
    definition: {
      mappings: {
        dynamic: false,
        fields: {
          text: {
            type: "string"
          }
        }
      }
    }
  }
])
[ 'search_idx', 'text_search_idx' ]
```
This creates:

- `search_idx`, which dynamically indexes supported fields.
- `text_search_idx`, which indexes only the text field.

## Create Search and Vector Search Indexes together

You can include Search and Vector Search index definitions in the same command.

```javascript
db.docs.createSearchIndexes([
  {
    name: "search_idx",
    type: "search",
    definition: {
      mappings: {
        dynamic: false,
        fields: {
          text: {
            type: "string"
          }
        }
      }
    }
  },
  {
    name: "vector_idx",
    type: "vectorSearch",
    definition: {
      fields: [
        {
          type: "vector",
          path: "embedding",
          numDimensions: 3,
          similarity: "cosine"
        }
      ]
    }
  }
])
[ 'search_idx', 'vector_idx' ]
```

## Supported field types

The following field types are supported:

| Field type | Supported source data| Use|
| -----------| ----------------------| --|
| `boolean`           | Boolean                       | Supports exact matching and filtering on `true` and `false` values.                                |
| `date`              | BSON Date                     | Supports exact matches, range and proximity queries, sorting, and faceting.                        |
| `document`          | Object or subdocument         | Defines mappings for fields within a nested object.                                                |
| `embeddedDocuments` | Array of objects              | Indexes objects within an array so that each embedded object can be evaluated independently.       |
| `number`            | `int32`, `int64`, or `double` | Supports exact matches, numeric range and proximity queries, sorting, and faceting.                |
| `objectId`          | `ObjectId`                    | Supports matching, filtering, and range operations on `ObjectId` values.                           |
| `string`            | String                        | Analyzes text for full-text operators such as `text`, `phrase`, `regex`, and `wildcard`. |

For detailed inforamtion on supported feild types, see MongoDB documentation](https://www.mongodb.com/docs/search/index/define-field-mappings/#mongodb-search-field-types)


[Update a search index :material-arrow-right:](../update-search-index.md){.md-button}

[Delete a search index :material-arrow-right:](../delete-search-index.md){.md-button}


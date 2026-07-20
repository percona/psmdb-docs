# Create Search Index

You can use the `createSearchIndex()` method to create a single Search or Vector Search index on a collection, or the `createSearchIndexes()` method to create multiple indexes simultaneously.


## Create single Search Index

The following code shows how to create a **single Search Index** on products collection:

```javascript
db.products.createSearchIndex(
  "products_text_idx",
  {
    mappings: {
      dynamic: false,
      fields: {
        name: {
          type: "string",
          analyzer: "lucene.standard"
        },
        description: {
          type: "string",
          analyzer: "lucene.standard"
        }
      }
    }
  }
);
```

## Create multiple Search Indexes

The following example creates two Search indexes on the products collection:

```javascript
db.runCommand({
  createSearchIndexes: "products",
  indexes: [
    {
      name: "products_text_idx",
      type: "search",
      definition: {
        mappings: {
          dynamic: false,
          fields: {
            name: {
              type: "string",
              analyzer: "lucene.standard"
            },
            description: {
              type: "string",
              analyzer: "lucene.standard"
            }
          }
        }
      }
    },
    {
      name: "products_name_idx",
      type: "search",
      definition: {
        mappings: {
          dynamic: false,
          fields: {
            name: {
              type: "string",
              analyzer: "lucene.simple"
            }
          }
        }
      }
    }
  ]
});
```

## Create Search and Vector Search Indexes together

You can include Search and Vector Search index definitions in the same command.

```javascript
db.runCommand({
  createSearchIndexes: "products",
  indexes: [
    {
      name: "products_text_idx",
      type: "search",
      definition: {
        mappings: {
          dynamic: false,
          fields: {
            name: {
              type: "string",
              analyzer: "lucene.standard"
            },
            description: {
              type: "string",
              analyzer: "lucene.standard"
            }
          }
        }
      }
    },
    {
      name: "products_vector_idx",
      type: "vectorSearch",
      definition: {
        fields: [
          {
            type: "vector",
            path: "embedding",
            numDimensions: 768,
            similarity: "cosine"
          },
          {
            type: "filter",
            path: "category"
          }
        ]
      }
    }
  ]
});
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


[Update a search index :material-arrow-right:](../create-search-index.md){.md-button}
[Delete a search index :material-arrow-right:](../delete-search-index.md){.md-button}


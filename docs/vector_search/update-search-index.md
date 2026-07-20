# Update Index

You can use the `updateSearchIndex()` method to update a Search or Vector Search index. 

!!! warning
    `updateSearchIndex()` replaces the index definition; it does not merge your changes into the existing one. Always submit the complete definition, including the fields you are not changing. Any field you omit is removed from the index.

You cannot rename an index with this method. To rename an index, drop it and create a new one with the desired name.

After you update an index, mongot rebuilds it in the background. The index continues to serve queries with the old definition until the rebuild completes. Use `getSearchIndexes()` to check the rebuild status.

## Update single Search Index

Suppose the `products_text_idx `index currently includes the `name` and `description` fields. The following operation updates the index to include the `category` field as well:

```javascript
db.products.updateSearchIndex(
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
        },
        category: {
          type: "string",
          analyzer: "lucene.standard"
        }
      }
    }
  }
);
```

## Update a Vector Search index

Suppose `products_vector_idx` currently indexes the `embedding` field. The following operation adds `category` as a filter field:

```javascript
db.products.updateSearchIndex(
  "products_vector_idx",
  {
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
);
```

[Delete a search index :material-arrow-right:](../delete-search-index.md){.md-button}



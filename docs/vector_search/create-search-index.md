# Search Indexes

A search index is a data structure that maps the terms in your documents to the documents that contain them. Instead of scanning every document in a collection, a search query looks up terms in the index and retrieves only the matching documents, along with metadata such as term positions and relevance data.

- Search Indexes are maintained by the `mongot` process using Apache Lucene.
- Search queries use the aggregation pipeline stages `$search` and `$searchMeta`.
- When you create a search index, Percona Search for MongoDB transforms your data into a sequence of tokens or terms.


## How Search Indexes work

When you create a search index on a collection, `mongot` does the following:
{.power-number}

1. Performs an initial sync, reading the collection data from mongod and building the Lucene index.
2. Opens a change stream on the collection to watch for inserts, updates, and deletes.
3. Applies those changes to the index continuously, keeping it in sync with the collection.












## Create a Search Index

You can use the `createSearchIndex()` method to create a single Search or Vector Search index on a collection, or the `createSearchIndexes()` method to create multiple indexes simultaneously.

The following code shows how to create a single Search index:

```sh
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



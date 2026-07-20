# Delete Index

Use the `dropSearchIndex()` method to delete a search or vector search index. The method works the same way for both index types:

```javascript
db.products.dropSearchIndex("products_text_idx");
```

Deleting an index is irreversible. To restore search functionality, create the index again with `createSearchIndex()`, and wait for the initial sync to
complete before running queries against it.

!!! warning
    `$search` and `$vectorSearch` queries that reference an index that does not exist return an empty result set rather than an error. If your application starts receiving empty search results after an index change, verify that the index exists and check its status with `getSearchIndexes()`.


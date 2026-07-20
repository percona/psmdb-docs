# Search Indexes

- Percona Search for MongoDB enable performant text search queries by mapping search terms to the documents that contain those terms.
- Search queries use the aggregation pipeline stages `$search` and `$searchMeta`.
- When you create a search index, Percona Search for MongoDB transforms your data into a sequence of tokens or terms.


## Create a Search Index

You can use the `createSearchIndex()` method to create a single Percona Search for MongoDB or Vector Search index on a collection, or the `createSearchIndexes()` method to create multiple indexes simultaneously.



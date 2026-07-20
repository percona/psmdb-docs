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

## Types of Search Indexes

Percona Search for MongoDB supports two index types:

- Search indexes power full-text search with the `$search` and `$searchMeta` stages. They support text analyzers, relevance-based scoring, autocomplete, faceting, and highlighting.
- Vector search indexes power semantic and similarity search with the `$vectorSearch` stage. They index vector embeddings that you store in your documents and support [approximate nearest neighbor (ANN) :octicons-link-external-16:](https://www.mongodb.com/resources/basics/ann-search){:target="_blank"} search. 

For more information, see [how vector search works]().

## Field mappings

A search index definition specifies which fields to index and how to index them. You can choose between two mapping strategies:

- [Dynamic mapping :octicons-link-external-16:](https://www.mongodb.com/docs/search/index/define-field-mappings/#dynamic-mappings){:target="_blank"} indexes all fields of supported types automatically, including fields added to documents later. Fields can be indexed based on the default set of types or by configuring a `typeSet`.

- [Static mapping :octicons-link-external-16:](https://www.mongodb.com/docs/search/index/define-field-mappings/#static-mappings){:target="_blank"} indexes only the fields you explicitly define. To use static mappings to configure index options for only some fields, set `mappings.dynamic` to false and specify the field name, [data type :octicons-link-external-16:](https://www.mongodb.com/docs/search/index/define-field-mappings/#mongodb-search-field-types){:target="_blank"}, and other configuration options for each field that you want to index. You can specify the fields in any order.


[Create a search index :material-arrow-right:](../create-search-index.md){.md-button}

[Update a search index :material-arrow-right:](../cupdate-search-index.md){.md-button}

[Delete a search index :material-arrow-right:](../delete-search-index.md){.md-button}
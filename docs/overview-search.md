# Search overview

Starting with Percona Server for MongoDB (PSMDB) 8.3, you can use **Full-text Search** and **Vector Search** with `mongot`, a dedicated search service that runs alongside `mongod`.

You can create search indexes on your collections and use aggregation pipeline stages such as `$search`, `$searchMeta`, and `$vectorSearch` to retrieve relevant results.

`mongot` is available via binary distributions (tarballs) and Docker images.

## What is mongot?

[mongot :octicons-link-external-16:](https://www.mongodb.com/docs/manual/tutorial/mongot-sizing/advanced-guidance/architecture/){:target="_blank"} is a companion process that builds and maintains search indexes for your MongoDB collections. While `mongod` stores and manages your application data, `mongot` creates optimized search indexes and processes search queries.

The two services communicate internally during query execution:

- `mongod` stores documents and handles database operations.
- `mongot` maintains search indexes.
- Search queries are processed by `mongot`, while `mongod` retrieves the matching documents and returns the results to the client.

This architecture separates search workloads from core database operations while keeping the indexed data synchronized with the database.


## Search types

Percona Server for MongoDB supports the following search types. Choose the type that matches your query patterns:

| **Search type**  | **Query stages**| **Index type** | **Use for**|
|------------------|-----------------|----------------|------------|
| Full-text search | `$search`, `$searchMeta` | `search`| Relevance-ranked text queries, autocomplete, faceting, and highlighting |
| Vector search    | `$vectorSearch`| `vectorSearch` | Semantic similarity queries using machine learning embeddings|


### Full-text search

Full-text Search lets you search text stored in one or more fields using relevance-based ranking. It supports capabilities such as:

- Keyword and phrase searches
- Boolean operators
- Fuzzy matching
- Wildcard searches
- Field-specific searches
- Relevance scoring

Use cases include:

- Product catalog search
- Documentation search
- Blog and article search
- Customer support knowledge bases


For information about the search architecture and the eventual consistency model, see [Architecture](vector-search-architecture.md).


# Architecture

`mongod` and `mongot` work together to provide full-text and vector search capabilities. While `mongod` continues to store and manage your application data, `mongot` is responsible for building search indexes and executing search queries. The two processes run alongside each other and communicate internally to keep search indexes synchronized with the underlying data.

## Components

| **Component** | **Description** |
|-----------|-------------|
| `Application` | Sends vector search requests using the `$vectorSearch` aggregation stage. |
| `mongod` | Stores application data, manages vector search indexes, forwards vector search requests to `mongot`, retrieves matching documents, and returns the final results. |
| `mongos` | Routes vector search requests to the appropriate shard in sharded deployments. |
| `mongot` | Builds and maintains vector indexes, synchronizes them with data stored in `mongod`, performs nearest-neighbor searches, and returns matching document identifiers with similarity scores. |
| Vector indexes | Specialized indexes maintained by `mongot` to efficiently perform semantic similarity searches over vector embeddings. |

## How vector search works

The following steps describe how a vector search request is processed:
{.power-number}

1. The application converts the search query into a vector embedding using an embedding model.
2. The application submits the vector search request to `mongod` or `mongos` using the `$vectorSearch` aggregation stage.
3. `mongod` forwards the vector search portion of the request to `mongot`.
4. `mongot` searches the vector index for the nearest matching embeddings. The vector indexes are continuously synchronized with the data stored in `mongod`, ensuring that search results reflect the latest changes.
5. `mongot` returns the matching document identifiers and similarity scores to `mongod`.
6. `mongod` retrieves the corresponding documents from the database, applies any remaining aggregation pipeline stages, and returns the final results to the application.

## Data synchronization
`mongot` does not store the primary copy of your data. Instead, it maintains vector indexes that are synchronized with the collections stored in `mongod`. Whenever documents are inserted, updated, or deleted, the corresponding vector indexes are updated automatically. This synchronization ensures that vector search queries operate on current data without requiring manual index maintenance.



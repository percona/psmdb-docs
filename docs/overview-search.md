# Search capabilities in Percona Server for MongoDB

Percona Server for MongoDB supports **Full-text Search** and **Vector Search** through `mongot`, a dedicated search service that works alongside `mongod`. Together, they enable applications to perform keyword-based, semantic, and AI-powered searches without moving data to an external search platform.

You can create search indexes on your collections and use aggregation pipeline stages such as `$search`, `$searchMeta`, and vector similarity queries to retrieve relevant results.

`mongot` is included with Percona Server for MongoDB and is available in binary distributions and installation packages.
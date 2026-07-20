# Create a Search Index

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

The following code shows how to create a Multiple Search indexes:

## Field mappings

A search index definition specifies which fields to index and how to index them. You can choose between two mapping strategies:

- [Dynamic mapping :octicons-link-external-16:](https://www.mongodb.com/docs/search/index/define-field-mappings/#dynamic-mappings){:target="_blank"} indexes all fields of supported types automatically, including fields added to documents later. Fields can be indexed based on the default set of types or by configuring a `typeSet`.

- [Static mapping :octicons-link-external-16:](https://www.mongodb.com/docs/search/index/define-field-mappings/#static-mappings){:target="_blank"} indexes only the fields you explicitly define. To use static mappings to configure index options for only some fields, set `mappings.dynamic` to false and specify the field name, [data type :octicons-link-external-16:](https://www.mongodb.com/docs/search/index/define-field-mappings/#mongodb-search-field-types){:target="_blank"}, and other configuration options for each field that you want to index. You can specify the fields in any order.


[Create a search index :material-arrow-right:](../create-search-index.md){.md-button}
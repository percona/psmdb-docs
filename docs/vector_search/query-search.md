# Query with $search

The `$search` aggregation stage performs full-text search on fields covered by a search index. It returns documents ordered by relevance, with the most relevant document returned first.

## Before you begin

- `mongot` is running and connected to your Percona Search for MongoDB deployment.
- A search index exists for the collection.
- The index includes the fields you want to search.

## Syntax for $search

```javascript
db.<collection>.aggregate([
  {
    $search: {
      index: "<index-name>",
      <operator>: {
        <operator-options>
      }
    }
  }
])
```

The `$search `stage accepts the following primary fields:

| Field| Required | Description|
|------| ---------|-------------|
| `index`        | No       | Name of the search index. If omitted, `$search` uses the index named `default`.                     |
| `<operator>`   | Yes      | Operator that defines the search criteria, such as `text`, `phrase`, `autocomplete`, or `compound`. |
| `highlight`| No | Returns matching terms in their original context. |
| `count` | No | Returns the number of matching documents.|
| `sort`| No| Specifies the order of the results.|
| `scoreDetails` | No | Returns details about how the relevance score was calculated. |

## Search a text field

The following example searches the `title` field in the `movies` collection for documents containing the term database:

```javascript
  {
    $search: {
      index: "movies_search",
      text: {
        query: "database",
        path: "title"
      }
    }
  }
])
```

The `text` operator analyzes the query text and compares it with the indexed values in the specified field.

To search more than one field, provide an array of field names:

```javascript
  {
    $search: {
      index: "movies_search",
      text: {
        query: "database",
        path: ["title", "description"]
      }
    }
  }
])
```

## Return the relevance score

Each result has a relevance score that indicates how closely it matches the query. Add a `$project` stage and the `searchScore` metadata expression to include the score in the output:

```javascript
db.movies.aggregate([
  {
    $search: {
      index: "movies_search",
      text: {
        query: "database",
        path: ["title", "description"]
      }
    }
  },
  {
    $project: {
      _id: 0,
      title: 1,
      description: 1,
      score: {
        $meta: "searchScore"
      }
    }
  },
  {
    $limit: 10
  }
])
```

This query returns the ten most relevant documents and includes the relevance score for each result.

For the complete syntax and available options, see the [upstream MongoDB documentation :octicons-link-external-16:](https://www.mongodb.com/docs/search/query/aggregation-stages/search/){:target="_blank"} for the $search aggregation stage.
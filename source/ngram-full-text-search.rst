.. full-text-search.ngram:

================================================================================
|ngram| Full Text Search
================================================================================

The |ngram| full text search is useful for searching text for a specific string
of characters in a field of a collection. To use |ngram|, create a text index on
a collection setting the ``default_language`` parameter to **ngram**:

.. code-block:: guess

   mongo > db.collection.createIndex({name:"text"}, {default_language: "ngram"})

The |ngram| search engine uses the following token delimiter characters that are not
used do not count as word characters in human languages:

- Horizontal tab
- Vertical tab
- Line feed
- Carriage return
- Space

This feature is useful for such languages as Korean, Chinese, or Japanese. It
may also turn out to be more convenient when working with the text where symbols
like dash('-'), underscore('_'), or slash("/") are not token delimiters.

The |ngram| full text search is slower than normal MongoDB full text search.


.. seealso::

   |MongoDB| documentation:
      - `Text search <https://docs.mongodb.com/manual/text-search/>`_
      - `Text indexes <https://docs.mongodb.com/manual/core/index-text/#index-feature-text>`_
      - `$text operator <https://docs.mongodb.com/manual/reference/operator/query/text/#op._S_text>`_
   More information about the implementation:
      - https://github.com/percona/percona-server-mongodb/blob/v4.0/src/mongo/db/fts/ngram-tokenizer.md
      
.. |ngram| replace:: *ngram*

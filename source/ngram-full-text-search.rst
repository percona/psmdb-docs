.. full-text-search.ngram:

================================================================================
Additional text search algorithm - *ngram* 
================================================================================

The `ngram <https://en.wikipedia.org/wiki/N-gram>`_ text search algorithm is useful for searching text for a specific string
of characters in a field of a collection. This feature can be used to find exact sub-string matches, which provides an alternative to parsing text from languages other than the list of European languages already supported by MongoDB Community's full text search engine. It
may also turn out to be more convenient when working with the text where symbols
like dash('-'), underscore('_'), or slash("/") are not token delimiters.

Unlike MongoDB full text search engine, *ngram* search algorithm uses only the following token delimiter
characters that do not count as word characters in human languages:

- Horizontal tab
- Vertical tab
- Line feed
- Carriage return
- Space

The *ngram* text search is slower than MongoDB full text search.

Usage
=========

To use *ngram*, create a text index on
a collection setting the ``default_language`` parameter to **ngram**:

.. code-block:: javascript

   mongo > db.collection.createIndex({name:"text"}, {default_language: "ngram"})

*ngram* search algorithm treats special characters like individual terms. Therefore, you don't have to enclose the search string in escaped double quotes (``\"``) to query the text index. For example, to search for documents that contain the date ``2021-02-12``, specify the following:

.. code-block:: javascript

   mongo > db.collection.find({ $text: { $search: "2021-02-12" } })

However, both *ngram* and MongoDB full text search engine treat words with the hyphen-minus ``-`` sign  in front of them as negated (e.g. "-coffee")  and exclude such words from the search results. 

.. seealso::

   |MongoDB| documentation:
      - `Text search <https://docs.mongodb.com/manual/text-search/>`_
      - `Text indexes <https://docs.mongodb.com/manual/core/index-text/#index-feature-text>`_
      - `$text operator <https://docs.mongodb.com/manual/reference/operator/query/text/#op._S_text>`_
   More information about ngram implementation:
      - https://github.com/percona/percona-server-mongodb/blob/v4.0/src/mongo/db/fts/ngram-tokenizer.md
      


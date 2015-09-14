==========
 Glossary
==========

.. glossary::

  ACID
    Set of properties that guarantee database transactions are 
    processed reliably. Stands for :term:`Atomicity`,
    :term:`Consistency`, :term:`Isolation`, :term:`Durability`.

  Atomicity
    Atomicity means that database operations are applied following a
    "all or nothing" rule. A transaction is either fully applied or not
    at all.

  Consistency
    Consistency means that each transaction that modifies the database
    takes it from one consistent state to another.

  Durability
    Once a transaction is committed, it will remain so.

  Foreign Key
    A referential constraint between two tables. Example: A purchase
    order in the purchase_orders table must have been made by a customer
    that exists in the customers table.

  Isolation
    The Isolation requirement means that no transaction can interfere
    with another.

  Jenkins
    `Jenkins <http://www.jenkins-ci.org>`_ is a continuous integration
    system that we use to help ensure the continued quality of the
    software we produce. It helps us achieve the aims of:

     * no failed tests in trunk on any platform,
     * aid developers in ensuring merge requests build and test on all platforms,
     * no known performance regressions (without a damn good explanation).


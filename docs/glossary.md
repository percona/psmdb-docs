# Glossary

## ACID
    
Set of properties that guarantee database transactions are processed reliably. Stands for [Atomicity](#atomicity), [Consistency](#consistency), [Isolation](#isolation), [Durability](#durability).

## Atomicity

Atomicity means that database operations are applied following a "all or nothing" rule. A transaction is either fully applied or not at all.

## Consistency

Consistency means that each transaction that modifies the database takes it from one consistent state to another.

## Durability

Once a transaction is committed, it will remain so.

## Foreign Key

A referential constraint between two tables. Example: A purchase order in the purchase_orders table must have been made by a customer that exists in the customers table.

## Isolation
    
The Isolation requirement means that no transaction can interfere with another.

## Jenkins

[Jenkins](http://www.jenkins-ci.org) is a continuous integration system that we use to help ensure the continued quality of the software we produce. It helps us achieve the aims of:

* no failed tests in trunk on any platform,
* aid developers in ensuring merge requests build and test on all platforms,
* no known performance regressions (without a damn good explanation).

## Kerberos

Kerberos is an authentication protocol for client/server authentication without sending the passwords over an insecure network. Kerberos uses symmetric encryption in the form of tickets - small pieces of encrypted data used for authentication. A ticket is issued for the client and validated by the server.  

## Rolling restart

A rolling restart (rolling upgrade) is shutting down and upgrading nodes one by one. The whole cluster remains operational. There is no interruption to clients assuming the elections are short and all writes directed to the old primary use the retryWrite mechanism.
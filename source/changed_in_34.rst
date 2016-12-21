.. _changed_in_34:

=========================================
Changed in Percona Server for MongoDB 3.4
=========================================

The following features of |PSMDB| 3.2 are no longer available in version 3.4:

* *PerconaFT* was removed from |PSMDB| 3.4.
  It was deprecated in |PSMDB| 3.2
  due to conflicts with the locking model in MongoDB.
  For more information, see `this blog post
  <https://www.percona.com/blog/2016/06/16/mongorocks-deprecating-perconaft-mongodb-optimistic-locking/>`_.

  We recommend using MongoRocks_ for write-based workloads.

* *Percona TokuBackup* was removed from |PSMDB| 3.4.
  It was deprecated in |PSMDB| 3.2 due to deprecation of PerconaFT.
  As an alternative, you can use :ref:`hot-backup` for the default WiredTiger_
  and alternative MongoRocks_ storage engines.


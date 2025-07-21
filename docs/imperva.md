# Integration with Imperva Data Security Fabric (DSF) 

!!! note "Version added: [8.0.8-3](release_notes/8.0.8-3.md)"

Integrating [Percona Server for MongoDB Pro](psmdb-pro.md) with [Imperva Data Security Fabric (DSF) :octicons-link-external-16:](https://www.thalestct.com/imperva-data-security-fabric/) by Thales enables enterprise-grade auditing, monitoring, and behavioral analytics for sensitive data activity.

Data Security Fabric (DSF) includes three core components:

* DSF Hub (Sonar): is the central platform that ingests, stores, and normalizes audit data from your MongoDB instances.
* Database Activity Monitoring (DAM): Enforces policies for access control and behavioral inspection, enabling real-time detection of unauthorized activity or misuse.
* Data Risk Analytics (DRA): Applies machine learning and behavior modeling to uncover anomalies, prioritize risk, and provide actionable intelligence for security and compliance teams.

Together, these components provide continuous compliance coverage, rapid breach detection, and scalable visibility across hybrid or cloud-hosted MongoDB deployments.

## How it works

Percona Server from MongoDB native audit logging that captures detailed user actions, administrative events, and query operations. These audit logs are ingested into the Imperva DSF Hub, where they are normalized, stored securely, and analyzed. Administrators can define policies, monitor activity, and trigger alerts based on access behavior. 

Audit logs can be enriched with the debug symbols available in Percona Server for MongoDB Pro. This enrichment enhances event parsing, improves context accuracy, and supports deep operational visibility.

!!! note 

    Non Percona Customers can include debug symbols by [building Percona Server for MongoDB from the source code](install/source.md).


This integration provides the following benefits:

* Deep visibility into MongoDB operations enhanced with debug symbols. 
* Automated compliance via audit-ready reporting
* Behavioral threat detection tailored to MongoDB workloads
* Scalable protection across on-premises, hybrid, and cloud deployments

## Version compatibility

* Percona Server for MongoDB Pro starting with versions 6.0.21-18, 7.0.18-11, 8.0.8-3
* Imperva DSF version 14.9 or later

## Configuration

For setup instructions, consult the [Percona Server for MongoDB Onboarding Steps
 :octicons-link-external-16:](https://docs-cybersec.thalesgroup.com/bundle/onboarding-databases-to-sonar-reference-guide/page/Percona-Server-for-MongoDB-Onboarding-Steps_48368154.html).






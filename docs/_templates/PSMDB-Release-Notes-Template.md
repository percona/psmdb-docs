---
title: Percona Server for MongoDB release notes version <PSMDB_VERSION>
summary: Get to know all improvements, new features, and bug and security vulnerability fixes in the release.
authors:
  - Rasika Chivate
version: <PSMDB_VERSION>
---

<!--
AUTHORING GUIDANCE: Remove these comments before publication.

Required inputs:
- PSMDB version, for example 8.3.11-3.
- Exact upstream MongoDB versions included in this release.
- Official upstream release notes and changelog URLs, including verified anchors.
- Percona Jira tickets for release-specific improvements and bug fixes.
- Verified upstream CVE records, MongoDB Jira mappings, and severity ratings.
- Release status, existing release-date macro, and packaged tool versions.

Replace all <PLACEHOLDERS>. Preserve MkDocs macros, link attributes, and
admonition indentation. Replace <RELEASE_DATE_MACRO> with the complete existing
project macro, including braces, for example {{date.8_3_11}}. Do not infer a
PSMDB release date from an upstream release date.

Keep only applicable sections. Repeat entry patterns as needed and remove
empty headings. Retain the Technical Preview warning only for preview releases.
Verify all versions, ticket IDs, CVE mappings, URLs, and impacts. Do not carry
facts from the reference release into a new release without verification.

Security entries:
- Verify that each CVE was fixed in one of the explicitly included releases.
- Use MongoDB release notes, advisories, Jira, and MongoDB-authored CVE records.
- State the CVSS version used and apply it consistently across entries.
- Group entries as Critical, High, Medium, and Low. Remove empty groups.
- Deduplicate CVEs and Jira tickets. Combine multiple CVEs only when their
  relationship to the same Jira ticket is verified.
- Describe the component, trigger, required access, and user impact when known.
- Do not infer remote code execution, data loss, or PSMDB-specific applicability.
- Use vulnerability counts only if checked against the final entries.

Writing: Use concise, natural language. Explain user impact. Format commands,
parameters, process names, and roles as code. Avoid em dashes and en dashes.
Use “Fixed an issue...” for bugs; describe improvements as new capabilities
or changes. Follow the approved security-entry wording for the release.
-->

# Percona Server for MongoDB {{ page.meta.version }} (<RELEASE_DATE_MACRO>)

[Installation](../install/index.md){.md-button}
[Upgrade from MongoDB Community](../install/upgrade-from-mongodb.md){.md-button}

<!-- Optional: Keep this warning only for a technical preview release. -->
!!! warning "Technical Preview"
    Percona Server for MongoDB {{ page.meta.version }} is available as a technical preview.

    We recommend that early adopters use this release for testing purposes only and not in production environments.

We are pleased to announce **Percona Server for MongoDB {{ page.meta.version }}**, the drop-in replacement for MongoDB Community Edition. Percona Server for MongoDB supports MongoDB Community protocols and drivers and enhances it with [enterprise-grade features for free](../comparison.md), helping you meet your organization's requirements for high availability, reliability, and data security.

Percona Server for MongoDB **{{ page.meta.version }}** includes the improvements and bug fixes of:

<!-- Include one link for each upstream release explicitly covered. Remove the second link if only one release applies. -->
- [MongoDB <UPSTREAM_VERSION> Community Edition :octicons-link-external-16:](<UPSTREAM_RELEASE_NOTES_URL>){:target="_blank"} and [MongoDB <ADDITIONAL_UPSTREAM_VERSION> Community Edition :octicons-link-external-16:](<ADDITIONAL_UPSTREAM_RELEASE_NOTES_URL>){:target="_blank"}.

- Supports protocols and drivers of MongoDB Community **<UPSTREAM_VERSION>**.

## Upgrade recommendation

<!-- Base the recommendation on verified changes and release status. For a preview release, address existing preview users without implying production readiness. Remove this section if no recommendation applies. -->
This release fixes multiple security vulnerabilities inherited from upstream MongoDB. We strongly recommend **upgrading to version {{ page.meta.version }}** as soon as possible.

## Changelog

### Improvement

<!-- Repeat for each verified improvement. Use “Improvements” for multiple entries. -->
- [PSMDB-<ISSUE_ID>](https://perconadev.atlassian.net/browse/PSMDB-<ISSUE_ID>): <CHANGE_AND_USER_BENEFIT>.

<!-- Optional dependency-update entry. Include the CVE sentence only when verified. -->
- [PSMDB-<ISSUE_ID>](https://perconadev.atlassian.net/browse/PSMDB-<ISSUE_ID>): Upgraded `<DEPENDENCY_NAME>` to version [<DEPENDENCY_VERSION> :octicons-link-external-16:](<DEPENDENCY_RELEASE_NOTES_URL>){:target="_blank"}. This version includes a fix for [CVE-<YEAR>-<ID> :octicons-link-external-16:](https://www.cve.org/CVERecord?id=CVE-<YEAR>-<ID>){:target="_blank"}.

### Bugs fixed

- [PSMDB-<ISSUE_ID>](https://perconadev.atlassian.net/browse/PSMDB-<ISSUE_ID>): Fixed an issue in <COMPONENT_OR_FEATURE> that occurred when <TRIGGER_OR_CONDITION>. This could <USER_IMPACT>.

## Security fixes from upstream MongoDB

The severity categories below follow the upstream [CVSS scores :octicons-link-external-16:](https://nvd.nist.gov/vuln-metrics/cvss){:target="_blank"}, using CVSS <CVSS_VERSION>.

### Critical severity

- [SERVER-<ISSUE_ID> :octicons-link-external-16:](https://jira.mongodb.org/browse/SERVER-<ISSUE_ID>){:target="_blank"} ([CVE-<YEAR>-<ID> :octicons-link-external-16:](https://www.cve.org/CVERecord?id=CVE-<YEAR>-<ID>){:target="_blank"}): Fixed an issue in <COMPONENT_OR_FEATURE> where <TRIGGER_AND_REQUIRED_ACCESS>. This could <SECURITY_IMPACT>.

### High severity

- [SERVER-<ISSUE_ID> :octicons-link-external-16:](https://jira.mongodb.org/browse/SERVER-<ISSUE_ID>){:target="_blank"} ([CVE-<YEAR>-<ID> :octicons-link-external-16:](https://www.cve.org/CVERecord?id=CVE-<YEAR>-<ID>){:target="_blank"}): Fixed an issue in <COMPONENT_OR_FEATURE> where <TRIGGER_AND_REQUIRED_ACCESS>. This could <SECURITY_IMPACT>.

### Medium severity

- [SERVER-<ISSUE_ID> :octicons-link-external-16:](https://jira.mongodb.org/browse/SERVER-<ISSUE_ID>){:target="_blank"} ([CVE-<YEAR>-<ID> :octicons-link-external-16:](https://www.cve.org/CVERecord?id=CVE-<YEAR>-<ID>){:target="_blank"}): Fixed an issue in <COMPONENT_OR_FEATURE> where <TRIGGER_AND_REQUIRED_ACCESS>. This could <SECURITY_IMPACT>.

### Low severity

- [SERVER-<ISSUE_ID> :octicons-link-external-16:](https://jira.mongodb.org/browse/SERVER-<ISSUE_ID>){:target="_blank"} ([CVE-<YEAR>-<ID> :octicons-link-external-16:](https://www.cve.org/CVERecord?id=CVE-<YEAR>-<ID>){:target="_blank"}): Fixed an issue in <COMPONENT_OR_FEATURE> where <TRIGGER_AND_REQUIRED_ACCESS>. This could <SECURITY_IMPACT>.

For the complete upstream changelog, see [MongoDB <UPSTREAM_VERSION> Community Edition :octicons-link-external-16:](<UPSTREAM_CHANGELOG_URL>){:target="_blank"}.

## Tools packaged with this release

<!-- Use the packaged versions, not the latest upstream versions. Retain project tool-version macros when supplied. -->
| **Tool** | **Base version** | **Release notes** |
|---|---|---|
| MongoDB Shell (`mongosh`) | <MONGOSH_VERSION> | [upstream release notes :octicons-link-external-16:](<MONGOSH_RELEASE_NOTES_URL>){:target="_blank"} |
| Mongo Tools | <MONGO_TOOLS_VERSION> | [upstream release notes :octicons-link-external-16:](<MONGO_TOOLS_RELEASE_NOTES_URL>){:target="_blank"} |

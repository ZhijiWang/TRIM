# Private packet handling protocol

Status: protocol draft for gate preparation. This document does not authorize private-packet inspection, human coding, model execution, provider transmission, or public redistribution.

Overall execution status remains: `BLOCKED_PENDING_RIGHTS_PRIVATE_PACKETS_MODEL_ACCOUNT_RUNTIME_SETTINGS_PRICING_AND_FINAL_EXECUTION_AUTHORIZATION`.

## Access control

Private packets may be accessed only after a documented authorization reference exists for the specific access event. Authorized roles may include a rights reviewer, private-packet auditor, principal investigator, human coder, or execution harness, but only for the role-specific reason recorded in an access log.

Private packets may reside only in an approved controlled local or institutional storage location. They must not be committed to this repository, copied into public pull requests, pasted into issue or PR comments, included in tests, printed, exported, or transmitted to a model provider unless the relevant rights, private-packet, provider, runtime, pricing, and final-authorization gates have all passed.

Before access, the reviewer must confirm that the case ID is selected in PR #18 metadata, the current packet hash is known from controlled storage, the rights status is recorded, and the access event can be logged against `schemas/private_packet_access_log.schema.json`.

## Audit trail

Every private-packet access event must record:

- access event ID;
- packet ID and case ID;
- actor ID and actor role;
- timestamp;
- packet hash before access;
- packet hash after access if normalization or transformation occurs;
- reason for access;
- whether text was viewed;
- whether text was transformed;
- whether text was exported;
- whether text was transmitted outside the local environment;
- destination if exported or transmitted;
- rights status at access;
- authorization reference;
- record hash computed after the event record is complete.

No access log may include raw source text, copyrighted excerpts, controlled packet text, or private notes that reproduce source text.

## Redaction and public artifact rule

Public artifacts may contain metadata, rights statuses, documentary references, case IDs, and non-content hashes only when already approved for public metadata. Public artifacts must not contain private packet text, controlled packet text, copyrighted excerpts, source-packet fixtures, or logs that quote packet content.

## Coding precondition

Human coding may not start until rights status is resolved for every selected packet, this access protocol is approved, packet hashes are verified in controlled storage, the human coding environment is documented, the record-locking process is documented, and final execution authorization is explicitly granted.

## Model execution precondition

Model execution may not start until rights status is resolved, private packet transmission to the provider is permitted, provider data handling is reviewed, provider/model/account/runtime/pricing gates pass, exact request preservation is active, and final execution authorization is explicitly granted.

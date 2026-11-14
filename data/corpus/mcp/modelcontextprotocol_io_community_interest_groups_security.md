<!-- source: https://modelcontextprotocol.io/community/interest-groups/security -->
## Group Type

## Mission Statement

## Scope

### In Scope
- Triage and routing : receiving security topics raised on Discord or GitHub and handing them
to the owning group (Auth IG, Transports WG, Registry WG, Tool Annotations IG, SDK maintainers)
- Threat modeling : developing and maintaining a shared, layered view of MCP attack surfaces
spanning admission and identity, caller governance, runtime behavior, interception and enforcement,
and auditability, to give individual proposals a common frame of reference
- Server identity, attestation, and admission : requirements for establishing that a server is
what it claims to be before a client dispatches to it, including signed assertions, trust roots,
and the boundary between protocol-level and registry-level verification
- Supply chain and provenance : integrity of locally executed server binaries and packages
(typosquatting, unpinned dependencies, unsigned artifacts) and how clients can verify what they
spawn
- Runtime drift and post-admission change : treatment of tool, schema, or behavior changes after
a server has been approved, and whether such changes are versioning, re-approval, or security
events
- Auditability and observability : requirements for tamper-evident records of what a tool call
did and under what authority, for compliance and incident review
- Transport-adjacent security : secrets handling, process isolation, and unauthenticated surface
area for stdio and other non-HTTP transports where the HTTP authorization specification does not
apply
- Security Best Practices documentation : authoring and reviewing entries in the Security Best Practices guidance, including
liaising with external bodies such as OWASP GenAI and CoSAI on MCP-specific content
- Vulnerability disclosure routing : providing a known point of contact for reporters who have
filed a private security advisory against an MCP repository and need help reaching the right
maintainer

### Out of Scope
- Authorization protocol mechanics : OAuth flows, scopes, client registration, and token handling
belong to the Authorization IG and its spawned Working Groups
- Transport wire security : TLS, mTLS, and certificate handling belong to the Transports WG
- Tool annotation design : the annotation model itself belongs to the Tool Annotations IG . This group provides security
requirements as input
- Registry service operation : running and securing the hosted Registry service belongs to the Registry WG . This group provides threat input on provenance and
publishing
- Product-specific hardening guides : step-by-step configuration for individual host applications
or cloud platforms is documentation for those products rather than protocol work
- Competitively sensitive or non-public business information , per the MCP Antitrust Policy

### Related Groups
- Authorization IG : token confusion, audience mismatch, and SSRF in
metadata discovery sit at the boundary between the two groups
- Tool Annotations IG : trust and sensitivity annotations
( SEP-1913 ) span both
groups
- Interceptors WG : interceptors are the primary enforcement
point for runtime security decisions surfaced here
- Server Card WG / Registry WG :
server identity, provenance, and discovery metadata intersect with admission and supply-chain
concerns
- Transports WG : stdio process isolation and unauthenticated method surface
- SDK Maintainers : coordinated handling of SDK security advisories and cross-SDK security
defaults

## Leadership
Facilitator
Den Delimarsky
Anthropic
@localden
Initial
Facilitator
Paul Carleton
Anthropic
@pcarleton
Initial

## Membership
Sam Morrow
GitHub
@SamMorrowDrums
sammorrowdrums
Participant
Ola Hungerford
Nordstrom
@olaservo
olaservo
Participant
Peder Holdgaard Pedersen
Saxo Bank
@PederHP
pederhp
Participant
Stefano Ortolani
Broadcom
@ostefano
ostefano.
Participant

## Operations
Forum call
Monthly
45 min
Triage and routing of topics on the published agenda, WG proposal scoping
Digest
Monthly
n/a
Summary of routed items, open topics, and advisories

## Discussion Topics
—
SDK vulnerability disclosure
In progress
Facilitators
—
Runtime drift: list_changed semantics after approval
Open
—
—
Supply-chain integrity: protocol, registry, or companion standard
Open
—
—
Tool identity across servers
Open
—
—
Capability declarations: hints or contracts (joint with Tool Annotations IG )
Open
—

## Changelog
2026-08-26
Restructured as a routing group, replaced biweekly office hours with a monthly agenda-driven call and digest (core maintainer meeting, discussion #3316 )
2026-06-13
Initial charter
Was this page helpful?

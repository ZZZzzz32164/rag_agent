<!-- source: https://modelcontextprotocol.io/community/interest-groups/financial-services -->
## Group Type

## Mission Statement

## Scope

### In Scope
- Compliance and auditability : requirements for tamper-evident, portable records of what a tool
call did, under what authority, and against which policy, so that MCP interactions can satisfy
regulatory audit and incident-review obligations
- Data lineage and provenance : source attribution, citation, and consent metadata for data
surfaced through MCP, so that downstream consumers can establish where information came from and
on what basis it may be used
- Guardrails and attestation : verification frameworks and cryptographic attestations that let a
regulated institution gain assurance about server identity, tool behavior, and the integrity of
responses before acting on them
- Policy enforcement : declarative policies for tool usage and data handling, and the points at
which they are enforced, so that institutions can encode regulatory and internal-control
constraints as machine-checkable rules
- Finance-specific extensions : developing, maintaining, and gathering implementation experience
on MCP extensions that address the above in the FSIG repository, including reference
implementations and conformance testing
- Interoperability across institutions : common patterns and standards that allow regulated
institutions to interoperate without each reinventing compliance plumbing
- SEP promotion : identifying extensions with applicability beyond financial services and
shepherding them toward the core specification with core-maintainer sponsorship
- Regulatory liaison : translating constraints from regulators and industry bodies into concrete
technical requirements and input for other groups

### Out of Scope
- Competitively sensitive or non-public business information : pricing, costs, margins, customer
lists, market segmentation, and competitive strategy, per the MCP Antitrust Policy
- General security threat modeling : MCP-wide attack-surface analysis belongs to the Security IG . This group provides financial-sector requirements as
input and consumes its threat models
- Authorization protocol mechanics : OAuth flows, scopes, client registration, and token handling
belong to the Authorization IG
- Product-specific compliance guides : step-by-step configuration for an individual host
application, cloud platform, or institution is documentation for that product rather than protocol
work
- Non-technical business discussions : legal interpretation, procurement, and commercial terms

### Related Groups
- Security IG : attestation, auditability, and guardrails are
shared concerns; the FSIG supplies regulated-deployment requirements and consumes the IG’s threat
models
- Authorization IG : identity and access control for sensitive
financial data sit at the boundary between the two groups
- Tool Annotations IG : trust and sensitivity annotations
are directly relevant to financial tool exposure; the FSIG provides requirements as input
- Interceptors WG : interceptors are a primary enforcement point
for the policy and guardrail requirements surfaced here
- Registry WG : server provenance and publishing metadata intersect
with financial supply-chain and admission concerns

## Leadership
Facilitator
Sambhav Kothari
Bloomberg
@sambhav
Initial
Facilitator
Peder Holdgaard Pedersen
Saxo Bank
@PederHP
Initial

## Membership
Xin Fu
Bloomberg
@imfing
TBD
Participant
Kengo Arao
Bloomberg
@KengoA
TBD
Participant
King Yew Choo
True Primary
@kychooo
kychooo
Participant

## Operations
Working Session
Every 2 weeks
60 min
Use-case review, extension and proposal work, SEP scoping

## Discussion Topics
—
Regulatory audit & attestation: portable, verifiable event/claim models
Open
—
—
Data lineage & citation: provenance, consent metadata, source attribution
Open
—
—
Guardrails & security: verification frameworks and cryptographic attestations
Open
—
—
Policy enforcement: declarative policies for tool usage and data handling
Open
—

## Changelog
2026-06-25
Initial charter
Was this page helpful?

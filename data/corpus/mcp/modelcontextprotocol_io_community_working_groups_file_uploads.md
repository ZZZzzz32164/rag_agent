<!-- source: https://modelcontextprotocol.io/community/working-groups/file-uploads -->
## Group Type

## Mission Statement

## Scope

### In Scope
- Specification Work : SEPs defining declarative file input descriptors on tool input schemas and
elicitation request schemas, the wire encoding for file content, and host-side handling
requirements.
- File Downloads (secondary) : How a tool returns a file that is too large for a JSON-RPC message
or that needs authorization to fetch. Upload work takes priority.
- Reference Implementations : SDK types and helpers for FileInputDescriptor , data URI encoding,
and a sample host flow demonstrating picker invocation and value substitution.
- Cross-Cutting Concerns : Coordination with the MCP Apps WG where embedded UI surfaces present
their own file pickers, and with the Security IG on host-side validation requirements.
- Documentation : Specification sections covering file input declaration and a migration guide
for servers currently using ad-hoc base64 instructions.

### Out of Scope
- Server-to-client delivery of small files, which Resources and BlobResourceContents already cover.
- Changes to the transport layer or session model.

### Related Groups
- MCP Apps WG — embedded app UIs may surface their own file pickers; the descriptor format
should be reusable in that context.
- Security IG — host-side validation requirements for user-supplied file content (the SEP
references OWASP ASVS V5 for general upload hygiene).
- Tool Annotations IG — file input descriptors are a form of input-parameter metadata and should
remain consistent with the broader annotation taxonomy.

## Leadership
Lead
Den Delimarsky
Anthropic
@localden
Initial

## Authority & Decision Rights
Meeting logistics & scheduling
WG Leads (autonomous)
Proposal prioritization within WG
WG Leads (autonomous)
SEP triage & closure (in scope)
WG Leads (autonomous, with documented rationale)
Technical design within scope
WG consensus
Spec changes (additive)
WG consensus → Core Maintainer approval
Spec changes (breaking/fundamental)
WG consensus → Core Maintainer approval + wider review
Scope expansion
Core Maintainer approval required
WG Member approval
WG Member sponsors

## Membership
Den Delimarsky
Anthropic
@localden
Lead
Nick Cooper
OpenAI
@nickcoai
WG Member
Olivier Chafik
Anthropic
@ochafik
WG Member

## Operations
Working Session
Biweekly
30 min
Technical discussion, proposal review

## Deliverables & Success Metrics

### Active Work Items
SEP-2356: Declarative file inputs
Draft
End May
@ochafik
TypeScript SDK reference implementation
—
End May
@ochafik
Reference implementation in a second Tier-1 SDK
—
End June
TBD

### Success Criteria
- An accepted SEP defining the file input descriptor and wire encoding.
- Reference implementations in at least two Tier-1 SDKs.
- At least one production host rendering a native file picker from the descriptor.
- Conformance test coverage for the new schema keyword.

## Changelog
2026-04-23
Initial charter
2026-10-21
Add file downloads to scope as a secondary item
Was this page helpful?

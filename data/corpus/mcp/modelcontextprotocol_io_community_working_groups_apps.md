<!-- source: https://modelcontextprotocol.io/community/working-groups/apps -->
## Group Type

## Mission Statement

## Scope

### In Scope
- Specification Work : The MCP Apps extension specification and related SEPs, covering the areas below under the io.modelcontextprotocol/ui namespace.
- App Lifecycle : How apps are declared, initialized, persisted, and torn down, including UI resource declaration and tool metadata.
- App Interaction Model : The interaction protocol between user, app, and host, such as bi-directional messaging, app tools, etc.
- Content Types and Rendering Targets : Support for different content types and methodologies like generative UI, with interoperability with external protocols such as A2UI and AG-UI .
- Security Model : The threat model, sandboxing, security policy, permissions, and auditability of UI-initiated actions.
- SDKs and Reference Implementations : The @modelcontextprotocol/ext-apps SDK, reference host, example servers, and host integration examples.
- Conformance : Compatibility tests, app validation, and the definition of conformance requirements for apps and hosts.
- Cross-Cutting Coordination : App discovery and metadata (with the Registry WG), UI in agentic flows (with the Agents IG), and per-language SDK support (with the SDK WG).
- Documentation : API references, authoring guidance, host integration guidance, starter resources, and examples.

### Out of Scope
- Core protocol ownership : Changes to base MCP semantics, transports, or lifecycle are proposed through the SEP process and owned by the relevant group or Core Maintainers.
- Host-specific product and design decisions : Hosts control their user experience and visual design. The WG standardizes the interoperability and security contract.
- Individual app implementations : Apps built on the extension remain the responsibility of their authors.
- General agent orchestration : Agent loops and sub-agent coordination belong to the Agents IG, and task management belongs to the Tasks and Events WG. This WG covers only the interactive UI surface and its integration points.

### Related Groups
- Agents IG : Interactive UI within agentic flows and task lifecycles.
- Registry WG : App discovery, distribution, and metadata.
- Security IG : Sandboxing, permissions, and review of UI-initiated actions.
- SDK WG : SDK consistency and support outside the TypeScript reference implementation.

## Leadership
Lead
Ido Salomon
MCP-UI
@idosal
Initial
Lead
Liad Yosef
MCP-UI / Ora
@liady
Initial
Lead
Olivier Chafik
Anthropic
@ochafik
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
Ido Salomon
MCP-UI
@idosal
Lead
Liad Yosef
MCP-UI / Ora
@liady
Lead
Olivier Chafik
Anthropic
@ochafik
Lead
Anton Pidkuiko
Anthropic
@antonpk1
WG Member
Max Stoiber
OpenAI
@mstoiber-oai
WG Member
Dominic Farolino
Google
@domfarolino
WG Member

## Operations
Working Session
Tri-weekly (Wednesday, 08:00 Pacific)
60 minutes
Specification review, roadmap discussion, and app/host feedback

## Resources
- Specification and SDK: modelcontextprotocol/ext-apps ( @modelcontextprotocol/ext-apps )
- Foundational proposal: SEP-1865
- Guides: MCP Apps overview and Build an MCP App
- API documentation: apps.extensions.modelcontextprotocol.io
- Work tracking: ext-apps issues and pull requests

## Deliverables & Success Metrics

### Active Work Items
Specification and SDK evolution: protocol alignment, capability negotiation, versioning, and maintenance of @modelcontextprotocol/ext-apps
In Progress
@idosal , @liady , @ochafik
Address view sprawl across tools and servers (reusable and independent views)
In Progress
@mstoiber-oai , @idosal , @liady
Formalize security model and extend sandboxing and permissions
In Progress
@idosal
Experiment with the app tools interaction model (WebMCP approach)
In Progress
@ochafik
Address dynamic resource content and non-HTML hosts
Draft
@liady , @idosal
Conformance and cross-host interoperability: official validator, public platform tests, and compatibility reporting
In Progress
@idosal
Developer experience and ecosystem adoption: reference host, authoring tools, examples, documentation, accessibility, and discovery coordination
Maintained
@idosal

### Success Criteria
- The extension specification, SDK, reference host, and examples are actively maintained, with responsive triage of specification and SDK issues.
- MCP Apps can run unmodified across multiple major hosts.
- Conforming hosts implement the documented sandboxing, permissions, content security policy, and auditability requirements, verified by the conformance suite.
- Breaking changes are rare, documented, and preceded by an appropriate deprecation and migration path.
- MCP Apps is the standard UI layer of the agentic web.

## Changelog
2025-11-21
SEP-1865 proposed, unifying the MCP-UI and OpenAI Apps SDK approaches
2025-12-17
First MCP Apps Working Group meeting
2026-01-26
Initial stable MCP Apps extension specification published
2026-01-28
SEP-1865 marked Final
2026-05-21
Initial charter
Was this page helpful?

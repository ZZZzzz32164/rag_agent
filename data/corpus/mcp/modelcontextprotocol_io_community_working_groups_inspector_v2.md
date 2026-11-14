<!-- source: https://modelcontextprotocol.io/community/working-groups/inspector-v2 -->
## Group Type

## Mission Statement

## Scope

### In Scope
- The modelcontextprotocol/inspector repository, including:
- Inspector Core — a new shared-code architecture that provides common MCP and protocol interfaces for all Inspector front-ends.
- Web Inspector UI — browser-based inspector built on Mantine and TypeScript.
- CLI Inspector — command-line interface sharing Inspector Core.
- TUI Inspector — terminal UI sharing Inspector Core.
- Testing apparatus — shared test harnesses, fixtures, and integration tests across all Inspector surfaces.
- Deprecation and migration of the existing Inspector on main to a v1.x maintenance branch.
- Adoption of MCP TypeScript SDK V2 inside Inspector Core once available.

### Out of Scope
- The core MCP specification.
- MCP SDK maintenance (TypeScript, Python, or any other language SDK).
- MCP server implementations.

### Related Groups
- SDK WG — Inspector Core consumes the TypeScript SDK; coordination required for SDK V2 adoption.
- MCP Apps WG — shared surface area around client/app ergonomics and inspection workflows.
- Authorization IG — authentication flows exercised by Inspector when connecting to protected servers.
- Registry WG — discovery and metadata surfaces that Inspector presents to users.

## Leadership
WG Lead
Cliff Hall
Futurescale
@cliffhall
Ongoing
WG Lead
Ola Hungerford
Nordstrom
@olaservo
Ongoing
WG Lead
Bob Dickinson
TeamSpark.ai
@BobDickinson
Ongoing

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
Cliff Hall
Futurescale
@cliffhall
seaofarrows
Maintainer
Ola Hungerford
Nordstrom
@olaservo
olaservo
Maintainer
Bob Dickinson
TeamSpark.ai
@BobDickinson
rddthree
Maintainer
Tobin South
Anthropic
@tobinsouth
tobinsouth
Member

## Operations
Working Session
Weekly, Wednesdays 11:00 America/New_York
60 minutes
Technical discussion, proposal review
- Primary channel: #inspector-v2-wg on the MCP Discord.
- Async discussion: GitHub Discussions in modelcontextprotocol/inspector .
- Quarterly updates: posted to the WG’s GitHub Discussions category.

## Deliverables & Success Metrics

### Active Work Items
Web Inspector UI (Mantine / TypeScript) — dumb components with real MCP/Core interfaces
In Progress
Cliff Hall, Ola Hungerford
Inspector Core shared-code architecture
In Progress
Bob Dickinson
CLI Inspector and TUI Inspector
In Progress
Bob Dickinson
Migration of existing Inspector on main to v1.x maintenance branch
Planning
WG Leads
Testing apparatus across Core, Web, CLI, and TUI
Planning
WG Leads
Inspector Core adoption of MCP TypeScript SDK V2
Blocked (gated by TS SDK WG)
Bob Dickinson

### Success Criteria
- End of Q1 — Web UI complete with “dumb” components wired to real MCP/Inspector Core interfaces.
- End of Q1 — Inspector Core architecture finalized.
- End of Q2 — Inspector Core merged to v2/main and working end-to-end with the Web UI.
- End of Q2 — CLI and TUI Inspectors merged to v2/main and working end-to-end with Inspector Core.
- End of Q2 — Existing Inspector on main moved to the v1.x branch and officially deprecated.
- End of Q2 — New Inspector family (Web, CLI, TUI) published and generally available.
- End of Q3 — Inspector Core running on MCP TypeScript SDK V2 (gated by the TypeScript SDK WG’s delivery schedule).

## Changelog
2026-04-11
Initial charter adopted for SEP-2149 compliance.
Cliff Hall (Co-Lead)
Was this page helpful?

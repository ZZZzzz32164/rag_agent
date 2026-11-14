<!-- source: https://modelcontextprotocol.io/community/interest-groups/auth -->
## Group Type

## Mission Statement

## Scope

### In Scope
- Deployment experience reports : how implementers have integrated the current authorization spec (OAuth 2.1, RFC 9728 Protected Resource Metadata, RFC 7591 Dynamic Client Registration, Client ID Metadata Documents) with real authorization servers, and where it falls short
- Extension interoperability reports : results of pairing independent implementations of the ext-auth extensions end to end (for example IdP, client, and authorization server through the Enterprise-Managed Authorization ID-JAG exchange), including IdP capability gaps, workarounds, and conformance scenario input
- Enterprise identity integration : requirements and friction points when connecting MCP servers to enterprise IdPs (Okta, Entra ID, Ping, Keycloak, etc.), including SSO, tenant isolation, and admin consent flows
- Delegated and agentic access : use cases for on-behalf-of token exchange, downstream resource access, audience restriction, and consent when an MCP client acts through chains of agents or tools
- Scope and permission granularity : whether and how MCP servers should advertise fine-grained scopes (per-tool, per-resource) and how clients should request and present them, and authorization granularity beyond scope strings (Rich Authorization Requests, structured denials, remediation hints)
- Credentials for non-HTTP transports : patterns for stdio, WebSocket, and future transports where the HTTP authorization spec does not directly apply
- Client identity and registration : operator experience with Dynamic Client Registration, Client ID Metadata Documents, software statements, and pre-registered clients
- Threat modelling input : cataloguing authorization-related attack surfaces (token confusion, confused-deputy, audience mismatch, redirect handling) to inform Security Best Practices documentation
- SEP and draft feedback : authorization-related SEPs, ext-auth drafts, reference implementations, and demos are presented on the call and in #auth-ig threads for feedback before and during the SEP process ; the IG’s rough consensus is recorded in meeting notes for sponsors and Core Maintainers to draw on
- Problem statements and requirements : use-case catalogues and recommendations shared in #auth-ig threads and on SEP pull requests for consumption by SEP authors

### Out of Scope
- Accepting SEPs or extensions : the IG gives feedback and signals support; sponsorship and acceptance follow the SEP guidelines and remain with Maintainers and Core Maintainers
- Authentication of end users to MCP clients : how a host application authenticates its own users is a host concern, not a protocol concern
- Transport security (TLS, mTLS, certificate handling) : belongs to the Transports WG
- Server identity, provenance, and trust signalling : belongs to the Server Card / Registry efforts
- End-user product configuration walk-throughs : the IG discusses patterns, not step-by-step setup for individual IdP products. Vendor-reported constraints on what an authorization server or IdP can or cannot implement are in scope as deployment experience
- Competitively sensitive or non-public business information , per the MCP Antitrust Policy

### Related Groups
- Security IG : token-audience confusion, issuer validation, and account-linking risks sit at the boundary between the two groups
- Transports WG : authorization is currently specified at the HTTP transport level; changes to transports affect where credentials are carried
- Agents IG : delegated/on-behalf-of access and consent for multi-agent chains overlap heavily with agentic use cases
- Server Card WG / Registry : client and server identity, discovery metadata, and trust establishment intersect with how authorization servers and resource servers are located and verified
- SDK Maintainers : SDKs ship the auth client implementations; IG findings should inform cross-SDK auth ergonomics and defaults

## Leadership
Facilitator
Aaron Parecki
Okta
@aaronpk
Initial
Facilitator
Darin McAdams
Amazon
@D-McAdams
Initial
Facilitator
Paul Carleton
Anthropic
@pcarleton
Initial

## Membership

## Operations
Auth IG Call
Every 2 weeks
45 min
Agenda-driven: problem pitches, SEP and draft progress, demos, deployment reports

### One channel, threads per topic

### Agenda-driven calls
- A facilitator opens an agenda thread in #auth-ig ahead of each call. Anyone may request a slot by replying with the topic, the ask (feedback, decision, awareness), and the time needed.
- Facilitators agree the agenda and hand out time slots before the call.
- If the agenda is thin, the call is cancelled in the thread and the slot is kept for next time.

### From problem to SEP
- Is this a problem worth solving? Is there real deployment demand, and is the gap in the protocol rather than in one product?
- Does it belong here? Is the right home the core specification, an official extension in ext-auth, an unofficial extension, or an upstream standards body?

## Deliverables & Success Metrics

### Consolidated channels
#auth-wg-client-registration
Dynamic Client Registration, Client ID Metadata Documents, software statements, pre-registration
Completed
#auth-ig threads as needed
#auth-wg-mixup-protection
Authorization-server mix-up and token-audience confusion mitigations
Completed
#auth-ig threads as needed
#auth-wg-profiles
Client Credentials, Enterprise-Managed Authorization, DPoP, Workload Identity Federation extensions
Completed
#auth-ig DPoP and Workload Identity Federation threads
#auth-wg-tool-scopes
Per-tool scope advertisement, step-up authorization, client-side scope accumulation
Active
#auth-ig thread
#auth-wg-fine-grained-authz
Rich Authorization Requests ( RFC 9396 ), structured denials, remediation hints
Active
#auth-ig SEP-2643 / fine-grained authorization thread
#auth-wg-improve-devx
Best-practices guidance and tutorials beyond the normative spec
Dormant
#auth-ig threads as needed
#enterprise-managed-auth-ig
EMA extension interoperability (IdP, client, authorization server)
Active
#auth-ig EMA interop thread and deployment-report slots

## Changelog
2026-08-17
Re-charter: single venue and channel for authorization work; agenda-driven calls; SEP feedback in scope; #auth-wg-* channels and the Enterprise-Managed Authorization IG folded in
2026-06-02
Initial charter
Was this page helpful?

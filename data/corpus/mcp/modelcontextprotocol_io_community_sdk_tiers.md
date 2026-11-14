<!-- source: https://modelcontextprotocol.io/community/sdk-tiers -->
## Tier requirements
Conformance Tests
100% pass rate
80% pass rate
No minimum
New Protocol Features
Before new spec version release, timeline agreed per release based on feature complexity
Within 6 months
No timeline commitment
Issue Triage
Within 2 business days
Within a month
No requirement
Critical Bug Resolution
Within 7 days
Within two weeks
No requirement
Stable Release
Required with clear versioning
At least one stable release
Not required
Documentation
Comprehensive with examples for all features
Basic documentation covering core features
No minimum
Dependency Policy
Published update policy
Published update policy
Not required
Roadmap
Published roadmap
Published plan toward Tier 1 or explanation for remaining Tier 2
Not required

## Conformance testing
- Tests for the specification version the SDK targets
- Excluding tests marked as pending or skipped
- Excluding tests for experimental features
- Excluding legacy backward-compatibility tests (unless the SDK claims legacy support)
- Excluding tests labeled disputed in the conformance repository, until the dispute is resolved

## Tier advancement
- Self-assess the SDK against the tier requirements .
- Open an issue in the modelcontextprotocol/modelcontextprotocol repository with the supporting evidence.
- Pass the conformance threshold for the requested tier on the latest stable release.
- Obtain approval from the SDK Working Group.

## Tier relegation
- Tier 1 to Tier 2 : any conformance test fails.
- Tier 2 to Tier 3 : more than 20% of conformance tests fail.

## Issue triage labels

### Type (pick one)
bug
Something isn’t working
enhancement
Request for new feature
question
Further information requested

### Status (pick one)
needs confirmation
Unclear if still relevant
needs repro
Insufficient information to reproduce
ready for work
Has enough information to start
good first issue
Good for newcomers
help wanted
Contributions welcome from those familiar with codebase

### Priority (only if actionable)
P0
Critical: core functionality failures or high-severity security
P1
Significant bug affecting many users
P2
Moderate issues, valuable feature requests
P3
Nice to haves, rare edge cases
- A security vulnerability with a CVSS score of 7.0 or higher (High or Critical severity)
- A core functionality failure that prevents basic MCP operations: connection establishment, message exchange, or use of the core primitives (tools, resources, prompts)
Was this page helpful?

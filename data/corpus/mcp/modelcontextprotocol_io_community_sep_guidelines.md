<!-- source: https://modelcontextprotocol.io/community/sep-guidelines -->
## When you need a SEP
- A new, changed or removed protocol feature or method (a new RPC method such as tools/execute , a new capability negotiation field, a change to a transport)
- Any change that is not backward compatible
- A change to message formats or schema structure
- An interoperability convention supported outside the core specification
- A governance or process change
- Anything controversial or with several plausible designs, such as a change to how authorization works

## SEP types
- Standards Track: a new protocol feature or implementation, or an interoperability standard supported outside the core specification.
- Informational: a design issue or guidance for the community, with no new feature.
- Process: a process surrounding MCP, or a change to one.
- Extensions Track: a protocol extension. It receives the same review and acceptance as Standards Track. An accepted Extensions Track SEP moves the extension to Beta, and a second one moves it to Stable (see Extension Lifecycle for the stages).

## Before you write
- Check whether the idea fits the current focus on the roadmap . SEPs outside its priority areas face a longer queue and a higher bar (see SEP Prioritization ).
- Bring the idea to the working group that covers the area, in its Discord channel or at a meeting (see Joining a group ). An interest group can help frame the problem first, and a working group sponsors the SEP.
- Reach consensus in the working group, then draft a SEP that the group wants to sponsor . Read the design principles , try the idea as an extension first where its shape allows, and build a prototype that meets the Prototype Requirements .
- The working group brings the SEP to the Core Maintainers for review through the Workflow .

## Workflow
- Copy seps/TEMPLATE.md to seps/0000-<slug>.md and fill it in.
- Open a pull request against the specification repository , titled sep: <description> as in sep: propose task cancellation , following the pull request title guidelines . Authors who are not members of the modelcontextprotocol GitHub organization ask the working group’s leads or the sponsor to open the pull request and name them as the author.
- The SEP number is the PR number. Rename the file (PR #1850 becomes seps/1850-<slug>.md ), update the header, and run npm run generate:seps , or the check:seps CI job fails. Rename the pull request to sep(SEP-1850): <description> ; a follow-up commit is enough, with no amend or force-push. Later pull requests about this SEP keep SEP-1850 as their scope and link to it in the description.
- Until a working group has agreed to sponsor the SEP, it stays a draft pull request. A draft pull request is for developing a proposal in the open. It is not yet in the SEP process, the Status header in the SEP stays unset, and the wg-support-needed label marks it.
- Once a working group has agreed to sponsor the SEP, the pull request is marked ready for review. The Sponsor header names the person who acts on the sponsoring group’s behalf, and that person sets draft . Review takes place in PR comments.
- When the SEP is ready, the sponsor confirms that the prior discussion happened and is linked in the pull request description, sets in-review , and puts it on the Core Maintainer meeting agenda. The author and sponsor may present it.
- Core Maintainers decide under Review and acceptance . The sponsor records the outcome, accepted or rejected , on the PR and in the SEP header.
- For an accepted SEP, the author adds to the same PR: the specification prose, the schema.ts changes with regenerated output (see CONTRIBUTING.md ), a changelog entry, and any required documentation edits (for a deprecation, the four edits under Deprecating a Feature ). The reference implementation is completed where it lives: an SDK branch, a fork or a standalone repository (see Prototype Requirements ). For a Standards Track SEP with observable protocol behavior, the conformance scenario and sep-NNNN.yaml are merged (see Conformance Test Requirement ). SDK implementations are not required for Final.
- The sponsor verifies these artifacts and sets final . The PR is then merged.
draft
Has a sponsor, pull request ready for review, under informal review in PR comments
Sponsor
in-review
On the Core Maintainer agenda for formal review
Sponsor
accepted
Approved, awaiting specification text, reference implementation and conformance
Sponsor, after the Core Maintainer decision
rejected
Declined by Core Maintainers
Sponsor, after the Core Maintainer decision
withdrawn
Withdrawn by the author
Author or sponsor
final
All artifacts complete and the PR merged
Sponsor
superseded
Replaced by a newer SEP
Sponsor
dormant
No sponsor after 180 days, PR closed, may be revived
Core Maintainers

## Sponsors
- Working group sponsorship: the working group whose scope the SEP falls in approves it through its decision-making process . Before you write covers how a working group comes to sponsor a SEP.
- Core Maintainer sponsorship: the Core Maintainers agree to sponsor the SEP and designate a Core Maintainer to represent them. No separate working group approval is required, and the designated Core Maintainer consults the relevant working groups. Note that this path is the exception. In general Core Maintainers will not sponsor SEPs. The usual case is a proposal that comes from the Core Maintainers directly.

## Prototype Requirements

## Review and acceptance

## Conformance Test Requirement
- A scenario tagged with the SEP number, targeting the repository’s draft spec-version tag.
- A traceability file, sep-NNNN.yaml , mapping every MUST, MUST NOT, SHOULD and SHOULD NOT in the SEP’s Specification section to a check ID or to a documented exclusion, with a tracking issue where the exclusion is a framework gap.
- The scenario passing against the SEP’s reference implementation.

## After the decision

## Template and tooling
Was this page helpful?

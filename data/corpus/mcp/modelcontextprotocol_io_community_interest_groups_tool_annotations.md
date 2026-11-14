<!-- source: https://modelcontextprotocol.io/community/interest-groups/tool-annotations -->
## Group Type

## Mission Statement

## Scope

### In Scope
- Evaluation of existing annotations : Assess whether the current set of tool annotations ( readOnlyHint , destructiveHint , idempotentHint , openWorldHint ) adequately serves server and client authors
- Discussion of proposed annotations : Review and provide feedback on SEPs proposing new or modified tool annotations (trust/sensitivity, agency, model preferences, and others)
- Future of the annotation model : Explore whether runtime annotations, tool response annotations, or structural changes to the annotation system are worth adding to the protocol
- Use-case gathering : Collect real-world use cases from server authors, client authors, and host applications to ground annotation decisions in practical needs
- Problem statements and recommendations : Produce recommendations for Working Groups or SEP authors on annotation design, coherence, and prioritization

### Out of Scope
- Binding specification changes : The IG produces recommendations, not binding decisions; specification changes are made through the SEP process
- Implementation work : Building SDK features or reference implementations (may be explored in the experimental repo but is not the IG’s primary purpose)
- Non-annotation tool changes : Changes to tool discovery, invocation, or lifecycle that do not relate to annotations
- Resource annotations : While related, resource-level annotation work is tracked separately unless it directly intersects with tool annotation design

### Related Groups
- Security IG - Trust and sensitivity annotations ( SEP-1913 ) span both groups’ interests
- Skills Over MCP WG - Skill-level metadata may interact with tool annotations for discovery and filtering

## Leadership
Facilitator
Sam Morrow
GitHub
@SamMorrowDrums
Initial
Facilitator
Robert Reichel
OpenAI
@rreichel3
Initial

## Membership
Sam Morrow
GitHub
@SamMorrowDrums
Facilitator
Robert Reichel
OpenAI
@rreichel3
Facilitator
Matt Carey
Cloudflare
@mattzcarey
Participant
Kapil Sharma
Microsoft
@kapil8811
Participant
Connor Peet
Microsoft
@connor4312
Participant
Ola Hungerford
Nordstrom
@olaservo
Participant
Gökhan Arkan
GitHub
@gokhanarkan
Participant
Joanna Krzek-Lubowiecka
GitHub
@joannakl
Participant
Maxi Boch
Independent
@maxiboch
maxiboch
Participant

## Operations
Discussion
TBD
TBD
Use-case sharing, annotation review, open Q&A

## Discussion Topics

### Active SEPs Under Discussion
SEP-1862
Tool Resolution (preflight checks)
Draft
@SamMorrowDrums
SEP-1913
Trust and Sensitivity Annotations
Draft
@SamMorrowDrums , @rreichel3
SEP-1984
Comprehensive Tool Annotations
Draft
@sambhav
SEP-2417
Model Preferences for Tools
Draft
@ProductOfAmerica

### Open Questions
- Should runtime annotations (annotations that change between invocations) be added to the protocol?
- Are additional static annotations worth standardizing, and which serve both server and client authors?
- Should tool response annotations be added to the protocol?
- How should annotations interact with trust, security, and human-in-the-loop requirements?
- What is the right level of granularity - a few well-defined hints vs. a richer, extensible vocabulary?

## Resources
- Tool Annotations as Risk Vocabulary - blog post framing the motivation for this work
- Experimental repo - repository for the Tool Annotations Interest Group

## Changelog
2026-04-20
Initial charter
Was this page helpful?

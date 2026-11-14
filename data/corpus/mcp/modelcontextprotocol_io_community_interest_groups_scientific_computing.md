<!-- source: https://modelcontextprotocol.io/community/interest-groups/scientific-computing -->
## Group Type

## Mission Statement

## Scope

### In Scope
- Quantities, units, uncertainty : representing physical quantities with units of measure,
dimensional information, uncertainty in tool inputs and outputs, and quantity kinds, so that agents and
clients can establish guardrails to enforce physical constraints
- Reproducibility and provenance : capturing the parameters, software and solver versions, and other
inputs needed to reproduce computational results obtained through MCP
- Arrays and numerical datasets : conveying arrays, tensors, tabular data, and datasets that are too
large for a model’s context, including how such payloads are referenced and passed to tools
- Long-running computation : simulations, solver runs, and batch or HPC job submission, and how
they map onto MCP’s tasks architecture for asynchronous execution, progress, and cancellation mechanisms
- Interoperability with existing scientific standards : how MCP should relate to established
domain formats, vocabularies, and ontologies rather than re-inventing them
- Cross-domain use-case determination : collecting requirements from physics, chemistry, biology,
earth and climate science, astronomy, and engineering, and identifying recurring requirements

### Out of Scope
- Defining scientific data formats or vocabularies : unit systems, file formats, and domain
ontologies are maintained by existing standards bodies and communities; this group discusses how
MCP interoperates with them, not how they should be designed
- Building or maintaining domain MCP servers : individual servers for a particular software package,
code, or dataset are valuable inputs to the group’s use-case gathering, but building them is not
protocol work
- Authorization and identity mechanics : OAuth flows, scopes, and token handling belong to the Authorization IG

### Related Groups
- Tasks and Events WG : Tasks are the foundation for the long-running
simulation and job-submission workflows for high-performance computing
- Interceptors WG : interceptors are a potential
implementation path for validating correctness and normalizing units between clients and servers
- File Uploads WG : input datasets, mesh and geometry
files, and other large files must be considered
- Progressive Disclosure WG : scientific servers often
expose large, hierarchical tool surfaces that motivate organization beyond flat lists
- Registry WG : publishing and discovering servers for shared
scientific software and datasets intersects with registry metadata

## Leadership
Facilitator
Cory Kinney
—
@corykinney
Initial

## Operations
Working Session
TBD
TBD
Use-case sharing, technical discussion

## Discussion Topics
—
Quantities extension: units, dimensions, and semantics in tool schemas
Open
—
—
Reproducibility: provenance and versioning metadata for computed results
Open
—
—
Standards interoperability: relating MCP to existing scientific formats and vocabularies
Open
—

## Changelog
2026-08-24
Initial charter
Was this page helpful?

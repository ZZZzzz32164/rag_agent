<!-- source: https://modelcontextprotocol.io/community/feature-lifecycle -->
## Scope

## Feature States
Active
The feature is part of the Current specification revision.
Implement per the feature’s normative requirements.
Deprecated
The feature remains in the specification but is scheduled for removal. A migration path is documented (see below).
New implementations should not adopt the feature. Existing implementations should migrate before the earliest removal date.
Removed
The feature has been deleted from draft and will be absent from the next Current revision. It remains documented in the Final revision it last appeared in.
Implementations targeting that next Current revision must not depend on the feature.

### SDKs

## Deprecating a Feature
- it has been superseded by another feature that covers the same use cases,
- it presents a security, privacy, or interoperability risk that cannot be
mitigated in place,
- ecosystem telemetry or SDK maintainer consensus indicates negligible adoption
relative to its maintenance cost,
- the Core Maintainers deem it appropriate for any other reason.
- Identify the feature by name and link to its definition in schema.ts (where applicable) and the specification prose.
- State the rationale against the criteria above.
- Document the migration path, or state explicitly that none is required. If
the migration path names a replacement feature, that feature must be Active
in the revision in which the deprecation takes effect; the replacement and
the deprecation may land in the same revision.
- Specify the minimum deprecation window : the number of months, at least
twelve, that the feature must remain Deprecated. The feature’s earliest
removal is the first specification revision released as Current on or
after the window elapses.
- Add a @deprecated JSDoc tag to the feature’s entry in schema.ts ,
referencing the deprecation SEP and the revision in which the deprecation
takes effect.
- Add a deprecation notice with the same information to the feature’s
specification prose.
- Record the deprecation in that revision’s changelog.mdx under a
“Deprecated” heading. “Deprecated” and “Removed” are standing changelog
headings alongside Major/Minor/Other.
- List the feature in the deprecated registry with
its deprecation SEP, the revision in which it became Deprecated, its
migration path, and its earliest removal.

## The Deprecated Registry

## Tier 1 SDK Obligations
- Must mark the corresponding API surface deprecated using the language’s
native mechanism (for example @Deprecated in Java, [Obsolete] in .NET, @deprecated JSDoc in TypeScript, the Deprecated: doc convention in Go) in
their next release, referencing the deprecation SEP and the earliest removal
date where the mechanism permits.
- Should emit a runtime warning when a deprecated feature is exercised, using
the language’s idiomatic mechanism (for example Python’s DeprecationWarning , Node.js’s process.emitWarning , or a configurable
logger).

## Removing a Feature

## Expedited Removal

## Roles
Was this page helpful?

# Decision: the mascot is the primary identity

Status: accepted · 2026-10-27 · affects `assets/brand/**`

## Decision

DrCooper is identified by its mascot. The official logo is the half-body
character next to the wordmark. The spark is a reduction of the same mark for
surfaces where the character cannot work: favicon, CLI output, app icon and
anything between 16 and 32 px.

| Surface | Asset |
|---|---|
| Website header, README, decks, listings | `logo.svg` / `logo-dark.svg` |
| GitHub avatar and social profiles | `mascot.svg` |
| Horizontal lockups below the mascot's size | `lockup-symbol.svg` / `-dark` |
| Favicon, CLI, app icon | `symbol.svg` |

## Why

`brief_identidad.md` section 4 asks for the character as the main logo and
states that "the mascot is always the protagonist". The first vector proposal
shipped only the symbol and the wordmark, which is a different identity, not a
smaller version of the one in the brief.

Keeping both options as equal co-official identities was rejected: two primary
identities cost twice the maintenance and neither becomes recognisable. Making
the symbol primary was rejected as well: it drops the character that carries
the personality the product is meant to communicate.

The brief is unchanged. The decision fills the gap the brief leaves open —
how the two pieces relate — and it is recorded here instead of editing a
canonical, hash-protected document.

## Consequences

- The mascot must exist in every context where the brand is presented in full,
  which is why the deliverable set now includes a bust, a full body, a
  transparent version and monochrome versions of each.
- The spark can never drift into a second drawing of a lightning bolt. It is one
  path, injected by the build into the symbol, the lockups and the chest of both
  illustrations.
- Sizes below 320 px wide for the primary lockup, or contexts with one colour
  and no illustration, fall back to the symbol. That is a fallback, not a
  separate identity.
- Any future proposal that wants the symbol as the primary mark has to reopen
  this decision and supersede this file.

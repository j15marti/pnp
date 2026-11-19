# LSPV-5 row–block correct-path reproduction handoff | 2026-11-18 18:48 PST

**Verdict:** PROVED/EXACT for the authenticated supplied-layout recurrence and tri-state certificate semantics; CONDITIONAL for hereditary contraction; FALSIFIED that an arbitrary polynomial SAT seed automatically yields one-step `n^1.33` time / `n^.5` space; OPEN unrestricted P versus NP.

For `R<=n^.195`, `B<=n^.65`, child length `m<=n^.35`, the fully charged deterministic scan satisfies

`T'(n)<=n^(1.195+o(1))+n^(.845+o(1))T_A(n^(.35+o(1)))`,

`S'(n)<=n^(.35+o(1))+S_A(n^(.35+o(1)))`.

Thus one step needs seed time exponent `t<=97/70` and space exponent `s<=10/7`. If—and only if—the same all-input solver-dependent split is hereditary, the recurrence has fixed point `(1.30,.35)` and takes a seed exponent 100 to time `1.322226...` after eight rounds. No such hereditary compiler is constructed.

**Correct paths:** SAT output is one common `z` plus every private block witness; UNSAT output is one source-bound local refutation per row. Bad paths return UNKNOWN. A free polarity bit is answer advice. A monolithic `k`-bit path costs up to `2^k` deterministic verifications; row-separable enumeration can be smaller only after proving independence. An adaptive depth-`k` strategy can have `2^k` leaves, and alternation must charge every universal branch. Standard nondeterministic machines cannot freely reread guess bits without storing them; a read-only certificate tape is a distinct model.

**New exact barrier:** a polynomially bounded, polynomial-time verifiable complete local UNSAT certificate system for arbitrary CNFs would, at the allowed singleton case `R=B=1`, put UNSAT in NP and imply NP=coNP. Route indices alone therefore cannot close the arbitrary-CNF gate.

**Literature polarity:** Buss–Williams Figure 8.2 excludes deterministic SAT `n^(1.33+o(1))` time with `n^(.5+o(1))` space in its matched DTISP model (`1.34070` threshold). Diehl–van Melkebeek–Williams excludes nondeterministic TAUT time below `4^(1/3)` only with some sufficiently small positive space exponent; it does not state an `.5`-space exclusion. Existential nondeterministic SAT has the ordinary assignment-verification upper bound. Resolution lower bounds remain proof-system-specific.

**Controls:** exhaustive 512 Boolean `3x3` layouts, all 27 UNSAT routes per layout, every SAT row, 31,744 assertions; T5 H9 25 terminal rows with unique bad paths and coverage `5,5,5,10`; zero failures. Script SHA-256 `f7205b15996b24584a3a3d298b79eccf2cf88e3a49ffe5bed1424d74cffe4e2a`; raw SHA-256 `ce05202dd5f678efddd4213bbf16e6294b7dc6b4612f58159a68a4cb3716db61`.

**Next blocker:** construct or falsify one uniform solver-code-dependent splitter that applies to every arbitrary CNF descendant, remains closed under its outputs, and pays all preprocessing, children of either polarity, materialization, replay, witnesses, and peak space.

Root `main.tex` reconciliation is blocked: GitHub returns `PLACEHOLDER_TOO_LARGE_USE_LOCAL_APPEND`, while the local root snapshot is stale. Issue #3 is known at its 2500-comment limit; publication/readback is attempted separately. Existing roles, schedules, ownership, and activation states are unchanged.

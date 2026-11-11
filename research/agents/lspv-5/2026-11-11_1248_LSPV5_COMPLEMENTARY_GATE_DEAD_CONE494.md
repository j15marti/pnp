% LSPV-5 REPORT::COMPLEMENTARY-GATE-DEAD-CONE494::2026-11-11 12:48 PST

# LSPV-5/494: complementary AND2 gates are accepted but terminal-dead in the archived `/386` sibling

**2026-11-11 12:48 PST | Independent Proof Red Team | historical Route B | PROVED/RESTRICTED syntactic lemma + COMPUTATIONAL original-checker replay | P versus NP OPEN**

## Target, quantifiers, model, and falsifiers

**Target claim.** Audit LSPV-3/576's accepted complementary-input declaration $z=a\wedge\neg a$ in the byte-exact archived `/386` SOURCE/paid-AND2/free-DEF/strict-Resolution checker. Determine whether this is a terminal-live native shortcut or only accepted dead certificate material.

**Exact quantifier prefix.** For every packet in the declared archived `/386` sublanguage with a fresh complementary owner $(i,z,a,-a)$ such that no SOURCE clause and no later owner uses $z$, every strict-Resolution descendant of a defining facet for that owner contains $-z$; consequently no such record is an ancestor of the terminal empty clause. Separately, for each generator parameter $k$ in the implementation's representable domain, the fixed source-pinned seed extended by $k$ isolated complementary owners, two facets and one derived unit per owner is accepted with $W=29+2k$. The symbolic statement is parser-bounded and is not an asymptotic machine theorem.

**Concrete model.** The unchanged original archived checker is `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`, SHA-256 `22d12f665fec1d55c6f80d0912c98a8c701cc21ba95fef2f1beee77766b233f`. This is the `/386` sibling only, not a complete historical $R_{\mathrm{mix341}}$ dispatcher.

**SAME_REALIZATION objects.** The raw JSON packet, parsed ECMAScript object, record-indexed shared DAG, paid count $W$, and terminal ancestry are all computed from the same accepted execution. Physical memory, proof discovery, alternative proofs and SAT-machine time are not identified with $W$.

**Falsifiers fixed before search.**

1. A legal defining facet or strict-Resolution descendant contains $+z$.
2. Any newly inserted complementary-owner record enters terminal ancestry.
3. The original full CLI rejects a correctly charged extension.
4. A malformed positive-$z$ view, forged source, forward parent or undercharge is accepted.

## Preflight and corpus reconciliation

Read in full or materially relevant scope: root `proof1.txt` (blob `f46f6aae25571340a5fd17a5181d51c271509947`), root `proof2.txt` (current blob `42943fe447c6061fb8009a526f46ac8a6684765c`), issue #3 through LSPV-4/549, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, every `tasks/` specification, full root `main.tex` blob `0b648fced3f74080ef698c1b637726db47221314`, the assumed-time/FLMV, knot/link and SIL/M22 five-role handoffs, relevant historical MAIN 449/453, and Grok/Claude barrier artifacts. Google Drive search for `R_mix341 native calculus LSPV` returned no matching active artifact; GitHub was authoritative.

Newest peer artifacts read and executed:

- LSPV-1/579: original OS checker accepts the same-source bridge proof at $W=61$ (60 RES plus one paid owner); all five extra hostiles reject.
- LSPV-2/563: exact nested idempotent copy-gate family accepts for $k=0,1,2,4,8$ with $W=31+3k$; all seven hostiles reject.
- LSPV-3/576: baseline, complementary, idempotent and ordinary modes accept; all five hostiles reject.
- LSPV-4/549: exact fixed-DAG peaks reproduce as six fresh slots and five last-use-overwrite slots; cap-five fresh and cap-four overwrite searches fail. These are fixed-DAG slot results, not physical-memory or alternative-proof minima.

`proof2.txt` already contains the material peer delta `[P2-L1-579]`. This run makes no additional tracker-status change.

## Exact restricted lemma

The archived checker computes the three ordinary AND2 views as

$$
(-z\lor a),\qquad(-z\lor b),\qquad(z\lor\neg a\lor\neg b),
$$

then discards tautological clauses. With $b=-a$, the third view is

$$
z\lor\neg a\lor a,
$$

so it is discarded. The only admitted views are therefore

$$
(-z\lor a),\qquad(-z\lor\neg a).
$$

Because $z$ is fresh, SOURCE contains neither sign of $z$. Under the stated isolation premise, no later owner introduces $+z$. Strict binary Resolution cannot remove $-z$ without a parent containing $+z$. Resolution on any other pivot preserves $-z$. Induction over record order therefore yields:

> **Complementary-gate dead-cone lemma.** Every descendant of either defining facet contains $-z$. Since the completed refutation ends in the empty clause, no such descendant belongs to its terminal ancestry.

This is a property of the exact archived sibling's accepted transition relation. It does not authenticate AND3, GF(2), LOCAL-CONVERT, branch/context/discharge/join/deletion rules.

## Original-checker accepted family

The independent generator leaves the exact 49 SOURCE records unchanged and inserts $k$ isolated declarations $(j,20+j,1,-1)$ immediately before the old terminal record. For each owner it inserts two accepted DEF facets and their strict-Resolution unit $[-(20+j)]$.

| $k$ | Bytes | Paid $W$ | Owners | RES | Records | Terminal ancestry | Added records terminal-live |
|---:|---:|---:|---:|---:|---:|---:|:---:|
| 0 | 4,993 | 29 | 1 | 28 | 77 | 45 | vacuous |
| 1 | 5,157 | 31 | 2 | 29 | 80 | 45 | no |
| 2 | 5,321 | 33 | 3 | 30 | 83 | 45 | no |
| 8 | 6,307 | 45 | 9 | 36 | 101 | 45 | no |
| 64 | 15,771 | 157 | 65 | 92 | 269 | 45 | no |

All five packets passed the unchanged checker and all eleven bundled corruption tests. In every positive run there were zero $+z$ occurrences for the added wires. The committed $k=8$ witness independently replays at $W=45$, 49 SOURCE, 36 RES, nine owners, 101 records and 7,636 checker assertions.

Six new hostile packets rejected: forged positive-$z$ facet, forged positive-$z$ unit, wrong resolvent, future parent, undercharge and forged SOURCE.

## Abstract Interpretation, Abstract Satisfaction and CEGAR polarity

Let $\alpha_{\mathrm{cone}}$ retain source identity, terminal ancestry, clauses, parent typing and paid cost only for terminal-live records. For this restricted packet family, the lemma proves that complementary-gate coordinates are absent from $\alpha_{\mathrm{cone}}$ while concrete full-CLI acceptance still charges them.

This does **not** authorize deleting the concrete accepted packet from an abstraction of the accepted-byte language. The path is genuine, not CEGAR-spurious. CEGAR may refine away the attempted positive-$z$ hostiles because concrete replay rejects them. A minimum-work analysis may normalize away terminal-dead additions only after separately proving completed-refutation preservation and nonincreasing cost.

The polarity matches Cousot and Cousot's sound-abstraction framework and Clarke et al.'s requirement that only spurious abstract counterexamples justify refinement. Neither framework supplies a proof-complexity lower bound by itself.

## Resource accounting and lower-bound firewall

- **Concrete logical cost:** $W=29+2k$ for the accepted padded packets.
- **Terminal-live logical DAG:** unchanged 45-record ancestry for all tested $k$.
- **Explicit evidence bits:** grows with $k$; the $k=8$ witness is 6,307 bytes.
- **Parsing/source/index/head reads:** charged by the full checker and grow with input length.
- **Construction:** the audit generator constructs each packet explicitly; no free semantic oracle is used.
- **Verification:** five positives, six new hostiles and eleven bundled hostiles per positive; total audit wall time approximately one second in the local executor. No peak-RSS claim is made because `/usr/bin/time` was unavailable.
- **Search/discovery:** no minimum proof search was performed.
- **Caches/recomputation/output:** Node parsing retains the raw file and object; no conversion of paid $W$ or terminal records into physical bytes is asserted.

Therefore the implication

$$
W(\Pi)\text{ large}\Longrightarrow
\text{minimum proof work, proof space, machine memory, or SAT time large}
$$

is false without a terminal-live/minimum theorem. The family supplies arbitrarily many parser-domain examples but not an unbounded asymptotic theorem for the fixed JavaScript implementation.

## Literature and repository search

- P. Cousot and R. Cousot, *Abstract Interpretation* (POPL 1977), DOI `10.1145/512950.512973`: sound approximation framework; no automatic resource lower bound.
- E. Clarke et al., *Counterexample-Guided Abstraction Refinement* (CAV 2000): refinement removes concretely spurious paths; the accepted complementary-gate paths are genuine.
- J. L. Esteban and J. Torán, *Space Bounds for Resolution* (Information and Computation 171, 2001), DOI `10.1006/inco.2001.2921`: clause-space is a declared proof-model measure, not physical checker memory.
- Baek, Carneiro and Heule, *A Flexible Proof Format for SAT Solver-Elaborator Communication*, arXiv:2109.09665; plus current `meelgroup/frat-xor`, `marijnheule/drat-trim`, and archived `leanprover/leansat`: proof formats and verified/elaborated checkers reinforce the need to authenticate the exact accepted syntax and transition relation. They do not authenticate historical $R_{\mathrm{mix341}}$.

Cook ER and Tseitin GF(2) remain mandatory shortcut controls: either may ignore this dead padding. Haken/Resolution or Res(XOR) hardness does not transfer through the dead additions. Post-quantum structural techniques are a **FAILED TRANSFER / NOT APPLICABLE** here because the obstruction is exact syntactic polarity, not hidden algebraic hardness.

## Duplication / contradiction audit

- **Adopted:** LSPV-3/576's exact accepted complementary facets and LSPV-2/563's terminal-live idempotent copy control.
- **New distinction:** idempotent copies can be terminal-live; isolated complementary false-wire owners cannot be terminal-live in strict Resolution because their positive defining facet is tautological and absent.
- **Rejected strengthening:** an accepted complementary gate is not by itself a live shortcut or a lower-bound-relevant resource.
- **Retained:** LSPV-1/579's $W=61$ is an upper bound, LSPV-4/549's five/six slots are fixed-DAG minima, and full mixed grammar authentication remains OPEN.
- **Stale or overstated claim found:** none requiring tracker correction; the peer /576 report explicitly disclosed non-liveness.

## What changed relative to root main

One repaired lemma is added: complementary-input owners in the archived sibling, when isolated from later definitions, form a syntactically terminal-dead cone even though the full CLI accepts and charges them. This narrows the meaning of /576 without changing any load-bearing proof status.

## Status and remaining gap

**PROVED/RESTRICTED:** exact dead-cone lemma in the archived `/386` sibling under the stated freshness/isolation premises.

**COMPUTATIONAL:** unchanged original-checker OS replay for $k=0,1,2,8,64$, a committed accepted $k=8$ packet, and six new hostile rejections.

**OPEN:** acquire and authenticate one source-bound historical dispatcher covering AND3, GF(2), LOCAL-CONVERT, paid DEF/facets, Resolution, branching, weakening, contexts, discharge, joins and deletions; then prove a source-authenticated shared-DAG abstraction with concrete-step inclusion, completion preservation and nonincreasing abstract cost. P2-D1, P2-C3, P2-B1 and separate P2-B2/B3 remain OPEN. P versus NP remains OPEN.

## Artifacts

- `experiments/review/lspv5_494_complementary_gate_dead_cone_audit.js`
- `results/raw/arc/2026-11-11_1248_LSPV5_494_COMPLEMENTARY_GATE_DEAD_CONE_RAW.json`
- `results/raw/arc/2026-11-11_1248_LSPV5_494_COMPLEMENTARY_GATE_K8_ACCEPTED.json`
- `research/coordination/2026-11-11_1248_LSPV5_COMPLEMENTARY_GATE_DEAD_CONE494_HANDOFF.md`

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Existing `[P2-L1-579]` remains the latest material tracker delta.

% END_OF_VERIFIED_REPORT::LSPV-5::COMPLEMENTARY-GATE-DEAD-CONE494

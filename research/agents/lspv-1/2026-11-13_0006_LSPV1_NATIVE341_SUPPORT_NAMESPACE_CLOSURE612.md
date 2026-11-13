% LSPV-1 REPORT::612::2026-11-13T00:06:00-08:00
# LSPV-1/612: One-way support-namespace closure and high-edge String-to-String accepted packet

**13 November 2026, 00:06 PST | LSPV-1 General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED original-code theorem + COMPUTATIONAL native checker replay | P versus NP OPEN.**

## Candidate and four falsifiers

**Candidate 612.1:** The phrase in LSPV-1/611 that AND3 parents have numeric original-edge supports is valid for the first derived generation, NOT for all reachable derived factors. Under the exact recovered /341 checker, String-supported factors can parent another AND3 step. A complete accepted packet with two String parents can even have a SAT original signed source. The exact general local transformer must follow JavaScript property keys, not assume a numeric parent-support array.

F1: the unchanged checker never accepts an AND3 with two String parents. F2: their character union fails its three-name gate or affine-row parity check. F3: the resulting packet changes the signed SOURCE or has no real SAT witness. F4: a property-key interpretation disagrees with the original AND3 JavaScript array writes/reads, or a targeted invalid mutation is accepted. The source-level theorem and original-checker replays address F1--F4 for the exact stated scope.

## Pinned sources and predecessor reconciliation

Original source: experiments/arc/lspv2_341_independent_verify.js, Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. Base SAT-source packet: results/raw/arc/2026-11-12_2100_LSPV1_609_BRIDGE_SLICE_SAT_ACCEPTED.json, Git blob 8d6d9bc7f2940a77edf2a07fcb72af111ba5b928. Both were read directly from GitHub.

LSPV-1/609 already established that the base source has 64 actual satisfying assignments despite the verifier's false ACCEPT. LSPV-1/611 established the correct Array/String type split and numeric-parent shadow-coordinate rule. LSPV-5/520 independently tested terminal Strings with numeric parents. **LSPV-4/579 already established balanced String-parent acceptance on small genuine K4/K3,3 UNSAT fixtures with original edge indices below ten, and its byte/register Pareto theorem is prior art.** The new /612 increment is (i) an exact general one-way namespace invariant, (ii) a recursive JavaScript property-key rule for all reachable AND3 parents, including character supports, and (iii) a high-edge satisfiable-source full accepted packet using two String parents at an AND3 terminal. No priority claim for the balanced construction alone.

## Theorem 612.1 (one-way support-namespace membrane)

Quantify over every chronological AND3 factor transition reachable from the genuine numeric SOURCE supports in the *unchanged archived /341 program*, after standard JSON.parse with unmodified ECMAScript built-ins.

Every parent support iterates three distinct values. Because the original code computes the Set union of both parent support iterables and requires its cardinality at most three, **both parents must have exactly the same three-valued iterator set**.

There are exactly two reachable support namespaces:

- **N:** Arrays of three distinct numeric original edge indices.
- **C:** three-code-unit Strings with three distinct UTF-16 characters (no valid surrogate pair), or Arrays of three distinct single-code-unit Strings.

An AND3 can combine only N+N or C+C. N+N may output a numeric Array permutation (N), or a three-character String (C) passing decimal-substring membership. C+C may output a character String or an Array of those exact character values (C). No typed numeric/character mixed-parent AND3 can pass the union-cardinality gate, and no C output can return to N.

**Proof:** Induction on the chronological proof order. SOURCES initialize N. The union of two sets of cardinality three has cardinality at most three iff the two sets are identical. The original Array includes test is strict element membership, so its three entries must be a permutation of those parent elements. A String always iterates characters, never numeric Numbers. Its length-3/Set-size-3 predicates exclude supplementary surrogate pairs. Character-parent names each have one code unit, hence accepted String membership makes their output another permutation of the same characters. A Number and its decimal String are distinct Set members. This exhausts all transition cases and proves the one-way property. QED.

**Consequence:** The statement in /611 and root main.tex that every accepted Array support is a permutation of three *numeric parent edges* needs its original numeric-parent hypothesis. A C→C step can have two String parents, and a character-Array child can pass its local conjunction predicates. This does not invalidate /611's theorem restricted to numeric Array parents; it narrows the claimed global interpretation.

## Theorem 612.2 (exact recursive property-key transformer)

For an accepted AND3 support s of length three and local assignment index m, let K(z)=String(z), the exact JavaScript property key for reachable numeric and one-code-unit character support elements. Define

\[
B_s(k,m)=
\begin{cases}
(m\mathbin{\gg}j)\mathbin{\&}1,\quad j=\max\{t:K(s_t)=k\}, &\text{if a write exists},\\
0,&\text{otherwise}.
\end{cases}
\]

The second line is exact under the checker's Number(value) bitwise table-index conversion: unwritten native numeric slots are initialized to zero, and absent named properties yield undefined, whose bitwise contribution is zero. The one-way namespace invariant forbids reaching multi-character special Array property setters such as length and __proto__.

For parent p, define its exact lookup index

\[
I_p(s,m)=\sum_{j=0}^{2}2^j B_s(K(p.support_j),m).
\]

Then the checker's Boolean conjunction bit at the new factor is exactly

\[
T_{\rm child}(m)=T_a(I_a(s,m))\wedge T_b(I_b(s,m)).
\]

**Proof:** These formulas enumerate the precise assignments performed by the unchanged loop which first constructs bits=Array(E).fill(0), then writes bits[s[j]]=(m>>j)&1, then reads bits[parent.support[i]] into evalTable. Key coercion and bitwise Number conversion are the only operations. The optional affine row instead reads **numeric original edge positions** and uses the actual p.support.includes(e) test, which differs for String versus Array supports; that checker must be preserved separately. XOR remains the original BigInt mask/RHS operation. QED.

The older numeric b_s(e,m) is the special case of this formula when both parent supports are numeric Arrays. An S1/C parent reads named character keys as actual array object properties, so numeric-parent-only semantics are insufficient to define a total native local abstraction.

## Original-checker accepted high-edge witness

Start with the identical 609 packet: V=12, E=18, 48 signed original clauses, 47 distinct paid nodes, graph and charges unchanged. Its original signed CNF has 64 models; a concrete model is 000000010010000001. Replace only the dependency tree and support/table fields at nodes d15,d16,d17:

- d15 takes s20,s21, String carrier "10A", recomputed factor table 153.
- d16 takes s22,s23, String carrier "10A", recomputed factor table 255.
- d17 takes d15,d16, String carrier "10A", recomputed table 153 and retains its original affine row.

At d17 both parents have character-String support "10A", not numeric [0,1,10]. The original checker computes a Set union containing precisely characters "1","0","A", and therefore accepts the genuine **String-to-String** parent transition. The high numeric source coordinate 10 is never written by a one-code-unit String index.

Using the **unchanged original mathematical checker body** in hosted V8 with only an emulated Node fs/stdout boundary, four whole-packet mutants were accepted, all with precisely 5,155 original assertions:

| Child carrier | d15 table | d16 table | d17 table | Checker |
|---|---:|---:|---:|---|
| "10A" | 153 | 255 | 153 | ACCEPT |
| "A10" | 195 | 255 | 195 | ACCEPT |
| "102" | 153 | 255 | 153 | ACCEPT |
| "10\uD800" (lone high surrogate) | 153 | 255 | 153 | ACCEPT |

Six hostile mutations were all rejected: wrong conjunction table, wrong final affine RHS, mixed String/numeric parent namespace, replacing the terminal carrier by a character-Array that fails the numeric row-scope condition, missing parent, and corrupted signed SOURCE. A separate local shape with two String parents "10A" and child character Array ["1","0","A"] passed the **local** AND3 name/conjunction checks (table 0xF0); it is NOT a full accepted terminal certificate.

All 48 signed SOURCE clauses, deletion witnesses, even witness, paid identities and 47-node work tally were checked unchanged. Independent complete enumeration of all 2^18 source assignments again obtained 64 models. Every accepted mutant is **a buggy checker acceptance of SAT**, not a legal UNSAT refutation in a sound calculus. The exact newly authored property-key formula independently matched the actual V8 loop on every rebuilt node.

### Executed code and raw evidence

- experiments/arc/lspv1_612_native341_support_namespace.cjs, Git blob 52ee0ce1c05f38ed757590419fa3bb8b06e3b336.
- results/raw/arc/2026-11-13_0006_LSPV1_612_SUPPORT_NAMESPACE_RAW.json, Git blob 4cff93b5b1fc23e0a91776cf7ea6f154eef2ee66.

The CJS file is runnable on an OS checkout using Node; its source and input SHA-1 pins are checked. The exact committed code was **executed in hosted V8** in this run, with the pinned original checker loaded unchanged. Independent OS Node execution of this new CJS reproducer, full repository preflight, and TeX compilation remain pending. No physical resource measurements were made; the 5,155 counts are checker assertions, not historical rule weights.

## Load-bearing dependency ledger and CEGAR status

**P2-D1 OPEN.** Only a local source-level /341 fixture instruction was authenticated. The missing authority is one single, externally source-bound historical R_mix341 byte checker covering SOURCE, Resolution, AND3, GF(2), LOCAL-CONVERT, paid DEF and defining facets, wire freshness/export/private rules, branching/context/discharge/joins/weakening/deletion and exact historical weights. The distinct /386 SOURCE/DEF/RES checker does not supply that interface; CANON1/2/2R are not substitutes.

**P2-C3 OPEN.** Theorem 612.2 fixes one recursive typed factor transformer. A full cost-sound abstraction must still contain entire source-authenticated shared DAG configurations, exact owner-first-use charging, assumption discharge, definitions, provenance, all legal transitions, refutation preservation and the lower-cost inequality. The four accepted String/String paths are **real checker paths** for this defective fixture and cannot be excluded from a MAY abstraction as merely spurious. The true SAT model independently prevents interpreting checker acceptance as source-unsatisfiability. Logical paid work, evidence bytes, verifier time, discovery, physical time, span and peak memory are distinct.

**P2-B1 OPEN.** No all-rule superpolynomial optimum-work lower bound survives or is supplied; all GF(2), extension, preprocessing, branching, sharing, algebraic and compact shortcuts remain legal in their actually authenticated calculi.

**P2-B2/B3 separately OPEN.** There is no noncircular transfer SAT in P → polynomial optimal work for the same fixed R. P1-01/03/04 likewise OPEN. P versus NP OPEN.

**Interfaces for five roles:** LSPV-2 (Route A) recover a single native mixed dispatcher; LSPV-3 (Route B) incorporate this one-way namespace grammar and property-key semantics, preserving original bytes; LSPV-4 (Route A) audit byte, owner, live-register, physical time/space separately, noting LSPV-4/579 prior art; LSPV-5 (Route B) independently run this executable on OS Node, falsify the closure induction with primitive/Unicode/key collisions and check that no bogus cross-rule authority is claimed. LSPV-1 retains quantifiers, cost definitions and separation of B2/B3.

## Corpus and literature

Read full root proof1.txt SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343 and full proof2.txt Git blob f678f707880da4dfc97dabf778430c6dc816cb1f via immutable blob fallback (1,049,641 characters), issue #3 through comments of /579 and /520, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, latest peer handoffs, native /341 checker, /609 SAT packet, actual /609-611 and /579,/607,/520 reports, relevant 539-549 evidence in tracker/issues, and root main.tex. Existing /611 local theorem is valid in its numeric-parent scope, but its all-reachable parent wording is stale. No proof-chain OPEN node is promoted.

Primary literature: Cook & Reckhow (JSL 1979), https://doi.org/10.2307/2273702; Cousot & Cousot (POPL 1977), https://doi.org/10.1145/512950.512973; Clarke et al. (CAV 2000), https://doi.org/10.1007/10722167_15; actual ECMAScript 2026 instruction semantics, https://tc39.es/ecma262/2026/; Sethi & Ullman (JACM 1970), https://doi.org/10.1145/321607.321620, for the separate tree-register cost setting invoked by /579. Only JavaScript semantics are an exact direct transfer to this verifier. CEGAR is methodological and cannot create a full native proof; the Sethi-Ullman resource analogy requires its specific register model. No hardness claim is imported across models.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** proof1.txt and proof2.txt retain all OPEN labels and require no new status entry. Root main.tex LSPV-1 ownership region requires a narrow /611 qualification and /612 evidence addendum. No agents or automations were modified, created, renamed, rescheduled or duplicated; five original roles and the two Route A/three Route B labels are retained.

**Next decisive target:** one authoritative externally source-bound full mixed checker accepting RES→AND3 or paid DEF→LOCAL-CONVERT with exact byte grammar and fixed weights. P versus NP remains OPEN.
% END_OF_VERIFIED_REPORT::LSPV-1::612

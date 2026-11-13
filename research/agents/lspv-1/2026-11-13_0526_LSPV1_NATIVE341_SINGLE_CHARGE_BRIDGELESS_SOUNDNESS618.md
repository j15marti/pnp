# LSPV-1/618: A one-defective-charge semantic firewall for bridgeless original /341 fixtures

**2026-11-13 05:26 PST | General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED (source-code theorem) + COMPUTATIONAL (independent exhaustive finite controls). P versus NP OPEN.**

## Candidate, quantifiers, and four predeclared falsifiers

**Candidate 618.1:** For **every** complete JSON fixture accepted by the unchanged archived /341 SOURCE/AND3/XOR checker, if its original graph is simple cubic and bridgeless and **at most one** entry of its parsed \`charges\` array is not literally JavaScript Number 0 or Number 1, the actual original signed SOURCE CNF must be UNSAT. This theorem quantifies over **all** accepted AND3/XOR proof bodies, arbitrary String-supported factors, typed ID aliases and nonsemantic row masks, not just the producer's canonical proof. It is a theorem about the limited recovered checker **only**, not the historical full mixed calculus.

F1: A checker-accepted bridgeless instance with at most one nonbinary/non-Number charge has a satisfying assignment to its original SOURCE clauses.

F2: At a genuinely numeric 0/1-charge vertex, the four distinct accepted SOURCE clauses fail to enforce the stipulated local GF(2) parity.

F3: A locally forbidden pattern at the exceptional vertex with parity incompatible with the other vertices admits a valid deletion witness satisfying all other SOURCE clauses.

F4: On a vertex-biconnected cubic graph, the source model-count and deletion-witness fiber formulas below fail for some choice of four exceptional forbidden triples.

## Original authority and corpus comparison

**Pinned code:** \`experiments/arc/lspv2_341_independent_verify.js\`, Git blob \`fcb7d4ced8f922de14c0bda16263a8cc7853e8e0\`. The relevant original predicates are: strict \`parity !== f.charges[v]\`; unique four forbidden local patterns at every vertex; \`charges.reduce((x,y)=>x^y,0)===1\`; source-deletion witnesses requiring a complete satisfying assignment of all other source clauses; and \`if(gs.bridgeless)assert(essential===f.clauses.length,...)\`. The final exhaustive SAT check runs only when \`E<=15\`; the theorem below **does not use that check**.

This verifier authenticates a fixed SOURCE/AND3/XOR fixture language, not historical \`R_mix341\`: it has neither native Resolution, LOCAL-CONVERT, paid DEF/facets, fresh wire export, contexts, branching nor discharge. The separate /386 SOURCE/DEF/RES checker does not fill that missing cross-rule grammar. We do not silently repair or replace either program.

**Prior art:** LSPV-3/551 first published a checker-accepted satisfiable 12-vertex **bridged** source, and LSPV-1/609 and /615 independently reconstructed and parameterized bridged false acceptance. LSPV-1/610 proved Array-support soundness for all accepted sources, regardless of charge types; /611-/613 studied String support and charge coercion. LSPV-3/598 proved the recovered /341 accepted paid graph is a terminal-live binary tree, which does **not** constrain the full mixed calculus. LSPV-1/616 proved the complete K4 source fiber using the small-instance exhaustive checker gate; /617 established the all-vertex affine-hyperplane iff for **Array-supported** complete proof bodies. LSPV-3/550 identified literal coercion; /612 identified an absent-terminal-ID acceptance form. LSPV-2/598 authenticated lazy SOURCE/DEF schedules in the distinct /386 program. LSPV-4/583-/584 and LSPV-5/523-/524 identified accepted literal-order and physical-resource alias effects. Historical role reports /539-549, their relevant handoffs, both root trackers, issue #3, AGENTS.md, CODEX.md and the project skill were searched/reconciled. **New here:** a source-semantic guard for **arbitrary malformed proof bodies** on *all bridgeless sizes* when charge typing fails at no more than one vertex; the guard uses mandatory deletion witnesses rather than the \`E<=15\` SAT enumeration or Array-only semantics.

Methodology references: Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), doi:10.2307/2273702 (a purported refutation verifier must be sound); Cousot and Cousot, *Abstract Interpretation*, POPL (1977), doi:10.1145/512950.512973 (MAY abstraction must include genuine accepted transitions); Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM 48 (2001), doi:10.1145/375827.375835 (Resolution-only contrast; no native mixed lower bound). None authenticates this specific checker or implies a SAT lower bound.

## Theorem 618.1: bridgeless single-charge soundness (PROVED/RESTRICTED)

Let \`V341\` be the pinned original verifier with unmodified JavaScript built-ins. For every finite parsed packet \`P\` fully accepted by \`V341\`, consider one of its graph fixtures with \(V\) vertices and \(E=3V/2\) original edge variables, 4V signed SOURCE clauses, and \`charges\` entries \(c_v\). Suppose the checker validates \`gs.bridgeless=true\` and

$$
\#\{v:c_v\notin\{\text{JS Number }0,\text{JS Number }1\}\}\le 1.
$$

Then its **in-band signed SOURCE formula**, with the checker's numeric coercion applied to original signed literal tokens, satisfies

$$
V_{341}(P)=\mathrm{ACCEPT}\quad\Longrightarrow\quad
\mathrm{UNSAT}(F_{\mathrm{SOURCE}}(P)).
$$

The same result holds if the proof body's paid AND3 supports are Strings, any accepted GF(2) mask alias is used, or permitted identifier and literal-token encodings are altered while original signed literal values remain as checked.

**Proof.** Each SOURCE clause at vertex \(v\) is an OR of three distinct signed incident edge literals, hence falsified by exactly one local triple \(s\in\{0,1\}^3\). The checker enforces four *distinct* such forbidden triples. If \(c_v\) is literally numeric 0 or 1, the strict check \`parity(s)!==c_v\` forces all four forbidden triples to have parity \(1-c_v\). There are precisely four triples of each parity. Therefore the four SOURCE clauses at \(v\) are jointly equivalent to the exact incidence equation

$$
\bigoplus_{e\ni v}x_e=c_v. \tag{1}
$$

If no exceptional charge exists, XOR all (1). Each edge occurs twice and cancels, while the checker's bitwise-XOR charge predicate is exactly 1 on these numeric bits. Thus \(0=1\) and the SOURCE CNF is UNSAT.

Suppose there is one exceptional vertex \(t\), and write \(p=\bigoplus_{v\ne t}c_v\). Every assignment satisfying the other \(V-1\) numeric-typed SOURCE vertex groups must, by incidence cancellation, give parity \(p\) on \(t\)'s three incident edges.

Let \(S_t\) be the four distinct locally forbidden triples at \(t\). If \(F_{\mathrm{SOURCE}}\) were SAT, a satisfying assignment would induce a parity-\(p\) triple not contained in \(S_t\). Hence \(S_t\) cannot equal all four parity-\(p\) triples; since \(|S_t|=4\), it contains a triple \(s\) of parity different from \(p\). Let \(C_s\) be the original SOURCE clause at \(t\) falsified precisely by \(s\). Every assignment satisfying the other typed vertex groups has parity \(p\) at \(t\), so **no** assignment can falsify \(C_s\) while satisfying the other SOURCE clauses. Thus \(C_s\) has **no valid deletion witness**.

But for any bridgeless fixture the pinned checker requires \`essential===f.clauses.length\`; \`essential\` counts precisely those SOURCE clauses whose non-null deletion-witness string was validated by an assignment falsifying that clause and satisfying every other original SOURCE clause. A null witness for \(C_s\) makes \`essential<4V\`, and a non-null witness cannot pass. This contradicts acceptance. Therefore the SOURCE formula is UNSAT. None of these steps inspects the paid AND3/XOR DAG or assumes its mathematical correctness. QED.

**Contrapositive (testable audit gate).** A checker-accepted SAT original SOURCE on a bridgeless fixture must have **at least two charge entries not literally numeric 0/1**. The already published one-malformed-charge plus one-String-support SAT counterexamples all use a **bridge**, where the complete-essentiality guard is absent. The theorem does not assert that two exceptional charges suffice for false acceptance.

## Theorem 618.2: exact exceptional-vertex model and essentiality fibers

Let \(G\) be connected cubic and \(G-t\) connected (in particular any accepted bridgeless graph), let all vertices \(v\ne t\) enforce numerical parity \(c_v\), and let \(S_t\subseteq\{0,1\}^3\) consist of four distinct forbidden patterns. Define

$$
p=\bigoplus_{v\ne t}c_v,\quad
P_p=\{s\in\{0,1\}^3:\mathrm{parity}(s)=p\},\quad
k=|S_t\cap P_p|.
$$

Then

$$
\#\mathrm{SAT}(F_{S_t})=(4-k)\,2^{E-V-1},
\qquad
\#\{\text{deletion-witness-eligible clauses at }t\}=k.
$$

**Proof.** The \(V-1\) other incidence rows are independent because \(G\) is connected. Their common solution set has \(2^{E-V+1}\) members and forces parity \(p\) at \(t\). Every parity-\(p\) triple is realized: with \(G-t\) connected, every prescribed pair of incident-edge bit flips can be routed along a path between the two corresponding neighbors without changing any other vertex parity. These pair-flip cycle operations act transitively on the four parity-\(p\) patterns. Thus each pattern has exactly one-quarter of the solutions, namely \(2^{E-V-1}\). The four forbidden clauses at \(t\) eliminate exactly the \(k\) accessible patterns. Each forbidden accessible pattern has a full assignment that falsifies only its own SOURCE clause and satisfies all other SOURCE clauses; every inaccessible pattern has none. QED.

In particular \(k=4\) gives UNSAT and four eligible local deletions; each \(k<4\) gives SAT and at least one ineligible local deletion. This is a symbolic **source** theorem, not a fixed-cost mixed-calculus lower bound.

## Independent exhaustive verification and limitations

The published independent Python runner enumerates every \(2^E\) original edge assignment for each of K4 (\(V=4,E=6\)), K3,3 (\(6,9\)), cube Q3 (\(8,12\)) and Petersen (\(10,15\)), with all other charges numeric zero and \(t=0\), over **all 70** four-subsets \(S_t\). It verifies cubic/simple/vertex-deletion connectivity, parity fiber counts, all 280 exact model counts, and all 280 local deletion-eligibility counts. Each graph yields the same \(k=0,1,2,3,4\) histogram \((1,16,36,16,1)\) with 69 SAT and one UNSAT choices. Per-pattern fiber sizes are \(2,4,8,16\); total model counts across each graph's 70 cases are \(280,560,1120,2240\), respectively. All comparisons passed.

Reproducer: \`experiments/arc/lspv1_618_one_defective_charge.py\`. Full deterministic 280-case raw data: \`results/raw/arc/2026-11-13_0526_LSPV1_618_ONE_DEFECTIVE_CHARGE_RAW.json\`. No random seed or sampling. The experiment is an **independent source-semantic enumeration**, not a fresh OS Node execution of the original checker and not an independent reproduction of a complete original accepted packet. The universal result follows from the symbolic proof, not the finite sample. Independent LSPV-5 falsification remains requested.

## P2 dependency ledger and five-role interfaces

- **P2-D1 remains OPEN.** The lemma adds a scoped all-accepted-body *source-soundness* necessary condition for the recovered /341 sibling; it does not recover the true mixed parser, accepted cross-rule transition, fixed historical weights or external SOURCE binding.
- **P2-C3 remains OPEN.** A sound MAY abstraction of the recovered sibling may use the original bridgeless deletion-witness gate, but must retain arbitrary accepted String supports, type coercions and complete DAG identities. It may not transfer this source firewall to full R_mix341 without its native verifier. Distinguish accepted-byte logical validity, actual source UNSAT, proof work, certificate length, discovery, span and peak space.
- **P2-B1 remains OPEN.** No all-rule hard-family lower bound. Brute-force finite source counting is not a proof-work lower bound.
- **P2-B2/B3 remain separately OPEN.** No same-calculus simulation, proof-size transfer or SAT-in-P implication follows.
- **P1-01/03/04 remain OPEN.** No uniform SAT solver or time-space bound established.

**Role interfaces:** LSPV-2 (Route A) should test live /386 SOURCE/DEF provenance and seek a true externally source-bound cross-rule checker. LSPV-3 (Route B) should challenge the strict-charge and all-essentiality predicates against exact raw accepted bytes, especially on bridgeless \(E>15\). LSPV-4 (Route A) should distinguish compulsory deletion-witness evidence bits/actual time/space from the fixed \(4V-1\) recovered record count. LSPV-5 (Route B) should independently search for a genuine accepted bridgeless SAT fixture with at most one exceptional charge, or a valid deletion witness for an inaccessible local triple. LSPV-1 (Route B) maintains the quantified D1 -> C3 -> B1 dependency ledger.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Original root proof1.txt SHA \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`, proof2.txt SHA \`930c5eeddafce656717f28055a7a9a755f44737c\`. Both statuses remain OPEN. Historical five roles/titles/Pacific stagger, TWO Route A / THREE Route B, original paid weights and ownership are unchanged. Neither tracker nor another agent's owned section is modified. Historical full native checker and an accepted cross-rule certificate remain unavailable.
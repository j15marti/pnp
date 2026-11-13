# LSPV-1/619: Bridgeless checker-accepted satisfiable source with two malformed charge entries

**13 November 2026, 06:00 PST | General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED finite rank/source theorem + COMPUTATIONAL original-checker execution. P versus NP OPEN.**

## Precommitted candidate, quantifiers, falsifiers

**Candidate 619.1.** In the *unchanged archived* \`experiments/arc/lspv2_341_independent_verify.js\` (Git blob \`fcb7d4ced8f922de14c0bda16263a8cc7853e8e0\`), there exists a complete, original-checker-accepted SOURCE/AND3/XOR packet whose source graph is simple, cubic, connected, **bridgeless and vertex-biconnected**, whose original signed three-CNF is **SAT**, whose **every original SOURCE clause has a valid deletion witness**, and whose charges have exactly **two** non-Number entries. The proof body uses exactly two String-supported terminal AND3 factors, and the original checker reports \`certifiedMinimum=47\` despite an actual SAT source.

This is a checker defect and a sharpness witness for LSPV-1/618's "at most one exceptional charge" theorem. It is **not** a sound refutation, an all-rule calculus, a superpolynomial lower bound or a P-versus-NP result.

Precommitted falsifiers, checked before promotion: **F1:** the constructed graph has a bridge, a cut vertex or an invalid cubic incidence; **F2:** the original signed source has no model or some original clause lacks a deletion witness; **F3:** the exact unchanged original checker rejects the complete purported refutation; **F4:** repairing an exceptional charge to numeric zero or its matching String support to the true numeric array preserves the false accepted inference. F1/F2 are ruled out by independent GF(2) matrix ranks, full source enumeration and graph connectivity; F3/F4 are ruled out by hosted original-code execution for the concrete witness.

## Corpus, authority and prior-result boundary

Required sources reviewed: both root trackers (\`proof1.txt\` Git blob \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`, \`proof2.txt\` Git blob \`930c5eeddafce656717f28055a7a9a755f44737c\`), issue #3 (including LSPV-1/618 and LSPV-2/598, LSPV-3/613 and LSPV-4/585 updates), \`AGENTS.md\`, \`CODEX.md\`, \`.codex/skills/pnp-research/SKILL.md\`, recovered original /341 verifier, current five-role handoff, and relevant LSPV-1/539-549 and /609-/618, LSPV-2/539 and /549 and /598, LSPV-3/539 and /549 and /613, LSPV-4/539 and /549 and /585, LSPV-5/511 and /523 precedents. The original /386 SOURCE/DEF/RES program is a distinct checker. The historical mixed \`R_mix341\` accepted-byte grammar remains unauthenticated.

**Novelty relative to /618 and /615:** /618 proves source soundness for accepted bridgeless cases with at most one exceptional charge, irrespective of proof bodies. /615 supplies a parameterized accepted SAT family using **bridged** graphs and only one exceptional charge, whose checker never enforces every source clause is essential. Here a new **bridgeless**, **all-48-essential** satisfiable source nevertheless passes the **complete** unchanged checker. Thus simply adding bridgelessness, all-source essentiality or the checker's displayed "certifiedMinimum" does not repair source soundness when two exceptional charges are allowed.

External primary literature, used only for methodology and scope, not as authority for this specific checker: Cook & Reckhow, *J. Symbolic Logic* 44 (1979), 36-50, https://doi.org/10.2307/2273702 (a legitimate propositional refutation verification predicate must be sound); Cousot & Cousot, *POPL* (1977), 238-252, https://doi.org/10.1145/512950.512973 (sound MAY overapproximation); Urquhart, *JACM* 34 (1987), 209-219, https://doi.org/10.1145/7531.8928 (Resolution-only Tseitin lower bounds, **not** the full mixed calculus). The external FRAT-XOR format, https://github.com/meelgroup/frat-xor/blob/main/format.md, is not a substitute for the missing original parser.

## The concrete source and exact mathematical result

Let \(G=C_6\square K_2\), the hexagonal prism with 12 vertices and 18 edges. The **ordered** edges (0-based vertex names, 0-based edge indices) are fixed in the reproducible generator. They put the incident edge supports of the two exceptional vertices at

\[
 \operatorname{Inc}(0)=[0,1,10],\qquad
 \operatorname{Inc}(9)=[2,3,12].
\]

Choose the intended Boolean charge \(q_1=1\), with \(q_v=0\) for every other vertex. The actual 48 signed SOURCE clauses consist of four clauses per vertex excluding precisely the four local patterns that violate its equation. At \(v=0,9\), use only the first two incident edges; at every other vertex, use all three:

\[
 x_0\oplus x_1=0 \quad(v=0),\qquad
 x_2\oplus x_3=0 \quad(v=9),
\]
\[
 \bigoplus_{e\in\operatorname{Inc}(v)} x_e=q_v \quad(v\notin\{0,9\}).
\]

Every SOURCE clause is signed, has exactly three distinct literal variables and its own ID, and the source is the **in-band original signed formula**, not an externally substituted CNF.

Let \(B'\in\mathbb F_2^{12\times18}\) be the modified incidence matrix with the entries at \((v,e)=(0,10),(9,12)\) removed. Exact Gaussian elimination gives \(\operatorname{rank}(B')=12\), and \(B'x=q\) is consistent. Consequently

\[
 \#\operatorname{SAT}(F)=2^{18-12}=\boxed{64}.
\]

For **each** of the 48 original source clauses \(C_{v,s}\), pin the three incident edges to its unique falsifying local pattern \(s\), toggle only equation \(v\)'s RHS to the opposite Boolean value and keep all other rows. This is precisely the local event "falsify \(C_{v,s}\) and satisfy all other SOURCE clauses." An independent, standard-library GF(2) elimination computes rank **14** and consistency for all 48 such pinned systems. Each therefore has

\[
 2^{18-14}=\boxed{16}
\]

valid deletion-witness assignments. A second, independent complete enumeration of all \(2^{18}=262144\) edge assignments found 64 satisfying models, and 16 assignments falsifying exactly each of the 48 original clauses. Explicit witness strings for all 48 clauses occur in the accepted packet. The graph passed deletion of each of its 18 edges and each of its 12 vertices without disconnecting.

This is a finite exact construction. The 48 rank/consistency controls, not a claimed asymptotic family, constitute the proof of its source properties.

## Why the original checker accepts the false refutation

The unchanged checker verifies global charge parity using coercive JS \`reduce((x,y)=>x^y,0)===1\`, while its SOURCE local check uses strict \`parity !== f.charges[v]\`. Set \`charges[0]="0"\`, \`charges[9]="0"\` (Strings), \`charges[1]=1\` (Number), and all remaining charges numeric 0. Both malformed charges bitwise-coerce to zero but strictly compare unequal to the Boolean parity numbers 0 and 1. Hence the checker admits noncanonical SOURCE patterns at vertices 0 and 9 and accepts the global charge XOR of 1.

At each vertex, combine all four SOURCE factors in three paid AND3 steps, with the final step annotated by a three-edge affine row. At vertex 0 use **String** \`support:"102"\` for final AND3 \`d2\`; at vertex 9 use **String** \`support:"123"\` for final AND3 \`d29\`. The checker's JS \`String.includes(Number)\` tests permit numeric parent support sets [0,1,10] and [2,3,12], respectively, while its \`support[i]\` indexing iterates characters and writes edge bits [1,0,2] and [1,2,3]. It **never assigns** actual edge bits 10 or 12 during local table/row tests. The two real 2-bit relations therefore pass the checker's false **3-bit** affine annotation tests on shadow slices. XOR the twelve purported vertex rows in eleven paid GF(2) steps to create an operational terminal \`0=1\`.

Distinct paid records: \(3(12)+(12-1)=47\), with chronological references, a complete shared ancestor cone containing all 48 SOURCE IDs, and 48 valid deletion witnesses. The checker returns \`allEssential:true\`, \`bridgeless:true\`, and \`certifiedMinimum:47\` although the source is SAT. These fields certify properties of a defective accepted *fixture program*, **not** of a mathematically sound proof system.

## Executed controls and exact evidence

- Original checker blob: \`fcb7d4ced8f922de14c0bda16263a8cc7853e8e0\`, unchanged mathematical implementation in hosted V8 with only virtual \`fs.readFileSync\`, \`process.argv\` and \`console\` adapters.
- Original checker: one **ACCEPT**, **5,583 assertion groups**. Its own five built-in corruption tests also reject as part of this count.
- Nine separately generated hostile packets: **9 REJECT**. They individually repair the two String charges, repair the two String supports, corrupt a parent ID, corrupt the GF(2) terminal, corrupt an original deletion witness, corrupt a signed SOURCE literal or corrupt the even-parity witness.
- Exact source: \(V=12\), \(E=18\), \(m=48\), \(W_{\rm record}=47\), \(|\operatorname{SAT}(F)|=64\), all 48 essential, 16 deletion models per clause.
- External OS Node driver was published and syntax-validated by hosted JS parsing, **but was not executed by an operating-system Node process in this run**. The independent Python rank audit was executed locally using standard Python, and graph connectivity was separately checked. No repository-wide preflight or LaTeX compile was completed.

Reproduction and immutable raw evidence:

1. \`experiments/arc/lspv1_619_bridgeless_dual_exception.cjs\`: deterministic generator, 2^18 Boolean enumeration, full OS-subprocess driver pinned to original blob, all nine adversarial inputs.
2. \`experiments/arc/lspv1_619_independent_rank.py\`: independent exact graph, GF(2) rank and 48 deletion-control verifier, no nonstandard dependencies.
3. \`results/raw/arc/2026-11-13_0600_LSPV1_619_BRIDGELESS_SAT_ACCEPTED.json\`: complete 10,113-byte JSON+LF accepted fixture.
4. \`results/raw/arc/2026-11-13_0600_LSPV1_619_BRIDGELESS_DUAL_EXCEPTION_HOSTED_RAW.json\`: original-checker V8 decisions, errors, proof metrics and charge/support details.
5. \`results/raw/arc/2026-11-13_0600_LSPV1_619_BRIDGELESS_RANK_RAW.json\`: independent source-rank audit summary.

To execute from a repository checkout, run \`node experiments/arc/lspv1_619_bridgeless_dual_exception.cjs\` and \`python3 experiments/arc/lspv1_619_independent_rank.py\`. The Node runner refuses to operate if the original checker Git blob has changed.

## Exact main-chain implication and non-implications

**[P2-D1] OPEN.** The new native accepted-byte certificate materially **falsifies** any proposal that merely imposing bridgelessness and checking all SOURCE deletion witnesses is enough to make the recovered /341 checker source-sound **without charge typing**. It does not refute the LSPV-1/618 theorem, which assumes at most one exceptional charge; this witness shows its charge-count threshold is **sharp** among checker-accepted bridgeless cases.

**[P2-C3] OPEN.** Any MAY abstraction of this actual recovered checker must retain the two String-charge and two String-support semantics. It must distinguish "operationally checker-accepted" from "mathematically UNSAT". A CEGAR replay that accepts this path cannot label it spurious merely because its source is satisfiable. The complete full-rule historical transition system, alpha/gamma, once-paid node ledger, assumptions/contexts/discharge and full fixed weights remain missing.

**[P2-B1] OPEN.** The checked field \`certifiedMinimum:47\` is **not** an authenticated minimum-work refutation of this SAT source and says nothing about unrestricted optimal shared-DAG refutation cost, including all GF(2), Resolution, DEF, LOCAL-CONVERT, branching, learning, sharing and compact algebraic shortcuts.

**[P2-B2/B3] OPEN separately.** No same-calculus polynomial-work transfer follows. P1-01, P1-03 and P1-04 remain OPEN. Logical paid record count 47, original evidence bits 10,113, actual proof discovery, wall-clock time, verification probes, span and peak space are separate metrics. No oracle, answer table, source substitution or silent model switch is used.

**TRACKERS REVIEWED; NO MATERIAL ROOT-STATUS CHANGE.** \`proof1.txt\` and \`proof2.txt\` remain OPEN. Historical 2 Route A / 3 Route B roles, titles, Pacific hourly schedules, original rule weights and manuscript ownership boundaries remain unchanged. LSPV-5 independent hostile replay is requested.

**Next decisive target:** recover an externally original-source-bound, authoritative **single** historical checker recognizing genuine RES-to-AND3 or paid DEF-to-LOCAL-CONVERT plus discharge. The present recovered sibling checker cannot serve as that authority.

**P versus NP remains OPEN.**

# LSPV-2/447: Exact semantic charge-syndrome quotient for shared Tseitin SAT queries

**2026-11-06 09:17 PST. Route A primary. KNOWN graph algebra + PROVED/RESTRICTED future-query memory theorem + COMPUTATIONAL finite controls. P vs NP OPEN.**

## IDEA -> SEARCH -> ITERATE and 4 falsifiers

Hypothesis: prior /437 and /446 parent-scale charge arrays retain much more than the information necessary to answer later SAT questions after arbitrary vertex-charge edits. For a fixed authenticated graph, the sufficient semantic summary is one XOR parity bit **per connected component**.

Falsifiers: F1, global charge parity falsely classifies disconnected inputs; F2, two distinct component syndromes might have identical answers to *all* future edit queries; F3, a claimed space bound hides retained original input or head location; F4, graph recognition, connectivity, child production or guest execution is silently free. **F1 and F4 are real restrictions; F2 is ruled out by the exact distinguishability theorem; F3 is excluded in the sealed-source protocol, not in unrestricted random access.**

## Published hard family and exact strict 3-CNF

Let G=(V,E) be simple cubic with H vertices and M=3H/2 edges. A source edge e has Boolean variable x_e. Charge vector chi is in GF(2)^H. For each vertex v with incident edge IDs a<b<c let l_0(x)=x and l_1(x)=not x. Its **four original proper width-three clauses**, indexed by p,q in {0,1}, are

$$
C_{v,p,q}=l_p(x_a)\\lor l_q(x_b)\\lor l_{p\\oplus q\\oplus1\\oplus\\chi_v}(x_c).
$$

The clauses exactly enforce x_a XOR x_b XOR x_c=chi_v. Thus there are 4H clauses and 12H signed occurrences. With fixed-width variable IDs of w=ceil(log2(M+1)), the signed original source body requires 12H(w+1) bits. Earlier LSPV-2/438 and /446 add an explicit graph/charge source header of O(H log H) bits. N=Theta(H log H). The local reproducibility archive uses uncompressed ASCII DIMACS and records byte-exact hashes separately. Never mistake it for the older packed packet.

For growing constant-degree **expander** graphs and odd charge, Urquhart (JACM 1987) and Ben-Sasson/Wigderson (JACM 2001) establish exponential lower bounds for **ordinary shared-DAG Resolution**, not general SAT machines, full mixed R_mix341, ER, or GF(2). No unverified finite graph here is claimed as asymptotically hard. The family is native strict 3-CNF, with no conversion overhead.

## Theorem 447.1: exact graph-component syndrome (KNOWN algebra; fully proved at this scope)

Let the graph have c connected components K_1,...,K_c, and write sigma(chi)_i = XOR_{v in K_i} chi_v. The vertex-edge incidence matrix B has image equal to ker(sigma): each edge contributes twice to its component parity; conversely, a spanning forest solves every prescribed even-parity component charge by assigning tree edges successively. Therefore

$$
SAT(F_{G,chi}) \\iff sigma(chi)=0,\\qquad rank(B)=H-c.
$$

Every satisfiable charge vector has exactly 2^(M-H+c) satisfying assignments on original edge variables. After a future charge toggle vector u,

$$
SAT(F_{G,chi XOR u}) \\iff sigma(chi)=sigma(u).
$$

This **exactly preserves the original signed clauses' SAT label**. For a connected graph c=1, even if ordinary Resolution is exponentially hard, a parity algorithm gives a one-bit semantic shortcut, with graph authentication charged.

## Theorem 447.2: tight c-bit future-query state floor (PROVED/RESTRICTED)

Fix G and publicly known component indices. A deterministic preprocessor sees the original chi, then loses ALL further access to its charge bits; no charge-dependent cached data or head position is uncharged. It must answer SAT after **every possible future subset of vertex toggles**, queries possibly adaptive.

For every syndrome s in {0,1}^c choose chi with a single charged representative vertex in each component where s_i=1. For each z in {0,1}^c choose a future query toggling exactly those representatives for which z_i=1. The query answer is **f_s(z)=[s=z]**. Distinct s induce pairwise different functions, so a deterministic preprocessor must retain >=2^c distinguishable states, requiring **at least c bits**. The stored syndrome reaches the bound. QED.

This is NOT a lower bound for one SAT query, or when original charges can be reread. It is NOT a SAT decision-time or proof-complexity lower bound. For disjoint K4 components, c=Theta(N/log N), so a one-pass permanent future-query summary can exceed the proposed sqrt(N) memory, whereas a connected graph only needs one parity bit.

## Strongest shortcut and all-phase accounting

When source graph G is read-only and independently authenticated, components can instead be found on demand in deterministic **logarithmic space** using Reingold's undirected-connectivity theorem (JACM 2008). Loop over each minimum-ID component representative and XOR charges of its connected vertices, using O(log N) writable space, but H^2 connectivity calls and unspecified polynomial time. Source and edit rescanning, index-head manipulation, constructing/validating graph input, parsing every original signed clause, and correctness on nonfamily or malformed inputs remain charged. This does **not** prove the historical FLMV N^(11/10) time limit or a universal A->Phi(A). No children were constructed. Materialized child formula bits and child guest calls are zero in this experiment, not free placeholders.

The full machine requirements remain

$$
t'\\le\\max\\{11/10,3/5+t/2\\},\\qquad
s'\\le\\max\\{1/2,s/2\\},
$$

with all-phase peak s'<=max(rho,eta,lambda,lambda*s). The argument says **nothing** about R_mix341 proof-DAG node minimum or B3; those belong to Route B and remain OPEN.

## Independent finite tests and hostile controls

Local archival producer `lspv2_447_component_syndrome.py` enumerated **every edge assignment** on five cubic graphs and checked every charge vector against the exact syndrome image: K4 (H=4), cube (8), Petersen (10), K4+K4 (8), 3xK4 (12). **5,648 distinct charge patterns, 5,740 future-query checks, 686 corrupted original clause-packets rejected**. An independently authored Node verifier rebuilt the graph and signed local 3-CNF gadgets, independently enumerated assignments and cross-checked the raw JSON: **6,531 assertions PASS**. The two-component control with one odd charge in each component is globally even but **UNSAT**, refuting the incorrect one-global-parity shortcut.

These are finite host-language checks, NOT native FLMV transitions, proof-size certificates or tests of an arbitrary SAT decider. The complete executed Python code, independent JS, exact fixture metadata, raw JSON and SHA-256 manifest are in the separately prepared local archive.

## Actual source reconciliation

Read live issue #3, historical handoff at commit 4e29ed7646f484707767acb6e63ec5f38afd98a8, AGENTS.md, CODEX.md, project skill, and LSPV-2/446 handoff blob 5f429e9f99c4bf45ae6e469deb76b71ffa3042c2. Peers: LSPV-4/438 (expander giant-core deletion), /442 (UP containment), /443 (ETH small-oracle no-go); LSPV-1/452 (declared-R semantic GF(2) compiler); LSPV-3/454 (strict-3 certificate); Grok GROKPROOF/2026-11-06_1617_PROGRESS.md; Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex. Earlier /440 already noticed disconnected parity failure. This work states an exact future-edit quotient instead of claiming new discovery of the parity invariant.

Both required external repos examined: konard/p-vs-np README.md and scripts/proof_status.json (limited formal scope); blkph0x/p-vs-np-proof-research METHOD_INDEX.md and INDEPENDENT_AUDIT.md (conditional native-region prerequisites). Also inspected CNFgen cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab and openai/math directory. No external build or correctness claim was inferred from a badge. Primary papers: FLMV, JACM 52(6):835-865 (2005), doi:10.1145/1101821.1101822; Urquhart, JACM 34(1):209-219 (1987); Ben-Sasson/Wigderson JACM 48(2):149-169 (2001); Reingold, JACM 55(4) (2008), doi:10.1145/1391289.1391291. No separately branded Google search was used; the available web index was searched.

**OPEN:** No universal solver-dependent, all-input, recursively iterable, both-label/malformed-aware same-machine FLMV contraction. No B3 or P vs NP proof. Existing 2 Route A / 3 Route B allocation, historical weights, schedules and root main.tex unchanged.
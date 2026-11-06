# LSPV-2/442: unordered, variable-renamed, original-source cubic Tseitin recognition

**2026-11-06 04:55 PST | Route A primary | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## IDEA, falsifiers, and duplication audit
Hypothesis: LSPV-2/441's no-annotation logspace recognizer extends beyond its *canonical quartet ordering and special edge-ID convention* to all strict DIMACS presentations formed by arbitrary clause order, within-clause literal permutation, and injective variable-ID renaming of a cubic Tseitin original 3-CNF. Falsifiers: (1) shuffled legitimate quartet rejected; (2) forged parity quartet or duplicated edge accepted; (3) disconnected graph with two odd components and globally even charge falsely declared SAT; (4) proposed graph construction secretly materializes an O(N)-space dictionary.

Before claiming novelty, read issue #3 through **LSPV-2/441 at 04:16 PST**, LSPV-4/437 and LSPV-1/446. An initial fixed-packet experiment in this run duplicated **already proved LSPV-2/441**, so it was retired as a new claim. LSPV-2/422 already established compact affine boundary messages and expander separator costs; those are not re-claimed. Also read Nov. 2 governing handoff, AGENTS.md, CODEX.md, pnp skill, LSPV-2/440, Grok 2026-11-06_0920, Claude TPORT-0002, konard/p-vs-np/proofs/complexity/README.md (different one-tape model), blkph0x/p-vs-np-proof-research/METHOD_INDEX.md and CERTIFIED_RESIDUAL_QUOTIENT_REPORT.md (incomplete classifier), cnfgen/families/tseitin.py (original generator), FRAT-XOR/format.md (different proof rules), and openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (fixed-driver costs only). Indexed web rather than branded Google search was available.

## Exact family, published bound, proof model
Let G be a finite simple cubic graph on even H vertices, with 3H/2 edges and a charge vector chi. Each vertex contributes the four *original proper signed 3-clauses* that exclude assignments of its three incident edge bits with XOR unequal to chi_v:

$$
F_{G,\chi}=\bigwedge_{v}\bigwedge_{a\in\{0,1\}^{E(v)}:\oplus a\ne\chi_v}
\left(\bigvee_{e\in E(v)}\ell_{e,a_e}\right),\quad
\ell_{e,0}=x_e,\;\ell_{e,1}=\neg x_e.
$$

Exactly 4H clauses; 3H/2 used variables. In ordinary polynomial-length edge-ID naming, N=Theta(H log H) encoded bits. Arbitrarily huge IDs enlarge N and must be charged, not silently treated as H. Suitable odd-charge connected cubic *expander* sequences have Resolution proof size exp(Omega(H)) against unrestricted shared-DAG **binary Resolution**, per Urquhart (JACM 1987, DOI 10.1145/7531.8928) and Ben-Sasson–Wigderson (JACM 2001, DOI 10.1145/375827.375835). These are restricted proof-size lower bounds, not arbitrary-algorithm SAT lower bounds or a theorem about the full mixed R_mix341 calculus. Clause reordering and variable renaming preserve the native Resolution DAG size by isomorphism. Cook ER and GF(2) parity shortcuts are mandatory upper-bound controls.

## Theorem 442.1 (PROVED/RESTRICTED)
There is a deterministic logspace, polynomial-time, no-supplied-annotation recognizer for the stated graph family in **arbitrarily ordered strict DIMACS 3-CNF**, invariant under injective variable renaming, including extremely long variable tokens. It can report SAT or UNSAT correctly for recognized instances, OUTSIDE for well-formed sources not recognized, and BAD_FORMAT for malformed source grammar.

*Proof.* Treat each original three-literal clause as a triple of unsigned variable-token substrings. Sort the three names through repeated indexed input comparisons (not stored integer names); reject repeated support. Enumerate only the first clause in source order of each distinct support, and for each representative rescan *all* original clauses. Collect an 8-bit mask of negation patterns after matching and ordering each triple. Require **exactly four distinct masks, all even or all odd parity**. Forbidden-mask parity p gives vertex charge 1-p. Require each variable-token name to occur in exactly two distinct support groups. Reject two groups sharing more than one variable, yielding a simple cubic graph. Index vertices by the source-position rank of representative supports. A neighbor query is logspace-computable through repeated support scans. Applying Reingold's deterministic logspace undirected reachability (JACM 2008, DOI 10.1145/1391289.1391291) to that implicit graph, loop over component-minimum vertices and XOR their component charges. All state consists of O(log N) source offsets, counters and a constant-size sign mask, and logspace-computable reachability composed with the input decoder. The entire algorithm has polynomial but **not certified near-linear** time. No full adjacency array or annotation is materialized on machine work tape. QED.

## Theorem 442.2 (KNOWN algebraic upper-bound control)
For arbitrary finite G, including disconnected G,

$$
\operatorname{SAT}(F_{G,\chi})\iff
\forall C\in\operatorname{Comp}(G):\bigoplus_{v\in C}\chi_v=0.
$$

Each component incidence matrix has rank |C|-1 over GF(2). The condition is necessary by summing all vertex equations, sufficient by column-space characterization. **Hostile falsifier:** two disjoint K4 components each with one odd charge are UNSAT although global XOR of all charges is zero. This is a validation control, not a newly invented hard family.

## Experimental verification (COMPUTATIONAL)
The Python producer (seed 442) generated **72** original strict-DIMACS sources from K4, cube, Petersen, Heawood, bridged K4 and disconnected two-K4, with randomized clause/literal order, arbitrary sparse injective variable renaming and some **1025-bit variable IDs**, 30 SAT and 42 UNSAT. It rejected **48** malformed-header/duplicate-clause controls; final producer had **123 assertions**. Separately written JavaScript verification performed **434 assertions**: exact original clause-multiset reconstruction from the edge graph, SHA-256 source verification, independent GF(2) Gaussian elimination, corruption rejection, and disconnected globally-even UNSAT. An initial independent elimination implementation bug was found and fixed before final replay. Host Python/Node scripts materialize source and graph objects; **neither is an execution of the native FLMV logspace machine or historical R_mix341 checker**. Full 947KB raw source ledger, executed Python producer, executed independent JavaScript verifier, logs and integrity manifest are in the local reproducibility archive, SHA-256 of raw JSON: `07bf11d199d7655bffbee7b4497293144a4c417b55bbd30f21a5b859adce2430`.

## Resource and transfer firewall
The abstract recognizer's work-tape peak is O(log N); read-only original-source bytes count toward N. Its repeated scans, indexed input operations, token comparisons, component queries, and head/index erasures give time N^{O(1)} of unspecified exponent. Externally materializing graph or original-source copies incurs their full bit length. It does NOT establish the needed local N^{11/10+o(1)} time, recursively smaller SAT children, all-input correct join, arbitrary guest-program speed-up, or same-machine all-input FLMV contraction. An OUTSIDE source must be passed to a fully charged, total general SAT/malformed-input path. No R_mix341 inference, weighted shared DAG, branch discharge, B3 proof or universal machine lower bound is inferred. Preserve the existing two Route A/three Route B allocation and historical weights. Root main.tex could not be safely updated: a nonempty SHA returned an empty readable file body; do not overwrite it.

**Advance:** exact original-source recognition under arbitrary ordering/variable renaming without auxiliary graph annotation; verified independent finite controls. **OPEN:** near-linear charged recognizer, universal A→Phi(A), unrestricted mixed lower bound, B3 and P versus NP.

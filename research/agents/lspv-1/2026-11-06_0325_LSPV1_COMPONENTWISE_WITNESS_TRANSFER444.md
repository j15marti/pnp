# LSPV-1/444: Componentwise cubic-Tseitin witness transfer and the disconnected-charge falsifier

**November 6, 2026, 03:25 PST | Route B lead | PROVED/RESTRICTED, with COMPUTATIONAL finite controls.** Historical R_mix341, five-role 2A/3B allocation, native rules, schedules and weights unchanged. B1/B2/B3, full mixed superpolynomial lower bounds and P versus NP **OPEN**.

## IDEA -> SEARCH -> ITERATE

**Hypothesis.** Extend prior LSPV-1/443's *connected* cubic-Tseitin syntactic SAT-preserving map to disconnected graph components, with explicit polynomial-time witnesses translated **in both directions**, a true strict-resolution certificate, and source-level verification.

Four falsifiers: (F1) global even charge suffices on disconnected cubic graphs; (F2) recovering a source witness from a target model needs an SAT solver; (F3) componentwise source-target overhead or target strict-Resolution work is superlinear; (F4) malformed, nonfamily, sparse IDs, source mutations, corrupt pivots or root are accepted. F1 was disproved by two odd-charge K4 components, while F2-F4 have constructive repairs and finite checked controls.

Prior/443 already established the connected hard-to-easy transformation; the parity-chain idea and strict-RES suffix are not new. New focus is the **exact componentwise extension, two constructive witness translators and disconnected falsifier**. No independent academic originality claim.

## Known hard family and controls

For any simple cubic graph G=(V,E) of h vertices and c components, introduce one original edge variable x_e per e, with |E|=3h/2. At each vertex v of degree 3 choose a charge chi_v and include precisely four signed width-three source clauses, each excluding one local assignment with wrong XOR parity. Hence the original F_(G,chi) has 4h proper ternary clauses and indexed input length Theta(h log(h+2)). The connected odd-charge case is UNSAT. On appropriate cubic *expander* sequences, Urquhart (1987) and Ben-Sasson/Wigderson (2001) establish 2^{Omega(h)} size for **unrestricted shared-DAG ordinary Resolution**. This is certified proof-size hardness in that named system, not hardness for all algorithms.

Mandatory upper controls: in declared original-coordinate historical R_mix341, the established bridgeless cubic original has exact 4h-1 paid AND3/XOR proof work (LSPV-2/341). For its guarded strict-3CNF version, LSPV-1/436 and independent LSPV-5/REFEREE383 give a *rule-level* 12h+2 RES/AND3/XOR upper proof, not accepted-byte checker certification. Haken's unary PHP is Resolution-hard but has Cook's polynomial Extended-Resolution shortcut. Braun's bit-PHP Res(XOR) 2026 preprint uses a different calculus and wider source CNF; no proof-size or 3CNF transfer is inferred.

## Theorem 444.1 (componentwise syntactic reduction)

Recognize only an exact signed-cubic Tseitin syntax: group clauses by unordered support triples; require all four wrong-parity signed clauses for each vertex, each variable in exactly two vertex supports, and a simple cubic incidence graph, allowing c >= 1 connected components. This recognition is deterministic polynomial in the encoded input length and requires no SAT oracle. Malformed DIMACS is rejected distinctly; every other valid CNF is returned unchanged. Reindex recognized output variables compactly.

For each original vertex, force a fresh charge bit c_v = chi_v. Within each connected component of k vertices, add k-1 two-input XOR gates computing the XOR of its charge bits; require the output to be zero. Encode each XOR gate by its four exact width-three clauses. Encode each of the h+c forced input/output units by four signed width-three padding clauses using two fresh private variables.

The output H has exactly

$$
m(H)=4(h-c)+4(h+c)=8h,\qquad
n(H)=h+(h-c)+2(h+c)=4h+c.
$$

Over the original binary incidence matrix B, rank(B)=h-c. Its system Bx=chi is feasible **iff each component's total chi charge is even**, which is exactly the feasibility condition for the target's separately forced XOR chains. Consequently

$$
F_{G,chi} \in SAT \quad\Longleftrightarrow\quad H_{G,chi}\in SAT.
$$

**Forward witness map.** Given a satisfying assignment for the original edges, set each charge bit to chi_v, calculate its component's XOR chain and set every padding bit to 0.

**Reverse witness map.** Given any satisfying target model, find a rooted spanning forest in G. Set all non-tree original edges to 0; for each nonroot vertex v, set its parent edge to the XOR of charges in the rooted subtree at v. The parity at each nonroot vertex is chi_v by cancellation, and the root equation is satisfied by the even component charge. This yields an original-edge satisfying assignment with no search oracle. Both mappings are polynomial-time; on valid nonfamily CNF use identity witness maps.

An important caveat: these maps translate satisfying witnesses and therefore say nothing by themselves about negative-instance refutation certificates. On an UNSAT input the witness translations are vacuous. Proof-size lower-bound preservation still needs a **reverse proof simulation**.

## Theorem 444.2 (explicit strict Resolution target upper bound)

If a component has odd total charge and size k, its target has an original-target-source-authenticated strict binary-Resolution refutation with exactly

$$
3(k+1)+2(k-1)+1=5k+2
$$

**distinct paid RES inference nodes**. Recover k forced input units and one output unit from their four padding clauses in 3 oriented RES operations each; propagate each XOR gate's forced output using two RES nodes and the genuine gate clause; resolve conflicting final units in one RES. Every premise and pivot is source-labelled. This is an **upper witness, not an exact global minimum**. With several odd components choose the smallest.

**Disconnected falsifier:** disjoint union of two K4 graphs, each charged oddly, has **even total charge but is UNSAT**. A single global charge chain incorrectly yields SAT. The repaired target has one charge chain *per component*, preserving the UNSAT label.

For *connected* suitable original odd cubic expanders with 2^{Omega(h)} ordinary Resolution minimum, the syntactically reduced target has 5h+2 strict-Resolution work, even though both directions of satisfying-witness translation are polynomial. Consequently **SAT equivalence plus bidirectional efficiently computable positive witnesses does not imply Resolution proof-size hardness transfer**. This is a precisely qualified transfer falsifier, not a lower bound on R_mix341 or on all SAT algorithms.

## Reproducibility and hostile controls

Two Python producers and two separately implemented Node verifiers checked 20 exact source/target packets. Connected graph controls: K4, K3,3, cube and prism6, with four charge patterns each, 16 packets; even-charge source model counts respectively 8, 16, 32 and 128. Disconnected controls: two K4 components under even/even, even/odd, odd/even and odd/odd charge, four packets; output has 64 original ternary clauses and 34 variables. Every odd component proof has 22 paid nodes. The even/even original has 64 models; odd/odd is UNSAT despite globally even charge. Across experiments: 240 Python assertion groups, 2,009 independently checked JavaScript assertions and 33 rejected malformed/corrupted controls; no failures. The local ZIP contains all 20 exact packets, source SHA-256 hashes, complete Python producer, independent verifier code, raw records and checksum manifest. No historical authoritative mixed-certificate byte checker was executed; finite witnesses do not prove minimum cost.

Actual machine costs are separate from logical nodes: all source/index reads, parsing, recognition, graph DFS, construction, output and certificate bytes, verifier time, hash and pointer work, cache/retrieval/recomputation, failed policy checks and peak simultaneous space are additionally charged. These programs run in polynomial time/space relative to the actual input encoding. Measured host execution times were under a few seconds and RSS approximately 97 MiB for Python producers, 32 MiB for Node verifiers. No FLMV same-machine exponent is inferred; materialized-child peak bound retains s' <= max(rho,eta,lambda,lambda*s), including transient preprocessing in rho.

## Sources and publication boundary

Current issue #3 and governing historical handoff at commit 4e29ed7646f484707767acb6e63ec5f38afd98a8 were read. Historical exact grammar: `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob c87acd11. Previously known connected transform: `research/agents/lspv-1/2026-11-06_0300_LSPV1_TSEITIN_SYNTAX_ERASURE443.md`, blob 8e2d7e4. Independent guarded native shortcut: `research/main/2026-11-06_0248_MAIN_ORIGINAL_COORDINATE_RECOVERY_REPLAY_REFEREE383.md`, blob d15f283. Peer /444 prefix type blocker, LSPV-3/427 branch source lifting and REFEREE367 context DAG checks were reviewed. Actual Grok 2026-11-06 09:20 UTC and Claude 2026-10-28 ONETAPE reports were read. AGENTS.md, CODEX.md and repo pnp-research skill were reviewed. Local preflight could not run without a checkout; root main.tex was not modified.

Required change-aware external checks: konard/p-vs-np head ecedd2b45f1c524d85c00b2da27a9c140025550c (proof-status JSON); blkph0x/p-vs-np-proof-research head 7dedc73f758dfbdc072e7aa29dfc08505761ebd5 (METHOD_INDEX.md), both unchanged. Also reviewed meelgroup/frat-xor/format.md, peitl/short-proof README and openai/math's concrete SAT node-cost Lean file. No native byte grammar or B3 theorem located. Primary literature checked: Urquhart JACM 1987 DOI 10.1145/7531.8928; Ben-Sasson/Wigderson JACM 2001 DOI 10.1145/375827.375835; Haken TCS 1985; Cook SIGACT News 1976; Braun arXiv:2609.23015; Pang arXiv:2610.00837. Indexed web search used; Google-branded access unavailable.

## Precise remaining arrows

(i) Find a **genuinely superpolynomial** worst-case lower bound on the global minimum across every *legal fixed* R_mix341 RES/AND3/GF(2)/LOCAL/DEF shared DAG, accounting for all shortcuts; (ii) prove noncircular same-calculus

$$
SAT\in P \implies \overline W_{R_{mix341}}(N)=N^{O(1)},
$$

without assuming short UNSAT certificates, correctness reflection or an oracle. B1/B2/B3 and P versus NP remain **OPEN**.

# TMR-4/054: A sharing-safe circuit-signal hypercut gives an exact rank factorization and a charged #Circuit-SAT algorithm

**2026-11-15 14:55 PST | TMR-4, PNP Cost-Sound Abstraction | Tracks A/C.**
**Scientific status: PROVED/EXACT for the stated circuit-representation lemmas; COMPUTATIONAL for finite tests; independent mathematics review OPEN. Unrestricted SAT-machine transfer OPEN. P versus NP OPEN.**

## 1. Precommitted candidate and falsifiers

**SCUT054.** For every finite acyclic Boolean circuit with explicitly named n inputs, fan-in at most two, any amount of sharing/fanout, and one designated Boolean output, and for every FIXED disjoint partition X:Y of its n inputs, one can find in polynomial time a bipartition of the input and gate nodes minimizing the number r of distinct crossing *signal identities*. The output assignment matrix satisfies rank_K(M_f) <= 2^r over EVERY field K. Moreover, the same cut yields a uniform exact #Circuit-SAT algorithm with total bit-time poly(L) times 2^r(2^|X|+2^|Y|), including cut discovery and exact arithmetic, and polynomial writable space. Here L is the explicit circuit encoding length; r is circuit-dependent and not an intrinsic lower-bound measure for arbitrary algorithms.

**Falsifiers fixed before the proof and computation:** (F1) DISJ_k has rank 2^k and a linear-size depth-two circuit, so any superpolynomial-circuit inference must fail; (F2) affine inner-product and equality have tiny algebraic descriptions and must not be labeled SAT-hard; (F3) one shared gate signal fanning out to many opposite-side consumers must be charged ONCE, not one per use, while the factorization remains exact; (F4) eliminating existential selector or auxiliary wire variables can collapse slice ranks, so the theorem must concern the actual function and a declared circuit, not a mandatory solver materialization.

The purpose is a restricted, costed *positive simulation/representation* bridge after TMR-4/051-053. It is NOT a circuit-size lower bound for SAT, a proof of a hard formula, or a claim of novelty relative to communication-complexity and separator methods.

## 2. Precise objects and signal capacity

A circuit C is an acyclic list of n named input nodes and g gate nodes, with a topological ordering. Gate operations may be AND, OR, XOR, NOT (or any fixed Boolean finite-arity gate). Each gate output and each original input is ONE signal identity, regardless of how often consumers reread or fan it out. Let V=n+g; there are w declared gate-input occurrences and L=Omega(n+g+w) encoded bits (ordinary binary indices need O(log V) bits).

Fix input sides: all x in X must lie in the left node set S and all y in Y in the right node set. Every internal gate may be assigned either side, including the output gate. For each signal driver v, define its hyperedge H_v as v together with ALL gate nodes that consume v (deduplicate repeated references). Define

$$
r(S)=|\{v: H_v\cap S\ne\varnothing,\ H_v\setminus S\ne\varnothing\}|,\qquad
r^*(C;X:Y)=\min_{S:X\subseteq S,\;Y\cap S=\varnothing} r(S).
$$

Each hyperedge is charged once, even when its signal has many sinks, because one boundary bit z_v is sufficient for all its remote consumers. Every cross-boundary signal may have either orientation and multiple remote consumers. The entire explicit circuit and its sharing remain intact. This quantity is a cut of a *specified circuit*, not a minimum over all equivalent circuits or solver representations.

## 3. Exact mincut construction, no free partition discovery

For each signal-hyperedge H_v create two gadget vertices a_v,b_v with the one unit-capacity directed arc a_v -> b_v. For each node u in H_v add arcs u -> a_v and b_v -> u of capacity INF=V+2. Attach source s to all X inputs and all Y inputs to sink t using INF arcs. Let original circuit nodes be freely placed by the cut. A cut of capacity <INF cannot violate a terminal assignment. For each split H_v, some left vertex forces a_v left and some right vertex forces b_v right, necessarily crossing the unit arc. For a monochromatic H_v both auxiliaries can be placed together on that side at zero cost. Therefore the minimum s-t cut capacity equals r^*(C;X:Y) EXACTLY.

This builds O(V) gadget vertices and O(V+w) arcs and has a standard uniform polynomial-time maxflow solution. The returned residual partition supplies the concrete side assignment and the exact crossing-signal list. In the executed Python implementation each gadget uses one unit arc and directed large-capacity incidence arcs; a residual mincut is checked against brute-force placement of every internal gate whenever g<=10. A higher-level strategy may choose multiple original-variable partitions adaptively, but its search/repeated maxflows must be separately charged. In this run the canonical balanced X:Y partition is fixed and declared before the cut.

## 4. Sharing-safe factorization lemma and proof

Fix ANY legal node partition S and let Z be its r crossing signal identities. For each bit assignment z in {0,1}^r, define A_z(x) as the indicator that ALL left-side gate equations, local input equations, boundary-signal equalities z_v=value(v) for left-owned crossing signals, and (if left-owned) the output=1 requirement hold. Define B_z(y) analogously for right-side gate equations and output. Every incoming crossing signal is treated as the corresponding declared z_v rather than an unrestricted oracle.

**THEOREM (restricted, exact):**

$$
f(x,y)=\sum_{z\in\{0,1\}^r}A_z(x)B_z(y)
\quad\text{as an equality of nonnegative INTEGERS,}
$$

$$
M_f=\sum_z a_zb_z^T,\qquad
\operatorname{rank}_K(M_f)\le 2^r
\quad\text{for EVERY field }K,
$$

and

$$
\#C=\sum_z\left(\sum_x A_z(x)\right)
                 \left(\sum_y B_z(y)\right).
$$

**Proof.** Each local gate checks its Boolean truth-table equation using either a locally owned predecessor signal or the matching boundary bit z_v. These constraints separate completely into an x,z relation and a y,z relation. For any fixed x,y, acyclicity and deterministic gates give one and only one valuation of EVERY signal. Its restriction to Z satisfies both local systems, and satisfies the appropriate output=1 equation exactly when f(x,y)=1. No other z can satisfy both: all local gate and input equations together constitute the FULL original circuit's deterministic defining equations. Hence the integer sum is exactly 0 or 1. Over any field reduce that integer identity into K and use subadditivity of matrix rank, since each outer product has rank at most one. Sum the integer identity over x,y for the counting formula. QED.

The proof does not assume syntactic disjointness of the gate sets, nor unfold shared nodes into a tree. One crossing signal can feed any number of opposite-side consumers; all consume the SAME z_v. It also does not assume an unknown exponential matrix is materialized by a circuit evaluator.

## 5. Uniform exact counting algorithm and fully charged ledger

Set a=|X|, b=|Y|, r=r^*(C;X:Y). Read/validate C, construct and solve the polynomial-size auxiliary flow network, retain the selected side and crossing list, then enumerate each of the 2^r boundary strings. For each z, enumerate all 2^a local X assignments and all 2^b local Y assignments, evaluate local gates in topological order with incoming z values, compute exact integer counts Acount_z and Bcount_z, multiply and accumulate. Output the (n+1)-bit exact integer #C.

On a fixed-bit alphabet multitape implementation, using the original explicit binary source as input and ordinary bit arithmetic, the SAME algorithm has conservative bounds

$$
T(C)\le \mathrm{poly}(L)\bigl(1+2^r(2^a+2^b)\bigr),\qquad
S(C)\le\mathrm{poly}(L+n).
$$

There is no unbounded-word unit-cost assumption: gate addresses need O(log V) bits; each local count has <=n+1 bits; products and the total count have <=n+1 significant bits (partial sums are nonnegative and at most total #C<=2^n); maxflow capacities are <=V+2; all source reads, parsing, graph storage, directed arcs, queue/work arrays, cut verification, gate evaluation, integer multiplication and output writing are included in polynomial overhead. No same-machine strict FLMV bounds are claimed, and the algorithm is not polynomial in n when r or the larger input side is linear.

For a balanced canonical split a=floor(n/2), b=ceil(n/2), this gives T<=poly(L) 2^{r+ceil(n/2)} (up to a constant factor), and a genuine 2^{o(n)}-factor saving compared with brute force ONLY when r <= (1/2-epsilon)n for a fixed epsilon>0. If r=O(log n), runtime is O*(2^{ceil(n/2)}). A finding algorithm for a better variable partition, a new equivalent circuit, or a more efficient #SAT compression is NOT free or included. A large r provides NO lower bound because any alternate algebraic algorithm can bypass this procedure.

**No hidden direction reversal:** this establishes a cheap algorithm from a small explicit *circuit cut*. It does NOT prove that all cheap algorithms induce small cuts, nor that a circuit with large r requires much time.

## 6. Falsification controls and finite reproduction

Deterministic CPython 3.13.5, standard library only, revision tmr4-signalcut054.v1, seed 202611151452, GF(2) and GF(65521), 97 circuits, **576 explicitly counted assertions and 0 failures**. Every case tested mincut capacity versus its returned physical crossing identities, exact full assignment matrix factorization entrywise, exact integer #SAT agreement, field ranks <=2^r, and (g<=10) exhaustive brute-force optimal gate placements. The 96 generic/family circuits consist of 16 named DISJ/EQ/IP/separable examples with k=1..4 and 80 seeded topological shared circuits with 4 inputs and 1..7 gates; an additional REUSE circuit tests repeated fanout. The code reconstitutes the full 26,639-byte deterministic JSON raw evidence. The published immutable zlib/base64 file contains those exact bytes; SHA-256 uncompressed 816772fab25302b7cb5469f6d6ccb92586b149d0fc675d242446ebb02b60292c. Script SHA-256 0edaa8c76b453dfc29fac3a6fcfdf4003bf8ed697aa3d0322bd1e8c09fc057fa.

| Family (n=6) | LIVE gate nodes | r* | rank GF(2) | rank GF(65521) | exact #SAT |
| --- | ---: | ---: | ---: | ---: | ---: |
| DISJ3 | 8 | 3 | 8 | 8 | 27 |
| EQ3 | 8 | 3 | 8 | 8 | 8 |
| IP3 | 5 | 3 | 3 | 7 | 28 |
| SEPARABLE3 (parity X AND parity Y) | 5 | 1 | 1 | 1 | 16 |

At k=4, DISJ and EQ each have r*=4 and rank 16 over both fields, IP4 has rank 4 over GF(2) but 15 over the odd field, and SEPARABLE4 has r*=1 and rank 1. For the shared-fanout REUSE graph, the mincut crosses exactly the two original input signals x0,x1 despite repeated x0 uses; a crossing signal is charged ONCE. The 97-case distribution of r is {0:18,1:56,2:17,3:3,4:3}; no rank or factorization failure was observed.

**Raw decoding:** retrieve results/raw/tmr/2026-11-15_1455_TMR4_SIGNALCUT054_FULL_RAW_JSON_ZLIB_BASE64.txt; base64-decode then zlib-decompress it to obtain the unmodified raw JSON. A standalone reconstruction, for example, is Python base64.b64decode followed by zlib.decompress. The source independently reproduces the exact JSON with sorted keys and indentation.

**DISJ falsifier:** DISJ_k has full 2^k rank and r*=k for the supplied circuit, yet its native depth-two unbounded-fan-in Boolean circuit uses O(k) gates/wires and its CNF is 2-SAT. Therefore no superpolynomial circuit lower bound is licensed. **Affine/Gaussian falsifier:** IP_k has r*=k but its algebraic counting formula is cheap; the displayed enumerator is not optimal. **Selector and witness control:** a unique satisfying assignment's full indicator matrix is rank one, and TMR-2/052-053 shows an authentic selector projection may collapse two large slice ranks to one; the present proof only concerns the FINAL Boolean function after specifying its circuit, not a mandatory expanded selector matrix. Horn, bounded-treewidth, 2-SAT, equality, independent products, auxiliary variables, padding, alternative bases, caching/rereading and equivalent rewrites remain legal alternatives. Local invertible bases preserve rank; no characteristic-two Walsh-Hadamard inference. SAT decision on encoded formulas is distinct from this fixed-circuit evaluation matrix.

## 7. Four mandatory gates

| Gate | Status | Exact reason |
| --- | --- | --- |
| 1. DISJ sanity | **PASS (restricted); FAIL for unrestricted rank-to-work** | r*=k and rank=2^k coexist with a linear-size depth-two circuit and easy 2CNF. No prohibited transfer asserted. |
| 2. Relativization | **PASS for representation lemma; OPEN for separation** | Deterministic local equations, cut minflow and finite-field rank do not yield P!=NP. No nonrelativizing step; Baker-Gill-Solovay, algebrization and Natural Proofs obstacles to an eventual unrestricted bridge remain. |
| 3. Simultaneous DTISP | **NOT APPLICABLE to representation theorem; OPEN for forbidden-box transfer** | One exact counting algorithm has both T and S above, but S=poly(L) and time exponential generally. No SAME machine is placed inside strict FLMV limits. |
| 4. Configuration counting | **PASS as upper-bound guard ONLY** | For total deterministic read-only-input, writable-space-s machines, T<=2^{O(s+log L)}. This is not a lower bound and does not constrain randomized/quantum stopping time by itself. |

The circuit-to-CNF standard functional Tseitin lift of g LIVE fan-in-two gates requires n+g variables and O(g) local clauses with O((n+g)log(n+g)) source bits and original-input assignment unique extensions. Such a lift does NOT reduce r automatically, nor turn the stated 2^{r+n/2} procedure into a uniform 2^{o(n)} algorithm for arbitrary polynomial-g circuits. October 2026 #SAT manuscripts, formalization scope and Williams/Bathie-Williams hierarchy premises are independent; no NP-level contradiction or general lower bound follows.

## 8. Corpus, provenance, next target

Governing main directive read FIRST (blob 7b8804dc7587abc5134055b5b0d16a143055ca5a). Relevant TMR-4/051-053 adaptive-switch rank results, TMR-2/052-053 selector/zeta controls, TMR-1/052-053 compression and unique-extension ledgers, TMR-5/048-049 affine and scalar-count falsifiers, TMR-3 Tree Evaluation resource warning, current AGENTS.md/CODEX.md/skill and issue #3 consulted. Related primary baseline: Kushilevitz-Nisan, Communication Complexity (1997), communication rectangles; On the Expressive Power of CNF Formulas of Bounded Tree- and Clique-Width (2011), separator communication reasoning; Lokshtanov et al., Beating Brute Force for (Quantified) Satisfiability of Circuits of Bounded Treewidth (SODA 2018). The theorem is supplied with a self-contained proof; no priority or novelty claim over these precedents.

Repository preflight via a full local checkout could not execute because git DNS resolution failed; GitHub connector readbacks and local deterministic Python execution were used instead. Root proof1.txt was readable (SHA 06f7ebc8), but root proof2.txt (SHA 930c5eed) and main.tex (SHA 6ac34c5d) returned empty bodies through the connector; they were NOT assumed empty, reconstructed or edited. Historical /341 FAIL as full UNSAT authority; /386 RESTRICTED. **TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.**

**ONE NEXT LEMMA:** characterize whether r^*(C;X:Y) after a bounded-cost, algorithm-independent *rewriting* can be made small for nontrivial restricted shared circuit families, while charging its discovery, wire blowup and exact count preservation. Alternatively exhibit an easy affine/Horn family with large r* for EVERY balanced X:Y in its given representation, conclusively denying a proposed inference from this parameter to computation time. A reverse cost-sound arbitrary-SAT-machine transfer remains OPEN. **P versus NP remains OPEN.**

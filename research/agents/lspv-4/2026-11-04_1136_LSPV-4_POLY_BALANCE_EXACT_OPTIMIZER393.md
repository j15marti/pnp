# LSPV-4/393: Polynomial balance and conditional exact minimum-proof extraction

November 4, 2026, 11:36 PST. **PROVED/EXACT elementary conditional lemma; COMPUTATIONAL finite Resolution controls; OPEN for full fixed R_mix341, B1/B2/B3 and P versus NP.** Specialist review pending. Original rules and node weights unchanged.

## IDEA -> SEARCH -> ITERATE

**IDEA:** If SAT is in P and the fixed mixed calculus has polynomially bounded minimum node count, can perfect shortest-derivation selection be implemented efficiently? Falsifiers: (1) node count hides exponential evidence bits; (2) succinct rows require coNP-hard universal verification; (3) prefix oracle needs nonuniform advice; (4) extractor hides a sublinear-space claim.

**SEARCH:** The shared 2026-11-02_1204 five-role handoff and LSPV-4/341 had already refuted pointwise B1 for ordinary Resolution by a fast canonical PHP recognizer. Atserias and Müller (2019/2020, arXiv:1904.02991) prove Resolution automatization NP-hard and explicitly note P=NP makes it automatizable. Cook and Reckhow (1979) formalize polynomial proof verification; Krajicek (2022, arXiv:2208.11642) discusses proof-system polynomial balance. LSPV-1/396 (sha 0355068b) proves a separate succinct all-row validity problem coNP-complete; LSPV-3/399 (sha f8a54ca5) exhibits a nonlinear original-support and paid-port firewall. Reviewed `GROKPROOF/2026-11-04_1518_PROGRESS.md` (sha 4e2bb9d9), Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` and `2026-10-28_1452_CLAUDE_TPORT-0002.tex`; none proves B3. Actual web queries: "Cook Reckhow proof systems polynomially bounded iff NP coNP automatizability P NP self reducible proof search shortest proof", "SAT polynomial time polynomially bounded proof system automatizable", "Automating Resolution NP-Hard", "Haken 1985 intractability of resolution". GitHub connector search `resolution` in `openai` returned unrelated geometric/agent-turn usages; no applicable SAT proof checker was found. Direct Google-branded search unavailable; general web and GitHub connector were used.

**ITERATE:** Since the recognizer is prior work, the sharpened question concerns *exact optimal proof search*. Add one essential explicit hypothesis: a fixed polynomial bound on all certificate bits as a function of source length and charged node count. The theorem below follows by an NP-prefix self-reduction. First finite generator accidentally conflated coordinates and signed literal IDs, producing an illegal tautological clause; fixed before accepting results. Parser also tightened to reject duplicate literals.

## Exact conditional theorem

Let R be one fixed complete sound refutation calculus with nonnegative integer node weights. Assume:

- **V**: an explicit, uniform polynomial-time checker validates an entire binary certificate, source references, rule evidence, and its exact node cost.
- **PB**: there exists a single polynomial b such that whenever an UNSAT CNF F of bit length N has W_R(F)<=q, it has some complete valid R proof of cost <=q and at most b(N+q) encoded bits (including ALL gate descriptions, signed ports, conversion annotations and metadata).
- **PMin**: one fixed polynomial P0 has W_R(F)<=P0(N) for all UNSAT F. This is the consequent of B3, not an established fact for R_mix341.

**PROVED/EXACT conditional implication:** If SAT is additionally in P, one fixed uniform polynomial-time algorithm rejects malformed input, supplies a checked SAT assignment on SAT inputs, and supplies a *minimum paid-node-cost* R refutation on every UNSAT input.

**Proof:** The predicate `exists authenticated R proof y of length <=B=b(N+P0(N)), cost <=q, extending prefix u` belongs to NP: y is a polynomially long witness checked by V. Since SAT is in P, this fixed NP predicate is uniformly decidable in P via Cook--Levin. Binary-search q in [0,P0(N)] to find the least feasible cost, then choose each of at most B certificate bits using prefix feasibility, keeping one possible completion. The resulting proof has cost exactly W_R(F). Use one hardcoded *fixed polynomial* P0 and b, not per-instance advice. SAT witnesses follow standard variable self-reduction. Malformed strings are rejected before proof search. QED.

At most `B+ceil(log2(P0(N)+1))+O(1)` prefix queries are made. With guest SAT decider A, each NP-feasibility query has length D=(N+B)^O(1), yielding a conservative full-work bound

$$
T_{extract} <= (B+\log(P_0(N)+2)+O(1)) [D^{O(1)}+T_A^{wc}(D)].
$$

The straightforward extractor retains an O(B)-bit proof prefix and polynomial-length SAT queries, **not** an N^1/2 writable-space bound. Acquisition, guest indices, query construction, output, proof checking, all-phase memory and failed selections are charged. This is NOT a new B3 proof. The actual full R_mix341 LOCAL-CONVERT exported-wire grammar is still unsettled, so V and PB are unproved for that exact calculus. An exponential implicit row stream is not polynomially checkable merely because one expanded row is easy.

## Established hard-family model

Unary PHP(h+1,h) has h(h+1) Boolean variables and (h+1)+h*binom(h+1,2) explicit signed CNF clauses, of bit length Theta(h^3 log(h+2)). Haken (1985) gives constants c>0,h0 such that for every h>=h0 every ordinary **shared-DAG Resolution** refutation needs >=2^(c h) lines. This is **not** a lower bound for the mixed system or arbitrary machine computations. Cook (1976) gives polynomial Extended Resolution PHP proofs; native GF(2) handles odd Tseitin. Braun (2026, arXiv:2609.23015) gives >exp(n/(32768 ell^2)) **Res(oplus)** lines for bit PHP with n=2^ell, ell>=32, quantifying over DAG proofs in that restricted calculus, not unrestricted SAT algorithms.

## Computational exact finite audit

Exhausted all 256 subsets of eight nonempty non-tautological source clauses over variables x,y. Exactly 95 SAT and 161 UNSAT. Prefix feasibility with explicit Resolution replay plus an independent BFS on closure states and an independently written referee agree on optimum charged nodes: **112 UNSAT instances at q=1; 48 at q=2; 1 at q=3**. Primary implementation logged 2,124 prefix oracle calls and 912 candidate expansions. Verified all 95 SAT witnesses and all 161 authenticated proof DAGs; 12 malformed sources rejected. Odd/even K4 Tseitin controls have 0/8 models. Independent referee checked 256 formulas, 1,024 assignment pairs, 161 optima and rejected one corrupted record. These are finite computations, not complexity lower bounds.

Compact Python reproducer: `experiments/arc/lspv4_393_compact.py`. Machine-readable summary: `results/raw/arc/2026-11-04_1136_LSPV4_393_MINIMUM_PREFIX_SUMMARY.json`. The extended complete code, raw 256-case ledger and independent referee are in the conversation reproducibility archive.

**Next:** freeze and verify all R_mix341 LOCAL-CONVERT/DEF/AND3/GF(2) certificate payload rules and polynomial balance PB, then separately prove B3 instead of assuming it. For materialized child recurrences rho includes every phase: s'<=max{rho,eta,lambda,lambda*s}. P versus NP remains OPEN.

### References

[1] Cook and Reckhow, The Relative Efficiency of Propositional Proof Systems, JSL 44 (1979) 36-50.

[2] Atserias and Müller, Automating Resolution is NP-Hard, JACM 67 (2020), arXiv:1904.02991.

[3] Haken, The Intractability of Resolution, TCS 39 (1985) 297-308.

[4] Cook, A Short Proof of the Pigeon Hole Principle Using Extended Resolution, SIGACT News 8(4) (1976) 28-32.

[5] Krajicek, On the Existence of Strong Proof Complexity Generators, arXiv:2208.11642.

[6] Braun, An Exponential Lower Bound for the Bit Pigeonhole Principle in Resolution over Parities, arXiv:2609.23015 (2026).

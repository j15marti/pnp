# LSPV-2/389: Exact signed-affine matroid-circuit proof minima, source-projection rank criterion

**2026-11-04 04:15 PST.** **PROVED/EXACT** for the specified fixed-calculus infinite promise class; **COMPUTATIONAL** for independent finite replay; specialist mathematical referee pending. P versus NP **OPEN**.

## New theorem in unchanged R_mix341

For an explicitly signed-CNF-encoded GF(2) system with rows of width two or three, let rows form a binary matroid circuit (every row-deletion leaves independent rows, all row masks XOR to zero), with overall odd charge XOR. For each row i, test rank of the projection of ker(A without row i) onto that row's literal-variable support. **If its dimension is d_i-1 for every row, then all M=Σ 2^(d_i-1) original signed clauses are independently indispensable, and the global minimum is W_Rmix341(F)=M-1.**

The proof uses source-arity lower bound for *every* legal shared DAG in the original mixed system, and constructs a matching source-authenticated AND3-plus-XOR DAG with exactly M-1 paid nodes. Input must include fully expanded parity CNF blocks and an explicitly checked partition. No assumption that a fixed optimization policy discovers the proof. No uncharged GF(2), helper definitions, LOCAL-CONVERT payloads or source-label axioms. This is not a lower bound on any arbitrary algorithm.

## Nontrivial finite witnesses

* Three all-charge-one binary rows on 3 variables: six indispensable clauses, W=5, already known in /387.
* New 4-variable non-graph hypergraph, mixed row widths 3/2/3: 10 indispensable original clauses, **exact W=9**; row-projection dimensions 2/1/2.
* New 5-variable four-row hypergraph, widths 3/3/2/2: 12 indispensable clauses, **exact W=11**; projection dimensions 2/2/1/1.
* Flipping the final 5-variable parity RHS gives a **SAT** control.
* The 4-variable rank-defective UNSAT circuit has 12 signed source clauses but **only eight independently essential**; its projected ranks 1/1/1/1 do not fulfill the criterion.
* No malformed strings/corrupted proofs are silently accepted: separate checker rejects six forged proof/data records. Python cross-language audit checked seven additional corruptions.

The repo-published complete JavaScript producer independently reproduces its raw JSON; separately implemented Node verifier performed **536 checks, six corrupted-proof rejections**, reconstructing signed source and partition, GF2 ranks, full truth tables, parity labels, and deletion/flip SAT witnesses. A Python-built independent producer/verifier also passed **667 assertions and seven corruptions**. These counts are software checks, not an independent asymptotic mathematical proof. All repository files were read back byte-for-byte.

## Historical duplication and research controls

The immediately preceding /388 finite n<=3 result was independently reproduced (1,032 fixtures, 19,012 checker assertions), but its theorem already appeared in original **LSPV-2/343** LOW-SUPPORT-MINCORE, so /388 is **verification/replication, not a novel result**. LSPV-2/341 and /387 are legitimate mathematical precursors.

Starting certified hard-family anchor remains **Haken 1985**: for each large h, *every ordinary shared-DAG Resolution* proof of unary PHP(h+1,h) has at least 2^(c h) lines; h(h+1) Boolean variables, (h+1)+h*C(h+1,2) source clauses, Θ(h³ log h) explicit signed bits. **Cook 1976** supplies polynomial Extended Resolution proofs of the *same* family. Neither theorem is an all-algorithm SAT lower bound. Affine/Tseitin GF(2) shortcuts are mandatory controls that defeat Resolution-to-mixed lower bound transport.

Actual Grok reviewed at `GROKPROOF/2026-11-04_1217_PROGRESS.md` (blob cae0560d): full all-input charged circuit-cut method remains unproved. Actual Claude reviewed at `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (blob 1f9fc727): restricted alternation-trading method, not B3. Relevant project peers are LSPV-3/391 interface quotient cost gap, LSPV-4/383 source acquisition, LSPV-5/334 node/bit normalization, LSPV-1/386 restricted observable normalization. No cross-role claim supplies B3.

## Resources and scope

Logical minimum and physical construction are distinct. For this bounded-row explicit-source class, a fully materialized deterministic compiler/checker has polynomial encoded bit output, verification time, bit-access/conversion/update work and peak simultaneous memory. It is not a bound on arbitrary alternative exponential intermediates, which must be charged; nor is the perfectly free optimizer's discovery work included in W. LSPV-4's full-space envelope remains s'<=max{rho,eta,lambda,lambda*s}.

**OPEN:** B1 pointwise, B2 worst-case over all input strings, B3 conditional SAT-in-P to polynomial Wbar for the same fixed R, any general-input superpolynomial mixed-system minimum, and P != NP.

## Published outbox and role handoff

- Mathematical theorem and exact model: `research/agents/lspv-2/2026-11-04_0415_LSPV-2_AFFINE_MATROID_PORT389.tex`
- Producer: `experiments/arc/lspv2_389_matroid_port_compiler.js`
- Independent verifier: `experiments/arc/lspv2_389_matroid_port_independent_verify.js`
- Machine-readable complete source/proof records: `results/raw/arc/2026-11-04_0415_LSPV2_AFFINE_MATROID_PORT389_raw.json`
- This handoff: `research/coordination/2026-11-04_0415_LSPV2_AFFINE_MATROID_PORT389_FIVE_ROLE_HANDOFF.md`

**Falsifiers.** (F1) Minimal dependent equations alone yield all-clause indispensability: false, rank-failure instance. (F2) All-charge-one sources require a zero-charge initializer: false, odd triangle. (F3) Wrong-charge parity flip preserves UNSAT: false, SAT control. (F4) Exact affine family W=M-1 proves unrestricted B3: invalid extrapolation.

**LSPV-1:** independently check rank-projection quantifier scope and the gap between B3 and affine cases. **LSPV-2:** attack the condition with unbounded row width/compact source; expand precise LOCAL-CONVERT port semantics without altering R. **LSPV-3:** test signed hypergraph source pivots, conservative definitions and representation-equivalent short circuits. **LSPV-4:** audit bit-time, child access, verification, peak and all-phase resources including lazy alternatives. **LSPV-5:** referee every mixed-system lower-bound transport and whether candidate source invariant survives strongest permitted calculus.

No tasks, states, schedules, proof-system rules or ownership were changed. The report is separately published as role-owned work; external referee pending. P versus NP OPEN.

**Root manuscript reconciliation safeguard:** The authenticated current root `main.tex` ranged fetch returned a zero-length content body at blob SHA `6636883c332e399eec4130434d233cf9f0345d1a`. Consequently the large original manuscript was **left unchanged** rather than overwriting any existing content. LSPV-5 should incorporate the new restricted theorem only after an intact complete blob is retrieved, within the role-owned region and with byte-for-byte outside-region preservation. The issue #3 coordination comment was successfully published and read back as [issuecomment-6630670739](https://github.com/j15marti/pnp/issues/3#issuecomment-6630670739).

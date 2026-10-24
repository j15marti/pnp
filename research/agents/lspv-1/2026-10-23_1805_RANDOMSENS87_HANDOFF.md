# RANDOMSENS87 five-role handoff (2026-10-23 18:05 PDT)

**Global status:** P versus NP OPEN. **Local theorem:** PROVED/EXACT in a declared addressed-word random-access input-query model, independent external review pending. **Experiment:** COMPUTATIONAL, 30,609 checks, zero failures, seeded full local audit; published compact script plus machine-readable summary.

**Role 1 central result.** Define independent analysis parameter beta_w(F) as the maximum number of pairwise word-disjoint opposite-label legal input changes from F. For any arbitrary state-adaptive total bounded-error randomized exact SAT decision procedure A with per-input error <=epsilon<1/2 and no uncharged input-dependent advice,

    E[source word queries by A on F] >= (1-2*epsilon)*beta_w(F).

Proof couples the same random coins on F and each opposite-label neighboring source. Unless a differing word is read, all future computation, learning, switching, caches and outputs are identical. Each opposite-label pair therefore requires the differing word to be queried with probability at least 1-2epsilon. Pairwise disjoint supports add in expectation. For deterministic exact, epsilon=0.

**Source instantiation.** Import Role 4 TWO-SIGN-SWAP64's source-checked legal signed exact-(2,2) U (UNSAT) and V (SAT) with 198 variables, 264 clauses and the same ordered unsigned supports, differing in two occurrences of x3. Role 2 DOECKER-CORE-CERT61 supplies the independent UNSAT proof dependency, not rerun here. The p-block disjoint SAT product all-V has p pairwise disjoint two-word sensitive mutations to one-U UNSAT. Therefore every exact addressed-word SAT decider, adaptive or not, reads >=p different words; error-epsilon randomized version uses >=(1-2epsilon)p expected words. Input has (1056p+2) fixed-width words, so this is only Omega(N/log N), not superlinear. An O(p) source-aware recognizer bypasses rich representation.

**Coefficient sharpness:** On the abstract p-field AND promise, mix immediate guess FALSE (prob epsilon), immediate guess TRUE (prob epsilon), and a complete exact scanner (prob 1-2epsilon). Worst-case per-input error epsilon, and on all-V average probes exactly (1-2epsilon)p. For full CNF, pay template validation and exact fallback, and claim only O(p) upper bound.

**Adaptive SAT/UNSAT controls:** All 254 orientation-chain 2-SAT patterns q<=7 checked by independent SCC, brute-force for q<=5; 10 hybrid state ledgers; signed exact-(2,2) four-clause parity quartet SAT and separate eight-clause UNSAT 3-variable controls; reverse shared-source circuit agreement. Randomized promise 16 parameter combinations with 12,000 trials each. Full audit sha256 efb2dc161ad783c40da3ea18e296895ae7a87b59c3a8643f5f3b3238a76f2a7c.

**Role 2 assignment:** Test an adaptive source-coherent backward selector or affine summary that avoids materialization yet pays the required probes. **Role 3:** Verify the coupling proof under arbitrary method switching and consider non-standard bulk-input access. **Role 4:** Seek UNSAT-centered signed exact-(2,2) disjoint sensitivities without an uncharged OR-shield and audit uniform grammar. **Role 5:** Maintain the strict distinction between randomized input acquisition, restricted representation cost, and unrestricted exact SAT time.

**First missing implication:** Any independently defined parameter yielding superpolynomial post-acquisition continuation/compression time for *all* total uniform exact SAT deciders, even with arbitrary adaptive source reads, SCC, Horn, affine, backtracking, learning, caching and direct decision. Current beta_w cannot serve: beta_w<=number of input words. No P=NP or P!=NP proof.

**Files:** research/agents/lspv-1/2026-10-23_1805_LSPV-1_RANDOMSENS87.tex, adjacent _minirepro.py and _results.json. Publication must be verified by GitHub readback. Do not assume the full local audit file is available in another runtime. Existing schedules untouched.

# LSPV-1 AFFINE-ROW-ER2-SIMULATION375

**November 3, 2026, 17:00 PST.** Status: **PROVED/EXACT in the declared bounded-output subgrammar, independent specialist review pending**. **COMPUTATIONAL** semantic controls. **OPEN:** full `Rmix341` LOCAL-CONVERT normalization, B1, B2, B3, superpolynomial worst-case full-mixed derivation cost, P versus NP. Existing rules, weights, tasks, states, schedules, identities remain unchanged.

## Fixed calculus and established hard family

Preserve the exact fixed `Rmix341` from `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`: source clauses are authenticated free leaves; strict binary RES, AND3, binary GF(2) addition, locally justified CONVERT and paid conservative two-input signed DEF are unit charged; shared inference DAG nodes count once. Let `E=ER2` be the existing RES+DEF subsystem. Let `L3` be the already proved bounded-local subsystem of LSPV-1/359, with exact at-most-three-named-variable truth tables but **without** opaque arbitrary circuit payloads. Let `X3` consist of `L3` plus legal arbitrary-width native GF(2) row addition, with rows permitted only over source variables or outputs of earlier paid DEF nodes and initial rows checked from exact local parity factors. This is a restricted proof-usage fragment of the unchanged R, not a newly added calculus.

For valid UNSAT F of encoded bit length N, W_S(F) is the attained minimum sum of unit weights over distinct derived inference nodes in a valid shared DAG, and Wbar_S(N) is the maximum over valid UNSAT inputs of length <= N, empty maximum zero.

**Published lower-bound anchor.** For standard unary PHP with h+1 pigeons and h holes, Haken (1985) proves for some c>0 and h0, for every h>=h0 and **every unrestricted DAG ordinary Resolution proof** of the original PHP_h, at least 2^(ch) proof lines. Variables h(h+1); clauses (h+1)+h*choose(h+1,2); explicit signed-input bit length N_h=Theta(h^3 log(h+2)). Thus the paid derived-node lower bound is 2^(ch)-m_h, but **only for ordinary Resolution**. Cook (1976) supplies polynomial Extended Resolution proofs of PHP. Expander Tseitin also has exponential ordinary-Resolution lower bounds yet the fixed mixed system has the verified 4h-1 affine shortcut on odd cubic bridgeless graphs. Neither published lower bound is a universal SAT machine-time bound.

## PROVED/EXACT scoped polynomial simulation lemma (specialist review pending)

There is an absolute nondecreasing polynomial p such that **for every valid UNSAT F**,

$$
W_{X3}(F) \le W_E(F) \le p(N + W_{X3}(F)+1).
$$

A conservative size envelope is p(z)=C(z+2)^4 with a constant C independent of F, its proof, or N. The proof translates **every** valid X3 proof of q nodes, not merely a favored algorithm or instance family. This is a proof-node existence upper bound with free optimal selection, not proof-search runtime.

**Proof.** Take any X3 shared DAG pi with q paid nodes. Canonically rename all original and earlier paid-DEF variables: their number v is at most N+q. Replay each signed RES pivot and each conservative signed DEF in E. LSPV-1 Result 359 already converts each local three-variable AND3/CONVERT factor node into at most 440 paid E inferences, including authentication and paid weakening. Where a local parity factor is exposed as a row, encode its parity with a constant number of signed two-input AND definitions and derive its row-output unit from its at-most-four truth-table blocker clauses using a fixed constant-size Resolution proof.

For **an arbitrary-width native XOR row step**, suppose two authenticated rows with masks alpha,beta and right-hand-side bits a,b derive the row with mask alpha XOR beta and right-hand-side a XOR b. Give each row a parity prefix circuit with v positions. Each two-input XOR gate has a constant-size implementation by paid signed two-input AND definitions, for example p=(u AND NOT w), q=(NOT u AND w), r=(NOT p AND NOT q), whose output is NOT r. The known fixed strict signed copy and true-rail templates handle degenerate inputs, never as free gates. Write A_i,B_i,C_i for prefix parities of the two input masks and their XOR. Introduce four clauses representing the three-variable identity C_i=A_i XOR B_i. At i=0 it holds by the paid constant rail. For each i, each prefix updates by XOR with either x_i or zero. The four choices of mask bits (alpha_i,beta_i) yield only four fixed Boolean implication templates over at most seven prefix/input variables plus a fixed number of gate wires. Each template is a sound fixed finite CNF entailment, so ordinary Resolution completeness and the existing paid literal-weakening compiler provide a **uniform finite strict RES+DEF certificate** for its four output clauses. Consistent renaming reuses this constant template for each i and each step. At i=v, two input-output units and the final identity clauses yield the output row unit using genuine Resolution. Thus each wide XOR row step costs O(v+1) E nodes, with canonical masks and gate bits explicitly encoded, not 2^v blocker clauses. When the final row is 0=1, the true/false rail and a final paid Resolution inference yield contradiction. There are at most q steps, so the translated E proof costs O(q(v+1)+440q+1), safely dominated by C(N+q+3)^4. This construction is fully uniform across F and DAGs, including arbitrary adaptive row order, sharing and intermediate growth.

Since E is contained in X3, W_X3(F)<=W_E(F). Minimize freely over pi and maximize over encoded inputs to obtain the claimed polynomial comparison. In particular a superpolynomial worst-case lower bound for E is equivalent to such a lower bound for X3, **but nothing here proves either lower bound**, and the result does not imply any corresponding lower bound for full Rmix341.

## Exact scope and falsifiers

F1: Exponential CNF expansion of a long parity row is indispensable. **FALSIFIED in X3** by O(v) paid parity-prefix gates plus constant local certificates; truth-table materialization would have its true output cost if selected. F2: Haken's exponential ordinary-Resolution lower bound transfers to X3. **FALSIFIED as an inference** because the embedded E has polynomial PHP refutations. F3: An arbitrary unit-cost circuit-valued LOCAL-CONVERT can be normalized at polynomial cost in its node count. **OPEN**: the LSPV-4/363 and Red Team/315 payload/CVP controls show why syntax U, with arbitrarily long uncharged circuit bodies, cannot be assumed to have polynomial verification length. F4: The native row identity is a SAT/equivalence oracle. **REJECTED**: each affine mask and rhs is checked syntactically; the E translation consists exclusively of independently justified paid gate slots and strict Resolution steps.

## Independent computational controls and resource accounting

A deterministic JS producer and a separately authored no-import JS independent verifier each tested **21,844 mask pairs** over widths one through seven, **2,396,744 full assignment identities**, and **30,948 corrupted declared XOR result masks**. The independent checker also established rank three for K4 vertex-edge incidence; the even- and odd-charge K4 model counts were **8 and 0**. No randomized tests, new hard families or native full ER2 compiler replay are claimed. The checks verify only finite affine semantics and adversarial row-mask rejection; they do not independently verify the symbolic all-size strict ER simulation.

Normalizing q X3 records uses at most O((N+q)^2 log(N+q+2)) encoded evidence bits for signed clauses, masks, paid names, rules and references. This is **not** a bound for every opaque full-R circuit payload. Parsing, all input bits and reference reads, proof construction, name allocation, validation, output, cache/storage and all live ancestors are charged to actual implementation work; the free logical optimum does not include proof acquisition. No physical time-space lower bound or FLMV contradiction follows. The materialized-child envelope remains s'<=max{rho,eta,lambda,lambda*s}, with rho covering every local phase.

## Corpus and provenance

**CORPUS REVIEWED:** November 2 12:04 full refocus directive and appendenda; current issue #3; root main.tex full readback at blob 41bdb641f441ca2f0b4555ecc00496bef80415b0; AGENTS.md, CODEX.md, repo pnp-research SKILL; original LSPV-2/341; LSPV-1/337, 357, 359, 361, 365, 373, 374; peer LSPV-2/365, 369, 373, 374; LSPV-3/374, 378; LSPV-4/363, 372; Red Team/308, 313, 315, 324. **DUPLICATION AUDIT:** Result 359 already handled L3-only simulation. Red Team/308 already checked local signed XOR/associativity/cancellation templates on a lifted Tseitin family. LSPV-2/369 gave a native GF2-to-Res(oplus) backtranslation at exponential 2^b DEF-exposure overhead. The distinct increment here is a **polynomial all-input, all-shared-DAG simulation of global native XOR row interleaving into existing paid ER2**, restricted to normalized L3 conversions. No academic originality is claimed for general ER simulation principles. **WHAT CHANGED:** a narrower proof-system polynomial comparison, not any full-R B3 or hardness claim. **ADOPTED:** the local authenticated 359 compiler and 308 signed gate templates. **REJECTED:** reversal of ordinary Resolution lower bounds, hidden representation normalization, pointwise to worst-case quantifier flips. **STALE CLAIM:** any claim that long XOR rows necessarily cost exponential E proofs would be invalid in X3.

**Grok and Claude:** Read actual GROKPROOF/2026-11-03_2214_PROGRESS.md at blob 59fe73c20473bd6bc20500cf58d75e42519aee88. Its fully charged arbitrary-A ARC transformation remains OPEN. Read actual research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex at blob b7150bb9ed964affd5fb90ecd24b0aa35d600bf9. Its portfolio results hold in specified alternation-trading systems, not arbitrary SAT computation or B3. Independent assessment: neither supplies the missing transfer.

**Research queries:** Haken PHP lower bound, Cook ER pigeonhole proof, Buss 1987 Frege PHP, Cook–Reckhow p-simulation, Kiesl–Rebola-Pardo–Heule–Biere (2020) DPR/DRAT-to-ER, project searches 'GF2 row extended resolution polynomial', 'XOR row ER2 proof', 'LOCAL-CONVERT polynomial normalization', 'GROKPROOF', 'research/agents/claude', and github.com/openai proof checkers. No compatible OpenAI-owned fixed-R checker was identified. Repository-wide preflight/native full ER2 compiler replay was not run.

**NEXT GAP:** settle authoritative full-R circuit LOCAL-CONVERT grammar and prove a downstream-preserving polynomial normalization, or explicitly exhibit a legal violating proof. No unproved claim that the subgrammar covers every full-R proof.

**B1 OPEN; B2 OPEN; B3 OPEN; full Rmix341 superpolynomial Wbar OPEN; P versus NP OPEN.**

## References

[1] A. Haken (1985), *The Intractability of Resolution*, Theoretical Computer Science 39, 297-308.

[2] S. A. Cook (1976), *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4), 28-32.

[3] S. Buss (1987), *Polynomial Size Proofs of the Propositional Pigeonhole Principle*, JSL 52(4), 916-927.

[4] S. Cook and R. Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems*, JSL 44(1), 36-50.

[5] B. Kiesl et al. (2020), *Simulating Strong Practical Proof Systems with Extended Resolution*, J. Autom. Reason. 64, 1247-1267, DOI: 10.1007/s10817-020-09554-z.

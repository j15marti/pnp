# LSPV-1/386 five-role handoff: bounded-observation certificate bit normalization

**November 4, 2026, 02:56 PST.** Same fixed original R_mix341 and five existing roles; schedules, enabled states and task IDs unchanged. **PROVED/EXACT only in a typed bounded-observation fragment, independent mathematical review pending; CONDITIONAL for original R_mix341; COMPUTATIONAL finite controls. P versus NP remains OPEN.**

## Result and exact scope

For **every** valid UNSAT source F encoded in N bits and **every** q-paid-node refutation in a calculus interface where (i) each huge LOCAL-CONVERT circuit depends on at most three authenticated original Boolean variables, (ii) each later paid node observes at most a fixed number a of exported gate ports and only their Boolean values, (iii) gate IDs can be consistently alpha-renamed, and (iv) every new global DEF is paid, there exists a same-source, same-paid-node-count refutation with full explicit certificate length at most

$$
K_a(N+q+2)^3
$$

bits. Source variable declarations and original signed identifiers are preserved; fresh DEF IDs move above the original declared bound.

Proof: at most aq port observations across all q paid consumers; each observed port is one of 256 Boolean functions on a common at-most-three-bit support. Build at most 6656 canonical gates per circuit producer, plus the actually observed output aliases, preserving the complete vector of observable functions and every extensional downstream check. Normalize the at most q fresh DEF identifiers and each clause/GF(2) mask over at most v+q appearing variables, v<=N; summing signed ID, source pointer and output bytes yields the cubic bit cap. Conversion may still require reading and evaluating an arbitrarily long original circuit; no physical runtime bound follows.

Combining this **conditional-fragment** bit cap with LSPV-1/385 gives exact computability of the fragment's proof budget and W,Wbar, and NP membership of unary-budget feasibility for a polynomial-time-checkable witness grammar. It gives **no** polynomial bound q=N^{O(1)} and closes no B1/B2/B3 implication.

**Novelty/duplication:** This is a quantified global all-q bounded-observation consequence of previously published LSPV-1/379 (vector-valued semantic quotient), /385 (cost-compactness), and LSPV-5/334 (private-wire bit normalization). It is not a new hard-family lower bound. A proposed Gödelian alternative was discarded as duplicate of LSPV-1/357.

**Unresolved original grammar:** The original /341 rule text does not explicitly settle named output exports and whether a paid consumer can access unbounded independent/public wires or circuit syntax. Do not promote this theorem to the whole unchanged R_mix341 until the exact parser/semantics are verified.

## Independently checked finite controls

Python iterative evaluator: **3,436** assertions. GitHub-readback JS recursive checker executed with test-only assert/fs shims: **2,327** assertions. Four acyclic circuits with 12/120/1200/4800 private gates and 14/43/43/43 observed ports; respectively 9/11/7/7 unique 3-bit functions. All eight assignments compared; root-same/public-wire-opposite, same-source SAT/UNSAT, and malformed proof-input controls. This is not a native full mixed-calculus checker. No random seed.

## Five specialist next tests

1. **LSPV-1, formal W/B1/B2/B3:** obtain precise original named-wire and extensional legal-rule semantics; attempt promotion of the proved typed fragment or isolate an exact unproved hypothesis.
2. **LSPV-2, circuits/affine:** implement hostile legal LOCAL-CONVERT multi-output and DEF access test, including unbounded embedded circuit payloads and GF(2)/Tseitin escapes. Identify whether a public-port consumer has fixed arity.
3. **LSPV-3, hypergraph DAG:** independently audit alpha renaming, shared ancestor identities, original signed source references, public-bank vector correlations and conservative DEF scope.
4. **LSPV-4, fully charged T/S:** account for arbitrary L-bit payload access, local gate evaluation, source IDs, optional rescan, output, proof replay and peak live space; do not treat the existential cubic bit cap as a polynomial-time procedure on supplied L much larger than N+q.
5. **LSPV-5, adversarial:** attack the fixed-a port-use assumption and intensional name/syntax consumers with a **legal source-authenticated** counterexample, then audit the inference from proof-bit bounds to B3. No new proof-packing rule is allowed in the target.

## Source and publication record

Formal report: research/agents/lspv-1/2026-11-04_0256_LSPV-1_BOUNDED_OBSERVATION_BIT_NORMALIZATION386.md (blob 82f85a2d66841929970b261a360156be0306ac90).
Producer: experiments/arc/lspv1_386_observed_port_normalize.py (blob 9553b4224babc182ff99063bf8411a09cf106815).
Independent verifier: experiments/arc/lspv1_386_independent_verify.js (blob 5244542747ced6ef1942e338f9f62287f35c1375).
Raw results: results/raw/arc/2026-11-04_0256_LSPV1_BOUNDED_OBSERVATION386.json (blob c87383913cf56b822641cb0e2844580dc96c5f0f).
All were checked by GitHub readback. Main.tex reconciliation and issue #3 write/readback are separate steps.

Original grammar: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex blob c87acd11.
Peer Red Team /334: research/coordination/2026-11-04_0248_LSPV5_TO_FIVE_ROLE_NODE-BIT-NORMALIZATION-OPTIMAL-SYSTEM-FIREWALL-REFEREE334.md blob 961e58ad.
Grok GROKPROOF/2026-11-04_0213_PROGRESS.md blob 8e7d1876; Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex blob 9a5b05d6; both read and neither provides B3.

**Haken 1985:** unrestricted shared-DAG ordinary Resolution PHP lower bound only. **Cook 1976:** polynomial paid-ER PHP shortcuts. **Braun 2026:** recent extension-free unrestricted DAG Res(oplus) bit-PHP lower bound only; not unrestricted machine hardness. All B1/B2/B3 and mixed-system superpolynomial Wbar remain OPEN; P versus NP remains OPEN.

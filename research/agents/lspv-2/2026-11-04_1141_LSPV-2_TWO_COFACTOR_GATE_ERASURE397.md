# LSPV-2/397: Two-cofactor elimination of conservative binary extension gates

**November 4, 2026, 11:41 PST.** PNP SAT-Circuit Reduction Builder, role LSPV-2, original five-role schedule unchanged.

**Status:** PROVED/EXACT within the expressly restricted ordinary shared-DAG Resolution + paid signed AND2 definition system `E={RES,VARDEF}`, independent specialist mathematical review pending; COMPUTATIONAL for the independently checked finite cases; KNOWN THEOREM Haken 1985 and Cook 1976. OPEN for full fixed R_mix341, B1/B2/B3, worst-case superpolynomial mixed minimum and P versus NP. The theorem concerns proof cost, not unrestricted SAT machine time.

## IDEA before SEARCH

Previous LSPV-1/371 eliminated each signed AND2 definition with at most 64-fold proof-size expansion. Hypothesis: for a final fresh gate `y=a AND b`, fixing only the original variable underlying signed input `a` forces `y` to be either 0 or the single signed literal `b`. If ordinary shared-DAG Resolution is closed under literal/constant substitutions, the resulting two cofactor refutations can be lifted and resolved, yielding an overhead of only two rather than 64 per definition.

Falsifiers: (F1) a strict Resolution step requiring more paid lines after literal substitution; (F2) a defining clause surviving rather than becoming a tautology; (F3) guarded proof branches cannot be merged without forbidden free weakening; (F4) duplication by an existing equally strong ER2 theorem.

## SEARCH, exact sources and iteration

Read original fixed R_mix341 `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob c87acd11), required five-role coordination directive `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, issue #3, AGENTS.md, CODEX.md, and the project research skill. Found and compared direct predecessor `research/agents/lspv-1/2026-11-03_1306_LSPV-1_HAKEN_EXTENSION_BUDGET371.tex` (64^g erasure), LSPV-2/371 (different 4^g affine Res(XOR) fragment), /378 Cook-extensions and immediate /396 source-section reflection, LSPV-1/396 succinct-row audit and red-team REFEREE342. No claim that gate erasure itself is new.

Read actual Grok `GROKPROOF/2026-11-04_1518_PROGRESS.md` (blob 4e2bb9d9) and Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (blob 9a5b05d6) and `2026-10-28_1326_CLAUDE_TPORT-0001.tex` (blob b7150bb9). Both leave unrestricted transfer OPEN. Primary literature inquiries: `Haken 1985 The Intractability of Resolution`, `Cook 1976 A Short Proof of the Pigeon Hole Principle Using Extended Resolution`, `resolution proofs closed under restrictions literal substitution projection`, `extended resolution eliminate one gate proof size`, and `Atserias Muller Automating Resolution is NP-Hard`. Checked accessible abstracts/publisher information and project detailed theorem audits; original paywalled Haken/Cook complete papers were not retrieved. Direct Google-branded search was unavailable: general web was searched instead. Authenticated searches on github.com/openai included `resolution substitution`, `SAT proof checker`, `CNF resolution`, `propositional`. Read `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFWidthSearch.lean` blob 14a9f16d, which concerns executable CNF-search resource accounting, not proof backtranslation. No relevant ready-made verifier found.

## Fixed restricted model

Original `F` is an arbitrary finite valid signed CNF. Original clauses are free proof premises. Strict ordinary binary Resolution with an explicitly named complementary pivot costs one distinct DAG inference; shared nodes are paid once. Each conservative fresh gate `y ↔ (a AND b)` costs one paid VARDEF and supplies the exact three defining clauses `(not y OR a)`, `(not y OR b)`, `(y OR not a OR not b)`, where the signed inputs have distinct underlying predecessor variables. Gates are acyclic, with no output later referred to by earlier definitions. Let `g` be the number of gates, `r` the number of paid Resolution nodes; `q=g+r`. This is a **proper subgrammar** of fixed R_mix341: its AND3, native GF(2), and especially circuit-valued LOCAL-CONVERT are not covered. No new R_mix341 rule is authorized.

**Lemma A (strict shared-Resolution under literal/constant substitutions).** For any fixed substitution mapping each variable to a signed literal or constant, a strict Resolution DAG can be replayed with no more derived nodes, maintaining for each non-tautological image clause a derived subclause. Induct on the source-ordered DAG: when mapped complementary pivots survive, resolve the two strengthened parents once; otherwise inherit the stronger parent; if one parent is tautologically satisfied, the other subsumes the target unless the target also is tautological. The empty final clause persists. This requires neither arbitrary semantic entailment nor paid weakening.

**Lemma B (one gate).** Let B be the old-source bank, y its last fresh AND2 gate. Cofactor the original variable v underlying a at 0 and 1. Substitute y=0 in the branch where a is false, y=b in the other. Every clause of the complete y definition becomes a tautology. Lemma A yields strict Resolution refutations of B|v=0 and B|v=1, each with at most r steps. Lift to original B by adjoining the false-assignment guard v or not-v and replaying the strengthened clauses. Each branch derives its guard unit with at most r steps or directly yields empty. Resolve opposite guard units once. Hence a strict B-only refutation uses at most 2r+1 derived nodes.

**Theorem 397 (all-size, source-preserving gate erasure).** For EVERY UNSAT original F, EVERY acyclic complete bank of g paid signed AND2 definitions as above and EVERY strict Resolution refutation from F plus those definitions with r distinct derived Resolution nodes,

$$
\boxed{W_{\mathrm{Res}}(F)+1\le 2^g(r+1).}
$$

Equivalently, for any legal paid E proof with total q=r+g,

$$
W_{\mathrm{Res}}(F)\le 2^g(q-g+1)-1.
$$

**Proof:** Apply Lemma B to remove the last gate and treat earlier banks as old source. Repeat backwards g times; if r_j is the current number of derived Resolution nodes, `r_(j-1)+1 <= 2(r_j+1)`. All gate-definition clauses disappear when their gate is removed. The terminal refutation uses only original F. No optimizer budget assumptions.

**Known-hard-family consequence (restricted E, not full R_mix341).** Let P_h be the explicit unary pigeonhole CNF PHP_(h+1)^h on h(h+1) variables, with `m_h=(h+1)+h*binom(h+1,2)=Theta(h^3)` signed clauses and conventional signed-index encoding N_h=Theta(h^3 log(h+2)) bits. Haken (1985) proves there are c>0,h0 such that, for **every** h>=h0 and **every** unrestricted ordinary shared-DAG Resolution refutation of P_h, at least 2^(ch) proof lines are necessary. Thus W_Res(P_h)>=2^(ch)-m_h and all E proofs obey

$$
\boxed{2^g(r+1)\ge 2^{ch}-m_h+1.}
$$

For any fixed polynomial bound on q as a function of N_h, `g>=ch-O(log h)`. If g=o(h), r must be exponential in h. This improves LSPV-1/371's factor 64 to factor 2 **only within this fixed proof fragment**. Cook's polynomial Extended Resolution PHP proofs use many paid gates and are consistent with this result. Haken's theorem does not quantify over mixed R_mix341 or all uniform SAT algorithms.

## ITERATE: experiments and corrected failures

The complete local Python producer (also supplied in the run archive) exhaustively tested 3,528 well-typed 3-variable single-Resolution literal/constant substitutions; an actual five-step proof of `(x) AND (w) AND (not x OR not w)` plus `y=x AND w` becomes a strict two-Resolution source-only proof. Two cofactor proofs cost 0 and 1; a second unused nested gate `z=y AND v` is removed in reverse definition order, again yielding 2 source-only steps. The signed input gate `y=(not x) AND w` passed truth-table controls. A separately authored JavaScript verifier replayed 22 strict proof inferences and rejected 3 corruptions; SAT source-deletion and UNSAT controls passed. A source restriction can already contain empty source clause, producing a legitimate zero-node branch: an early incorrect implementation assumption was repaired. Another early bug confused Python int literal 1 with bool True; corrected by strict type check. Finite tests support, but do not substitute for, the symbolic proof. The example's two-node original proof is exact by the three indispensable original clauses; its five-node extended witness was not optimized.

## Fully charged resources and transfer limits

The theorem measures **paid proof-DAG nodes** only. A literal compiler must read, parse, access and validate the supplied proof and clauses, materialize cofactors and source guards, build/verify every output row, output full encoded bits, and allocate all concurrently live states. In a straightforward implementation the time and output bits can grow as `2^g poly(N+L+r)`, for input proof length L; peak memory for eager materialization can scale comparably. Proof search is separate and unrestricted optimal choice is free only in the mathematical minimum. Allocating then freeing N bits still incurs phase-peak rho>=1 in the FLMV envelope `s' <= max{rho,eta,lambda,lambda*s}`. No polynomial overhead for unrestricted g, no all-algorithm domination, no B1/B2/B3.

The fully fixed R_mix341 adds RES, support-three AND3, GF(2) addition, checked LOCAL-CONVERT, charged conservative DEF. This run gives NO gate-erasure theorem for its other rule types or for unbounded opaque circuit payloads, and NO superpolynomial worst-case minimum for the combination. Next task: freeze the original LOCAL-CONVERT typed exported-wire grammar and test the same two-cofactor simulation on all legal mixed operations. All five agent identities/states/schedules unchanged. Root main.tex was retrieved as blob SHA but with zero-length content; it must not be partially overwritten. Repository local checkout-dependent preflight and LaTeX compilation were unavailable, not claimed.

## References

[1] Haken, A. (1985), The Intractability of Resolution, Theoretical Computer Science 39, 297-308, DOI 10.1016/0304-3975(85)90144-6.

[2] Cook, S. (1976), A Short Proof of the Pigeon Hole Principle Using Extended Resolution, SIGACT News 8(4), 28-32, DOI 10.1145/1008335.1008338.

[3] Atserias, A. and Müller, M. (2020), Automating Resolution is NP-Hard, JACM 67(5), Article 31. Proof automatization concerns searching for proofs, not their unavoidable length.

[4] Cook, S. and Reckhow, R. (1979), The Relative Efficiency of Propositional Proof Systems, JSL 44(1), 36-50.

**P versus NP remains OPEN.**

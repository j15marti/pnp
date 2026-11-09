# Living log: worst-case minimum derivation cost (Wbar_R) program

Canonical directive: `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`.
Objective: Wbar_R(N) = max over UNSAT F, |<F>| <= N, of min over refutations pi of cost_R(pi); free choice of the best derivation (search cost not charged).
Primary bridge B3: SAT in P  =>  Wbar_R(N) <= poly(N), for the SAME fixed R. B1 => B2 => B3.
**Status: P versus NP OPEN. B1, B2, B3 and a superpolynomial Wbar_R are all OPEN. Entries below are CANDIDATE/KNOWN as labelled.**
Append-only; newest entry last. Root `main.tex` ownership rules are untouched by this log.

---

## Entry 2026-11-09 (scheduled run, general lead role)

### Corpus reviewed
AGENTS.md; the Nov-2 directive; root `main.tex` B3 paragraphs (REFEREE296 relativization barrier; size-optimality bridge to B1); newest handoffs LSPV-1/545, LSPV-2/528, LSPV-3/542 (parity facets), LSPV-5/460-462; repo-wide search for "worst-case", "B3", "multisign". Not re-read byte-for-byte: the ~5000 historical reports.

### Literature check (web, standard search; snippets only, not full-text verified)
1. Krajicek-Pudlak / Cook-Reckhow: a polynomially bounded Cook-Reckhow system exists iff NP = coNP. (KNOWN THEOREM.)
2. Messner: P = NP gives p-optimal systems in the sense of the open optimal-system question. The question of whether TAUT has an (p-)optimal system is still open; arXiv 2602.02294 (early 2026) restates this as open. Relevance: B3 holds for any R that is p-optimal among Cook-Reckhow systems, which is the existing size-optimality bridge in main.tex. No new information that changes it.
3. Extended Frege superpolynomial lower bounds: still open as of this search. 2026 progress is on neighbouring systems only: Alekseev (Theory of Computing 2026; Res-Lin / binary value principle, exponential lower bounds), de Rezende-Engstrom-Ghannane-Risse (May 2026 arXiv; tree-like semantic Frege with bounded line size). Neither covers a calculus containing extension/DEF plus AND3/XOR plus RES, so neither bounds R_mix341.
4. Pich-Santhanam (2023): a superpolynomial EF-with-witnessing-axioms lower bound would imply SAT needs superpolynomial circuits. Reads as the converse direction of what B3 needs; it is evidence that lower bounds for strong calculi are hard to separate from circuit lower bounds, not a bridge.
5. Bounded-arithmetic line (Krajicek-Oliveira, Li-Oliveira, Chen-Li-Oliveira): relevant to the reflection gap in item "B3 decomposition" below. Cited from memory, NOT verified in this run; read before relying.

### New precise statement (CANDIDATE bookkeeping, elementary)
**B3 decomposition.** For a fixed Cook-Reckhow-verifiable R with cost polynomially dominated by encoded length:
- (a) "Wbar_R superpolynomial" is equivalent to "R is not polynomially bounded".
- (b) B3 is the material implication  (SAT in P) => (R polynomially bounded). In a world with P != NP it is vacuously true, so B3 can only be *proved* by deriving R's short proofs from the hypothesis SAT in P. Any proof of B3 is therefore a proof under that hypothesis, and cannot go through a direct lower bound on R.
- (c) Known sufficient routes: (i) R p-optimal among Cook-Reckhow systems (open in general); (ii) R contains the Cook translation of PV/S^1_2 AND the polynomial-time decider A is *provably correct* in that theory for the UNSAT side. Unprovable-correctness is the exact gap: Levin's universal search certifies SAT answers by witnesses but gives nothing for UNSAT answers, so it does not supply (ii).
- (d) Hence the weakest sufficient bridge is a **uniform provable-correctness statement for the UNSAT side of some P-time SAT decider, inside R**. This matches the RT/SC obligations already tracked in main.tex and sharpens them to one sentence. It introduces no new theorem beyond (a)-(c), which are folklore/KNOWN; the contribution is the packaging as a single falsifiable obligation.

### What this does NOT establish
No lower bound on Wbar_R, no B1/B2/B3, no transfer theorem. Multisign DAG hypergraph minimal-state work continues in LSPV-1/2/3 reports; this entry adds none.

### Suggested next obligations per role (from the packaging above)
- Lead: state (c)(ii) for R_mix341 as a precise conditional theorem, listing which PV axioms the rule set can simulate.
- Circuit Builder / Certificates: continue the DEF/owner/facet grammar work (LSPV-3/542 handoff) so that any short-proof witness is a checked DAG.
- Resource Auditor: charge reflection-proof size and peak space when (ii) is instantiated.
- Red Team: look for a fixed A whose UNSAT-correctness is independent of the simulated fragment (countermodel) and for hidden free-oracle leakage.

% END_OF_LOG_ENTRY 2026-11-09

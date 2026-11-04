# LSPV-2/392: NP-complete singleton source criticality inside uniformly one-step UNSAT CNFs

**November 4, 2026, 07:07 PST, America/Los_Angeles.** **PROVED/EXACT (symbolic, independent specialist review pending)** for the reduction and semantic identities; **COMPUTATIONAL** for finite independent tests; **KNOWN** for 3-SAT NP-completeness and published proof-system theorems; **OPEN** for B1/B2/B3, superpolynomial mixed-calculus minima, and P versus NP.

## Fixed model and the question

Use the unchanged source-authenticated `R_mix341` of LSPV-2/341 (original blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`), including its native strict binary Resolution rule, free labelled original clauses, one paid node per distinct inference and no empty source axiom. We do **not** add any rule. Other allowed mixed rules, paid gates, GF(2), and authenticated conversions are still available. The entire construction uses only the native Resolution subcalculus, so its cost upper bound is valid even if a proof chooses any other rule. With nonempty source clauses and no zero-cost inference to the empty clause, the lower bound is one paid node.

For an UNSAT labelled CNF F define source clause i to be indispensable when removing only that labelled clause makes the remaining CNF satisfiable. Let E(F) denote the number of indispensable original source clauses. This is a source-dependent semantic statistic, NOT an all-algorithm runtime invariant.

## Theorem 392.1: Exact essentiality carrier with a constant proof

For every proper CNF H over original variables x (all clauses nonempty, no occurrence of fresh t), let the labelled formula be

$$
F_H = (t) \;\land\; (\neg t) \;\land\; \bigwedge_{C\in H}(\neg t\lor C).
$$

The first two labelled source clauses have indices 0 and 1; the guarded source clauses have indices 2 onward. For *every* H:

$$
F_H\in\mathrm{UNSAT},\qquad
W_{R_{\mathrm{mix341}}}(F_H)=1,
$$

and the exact original-clause indispensability spectrum is

$$
\boxed{ E(F_H)=1+\mathbf 1_{\{H\in\mathrm{SAT}\}}. }
$$

More precisely, index 0 (the positive unit t) is always indispensable; index 1 (the negative unit not-t) is indispensable iff H is satisfiable; all indices at least 2 are inessential.

**Proof.** A single ordinary Resolution inference with parents (t) and (not t), pivot t, derives the empty clause. No source is empty and no sound zero-cost axiom derives the empty clause, so the paid minimum in this fixed rule convention is exactly 1. Deleting (t) leaves (not t) and every guarded clause; the assignment t=0 satisfies these regardless of H. Deleting (not t) forces t=1 and makes every guarded clause equal its original C, hence the remainder is satisfiable iff H is. Deleting any guarded clause leaves the contradictory units untouched, so the remaining source is UNSAT. This proves all claims. QED.

The construction is a uniform polynomial-time mapping. For 3CNF H the output is an explicit signed CNF with source width at most four and two unit clauses. After renumbering variables, if L is the signed indexed encoding length of H, the output requires O(L log(L+2)) bits under a conventional binary literal-index format. This includes every added guard literal and its clause delimiter. Nothing is implicit or granted zero output cost.

## Theorem 392.2: NP-completeness even with a one-step refutation

Restrict to the syntactically recognizable image of the above mapping on proper nonempty 3CNF inputs H. The language

$$
\mathrm{ONE\!\_RES\!\_CRITICAL}
=\{F_H: (\neg t)\text{ is an indispensable labelled clause}\}
$$

is NP-complete under polynomial-time many-one reductions, **although every input F_H is UNSAT and has a fixed one-inference Resolution refutation**.

**Proof.** By Theorem 392.1 membership is equivalent to SAT(H). A witness is an assignment satisfying all H-clauses (equivalently satisfying F_H without its negative unit), verifiable in polynomial time. The wrapper, distinguished negative-unit label and removal of the guard literals are syntactically recognizable in polynomial time for the declared image grammar. The mapping from general proper nonempty 3SAT to this language is polynomial and preserves both labels. Thus the language is NP-hard and in NP. QED.

This is **not an unconditional superpolynomial machine lower bound**. NP-completeness of *extracting the semantic statistic* does not imply difficulty of *deciding the source formula F_H*, whose UNSAT status has an explicit trivial proof. It is not a counterexample to B1, B2 or B3. Its classification is **candidate-invariant failure** and **family failure** for any claim that computing E is necessary before deciding SAT.

### Theorem 392.3: Conservative auxiliary circuits cannot rescue the metric as runtime

Suppose D(x,t,y) is a fixed conservative definitional extension with the strong property

$$
\forall (x,t)\;\exists y:\ D(x,t,y).
$$

For every subset S of original labelled clauses, S is SAT iff S together with D is SAT. In particular, deletion of any original source clause preserves its indispensability status, and the one-step refutation using original (t),(not t) remains valid. This applies to fully charged conservative Boolean gates and authenticated extensions when that totality hypothesis actually holds. Nonconservative restrictions or forged active clauses do not qualify. The result is about original-source criticality, not essentiality of newly introduced definition clauses.

## Falsifiers, controls and provenance

1. **F1:** A source statistic taking two exact values might classify only easy source labels. **FALSIFIED as an acquisition claim:** distinguishing E=1 from E=2 on this uniformly easy UNSAT image is NP-complete by the SAT reduction, not by a proven runtime lower bound.
2. **F2:** The guard source C might itself be essential. **FALSIFIED:** contradictory units survive deletion of any one guarded clause, even when H is minimally UNSAT.
3. **F3:** Conservative AND/XOR circuits make the original source-deletion property disappear. **FALSIFIED under all-subsets totality:** original deletion witnesses extend through D; the original one-node proof remains.
4. **F4:** This NP-complete acquisition problem refutes B2/B3. **FALSE INFERENCE:** a uniform correct general SAT decider may use the one-step shortcut on this syntactic family and unrelated tactics elsewhere; this gives no global worst-case runtime bound.

**Finite independent verification:** the primary source-clause deletion enumerator tested all 256 subsets of eight nonempty, non-tautological clauses on two variables: 95 satisfiable H give E=2, 161 UNSAT H give E=1. It also tested 1,024 deterministic three-variable clauseset samples from the 26-clause universe, using seed 123456789: 58 SAT and 966 UNSAT. It performed **6,667 assertions** and rejected eight malformed source/pivot controls. The independent verifier used a separate bitset satisfying-assignment implementation, independently reconstructed all sources, deletions and the Resolution pivot: **7,680 assertions**, identical histograms, both labels. Total instrumented assertion count **14,347**. A single finite test does not prove NP-completeness; the all-input reduction above does.

Files and immutable source blobs:
- `experiments/arc/lspv2_392_guarded_essentiality.js`, Git blob `83d07666bd71aeb752321c66aaa98e22a8e8fd27`.
- `experiments/arc/lspv2_392_independent_bitset_verify.js`, Git blob `f8f02f895a9645da30aa389acbaa025f6eb7712b`.
- `results/raw/arc/2026-11-04_0707_LSPV2_GUARDED_ESSENTIALITY392_raw.json`.

**Model cost firewall:** A proof of the fixed input F_H has one paid RES node, but the encoded input is O(L log L), the wrapper constructor costs polynomial bit-time and O(poly L) peak memory, and the full well-formedness and image recognizer must read and validate its explicit input representation. The published finite exhaustive optimizers enumerate assignments and do **not** constitute an efficient SAT solver for H. The one-step proof is readable and checkable in polynomial time, with its pivot and two parent units explicit. Logical node count is not that verification or encoding time, and neither is a lower bound on an arbitrary decider. No exponential intermediate representation is silently discarded; if one is introduced by a different proof path, its materialization, bit access, checking and peak space must be accounted for.

**Established hard-family calibration:** Haken (1985) gives constants c>0, h0 such that for every h>=h0 every *ordinary shared-DAG Resolution* refutation of the **explicit unary PHP(h+1,h) CNF**, encoded by h(h+1) Boolean variables and (h+1)+h*binom(h+1,2) clauses (N_h=Theta(h^3 log(h+2)) signed-indexed bits), has at least 2^(c h) proof lines. The proof system is Resolution, NOT R_mix341, Res(XOR), Extended Resolution or a model of arbitrary SAT machine computation. Cook's 1976 Extended Resolution upper proofs of PHP are a mandatory representation shortcut control. The present H-to-F_H construction intentionally creates a DIFFERENT source formula with a contradictory two-clause core; it is not a legal source-preserving transfer of Haken hardness.

**Corpus / duplication audit:** Nov 2 refocus at `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` blob `033b54b87`, issue #3, AGENTS.md, CODEX.md, research skill, original R/341, LSPV-1/378 deletion-fibre, LSPV-2/390 affine indispensable counts, LSPV-2/391 MaxCut repair counterexample, and LSPV-3/395 minimum-core padding were reviewed. Those works already show related **source-ancestry** and **source-edit** failures. This report isolates a *single labelled essentiality bit* that encodes SAT on an all-UNSAT, one-proof-node image, and does not claim the general concept of clause criticality is new academic mathematics. Grok `GROKPROOF/2026-11-04_0720_PROGRESS.md` blob `06304e87` and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727`, `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob `9a5b05d6` were directly read. They address different restricted machine/portfolio models and do not establish unrestricted B3.

## Transfer implications and next gap

Retain precisely B1 (pointwise), B2 (all-input worst-case per uniform total decider), and B3 (SAT in P implies polynomial Wbar for the SAME preselected R). None has been established by this calculation. The instance can have an NP-complete-to-extract *property* while the decision/reasoning task is constant in logical node cost; thus property-acquisition hardness is not a computational invariant for deciding SAT. The next LSPV-2 target is to test nonaffine source-block invariant candidates after **fully authenticated conservative circuit extensions** and search for a genuinely stronger universal mixed-proof lower bound beyond the linear source-core floor.

## References

[1] A. Haken, "The Intractability of Resolution," *Theoretical Computer Science* 39 (1985), 297-308.

[2] S. A. Cook, "A Short Proof of the Pigeon Hole Principle Using Extended Resolution," *SIGACT News* 8(4) (1976), 28-32.

[3] S. A. Cook and R. A. Reckhow, "The Relative Efficiency of Propositional Proof Systems," *Journal of Symbolic Logic* 44(1) (1979), 36-50.

[4] S. A. Cook, "The Complexity of Theorem-Proving Procedures," *STOC* (1971), 151-158.

**External specialist review pending.** No algorithm-independent SAT lower bound, all-input machine transfer, or P versus NP proof is claimed.

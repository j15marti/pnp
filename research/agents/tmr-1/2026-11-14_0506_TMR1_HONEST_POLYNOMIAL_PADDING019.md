# TMR-1/019: honest polynomial padding saturates source observation without a processing lower bound

**Pacific timestamp:** 2026-11-14 05:06 PST (America/Los_Angeles). **Agent:** TMR-1 Machine Model Lead. **Claim:** TMR1-HPP19, CANDIDATE/RESTRICTED pending independent TMR-2/TMR-5 review. **Finite native execution:** COMPUTATIONAL. **Unrestricted 3-SAT lower bound and P versus NP:** OPEN.

## 1. Claim and exact model

Fix an ordinary explicit binary encoding E of proper 3-CNF with polynomial-time syntactic validation and the standard NP-complete SAT membership language. Let x be an E-source of **encoded bit length** L>=1, not clause or variable count. Fix an integer degree d>=2 once in the finite program and define

$$
p_d(x)=1^L\,0\,x\,0^{L^d},\qquad N=|p_d(x)|=2L+1+L^d.
$$

A padded source is valid iff its complete unary delimiter, exactly L payload bits, complete L^d zero suffix, and source E grammar all validate. Its SAT or UNSAT label is that of x; every other input is MALFORMED. The same fixed finite total deterministic multitape machine handles all input lengths. One locally moving read-only input head starts at left endmarker zero, with data at positions 1,...,N and right marker N+1. All traversals, copying, counters, arithmetic, parsing, work cells and answer outputs must be charged. No free random access, per-length program or lookup table is assumed.

**Theorem HPP19(A), conditional only on the stated ordinary E.** The padded SAT membership language is polynomial-time many-one equivalent to the original E-3SAT and hence NP-complete. Its tri-label version admits uniform polynomial-time translations in *both directions* preserving SAT, UNSAT and MALFORMED; this is not the claim that either language belongs to P.

**Theorem HPP19(B).** For each valid padded source y=p_d(x) and **every** correct fixed total tri-label deterministic machine A, its complete real execution must read every one of the L^d zero-suffix data cells. In particular,

$$
|Q_A(y)|\ge L^d=N-(2L+1)=N-O(N^{1/d}),\qquad T_A(y)=\Omega(N).
$$

The Omega(N) bound is for a locally moving physical input head, not an abstract random-access query oracle. It remains true for both SAT and UNSAT on the **tri-label** function.

**Theorem HPP19(C), essential output-alphabet audit.** For ordinary **binary** SAT membership (MALFORMED and UNSAT both NO), the suffix-bit argument applies on valid SAT inputs but does not imply suffix observation on valid UNSAT inputs. One fixed correct total binary decider can return NO on **every** valid padded UNSAT source after reading only the initial 2L+1 payload/header bits, before reading *any* of its L^d suffix bits. The constructed decider is not asserted polynomial time.

This is an honest **polynomial** encoding, unlike the exponential-padding TMR-1/018 and TMR-2/018 controls. It shows that an almost-maximal, universally mandatory source-observation certificate can be introduced by inexpensive syntactic padding even while the language retains its original NP-completeness.

## 2. Proof of polynomial equivalence and fixed-machine charges

Forward map f_d(x)=p_d(x) writes at most 2L+1+L^d bits using a fixed-degree nested counter; a one-input-head multitape transducer can count L, emit its unary header, reread/copy x, and emit L^d zeros in polynomial L time, with all output transitions paid. Malformed x maps to a malformed padded string; this holds even for length zero (a chosen standard E with empty string invalid). For the inverse g_d, parse all of y, validate the exact padded grammar, and output its E payload x. If y is malformed, output a fixed malformed E string. This is a fixed polynomial N time total translation, using ordinary counters and charged tape operations. Both preserve the three labels.

The padded membership language is in NP: parse its polynomial-length syntax and verify the underlying E-3CNF assignment, whose length is polynomial in L<=N, in deterministic polynomial time. Since f_d is a uniform polynomial-time many-one reduction from NP-complete E-3SAT, padded SAT is NP-hard and hence NP-complete. Conversely g_d reduces it to original E-3SAT. By TMR-1/018's charged polynomial-encoding equivalence, its all-A, all-k separation target is logically equivalent to the corresponding original-E target. **This equivalence is a standard reduction-level safeguard, not progress on deciding whether the target is true.**

For contrast, the encoding 1^L0x0^{2^L} is *not* a polynomial forward translation, and allows assignment brute force in polynomial time measured in its inflated N. No analogous general brute-force upper bound follows here: for fixed d, 2^L grows superpolynomially in N=Theta(L^d).

## 3. Proof of compulsory observation and of binary-output escape

Fix valid y and a suffix data coordinate j in {2L+2,...,N}. Change just y_j=0 to 1, obtaining an identical-length y^(j) with the same unary header and E payload but an invalid required suffix. The correct tri-label answers differ: A(y) in {SAT,UNSAT} and A(y^(j))=MALFORMED. If the full concrete execution of A on y never read data coordinate j, determinism and induction on **entire actual machine configurations** show that its run on y^(j) would have every same source observation, writable tape action, head move and terminal label. Contradiction. This holds separately for all L^d suffix coordinates, without an online assumption and regardless of adaptive rereads, caching, compact algebra and arbitrary polynomial or exponential workspace. Reaching the last data cell physically from left position zero requires at least N head moves. Thus HPP19(B) follows.

For binary outputs on a valid SAT x, the same one-bit change converts YES to NO, so those reads are still forced. For a valid UNSAT payload, however, every string having prefix 1^L0x is NO: it is either malformed or a valid UNSAT padded source. Build one fixed binary machine B_d as follows. Scan the header and read L payload bits. If insufficient bits or malformed E syntax, return NO. Otherwise decide E-3SAT on the extracted x by a **fully charged, finite uniform brute-force assignment algorithm**, including all intermediate operations. If UNSAT, return NO immediately, without inspecting the suffix. If SAT, physically scan and validate all L^d required zeros and the right endmarker; return YES exactly when the suffix is correct, and NO otherwise. This single machine halts correctly for every binary source length, returns NO on every malformed string, and on each valid UNSAT padded source visits no suffix data cell. It may take 2^{O(L)} poly(L) transitions in its first phase, which is explicitly allowed for this **counterexample to compulsory suffix acquisition**, not offered as a P algorithm. HPP19(C) follows.

The tri-label theorem and binary-output counterexample are compatible: they concern different output contracts. Neither one proves a mandatory superpolynomial semantic-processing cost for 3-SAT.

## 4. Exact relevance to existing research and hostile controls

- **Independent peer audit of TMR-2/018:** the source-aware deterministic replay proof applies unchanged when 2^L suffix bits are replaced by L^d; the original TMR-2 proof is valid at its stipulated tri-label scope. The new insight is that padding need not be superpolynomial to force near-total observation; here NP-completeness is retained under polynomial, two-way, charged translations. The original exponential-padding results remain unmodified.
- **TMR-1/018:** its warning about arbitrary exponentially distorting representations remains valid. This run strengthens the *limitation of observation arguments*, not the overbroad encoding-invariance claim. Input-read lower bounds need an explicit separation of syntactic validation from SAT-specific processing even under honest encodings.
- **TMR-3/017 caching:** a simulator can keep the whole source with O(N) charged workspace or use compact algebra. The bit-hitting proof counts only first observation, not recurrent processing. The same-machine observation bound is Omega(N) and is consistent with any polynomial running time or workspace.
- **TMR-4/019 and TMR-5/016 abstractions:** a cost-sound abstract path must represent these actual physical first reads if it claims a matching tri-label answer; nevertheless a valid potential based only on them is at most linear here. No abstract superpolynomial potential has been derived.
- **Hostile algorithms:** the independent finite fixture is a proper-three-distinct-variable 3-CNF *unit-forcing gadget* whose SAT answer is a one-bit consensus check; it is deliberately Horn-like/easy. Standard 2-SAT, Horn, XOR/Gaussian, bounded-treewidth, products, auxiliary variables and source-copying remain admissible cheap controllers. The general NP-complete payload remains in the theoretical theorem, not in finite fixture timings.
- **Quantifier audit:** the target remains forall A, forall k>=1, forall C>0, forall L0, exists F with A one fixed all-length total correct program, and |F| its actual bit length. Neither an Omega(N) read obligation nor NP-completeness excludes an arbitrary polynomial-time A; small-space restrictions, per-length minima and fixed superlinear exponents do not close the missing arrow.

## 5. Actually executed independent native tests

New standalone CPython code experiments/tmr/tmr1_polynomial_padding019.py executed in three independent sub-25-second fixed-degree chunks d=2,3,4. For each d every binary toy payload of lengths 1,...,6 was tested, including both labels, plus every suffix-zero flip and selected prefix flips. The toy semantic parser was independently checked using a brute-force evaluator for strict three-distinct-variable ternary clauses with private auxiliary variables, for every payload length through 5. The physical source scan explicitly uses only the **current read-only-head position** for each observation. A separate physical-prefix trace confirms that the binary NO decider never visits the suffix on UNSAT payloads. The mathematical claims apply to general E; finite tests do not.

| Measure | Actual total over d=2,3,4 |
|---|---:|
| Valid toy payloads / SAT / UNSAT | 378 / 36 / 342 |
| One-bit suffix flips proven MALFORMED by reference parser | 130,302 |
| Binary SAT-to-NO suffix-neighbor checks | 5,614 |
| Binary UNSAT runs physically stopped before suffix | 342 |
| Header/payload bit mutations audited | 1,734 |
| Independent proper ternary clause truth-table controls | 186 |
| Genuine full-scan source-head moves | 134,910 |
| Assertion failures | **0** |

Per-degree counts, fixture digests and limitations are in immutable results/raw/tmr/2026-11-14_0506_TMR1_HONEST_POLY_PADDING019_RAW.json. Each native chunk took 0.133, 0.234 or 1.842 seconds. These are **COMPUTATIONAL** checks. The Python-level parser, integer arithmetic and truth-table enumeration were **not** lowered to a charged arbitrary-multitape instruction interpreter. The all-length statements use the symbolic machine arguments in Sections 2 and 3.

## 6. Primary literature, original repository evidence and publication status

**Primary works freshly checked, with exact scope:**

1. Stephen A. Cook, *The Complexity of Theorem-Proving Procedures*, STOC 1971, pp. 151-158, https://doi.org/10.1145/800157.805047. Establishes polynomial reducibility and completeness context, not a deterministic 3-SAT time lower bound.
2. Richard M. Karp, *Reducibility Among Combinatorial Problems*, 1972, pp. 85-103, https://doi.org/10.1007/978-1-4684-2001-2_9. NP-complete reduction context, with no claimed source-bit observation theorem.
3. Leonard Berman and Juris Hartmanis, *On Isomorphisms and Density of NP and Other Complete Sets*, SIAM J. Comput. 6(2), 1977, pp. 305-322, https://doi.org/10.1137/0206023. P-isomorphism investigation, not a theorem that arbitrary padding preserves cost.
4. Harry Buhrman and Ronald de Wolf, *Complexity Measures and Decision Tree Complexity: A Survey*, Theor. Comput. Sci. 288(1), 2002, pp. 21-43, https://doi.org/10.1016/S0304-3975(01)00144-X. Certificate/query and decision-tree model distinctions, not unrestricted SAT machine separation.

Read governing replacement directive first, and fully recovered root proof1.txt (28,714 UTF-8 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), root proof2.txt from authentic Git blob (1,051,196 characters, SHA 930c5eeddafce656717f28055a7a9a755f44737c; ordinary contents endpoint blank), and canonical root main.tex from authentic Git blob (2,530,965 characters, SHA 91b4e582c16cb7f60c9aa1ea2aebf09cd4caa2c6; ordinary contents endpoint blank). Read issue #3 through TMR-4/019; AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md; five current TMR handoffs; original TMR-1/018, TMR-2/018, TMR-5/016 and relevant code/raw. Historical counterexamples retain their original status. Replacement directive overrides legacy ownership directives. No schedules changed.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither general P=NP algorithm nor unrestricted P!=NP lower-bound arrow was established. Root main.tex left unchanged for TMR-5 synthesis; TMR-1/019 requests insertion only under the authorized TMR-1 region after independent review. Do not promote this claim on tests alone.

**Next single target:** TMR-2/TMR-5 independently audit the two-way polynomial tri-label translation, the exact one-head suffix certificate, and the fixed-program binary early-UNSAT escape. Then seek an *unavoidable semantic-processing* charge that is robust even under these honest polynomial padding transformations and all polynomial workspace. No unconditional superpolynomial SAT bound is presently proved.

END_OF_REPORT::TMR-1::019::2026-11-14_0506_PST

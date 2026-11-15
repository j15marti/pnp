<!-- TMR-5 REPORT::SEPCRYPTO038::2026-11-15T02:50:00-08:00 -->
# TMR-5/038: Separator-lattice audit and the cryptographic non-interpolation barrier for the fusion transfer

**Run start:** 2026-11-15 02:49 PST (America/Los_Angeles). Role TMR-5, Independent Proof Red Team. Governing directive: `research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md` (fusion-Lipschitz). The scheduled prompt also restates the shared objective
$\overline W_R(N)=\max_{F\in\mathrm{UNSAT},|\langle F\rangle|\le N}\min_{\pi:F\vdash_R\bot}\mathrm{cost}_R(\pi)$
and the bridge $B_R:\ \mathrm{SAT}\in\mathrm P\Rightarrow\overline W_R(N)\le\mathrm{poly}(N)$.

**Verdict.** TMR-1/041's separator lattice, its uniqueness criterion, the complementary NAE_n pair and the C-SEP all-step tariff **PASS** independent review at their stated scope. One statement is **overstated** and the conclusion can be **strengthened**; both corrections are recorded below. New: **KNOWN THEOREM transfer → CONDITIONAL barrier.** The directive's §5 fusion transformer $\rho(I_n)\le O(W_R(F_n))$, if $\rho$ can be evaluated as a Boolean circuit, is a feasible-interpolation theorem for $R$. It is therefore false for every $R$ that p-simulates Extended Frege unless RSA is breakable in P/poly (Krajíček–Pudlák 1998), and false for every $R$ that p-simulates TC⁰-Frege unless Blum integers can be factored in P/poly (Bonet–Pitassi–Raz 2000). **Bridge trichotomy (PROVED/EXACT, elementary):** for every $R$ whose $\overline W_R$ already has a proved superpolynomial lower bound, $B_R$ is *logically equivalent* to SAT ∉ P. The bridge is weaker than P ≠ NP only for systems that have no known lower bound. Finite replay is COMPUTATIONAL: 16,620 checks, 0 failures. **P versus NP OPEN.**

## 1. Claims and falsifiers fixed before work

Targets: TMR-1/041 explicitly asked TMR-5 to (i) audit the uniformity behind its NP∩coNP classification, (ii) audit the conditional NP ⊄ P/poly conclusion, and (iii) replay the 64-separator control. Preselected falsifiers:
- (F1) the lattice count or the uniqueness criterion fails on some small instance;
- (F2) uniqueness without uniformity still lands in NP∩coNP;
- (F3) the stated conclusion of §4 is mis-sized;
- (F4) a legal C-SEP APPEND step discharges more than one unit, or a zero-cost step increases R;
- (F5) the directive's fusion transformer could hold for proof systems strong enough to matter.

## 2. Independent replay (COMPUTATIONAL)

Source: `experiments/tmr/tmr5_separator_crypto_audit038.py`. It uses only the Python standard library, was written independently of TMR-1's JS, and runs deterministically in about 1.7 s. Its raw output is `results/raw/tmr/2026-11-15_0250_TMR5_SEPCRYPTO038_RAW.json`; a second run was byte-compared against the raw file and matched.

| Check | Result |
|---|---|
| Exhaustive lattice, n=1,2,3, every disjoint (U,V) and every candidate table | count $=2^{\lvert\Omega\setminus(U\cup V)\rvert}$ always; unique iff $U\cup V=\Omega$; totals $3^{2^n}$ pairs, $2^{2^n}$ unique, $4^{2^n}$ tables (n=3: 6561/256/65536, matches TMR-1) |
| 64-separator control U={000}, V={001}, each a 7-clause proper 3-CNF | projections exact; exactly 64 separators |
| NAE_n complementary pair, n=3..7 | wide pair partitions $\{0,1\}^n$; an independent OR-chain/AND-chain Tseitin encoding of width ≤ 3 has projection exactly NAE_n |
| C-SEP lab, n=2, constants and inputs free, all 205 reachable wire-sets, all 16 targets | exact $R$ by fixpoint; every APPEND row satisfies $0\le R(S)-R(S')\le 1$ (0 violations); for example XOR needs 7 AND/NOT gates, OR needs 4 |

Total: 16,620 assertions, 0 failures. F1 and F4 are not triggered at these sizes. The general proofs are TMR-1's symbolic arguments, which I re-derived and accept.

## 3. Red-team corrections to TMR-1/041

**C1 (uniformity is essential; F2 confirmed as a caveat, not an error).** Take a unary undecidable set $H$ and, for each n, the constant pair: $A_n=\top,B_n=\bot$ if $n\in H$, otherwise the reverse. These have polynomial size and complementary projections, so the unique interpolant is $1[n\in H]$, which is not in NP. TMR-1 already stated uniform constructibility as a hypothesis. This control shows the hypothesis cannot be dropped. It is harmless for circuit lower bounds, because each such interpolant is a single gate.

**C2 (strengthen).** Under TMR-1's hypotheses the hard separator is the NP∩coNP language U itself. The conclusion is therefore $\mathrm{NP}\cap\mathrm{coNP}\not\subseteq\mathrm{P/poly}$, which implies NP ⊄ P/poly and hence P ≠ NP. Stating the sharper class makes clear that the route needs a general-circuit lower bound for a language that is presumably *not* NP-hard (for example, factoring-type languages). No such explicit unconditional lower bound beyond about $5n$ gates is known for any NP language.

**C3 (overstatement).** TMR-1/041 calls NP ⊄ P/poly "strictly a stronger conclusion than merely P != NP". It is at least as strong, since it implies P ≠ NP, but it is not known to be strictly stronger. Strictness would require knowing that P ≠ NP and NP ⊆ P/poly are jointly consistent or jointly true, and that is open. Correct wording: "implies P ≠ NP; the converse is not known." STALE/OVERSTATED wording only. No theorem changes.

## 4. New: cryptographic non-interpolation blocks the circuit-faithful fusion transformer (KNOWN THEOREM transfer → CONDITIONAL barrier)

**Definition.** Call a map from $R$-refutations of $A(X,Y)\wedge B(X,Z)$ to separators *circuit-faithful of degree c* if, from any refutation of cost $W$, it yields a separator whose fusion cost is $\rho\le O(W)$, and that separator is computable by an AND/NOT circuit of size $\le(\rho+n)^c$. TMR-1/041 §4 needs exactly the second clause in order to reach the circuit conclusion, and directive §5 asks for the first. Together they say that **R has feasible interpolation**, in the Krajíček 1997 sense with circuit size polynomial in proof size.

**Proposition 4.1 (CONDITIONAL on cited theorems).**
(a) If RSA is secure against P/poly adversaries, no proof system $R$ that p-simulates Extended Frege admits a circuit-faithful fusion transformer.
(b) If Blum-integer factoring is hard for P/poly, the same holds for every $R$ that p-simulates Frege or TC⁰-Frege.

*Proof.* Krajíček–Pudlák (Inform. and Comput. 140(1):82–94, 1998) build, assuming RSA is secure, a disjoint NP pair whose disjointness has polynomial-size EF proofs (via $S^1_2$) and which no P/poly set separates. Bonet–Pitassi–Raz (SIAM J. Comput. 29(6):1939–1967, 2000) do the same with polynomial TC⁰-Frege proofs, assuming Blum-integer factoring is hard. Write those propositional disjointness statements as split CNFs $F_n=A_n\wedge B_n$, which costs polynomial overhead. A p-simulating $R$ refutes them at polynomial cost $W_R$. A circuit-faithful transformer would then give polynomial-size separator circuits, contradicting the assumption. ∎

**Consequences for the shared objective.**
1. For strong systems (EF, Frege, TC⁰-Frege), the very systems where $\overline W_R$ lower bounds are open, the interpolation/fusion route to lower-bounding $W_R$ cannot work, conditional on standard cryptography. A lower bound for such an $R$ must come from a measure with no efficient circuit evaluation, i.e., **non-interpolation-based** methods.
2. For weak systems that do have feasible interpolation (Resolution, Cutting Planes, and Res(k) for small k in restricted forms), the fusion route can lower-bound $W_R$. But exponential $\overline W_R$ lower bounds are already known there (Haken 1985; Ben-Sasson–Wigderson 2001; Pudlák 1997 for CP). Proposition 5.1 below shows that their bridge $B_R$ is then exactly P ≠ NP.

## 5. Bridge trichotomy for $B_R$ (PROVED/EXACT, elementary logic)

**Proposition 5.1.** Fix a Cook–Reckhow system $R$.
(i) If $\overline W_R(N)\ge N^{\omega(1)}$ is a proved theorem, then $B_R\iff\mathrm{SAT}\notin\mathrm P$.
(ii) If $R$ is p-bounded, then $B_R$ is trivially true and gives no lower bound; p-boundedness of any system is equivalent to NP = coNP (Cook–Reckhow 1979).
(iii) Otherwise, proving $B_R$ together with a superpolynomial $\overline W_R$ lower bound proves P ≠ NP, and neither half is currently known.

*Proof.* (i): if the consequent of $B_R$ is false, the implication holds iff its antecedent is false. (ii) and (iii) follow directly from the definitions. ∎

**Reading.** For Resolution, the system used in most of the corpus's finite work, the "weakest sufficient bridge" is a restatement of the conclusion, not a weaker lemma. This matches the November 2 refocus record of Haken-based controls and the World-Ledger rule that a statement equivalent to P ≠ NP is a reformulation. The bridge is weaker than P ≠ NP only for an $R$ with no known lower bound, and §4 then rules out the interpolation route to that lower bound under standard cryptography. The user's point stands and is retained: choosing the optimal derivation for free is legitimate *for lower-bounding $W_R$*. The obstacle is the transfer $B_R$, not the min-over-derivations convention.

## 6. Barrier-transfer and PQ ledger

- **Directly transferable theorem:** feasible-interpolation failure under RSA or factoring hardness (KP98, BPR00), applied to the circuit-faithful fusion transformer (§4).
- **Structural analogy:** the collision-extraction/binding lesson in the AGENTS.md PQ ledger item 6. Here the cryptographic primitive is a hostile control and is **not** used as a hardness assumption in any claimed unconditional proof.
- **Failed transfer:** reading feasible interpolation as a lower-bound method for strong systems.
- **Relativization / natural proofs:** a circuit-faithful route whose separator lower bound is a natural property would face Razborov–Rudich under the same cryptographic assumptions. No unconditional claim depends on this.

## 7. Corpus reviewed, duplication audit, root changes

**CORPUS REVIEWED:** the fusion-Lipschitz directive; the 2026-11-13 TM-resource replacement; the 2026-11-02 worst-case minimum-derivation refocus (Haken controls); root `proof1.txt` (blob `06f7ebc8…`), `proof2.txt` (blob `930c5eed…`) and `main.tex` (pre-edit blob `6ac34c5d…`); AGENTS.md; the TMR-5 handoff; TMR-1/041 (blob `f8b3a673…`), TMR-1/038 and /035, TMR-4/042 (blob `3b83d21a…`); TMR-5/037; codex SAT-polynomial assumption audit; the World Ledger pointer.

**Predecessor check:** TMR-4/042 exists, is substantive, and was committed in b0df946a. Verified, so no recovery request is needed.

**DUPLICATION / CONTRADICTION AUDIT:** a repository search for Bonet/Pitassi/Raz, Krajíček–Pudlák RSA and "feasible interpolation" found earlier mentions of feasible interpolation as background only (TMR-1/038, TMR-5/037, LSPV-4 MODELBRIDGE). None found the cryptographic non-interpolation obstruction to the §5 fusion transformer, or the bridge trichotomy stated as such. The Haken-based B1/B2 quantifier controls of November 2 are consistent with §5 and complementary to it.

**WHAT CHANGED RELATIVE TO ROOT MAIN:** one new TMR-5 paragraph in the TMR-5-owned region.

**ADOPTED:** TMR-1/041 §§2–3, 5–7. **REJECTED (wording):** "strictly stronger". **RETIRED:** none.

**STALE OR OVERSTATED CLAIMS FOUND:** C3.

**Limitations:** the literature claims are taken from the cited abstracts and standard surveys; the full text of KP98 and BPR00 was not re-read this run. The finite replay covers n ≤ 3 (lattice), n ≤ 7 (NAE) and n = 2 (C-SEP). It did not run a physical Turing machine, compile LaTeX, or run the repository preflight.

## 8. Ranked status ledger

| Rank | Component | Status |
|---|---|---|
| 1 | TMR-1/041 separator lattice and uniqueness ⇔ cover | PASS, PROVED/RESTRICTED, independently replayed |
| 2 | Uniform complementary pair ⇒ NP∩coNP; nonuniform constant pairs show uniformity is necessary | PASS with caveat C1 |
| 3 | Conditional circuit conclusion | CONDITIONAL; correctly NP∩coNP ⊄ P/poly; "strictly stronger" overstated (C3) |
| 4 | C-SEP all-step tariff | PASS, n=2 exhaustive; initial value = minimum separator circuit size, so it is not a gap theorem |
| 5 | Circuit-faithful fusion transformer for R ⊇ EF or ⊇ TC⁰-Frege | CONDITIONAL FAIL (KP98 / BPR00) |
| 6 | $B_R$ for R with a known superpolynomial $\overline W_R$ | PROVED/EXACT equivalent to SAT ∉ P, i.e. a reformulation |
| 7 | Superpolynomial $\overline W_R$ for a strong R, by a non-interpolation method | OPEN |
| 8 | All-machine transfer; P versus NP | OPEN |

**ONE NEXT TARGET:** TMR-1 and TMR-2 should name a proof system $R$ with all three of these properties: (a) no known superpolynomial lower bound, (b) believed to lack feasible interpolation, (c) a candidate lower-bound measure that is *not* circuit-evaluable. Res(lin) over GF(2) and its stronger fragments are candidates. Otherwise, record that the fusion branch can only reprove known weak-system bounds. TMR-4 should check whether any current TMR tariff potential is circuit-evaluable, which would make it a feasible-interpolation measure.

## References

1. J. Krajíček, P. Pudlák, "Some consequences of cryptographical conjectures for $S^1_2$ and EF", *Information and Computation* 140(1):82–94, 1998, doi:10.1006/inco.1997.2674. https://dblp.org/rec/journals/iandc/KrajicekP98.html
2. M. L. Bonet, T. Pitassi, R. Raz, "On interpolation and automatization for Frege systems", *SIAM J. Comput.* 29(6):1939–1967, 2000. https://collaborate.princeton.edu/en/publications/on-interpolation-and-automatization-for-frege-systems/
3. J. Krajíček, *J. Symbolic Logic* 62(2):457–486, 1997 (feasible interpolation).
4. S. Cook, R. Reckhow, *J. Symbolic Logic* 44(1):36–50, 1979.
5. A. Haken, *Theor. Comput. Sci.* 39:297–308, 1985. E. Ben-Sasson, A. Wigderson, *JACM* 48(2):149–169, 2001. P. Pudlák, *J. Symbolic Logic* 62(3):981–998, 1997.
6. A. Razborov, S. Rudich, "Natural proofs", *JCSS* 55(1):24–35, 1997.

<!-- END_OF_VERIFIED_REPORT::TMR-5::SEPCRYPTO038 -->

# TMR-2/045: Overlapping nonlinear Feistel scales share a compact witness, and one genuine nonterminal activation collapses their rank tariff

**2026-11-15 06:09 PST, America/Los_Angeles | MULTISCALE105 | TMR-2 PNP Information Necessity.**

**Status:** PROVED/RESTRICTED for the explicitly qualified shared-gate source and authenticated record calculus, independent mathematical peer review OPEN. Replayed finite checks COMPUTATIONAL. A superpolynomial actual SAT-machine obstruction and all-correct-decider transfer remain OPEN. P versus NP OPEN.

## 1. Candidate and four preselected falsifiers

**Candidate:** Even after moving from one nonfactorizing Feistel communication interface to many overlapping scales, the sum of their exponentially large residual cofactor/rank obstructions might admit a fusion-safe fixed positive all-step tariff and create a superpolynomial initial potential.

**Preselected falsifiers:** (F1) a compact shared circuit computes all scales jointly; (F2) a correct total uniform SAT decider authenticates this canonical family and outputs a polynomial-time witness; (F3) a single authentic **nonterminal** activation discharges all latent scale ranks while costing one, after every recorded gate has separately been paid; (F4) Gaussian, Tseitin-definition, learning, equality, bounded-separator, or autarky quotients permit an even cheaper execution than the proposed lower bound. F1, F2, and F3 are realized. F4 is left conservative MAY, not forbidden.

The construction tests the *union* of overlapping rank demands, not a separate multiplication of per-stage lower bounds.

## 2. Exact corpus recovery and prior art

Governing fusion directive: research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md, blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6, read FIRST. Subsequently reviewed research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md, proof1.txt complete 28,714 chars blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343, proof2.txt complete Git blob 1,051,196 chars 930c5eeddafce656717f28055a7a9a755f44737c, main.tex complete Git blob 2,545,859 chars 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34, current issue #3 and latest comments, AGENTS.md, CODEX.md, repository research skill, all five TMR handoffs, earlier TMR-2/044 report/code/matrix, TMR-1/043 dynamic fusion report, and LEAD-0029 Lipschitz audit. Large tracker/manuscript files were fetched by full Git blob after ordinary contents reads returned empty bodies. Historical checker /341 is FAIL as full logical UNSAT authority; /386 is RESTRICTED. Neither changed.

**Prior project results explicitly reused, not claimed as new:** TMR-2/044 proves the nonlinear invertible two-shear Feistel circuit has a full affine hull, non-Schaefer interface, exact exponential permutation rank, and a polynomial SAT witness; LSPV-1/392 already proves a robust recognized-family total-decider patch. This run's new restricted result is the *same-source overlapping multiscale* construction, globally shared gate-ID accounting, genuine nonterminal joint activation row, and exact coupled multiscale tariff.

Primary background for scope comparison: T. J. Schaefer, "The Complexity of Satisfiability Problems", STOC 1978, DOI https://doi.org/10.1145/800133.804350; E. Ben-Sasson and A. Wigderson, "Short Proofs Are Narrow: Resolution Made Simple", JACM 48(2), 2001, DOI https://doi.org/10.1145/375827.375835; see original TMR-2/044 for the independently stated Feistel algebra and caveat that no cryptographic security or general SAT hardness is asserted.

## 3. Explicit nested shared-input proper-3CNF family

For integer m>=5, take the SAME original input vectors X=(x_1,...,x_m) and Z=(z_1,...,z_m). For each scale j=5,...,m, define over GF(2) the quadratic form and mixing vector

$$
Q_j(t)=\bigoplus_{\substack{1\le a<b\le j\\\{a,b\}\notin E(C_j)}}t_at_b,\qquad
(g_j(t))_i=Q_j(t)\oplus t_i t_{i+1},
$$

with cyclic indices i+1 mod j and E(C_j) the j-cycle. Define the reversible two-shear map on the *overlapping prefix* (X_[j],Z_[j]):

$$
U^{(j)}=X_{[j]}\oplus g_j(Z_{[j]}),\qquad
V^{(j)}=Z_{[j]}\oplus g_j(U^{(j)}).
$$

For every j, construct the same exact AND/XOR Tseitin circuit as TMR-2/044. A global structural hash (gate type plus its two predecessor wire identities, sorted for commutative AND/XOR) REUSES a gate when another scale literally computes the same primitive with the same inputs. Each authentic shared gate is charged **once**. The resulting source F_m is the conjunction of every gate definition at every scale, including original binary-to-proper-3CNF padding pairs, with a uniform sign flip on odd-indexed original X variables in all their occurrences. Every source clause has exactly three distinct variables. The original X and Z variables are shared; other wires have globally distinct IDs unless genuine structural hashing merges an identical gate.

Let G_m be the actual number of distinct shared AND/XOR identities. Then

$$
G_m\le\sum_{j=5}^m(2j^2-2)=O(m^3),
\qquad |F_m|_{\rm bits}=O(m^3\log(m+2)),
$$

for canonical binary-indexed source syntax (the executable's ASCII bytes are reported separately). This growing family is polynomial-time printable. All gates are constructible and all clauses are verifiable in polynomial time, with the exact explicit witness X=0, Z=0 before the uniform odd-X sign flip and every gate/padding wire equal to its evaluated value. Neither the complete all-zero nor all-one assignment satisfies F_m. Signed renaming and clause duplicate controls remain honest alternate encodings, not automatically recognized by the canonical-string fast path.

**Theorem 045-A (simultaneous interface projection; PROVED/RESTRICTED).** Fix any j in [5,m]. Existentially project F_m onto X_[j],Z_[j],U^(j),V^(j) and eliminate all other wires and inputs. The resulting relation is exactly the graph of the displayed two-shear bijection. In particular its 2^(2j) by 2^(2j) communication matrix has rational rank and minimum all-one rectangle cover exactly

$$
R_j=2^{2j}=4^j.
$$

**Proof.** Every gate definition enforces its Boolean truth function, and the padding pair preserves its original binary clause. Given any total X,Z, each scale's circuit has a unique gate-wire evaluation, so all scales can be satisfied simultaneously without imposing additional restrictions on X,Z. Thus removing the other scales leaves exactly the j-th input/output graph, including the harmless fixed X gauge flip. The inverse is Z_[j]=V^(j) XOR g_j(U^(j)) and X_[j]=U^(j) XOR g_j(Z_[j]); hence the graph is a permutation of 2^(2j) inputs. Its matrix is a permutation matrix, with rank and all-one rectangle cover both 2^(2j). QED.

TMR-2/044's full-affine-hull and nonfactorizing/non-Schaefer statements apply to EACH individual projected j-interface (j>=5). Different j have different external arities and ranks and share input bits, so their raw rank contributions cannot be regarded as independent costs. This report does NOT assert inequivalence after an unrestricted cheap compact-circuit quotient: the explicit circuits themselves defeat that assertion.

## 4. Authenticated shared-DAG record transition system

This is a **separate exact record calculus**, not a physical multitape SAT-machine simulation. State is C=(F_m,G_m,P,a,h,v), where F_m and its gate DAG G_m are preauthenticated, P is the set of uniquely paid CHECK gate identities, a in {0,1} is a nonterminal global activation flag, h in {0,1} is unfinished HALT, and v in {0,1} is freely reversible view metadata. Legal transitions are exhaustive:

1. VIEW(v=0/1) and NOP cost 0, no alteration of source, P,a,h.
2. CHECK_ID(g) cost 1, only when a=0 and gate g not already in P, adds exactly this gate to P. All original AND/XOR obligations remain required.
3. ACTIVATE cost 1, only when P is the entire G_m and a=0, sets a=1 but leaves h=1. **This is not HALT.** It activates all previously verified scale outputs in one authentic charged record event.
4. HALT cost 1, only with a=1 and h=1, sets h=0. Goals are absorbing, and require a=1,h=0,P=G_m.

No hidden free computation, path deletion, one-step bulk gate creation, or source oracle is included. If transferred to a richer machine, all additional concrete operations must be admitted as MAY and reaudited. Legitimate source-witness recognition is allowed in the actual SAT decision problem but is outside this deliberately qualified record-completion service.

The authentic zero-cost closure is the two-state reversible VIEW SCC for each fixed (P,a,h). The obstruction below is identical on both presentations, so **no free path decreases it**.

Define

$$
S_m=\sum_{j=5}^m(R_j-1)
=\frac{4^{m+1}-4^5}{3}-(m-4).
$$

The seven-column reduced-product vector is

$$
\mathbf p(C)=
(0,\ 0,\ (1-a)S_m,\ 1-a,\ G_m-|P|,\ 0,\ h).
$$

The SEP coordinate is deliberately raw exponentially amplified multiscale interface rank. The FUS coordinate is one genuine activation obligation; GAMMA counts every unpaid distinct shared primitive; MACHINE counts true unfinished HALT. Every coordinate is nonnegative, closure invariant, and vanishes at completed goals.

## 5. Exact full rule tariff and exact rational LP

| Authentic transition | Cost | SEP discharge | FUS discharge | GAMMA discharge | MACHINE discharge |
|---|---:|---:|---:|---:|---:|
| VIEW / NOP | 0 | 0 | 0 | 0 | 0 |
| CHECK_ID | 1 | 0 | 0 | 1 | 0 |
| ACTIVATE (nonterminal) | 1 | S_m | 1 | 0 | 0 |
| HALT | 1 | 0 | 0 | 0 | 1 |

All other columns CNF, AFFINE, INTERFACE have zero discharge. Thus for nonnegative weights the **complete necessary and sufficient tariff cone** is

$$
\lambda_\Gamma\le1,\qquad
S_m\lambda_{\rm SEP}+\lambda_{\rm FUS}\le1,\qquad
\lambda_{\rm machine}\le1.
$$

No other transitions are silently excluded from *this record calculus*. A rank-only weight lambda_SEP=1 is defeated by the one cost-one ACTIVATE, which discharges S_m even while h stays 1. This is a stronger timing control than relying on a final terminal mask.

The initial potential is

$$
\Phi(C_0)=S_m\lambda_{\rm SEP}+
\lambda_{\rm FUS}+G_m\lambda_\Gamma+\lambda_{\rm machine}.
$$

The exact optimum is

$$
\boxed{\max_{\lambda\ {\rm feasible}}\Phi(C_0)=G_m+2.}
$$

**Proof.** The tariff inequalities bound the three displayed blocks of initial potential by 1, G_m and 1 respectively. Uniform rational weights (lambda_CNF,lambda_AFFINE,lambda_SEP,lambda_FUS,lambda_GAMMA,lambda_INTERFACE,lambda_MACHINE)=(0,0,0,1,1,0,1) attain G_m+2. A real complete trace consists of G_m distinct CHECK_ID events, one ACTIVATE and one HALT, so its cost is exactly G_m+2. Conversely each G_m gate is a mandatory distinct CHECK and both additional events are mandatory; the lower bound matches. QED.

If each scale receives an independent weight lambda_j, the authentic joint ACTIVATE row is

$$
\sum_{j=5}^m(4^j-1)\lambda_j+\lambda_{\rm FUS}\le1.
$$

Consequently **all scale-rank charges together contribute at most one**, not a product or a sum of independently calibrated stage prices. A fixed positive uniform lambda_SEP is impossible over unbounded m. Choosing m-dependent exponentially small rank coefficients cannot improve G_m+2. Since encoded input length grows at least m and G_m=O(m^3), the **optimal valid initial gap is polynomial**, not superpolynomial.

A correct SAT decider can also compute the canonical generator, compare the input exactly, emit the constructive witness/answer when matched, and run a fixed total exhaustive fallback otherwise. Enumerating indices j<=input length gives a polynomial-time *canonical-family* recognizer because the source generator is polynomial-time and input length >=m. This is the recognized-family patch principle already rigorously recorded in LSPV-1/392; it is not an unrestricted SAT algorithm. It separately defeats any claim that this particular explicit polynomially printable, known-label family is difficult for EVERY correct total SAT decider.

## 6. All required cheap controls and source honesty

Affine/Tseitin and Gaussian elimination: exact XOR and AND definitional gates are explicitly present; unrestricted Gaussian/definition processing is NOT charged as a new hardness obligation. Horn, dual-Horn, 2-SAT/Krom/SCC: local projected interfaces are nonlinear/non-Schaefer per TMR-2/044, but these classifications do not prevent a cheap shared witness. Treewidth/separator DP: potentially useful; no treewidth-to-time claim is made, and any valid decomposition remains MAY. Autarky/private variable elimination: any certified deletion is allowed in an actual solver, not declared impossible. Equality/union-find and renaming: elementary equality and gauge transformations provide no tariff by themselves. Extension variables and shared circuits: gates are explicit, structural sharing is actually applied and CHECK IDs are globally deduplicated. Learning, preprocessing, caching, rereading, recomputation and branch sharing: all legal actual-machine shortcuts remain available and may only reduce decision time. Padding: the two-clause proper-3CNF pads are fully encoded and byte-counted; size is not inflated for a purported lower bound. Both all-zero and all-one full source controls fail, while a verified nontrivial assignment exists. The historical exact-2P2N near-q-Horn radius remains a separate **RESTRICTED** component, not a branch-count claim.

No physical-machine transition count for generating/recognizing the source is asserted by the record tariff. The separate algorithmic patch requires normal polynomial accounting for parsing, all generated bytes, comparison, witness verification and fallback. It can be compiled into a fixed finite deterministic multitape program with a polynomial overhead, but this report does not provide a compiled TM binary or exact transition trace.

## 7. Reproducibility, interpretation, and handoff

Exact executable: experiments/tmr/tmr2_multiscale_activation105.js, source Git blob 5765946d4ac916ad6c529de51b688643a9e63516. Fresh source-byte V8 replay completed **179,822 assertions, zero failures** on m=5..9. Exhaustive per-scale permutation/inverse checks include all j<=7; exhaustive whole-source assignments at m=5,6; sampled whole-source controls at m=7,8,9. Mathematical all-m results rely on the proofs above, not finite tests.

Separate evidence: results/raw/tmr/2026-11-15_0609_TMR2_MULTISCALE105_V8_RAW.json and results/raw/tmr/2026-11-15_0609_TMR2_MULTISCALE105_TARIFF.json. Finite gate counts and source ASCII bytes: m=5 (48,2589), 6 (107,6429), 7 (186,11628), 8 (288,18378), 9 (416,26881). Corresponding exact optimal record-work costs: 50,109,188,290,418. All codes and tables are reproducer evidence, not independent asymptotic proofs.

**TMR-3:** audit whether a genuine physical algorithm can preactivate or record shared outputs at even lower charge; never map this record grammar directly to TM transitions. **TMR-4:** include a single nonterminal activation row in any richer machine's cost-sound MAY closure; verify the coupled multiscale LP. **TMR-5:** independently audit same-source projection, global gate identity hash, and absence of a free shortcut in the *qualified* record calculus. **TMR-1:** preserve the universal-decision-machine and same-system transfer gate, and audit any inappropriate fixed explicit known-label family hardness quantifiers.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt, proof2.txt, main.tex and all five existing agent schedules remain untouched. Superpolynomial initial tariff, same-system all-decider SAT transfer, and P versus NP remain OPEN.

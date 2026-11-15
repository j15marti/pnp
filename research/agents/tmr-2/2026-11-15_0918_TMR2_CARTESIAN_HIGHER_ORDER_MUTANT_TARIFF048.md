# TMR-2/048: Cartesian higher-order SAT-mutant certificates and exact physical tariff

**2026-11-15 09:18 PST | TMR-2 / PNP Information Necessity.** PROVED/RESTRICTED source-specific theorem; independent mathematical review OPEN. Finite observations COMPUTATIONAL. P versus NP OPEN.

## Candidate, immediate falsifiers, source recovery

**Candidate (stated before literature/corpus search):** An UNSAT CNF with no *single-sign* SAT neighbor might still force a correct general SAT decider to read many source signs, because every counterfactual SAT neighbor changes one sign in each of several contradictory components. The right dynamic obstruction is the minimum input hitting set of still indistinguishable SAT mutants, not the number of mutants.

**Falsifiers:** (1) a claimed Cartesian sign mutant is malformed or unsatisfiable; (2) a correct total decider rejects while each component has an unread authentic sign; (3) zero-cost closure changes source-read history; (4) one authentic paid source step reveals multiple previously unread sign positions, or an inexpensive permitted algorithm defeats the potential. All are tested or explicitly model-scoped. Real cheap executions remain legal.

**Primary literature:** N. Nisan, “CREW PRAMs and Decision Trees,” *SIAM Journal on Computing* 20 (1991), 999-1007, DOI https://doi.org/10.1137/0220062; H. Buhrman and R. de Wolf, “Complexity measures and decision tree complexity: a survey,” *Theoretical Computer Science* 288 (2002), 21-43, DOI https://doi.org/10.1016/S0304-3975(01)00144-X. Certificate complexity and sensitivity are classical. This is a new explicit source-specific tariff calibration, not a new generic decision-tree theorem. Neither paper yields a lower bound for unrestricted polynomial-time SAT.

**Recovered repository state:** Read first governing 2026-11-14 Fusion-Lipschitz refocus (blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6); then 2026-11-13 TMR replacement directive; complete root proof1.txt (06f7ebc8c2283304a0f5200b518c6e48fa41e343), complete proof2.txt (930c5eeddafce656717f28055a7a9a755f44737c), complete root main.tex (6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34), issue #3 including latest peer posts, AGENTS.md, CODEX.md, research skill, and five current TMR handoffs. The directly relevant original report and executable are TMR-2/047 (PHYSICAL_SIGN_FUSION_TARIFF047.md) and experiments/tmr/tmr2_sign_fusion047.js (blob 21db9a00d1583206ae89fa669165d95e13e1ab43), supported by TMR-1/045 and historic LSPV-4/499,/506 single-sign witnesses. The local one-sign pivotal Tseitin lemma is inherited. TMR-3/047, TMR-4/048, and TMR-5/044 study other preauthenticated fused record authorities and cannot be substituted. The exact-2P2N near-q-Horn radius remains RESTRICTED as a syntax component, not a general branch theorem. Historical /341 FAIL as full UNSAT logical authority; /386 RESTRICTED. No root file or schedule was changed.

## Authentic growing CNF family

For integers m>=2 and r>=2 take r disjoint copies B_m^(i) of the original TMR-2/047 odd-charge circular-ladder cubic-graph Tseitin proper 3CNF. Each component has H=4m degree-three vertices, E=6m edge variables, 16m proper ternary clauses and q=48m independently authentic literal-sign coordinates. Each untouched copy is UNSAT: xor of all vertex parity constraints is 0=1. For EVERY one of its q signs, flipping that sign alone makes that copy SAT, with a constructive G minus v spanning-tree assignment satisfying all its other vertex equations.

Concatenate the r copies with disjoint variable ranges in one exact signed counted binary source encoding F_(r,m). The header consists of 00110101, gamma(6mr), gamma(16mr), followed by 48mr variable-index/polarity occurrences with index width w=ceil(log2(6mr+1)). Honest encoded bit length is

$$N_{r,m}=8+\ell_\gamma(6mr)+\ell_\gamma(16mr)+48mr(w+1)=\Theta(rm\log(rm)).$$

Let B_i be the set of q positions corresponding to the literal-sign bits in component i. For every tuple b=(b_1,...,b_r) in B_1 x ... x B_r, the binary formula obtained by toggling exactly these r positions is **valid and SAT**: each component independently becomes SAT on its own variables. These q^r explicit mutants are distinct. Any SINGLE sign flip leaves r-1 independent contradictory components unchanged, and so the full CNF stays UNSAT. The vanishing first-order sensitivity assertion concerns only these authentic sign positions, not arbitrary malformed or header-bit changes.

For r=m, q^r=(48m)^m is superpolynomial in honest input length N=Theta(m^2 log m). This is semantic counterfactual multiplicity, not time or source entropy.

## Concrete physical machine, zero-cost closure, and goals

Fix ANY one correct total deterministic 3CNF-SAT decider A using a read-only original binary input tape with ONE local original-source head, and any finite constant number of finite-alphabet local work tapes. Every original-source read, work action, reread, write, copy, recomputation, Gaussian step, learning, output and HALT costs one genuine physical transition. At most ONE previously unread original source position can be observed in a transition. The full concrete configuration includes original source, A, control, all heads/tapes, and a mathematical *ghost* R(C) recording which original input positions have actually been read in THIS execution. The ghost is not program advice or a free computational service.

There are no zero-price physical machine steps. Optional reversible VIEW aliases change only presentation metadata, not A, source, tapes or R, so authentic zero-cost SCC quotient preserves all obstruction components. Unknown operations remain MAY; extra source input ports or random access require a different tariff and are not silently forbidden.

A completed goal on original F_(r,m) must be a rejecting HALT because the source is UNSAT. This source is not under a promise: A must also be correct on every SAT mutant and on unrelated valid or malformed inputs according to its fixed parser.

## Exact dynamic input-hitting component

Set u_i(C)=|B_i\setminus R(C)|, the number of still-unread signs in component i. Define explicit still indistinguishable mutant-difference hyperedges

$$\mathcal E(C)=\{\{b_1,\ldots,b_r\}:b_i\in B_i\setminus R(C)\}.$$

When all u_i>0, select one still-unread sign from each component. The resulting SAT source agrees on EVERY bit read by A so far, hence the deterministic trace must be the same through C. A correct total SAT decider cannot reject here. Thus every completed rejecting goal has at least one u_i=0, even if the machine uses completely different representation and computation than an XOR solver.

The minimum cardinality of a hitting set of all Cartesian edges is EXACTLY min_i u_i: reading every unread sign in one component hits every tuple; reading fewer than each u_i leaves at least one unhit sign in every component, whose tuple avoids the read set. This is the classical certificate/adversary lower-bound argument on the **actual original input bits**.

Use the seven-vector

$$\mathbf p(C)=(0,0,\min_i u_i,\mathbf1[\min_i u_i>0],0,\prod_i u_i,0).$$

Columns are CNF, XOR, SEP, FUS, Gamma, Interface, Machine. The SEP component is the residual hitting number; FUS indicates an outstanding jointly satisfiable SAT counterfactual; Interface counts explicit uneliminated Cartesian counterfactuals. This is NOT a claim that the machine stores a gigantic table. Every component is unchanged by authentic zero-cost VIEW; every completed genuine rejecting goal has vector zero.

## Complete physical read-effect tariff and exact dual

A genuine price-one transition observing a NEW critical original sign in component j lowers u_j by one. Let b=min_(i!=j)u_i and Q_j=product_(i!=j)u_i. Its exact discharge is

$$\Delta_{\rm SEP}=\mathbf1[u_j\le b],\qquad
\Delta_{\rm FUS}=\mathbf1[u_j=1,\ b\ge1],\qquad
\Delta_{\rm Interface}=Q_j.$$

If another component is already complete, b=0 and the appropriate SEP/FUS/Interface discharges vanish. Every work step, copy, learned inference, original noncritical read, repeated sign read, input movement without a fresh critical sign, or HALT has zero discharge. An optional zero-price VIEW also has zero discharge. These are an exhaustive **effect partition** of actual paid physical microsteps, not a claim that a real SAT decider is restricted to an artificial record calculus.

Since 0<=u_i<=q, every possible discharge is coordinatewise bounded by (1,1,q^(r-1)). The bound is *attained by an authentic transition*: a fixed correct scanner-then-SAT decider scans the original input from left to right, and its last sign read of the first component has u_1=1 and all other u_i=q. That step discharges (1,1,q^(r-1)) at price one. This decider's eventual SAT fallback remains a valid total correct implementation. Thus the COMPLETE nonnegative tariff cone on these three active coordinates, when required for all such physical deciders, is

$$\boxed{\lambda_{\rm SEP}+\lambda_{\rm FUS}+q^{r-1}\lambda_{\rm Interface}\le1.}$$

Initially p=(0,0,q,1,0,q^r,0). Exact rational LP primal and paid-row dual certificates are

$$\boxed{\max_{\lambda\ge0}\Phi(F_{r,m})=q=48m.}$$

Primal: lambda_SEP=1, all other active lambda=0. Dual: multiply the authentic dominating price-one row q times, obtaining component capacities (q,q,q^r) which dominate initial (q,1,q^r), at total dual price q. For weights uniform across growing r=m, lambda_Interface must equal zero. The exponential raw mutant count is cancelled by the authentic exponential *one-read* joint discharge.

**PROVED/RESTRICTED actual same-machine necessity:** Every correct total deterministic SAT decider with the specified local original-source head must read all q signs of at least one original odd-charge component before rejecting F_(r,m). Therefore T_A(F_(r,m))>=q=48m. This is a true physical transition lower bound for every such A on the same exact source, but is polynomial and does not settle P versus NP.

## Mandatory hostile controls and real shortcut

Affine / Tseitin: one fixed total correct SAT decider can identify complete four-clause ternary XOR pattern groups, convert them to GF(2) equations, and run Gaussian elimination when all source clauses are so covered. It falls back to exhaustive SAT search for all other inputs. This exact family is accepted for parity refutation in polynomial time, so a superpolynomial claim here is FALSE. Parsing and reads are charged.

Horn, dual-Horn, Krom/2SAT: standard propagation and implication-SCC algorithms remain permitted, with no invented difficulty assigned to those controls. Separator/width: each ladder copy has bounded primal treewidth, and disjoint union preserves that bound. Ordinary separator DP is polynomial. Certified autarkies, equality/union-find, preprocessing and clause subsumption may simplify constraints after authentic input acquisition. Compact circuits, auxiliary/Tseitin definitions, extension variables, learning, sharing and AND reconvergence are all unrestricted; no prescribed DAG cost is inferred. Input rereading, caching and recomputation have their real costs but cannot create a SECOND first read. Renaming, literal flips, padding, alternate encodings and extra source ports require explicit requalification if changed. The stated model keeps one original head, not a zero-cost multiport oracle.

A single bit read can discharge q^(r-1) simultaneously distinct explicit SAT counterfactuals. Neither q^r mutants, r-scale AND combinations, Shannon entropy, state count, padded source, nor semantic multiplicity is time. There is a polynomial affine shortcut. The same-system physical linear input-transfer gate PASSES; a superpolynomial initial gap and all-program superpolynomial SAT bound remain OPEN. Known /341 and /386 guards retained without repair.

## Reproducible evidence, peer handoff

Reproducible self-contained JS at experiments/tmr/tmr2_cartesian_mutant_tariff048.js; exact V8 JSON at results/raw/tmr/2026-11-15_0918_TMR2_CARTESIAN048_V8_RAW.json; seven-column matrix at results/raw/tmr/2026-11-15_0918_TMR2_CARTESIAN048_TARIFF_MATRIX.json. The published JS was executed in V8 over 25 parameter pairs m=2..6,r=2..6: **781,024 assertions, zero failures; 11,616 actual constructed SAT mutants; 159,504 authentic physical sequential source-read effects; 159,504 zero-change VIEW controls; 20,480 exhaustively evaluated small original component truth assignments**. For r=2,m=2, all 96^2=9,216 Cartesian SAT mutant tuples were individually checked. For r=m=6, q^r=288^6=570630428688384 counts explicit valid SAT-mutant *tuples by proof*, not exhaustive computation; maximum genuine one-read interface discharge is 288^5=1981355655168. Witnesses use the original G-v spanning-tree construction; no compiled low-level physical TM was executed. Finite evidence is COMPUTATIONAL, all-parameter conclusions follow from symbolic arguments and await independent peer math review.

**Peer requests:** TMR-3 and TMR-4 audit the authentic joint physical last-first-copy sign row Delta=(1,1,q^(r-1)), w=1, and exact three-weight inequality. TMR-5 independently replay r-bit mutant SAT witnesses and source-encoding validity. TMR-1 preserve the source-specific one-original-head quantifiers and the polynomial affine shortcut; do not promote the model to unrestricted superpolynomial SAT.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** proof1.txt, proof2.txt, canonical main.tex and all five current agent schedules untouched.

**Next:** Seek an obstruction for which certificate hitting remains large AFTER all algebraic/circuit/learning/preprocessing controls, without identifying source-query necessity with superpolynomial machine work.

END_OF_REPORT::TMR2_CARTESIAN048::2026-11-15_0918_PST

# LSPV-1/533: exact charge-classifier degree and sharp logarithmic AND-depth qualification

**2026-11-09 04:00 PST | Route B lead | PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**
New restricted evidence node **[P2-L1-533]**, refining **[P2-L1-532]**, **[P2-L1-530]**, **[P2-L5-458]**. Primary OPEN dependencies remain **[P2-D1]**, **[P2-C3]**, **[P2-B1]**, **[P2-B2]**.

## IDEA -> SEARCH -> ITERATE; falsifiers declared before search

**Initial hypothesis.** The previous one-sided separating-polynomial threshold ceil(b/2) [P2-L1-532] can be strengthened for the DIFFERENT objective of computing the **entire exact charge predicate** on the original one-hot inputs. An exact Boolean charge classifier has degree b over GF(2) when q is odd, which implies only a logarithmic AND-depth lower bound even when branching and subcomputation sharing are permitted inside the circuit comparator.

Predeclared falsifiers: (F1) an odd-q exact charge indicator has a representation of degree <b; (F2) its full-support Fourier coefficient vanishes in characteristic two; (F3) a polynomial-size balanced q-state adder cannot realize the same function with O(log b) nonlinear depth; (F4) the claim is indistinguishable from the previously proved one-sided separator [P2-L1-532]. F1/F2 were rejected by proof and finite checks; F3 fails because the explicit balanced construction exists; F4 clarifies the *distinct output obligation* and prevents promotion to proof-system hardness.

**Search/audit.** Read complete main-branch root trackers proof1.txt (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; 18,553 bytes) and proof2.txt (prewrite blob cc404ff0d73f6868ef28a4fb1ba4427b9d95dca3; 712,458 bytes), issue #3 including latest LSPV-5/458 comment, AGENTS.md, CODEX.md, project SKILL, Nov 2 governing handoff, Nov 9 topology handoff, LSPV-1/532, LSPV-3/531, LSPV-5/458, Grok REWIRE and Claude TPORT2. Existing full/one-sided degree controls were checked for overlap. New required external repositories: konard/p-vs-np (main ec​edd2b45f1c524d85c00b2da27a9c140025550c; shared finite-machine model proofs/complexity/README.md) and blkph0x/p-vs-np-proof-research (main 7dedc73f758dfbdc072e7aa29dfc08505761ebd5; affine_projection_recognition_lab/fixed_width_hierarchy/THEOREM.md), both scoped, not unrestricted P-NP results. Also read actual meelgroup/frat-xor/main/README.md (external XLRUP checker, NOT native R_mix341) and prior project source experiments/arc/lspv1_532_fourier_degree.py. External primary context Pang arXiv:2610.00837v2 and Cook-Reckhow (1979), with Haken (1985) Resolution and Cook extended Resolution as controls. Web search confirmed Pang theorem is for fixed bounded-degree polynomial rules and not all mixed rules. Google-specific search availability was not independently established. Exact historical native accepted-byte grammar still unavailable to this run.

**Iterate.** Exact classification degree is b, whereas a *single nonzero polynomial that merely vanishes on correct assignments* first exists at degree ceil(b/2). Neither statement is by itself a lower bound for shared refutation DAGs. The degree-to-depth implication is logarithmic and matched asymptotically by a compact nonlinear Boolean circuit, under a separately specified gate model. This upper control must be admitted rather than excluded.

## Theorem 533.1: exact Boolean indicator, PROVED/RESTRICTED

Fix odd q>=3, b>=1, signed coefficients eps_i in {+1,-1}, c in Z_q. On b groups of exactly-one q-state indicators X_{i,a}, define the Boolean function

$$
f_{q,b,c,\epsilon}(x)=\mathbf{1}\{\sum_{i=1}^{b}\epsilon_i x_i=c\pmod q\}.
$$

The minimum GF(2) multilinear algebraic degree of any polynomial in the **original indicators** agreeing with f on every exactly-one assignment equals **b**:

$$
\deg_{\mathbb F_2}(f_{q,b,c,\epsilon})=b.
$$

*Upper bound.* The original-indicator sum of minterms

$$
f=\bigoplus_{\substack{a\in(\mathbb Z_q)^b\\\sum_i\epsilon_i a_i=c}}\ \prod_{i=1}^b X_{i,a_i}
$$

has degree <=b and is exact under the promised one-hot domains.

*Lower bound.* Work over a characteristic-two extension field K containing a primitive q-th root of unity zeta, which exists because q is odd. Fourier inversion on Z_q^b gives a nonzero coefficient zeta^(-tc)/q at every character with frequency (t eps_1,...,t eps_b), 1<=t<q. These frequencies have ALL b coordinates nonzero. A polynomial of degree <b in the original indicators restricts to a sum of terms each depending on fewer than b input groups; every such term has zero Fourier coefficient at any full-support frequency. Contradiction. Since the polynomial coefficients may be embedded from GF(2) to K, the lower bound holds over GF(2).

**Distinct from [P2-L1-532].** That earlier result proves the minimum degree ceil(b/2) for *one-sided separators* which vanish on valid charge tuples and reject AT LEAST ONE invalid tuple. The present theorem concerns ONE OUTPUT equal to the full predicate on EVERY valid and invalid tuple. A conjunction or family of many lower-degree separators is NOT ruled out.

## Corollary 533.2: limited nonlinear depth, PROVED/RESTRICTED

In a separately specified acyclic Boolean circuit with constants, NOT, XOR, AND gates of fan-in at most 3, define D as the maximum number of AND gates on any input-output path; XOR/NOT gates do not add to D. Expanding all wires as GF(2) polynomials proves by induction

$$
\deg(f_{\mathrm{output}})\le 3^D.
$$

Therefore any circuit whose single output computes the exact odd-q charge classifier on all promised original one-hot assignments has

$$
D\ge \lceil\log_3 b\rceil.
$$

This counts nonlinear depth, **not** total distinct inference work, physical time, evidence bits, or historical R_mix341 steps. No AND3 shape, constants, repeated ports, wire-export permissions, or native conversion are assumed for R_mix341.

**Mandatory matching upper control (different XOR/AND2 circuit model).** Combine pairs of one-hot q-state groups using

$$
Z_k=\bigoplus_{a+d=k\pmod q}(X_a\land Y_d).
$$

Each pair requires q^2 paid AND2 and q(q-1) XOR2 gates, and preserves exactly-one inputs and outputs. A balanced tree on b signed groups computes f as output bit c using q^2(b-1) AND2 and q(q-1)(b-1) XOR2 gates, AND-depth ceil(log_2 b). Sign changes are fixed input-index permutations. Thus at fixed odd q the minimum nonlinear depth is Theta(log b), whereas an explicit O(b)-gate construction exists. This is an **upper-bound circuit control** and not a native R_mix341 refutation, even if a different proposed calculus can encode the gates.

## Family/theorem/encoding/known-method/transfer ledger

**Family:** opposite-characteristic Z_3 Tseitin on connected cubic expander G_h with h vertices, nonzero total vertex charge; original project strict signed 3-CNF uses 3-state one-hot edge groups, one ALO per edge and 18 forbidden signed 3-clauses per degree-three vertex, giving 39h/2 source clauses where this source convention applies. **Published hard-system theorem:** Pang (2026), arXiv:2610.00837v2, exponential restricted Res(PC_r/F_2) size for specified fixed r and opposite-characteristic families and assumptions; check source-specific encoding/simulation directions before identifying exactly with the project's variant. **Known shortcuts:** source-authenticated K4 ordinary Resolution upper [P2-L1-527], local ER2 inverse/cancellation [P2-L1-524]/[P2-L1-526], compact nonlinear one-hot adder [P2-L5-458]. **Remaining transfer:** the currently unproved native R_mix341 original-source checker/normalization [P2-D1]/[P2-C3], superpolynomial lower bound allowing every mixed rule [P2-B1], and noncircular same-calculus B3 [P2-B2]. Lower bounds for only ResPC and gate depth do NOT establish any of those four obligations.

## Independent finite replay and resource qualification

Independent Python control executed at /mnt/data/lspv1_533_full_charge_degree.py: **14 configurations**, 2,276 coefficient checks and 2,276 exhaustive classifier-output reconstructions, odd q=3,5,7. Duration 0.543 seconds in the local run, NOT SAT machine time. GitHub-published independent JavaScript verifier: **17 odd-q configurations** including q=9, 452 nonzero top mixed-derivative evaluations and 553 local ternary/binary q-state adder-pair checks; even q=2 parity is the hostile negative control. All checks passed.

Published JS experiment: experiments/arc/lspv1_533_exact_charge_indicator_gate_depth.cjs. Published raw: results/raw/arc/2026-11-09_0400_LSPV1_533_EXACT_CHARGE_GATE_DEPTH_RAW.json. The scripts brute force bounded q^b input domains, with deterministic finite enumeration; they do not prove a general proof-system bound. Finite code storage is explicitly paid, not a free oracle. Python generated raw evidence is separately available in this run's sandbox; no claim of executing the historically authoritative checker. A conservative finite implementation bound for the JS enumerator is O(q^b b + (q-1)^b 2^b b) work and O(q^b b) simultaneous transient data cells before output; the actual machine peak was not instrumented. These are NOT exponents for FLMV, and parsing, source retrieval, publishing and failed search are excluded from the circuit lower-bound ideal minimum but are charged separately for any future implemented upper-bound transfer. The separate algebraic balanced circuit has O(q^2 b) gate cost and O(q b) stored live group bits under a suitable schedule, subject to explicit machine representation overhead.

**Scope/falsifiers:** Validity relies on odd q, the original exactly-one domain, an EXACT single-output function, a GF(2) multilinear degree metric and the specified comparator gates. Even-q parity and one-sided separator controls refute any unjustified wider reading. The q=3 compact shared adder is a concrete reason not to promote degree bounds to superpolynomial mixed-rule work. [P2-D1]/[P2-C3]/[P2-B1]/[P2-B2] stay OPEN.

TRACKER ACTION: new material restricted evidence is eligible for [P2-L1-533], not for a status promotion of any load-bearing node. Root main.tex was not edited because a complete safe read is unavailable. Retain exactly FIVE roles, TWO Route A and THREE Route B, historical weights and schedules.

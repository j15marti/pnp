# AFFINE-LUMPABILITY-RANK-GATE55

**Timestamp:** 2026-10-22 03:48 Asia/Seoul  
**Scope:** one bounded synthesis across the existing five roles. Circuit-SAT is a comparison/representation experiment, not a third P-vs-NP route.  
**Global status:** **P versus NP OPEN. P versus RP OPEN.**

## 1. Inputs and repair hypotheses

The newest substantive accessible role report was `RP-EARLY-AFFINE19` from :36. The user-supplied `DIGEST-LUMP19` handoff was available as exact prompt text, but its stated `/mnt/data` artifacts were not presumed accessible and no GitHub artifact existed. The shared Drive handoff remained unchanged.

After the required newest-report scan, the following repair hypotheses were fixed before detailed theorem/source comparison:

1. **Affine quotient rank certificate.** Restrict transition dynamics to affine maps and hashes to linear maps. Replace universal same-hash circuit equivalence by an exact row-space test that either constructs the quotient transition or returns a concrete colliding-state witness.
2. **Proof-carrying nonlinear quotient.** For general circuits, require a separately checkable certificate that `h(T(s,a))` factors through `h(s),a`. This is only a conditional repair: a polynomially complete certificate system for arbitrary equivalence would imply a major collapse unless additional structure is imposed.
3. **Hash augmentation with an explicit budget.** Add state coordinates until acceptance and transitions factor through the hash, but charge `K=2^k`, count-bit width, source reads, and peak table memory. Reject the repair if `K` ceases to be polynomial or exceeds the ARC/FLMV workspace target.

## 2. Exact affine lumpability criterion

Work over `GF(2)`. Let the machine state be `x in GF(2)^s`, the next random block be `a in GF(2)^r`, and

\[
T_a(x)=Ax+Ba+c.
\]

Let the exposed digest be the linear map `h(x)=Hx`, where `H` is `k x s`.

**Lemma 55A (ESTABLISHED, restricted).** The following are equivalent:

1. for all `x,y,a`, `Hx=Hy` implies `H T_a(x)=H T_a(y)`;
2. `ker H` is contained in `ker(HA)`;
3. `row(HA)` is contained in `row(H)`;
4. there is a `k x k` matrix `Q` with `HA=QH`.

When these conditions hold, the exact quotient transition is

\[
\bar T_a(z)=Qz+(HB)a+Hc.
\]

The condition is decidable by Gaussian elimination using

\[
\operatorname{rank}\begin{pmatrix}H\\ HA\end{pmatrix}=\operatorname{rank}(H).
\]

If it fails, elimination returns `d in ker(H)` with `HAd != 0`; the pair `x=0,y=d` has the same current hash and different next hashes under the same coin block.

**Proof.** If `Hx=Hy`, then `d=x-y` lies in `ker H`, while the difference of next hashes is `HAd`; this proves equivalence of 1 and 2. The standard annihilator identity over a finite-dimensional vector space gives equivalence of 2 and 3. Row containment is exactly the existence of row coefficients `Q` satisfying `HA=QH`, proving 3 iff 4. Substitution yields the displayed quotient. ∎

This is stronger than a promise that a quotient exists: it is a complete polynomial-time construction-or-falsifier for the affine model.

## 3. Exact propagation and resource ledger

Assume every step consumes one fresh random bit, every affine transition passes Lemma 55A, the initial hash distribution is known, and acceptance is a union of hash fibers. For `K=2^k`, exact counts propagate over the `K` quotient states by following two outgoing transitions per state.

For `m` random bits the direct ledger is:

- time `O(m K poly(s,k))`, including quotient evaluation and count addition;
- peak count-table space `O(K m)` bits because counts have at most `m+1` bits;
- matrix/source storage `O(s^2+ks)` bits, or separately charged source rereads;
- output one acceptance count or decision bit.

For an `r`-bit block, the direct bound becomes `O(m K 2^r poly(s,k))` unless additional structure aggregates the coin images. If acceptance is not constant on hash fibers, it must be added to the summary; this can increase `k` and double `K` per independent bit.

**Corollary 55B (ESTABLISHED, restricted).** A uniform RP verifier already presented in this affine-lumpable form, with `k=O(log n)`, polynomial state dimension and polynomially many transitions, is deterministically decidable in polynomial time by exact quotient counting. This is a restricted derandomization theorem, not P=RP.

## 4. Why DIGEST-LUMP19 blocks the unrestricted extension

For a bounded-fan-in circuit `F(u)`, let the random tape be `(b,u,t)`, expose `h=b`, and set

\[
h'=b\lor(F(u)\land t).
\]

On the fiber `b=1`, the next hash is always one. On the fiber `b=0`, all next hashes agree iff `F(u)=0` for every `u`: if `F` is satisfiable, a satisfying `u` with `t=1` gives one while the same `u` with `t=0` gives zero. Hence universal same-hash consistency holds iff `F` is UNSAT.

**Lemma 55C (ESTABLISHED, restricted hardness).** Deciding universal same-hash transition consistency for succinct bounded-fan-in circuits is coNP-hard, even for a one-bit exposed hash and the displayed transition. It is in coNP because two same-hash states with distinct next hashes form a polynomial witness to failure. Thus the problem is coNP-complete.

The associated RP language in the handoff still has the deterministic bypass `b=1`; the hardness concerns certifying that this selected hash is a valid quotient, not deciding the language. Short hashes therefore help only after every hidden source, timer, solver, history, and trace influence is proved to factor through them.

## 5. Integration with EARLY-AFFINE19 and Circuit-SAT

`EARLY-AFFINE19` and Lemma 55A identify two different restricted positive islands:

- early affine branch tests on the original random tape can be counted in `3^q poly(n)` time through depth `q`;
- affine state transitions can be quotiented and propagated in `O(mK poly(n))` time when the rank condition and fiber acceptance hold.

They do not provide a normal form for arbitrary RP machines. Dummy identical-child tests can destroy early acceptance depth without changing the language, and one nonlinear AND/OR gate can move quotient validation back to Lemma 55C.

For Circuit-SAT/Tseitin representations:

- unique gate traces preserve projected primary counts but do not certify hash lumpability;
- affine/XOR trace coordinates can be eliminated or checked by the rank criterion;
- AND/OR trace relations are nonlinear, so gate inspection must either expose a direct deterministic bypass or pay for semantic quotient validation;
- independently sampling deterministic trace variables artificially dilutes RP density and remains retired;
- gate sharing changes representation size, not the quantifiers in Lemma 55A or 55C.

## 6. Computational consistency check

`experiments/review/2026-10-22_affine_lumpability_rank_gate55_audit.py` passed **83,501 assertions**:

- 400 constructed affine-lumpable transitions, exhaustively checked on all states and two-bit coin blocks;
- 400 rejected affine transitions, each with a concrete same-hash/divergent-successor witness;
- 240 multi-step cases and 931 transitions where quotient counts exactly matched complete state-distribution enumeration;
- every Boolean truth table through three inputs for the DIGEST-LUMP19 gadget: among 276 functions, exactly the three zero functions—one at each arity—passed universal consistency.

The finite controls validate implementations and small examples only. Lemmas 55A–C carry the general claims.

## 7. Proof-status ledger and next discriminating tests

| Role | Status | Quantifier / model / peak-resource boundary | Single next test |
|---|---|---|---|
| :00 SAT→ordinary MKTP | **OPEN.** **ESTABLISHED restricted:** affine hash quotient can be evaluated exactly. | A quotient evaluator is an upper-bound mechanism, not an ordinary-KT lower bound. Its matrices, source access, count table, output index and exponent must all be charged against the actual `p_k`. | Extract `H,A,B,c` from one proposed target generator. If the rank test passes, derive the complete indexed-evaluator KT exponent; if it fails, record the collision witness and abandon hash-only generation. |
| :12 P≠RP | **OPEN.** **RETIRED:** coNP-hard quotient validation or a short hash implies a language outside P. | Separation still requires one uniform language in RP outside every deterministic polynomial-time decider. The DIGEST-LUMP language has the direct `b=1` decider. | Apply verifier replacement and the `b=1` bypass before every fiber-hardness argument; keep only a language claim quantified over all deterministic deciders. |
| :24 ARC/FLMV | **OPEN.** | A hash can serve as a hereditary boundary state only when all successors and acceptance factor through it on every input. `K m` count memory, acquisition, child output, replay and ancestors must fit the same-machine peak bound. | On one nonlinear high-width source, propose `H`, then either give a source-checkable factorization certificate or produce the first collision; tabulate `K m` peak space against the FLMV target. |
| :36 P=RP | **OPEN.** **ESTABLISHED restricted:** EARLY-AFFINE19 and Corollary 55B. | No uniform source-preserving compiler maps every RP computation to logarithmic early-affine depth or an affine-lumpable `O(log n)` hash. Advice and oracle leakage are forbidden. | Attempt such a compiler on a verifier with one nonlinear gate and on its dummy-query padded equivalent; require the same primary-randomness semantics and polynomial `K`. |
| :48 synthesis | **ESTABLISHED:** affine construction-or-witness criterion and general coNP barrier. **OPEN:** both class questions. | Source circuit, primary coins, deterministic trace, hash, timer/history and count table are distinct channels. | Add the rank/collision gate before all new digest proposals; route nonlinear survivors to an explicit certificate-size and verification-cost ledger. |

## 8. P-vs-NP route impact

- **MKTP magnification:** unchanged primary DAG. Affine digest dynamics with polynomial `K` are now an efficiently testable LOW/easy regime, not the missing deterministic total both-label HIGH generator. General nonlinear lumpability is coNP-complete and supplies no ordinary-KT gap.
- **ARC/FLMV:** unchanged independent route. The rank lemma is a valid restricted boundary contractor for affine transitions, but the required all-input nonlinear hereditary contractor and matched FLMV point remain OPEN.
- **Compact-history:** remains a supporting diagnostic. A small state/hash works only when the transition truly factors through it; fast-forwardable affine dynamics again show why history size alone is not time hardness.

## 9. Sources and publication audit

- Latest substantive role source: [`RP-EARLY-AFFINE19`](https://github.com/j15marti/pnp/blob/9641ee7ef65ac4ddcc9ce56903091d1d2a62c2a0/research/agents/rp-derandomization/2026-10-22_0236_RP_EARLY_AFFINE19_HANDOFF.md).
- Replacement firewall: [`VERIFIER-REPLACEMENT-FIREWALL54`](https://github.com/j15marti/pnp/blob/2a4a6fa5191fb5d4c47678481613d3840843da09/research/main/2026-10-22_0248_MAIN_VERIFIER_REPLACEMENT_FIREWALL54.md).
- `DIGEST-LUMP19` was supplied directly in the automation handoff; its claimed local `/mnt/data` artifacts were not treated as cross-runtime evidence. Its stated 4,663-assertion finite audit was not re-used as proof; the present audit independently checks the defining gadget.

Root manuscripts and role assignments were not modified. No circuit, hash, oracle, proof system, selected solver, finite computation, or conditional recurrence is claimed to settle either open problem.

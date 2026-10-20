# MMW-QUERY-ABSORPTION19 — exact cofinal space composition

**Time:** 2026-10-20 16:48 Asia/Seoul  
**Scope:** exactly two active routes: (I) MCSP/MKTP hardness magnification and (II) arbitrary-SAT-decider ARC contraction into a matched FLMV endpoint. COMPACT-HISTORY20 is a supporting diagnostic, not a third route.  
**Global status:** **P versus NP remains OPEN.**

## 1. Verified inputs and current peer state

This run read the governance and continuity files, COMPACT-HISTORY20 addendum, current `main.tex` and `main2.tex`--`main5.tex`, the shared fallback Doc, and the newest original peer artifacts. Root `main.tex` is now a substantive reviewed document (blob `719dc96a...`), but it was not edited because this synthesis does not own or need a root merge.

Newest load-bearing peer items:

* REDTEAM36 constructed an ordered proper-3CNF INDEX family and a **conditional** one-way SAT-to-MKTP composition. Its finite controls report 16,388 SAT/proper checks, 8,188 prefix-distinguishability checks, and no failures.
* UNIVERSAL-UNDECIDABLE-CERT3 proved that correctness is not recursively enumerable even inside a uniformly polynomial-clocked SAT-decider family. It also warned that a query of length `p^(d_k)` is not diluted when `d_k=Theta(k)`.
* REDTEAM37 proved a **conditional firewall**: under P=NP, no fixed polynomial circuit-size bound supplies shared indexed witnesses for all but finitely many YES tableaux of every EXP language. This blocks inference from a short transition program or unique trace to a universal compact witness; it does not refute the project-specific diagonal premise.
* CACHE-MISS-FRONTIER18 remains the direct ARC ledger: complete child materialization fits the `(241/200,1/2)` target only if `g<21/200`; incomplete arbitrary caching needs the much tighter `rho+g<1/400`. The compiler remains unbuilt.

## 2. Ideas proposed before the literature check

1. **Ordered-output ledger.** A one-way reduction is useful only when each downstream query is an ordinary encoded bitstring; query count, length, construction, live buffer, and solver workspace must be charged separately.
2. **Cofinal short-query test.** If MMW query length were `p^(d_k)`, increasing `k` would absorb the unknown solver exponent only if `d_k=o(k)`.
3. **Clocked-portfolio barrier.** A proof-certified fastest-correct portfolio cannot cover every correct polynomial SAT decider, so it cannot be the load-bearing source of the unknown PH-solver exponent.
4. **Shared-witness test.** `exists W forall i` can amortize indexed history, while `forall i exists W_i` can hide a full side table and is not composable.

## 3. Primary-source audit

* McKay--Murray--Williams, STOC 2019, Theorem 4.2, states for time-constructible `p(M)>=log M` a one-pass MKTP streamer with time `O(M p(M))`, space `O(p(M))`, and ordinary `Sigma_3 SAT` queries of length `O(p(M))`. The crucial query-length exponent is therefore **one**, independent of `k`: <https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf>.
* Cheraghchi--Hirahara--Myrisiotis--Yoshida, STACS 2021, proves model-specific one-tape/branching-program lower bounds for MCSP/MKTP. It does not construct a SAT-to-MKTP transducer: <https://doi.org/10.4230/LIPIcs.STACS.2021.23>.
* Oliveira--Pich--Santhanam magnification concerns nonuniform gap problems and does not supply the deterministic ordinary reduction required here: <https://theoryofcomputing.org/articles/v017a011/>.
* Ilango's reduction is in a random-oracle model; the deterministic standard-model replacement remains open: <https://eccc.weizmann.ac.il/report/2023/165/>.
* Fortnow--Lipton--van Melkebeek--Viglas concerns deterministic random-access machines with simultaneous time/space in the same realization. It does not validate a one-way streaming-to-random-access model transfer: <https://lance.fortnow.com/papers/files/tst.pdf>.
* Hutter's fastest-program theorem enumerates **provably** correct programs and explicitly avoids unproved correct programs. It cannot enumerate all correct SAT deciders: <https://arxiv.org/abs/cs/0206022>.
* Easy-witness results are conditional circuit/derandomization tools; they do not prove the project-specific `exists W forall i` compactness premise: <https://www.math.ias.edu/~avi/PUBLICATIONS/MYPAPERS/IKW02/IKW02.pdf>.

## 4. Built theorem: MMW ordinary-query cofinal absorption

### Theorem (conditional, exact machine interface)

Let `F(x,j)` be the ordered proper-3CNF INDEX family from REDTEAM36, with stream length `n=Theta(m log m)` and deterministic one-pass exact space lower bound `Omega(m)=Omega(n/log n)`.

Assume constants `a>0` and `rho<1`, and an unbounded set `K` of fixed positive integers, such that for every `k in K` there is a deterministic total transducer `R_k` satisfying all of the following:

1. it reads the SAT source exactly once from left to right;
2. it emits, in target order and without a readable uncharged output buffer, an **ordinary** MKTP instance of length `M=n^(a+o(1))`;
3. its threshold is `p=M^(1/k+o(1))` and hence eventually `p>=log M`;
4. it has exact both-label semantics (SAT maps to one MKTP promise side and UNSAT to the other, with the orientation fixed in advance);
5. it uses `n^(rho+o(1))` live bits, including source acquisition, replay state, target generation, and all advice (there is no external advice or timer).

Then existence of this cofinal family implies `P != NP`.

### Proof

Assume instead `P=NP`. Then `PH=P`, so ordinary `Sigma_3 SAT` has one deterministic polynomial-time decider `Q`. Fix a constant `C>=1` such that on length-`q` inputs, both the running time and workspace of `Q` are at most `q^(C+o(1))`. The language and encoding of `Q` are fixed and independent of `k`.

Feed the ordered output bits of `R_k` directly to the one-pass MMW Theorem 4.2 MKTP streamer. MMW's queries have length `O(p)`, not `p^(d_k)` for an uncontrolled `d_k`. Materialize one ordinary query at a time, run `Q`, discard its workspace, and resume the stream. Query multiplicity increases total time but not peak workspace because queries are sequential and the buffer is reused. The composite peak space is

`n^(rho+o(1)) + p^(C+o(1)) = n^(max(rho,aC/k)+o(1))`.

Choose a fixed `k in K` with `k>aC`, possible because `K` is unbounded. Both `rho<1` and `aC/k<1`, so the composite space is `n^(theta+o(1))=o(n/log n)` for some fixed `theta<1`. The composition remains a deterministic one-pass decider for the ordered INDEX-3CNF family, contradicting its `Omega(n/log n)` one-pass space lower bound. Therefore the cofinal transducer family cannot coexist with `P=NP`. QED.

### Adversarial checks

* **Query-length falsifier defeated for the exact MMW theorem:** primary Theorem 4.2 says length `O(p)`, so `d_k=1`; the UNIVERSAL warning remains valid for other, longer-query constructions.
* **Unknown exponent not eliminated:** `C` is still unknown. Cofinality absorbs it existentially; no effective bound or fastest-solver portfolio is obtained.
* **Query count does not hide space:** sequential reuse preserves the peak-space expression. It may make time enormous, which is harmless only because the terminal contradiction is the one-pass INDEX **space** lower bound, not FLMV.
* **Output cannot be stored:** the proof requires direct online composition. A random-access target, a pointer to the source, hidden advice, or a readable uncharged output tape invalidates the theorem.
* **Target semantics remain the weakest arrow:** no `R_k` satisfying totality, ordinary encoding, both labels, in-order output, and common `rho<1` is known.

## 5. Proof DAG v19

| Arrow | Status | Exact qualification |
|---|---|---|
| Ordered proper-3CNF INDEX -> one-pass `Omega(n/log n)` space | **ESTABLISHED / project proof** | Restricted one-pass source order; not random-access SAT |
| MMW MKTP streamer -> `O(p)` ordinary `Sigma_3 SAT` queries | **ESTABLISHED** | Target already present/streamed; `p>=log M`; one pass |
| `P=NP` -> one fixed polynomial ordinary-query solver exponent `C` | **ESTABLISHED** | Existence only; exponent unknown but independent of `k` |
| Cofinal `k` absorbs `C` in peak space | **PROVED CONDITIONAL** | Requires the stated `R_k` family and common `rho<1` |
| SAT -> deterministic total one-way ordinary MKTP `R_k` | **OPEN — weakest MCSP arrow** | Standard model, both labels, target order, charged source access |
| Arbitrary SAT decider -> hereditary charged ARC successor | **OPEN — weakest ARC arrow** | Same random-access machine; all inputs; simultaneous time and space |
| ARC recurrence -> FLMV forbidden point | **CONDITIONAL** | Fixed point `(6/5,1/2)` after a valid compiler; materialization budgets apply |
| Compact shared witness for project diagonal family | **OPEN diagnostic** | Must be one `exists W forall i`; REDTEAM37 blocks blanket inference |
| Hutter/Levin portfolio bounds unknown `C` for all correct deciders | **RETIRED as load-bearing** | Proof certification omits correct but unproved programs; unnecessary for cofinal MMW space route |

## 6. Allocation

* **:00 MCSP:** construct or falsify a genuinely ordinary, total, both-label, one-way `R_k`; report target-bit generation order and common `rho` explicitly. Do not substitute an oracle pointer.
* **:12 Universal Solver:** stop treating fastest-correct certification as necessary for the cofinal MMW route. Instead verify that the exact MMW `Sigma_3 SAT` encoding is fixed across `k`, and audit whether any proposed replacement query exceeds `O(p)` actual bits.
* **:24 ARC:** keep the route separate. Attempt one all-input random-access successor with complete child materialization `g<21/200`, including acquisition and output; the INDEX theorem does not transfer to FLMV.
* **:36 Red team:** attack `R_k` at ordinary target semantics, source advice, output buffering, and common-`rho` cofinality. For compact history, restrict any claim to the named diagonal family after the EXP-witness firewall.
* **:48 Synthesis:** retain this theorem as a conditional composition lemma; do not promote it without an explicit `R_k`.

## 7. Reproducibility and publication

The accompanying exact-rational audit checks the cofinal inequalities for 4,000 `(a,rho,C)` rows, verifies the `d_k=1` versus `d_k=k` contrast, the eventual `p>=log M` condition on explicit scales, and sequential-buffer peak independence. Finite arithmetic checks do not verify the asymptotic theorem or construct `R_k`.

**Conclusion:** the newest source check removes the feared `d_k` growth from the actual MMW theorem and makes the unknown PH-solver exponent non-load-bearing for the conditional one-way INDEX route. The decisive construction is still absent. **P versus NP remains OPEN.**

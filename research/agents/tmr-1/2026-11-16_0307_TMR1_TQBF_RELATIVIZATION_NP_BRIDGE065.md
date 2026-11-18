# TMR-1/065: a fully charged exact-counting oracle countermodel to an NP-level relativizing bridge

**Time:** 2026-11-16 03:07 PST. **Owner:** TMR-1 / PNP Machine Model Lead. **Track:** C, cross-track theorem architecture. **Branch:** existing draft PR #197, `tmr1-20261115-independent-lean060`, not main. **Status:** KNOWN-THEOREM-BASED PROVED/EXACT RELATIVIZED COUNTERMODEL, independent mathematical review OPEN. No claim of an unconditional physical #SAT speedup, a new complexity-class separation, or a P-versus-NP resolution.

## Candidate, quantifiers and falsifiers fixed before source review

**Candidate C1h-NP-RELATIVIZATION-BRIDGE:** Test the proposed (but absent) inference that a uniform polynomial-time exact counting algorithm for the fully authentic C1a--C1e shared-DAG/CNF pipeline, *by relativizing arguments alone*, forces $\mathrm{P}\ne\mathrm{NP}$.

Use the standard deterministic oracle-machine model: the complete binary input, oracle question word, query-tape head, work tapes, arithmetic, and output are physical and charged; a query to one fixed oracle $A$ returns one membership bit in one oracle transition. The oracle's own internal computation is **not** physically charged in this model. No advice or input-dependent machine is admitted.

The quantified falsifier is

\[
\exists A\ \exists U^{A}\ \exists d\ge1\ \forall x\in\{0,1\}^{*}:
\quad
U^{A}(x)=
\begin{cases}
\#D_x,&x\text{ encodes a valid C1 shared Boolean DAG};\\
\mathrm{INVALID},&\text{otherwise},
\end{cases}
\]
where $U^A$ is one total deterministic uniform polynomial-time oracle transducer with polynomial simultaneous writable space, *but* $\mathrm P^A=\mathrm {NP}^A$.

Falsifiers: (F1) the count-threshold problem is not in PSPACE; (F2) encoding a threshold query to the oracle requires exponential length or cannot be produced in polynomial time; (F3) the shared-DAG-to-counting pipeline changes the exact count or loses malformed-source behavior; (F4) $\mathrm P^A=\mathrm {NP}^A$ fails for the chosen fixed PSPACE-complete oracle.

All four are discharged below. This is an explicit falsification of a **relativizing** NP-promotion arrow, not an argument that every nonrelativizing approach fails.

## Primary-source and project-state grounding

The current C1 chain is complete encoded shared-gate source $\to$ charged parser $\to$ parsimonious functional Tseitin $\to$ four-density normalizer $\to$ exact low-first `MainResults.encInput` $\to$ fixed-machine counter and physical simulation (conditional on Anthropic's pinned source claim) $\to$ exact output $\to$ Jahanjou--Miles--Viola binary hierarchy witness $\to$ *conditional* mild infinitely-often $E^{NP}$ general-circuit consequence. The pinned proposition is Anthropic `eth/MainResults.lean` at commit `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`; its finite-stack semantics and exact output width are unchanged. Upstream Lean+nanoda acceptance is recorded, but a fresh independent rebuild remains OPEN. Original Jahanjou--Miles--Viola *Local Reductions*, Theorem 1 and Corollary 3, concern the correctly scoped $E^{NP}$ witness, not an NP separation.

The oracle equality argument is the standard Baker--Gill--Solovay PSPACE-complete-oracle construction, using Savitch's theorem. TQBF is PSPACE-complete under *uniform polynomial-time many-one reductions*. See references [1]--[3]. The new role-specific point is the explicit end-to-end exact counting/query/space ledger for the genuine C1 source and why this is a load-bearing barrier for C1f-to-NP promotion.

## Fully charged construction and proof

Let $A=\mathrm{TQBF}$, the fixed language of true, well-formed, closed quantified Boolean formulas.

For any width-at-most-three CNF $\phi$ on $n$ explicitly declared variables **in the C1 unary-$n$ encoding (so $n\le N$)**, let $N$ denote its complete encoded bit length and let
\[
L_{\ge}=\{\langle\phi,h\rangle: 0\le h\le2^n,\ \#\phi\ge h\}.
\]
The syntax parser rejects malformed inputs. A deterministic polynomial-*space* machine decides $L_{\ge}$ by enumerating all $2^n$ assignments in depth-first or iterative order, evaluating every clause on each one, and accumulating a saturated $(n+1)$-bit count. It uses $O(N+n)$ writable bits for the explicit input model, but may use $2^n\operatorname{poly}(N+n)$ steps. Thus $L_{\ge}\in\mathrm{PSPACE}$.

By PSPACE-completeness of TQBF, there is one fixed uniform deterministic polynomial-time many-one reduction $R$ with
\[
\#\phi\ge h\quad\Longleftrightarrow\quad R(\phi,h)\in A.
\]
Fix $d\ge1$ large enough that $R$ generates its **entire** question word of at most $(N+n+1)^d$ bits in at most $O((N+n+1)^d)$ locally headed tape actions, retaining at most that many writable bits. This absorbs the reduction, output serialization, address arithmetic, and query construction; it does not pretend that answering $A$ is an ordinary machine step.

Now parse the *entire* authentic original C1a input word $x$, reject bad headers, lengths, gate references and malformed trailing data, and construct the C1b parsimonious clause list and C1c exact all-occurrence/four-density normalizer. Serialize the C1d exact low-first input. Let $n'$ be the final variable count, $B_C$ the original source length, $B_A$ the formal word length, and $P=1+B_C+B_A+q$. The compiler and normalizer preserve $\#\phi=\#D_x$; $n'\le P$. Binary search on the integer interval $[0,2^{n'}]$ uses **at most $n'+1$ adaptive membership queries** to $A$, each of the form $R(\phi,h)$. Keep one shared oracle-query tape and reuse it between tests; all failed candidate thresholds are included. Emit the exact count in the declared $q+1$ output bits (leading zeros allowed), with the original count-preserving Tseitin variables stripped by interpretation, not by uncharged computation.

The one fixed sequential **oracle** implementation therefore satisfies
\[
Q_A\le n'+1,\qquad
T_{\mathrm{oracle}}=O\!\left(P^4+(n'+1)P^d\right),\qquad
S_{\mathrm{peak}}^{\mathrm{oracle}}=O(P+P^d)
\]
on its **same** complete execution, including the original source scan, shared gates/wire indices, all clause construction, false binary-search guesses, $n'+1$-bit arithmetic, whole-query materialization, all query accesses, buffers and final output. The peak is the maximum live footprint of this one execution, not a sum of distinct optimizers. Every oracle call costs one unit **only in the explicitly declared oracle model**. If $A$ must instead be computed by an ordinary no-oracle physical machine, no polynomial-time bound follows; direct threshold enumeration can take exponential time. The construction is a legal oracle-world countermodel, never a hidden speedup for the unrelativized pinned solver.

Finally, because $A$ is PSPACE-complete and belongs to PSPACE,
\[
\mathrm{PSPACE}\subseteq\mathrm P^A\subseteq\mathrm{PSPACE},
\]
and
\[
\mathrm{NP}^A\subseteq\mathrm{NPSPACE}
=\mathrm{PSPACE}\subseteq\mathrm P^A.
\]
Thus $\mathrm P^A=\mathrm {NP}^A=\mathrm{PSPACE}$. In this one world **exact #3SAT on authentic explicit formulas is polynomial-time uniform with polynomial simultaneous oracle workspace, yet NP does not separate from P relative to $A$**. Consequently, no proof using only the relativizing existence of a fast exact count algorithm can promote C1f to $\mathrm P\ne\mathrm{NP}$. Any actual NP-target bridge must identify a genuinely *nonrelativizing* dependency. This does not challenge the currently conditional $E^{NP}$ mild superlinear general-circuit bound or the pinned formal theorem's scope.

## Four gates and hostile controls

| Gate | Status and reason |
|---|---|
| DISJ sanity | **PASS, restricted.** DISJ on $k$ input pairs has exact satisfying count $3^k$ and a compact 2-CNF/depth-two circuit. The oracle transducer does not infer hardness from static rank or semantic mass. |
| Relativization | **FAIL for the candidate merely relativizing NP-promotion arrow.** The explicit fixed PSPACE-complete oracle simultaneously makes exact #3SAT polynomial-time and $\mathrm P^A=\mathrm{NP}^A$. **OPEN** for any specified nonrelativizing alternative, with algebrization/Natural Proofs checks still required. |
| Simultaneous DTISP | **PASS for joint oracle upper accounting; NOT APPLICABLE to an FLMV lower-bound contradiction.** The oracle model is declared; there is no forbidden polynomial-time/sublinear-space physical machine inferred. |
| Deterministic configurations | **PASS as upper-bound safeguard.** For fixed total deterministic oracle machine, query tape and head are included in writable configurations; the bound $T\le2^{O(S+\log N)}$ is an upper consistency bound only, not a work lower bound and not automatically quantum/randomized. |

Horn, 2-SAT, affine/Gaussian, bounded treewidth, equality, autarky, independent product, padding, auxiliary, selector and unique-solution controls remain legal shortcuts. Field/basis transformations, shared recomputation and source-authenticated compact alternatives remain admissible. Majority ties and quantum amplitudes are **NOT APPLICABLE** to this deterministic exact oracle construction. /341 remains FAIL as full UNSAT authority, /386 RESTRICTED.

## Execution, verification and independent-review status

The proof is **symbolic**, a specified charged oracle-machine construction and standard complexity-theorem composition. No new empirical or asymptotic solver tests were performed. No independent Lean 4.33.1/Mathlib build, per-theorem `#print axioms`, nanoda replay, native physical microtrace or pnp preflight was executed in this run; the current environment has no local private-repository checkout and no Lean/Lake/Cargo, and direct checkout of the public upstream source was blocked by DNS. Earlier upstream acceptance logs are independent evidence only of their own executed upstream CI run. External mathematical peer review is OPEN. The source formula and full current TMR-1 manuscript were examined at the existing draft branch; no legacy trackers were consulted.

## ONE next load-bearing lemma

Independently reproduce Anthropic's **pinned** Lean v4.33.1/Mathlib `MainResults.mainTheorem` and `ethIsFalse` with the exact trusted challenge statements, full transitive `#print axioms`, Lean and nanoda kernel replay, and final FinTM2 input/stack/output semantics. The failure of the preceding independent workflow *before any job step* remains an infrastructure blocker, not proof rejection. For a future NP-target arrow, a distinct **nonrelativizing** premise must be specified and checked. P versus NP remains OPEN.

## References

[1] T. Baker, J. Gill, and R. Solovay, “Relativizations of the P =? NP Question,” *SIAM Journal on Computing*, 4(4), 431–442 (1975). https://doi.org/10.1137/0204037

[2] W. J. Savitch, “Relationships Between Nondeterministic and Deterministic Tape Complexities,” *Journal of Computer and System Sciences*, 4(2), 177–192 (1970). https://doi.org/10.1016/S0022-0000(70)80006-X

[3] Jin-Yi Cai, *Lectures in Computational Complexity* (2003), sections 3.4.1 and 12.1 (TQBF PSPACE-completeness and the PSPACE-complete equality oracle). https://pages.cs.wisc.edu/~jyc/810notes/book.pdf

[4] H. Jahanjou, E. Miles, and E. Viola, “Local Reductions,” ECCC TR13-099, revision 3 (2014), Theorem 1 and Corollaries 2–3. https://eccc.weizmann.ac.il/report/2013/099/

[5] Anthropic, *A 2^{o(n)} Time Algorithm for 3-SAT*, pinned Lean `MainResults.lean`/`Solution.lean` at `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. https://github.com/anthropics/formal-math/tree/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth

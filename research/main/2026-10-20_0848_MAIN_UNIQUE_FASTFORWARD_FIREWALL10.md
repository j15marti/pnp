# UNIQUE-FASTFORWARD-FIREWALL10

**Synthesis time:** 2026-10-20 08:48 Asia/Seoul  
**Scope:** only (1) MCSP/MKTP hardness magnification and (2) arbitrary-SAT-decider ARC contraction into a matched FLMV endpoint. Compact History is a diagnostic supporting workload, not a third route.  
**Global status:** **P versus NP OPEN.**

## 1. Exact recovery

The governance files were read at blobs `35b960ee22b18904d2089f42b51c3548cf04aba5` and `92cd8990c80552d1a630a4ce7b2de3daec4ed57f`; the Compact-History addendum was read at blob `c4db652b2dc007d3902fcaf8f659f9b5ec0708f4` (the governing commit remains `c4e1f72f10976405fa2479c88499894d3d58633f`). Root `main2.tex`--`main5.tex` were read at blobs `56464cb3d6bf9fc0b853287d1917d03bcf329ce3`, `d82342d236feb2dcaadd03c8ae4c47a02d639137`, `0281dcfc8833a031f2c5967a05ab7fdd8423640f`, and `05d9adae357b2970437130c3673fa2cc27e155e0`. The shared fallback Doc was read. No fallback write was needed.

Newest original peer material:

* **REDTEAM27** corrects randomized source-access notation. With source-independent coins `R`, the touched set must be the zero-input execution set `U(R)`, and the TV bound is an expectation over `R`; a favorable realized `u` cannot be substituted into an unconditional bound.
* **REDTEAM28** proves the exact expected-access version
  \[
  \operatorname{TV}\leq \mathbb E_R\!\left[1-\frac{\binom{N-u(R)}k}{\binom Nk}\right]+\eta
  \leq \frac{k\,\mathbb E_R u(R)}N+\eta,
  \]
  hence `E A_zero >= N(1/3-eta)/(wk)` for all-input error at most `1/3` in the named-coordinate model. Its 13,556 branch executions and 10,592 exact assertions reported no failures. This repairs the randomized form of PREPROCESSOR-WORD-ACCESS8 but remains a restricted source-access theorem.
* REDTEAM28 also records the relevant hostile compact clock: a long deterministic trajectory can have a small indexed circuit. The exact theorem below upgrades that observation to a uniquely satisfiable succinct CNF family and an explicit single shared witness.

Root `main.tex` still contains a literal truncation placeholder; a newer independent-review commit only changed annotations around that placeholder. It was not edited.

## 2. Ideas proposed before literature search

1. **Expected zero-path acquisition lemma.** Replace worst-case randomized access by the Jensen/concave-envelope bound on `E|U(R)|`; falsifier: source-dependent selection of `U` without charging the reads used to choose it.
2. **Unique non-fast-forward witness condition.** Close CANONICAL-WITNESS-TRAP9's alternate-witness escape by uniqueness, but demand an independent lower bound for the unique indexed witness; falsifier: a unique modular-clock tableau with fast-forward arithmetic.
3. **Globally fixed degree gate.** Any Compact-History statement must have one exponent `d` valid for all designated YES inputs/programs, not `forall n exists d_n`; falsifier: lookup circuits make the latter vacuous.
4. **ARC acquisition inheritance.** An iterable all-input successor must charge formula acquisition, child construction, replay, and output in the same random-access machine; falsifier: ordinary SAT self-reduction, which uses at most `v+1` calls but contracts neither an unknown time exponent nor the input-storage term.

## 3. Primary-source model check

* CHMY's STACS 2021 theorem is a **randomized two-sided-error one-tape machine with an additional one-way read-only input tape**, at one fixed larger MCSP threshold. It is not a cofinal threshold-descent theorem for arbitrary machines: <https://doi.org/10.4230/LIPIcs.STACS.2021.23>.
* McKay--Murray--Williams give search-MCSP streaming/AC0 constructions with small-fan-in `Sigma_3 SAT` oracle gates and consequences for one-pass deterministic `poly(s)` space/update. This is the short-query component, not a SAT-to-MKTP reduction: <https://hdl.handle.net/1721.1/137518> and <https://doi.org/10.1145/3313276.3316396>.
* Oliveira--Pich--Santhanam's nonuniform GapMCSP magnification is circuit-model specific; e.g. their stated hypothesis uses `Circuit[N^(1+epsilon)]`, not an unrestricted machine lower bound: <https://theoryofcomputing.net/articles/v017a011/>.
* Hutter's fastest solver competes with programs carrying proofs of correctness and runtime bounds, with multiplicative/additive overhead. It does not manufacture such a proof or uniformly bound the winning polynomial exponent: <https://www.hutter1.net/ai/pfastprg.htm>.
* Ilango's published theorem is random-oracle-relative; real-hash instantiation is described as heuristic, not a deterministic standard-model reduction: <https://doi.org/10.1137/24M1652568>.
* FLMV is retained only as a deterministic random-access simultaneous time/space endpoint: <https://doi.org/10.1145/1101821.1101822>.

No primary theorem supplies the missing deterministic total `R_k`, a bounded universal exponent, or an all-input ARC successor.

## 4. New exact counterexample: uniqueness still does not imply a hard shared history

### Theorem (unique fast-forward tableau firewall)

For every `m >= 1`, let `T=2^m`. There is a uniformly locally indexed CNF `F_m` with `Theta(mT)` variables and clauses such that:

1. `F_m` has exactly one satisfying assignment;
2. its state variables encode the complete trajectory
   \[
   x_0=0,\qquad x_{t+1}=x_t+1\pmod {2^m}
   \quad(0\leq t<T-1);
   \]
3. one Boolean circuit `W_m(kind,t,j)` outputs **every** state and ripple-carry variable of that unique assignment;
4. in the binary-fanin `AND/OR/NOT` library,
   \[
   |W_m|\leq \ell+(m+1)(\ell-1)+5m+2=O(m\log m),
   \qquad \ell=\lceil\log_2(m+1)\rceil.
   \]

Thus the quantifier is the strong form `exists W_m forall indexed variables`, not the irrelevant pointwise form `forall i exists W_i`. Since `m=log T`, a unique exponentially long computation history can have a shared witness of size `poly(log T)`.

### Construction and proof

Use state bits `x[t,j]` and carry bits `c[t,j]`. Unit clauses set `x[0,j]=0` and `c[t,0]=1`. Standard width-three Tseitin clauses enforce

* `x[t+1,j] <-> x[t,j] XOR c[t,j]`, and
* `c[t,j+1] <-> x[t,j] AND c[t,j]`.

There are
\[
mT+(m+1)(T-1)
\]
variables and
\[
m+(T-1)(7m+1)
\]
clauses. Starting from the units, the ripple constraints determine every carry and next-state bit, proving uniqueness.

The single indexed witness is
\[
W_m(x,t,j)=\operatorname{bit}_j(t),\qquad
W_m(c,t,0)=1,
\]
and for `j>0`,
\[
W_m(c,t,j)=\bigwedge_{r<j}\operatorname{bit}_r(t).
\]
Decode binary `j` once into equality wires, share prefix ANDs of the time bits, multiplex the requested state/carry bit, and select by `kind`. This gives the displayed gate bound. The clause-at-index generator uses only fixed-block arithmetic and is uniform `poly(m)`; the explicit CNF itself has length `Theta(m2^m)`.

### Adversarial scope

This theorem does **not** show that the project's actual diagonal family has a small witness. It proves the narrower logical non-implication:

\[
\text{unique satisfying assignment} + \text{exponentially long history}
\not\Rightarrow
\text{large shared indexed-witness circuit}.
\]

Therefore uniqueness closes the alternate-witness selector trap but not the fast-forward escape. The Compact-History premise still needs a source-specific lower bound against every shared circuit for the actual diagonal transition; generic uniqueness, determinism, and long duration are insufficient.

## 5. Reproducible audit

`experiments/review/2026-10-20_unique_fastforward_firewall_audit.py` independently builds the CNF, checks the explicit assignment, performs complete unit propagation, evaluates the indexed witness at every existing variable, and compares against serial execution.

Results for `m=1,...,10`:

* 38,849 indexed state/carry bits checked;
* 40,927 assertions;
* all variables forced by unit propagation in every case;
* exhaustive satisfying-assignment counts for `m=1,2` were exactly `1,1`;
* at `m=10`, `T=1024`, 21,493 variables, 72,643 clauses, and the explicit witness bound is 89 gates;
* zero failures.

These finite checks validate the implementation, while the symbolic recurrence and circuit construction prove the theorem for all `m`.

## 6. Versioned proof DAG

### ESTABLISHED / source-matched

* MMW short-query/search streaming construction in its published model.
* CHMY one-tape fixed-threshold theorem in its published model.
* OPS nonuniform GapMCSP magnification under its stated circuit hypothesis.
* FLMV deterministic random-access simultaneous time/space lower bound.
* Fixed-exponent absorption: if a uniform `R_k` exists for every fixed `k`, an unknown fixed short-query solver exponent can be absorbed by choosing sufficiently large fixed `k`.
* REDTEAM28 expected zero-path acquisition lower bound in the named-coordinate source-access model.
* **This run:** unique fast-forward tableau firewall.

### COMPUTATIONAL

The 40,927-assertion audit above. It is verification evidence, not an unrestricted lower bound.

### CONDITIONAL

`SAT -> charged deterministic total R_k -> ordinary MKTP/KT at p_k=M^(1/k+o(1)) -> MMW short-query streamer under P=NP -> simultaneous SAT DTISP target -> matched FLMV contradiction`.

The ARC recurrence and its `(6/5,1/2)`-scale limit remain conditional on a universal, all-input, hereditary, jointly charged successor.

The Compact-History conditional separation remains conditional on a **single** `tau(n)^o(1)` shared satisfying-assignment circuit for every specified self-padded YES instance and program.

### OPEN (load-bearing)

1. Deterministic standard-model replacement for Ilango's random oracle.
2. Uniform total `R_k` with vanishing parameter, `p_k >= log M`, no `M`-bit side table, and fully charged construction/output.
3. Source-checkable SAT-monochromatic semantic fibers and deterministic replay avoidance.
4. A globally bounded proof-certified universal-solver exponent; Hutter relocates rather than removes this requirement.
5. Arbitrary SAT decider to an iterable all-input ARC successor with same-machine acquisition, replay, output, time, and live-space charges.
6. Actual diagonal-family all-witness/unique-witness circuit lower bound. Uniqueness alone is now retired as a repair.

### RETIRED / FALSIFIED

* planted/canonical witness hardness as a proxy for minimum/all-witness hardness;
* uniqueness plus long history as a proxy for indexed-witness hardness;
* `forall i exists W_i` as a substitute for `exists W forall i`;
* input-dependent witness degree `d_n` as a uniform compactness statement;
* timing/hash wrappers used simultaneously as a free reduction and a constructive refuter;
* restricted proof size, static physical counts, finite rank/moments, or source-only access bounds promoted to unrestricted SAT-machine lower bounds.

## 7. Allocation for the next cycle

* **:00 MCSP:** attempt an explicit deterministic `R_k` target on a source family that survives the expected-zero-path acquisition bound; report all source reads and whether `p_k >= log M`.
* **:12 Universal Solver:** formalize one fixed proof system and determine whether one global exponent `C` is provable for all MMW short queries; reject per-input/per-length exponents.
* **:24 ARC:** give a line-by-line random-access ledger for one candidate all-input successor, including input acquisition, child construction, replay, output, and peak live bits; test heredity after one iteration.
* **:36 Red Team:** search for a fast-forward circuit for the actual diagonal transition or prove a sharply stated source-specific obstruction; do not test uniqueness alone again.
* **:48 Synthesis:** combine only model-matched arrows and rerun the weakest-arrow audit.

The strongest falsifier is now explicit: if the proposed compact-history repair uses only uniqueness, determinism, and trajectory length, the increment family above defeats it with an `O(log T log log T)` shared circuit. Main effort stays on the deterministic total `R_k` and all-input ARC successor. **P versus NP remains OPEN.**


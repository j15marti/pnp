# TMR-1/062: Correct JMV variable-name domain and complete encoded address-to-count interface

2026-11-15 22:06 PST | TMR-1 / PNP Machine Model Lead | Track C | branch `tmr1-20261115-independent-lean060` (draft PR #197, not merged).

## Status, model, and named dependency

**C1f-NAME-ADDRESS-COMPOSITION: PROVED/EXACT, RESTRICTED symbolic interface, external mathematical review OPEN; finite integration tests COMPUTATIONAL.** The pinned Anthropic counting premise remains CONDITIONAL for independent reproduction. P versus NP remains OPEN.

**Precise quantifier prefix.** For every `ell>=1,v>=1`, every total authenticated decoder `D:{0,1}^ell -> (Option([0,2^v) x Bool))^3`, every total Boolean circuit `A:{0,1}^v->{0,1}` of `s` shared fan-in-two gates, and every fully encoded shared fan-in-two implementation of `D` with `g_D` gates, a uniform bit-machine compiles a violation circuit `B` and a uniquely extending width-three CNF, and writes the exact pinned `encInput 3` bits. Clauses with `None` are an additional width-at-most-three interface control, not a claim that JMV Theorem 1 uses such slots. JMV's source `D_x:{0,1}^ell->{0,1}^{3v+3}` always emits three signed v-bit variable names, and the index universe contains up to **2^v named variables**.

**Four falsifiers tested or audited:** (F1) replacing a full 2^v-entry candidate assignment by an invalid v-entry array; (F2) losing multiplicity of unused clause-address bits while counting violations; (F3) mishandling missing/empty, repeated or complementary literal slots; (F4) hiding a factor 2^v or factor ell*s in the symbolic compiler's gate budget.

**Correction to TMR-5/054:** its statement `a in {0,1}^v` is not the full Jahanjou-Miles-Viola variable-name domain when v is the *number of bits per variable label*. The correct full assignment is a function `a:{0,1}^v->{0,1}`, i.e. a bit string of length `2^v`. This is a domain/quantifier correction in a peer report, not a falsification of its valid-index masking identity. At v=2, the variable with name binary `10` can determine clause satisfaction while any two-bit purported assignment omits its value. The present construction keeps the full assignment **implicitly as a circuit**, never materializes 2^v bits in the hierarchy verifier.

## Exact lemma and proof

Let `U=2^v`, and define the total implicit assignment `a_A(j)=A(bits_v(j))`. For each address `z in {0,1}^ell`, write `D(z)=(L_1,L_2,L_3)`, where a present signed literal `(j,b)` has value 1 iff `a_A(j)=b`, and a missing slot is false. Define

```
BAD_A(z) = AND_{r=1}^3 (L_r is None OR a_A(index(L_r)) != sign(L_r)).
```

Then **for every** `A` and `D` (not just correct W-circuits),

```
#BAD_A = |{z in {0,1}^ell : clause D(z) is false under a_A}|
#BAD_A = 0  iff  a_A satisfies the conjunction of all addressed clauses.
```

This holds even with duplicated addresses/clauses, dead address bits, a tautology, or an empty clause: multiplication of nonzero violation counts is irrelevant to the *zero* test, but the exact #count includes all 2^ell addresses. If only the first `m<2^ell` addresses are authentic, an explicit comparator `[z<m]` (O(ell) gates) is necessary, or the remaining addresses must decode to true dummy clauses. **JMV's actual constant-locality reduction has the complete 2^ell address domain**, so its case incurs no range mask. See the independently verified TMR-5/054 scope correction.

**Proof.** Fix z. The three displayed factors are true exactly when the corresponding literals are all false, with None interpreted as false. Therefore BAD_A(z) is the failure indicator of the addressed clause. Sum over the original ell-bit addresses. There is no use of nonuniform advice indexed by 2^v assignments; each `a_A(j)` is evaluated by one actual copy of circuit A on the decoded v-bit index j. Deduplicating the *compiled CNF's* gate clauses has no effect on their semantics and does not identify address inputs. For every z, the functional shared-DAG Tseitin equations have exactly one gate-value extension, regardless of fan-out, repeated operands and dead gates. Pinning B's output admits exactly the addresses with BAD_A(z)=1. C1c's forced-zero auxiliary variables have one further extension. The final CNF count is therefore exactly #BAD_A. The pinned `n'+1`-bit low-first output suffices since `#BAD_A<=2^ell<=2^{n'}`. QED.

**Gate construction.** Copy the `g_D` decoder gates once, then instantiate three copies of A whose v-bit input ports are WIRED directly to each of the three decoded variable-name vectors; fixed original x and canonical padding inputs of W are hardwired constants, not separately guessed. With one present-bit mask, three XOR mismatch gates, three NOT and OR combinations, and two ANDs, at most 11 additional fan-in-two gates suffice beyond `g_D+3s`. Thus the composed ordinary circuit has

```
q = ell,   G <= g_D+3s+11,   V=q+G
m_CNF <=4V;   n'=V+O(1), m'<=4n'.
```

For JMV's three mandatory literals, presence masks may be omitted. For `ell=n+O(log n), v=Theta(ell), g_D=O(n)` after J56's paid uniform junta discovery and `s<=eta d n sqrt(log n)`, the previous `2^{(36 C eta d+o(1))n}` conditional hierarchy rate remains unchanged. No statement here supplies an NP circuit lower bound.

## Same-realization source-to-output resource ledger

The *authentic input* is the binary x, the guessed complete canonical circuit A_N encoded with all predecessor IDs/truth tables, and the uniformly reconstructed JMV D_x gate list. Source authentication and wrong-branch failures are charged, including complete source words and output bits. For a source circuit with q=ell inputs, G gates and `w_C=floor(log2(max(2,V)))+1`, its binary length is `B_C=q+G+2+G(2w_C+4)+w_C`. The formal low-first input to Anthropic is `B_F=n'+5+3m'(floor(log2(2n'))+1)`; its output has n'+1 bits.

The same actual nondeterministic branch first constructs D_x with all bounded-junta probing calls charged, guesses and verifies A_N, writes B's full original binary DAG, emits its unique-extension CNF and formal bits, simulates the one fixed finite-stack machine on the ordinary physical Turing machine, reads the entire exact count and compares to zero. There is no oracle answer or free shared gate materialization. A conservative matching budget, writing `P=1+n+ell+v+s+g_D+B_C+B_F`, is

```
T_total <= P^{O(1)} + O_M(T_M+B_F+1)
S_peak <= P^{O(1)} + O_M(T_M+B_F+1)
```

for this **same branch and same machine**, with the polynomial stage including J56's `n^{O(w)}` explicit source evaluations for fixed w. No strict small-space DTISP pair or NP-level hierarchy contradiction follows. For a generic decoder a ROM of size 2^ell is legal but must be charged; it cannot be substituted for JMV's poly(n)-gate local decoder in the asymptotic implication.

## Executed exact finite integration audit

Actually executed in the V8 Code Mode runtime: deterministic xorshift32 seed **20261115**, revision `tmr1-c1f-address-verifier062.v2`, 84 total small instances, **710 original clause-address evaluations**, **705676 materialized formal-input bits**, **11913 assertions**, **zero unexpected failures**. Real test stages: synthetic decoder ROM construction from complete bounded truth tables (NOT an efficient asymptotic JMV construction); three actual copies of shared-gate assignment circuit A over **2^v variable names**; original binary shared-DAG serialization with unary headers, low-first predecessor indices and four-bit gate tables; full source parse; functional four-clause-per-gate CNF; repaired C1c totalizer; exact low-first pinned formula encoding and decoding; address-by-address equality of direct clause violation, composed circuit output and canonical CNF extension. Hostile controls include empty and tautological clauses, missing slots, repeated literals, unneeded address inputs and changed internal gate values. No Lean kernel, actual JMV full reduction, nor runtime simulation of the pinned counting machine was executed. No brute-force full auxiliary assignment cube is claimed.

**Published code:** `experiments/tmr/tmr1_encoded_address_e2e062.js` (Git blob `49dfb23e792eb8dcd3c0d57e7dd1ea1458bdcecc`).

**Immutable raw:** `results/raw/tmr/2026-11-15_2206_TMR1_ENCODED_ADDRESS062_V8_RAW.json` (Git blob `cf9e0f221191687b521f68a98056adfb14882e75`).

**Primary source:** Jahanjou, Miles, Viola, *Local Reductions*, ECCC TR13-099 rev.3 (2014), Theorem 1: `D:{0,1}^ell->{0,1}^{3v+3}`, v bits per variable name, not v variables. https://eccc.weizmann.ac.il/report/2013/099/revision/3/download/ . Anthropic `MainResults.lean` and `Solution.lean`, pin `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`; original CI logs available but local independent kernel rebuild remains OPEN.

## Four mandatory gates, controls, next dependency

| Gate | Status | Reason |
|---|---|---|
| DISJ sanity | **PASS restricted** | A linear-size DISJ circuit yields a legal small A; address-to-violation identity never infers hardness from cut rank. |
| Relativization | **PASS local; OPEN for NP promotion** | The elementary compiler may relativize; no NP separation claimed. Any new NP bridge must be explicitly nonrelativizing and pass algebrization/Natural Proofs guards. |
| Simultaneous DTISP | **PASS scoped upper; NOT APPLICABLE to FLMV** | The branch ledger charges both T and S; no forbidden strict pair follows. |
| Configuration counting | **PASS guard** | Fixed total deterministic read-only-input machines obey T<=2^{O(S+log N)} as an upper bound, not a work lower bound; no quantum/randomized inference. |

Horn, 2-SAT, affine/Gaussian, treewidth, equality, autarkies, product, padding, selectors, unique-assignment rank-one, field-sensitive bases, cached/shared/compact alternative paths and legitimate cheap algorithms all remain admissible. Historical /341 stays FAIL as full UNSAT authority and /386 RESTRICTED.

**ONE next load-bearing lemma:** a fresh independent pinned Lean v4.33.1/Mathlib build of `MainResults.mainTheorem` and `MainResults.ethIsFalse`, followed by actual transitive `#print axioms`, nanoda and fixed-FinTM2 bit-semantics replay. PR #197's workflow attempts 1-3 failed before any execution step; treat that only as infrastructure blockage. This run had no repository checkout, so project preflight and compiled LaTeX were NOT executed. External mathematical review OPEN. P versus NP OPEN.

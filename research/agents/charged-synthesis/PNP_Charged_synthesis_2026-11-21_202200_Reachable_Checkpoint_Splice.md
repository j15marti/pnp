# Reachable checkpoints are the missing premise in dynamic crossing arguments

21 November 2026, 20:22 PST, America/Los_Angeles. PNP Charged Proof Synthesis.
Recovery source revision: 5fef2167d60d2ca34bbfa32f3211f5224e1a2380. Later publication parent is recorded in Git history.

**Named lemma: DYNAMIC-REACHABLE-SPLICE1**, within DYNAMIC-COMPATIBILITY-OBLIGATION1.
**Result:** PROVED/EXACT conditional crossing criterion and explicit cache obstruction. The automatic inference from initial-input hybrid validity to post-preprocessing hybrid reachability is FALSIFIED/RETIRED. Existence of sufficient compulsory dynamic checkpoints for arbitrary solvers remains OPEN.
**Review:** Self-contained reconstruction and finite checks in this run. Independent adversarial review requested from Redteam and Accounting before any broader promotion. No external review or proof-assistant verification. No historical novelty claimed for crossing-sequence splicing.

## 1. The integrated conclusion

The strongest established decision advance remains CHARGED-UNSAT-TRANSPORT1: for each fixed correct deterministic single-tape solver, some canonical UNSAT inputs require quadratic time and cubic cumulative cost on the same execution. Its source report has internal review only. Its matching polynomial solver remains a required control.

Bounds' newest fresh-information ceiling closes a tempting amplification route: one nested global history can learn at most N bits about a complete N-bit input. This does not upper-bound runtime or local retransmission. Accounting's earlier output-fiber result and Bounds' Boolean cleanup qualification separately block compulsory source recovery from a completed scalar answer.

The strongest remaining candidate is therefore actual local transfer after preprocessing. This report advances its first unresolved implication by stating exactly when the classical crossing proof applies to a reached checkpoint. It also gives a byte-level counterexample to simply restarting that proof after a correct joint comparison. A valid SAT hybrid of original input blocks need not be a reachable hybrid of the processed machine states. One stale cached answer bit suffices to break that inference.

This is an integration of the new Boolean continuation, not a counting-to-decision transfer. None of the earlier strict-C witness or count circuits supplies an unrestricted decision lower bound.

## 2. Fixed model, source, quantifiers and falsifiers

Fix a total deterministic solver A, correct for Boolean decision on every valid input of the compatibility problem, before choosing hard inputs or checkpoints. Its single physical tape, head, finite alphabet and control include all input, workspace, addresses, caches and output. A primitive transition moves at most one cell. Output is a Boolean bit and terminator at a fixed left origin. No extra input head, free original-source oracle, external clock or hidden state is available.

Use exactly the transport report's encoding, with proper ordered signed Boolean 3-clauses:
\[
1^n0\;\gamma(m+1)\;[\text{clauses}]\;[\alpha]\;[\beta]\;[y\text{-ID}],
\quad
N=3n+2+2\lfloor\log_2(m+1)\rfloor+3m(w+1)+w.
\]
For its family, \(r\ge3,\ n=8r-1,\ m=10r,\ w=\lceil\log_2(8r)\rceil\), and \(N=\Theta(r\log r)\). The supplied local assignments and release identifier are charged. Physical blocks are not the logical Horn and dual-Horn parts.

The family is \(I_{f,g}\), with maps \(f,g:[r]\to[r]\), obtained by the source clauses
\[
\bigwedge_i(\neg X_i\lor Y_{f(i)})\ \land\
\bigvee_i X_i\ \land\
\bigwedge_i(\neg X_i\lor\neg Y_{g(i)}),
\]
the proper-width-three conversion, and the adjacent-witness compiler in the transport report, §§3–5. Its full generator is pinned below. The decision equivalence is UNSAT iff \(f=g\). This includes both labels; a diagonal-only correctness promise is insufficient.

The conditional lemma below quantifies over every fixed A and every finite, uniformly enumerated family of genuine reached checkpoints satisfying its premises. It does not assert those premises for every correct A. Any future universal theorem must have the order
\[
\forall A\text{ correct}\ \forall K>0,a\ge1\
\exists\text{ input regimes and justified actual views},
\]
with costs compared to the same proposed cap and execution. A solver-specific distribution is permitted. A single hard input working for every A is not asserted.

Four concrete falsifiers:
1. A mixed checkpoint is not reached from an opposite-label valid input, even though its raw formula track is valid.
2. A cache, head coordinate, control state or relevant timestamp is omitted when states are spliced.
3. The proof supplies a decoder with virtual residual-query answers or full retained source information without adjusting its demand.
4. The same crossing belongs to several checkpoint suffixes but is charged as if reuse were one.

## 3. A sufficient reachable-splice criterion

Fix a cut c strictly right of the output cells. Conditional on public stratum B=b, let U range over a finite index set. The stratum specifies A, the original length, the cut address, a computable family/checkpoint enumerator, and a common nonhalting control state and head position left of c. Different checkpoint arrival times are permitted; an external clock is not.

For each u, a valid same-label input \(x_u\) reaches the specified configuration \(C_u\). Write its entire tape as \(L_u\mid R_u\), splitting at c. Include every track, cache, marker and occupied location. A checkpoint-selection algorithm is part of the fixed enumerator; it terminates on these inputs.

**Reachability premise.** For every distinct u,v in the conditional index set, the configuration with common head/control and tape \(L_u\mid R_v\) occurs on the run of A on some valid opposite-label input \(x_{u,v}\). The map giving these inputs/checkpoints is explicit and uniformly computable when the criterion is used as an effective decoder. Input lengths and any reduction costs must be recorded separately for a cap transfer. The diagonal input lengths here remain the original N.

Let \(E_c(x_u)\) be the real transitions strictly after its checkpoint that cross c before halt. Let \(CS_c(u)\) list the control state immediately after each such crossing.

**Conditional conclusion.** The map \(u\mapsto CS_c(u)\) is injective within each stratum.

**Proof.** Suppose distinct u,v have equal complete suffix crossing sequences. Starting at the mixed configuration, splice the left-side excursions of the continuation from \(C_u\) and right-side excursions of the continuation from \(C_v\). The common initial head/control start the first left excursion. Matching crossing states start each subsequent excursion, and the fixed transition function gives the required local updates. Equal crossing lengths give the same last head side and a finite halting continuation. The final fixed-left answer is inherited from the diagonal left computation and has the common diagonal label. By reachability, this continuation is a suffix of a valid opposite-label input's run, contradicting A's correctness. Thus the sequences differ. No online query service or witness production is presumed.

This is a sufficient criterion for this proof architecture, not a necessary characterization of every possible dynamic lower-bound method. Correctness alone does not establish the reachability premise.

### Decoder, records, overhead, event reuse

For each justified obligation j take \(U_j\) to be its diagonal index; \(B_j\) is precisely its public stratum and any extra supplied side information. If additional past information is included, condition on it and recheck the hypotheses on each remaining fiber.

Encode each crossing state and a distinguished END symbol using
\[
b_A=\lceil\log_2(Q_A+1)\rceil
\]
bits per symbol. The record \(\Pi_j\) is conditionally prefix-free, with
\[
|\Pi_j|=b_A|E_j|+h_j,\qquad h_j=b_A
\]
for a fixed public cut and checkpoint scheme. Adaptive nonpublic cut identities, endpoints, addresses, timing or family descriptions needed by the decoder must instead be carried in a self-delimiting header and added to h_j. Direction follows from the common starting side and alternating crossings; it is not a free additional signal.

An actual mathematical decoder enumerates the finite diagonal inputs in the stated stratum, simulates each from its authentic input through its computably selected checkpoint to halt, constructs its suffix crossing sequence, and returns the unique matching index. Every such simulation halts by the hypotheses. The decoder uses no external answers to residual SAT questions. Its computational cost includes all generation, simulation, address bookkeeping and comparisons and may be enormous. This is an information-theoretic decoder, not an efficient simulation of A or a claimed same-time algorithm. If used operationally, those costs must be charged; they are not counted as transitions that A itself performed.

The splicing proof, rather than an asserted requirement that A explicitly reconstruct u, proves
\[
H(U_j\mid B_j,\Pi_j)=0.
\]
Prefix coding and double counting then give
\[
\sum_j H(U_j\mid B_j)
\le b_A\sum_j\mathbb E|E_j|+\sum_j\mathbb E h_j
\le b_A\rho\,\mathbb E T_A+\sum_j\mathbb E h_j.
\]
Here \(\rho=\sup_{x,t}|\{j:t\in E_j(x)\}|\) is a proved bound on actual memberships in one execution. Distinct fixed spatial boundaries at one checkpoint have \(\rho=1\). Reusing the same boundary at q checkpoints with overlapping future suffixes can have \(\rho=q\). Neither syntactic erasure stages nor a list of semantic subproblems makes their physical events disjoint.

This supplies the requested inequality only under the explicit reachability, decoder and event premises. A fixed-cap contradiction requires the numerator to exceed \(b_A\rho K N^a\), with constants and input regime matched. An asymptotically decisive comparison must dominate the particular fixed K, not just have a similar power.

## 4. The paid-cache obstruction on the actual Boolean family

Use one fixed all-input-correct solver A_cache. It parses the full input, authenticates the canonical map family by exact regeneration, extracts both maps from their literal positions, compares them jointly, and caches \(d=[f\ne g]\). A failed admission returns UNKNOWN internally and invokes a correct total SAT fallback on the retained original formula. UNKNOWN is not UNSAT. Malformed inputs can be rejected by the input convention; the correctness domain is valid encodings.

The authentication verifies every header, clause, sign, identifier, witness bit, release ID and input endpoint. Arbitrary maps are allowed, so permutation recognition is unnecessary. The baseline report gives an O(N)-time, O(N)-space multitape implementation and its faithful O(N²)-time, O(N)-span single-tape simulation. Keep the original input on a protected track throughout, then erase temporary tracks, restore the head to the origin, and enter READY with the answer in one cache track at the origin. A constant finite alphabet can carry these tracks, with original input symbols unexpanded and auxiliary tracks initially blank. This is the transport report's model, with a per-machine finite alphabet. A globally fixed exact alphabet would require a separately priced encoding.

On every admitted member:
\[
T_{\rm prefix}=O(N^2),\quad S=O(N),\quad
CM_{\rm phys,prefix}=O(N^3),\quad CM_{\min,\rm prefix}=O(N^3).
\]
Copies, real access, comparison, simulated-head movement, retention, cleanup and return to origin are included. Prefix code discovery is a fixed uniform parser/generator, not advice. Failed candidates and general fallback remain charged; no polynomial guarantee is claimed outside the admitted family.

At READY, the configuration is exactly the original N source symbols plus the one cached bit, with all temporary state cleared. Three local transitions write the decision at cell 0, write its terminator at cell 1, return to cell 0 and halt. This uses head positions only 0 and 1, hence crosses none of the middle cuts. It need not erase the remaining source. Suffix time is three, peak span O(N), physical suffix CM O(N), and descriptive suffix CM O(N) by an input-based description. Total bounds remain the displayed quadratic/cubic ones. No minimum-description value is computed experimentally.

Take distinct permutations \(\pi,\sigma\). Both diagonal checkpoints have cache 0. Mixing their tapes at any common middle cut gives raw input \(I_{\pi,\sigma}\) and cache 0. But the genuine checkpoint on \(I_{\pi,\sigma}\) has cache 1 because that formula is SAT. The two configurations differ at exactly the origin cache field. The mixed configuration's continuation emits UNSAT, so it cannot be reached by this correct solver on any valid SAT input. Initial-input hybrid validity has survived; the required checkpoint reachability has failed.

This proves the all-parameter obstruction, not just its finite instances. It does not falsify the transport theorem or Bounds' theorem, whose stated premises remain intact. It falsifies only the proposed automatic restart after paid preprocessing.

On uniform diagonal permutations, choose U to be the permutation, B to be r, cut, common head/control and the common zero cache, and Pi to be the terminated suffix crossing record. Then \(H(U\mid B)=\log_2(r!)\), Pi is constant, and
\[
H(U\mid B,\Pi)=\log_2(r!)>0.
\]
There is no source decoder from that record. If the full retained input is supplied in B instead, the initial conditional entropy becomes zero. Both choices block the incorrect demand for different reasons. The entire configuration already determines the decision, as required by the full-state entropy obstruction.

## 5. Reproduction and exact scope of finite evidence

New code: [dynamic_synthesis_reachable_splice_20261121.py](../../../experiments/dynamic_synthesis_reachable_splice_20261121.py).
Raw: [dynamic_synthesis_reachable_splice_20261121.json](../../../results/raw/dynamic_synthesis_reachable_splice_20261121.json).

Run from repository root:
    python experiments/dynamic_synthesis_reachable_splice_20261121.py

The generator dependency is experiments/charged_unsat_transport_20261121/charged_unsat_transport_audit.py, SHA-256 98b46a013cabc3f969bcf58c08da2b1fd6937a26e1b46e75a06318e03d34d4f4, fetched at the recovery revision. It is imported without executing its previous exhaustive audit. The new independent parser extracts maps from encoded clauses, regenerates the entire input, forms full checkpoint tapes, and simulates the three explicit output transitions.

| r | N | Permutation pairs | Off-diagonal mixed states with stale cache |
|---|---:|---:|---:|
| 3 | 624 | 36 | 30 |
| 4 | 830 | 576 | 552 |

All 612 actual checkpoint suffixes return the correct label in three simulated transitions with zero selected-middle crossings. All 582 off-diagonal splices differ from their genuine checkpoint in one cell and emit the wrong stale answer. Thirty diagonal splices agree. One nonpermutation SAT map control is admitted. Four altered/malformed admission controls return UNKNOWN, including a syntactically valid forged witness trailer. Hashes identify artifacts only; semantic state comparisons use complete tuples.

At the smallest tested example, \(\pi=(1,2,3)\), \(\sigma=(1,3,2)\), cut 339 and N=624. Actual output is 1#, mixed output 0#. With the report's cell-span convention before constant conversion to bits, suffix CM is \(3(N+1)=1875\). These are exact suffix transition counts, not measured end-to-end single-tape times.

Script SHA-256: de31c2509c1a5a7e039ae01e1bc48452a7eaf24384d5d943a95c1ba5e0203dcc.
Raw SHA-256: ab66be424f406d41eb1c7083eb987193b13c068bd98e236416856090c2e801ee.

This reuses the existing small source families for a new question: reachability of spliced processed states. It does not rerun the completed source-satisfiability enumeration, claim new empirical hardness, or simulate arbitrary solvers. An initial local download had an extra trailing newline; the dependency digest check caught it, and exact original bytes were restored before the successful run. No mathematical test failed.

## 6. Reconciled dependency graph and current peer status

The dependency chain is:
authentic Boolean family -> decision-sensitive valid initial hybrids -> same-run physical crossings -> quadratic/cubic calibration.
For a new dynamic phase the chain must additionally contain:
actual checkpoint after paid preprocessing -> reachable opposite-label mixed checkpoints (or a different proved local-service argument) -> actual decoder -> bounded event reuse -> cap comparison.
The first new arrow is OPEN. This report gives a sufficient criterion and an explicit failure of automatic closure. Bounds' global-information ceiling blocks substituting globally fresh source entropy for this arrow.

All following source reports and available code/raw were recovered at 5fef2167d60d2ca34bbfa32f3211f5224e1a2380. Earlier source commits give their publication provenance; their claims retain their own review status.

| Role / revision | Exact premise and consequence | Integration |
|---|---|---|
| Construction, 2303eb12b08af4eaaf5e0a94e4097eb1599c835f, T5-DISJ-ORBIT-WIDTH1 | Symmetric strict-C DISJ orbit; authenticated quotient admits width-nine elimination; polynomial exact count and separate positivity decision. Explicit T5 N, conservative sole-tape O(N^20) successful path. | Closes the direct-evaluation alternative in Synthesis's 14:19 report. Original mask extraction still separate. Not a Boolean dynamic obligation. |
| Accounting, 4e2beb641518f2ba66e8604a85ff6e18dbbf67aa, T5-OUTPUT-FIBER-LOSS1 | After exact aggregation and cleanup, future cannot reconstruct a source label varying within one output fiber. General record bound subtracts residual entropy. | Source recovery after computation is not compulsory. Its conservative generic cleanup exponent is improved only under Bounds' separately stated Boolean/alphabet hypotheses. |
| Discovery, 2f50f80fbd579bdc04ca0fbf24626ee63a20897e, T5-SEPARATOR-FIBER-PRODUCT1 | Fixed one-separator strict-C template, private inventories, paid scanned admissions: linear full named witness diagram, zero normalized positive defect. All examples SAT. | Restricted representation upper bound, no decision lower bound. Shared growing-separator work remains separate. |
| Bounds, 5fef2167d60d2ca34bbfa32f3211f5224e1a2380, DYNAMIC-FRESH-INFORMATION-CEILING1 | Complete N-bit source, nested global history, targets measurable from source/history: total fresh information at most N. Boolean cleanup preserves time exponent with stated finite-alphabet convention. | Strongest new dynamic obstruction; does not preclude repeated physically justified local transfer. |
| Redteam, 960c4be768d6e9667b9d27db2ef36b3602dc54a3, T5-CANONICAL-ADMISSION1 | Canonical literal encoding and exact admission; one legal symmetric slot swap defeats the unguarded count evaluator. O(N) admission circuit. | Authentication required. No transfer to ordered R or arbitrary Boolean checkpoints. |
| Boolean baseline, 2547822e9e82c914a668d9b4de2c6991e490d7f0 | Proper Boolean compatibility family with supplied witnesses; one tape, explicit ordering, actual initial hybrids. | Internal-review-only \(\Omega_A(N^2)\) time and \(\Omega_A(N^3)\) CM; matching polynomial upper bound. |
| This report | Same fixed A, full reached configurations and reachable opposite-label mixed configurations. | Conditional suffix injection and prefix-free decoder; automatic restart falsified by A_cache. Universal local-view existence OPEN. |

Construction's old source bytes use \(N_C=n+2+2\lfloor\log_2(m+1)\rfloor+3mw\), without the Boolean sign/witness/release fields. Discovery's source has its own n,m. These are not interchangeable with the Boolean N in §2. Their finite evidence is retained as evidence of legal shortcuts, not added to Boolean lower demands.

No newest dynamic Construction/Accounting/Discovery/Redteam claim was available in their recovered handoffs at the source snapshot; the table explicitly preserves their latest earlier scopes. The new Bounds report was the sole post-directive specialist report recovered. All six roles being enabled does not mean six new mathematical results exist.

## 7. Same-execution cap ledger and gates

Fix \(T_A(x)\le K N^a\) on the claimed class, with A,K,a fixed and a>=1.

| Resource | General cap ceiling | Boolean calibration demand | What it excludes |
|---|---|---|---|
| Time | O(N^a) | Omega_A(N²) | a<2 |
| Peak span S | O(N^a) | Input-scale Omega(N) | No additional a>=1 exclusion |
| Physical CM | O(N^(2a)) | Omega_A(N³) | Alone a<3/2 |
| Self-contained descriptive CM | O(N^(a+1)) | Omega_A(N³) | a<2 |
| Count-map circuit size | O(N^a log N), for a capped count solver | No new count-map demand in this Boolean run | None |

The circuit ceiling is recorded for compatibility only; a Boolean decision solver is not thereby a counter. The new suffix criterion provides no independent CM lower bound. A cubic cumulative demand cannot be obtained by multiplying a time expectation by a peak on another input. The baseline simultaneous theorem, rather than such multiplication, supplies its cubic demand.

All costs of A_cache belong to one execution: raw input parsing, source authentication, map extraction, copying, relocation/representation conversion, comparison, buffers and real indices, clearing temporary work, shared cache storage, final writes and movement. It makes no oracle calls or virtual residual queries. Costs of a failed admission and fallback are not hidden. The matching family bound is an upper bound for one total solver on the recognized family, not a global polynomial SAT algorithm.

DISJ/equality gate: PASS, both labels and the legal cache control retained.
Simultaneous DTISP: PASS for the scoped criterion and cache ledger; no unrelated runs combined.
Deterministic-configuration gate: PASS, complete states and reachability used, no state-count-to-runtime inference.
Relativization: OPEN for any unrestricted separation; nonlocal oracle transitions invalidate this specific physical crossing argument.
Natural Proofs/algebrization: no bypass claimed or needed for this conditional classical method.

Relocation can destroy the old physical interface; new cuts need their own proof. Affine/Tseitin algebra, complement shortcuts, private-leaf/product evaluation and forced-domain simplification remain permitted. Large witness sets and syntactic width do not establish the missing checkpoint premise. A diagonal-supported hard distribution is legitimate only with all valid opposite-label hybrids in the solver's correctness domain. Terminal cleanup does not erase earlier paid work. Caching repeated residual answers is legal, and offline access is not replaced by online/streaming deadlines.

## 8. Fresh literature and official-repository search log

Task-specific queries:
- Repository: "checkpoint splice reachable", "dynamic rectangular", "cached decision"; branch query "charged".
- Literature: "Hartmanis one tape Turing machine crossing sequences initial configurations splicing quadratic 1968 pdf"; "Patrascu Demaine information transfer lower bounds preprocessing online partial sums addresses cells 2006".
- GitHub connector, independently under anthropics, openai, xai-org, google, google-research, google-deepmind: '"information transfer" "preprocessing"'.
- Web fallback: 'site:github.com/anthropics OR site:github.com/openai "SAT" "preprocessing"'; 'site:github.com/xai-org OR site:github.com/google OR site:github.com/google-research OR site:github.com/google-deepmind "information transfer" "lower bound"'.

Repository search surfaced older adaptive-switch rectangular transcripts, canonical online replay/caching, and checkpoint-provider reports. Those excerpts reinforce that reachability and online restrictions are old concerns; no novelty claim or uninspected theorem import follows. Branch search returned no matching charged branch, not an exhaustive proof that no drafts exist.

Hartmanis [1], 1968 original, pp.326–327, was read for its single-head crossing definition and segment-splicing lemma. The checkpoint criterion here is derived explicitly rather than claiming the source proves dynamic reachability. Pătraşcu–Demaine [2], 2006 journal version, §§5.3–5.4 and §6 introduction, was read for real cell addresses/contents and mandatory operation semantics. Its dynamic query service and cell-probe model do not transfer to one offline SAT answer without a new theorem. Both are primary literature; no general SAT lower bound is imported.

All six scoped connector searches returned no matches after one Google 429 was retried successfully. Web fallback produced an Anthropic formal-math issue and OpenAI math overview, alongside unrelated nonofficial hits. The Anthropic root and eth README were fetched at commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5 (root blob 1df53bfc14a022088d1b5757698f692bf79390b4; eth README blob 0b3dcf4a858ff802b3275fc5999ffb134c74de60). The README advertises a subexponential SAT/counting formalization and explicitly distinguishes its machine statement from the printed paper. No proof files, transitive axioms, physical simulation or kernel build were verified in this run. Therefore no advertised theorem is imported. Its relevance is that algebraic preprocessing must remain legal, not that it supplies this missing compulsory-checkpoint lemma. OpenAI's overview was seen at search-excerpt level only; no commit-specific technical result was used. Nonofficial repositories were excluded from official-owner findings.

Ownership was checked using Anthropic and OpenAI GitHub verified domains; xAI's corporate Grok release linking xai-org/grok; Google's organization-policy page naming google; Google Research's resources page and its actual link to google-research/google-research; and DeepMind's publication page linking google-deepmind/trecvit. These authenticate owner scopes, not mathematical claims. No applicable official-repository theorem or implementation was found for this exact dynamic reachability dependency. Search coverage is bounded.

## 9. Recovery, ownership and receiving dependency

Read the full current continuation directive, Boolean transport report, AGENTS.md, CODEX.md, repository research skill, compatible end-to-end authority and applicable T5 §§5–6,13.4,14–15. Recovered all six handoffs, own latest full Synthesis report, the five peer reports and their relevant original code/raw. The transport raw file records 620 earlier source cases; it was inspected, not rerun. The new Bounds proof has no solver experiment to rerun. No complete checkout exists, so repository preflight and LaTeX build were not run. No TMR manuscript is owned by this role.

**ONE next lemma: DYNAMIC-LOCAL-VIEW-EXISTENCE1. Lead owner: Construction with Accounting.** On a compact decision-sensitive Boolean family beyond the polynomial map-equality control, prove that every fixed correct solver under its proposed cap encounters an intermediate view that supports reachable opposite-label hybrids (or supply an alternative actual-service decoder), after arbitrary paid preprocessing and sharing. First show this for one nontrivial phase. Do not assert a superpolynomial number of phases before that premise is established.

Receiving tasks, all on this one dependency:
- Construction: explicit input family, full Boolean N, and valid mixed-checkpoint source construction.
- Accounting: public/local views, retained caches, exact decoder, framing/address charge and actual overlap rho.
- Discovery: strongest authenticated joint evaluator, algebraic shortcut or reusable decision cache on that family.
- Bounds: compare only proved same-run demand to fixed K,a; keep the global fresh-information ceiling separate from local transfer.
- Redteam: independently attack §3's reachability/output-side proof and §4's cache control, including an all-UNSAT promise and relocation.
- Synthesis: keep this edge OPEN until those checks close; do not multiply baseline and suffix demands without an actual event partition.

The role handoff is updated only in charged-synthesis; no peer file or historical manuscript ownership is changed. Issue #324 carries the review request and verified publication links. P versus NP remains OPEN.

## References

1. J. Hartmanis, Computational Complexity of One-Tape Turing Machine Computations, JACM 15(2), 325–339, April 1968. https://cse.iitkgp.ac.in/~goutam/toc/readingMaterial/computational-complexity-one-tape-Hart.pdf
2. M. Pătraşcu and E. Demaine, Logarithmic Lower Bounds in the Cell-Probe Model, SIAM J. Comput.35(4), 932–963, 2006. https://erikdemaine.org/papers/DynamicConnectivity_SICOMP/paper.pdf
3. Boolean transport baseline and original code/raw links: https://github.com/j15marti/pnp/blob/2547822e9e82c914a668d9b4de2c6991e490d7f0/research/main/Charged_UNSAT_Transport_2026-11-21.md
4. Bounds' current primary dependency: https://github.com/j15marti/pnp/blob/5fef2167d60d2ca34bbfa32f3211f5224e1a2380/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-21_200818_Dynamic_Fresh_Information_Ceiling.md
5. Source reports are the exact filenames recorded in each role's handoff at recovery revision 5fef2167d60d2ca34bbfa32f3211f5224e1a2380; original publication revisions are in §6. These are internal project evidence, not external certification.
6. Official-owner provenance: https://github.com/anthropics ; https://github.com/openai ; https://x.ai/news/grok-os ; https://opensource.google/documentation/reference/github/where ; https://research.google/resources/ ; https://deepmind.google/research/publications/122591/

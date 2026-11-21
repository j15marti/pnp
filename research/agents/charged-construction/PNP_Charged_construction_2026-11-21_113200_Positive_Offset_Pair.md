# Construction: a same-length decision/positive-count pair
2026-11-21 11:32 PST, America/Los_Angeles.

**T5-POSITIVE-OFFSET1 — PROVED/EXACT**, explicit strict-C circuit construction and count identities; external independent review pending. For every acyclic OR/NOT circuit H with p>=1 inputs, there are two uniformly generated strict-C instances B^-_H,B^+_H, of the SAME encoded length N and maximum occurrence five, with one known common multiplier M:
```
Z(B^-_H) = 2 M #CircuitSAT(H)
Z(B^+_H) = M (2^p + #CircuitSAT(H)).
```
Consequently SAT(H) iff SAT(B^-_H) iff Z(B^+_H)>M2^p. Every B^+_H is SAT. The positive version is a reduction to a count threshold, NOT a satisfiability-preserving reduction by itself.

**FALSIFIED/RETIRED proposed use:** merely shifting the zero count to a known positive baseline does not evade the output-atom obstruction. On any fixed-parameter source distribution with UNSAT mass p0, equality to M2^p gives the same advantage lower bound max(0,p0-2^-k) against a fake of average conditional min-entropy at least k. The positive family is retained as an exact interface and control, not promoted to a hard pseudoentropy pair.

**COMPUTATIONAL:** 98 source circuits, 294 generic unsplit T5 counts, complete generated split-size/occurrence and encoding checks. Symbolic proof below is separate from finite evidence. No lower bound, exponent exclusion, or decision separation follows.

ONE next dependency: **T5-SAT-SLICE-PAIR1**, Bounds owner, Redteam adversarial review and Synthesis tracking. Specify a fake/source pair that survives the full multiplier AND shifted-baseline atom test, with independently proved cap-facing indistinguishability or an explicit small falsifier. Sampling only SAT source circuits is a new premise, not supplied by this compiler.

## Quantifiers, fixed model, and four falsifiers
For EVERY finite topologically ordered OR/NOT circuit H, with p>=1 declared input bits (unused inputs allowed), o OR gates, t NOT gates, b=p+o+t base wires, and one designated output wire, the generators below give the stated identities. OR may read the same wire twice, fanout and shared gates are unrestricted, and output may be any base wire. Each gate has a fresh output name. No source assignment is part of the encoded target input.

Separately fix ONE total correct deterministic strict-C counter A, and constants K>0,a>=1 independent of the input, under T_A(N)<=K N^a. The machine is the handoff's fixed-alphabet, sole physical tape/head model, with input/work/output/control/head/addresses charged and no free input oracle or clock. A correct decider is a separate fixed machine. Our compiler execution and A's target execution have separate ledgers; a polynomial reduction does not preserve their concrete exponents for free.

Four falsifiers:
1. A Boolean-domain or gate gadget gives unequal fibers, admits a forbidden wire value, or loses strict distinct-name syntax under sharing/repeated OR inputs.
2. The selector contributes a source-dependent baseline, or the negative twin fails either direction of SAT equivalence.
3. The common n,m,N,E or occurrence ledger fails, including unused source inputs and output wires that are not the last gate.
4. Positive counts are treated as indistinguishable solely because zero disappears, or threshold decision is confused with SAT of the positive target.

C is exactly the symmetric relation containing all permutations of 012,123,234,340,401 over Z5 (30 ordered tuples). All clauses have three distinct variable names; anchors are variables, not constants. Ordered R has 40 tuples and means that the first value beats exactly one other value and loses to the other, with i beating i+1,i+3 mod5. It is different. C(x,y,z) iff R(x,y,z) AND R(y,x,z) permits an explicit conversion preserving assignments/count, doubling m and the maximum occurrence bound to ten. It is not performed in the reported N values. No historical S/Q substitution.

## Recovery and source revisions
Read the complete current baseline, including appended programs, the assignment directive, AGENTS.md, CODEX.md and repository research instructions. Baseline blob a886f3387a8676b9cc86afbf3bebf22630109d49, SHA256 c9a3a0f362c72dfad7548b0cd44723853f105dcdc6a4f9ea5fef4559d3bb2a33, 141084 UTF-8 bytes. This is recovery under its stated hypotheses, not independent certification of the entire baseline.

Recovered own [10:35 report](https://github.com/j15marti/pnp/blob/c5d8802644abe2caef15ef67153fa76ab8da1152/research/agents/charged-construction/PNP_Charged_construction_2026-11-21_103500_Unweighted_Three_Color.md), full generator blob ee2522b3a06906681275f58e0419fbee47b93091 and raw blob194d2bf5127715b9cf8c4b45f9ec0e8b9793b7b0 (76 graph cases). Its exact exclusion interface is used below. Read the complete earlier equality generator blob8d2586962e55c58408ea25089fc90cd6e22299d9 at [8ae69ba65b79af7d3da945293eacb7bbf1ebe2d1](https://github.com/j15marti/pnp/blob/8ae69ba65b79af7d3da945293eacb7bbf1ebe2d1/experiments/t5_construction_occurrence5_20261121.py).

Read [Bounds' zero-atom report](https://github.com/j15marti/pnp/blob/15d61b216e5741297b178ddaba6904be14c55806/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-21_105900_Zero_Atom_Minentropy.md) in full. This run addresses its named SAT-slice dependency. Issue324 recovered through Redteam comment7067852073. Accounting9f6787be1c19431c5848f0cc44f8e3ccd4b4a75c excludes auxiliary orientation entropy as compulsory work; Synthesis4c1d7f5ef16531313c82bd7a888fca03edd3f4f3 charges full multiplier conversion. Discovery1274ba70556d11dcea569a65b728ba256f5f6f07 and Redteam bb11ab09a212de9c2512e5e8f80d4002882571b7 concern scope-restricted representation expansion, not this count-map construction. Their compiler-context counts cannot supply the missing hardness premise.

Current head at publication preparation was0c29b10e0b9766b5c0e39a62d3b79da07ce79216, a continuation-log commit after Redteam. Preserve that and all other role files. The unfinished local Synthesis mixture draft from the preceding interrupted assignment is not a published premise or an independent review.

## Full generator and exact local fibers
Use one shared frame
A = AND_{i=0}^4 C(a_i,a_(i+1),a_(i+2)),
indices mod5. Every pair of anchor names shares a clause, so all five colors differ; allowed triples are complements of edges of a five-cycle. Thus the ten assignments are exactly a_i=s+i or s-i mod5.

The prior exact exclusion gadget, with a fresh helper h, is
U_k(X;h)=C(a_k,X,h) AND C(a_(k+2),a_(k+3),h).
In every frame it has precisely one helper extension iff X!=a_k, and zero otherwise. For k=0 in the identity frame, h is in{1,4}; X=1,2,3,4 respectively force h=4,1,4,1. Rotations/reflections give all cases.

NEW Boolean domain interface:
D(X)=U_2(X;h_2) AND U_3(X;h_3) AND U_4(X;h_4).
It has exactly one extension for X in{a_0,a_1}, zero otherwise. It uses three fresh helpers and six ordinary C-clauses. Unlike the baseline's three-clause Boolean domain, this variant has no factor2 per base wire. We pay the extra clauses rather than silently dropping the old multiplicity.

For every base wire impose D, interpreting a_0=0,a_1=1. For each NOT gate X=NOT P impose C(a_2,P,X). For each OR gate X=P OR Q use fresh Y,Z and the five clauses
```
C(a_1,a_2,Y), C(a_0,a_1,Z),
C(a_4,P,Y), C(a_3,Q,Z), C(X,Y,Z).
```
The first four clauses uniquely give (Y,Z)=(a_3 or a_0,a_4 or a_2), with choices controlled by P,Q respectively. For Boolean P,Q,X the last clause is satisfied iff X=P OR Q. These are the baseline section9 gate clauses, now combined with unit-fiber Boolean domains. Pin the chosen output O by C(a_0,a_2,O).

Each accepting Boolean input uniquely fixes all base wires and gate/domain helpers for each frame. Every target assignment conversely gives such an accepting input. Hence the unsplit compiler J(H) satisfies
Z(J(H))=10 #CircuitSAT(H),
n_J=5+4b+2o, m_J=6+6b+5o+t.
There is one GLOBAL tenfold factor, even with disconnected/dead gates or unused inputs. All declared T5 variables occur because every base wire has its domain clauses. Repeated OR inputs occur in different clauses, never twice in a single strict clause. Gate outputs/helpers are fresh.

## The same-length pair and both decision directions
Add a fresh Boolean source input s and one new OR gate W=s OR O to the circuit. Keep all original gates as a shared DAG. Let H^+ pin W and let H^- pin the OLD output O in that same augmented circuit. Both have p+1 inputs, o+1 OR gates, t NOT gates, and b+2 base wires. Their compiled unsplit clause lists differ only in the final output-pin identifier.

For every assignment x to H:
- In H^+, s=1 always accepts, giving exactly2^p assignments in total; s=0 accepts exactly the z=#CircuitSAT(H) accepting x. Thus #H^+=2^p+z.
- In H^-, acceptance is H(x)=1, and s is arbitrary. W is still uniquely evaluated, so #H^-=2z.

Both arguments are bijections, not just existential implications. If H has an accepting assignment, its negative twin has a satisfying extension (either s); if the negative twin has a satisfying assignment, projection gives an accepting H input. Therefore SAT(H) iff SAT(J(H^-)). Also z>0 iff #H^+>2^p, and z=0 iff equality. Every H^+ has a witness obtained by choosing s=1 and evaluating H on any input. Supplying that easy witness does NOT supply its exact count.

For the pair before splitting:
```
n_pair = 15+4b+2o
m_pair = 23+6b+5o+t
Z(J(H^-))=20z
Z(J(H^+))=10(2^p+z).
```
The two target SAT labels can differ at identical headers/length. The positive family alone has constant decision answer SAT; we explicitly reject it as a new hard SAT family. The negative twin preserves the separate decision path.

## Bounded occurrence, multiplier, and exact n,m,N ledger
Apply the existing full-domain equality-path splitter D to each unsplit target. Give every occurrence its own copy; for successive copies U,V of one source name add four fresh names b_1,...,b_4, put b_0=U, and emit the five frame clauses plus C(b_4,V,b_1). Its exact interface is2[U=V]: the frame fixes V=U and has two orientations for any common value. Links have disjoint private names, so each source solution has2^E lifts.

With all source variables used, E=3m_pair-n_pair. Every internal occurrence copy appears once in its source clause, three times as the outgoing frame endpoint and once as the incoming second endpoint, at most five. Private frame variables have degree at most four. The splitter changes
n_B=n_pair+5E, m_B=m_pair+6E.
For BOTH paired instances:
```
E = 54+14b+13o+3t
n_B = 285+74b+67o+15t
m_B = 347+90b+83o+19t
M = 10*2^E
Z(B^-_H)=2Mz
Z(B^+_H)=M(2^p+z)
3m_B-n_B=14E.
```
The orientation bits may be contracted; they are not compulsory solver information. The target split clause lists need not differ at only one clause because output occurrence membership changes equality paths.

For every stage use exactly
N(n,m)=n+2+2floor(log2(m+1))+3m ceil(log2(n+1)),
encoding1^n0 gamma(m+1) then one-based fixed-width identifiers. Let N_pair=N(n_pair,m_pair), N_B=N(n_B,m_B). Both twins have exactly equal N_pair and N_B. Each is Theta((b+1)log(b+2)). Do not substitute b for N.

One explicit source encoding is1^p0 gamma(g+1), then g records with one gate-type bit and TWO identifier fields of width w=ceil(log2(b+1)), then one output field; NOT repeats its input field canonically. Its exact length is
L=p+2+2floor(log2(g+1))+g(1+2w)+w.
Validation requires topological input IDs and the canonical second NOT field. N_B=O(L log(L+2)); it need not be O(L) when many inputs are unused. The extra unary source selector/input and target output are charged.

Executed false source H=NOT(x OR NOT x), p1,b4,o1,t2:
paired unsplit n33,m54,N1017, counts0 and20.
Paired split n678,m828,E129,N25538, counts0 and20*2^129.
The positive count equals the known threshold10*2^(129+1); it is SAT even though H is UNSAT. This is a legal counterexample to confusing the positive target's SAT label with the source label, not a counterexample to the proved threshold equivalence.

## The shifted atom control: positivity is insufficient
Fix p,o,t (hence b,N_B,E,M). Let a distribution choose any legal source circuits with these parameters; suppose Pr[z=0]=p0. Map them to the positive target encodings X. The true output Y equals the CONSTANT baseline c=M2^p with probability exactly p0.

For any fake Ztilde in0..5^{n_B}, with the same X marginal, put
g=E_x max_y Pr[Ztilde=y|X=x] and Hbar_inf=-log2(g).
If Hbar_inf>=k, then Pr[Ztilde=c]<=g<=2^-k.
The circuit [z=c], on ell=3N_B padded output bits, has at most2ell-1 gates: negate the positions where c has a zero and AND all bit tests. It ignores X. Thus for B>=6N_B,
Adv_B((X,Y),(X,Ztilde)) >= max(0,p0-2^-k).
The zero-atom calculation has moved to another efficiently testable atom. No count computation or source SAT recognition occurs in this test. A fixed p0=1/2 still prevents growing average-min entropy with vanishing advantage. This is not a Shannon-entropy bound and does not rule out the one-bit target.

For varying source parameters the constant test no longer automatically applies; any header/layout recognition and variable threshold computation must be charged. No free p extractor or supplied source annotation is asserted for arbitrary target strings. Fixed parameter slices already suffice for this control.

Exact counting remains connected: for a promised B^+ image and authenticated p,E, subtract2^p after division by M to recover z. Conversely z determines the target count. This is a paid arithmetic reduction, not a claim of pseudoentropy preservation with zero circuit loss. A proposed fake must respect the full M, range and baseline constraints. No cap-sized indistinguishability premise has been constructed.

## Downstream obligation and controls
The feature absent from the easy matching-cycle family is an arbitrary source OR/NOT circuit with shared gates and a genuine both-label negative image. Global algebra, evaluation of affine cores, exact gadget contraction and scalar caching remain legal. A subsequent compulsory-progress claim must apply to actual source-dependent work that remains after these operations. For the positive member it must distinguish counts above the baseline; it cannot demand finding one witness, because one is easy to construct. For the negative member it must establish SAT/UNSAT work, not infer it from a count lower bound.

Full-state H(Y|C_t)=0 remains an obstruction to ordinary remaining-work entropy. Auxiliary equality orientations are independent choices, not trace-decodable mandatory data. Relocation may move all hard computation away from original cuts. Private-leaf trees, matching cycles, bounded-width DP, affine/Tseitin, forced-domain and constant-function circuits remain easy controls, with their own contraction/evaluation costs. Our fixed circuit H can encode those subclasses, so no uniform hardness assertion applies to every member. Input renaming and color-frame reflection preserve counts. Boolean complement replaces z by2^p-z; for the positive lift the count becomes M(2^(p+1)-z), not a preservation of a proposed fake distribution. Sharing keeps one source gate per DAG node. Decision-witness packing is not inferred from frame multiplicity or large counts. SAT, UNSAT and UNKNOWN stay distinct; malformed encodings are rejected/UNKNOWN, never classified UNSAT solely by a parser failure. Hashes identify bytes, not semantic merge proofs.

## Complete charged resource ledger
Let U=L+N_pair+N_B+2. A fixed uniform scanner validates the source, assigns fresh IDs, emits domains/gates/pin and occurrence copies/equality links. A conservative repeated-scan implementation uses O(U^2) field visits, O(log U)-bit counters, and paid travel over O(U) cells. O(U^4) sole-tape time and O(U) simultaneous span suffice, including output layout; hence physical CM<=O(U^5). These are conservative construction upper bounds, not measured CPython runtimes and not A's compulsory work.

| Charge | Treatment on its actual execution |
|---|---|
| Parsing and source authentication | Read every source bit, check headers/topological IDs/output, validate all emitted C scopes. Recognizing a target as an image requires paid structural validation; generated-image promises do not authenticate arbitrary inputs. |
| Discovery and failed candidates | Research verifies fixed gadgets. Deployed compiler uses fixed tables. An arbitrary solver's failed recognition, parameter selection and fallback searches remain charged. |
| Representation changes and adaptation | Allocate real IDs, source-to-copy maps if retained, helpers and equality links; contraction/Boolean conversion and mode switching require actual work. |
| Queries, real accesses and addresses | No residual-count oracle is supplied. Repeated scans, head travel, counters, offset comparisons, address bits and indirect access cost are included. |
| Storage and sharing | Original input, output, maps and buffers coexist inside O(U) compiler span. Count physical cached objects once, including locations. Native DAG sharing is preserved. |
| Recomputation | Discarded maps/intermediate values must be reread/rebuilt. No free retained source or advice. |
| Arithmetic and output | M and c have O(U) bits; constant multiplication, shifts, exact division checks and subtraction use paid bit operations. Count output has at most3N_B bits plus terminator; the compiler emits the full N_B input. |
| Sampling | A source sampler followed by the paid compiler gives a target sampler with its actual costs. Conditioning on SAT, a fake sampler, and its indistinguishability proof are not provided. |
| Minimum-description CM | Compiler replay gives O(U^4(L+log U)) self-contained descriptive CM, distinct from physical O(U^5). Replay does not implement fast low-space evaluation. |
| Composition with A | Compiler plus target execution plus normalization/output costs; polynomiality transfers, no fixed exponent silently transfers. The atom-test circuit is yet another execution, not a time/space claim about A. |

For the SAME fixed A,K,a,N_B retain:
S_A=O(N_B^a), physical CM_A=O(N_B^(2a)), minimum-description CM_A=O(N_B^(a+1)), count-map circuit gates O_A(N_B^a log N_B).
Circuit wire serialization costs extra address bits; gate count is not descriptive entropy. No independent demands are added or multiplied. None of the construction's identities exceeds a cap ceiling; no exponent is excluded, much less every polynomial exponent. Counting separation alone would not prove P!=NP.

DISJ: NOT APPLICABLE, no communication/direct-sum theorem. Relativization: no nonrelativizing step; unrestricted separation OPEN. Simultaneous DTISP: PASS for separate same-execution ledgers, compulsory violation OPEN. Deterministic configurations: PASS for scope; no state-count runtime inference. Natural Proofs/algebrization: no barrier bypass or unrestricted circuit-lower-bound claim.

## Reproducible code and raw evidence
Run with Python3, assertions enabled:
```
python experiments/t5_construction_positive_offset1_20261121.py > results/raw/t5_construction_positive_offset1_20261121.json
```
Code SHA256:6cd122e55ab7150dff6c8a1a22099ec5b44b195395c9f83670965773417accdb.

The standalone runner enumerates all topological gate lists for p1,2 and g0,1,2 with output the last wire (94 cases), plus false, true, unused-input and shared-gate controls (four cases). It computes source truth tables, then uses a generic five-domain GAC/backtracking/memoization counter on THREE actual unsplit target clause lists per source: base compiler, positive lift, negative twin. It initially permits every color and does not fix anchors, invoke source truth tables, or contract gates in that counter. All294 counts match the formulas. Full clause lists/encodings for selected controls and split clause lists are in raw evidence.

Split counts use the earlier exact equality theorem, not full enumeration of their exponentially many orientations. The new generator checks split dimensions, occurrence<=5,3m-n=14E, exact encoding roundtrips and paired lengths. No Turing-machine benchmark or formal proof-kernel build. Same assistant session, not an external independent audit.

Reason for new experiment: this is a new unit-fiber Boolean compiler plus selector/count-threshold pair, not a rerun of graph-color or equality experiments. An initial196-count development check was extended to294 when the same-length negative twin was added; the final code/raw supersede that developmental output. Prior equality/graph suites were not rerun.

## Fresh task-specific literature and official-repository search log
Queries: “counting satisfying assignments always satisfiable formula disjunction fresh variable reduction”; “Cook1971 complexity theorem proving procedures original paper circuit satisfiability”. The former returned model-counting/BDD/DNF discussions but no directly imported positive-offset theorem. Cook's [original scan](https://www.cs.toronto.edu/~sacook/homepage/1971.pdf) was fetched; text extraction returned no readable lines, and screenshot retrieval was attempted. No new claim is imported from unreadable scan text. Our Boolean-to-T5 and selector identities are proved explicitly above; no historical novelty claim.

Read [Vadhan–Zheng, full version revised March8,2013](https://salil.seas.harvard.edu/sites/g/files/omnuum4266/files/salil/files/eccc2013.pdf), Definitions2.6,2.8,2.9 and2.10–2.11, and the polynomial-alphabet qualification. The nonuniform conditional definition requires an actual indistinguishable joint pair, not merely positive outputs. Its uniform variant involves sampling-oracle qualifications; the polynomial-output-alphabet sampling characterization cannot be imported for a full exponentially large count range. The shifted-atom proof here uses elementary guessing probabilities, not a Shannon-entropy theorem.

Fresh connected GitHub query “model counting satisfiable circuit selector” under all six official organizations anthropics,openai,xai-org,google,google-research,google-deepmind returned no results. This is a search-coverage statement, not absence of applicable repositories. Web fallbacks:
- site:github.com/anthropics “SAT” “counting”
- site:github.com/openai “model counting”
- site:github.com/xai-org “SAT” circuit
- site:github.com/google “model counting” SAT
- site:github.com/google-research counting satisfiability circuit
- site:github.com/google-deepmind satisfiability model counting

Promising Anthropic result inspected at commit16a5ce41304fcdaea4e0be7c132e1c361dc26da5: [eth/README.md](https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth/README.md), blob0b3dcf4a858ff802b3275fc5999ffb134c74de60, and [MainResults.lean](https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth/MainResults.lean), blob1c62a550fa1e4cbec65bb7112f92ad67589afddc. Read exact definitions: deterministic finite-alphabet FinTM2 stack machine, k-CNF clause lists without duplicate clauses, all variables occur, k>=1,n>=4,m>=2 for MainTheorem, explicit unary/fixed-field input and n+1-bit count output. The file states propositions only, not proofs; its comments explicitly exclude the simulation/rewriting proof from Lean. Repository claims subexponential counting. No proof/kernel build or end-to-end verification performed here, so no theorem is promoted/imported. Even its stated rate would not be a polynomial algorithm or a T5 lower bound. Legitimate tensor/algebraic aggregation must remain allowed by any future compulsory-progress lemma.

OpenAI/math main commit4eaee87548250b2682affda7d05d947c05554bae was recovered; this run's query/fallback returned no exact positive-offset result. Prior logs already screen its unrelated formal/preprint claims; no repeated deep review or proof import. xAI returned no applicable result. Google fallback surfaced [OR-Tools all-solutions documentation](https://github.com/google/or-tools/blob/stable/ortools/sat/docs/solver.md): snippet distinguishes finding some solutions from exhausting all solutions; useful testing context, not a proof of the count reduction. Google Research circuit_training is physical placement, not this count map. DeepMind code-verification snippets concern cryptographic model sanity/nonvacuity, not T5 counts. Those snippet screens were not full-file/build audits; no commit pin or formal verification claimed for them. Other hits were third-party repositories and were not counted as official.

Official ownership uses corporate-domain/official cross-link checks recovered in this continuous session: [Anthropic](https://github.com/anthropics), [OpenAI](https://github.com/openai), [xAI](https://x.ai/open-source), [Google Research](https://research.google/pubs/implicit-rate-constrained-optimization-of-non-decomposable-objectives/), [DeepMind](https://deepmind.google/blog/open-sourcing-mujoco/), [OR-Tools](https://developers.google.com/optimization). Product names alone were not accepted as ownership. No external code imported.

Bounded repository duplicate query “positive offset selector satisfiable” returned historical wrapper/Boolean snippets, not this exact T5 paired interface. First100 branch entries were screened; only agent/localshield1-t5-mixing-20261119 matched the relevant name filter, at16860248c019ad8b15fb7f7fd8fc5a73364e1ce2. This is a bounded screen, not a complete branch/novelty audit. No local checkout, so repository preflight/LaTeX compilation was not run. No TMR manuscript ownership or edits, retired trackers or schedules changed.

## Return to peers and publication scope
Bounds/Synthesis: the all-SAT positive image admits arbitrary circuit counts by an explicit shifted-multiplier identity, but source UNSAT mass remains an efficiently testable baseline atom on fixed-parameter slices. Do not treat removal of zero as an indistinguishability proof. Use the negative twin for the SAT/UNSAT reduction, with the same N and M; it has twice the source count.

Redteam: independently attack unit Boolean fibers, repeated OR inputs/shared outputs, same-length twin counting, the splitter's changed output paths, and the fixed-parameter qualification of the atom test. Review is requested, not completed. Existing graph-core service and typed-completion dependencies remain open; no peer file is overwritten.

Publish this separately named report, its code/raw, and Construction's own compact handoff with current-head protection and exact readback. ONE next dependency is Bounds T5-SAT-SLICE-PAIR1 as stated at the start. **P versus NP remains OPEN.**

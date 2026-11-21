# Discovery: scope-restricted contexts for nested renaming

2026-11-21 10:51 PST, America/Los_Angeles.

**T5-CONTEXT-ORBIT1 — PROVED/EXACT for the declared typed architecture; external independent review pending.** A renaming compiler may forget the accumulated permutation outside the record's authenticated declared scope. If Q distinct restricted contexts are reachable across the created handles, expansion has O(Q) native nodes and cumulative closed shortcut defect O(MQ). In particular, if every view has scope at most a fixed k, Q<=M(1+v^k), even when the global permutation group is factorial in v and the nesting depth is unbounded. This strengthens T5-SMALL-GROUP-RENAME1 without asserting any universal scalar-to-DLDD compiler.

COMPUTATIONAL evidence: 181352 assignment comparisons for the new compiler, plus 504 comparisons for a new fixed-footprint family, all passed. These finite checks supplement the proof, not establish its asymptotics. The generator/evaluator is imported from pinned Redteam code and is not independent new review.

ONE next dependency: **T5-LARGE-SCOPE-CONTEXT1**, owner Discovery, adversarial review Redteam, tracked by Synthesis: for views on growing scopes, prove a noncircular polynomial reachable-context bound from paid structural certificates, or construct a legal polynomial-description typed family whose minimum ordinary-DLDD expansion is superpolynomial. A large compiler context count alone would not prove the latter.

## Exact quantifiers, encoding and fixed solver

For every fixed deterministic correct counter A restricted to the architecture below, every explicitly encoded strict-C NAND bipartite graph input X, and its single actual execution, let W be paid bit-machine work, v the Boolean graph-variable universe, and M the number of created typed record identities including initialization and final target closure. Assume M<=c_A(W+v+1), with c_A independent of X. All dependencies point to older IDs. Deletion and later recreation receive fresh IDs. The theorem below applies to every finite such history and permits adaptive maps, parameters and sharing.

Fix K>0 and a>=1 independently of X when making the comparison T_A(N)<=K N^a on the handoff's fixed-alphabet deterministic sole-tape model with input, head/control, addresses and output charged. No runtime of the compiler below is substituted for A's runtime.

C is the symmetric 30-tuple relation comprising all permutations of 012,123,234,340,401 over Z_5. R is the distinct ordered 40-tuple relation: the first value beats exactly one of the other two, with i beating i+1 and i+3 modulo five. C(x,y,z) iff R(x,y,z) AND R(y,x,z), but this report operates on C and does not silently change its input. Historical S/Q theorems are not substituted.

The exact source encoding is unary n followed by gamma(m+1) and m triples of one-based w-bit variable IDs, w=ceil(log2(n+1)):
N=n+2+2 floor(log2(m+1))+3mw.
For this NAND image n=v+5,m=v+e+5,Z=10 #IS(H), where H is the bipartite input graph. Declared unused variables remain counted. These inputs are all SAT; the result concerns counting architecture, not a decision separation. Construction's new unweighted three-color image is a separate input family and is not silently substituted.

Four concrete falsifiers:
1. Two accumulated maps agreeing on a record's full declared scope yield different expanded functions or scopes.
2. A later nested view requires a forgotten outside-scope map entry despite exact scope typing.
3. A record of scope larger than k receives a nonidentity context although every traversed view has scope at most k.
4. Expansion/event bookkeeping omits free variables, shared identities, rebuilt records or typed final closure, invalidating Q or the at-most-M producing-event bound.

## Authenticated shortcut and allowed architecture

A native record is a constant, literal, NOT, read-once decision, or decomposable binary Boolean operator. Each has an explicit fixed original-variable scope S_u containing every variable its predicate depends on, including declared unused variables. Native child scopes are subsets of the parent scope. A decision label is outside both child scopes; its parent scope is their union with that label. Decomposable binary children have disjoint declared scopes, with parent their union. NOT retains scope; constants may have nonempty free scope. These are the scope rules implemented in the runner. They deliberately strengthen any ambiguous support-only formulation.

A view u=(b,h) contains an explicit permutation h of the common universe [v], and S_u=h(S_b) exactly. Its predicate is f_u(alpha)=f_b(alpha pulled back along h). Reusing its scalar count is valid by assignment bijection. Reusing the view as an original-source residual additionally requires exact mapped-source identity, including free scope, or a separately charged sound certificate. Equal counts or hashes do not establish that identity.

All source normalization, map construction, candidate search, checking and failed attempts are paid. The theorem does not give a fast general graph-isomorphism algorithm. It allows actual DAG sharing and arbitrarily deep nested views. There is no small-global-group premise. A switch outside this architecture can be a legitimate algorithmic improvement; this theorem then makes no claim about that execution. Scalar-only termination is not a typed target handle.

## Restricted-context proof

A context at u is an injective map r:S_u->[v]. Store its ordered image tuple in increasing order of S_u, together with u's record ID. The image set alone is insufficient. Define the uniform compiler:

```
Expand(u,r):
    key = (u, tuple(r(i) for i in sorted(S_u)))
    if key is cached: return its pointer
    if u = View(b,h):
        r_b(i) = r(h(i)) for i in S_b
        result = Expand(b,r_b)
    else:
        child c receives r restricted to S_c
        rename a literal/decision label i to r(i)
        create the same native operator with declared scope r(S_u)
    cache key -> result
    return result
```

Begin every requested handle with the identity restricted to its scope. No full accumulated map or enumeration of the generated permutation group is needed.

Induct on decreasing record IDs. For an assignment alpha on [v], the invariant is
Eval(Expand(u,r),alpha)=f_u((alpha_(r(i)))_(i in S_u)),
with declared scope r(S_u). The predicate is well-defined on that assignment because S_u contains all its variables.

Constants retain their free scope; literals use r(i). Native operations commute with substitution. Injectivity preserves disjointness of binary children and exclusion of a decision variable from its descendants. Child scopes being subsets makes restriction defined. At a view, h(S_b)=S_u ensures every required h(i) is in the domain of r, so r_b=r composed with h on S_b is defined and injective. The view semantics gives exactly the induction claim. Thus outside-scope action cannot re-enter through a later view: a base variable's image must first land inside the current declared scope. This is the missing composition justification requested by the prior report.

Equal restricted keys consequently produce identical compiler subproblems, not merely equal scalar answers. Dependencies strictly decrease, giving termination. A native key produces O(1) ordinary DLDD nodes after literal normalization; a view key is a pointer alias. Scope annotations have a separate bit cost. Memoization never assumes that two different keys denote the same function.

Let Q be the number of reachable keys in the recursive closure starting all M created handles at identity, retaining a shared analytical cache. Then every handle and their joint expansion use O(Q) native nodes. For each producing/final-closure event, its prefix expansion from scratch uses at most O(Q) nodes; this bounds its extension cost kappa_j even if its current library contains nothing useful. There are at most M normalized producing events; joint outputs are bounded by their total created records. Hence
sum_j kappa_j <= O(MQ),
and for any fixed c>=0 and disjoint charged actions q_j>=1,
D=sum_j max(kappa_j-c q_j,0)<=O(MQ).

This is an upper bound on the handoff's closed completion defect. It does not assert that A physically performs this expansion, nor that analytical history is free resident storage. Native no-output actions have zero positive progress; deletions cannot improve remaining completion potential. Physical rebuilding by A is charged again.

Always Q<=sum_u (v)_(|S_u|), with falling factorial (v)_s. Also Q<=gM if all maps lie in a group of order g, recovering the former bound. These are upper bounds only. Assuming Q polynomial without proof would merely restate the missing premise.

## A substantive polynomial subclass without a small group

Fix k>=0 independently of X and require every view base scope to have size at most k. Native roots and native operations may have arbitrarily large scopes. For v>=1,
Q<=M(1+v^k).

To prove this, follow any reachable recursion path from an identity root. Before its first view, native descent keeps the context equal to the identity on each child. After crossing a view, scope size is at most k and never grows: native descent takes a subset and every view preserves cardinality. Therefore a node of scope greater than k can only have its identity context. Each smaller-scope node has at most (v)_s<=v^k contexts. Summing over M records gives the bound. For v=0 there is just one empty context per record; equivalently replace v by max(1,v).

It follows that expansion is O(M(1+v^k)) and closed defect is O(M^2(1+v^k)), independently of depth or global group order. The condition is checked by a scan of declared view scopes, not by solving a group-size problem. Adaptive choices remain legal when every selected view satisfies it.

The new family illustrates the distinction. For v>=3, create native literals x_0,...,x_(v-1). For each i=1,...,v-1, view x_(i-1) under the full-universe adjacent transposition (i-1 i), obtaining x_i. Join x_0 and those views using native decomposable ANDs. The root has scope v, each view has scope one, M=3v-2, and the maps generate Sym([v]) of order v!. Adjacent transpositions generate every permutation by successive adjacent swaps. Thus the former small-global-group premise fails asymptotically, but this theorem gives a polynomial ceiling. For this particular history Q=4v-3; the new lemma is not claiming that its predicate is hard. This is a legal internal typed-DAG control, not a new T5 reduction or a decision-hard family.

## Uniform costs and same-execution ledger

The compiler is uniform given the authenticated finite history. Let B be its explicit history/source/certificate bit length. Put
L=ceil(log2(M+Q+v+2)),
H=N+B+(M+Q+1)(v+1)L.
H covers maps, scopes, IDs, context keys, output annotations and stack. Exact sequential table scans implement restriction, view composition and cache lookup without unit-cost word/address assumptions. O(M+Q) processed calls of bounded fanout, comparisons over O(H)-bit data and explicit tape scans give a conservative polynomial envelope O(H^6) bit time and O(H) span, hence physical CM O(H^7), for this separate compiler. These deliberately loose bounds do not certify arbitrary semantic source certificates: their checking/reconstruction cost must be added if not already discharged in A's paid authenticated history. Syntactic map/scope checks and exact explicit mapped-source list comparison are ordinary finite scans within such an envelope.

No efficient discovery bound is inferred from the existence of an expansion. Likewise, a compact evaluator need not materialize a relation at all.

| Stage | Required charge and distinction |
|---|---|
| Parsing/source authentication | Read original N bits; verify strict C, frame/domain normalization, complete scope and exact residual-source identity. Existing construction proofs retain their own hypotheses. |
| Discovery/failed candidates | Pay for all candidate maps, failed identities, parameter choice and certificates. No isomorphism oracle or free advice. Scope-size check is cheap; finding useful maps is separate. |
| Representation changes/switching | Pay map access, restriction, scope transport, allocation and every chosen mode. Unsupported modes leave this theorem's scope. |
| Queries, accesses and addresses | Pay actual source rereads, pointer lookups, index bits, head travel and caches. No virtual residual service or prescribed old-cut visit is required. |
| Retention/sharing | Charge source, maps, keys, buffers, exact counts and pointers simultaneously. One physical shared object counts once. O(Q) native nodes is not O(Q) physical bits. |
| Recompute/history | Recreated IDs increase M; erased data must be reconstructed at cost. Analytical history used in the proof is not a free store for A. |
| Evaluation/output | A view reuses an exact scoped count; copying/pointing and O(v)-bit arithmetic are charged. Native counting includes missing free-variable factors, NOT uses 2^|S|-Z. Write the final O(N)-bit T5 count and terminator; typed closure remains required. |
| Resource conventions | Compiler time, A's time, physical CM, description CM and witness node counts remain separate. No overlapping demands are summed or multiplied. |

Under fixed A,K,a,k and the same cap, v<=N and M=O_A(N^a). The new representation ceilings are O_A(N^(a+k)) nodes and O_A(N^(2a+k)) defect (k=0 also covered). They are not compulsory physical costs. The original cap ledger remains:

| Resource of A's same execution | Ceiling |
|---|---|
| Peak physical storage | O(N^a) |
| Physical cumulative storage | O(N^(2a)) |
| Minimum-description cumulative information | O(N^(a+1)) |
| Encoded-input count-map circuit gates | O(N^a log N) |

If the target also satisfies the handoff's separately justified DLDD demand 2^(Omega(sqrt(treewidth))), the fixed-k architecture under a polynomial cap implies treewidth O(log^2 N). This consequence is CONDITIONAL on that target representation theorem and the declared architecture. No unrestricted exponent is excluded, no padding regime is changed, and no decision consequence follows from the all-SAT NAND image.

## Reproducible finite evidence

Run from repository root with Python 3 and assertions enabled:
```
python experiments/t5_discovery_scope_context1_20261121.py > results/raw/t5_discovery_scope_context1_20261121.json
```

New code SHA-256: ca45bfd0eb1cf2d10c8fcfb4842e9a4aa1068c386af03c70982806d45aad00e0.
Dependency: experiments/t5_redteam_group_rename_audit1_20261121.py at commit 55805b5b8f8d6a453ddebb029a74b71de5252d07, SHA-256 0166c3f184725e8929acea8f938874b4ac781b78ba4d746450663f8a74a61630. The runner checks that hash before import. This is an integrity check, never a semantic merge proof.

The imported direct evaluator transforms assignments at each view; the new compiler independently transforms restricted label maps. Every output constructor checks typing. Reusing the prior test generator is warranted by the new cache-key algorithm; it is not a rerun presented as a new independent audit. Original raw evidence, blob 34ec395e70c7e29a0e2fb598d50fd1dd5b863cd7, was recovered. No second strict-C source enumeration was needed; its n=7,m=8,N=87 count30 remains prior evidence.

| Group/universe | M | New restricted keys | Prior full keys | New native nodes | Assignment checks |
|---|---:|---:|---:|---:|---:|
| S2 / 2 | 942 | 1812 | 1884 | 110 | 1688 |
| S3 / 3 | 1035 | 5219 | 6210 | 366 | 10704 |
| S4 / 4 | 1168 | 14760 | 28032 | 1306 | 90240 |
| D5 / 5 | 1379 | 10182 | 13790 | 1632 | 78720 |

These broad test calls start roots under all listed group elements, not just identity; their key counts test the invariant and are not claimed to equal the theorem's identity-root Q. Chains have depth24; all16 binary operators, complement, decomposable XOR, inconsistent affine, forced singleton, private-leaf star, path-independent-set, shared/rebuilt and free-scope controls are included. Original comparison tables are not asymptotic data.

The new adjacent-transposition family v=3,...,8 has Q=9,13,17,21,25,29 with M=7,10,13,16,19,22, checking all504 assignments in total. Group orders were enumerated only through v=6; v=7,8 use the symbolic adjacent-transposition proof, explicitly marked null for enumeration in raw evidence.

Additional controls reject caching by image SET alone: implication x_0->x_1 differs from its swap at (1,0), despite identical image sets. Empty-universe constants and one declared free variable are checked. Counts and detailed-row digests are reproducible; no physical benchmark, exhaustive search of all DAGs or kernel proof build is claimed.

## Controls, gates and scope

Affine/Tseitin: the symbolic proof transports an already typed predicate only. A Gaussian scalar result does not supply a typed base, so no known affine obstruction is evaded. Small finite affine controls test map semantics only. Private-leaf trees and matching instances retain their cheap dynamic programs; their many residuals are not charged as distinct necessary work. Forced-domain propagation remains legal; no syntactic-width hardness inference is made. Native NOT preserves complement cheaply in DLDD, without asserting this for plain DNNF.

Renaming/sharing/recompute are the proof's explicit subject. Relocation changes physical access cost, not context semantics, and forces no return to original cuts. Full-state entropy obstruction remains H(output|complete correct deterministic state)=0. Decision witnesses and arbitrary virtual residual queries are not required services. Failed authentication or a context-budget cutoff means UNKNOWN for this certificate, never UNSAT.

DISJ: NOT APPLICABLE, no communication lower bound. Relativization: OPEN for unrestricted transfer; no claimed nonrelativizing step. Simultaneous DTISP: PASS for distinct same-execution ledgers, OPEN for a compulsory violation. Deterministic configurations: PASS for scope, no runtime bound from state counts. Natural Proofs/algebrization: no new unrestricted circuit lower bound or barrier bypass.

## Recovery and fresh source/search log

Current base c5d8802644abe2caef15ef67153fa76ab8da1152. Complete baseline/instructions were recovered at startup in this continuous session: handoff blob a886f3387a8676b9cc86afbf3bebf22630109d49, 141084 UTF-8 bytes, SHA-256 c9a3a0f362c72dfad7548b0cd44723853f105dcdc6a4f9ea5fef4559d3bb2a33; assignment 776c2622d69dbcbb1c7c0d1361f299970fb7f1cc; AGENTS 01f05d238736da1a3a2a10c9586be3d882751212; CODEX 15639f62a254aa9cd36a949b9f9d81985e5ed538; research instructions 6f37fc1a1713b01abd91794d5523fb05a57efa2f. They remain baseline claims under their stated hypotheses, not independently recertified.

Recovered own full 09:54 report at [3168128](https://github.com/j15marti/pnp/blob/3168128105d8f040f41f8a49da8d6f0deffb9112/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-21_095400_Small_Group_Nested_Rename.md), full handoff b55f30204fe8a7a00d9863e47eacbe730ab30e10, and the [Redteam reconstruction](https://github.com/j15marti/pnp/blob/55805b5b8f8d6a453ddebb029a74b71de5252d07/research/agents/charged-redteam/PNP_Charged_redteam_2026-11-21_101500_Group_Context_Audit.md), original code/raw. Current issue324 supplied Synthesis's 4c1d7f5 variable-multiplier budget and Construction's c5d8802 unweighted three-color claim; neither is a premise of this compiler proof. The interrupted Accounting candidate was not completed or published. A bounded repository search for T5-CONTEXT-ORBIT1 found this open dependency in Discovery/Redteam, not a completed solution. No historical novelty claim.

Fresh literature queries on this run: “Variable Shift SDD identical vtree rule substitution equivalent 2020”; “Beame DLDD definition read once decomposable 2017”.
Read [Beame, Li, Roy, Suciu, TODS42(1),2017, Definition2.4](https://homes.cs.washington.edu/~beame/papers/numsat-journal.pdf), DOI10.1145/2984632, pp9–10. Its DLDD model permits native NOT and decomposable binary Boolean operators with read-once restrictions. It supplies the native model, not this context lemma or an arbitrary scalar compiler.
Read [Nakamura, Denzumi, Nishino, SEA2020 article22, Theorem6 and identical-vtree rule](https://drops.dagstuhl.de/storage/00lipics/lipics-vol160-sea2020/LIPIcs.SEA.2020.22/LIPIcs.SEA.2020.22.pdf), related full version arXiv:2004.02502v1. The theorem concerns compressed trimmed VS-SDDs on isomorphic vtrees and specified substitutions. Its scope/context discipline motivates the falsifier; no SDD canonicity or succinctness theorem is imported to arbitrary DLDDs. Both primary PDFs were available this run.

Fresh connected repository query “memoization variable scope permutation” under each of anthropics, openai, xai-org, google, google-research and google-deepmind returned no matches. Bounded web fallback queries: site:github.com/anthropics “memoization” “permutation”; site:github.com/openai “memoization” “scope”; site:github.com/xai-org symmetry SAT; site:github.com/google/or-tools symmetry permutation; site:github.com/google-research permutation memoization graph symmetry; site:github.com/google-deepmind permutation memoization symmetry.

Result screens: no applicable official Anthropic or xAI result returned. [OpenAI plugins React memoization guidance](https://github.com/openai/plugins/blob/main/plugins/build-web-apps/skills/react-best-practices/AGENTS.md) is UI material, not a diagram theorem. [Google Research fast-soft-sort/numpy_ops.py](https://github.com/google-research/fast-soft-sort/blob/master/fast_soft_sort/numpy_ops.py) concerns numerical permutation inversion, not exact compilation. DeepMind [mathematics_dataset](https://github.com/google-deepmind/mathematics_dataset/blob/master/mathematics_dataset/modules/arithmetic.py), [DNC addressing](https://github.com/google-deepmind/dnc/blob/master/dnc/addressing.py) and [AlphaTensor-Quantum](https://github.com/google-deepmind/alphatensor_quantum) returned permutation-related snippets but no scoped DLDD result; no proof imported. These are bounded snippet screens, not exhaustive repository audits; no new commit pin is claimed for files not deeply inspected.

Relevant known official repository file rechecked: [Google OR-Tools symmetry.h](https://github.com/google/or-tools/blob/100f66e6242ab8bf8d32feb8f3bf086db66ae2b5/ortools/sat/symmetry.h), commit100f66e6242ab8bf8d32feb8f3bf086db66ae2b5, blob2a82516f6c77145b1f56c9046ba536cdcf1e4fb7. Its full-problem symmetry assumption and guard for newly introduced literals reinforce the need for authenticated scopes. Its heuristic SAT propagation is not this compiler and proves no lower bound; no external code/build imported.

Official ownership verified earlier in this continuous session is retained, not inferred from product names: [Anthropic verified domain](https://github.com/anthropics), [OpenAI verified domain](https://github.com/openai), [xAI's repository links](https://x.ai/open-source), [Google Research corporate link](https://research.google/pubs/implicit-rate-constrained-optimization-of-non-decomposable-objectives/), [DeepMind corporate repository link](https://deepmind.google/blog/open-sourcing-mujoco/), [Google OR-Tools](https://developers.google.com/optimization). Fresh searches and prior logs were combined to avoid redundant unrelated deep reviews.

## Publication and next dependency

Only Discovery's separately named report/handoff and new experiment/raw files are written. No local checkout exists, so repository preflight and LaTeX compilation were not run. No TMR manuscript is owned by this role; no manuscript, schedule, enabled state or peer file changed. The prior Redteam dependency is read/imported unchanged.

Return to Redteam and Synthesis: the former instruction to retain full permutations can now be replaced, within these explicit scope rules, by the ordered restricted-key compiler and proof above. Adversarial review should attack outside-action re-entry and the large-scope identity argument before accepting the new result. This same continuous assistant session is not external independent review.

Next is T5-LARGE-SCOPE-CONTEXT1 as stated at the start. The unrestricted scalar bridge and **P versus NP remain OPEN**.

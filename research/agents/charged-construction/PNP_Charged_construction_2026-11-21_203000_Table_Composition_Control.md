# Explicit table composition is a polynomial dynamic-compatibility control

21 November 2026, 20:30 PST, America/Los_Angeles. Charged Construction.
**DYNAMIC-TABLE-COMPOSITION1. PROVED/EXACT** for the explicitly encoded Boolean family below. Its proposed role as a superpolynomial compulsory-stage family is **FALSIFIED/RETIRED**. Finite evidence is **COMPUTATIONAL**; independent adversarial review pending. P versus NP remains OPEN.

This responds to the new Construction assignment after completion of the preceding Synthesis task. It adds one family with input-dependent successive addresses, rather than another static comparison. The construction has both decision labels and adjacent local Horn/dual-Horn witnesses. Nevertheless, its stages force one deterministic path, which a globally correct solver can compute once and cache. This is a completed rejection of this candidate's hardness role, not a claimed advance toward an unrestricted lower bound.

## 1. Claim, quantifiers and falsifiers

For every r>=3, L>=1, explicit total tables f_1,...,f_L:[r]->[r], and endpoints s,t in [r], define the proper Boolean 3-CNF B below. Then
\[
B\text{ is SAT}\iff f_L(f_{L-1}(\cdots f_1(s)))=t.
\]
There is one fixed uniform correct solver on all valid Boolean compatibility inputs with a polynomial authenticated fast path on every canonical encoding of B; outside that image it uses a correct total fallback. Its successful sole-tape path has the conservative bounds T=O(N³), S=O(N), physical CM=O(N⁴), descriptive CM=O(N⁴). These are upper bounds for that one solver on this family, not global polynomial SAT bounds.

For any lower-bound comparison first fix a total correct deterministic solver A and a proposed cap T_A<=K N^a, a>=1 and K fixed. Use exactly the transport report's finite-alphabet single-head writable tape, fixed-origin Boolean output, all source/work/cache/address charges, and no free clock or source oracle. The exhibited fast path is a particular solver, not every A.

Four falsifiers:
1. Some proper generated CNF has a decision label different from the composed endpoint.
2. An exponentially large table or succinctly represented number of stages is omitted from N.
3. Compiler ordering or metadata silently reuses the old separated-input layout.
4. The supposedly compulsory repeated work collapses to one paid computation and a cached answer.

The first three are excluded by the construction/proof and checked at small parameters. The fourth occurs. No NP-completeness is asserted for this family.

## 2. Complete source clause generator

Use Boolean variables Z_{j,v}, 0<=j<=L,1<=v<=r, with ID jr+v. At every layer impose exactly one true Z. Introduce r-3 fresh chain variables a_{j,h}, h=1,...,r-3, with IDs
\[
(L+1)r+j(r-3)+h.
\]
Finally introduce two shared padding variables
\[
p=(L+1)(2r-3)+1,\qquad q=p+1.
\]
When r=3 the chain list is empty.

For every binary clause A OR B use the proper-width-three pair
\[
(A\lor B\lor p)\land(A\lor B\lor\neg p).
\]
This equals A OR B for either value of p. For a unit Z use the four clauses \(Z\lor \epsilon p\lor\delta q\), with epsilon,delta independently positive or negative. Their conjunction equals Z for every choice of p,q.

The ordered source F consists of:
1. Four clauses pinning Z_{0,s}, followed by four pinning Z_{L,t}.
2. For j=0,...,L, one at-least-one chain followed by padded clauses \(\neg Z_{j,u}\lor\neg Z_{j,v}\) for all 1<=u<v<=r, lexicographically.
3. For j=1,...,L and v=1,...,r, padded transitions
\[
\neg Z_{j-1,v}\lor Z_{j,f_j(v)}.
\]

The at-least-one chain is the single clause Z_{j,1} OR Z_{j,2} OR Z_{j,3} when r=3. Otherwise use
\[
(Z_{j,1}\lor Z_{j,2}\lor a_{j,1}),\quad
(\neg a_{j,h}\lor Z_{j,h+2}\lor a_{j,h+1})\ (1\le h\le r-4),
\quad
(\neg a_{j,r-3}\lor Z_{j,r-1}\lor Z_{j,r}).
\]
Every clause has three distinct variables. Sharing p,q across padding gadgets is sound because the identities hold pointwise for every p,q.

Exact source sizes:
\[
n_0=(L+1)(2r-3)+2,\qquad
m_0=(L+1)(r^2-2)+2Lr+8.
\]
The per-layer contribution is r-2 at-least-one clauses plus r(r-1) padded at-most-one clauses.

**Decision proof in both directions.** In any source model, exactly one Z at each layer is true. The initial pin identifies its first vertex as s. The transition out of that true vertex forces the next layer's true vertex to be f_j of the previous one. Induction therefore gives the unique layer path, and the last pin requires its endpoint to equal t. Conversely, when the composition reaches t, set exactly that path's vertices true. All transition clauses and both pins hold. For each chain choose \(a_{j,h}=\neg(Z_{j,1}\lor\cdots\lor Z_{j,h+1})\), which satisfies the OR chain. Either choice of p,q is legal. Thus a full source model exists.

These are projected unique layer paths, not unique complete satisfying assignments. No parsimonious count claim is used.

## 3. Adjacent-witness target and exact physical encoding

Introduce y=n_0+1, u=n_0+2, v=n_0+3. Emit the four selector clauses
\[
(y\lor u\lor v),\ (y\lor u\lor\neg v),\
(y\lor\neg u\lor v),\ (y\lor\neg u\lor\neg v).
\]
For source clause position i=1,...,m_0 with ordered literals (A,B,C), introduce z_i=n_0+3+i and emit consecutively
\[
(\neg y\lor A\lor z_i),\qquad(\neg z_i\lor B\lor C).
\]
This is precisely the established adjacent-witness compiler, applied to the newly derived clause list. Projection gives y AND F, so both SAT and UNSAT equivalences survive.

Let H consist of clauses with at most one positive literal; let D contain the rest. Set alpha to u=1 and everything else zero, and beta to u=v=1 with all other variables zero. Every H clause has at least two distinct negative variables, so alpha satisfies H. At beta, every compiled source pair is satisfied by its negative y or negative z_i literal; all dual-Horn selector clauses also hold. Thus beta satisfies D and the witnesses differ in one bit. No source-variable assignment is supplied by either local witness.

Exact target sizes:
\[
n=n_0+m_0+3=(L+1)(r^2+2r-5)+2Lr+13,\qquad m=2m_0+4.
\]
Serialize
\[
1^n0\;\gamma(m+1)\;[\text{ordered sign-plus-ID triples}]
\;[\alpha]\;[\beta]\;[y\text{-ID}]
\]
with w=ceil(log2(n+1)). The full bit length is
\[
N=3n+2+2\lfloor\log_2(m+1)\rfloor+3m(w+1)+w
=\Theta(Lr^2\log(Lr)).
\]
L>=1,r>=3 throughout. All tables are explicit: their descriptor has Lr entries of ceil(log2(r+1)) bits plus L,r,s,t headers, bounded by O(N). The formula lists all layers, so L is not an uncharged exponentially large iteration count.

Physical clause order is selector first, then compiled endpoint pins, then all layer constraints, then transitions in increasing j,v order, then witness/release trailer. Each source row becomes two adjacent target rows. Target identifiers are fixed from positions. This is not the separated L_pi M R_sigma layout, and no previous quadratic or cubic lower bound is transferred to it.

## 4. Authenticated cheap solver and complete costs

The partial evaluator receives only target bytes, not the source tables as an oracle. Parse its entire header, literal list, witnesses and release ID. From target n,m recover m_0=(m-4)/2 and n_0=n-m_0-3. Enumerate r=3,...,n_0, retaining only integers
\[
L=(n_0-2)/(2r-3)-1\ge1
\]
that satisfy the exact m_0 formula.

For a candidate, extract proposed source literals from the guarded clause pairs. Extract s from the first unit gadget and t from the second after subtracting Lr. Read proposed f_j(v) from the known transition source-row positions and subtract the layer offset jr. Reject any out-of-range field. Regenerate the entire source and target, and compare every bit including metadata and endpoint. Only exact equality admits the candidate. This verifies guard and helper IDs too; merely stripping those clauses would not.

On acceptance follow z_0=s, z_j=f_j(z_{j-1}), and decide whether z_L=t. Multiple admitted descriptions cannot produce conflicting answers because each has the proved equivalence to the same target formula. A failed candidate is paid work; if every candidate fails, return UNKNOWN and invoke exhaustive SAT fallback on the retained original input. Neither parser rejection nor failed family membership proves UNSAT.

A direct fixed-multitape implementation keeps O(N) bits for original input, a proposed source, target regeneration stream, tables and O(log N)-bit counters. O(N) candidate r values each permit at most O(N) bit work for candidate generation/comparison; integer tests and bounded scans fit a conservative O(N²) multitape budget. Successful table evaluation can scan each explicit table once, comparing current vertex IDs and retaining just the next vertex, O(Lr log(Lr)) bit work. A source-to-target generator, including supplied-table validation, fits the same conservative O(N²) budget and O(N) storage. Malformed counts are bounded against remaining source before allocations.

A fixed number of virtual tapes with O(N) span can be simulated by O(N)-length sweeps per virtual step on one physical tape. This gives the conservative sole-tape cost O(N³) and physical span O(N), hence physical CM O(N⁴). Self-contained configuration descriptions replay the N-bit source and a transition index, so descriptive CM is O(N⁴), separately. No claim of optimal exponent is made.

The ledger charges all parsing, table validation, parameter discovery, rejected candidates, regeneration, exact comparison, indexed access, copies, simulated movement, output, buffers and cached records. No hashing certifies semantics. No exponential validation loop in the finite test is part of this production algorithm. All source acquisition/reduction time is included rather than subtracted from an imported lower bound. On the same recognized execution, after computing the decision, A may cache its one-bit answer and output it locally; it need not revisit the original layer records.

For a separately proposed cap KN^a the general ceilings remain S=O(N^a), physical CM=O(N^(2a)), descriptive CM=O(N^(a+1)). The count-map O(N^a log N) simulation ceiling pertains to a count solver and supplies no counting claim here. Our O(N³) family solver demonstrates a polynomial escape; it does not exclude or establish all smaller exponents. No sum or product with another solver's cost is used.

## 5. Proposed obligation and why it fails

The feature absent from static equality is the dependent lookup address: layer j's queried v is determined by earlier tables. A candidate compulsory obligation would set U_j to that next vertex and try to charge a fresh comparison/transport at every syntactic layer, even after joint preprocessing.

For the explicit path-following algorithm one may record the actually accessed table word with its real address, framing and stage identifier. Let B_j include the current vertex and all retained source/cache information, E_j be the actual primitive accesses/movements, Pi_j their self-delimiting record, and rho the actual maximum overlap. Such records can describe this algorithm. They do not prove every correct solver answers this sequence of intermediate questions, or incurs it again after computing the endpoint.

If B_j contains the whole stored tables, U_j is mathematically determined and H(U_j|B_j)=0, although accessing it still has a physical cost. If B_j excludes tables, a separate locality and decoder theorem is needed. After caching the final answer, a proposed full-path decoder from the final suffix is generally impossible. The Synthesis reachable-splice criterion at 790875f74755a178e8ad810b67ebd603c10f6e89 gives the precise danger: valid original hybrids need not be reachable hybrids of cached states.

Therefore the shared inequality
\[
\mathbb E T\ge
(\sum_jH(U_j|B_j)-\sum_j\mathbb E h_j)/(b\rho)
\]
is available only after its decoder and event premises are proved. No positive universal demand or rho=1 is asserted here. There is no forced online schedule. An all-UNSAT correctness promise would be weaker still and permit an immediate negative answer.

The construction is retained as a **forced-domain, dependent-address control**. Its superpolynomial hardness role is retired by the explicit globally correct fast-path solver. This is not a counterexample to every possible dynamic transfer technique.

## 6. Finite evidence

[Code](../../../experiments/dynamic_construction_table_chain_20261121.py) and [raw](../../../results/raw/dynamic_construction_table_chain_20261121.json). Run:
    python experiments/dynamic_construction_table_chain_20261121.py

The code uses the pinned transport generator for the last compiler, independently generates all source rows, uses exact-byte authentication, exhausts one-hot layer paths, checks local Horn/dual-Horn witnesses, and constructs full target witnesses on SAT cases.

| r,L | Table/endpoint cases | SAT | UNSAT | n,m,N |
|---|---:|---:|---:|---|
| 3,1 | 243 | 81 | 162 | 39,60,1395 |
| 3,2 | 6561 | 2187 | 4374 | 55,86,1991 |

All 6,804 cases pass. Four further r=4,L=3 cyclic/constant-map cases include both labels, with n=113,m=180,N=4682. Two malformed inputs return UNKNOWN. Raw rows retain tables, endpoints, result and input fingerprint with a declared column schema. No randomness is used. These checks exhaust the table/endpoint parameter space at the two listed sizes and the one-hot layer choices; they do not enumerate every auxiliary assignment of the target or benchmark a physical Turing-machine prefix.

Script SHA-256: 1954a54d93773b1b96bf1c75a6fef108cbabaea6049866d66276350aede39624.
Raw SHA-256: 5a8781dafcf300cf49c3ad1ab1b05c59bbf228bb9206395dfe9ff5051975db00.
Imported transport generator SHA-256: 98b46a013cabc3f969bcf58c08da2b1fd6937a26e1b46e75a06318e03d34d4f4.
The parsing helper is the preceding Synthesis script at commit790875f74755a178e8ad810b67ebd603c10f6e89. No old baseline experiment was rerun. The new test concerns table composition and its newly derived encoding.

## 7. Controls, recovery and fresh searches

Boolean decision only. Symmetric C, ordered R and historical S/Q do not occur in this construction. Counting projection multipliers are not inferred from the existential compiler. Equality and forced-domain sanity PASS through the explicit path. Relocation, sharing, complement and global algebra remain legal. Private-leaf and affine/Tseitin controls are not restricted by this solver; UNKNOWN leads to a correct fallback. Syntactic stages and witnesses are not compulsory execution events. Simultaneous DTISP PASS for the displayed one-realization upper bounds. Configuration counting is not used as a lower bound. Relativization, Natural Proofs and algebrization yield no unrestricted separation claim.

Recovered current continuation/transport definitions, AGENTS/CODEX/research skill, relevant T5 model/cap definitions, Construction's full previous orbit-width report/handoff/evidence, and the current peer work during this continuous task. The prior Construction result remains an easy strict-C control; this new family is Boolean and has a different N. Complete current handoff body and SHA were checked before replacement. No full checkout or LaTeX preflight was run. No TMR manuscript ownership is acquired.

Fresh task-specific repository query "pointer composition compatibility" returned an earlier compatibility-selector DP audit and binary-adhesion composition excerpt. These were treated as prior easy-composition context, not a new theorem dependency. No historical priority for pointer following is claimed.

Literature query "Nisan Wigderson rounds communication complexity pointer chasing 1993 original pdf" found their author-hosted STOC1991 preliminary paper [1]. Its model and introduction were read: pointers are held by different parties, with prescribed communication rounds; following pointers is itself an explicit upper-bound protocol. The current single offline solver may hold all tables, so a bounded-round lower bound cannot be silently imported. The fresh search also found [2], arXiv:2508.19158v1, 26 August2025. Its full HTML introduction and model discussion distinguish unlimited interaction from bounded-round results and retain a partition between two parties; it even notes sending full inputs as a shortcut in one regime. No theorem from either is used to infer SAT hardness. The construction proof and its paid evaluation are direct.

Fresh connector query '"pointer jumping" "composition"' under anthropics,openai,xai-org,google,google-research,google-deepmind returned no hits after one Anthropic429 retry. Web fallback queries:
- site:github.com/google OR site:github.com/google-research OR site:github.com/google-deepmind "pointer jumping"
- site:github.com/anthropics OR site:github.com/openai OR site:github.com/xai-org "function composition" SAT
returned unrelated third-party material and no applicable official implementation. No repository code was imported. Ownership of those exact scopes was verified in the immediately preceding recovery via GitHub domain verification and corporate repository links, recorded in [3], §8. No product-name match is accepted as ownership. No official repository commit was inspected for a table-composition theorem, so none is claimed.

## 8. One next dependency and receiving roles

**DYNAMIC-SHARED-CHOICE1, owner Construction with Accounting and Redteam.** Replace this uniquely forced path by an explicit compact Boolean compatibility mechanism with genuinely unresolved shared choices, then either produce an authenticated joint polynomial evaluator or prove one actual intermediate local decoder premise after paid preprocessing. The receiving test must include the reachable-splice/cache obstruction in [3]. Merely adding layers, growing interface width, or selecting a different clause order is insufficient.

Bounds should compare only a subsequently proved same-run demand to its fixed K,a; Discovery should seek the strongest shared evaluator; Redteam should independently verify the source projection, metadata authentication and all-input fallback. Synthesis should retain this family as a retired hardness candidate and a live control. No unrestricted lower-bound claim is promoted before review. Current roles, schedules, titles and manuscript ownership are unchanged.

## References

1. N. Nisan and A. Wigderson, Rounds in Communication Complexity Revisited, author-hosted preliminary STOC1991 paper; journal version SIAM J. Comput.22(1),211–219,1993. https://www.math.ias.edu/~avi/PUBLICATIONS/MYPAPERS/NW91/proc.pdf
2. O. Fischer, R. Oshman, A. Rosén and T. Roth, Pointer Chasing with Unlimited Interaction, arXiv:2508.19158v1, 26 August2025. https://arxiv.org/html/2508.19158v1
3. Synthesis, reachable checkpoints and original-source audit, internal review requested: https://github.com/j15marti/pnp/blob/790875f74755a178e8ad810b67ebd603c10f6e89/research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-21_202200_Reachable_Checkpoint_Splice.md
4. Boolean compiler, physical model and baseline, internal review only: https://github.com/j15marti/pnp/blob/2547822e9e82c914a668d9b4de2c6991e490d7f0/research/main/Charged_UNSAT_Transport_2026-11-21.md

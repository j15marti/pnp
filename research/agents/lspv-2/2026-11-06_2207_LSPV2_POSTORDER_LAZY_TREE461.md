% LSPV-2/461 report | 2026-11-06 22:07 PST
# LSPV-2/461: Postorder streaming eliminates the tagged-TREE global offset table

**Route A | PROVED/RESTRICTED abstract streaming schedule; CONDITIONAL same-machine virtual guest simulation; COMPUTATIONAL finite controls. P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE and four falsifiers
Hypothesis: LSPV-2/460's `Theta(h log N)` writable source-offset directory is an artifact of its heap-order block layout, not a lower bound for exact OR-folded SAT on authenticated balanced trees. Serialize the same owner-tagged strict proper 3-CNF blocks in *postorder* and process them immediately, preserving only the pending subtree-message stack and the current block's start/end indices. This is a different explicitly promised source layout, not a source-agnostic transformation.

F1: The parser cannot know the correct heap-node owner from the forward postorder stream. F2: some parent requires an earlier child source offset rather than the child's completed boundary table. F3: ordinary guest OR-folding loses an AND-required child or admits incompatible boundary values. F4: virtual guest input, random access, or reset actually requires an uncharged physical block buffer, remote directory, or cost beyond the claimed bounds.

**Search-induced revision:** Established prior work already covers treewidth / junction-tree message passing (Darwiche, IJCAI 1999) and running-intersection authentication (project LSPV-1/135 and ARC229); LSPV-2/459 already gave the TREE OR-fold equation. LSPV-4/456 gave *PATH* indexed virtual-guest access and /458 identified the **TREE** global offset table as an obstruction to blindly inheriting PATH's smaller space exponent. The present narrow new step is a postorder **TREE source layout**, a paired bufferless traversal, and a charged conditional composition with the existing /456 and /458 virtual-guest simulation. It is not a new SAT algorithm and not a new general treewidth theorem.

## Precise input language and family ledger
Fix a power-of-two-minus-one heap-indexed full binary tree with `h=2^d-1` nodes and maximum interface width `w`. Each node v owns one contiguous block `F_v` of original strict proper three-literal clauses, arranged in **left-child, right-child, parent** postorder in the read-only binary input. Use LSPV-2/460 tags `P(v,i)` for private variables and `E(c,i)` for the interface owned by edge from c to floor(c/2), with unique numeric encoding `((tau*V+owner)*I+i)`, `I=2^K`, `V=2^ceil(log2(h+1))`, `K=bit_length(N+1)`. The source header declares d,w; each block carries a clause count and exactly three signed literals per clause. The locally verifiable owner rule is unchanged from /460, but the block **order is changed**. Source parser rejects trailing/truncated, illegal ownership, nonincident edges, repeated underlying variables, and broken headers. Impose `h,Lmax <= N^(1/2+o(1))`, `w <= (log2 N)/10+o(log N)`, and a balanced depth O(log h). A malformed or valid general CNF outside this promised grammar is NOT covered by the restricted theorem.

For established hardness control choose Urquhart's odd-charge cubic-expander Tseitin formulas: on a connected 3-regular H-vertex edge expander, one variable x_e per edge; for each vertex v with charge chi_v include exactly four clauses excluding assignments to its three incident edges whose parity differs from chi_v. Then 4H original strict ternary clauses, 3H/2 variables, binary length Theta(H log H), odd total charge implies UNSAT; suitable expanders have 2^Omega(H) ordinary shared-DAG Resolution refutations (Urquhart, JACM 1987), NOT arbitrary-machine hardness. The legitimate GF(2) charge-sum shortcut decides these families in polynomial time. Their intact-packet separators are large (LSPV-4/457), so they are an obstruction to automatically obtaining this restricted postorder grammar; no lower-bound-preserving reduction to small-width tree layout is asserted.

## Theorem 461.1: offset-free postorder evaluation (PROVED/RESTRICTED)
At the moment the stream reaches block v, messages for its two children are the top two completed entries on a LIFO stack; the current original block is contiguous and can be indexed using two O(log N)-bit endpoints. For each parent-interface assignment b define exactly
$$
M_v(b)=\mathrm{SAT}\Bigl(F_v\wedge\mathrm{pin}(E(v),b)\wedge\bigwedge_{c\in\mathrm{child}(v)}\ \bigwedge_{a:M_c(a)=0}D_{c,a}\Bigr).
$$
Here D_(c,a) is the genuine clause falsified exactly by interface assignment a. Every child's forbidden assignment is an AND conjunct. Each SAT guest existentially handles all *allowed* child assignments as an OR. A variable occurs outside a child only on its declared E(c) interface, so conjunction of child feasibility predicates is exact. No shared branch-local conclusion crosses an unrepresented assumption. After computing M_v, discard its two child tables. Induct on postorder to prove correctness of the root value.

The postorder stream determines v from a balanced traversal counter/stack in polylog N writable bits. No globally indexed table of h source offsets is built. At most O(log h) interface tables of at most 2^w bits coexist. The current read-only block is referred to by its two endpoints, **not copied** into writable space. The independent host implementation additionally materializes local guest CNFs for finite control: host RAM does NOT establish the abstract writable-space theorem.

## Theorem 461.2: CONDITIONAL lazy-guest resource composition
Add the explicit model premise that the original source clause records can be exposed at guest input positions by a deterministic indexed transducer using polylog N time and writable bits per access, with the child guest encoding *identical to the fixed general-CNF encoding accepted by A*. The provider synthesizes a legal guest header, unchanged current-block clause bytes, parent pins, and disallowed-child clauses, without materializing the whole guest. Each child message also has a rank/select table over its 2^w entries so access to the j-th forbidden clause costs polylog N, rather than secretly scanning the bitmap. Charge virtual guest read/write/index/head moves, restart epochs and high-water work space as in LSPV-4/456 and /458. This is a stated representation/simulation premise, not independently executed native FLMV bytecode.

There are
$$
q\le(h-1)2^w+1\le N^{3/5+o(1)}
$$
guest calls, each on a genuine ordinary CNF of encoded length
$$
B=O(L_{\max}+2^w w\log N+\mathrm{header})\le N^{1/2+o(1)}.
$$
Streaming validation reads O(N) source bits, local preparation and child rank tables cost O(h 2^w polylog N), and guest execution costs O(q B^t polylog N). Therefore, for fixed total correct A with t>=1 and s finite,
$$
t'\le\max\{1,3/5+t/2\},\qquad
s'\le\max\{1/10,s/2\},
$$
under the compatible same-machine virtual-port premise, since live local tables O(2^w log h) and current source indices polylog N replace the former O(h log N) offset directory. This strengthens the *restricted TREE implementation* envelope of /460 from local space exponent 1/2 to 1/10, but only for postorder sources and indexed lazy guests. It does not establish contraction on all inputs, recursion on the generated ordinary-CNF guest, or an unrestricted machine conversion.

An actual implementation must charge original input discovery, source parser, all input/index reads, rank/select construction, guest interpreter and high-water epochs, failed calls, message retention, output and all-phase peak. If the provider does not supply polylog indexed access, revert to materialized-child time/space from /459; do NOT claim the smaller bound. Logical work, certificate evidence bits, parallel span and physical execution costs remain different measures.

## Finite reproducibility
Executed Python original signed-3CNF source producer and forward-only online postorder implementation: 18 sources (9 SAT and 9 UNSAT, the UNSAT cases use **local complete three-variable signed 8-clause contradiction controls**, NOT certified expander-hard instances), balanced h=3,7,15; 282 actually executed local DPLL guests; 198 assertion groups pass; 108 malformed-rejection checks pass (two independent parser paths). Independent Node.js verifier reconstructs all 18 serialized sources and checks root satisfiability against independent whole-formula DPLL: 126 checks, 54 negative controls, 282 guest computations, PASS. Python implements an online scan with no source-offset directory, but uses a materialized local guest DPLL; Node tests exact semantics. Neither is native FLMV runtime/peak-space verification. SHA256: Python `6a0d298266b4d723c4bdd9be60d5795fe44d888e6a11e325b97402f29e16e4c2`; Node `514cb2dc43a2d29ad38c0a04341c37ae2f8a0d73a5303c34912f2021ce3d1e7e`; raw `34970aec09bfebd17910dc233d2eee66a332f2204095e3ae65296ee3d0c1b2fa`. Full unedited scripts, fixture bits, raw records and integrity manifests included in run archive.

## Source/authentication ledger
Actual project reads: `proof1.txt` [P1-S3], [P1-01], [P1-03], [P1-04]; `proof2.txt` [P2-A2], [P2-A4], [P2-A5], [P2-B2], [P2-D1]; coordination issue #3 and latest comments; AGENTS.md, CODEX.md, project SKILL.md; LSPV-2/459, /460; LSPV-4/456, /457, /458; earlier running-intersection LSPV-1/135; GROKPROOF/2026-11-06_2316_PROGRESS.md; Claude world-ledger README. Primary references: Fortnow-Lipton-van Melkebeek-Viglas JACM 2005 DOI 10.1145/1101821.1101822; Urquhart JACM 1987 DOI 10.1145/7531.8928; Darwiche IJCAI 1999 284-288. Independent repositories actually fetched: konard/p-vs-np README blob 0e0ec77f and proofs/complexity/README 7ee9a11e (different one-tape machine); blkph0x/p-vs-np-proof-research README f397a774 and affine_projection.../THEOREM.md 4aba9d94 (different representation problem); MassimoLauria/cnfgen/cnfgen/families/tseitin.py 4bb5fd19; meelgroup/frat-xor/format.md 986a21aa (external grammar not R_mix341); berkeley-abc/abc README 88a9d1a3; openai/math README cc5b0a03 (unverified research corpus). No branded Google interface or native FLMV profiler used. No change to historical R_mix341 grammar/weights or other agents' research.

**Actual advance:** an offset-free postorder authenticated TREE schedule and restricted conditional 1/10-local-space composition. **Verification:** Python + independent JavaScript finite controls passed. **Exact remaining gap:** all-input recursively iterable transformation for *every* polynomial SAT A, including ordinary CNF and malformed inputs, on the same native model [P2-A2]; [P1-01], [P1-03], [P1-04], [P2-B2] OPEN. P versus NP OPEN.

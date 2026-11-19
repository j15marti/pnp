# LSPV-2 T5 one-hot source-aware circuit and genus obstruction (2026-11-18)

**Historical Route A. Status:** PROVED/EXACT restricted circuit factorization and structural theorem, COMPUTATIONAL independent replay, OPEN uniform witness hardness and P vs NP.

## Candidate and falsifiers
For each fixed edge-minimal UNSAT oriented H for T5, replace per-deletion source-exact Boolean selectors with one shared EXACTONE detector and a one-hot witness ROM. Falsifiers: incorrectly accepted foreign or multiple deletions; wrong witness on any retained arc; source bit omitted; large-girth SAT shortcut. Original source bytes were hashed and the old versus new witness tables compared exactly.

## Theorem A, actual-source one-hot factorization
Use q=n(n-1) complete ordered-adjacency bits x_(u,v). For all e in E(H), let z_e=NOT x_e, and B=NOT OR_(a notin E(H)) x_a. Let ONE(z) mean exactly one absent expected arc. Then

    valid = B AND ONE(z)
    output(v,bit) = valid AND OR_{e : bit(w_e(v))=1} z_e.

Compute ONE with a balanced binary dynamic program storing ZERO and ONE states: Z=Z_L AND Z_R and O=(O_L AND Z_R) OR (Z_L AND O_R). The circuit emits a complete 3n-bit coloring, verifies all actual retained source arcs, rejects every non-deletion source and zeros invalid outputs. Uniform source/witness acquisition may cost exponential time. This is a **nonuniform fixed-H** circuit existence theorem, not a uniform witness-production bound.

For full arbitrary-source recognition, all q adjacency bits are essential, so **valid alone** requires at least q-1 binary gates and depth ceil(log2 q) in any fan-in-two AND/OR/NOT circuit. This bound is solely on exact source-mask recognition; it does not apply to computation under a deletion-only promise or to unrestricted algorithmic witness costs.

## Executed, exact witnesses unchanged
- Source H33 SHA256 `0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac`. Same 44 witnesses. Witness circuit **1799 -> 1735** gates, depth **20 -> 15**; complete verifier **3203 -> 3139** gates, depth **36 -> 31**; 2003 independently replayed masks, 2 hostile mutations detected. Valid-only binary-gate lower bound 1055. New netlist SHA256 `04d31051463bfc68c409d4786862f245e0af768f1b1fb3e204eed17751007c8f`.
- Source H9 SHA256 `deb4de3a8180d066e3788b3b5a127560c3c6d7289dc9389583c20a10cc5e98c3`. Same 11 witnesses. Witness circuit **175 -> 164** gates, depth **12 -> 11**; full verifier **446 -> 435** gates, depth **26 -> 25**; 2176 independently replayed masks, 2 hostile mutations detected. Valid-only binary-gate lower bound 71. New netlist SHA256 `591bc4334f98e870e6abc1baf5b9eaaa89553dffd814157ae709cf3ad6f1d2ae`.
- The original and new output witnesses are byte-for-byte identical. The new CSE threshold also differs; improvements are credited to the **combined compiler**. The complete locally executed gate-level Python compiler, independent DAG replayer, source files, netlists and SHA manifest are in the user's dated conversation reproducibility ZIP.

## Theorem B, orientable genus barrier
For connected, edge-minimal UNSAT H, degree-two threads have L<=3. At each branching vertex v a thread forbids at most 4-L possible T5 colors, so summing the necessary >=5 excluded choices gives 2 sum_threads(4-L)>=5b. Therefore if K is the suppressed core with b vertices and e_c edges, original n<=3e_c-(3/2)b. When original undirected girth is g>=7, K is simple, min-degree>=3, and its undirected girth is at least k=ceil(g/3).

A planar H must have **g<=15**: otherwise k>=6 and Euler's planar e_c<=3(b-2)/2 contradicts e_c>=3b/2. For an orientable genus-h embedding, Euler yields 2(h-1)>=(1-2/k)e_c-b. For k>=7, the preceding local capacity inequality implies

    h >= 1 + (k-6)*n/(12*k), k=ceil(g/3).

Thus **g>=19 forces h>=1+n/84**, and any toroidal critical H has g<=18. High-girth intrinsic-critical families must have unbounded, indeed linear-in-n, orientable genus after g>=19. This is a structural restriction, **not a time/space lower bound**.

## Hostile structural control
The cubic Tutte-Coxeter core (30 vertices, 45 edges, girth 8) with every core edge replaced by an arbitrarily oriented length-three path has 120 vertices, 135 arcs, girth 24. Independent greedy branch coloring and completion of 90 internal vertices satisfied all 135 arcs. It is SAT, not intrinsically critical. It falsifies the premise that girth or branching alone makes witnesses difficult.

The nine short endpoint relations, all 512 subfamilies, and two original T5 source graph structures were independently rerun. H33 girth8 is nonplanar; H9 girth5 is planar.

## Literature firewall
Cranston et al., *Orientations of 10-Edge-Connected Planar Multigraphs and Applications* (2026), https://arxiv.org/abs/2603.24292, establish an oriented chromatic number <=5 for sufficiently large-girth planar graphs; that does **not** assert homomorphism to this particular fixed T5. Kun's fixed-girth CSP transfer and Kayll-Morris oriented-girth results likewise do not prove growing-girth intrinsic-critical witness-hardness.

**OPEN:** Uniform construction of a growing-girth intrinsically critical family with superpolynomial worst-case exact-witness cost after all shortcuts and all-machine quantifiers. P versus NP remains OPEN. No automation, ownership, peer manuscripts or root trackers modified.

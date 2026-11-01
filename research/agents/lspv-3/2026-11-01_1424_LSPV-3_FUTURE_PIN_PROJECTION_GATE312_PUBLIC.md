# LSPV-3 GATE312: Future-pin-safe SAT decision projection
**November 1, 2026, 14:24 PST. PROVED/EXACT elementary restricted continuation theorem; independently COMPUTATIONAL F9 falsifier; external mathematical referee pending. P versus NP OPEN.**

## Universal obstruction
The all-input adaptive source-authenticated controller may cache an exact Boolean boundary feasibility relation or even **integer model-count fibers**, then pin an interior original variable that was existentially forgotten. An exact present-time boundary summary need not be a congruence under that future ADD action. This is a decision-only question: no recovered assignment values, injective pin keys, or SAT-label oracle are presumed.

## Precise theorem (known cylinder-set semantics)
For a valid duplicate-free proper Döcker Monotone 3-SAT-(2,2) original F, coherent pins p,q on the same source-variable set H, and disjoint boundary B and future-pinnable S outside H, define
```
mu_p(b,s) = #{ a satisfies F, a extends p, a|B=b, a|S=s }
rho_p(b,s) = 1[mu_p(b,s)>0]
```
When every compatible partial pin continuation on B union S is allowed (including complete pins), p and q agree in SAT/UNSAT under **every** such continuation iff their entire Boolean support tables rho agree. They agree in exact #SAT under every continuation iff their integer fiber tables mu agree. Proof: a partial pin selects a cylinder of (b,s) cells; OR or sum of cells gives the query, while a complete pin isolates any cell. This is elementary existential projection and not a new general complexity theorem. It does not require storing that table: the solver may recompute by indexed rereads or use another equivalent representation.

## Same-canonical-original F9 counterexample, strictly stronger than label-only
The valid original has positive supports (156),(238),(135),(469),(247),(789) and negative supports (468),(167),(234),(358),(129),(579). It has nine variables, twelve distinct proper monotone clauses, exactly two occurrences per sign and variable, and 70 satisfying assignments. In one-based source names take:
```
p = {x1=1,x2=0,x3=0}
q = {x1=1,x2=1,x3=0}
boundary B = {x7}
future ADD r = {x6=1}
```
The complete **integer** boundary fibers agree: mu_p(x7=0,1)=(4,4)=mu_q(x7=0,1), and each current residual has exactly eight satisfying assignments. Yet #SAT(F9|p,r)=**0** and #SAT(F9|q,r)=**2**. No original clause is empty directly after either pin set.

The UNSAT side has an independent original-clause-indexed UP derivation: clause 2 forces x8=1, clause 8 forces x7=0, clause 5 forces x4=1, and clause 7 (¬x4∨¬x6∨¬x8) is false. The SAT side has two complete source-clause checked witnesses. The same source, boundary, legal future ADD, and both decision labels are preserved.

## Four falsifiers
F1: current SAT label is continuation-safe. FALSIFIED, already in GATE308/309. F2: exact integer **boundary-only** count fibers are future-interior-pin-safe. FALSIFIED by this F9 pair. F3: boundary-plus-future support is necessary/sufficient for **all complete pin contexts**. PROVED (known cylinder criterion). F4: a short table guarantees polynomial-time universal discovery. OPEN/NOT JUSTIFIED; even zero-interface exact label acquisition can encode the original decision.

## Fully charged conditional acquisition
For f free names and k=|B|+|S|, brute acquisition is O(2^f poly(N)), not a free oracle. Given a source-verified primal tree decomposition of width w, standard Boolean/weighted clause-CSP bag DP retaining B union S obtains the table in poly(N)2^{O(w+k)} paid work, with up to 2^k entries and f+1 counting bits per entry. Source scanning, decomposition discovery/verification, failed selector options, switching, proof/GE, cache/replay, child/output/guest DELAY-COPY-RECOMP and simultaneous live peak space remain charged. This is polynomial only on **acquired** bounded-(w+k) families, not all canonical originals.

For a general state R:
```
W_D(R) = C_grammar+source/read/index/head
       + sum_{attempted policies} C_discovery/select/switch/failed
       + C_GE/proof/project/cache/replay
       + sum_{children R'}(C_reencode/output/guest(R,R')+W_D(R'))
```
Delta may increase; logical XOR is OFFLINE only. No uniform all-input polynomial aggregate-work potential is established.

## Independent tests
No-import verifier: **6,518 assertions**. F9 70 original models; (p,q,p+r,q+r)=(8,8,0,2); 264 SS/SU/US/UU original-clause pair modes; 6,144 assignment/complement identities; all 19,683 coherent F9 partial cubes (10,508 SAT, 9,175 UNSAT); 32 failing original-source completions for p+r; no directly empty clause; six-ish malformed-input/grammar controls; Y6 root 20 models; connected valid 15-variable G1 opposite-label pinned controls (4,0). Independent UP-first DPLL on p,q,p+r,q+r used 2/2/1/1 recursive nodes and 107/95/44/76 literal tests. Offline binary versus Gray assignment XOR totals: 1013 versus 511; not native FLMV writes. U198/V198 are inherited controls, not freshly replayed this run.

## Primary literature, prior art and limitations
The proof is classical support projection, related to Darwiche-Marquis, *A Knowledge Compilation Map* (2002), DOI 10.1613/JAIR.989, and de Colnet-Szeider-Zhang, *Compilation and Fast Model Counting beyond CNF*, arXiv:2502.00434. Döcker's M22 NP-completeness (arXiv:1912.08032) and FLMV's 2005 SAT time-space bound (DOI 10.1145/1101821.1101822) were inspected. Project earlier ARC-CNF-CONTINUATION121 proved common-CNF quotient collision conditions and EXACT22-FOUR-FIBERS155 already isolated universal projection-acquisition hardness. GitHub searches covered j15marti/pnp and openai/math; no novelty inference from search absence.

**OPEN:** a uniform, polynomial-total-work all-input adaptive controller; universally hereditary power-short arbitrary-A -> Phi(A) ARC; strict same-machine numerical FLMV transfer; P=NP and P≠NP.

Reproduction: [compact source checker](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv3_312/compact312_public.py), [independent no-import checker](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv3_312/verify312_public.py), [summary](https://github.com/j15marti/pnp/blob/main/results/raw/arc/lspv3_312/summary312_public.json). Full raw 19,683-cube census, complete extrema, 264 source-pair modes, and 32 UNSAT leaves are in the run's reproducibility ZIP.

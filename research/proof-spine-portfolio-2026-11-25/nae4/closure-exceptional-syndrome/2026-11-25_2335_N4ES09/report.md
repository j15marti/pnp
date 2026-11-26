# N4ES09 — Exact NAE4 boundary projection requires auxiliary state

2026-11-25 Pacific 23:35 scheduled iteration. PROVED scoped representation barrier and exact compiler; independent review pending. P versus NP OPEN.

## Obligation and authentication
First OPEN arrow: arbitrary NAE4 -> uniformly acquired exact semantic normalization with a fixed polynomial aggregate bound. Test the specific proposed universal remedy from N4ES08: repeated independent-private resolution projection, retaining explicit CNF and unconditional affine equations over boundary coordinates only. Falsifiers: failure of source promises, incorrect diagonal support, affine equations bypass the bound, or compact auxiliary-free CNF contradicts the counting proof. Source is four supplied partitions of positive distinct triples, globally linear; DDD arXiv:2412.03395v3 Theorem 3.6, Theorem 3.11 inspected primary HTML https://arxiv.org/html/2412.03395v3. No additional planarity promise. No full hardness gadget replay. Read AGENTS, CODEX, nested skill, pinned 20:20 directive, issue #327 (621 comments), N4ES08, peer N4FN04 and RT39 originals. Older report history used as context; no full MFC-34–46 recovery or new K5 replay. No checkout/preflight, no formal checker. Repository search "NAE4 guarded parity CNF boundary projection auxiliary" returned no exact duplicate (not priority claim).

## A. Compiler (PROVED)
Use the N4FN04 nine-point affine-plane module with retained partitions P0=(678), P1=(036)(147)(258), P2=(048)(156)(237), P3=(057)(138)(246). Each pair in AG(2,3) appears once. Among nine Boolean values at least 16 same-color pairs occur; ten retained NAE triples contribute ten. The two missing triples must each contribute three, hence each monochromatic and their colors opposite (six same-color points force >=18 pairs). Conversely opposite constant rows and any NAE interior triple satisfy all ten. Thus ports 0,1,2 carry z, 3,4,5 carry 1+z.

Given arbitrary signed NAE3 formula F with three distinct variables per clause and designated boundary variable set B, for each variable v create d(v)+1 modules if v designated, d(v) otherwise (at least one). Connect consecutive modules via P0 owner (0_i,1_i,3_{i+1}); NAE forces equal phases. Assign each occurrence its own module and use port 2 for positive, port 4 for negative. Add one P0 triple per original signed owner. For each designated variable reserve port 2 of its extra module. All owner ports used at most once in P0; P1–3 cover everything; P0 also covers interiors. Internal repeated pairs are impossible since connectors use only a pair in a deleted row; cross-module pairs cannot repeat because all P0 owners are disjoint. Hence partial source positive, linear, missing only P0 slots.

Make three disjoint copies, fill each unused slot j with owner (j_0,j_1,j_2) in P0. All four perfect partitions now cover every variable exactly once; linearity holds because filler triples are disjoint and cross-copy. For every model of F, choose sheet phases x,x,1+x; choose each interior 001; all fillers satisfied. Conversely each sheet of any model projects to F by the module theorem. This gives a linear-module, deterministic source adapter preserving actual selected variables and SAT/UNSAT. Copies use no target witness in construction. DDD Lemma 3.7 uses a related three-copy completion for a different partition extension; here used only on missing slots, proof above.

Define raw region R by deleting ONLY the filler owners of designated boundary ports. Actual shared boundary is exactly the three copies of those ports; no other source owner is outside. For the diagonal substitution D(x)=(x,x,1+x) of boundary coordinates, D(x) extends to R iff x extends to F. Necessity follows by restricting sheet0; sufficiency by the same explicit witness lift, even to the full source. Not claiming arbitrary off-diagonal fibers factor independently.

## B. Guarded parity obstruction (PROVED)
For even k>=2 take boundary variables x_1..x_k,g,h, relation T: (g!=h) OR (XOR_i x_i=1). This is complement-invariant and has full affine hull. For each x, both guard patterns 01 and 10 are accepted. Differences span all x directions and guard difference 11. An odd word with guard00 supplies an independent guard direction. Hence no nontrivial affine equality holds universally.

Build a 3CNF with k-1 prefix XOR gates, each gate p=a XOR b encoded by four length-3 clauses excluding the incorrect triples. Last p and g,h satisfy (g OR h OR p) AND (NOT g OR NOT h OR p). Use a common reference r and fresh u for each clause (a OR b OR c), translating to NAE(a,b,u), NAE(NOT u,c,r). For r=0, exact OR relation by two-value inspection; for r=1 complement every physical variable to normalize r=0. The projected relation in original physical boundary values is unchanged because k even and T complement-invariant. All three literals have distinct variable IDs. O(k) clauses, variables, occurrences; compile via A, designated B=all k+2 variables. Genuine NAE4 with O(k) physical variables/owners, source encoding O(k log k) bits under ordinary explicit indices.

Any auxiliary-free CNF plus a conjunction of affine equalities on actual boundary exactly representing R must, after substituting D(x), represent T. All affine equalities become tautological because T has full affine hull. Set g=h=0; remaining CNF represents odd parity on k bits. Each non-tautological clause must mention every variable, since otherwise its falsifying subcube contains an odd assignment. Each such clause forbids just one even word. Therefore >=2^(k-1) clauses. This is superpolynomial in explicit encoded source length, irrespective of order of variable elimination, duplicate removal or clause subsumption, for an exact flat auxiliary-free boundary interface. Applies even if additional sound forced information is derived: it cannot change the exact relation. No unrestricted computational lower bound. For pure CNF with s existential auxiliary bits, same substitution and guard fixing gives Emdin et al. MFCS 2022 Thm 1.1: m >= Omega((s+1)/k * 2^(k/(s+1))), maximum width >= k/(s+1). For s=O(log k) still superpolynomial. This imported bound is for existential CNF encodings, NOT CNF+XOR with auxiliaries. Direct proof for s=0 above.

## C. Exact bypass and signed controls
On diagonal contexts, retain one named parity observable p=XOR x and two guard clauses. This is an exact O(k) mixed affine/Boolean interface WITH one auxiliary, not affine hull. Given boundary pins, calculate p, decide, reconstruct prefix values, each OR-gadget u, each module phase and interiors and all fillers. For arbitrary guards on internal variables this bypass may be invalid; preserve guard provenance or decline. On full raw region, exact linear-size existential compiler itself remains available; not an unrestricted fast join of its auxiliary states.

Unconditional single-bit pins on the SAT full source are vacuous by complement symmetry. Certified initial/after-deduction/stagnation closure on these constructed quotients: extract module equalities (constant-size template), then each two-NAE OR relation and XOR gate truth table; evaluate forced prefix once inputs pinned. Both forbidden diagonal and attainable diagonal guards on SAME R are handled by exact support. No claim of universal closure or target-free recovery of arbitrary hidden circuit from raw source; the constructive proof uses original compiler IDs. Genuine full-source SAT/UNSAT neighbors: add for each boundary variable a relative pin gadget NAE(l,r,u), NAE(l,r,NOT u), which forces l!=r, with l chosen for prescribed relative value; fresh u. All g,h,x relative zero is UNSAT; flip only x1 requested relative value and the resulting source is SAT. The two gadgets differ in literal polarity, hence compiled port assignments change; source sizes equal. Full reverse proof through module and local truth tables, not exhaustive search. Exact pin/gate propagation resolves these controls, so they are NOT hard postclosure examples.

## D. Executed audit
Self-contained JS, no solver dependency. Exhaustive 512 module words; truth tables for OR, XOR, relative pin. Every source authenticated by full partitions and pair uniqueness; actual lifts checked against all original owners, including full-source SAT neighbors. All diagonal boundary words tested k<=8; deterministic sample of 64 words each k=16,32,64,128. UNSAT proofs via exact symbolic reverse and pinned parity, not full physical brute force. Results:
```json
{
  "checks": 23260740,
  "localModels": 12,
  "results": [
    {
      "k": 2,
      "variables": 1080,
      "owners": 1440,
      "boundary": 12,
      "testedWords": 16,
      "yes": 12,
      "no": 4,
      "neighborVariables": 1728,
      "neighborOwners": 2304
    },
    {
      "k": 4,
      "variables": 2430,
      "owners": 3240,
      "boundary": 18,
      "testedWords": 64,
      "yes": 48,
      "no": 16,
      "neighborVariables": 3402,
      "neighborOwners": 4536
    },
    {
      "k": 6,
      "variables": 3780,
      "owners": 5040,
      "boundary": 24,
      "testedWords": 256,
      "yes": 192,
      "no": 64,
      "neighborVariables": 5076,
      "neighborOwners": 6768
    },
    {
      "k": 8,
      "variables": 5130,
      "owners": 6840,
      "boundary": 30,
      "testedWords": 1024,
      "yes": 768,
      "no": 256,
      "neighborVariables": 6750,
      "neighborOwners": 9000
    },
    {
      "k": 16,
      "variables": 10530,
      "owners": 14040,
      "boundary": 54,
      "testedWords": 64,
      "yes": 49,
      "no": 15,
      "neighborVariables": 13446,
      "neighborOwners": 17928
    },
    {
      "k": 32,
      "variables": 21330,
      "owners": 28440,
      "boundary": 102,
      "testedWords": 64,
      "yes": 46,
      "no": 18,
      "neighborVariables": 26838,
      "neighborOwners": 35784
    },
    {
      "k": 64,
      "variables": 42930,
      "owners": 57240,
      "boundary": 198,
      "testedWords": 64,
      "yes": 48,
      "no": 16,
      "neighborVariables": 53622,
      "neighborOwners": 71496
    },
    {
      "k": 128,
      "variables": 86130,
      "owners": 114840,
      "boundary": 390,
      "testedWords": 64,
      "yes": 51,
      "no": 13,
      "neighborVariables": 107190,
      "neighborOwners": 142920
    }
  ],
  "scope": "exhaustive diagonal words k<=8; deterministic sampled words above; forward source witness validation; symbolic reverse via module/OR/XOR/pin truth tables, not exhaustive full source or general solver"
}
```
No general solver, arbitrary off-diagonal support table or generic template discovery executed. Historical K5/Fano and RT39 two-child barrier unchanged; no new lower bound inferred. Independent review pending.

## E. Resource ledger and next gate
For admitted compiled diagram with provenance, parsing/authentication and sorting pairs, creating original IDs, module and gate checks, diagonal guard decisions and full witness lift cost polynomial in encoded N; O(k) nodes/owners and O(k log k) index bits. Failed checks included, no branches or semantic oracle. Constant local truth-table work; arithmetic GF2, ordinary ID sorting and scans. Peak storage polynomial, cumulative <=(T+1)S on same serial machine. No embedding required. For explicit auxiliary-free normalization output length alone exceeds every fixed polynomial; this is restricted representation barrier only. DISJ scoped PASS; DTISP and configuration scoped; relativization/algebrization/Natural Proofs N/A to scoped construction, unrestricted OPEN. Next gate: acquire compact guarded affine/nonaffine interfaces on arbitrary source and prove controlled joint auxiliary-state elimination, not merely introduction of auxiliary names. N4FN04 already proves arbitrary module quotient can reproduce original NAE4; combine this with the new obstruction on exact interface language. Do not replace the missing join by a SAT oracle. A verified source-to-source adapter for signed NAE3 is supplied; cross-source claims require their own adapter.

## References and fresh search
DDD primary HTML above (Thm 3.6,3.11, Lemma 3.7 related completion). Emdin, Kulikov, Mihajlin, Slezkin, CNF Encodings of Parity, MFCS 2022, https://doi.org/10.4230/LIPIcs.MFCS.2022.47, https://arxiv.org/abs/2203.01082 (Thm 1.1 and proof read). N4FN04 original https://github.com/j15marti/pnp/blob/68c65a139a5088cb0cb1413246a209c1bcf742c5/research/proof-spine-portfolio-2026-11-25/nae4/four-partition-nae/2026-11-25_2317_N4FN04/report.md. Fresh web searches for Davis–Putnam resolution elimination, parity CNF, official google/or-tools (presolve examples, not a proof), anthropics/formal-math (counted formal theorem work), openai/miniF2F (benchmark), google-deepmind/miniF2F (fork explicitly not official product); no relevant xAI official solver/proof result surfaced. No external code imported. No schedule changes or public proof claim.

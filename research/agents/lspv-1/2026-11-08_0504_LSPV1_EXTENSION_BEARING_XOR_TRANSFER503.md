# LSPV-1/503 | Extension-bearing global GF(2) transfer with paid case reconvergence

**2026-11-08 05:04 PST | Route B | PROVED/RESTRICTED symbolic macro, COMPUTATIONAL controls, Pang asymptotic application CONDITIONAL on preprint | P versus NP OPEN.**

**Node IDs:** [P2-L1-503] (new scoped evidence); depends on [P2-L1-502], relevant [P2-L5-433]. The load-bearing [P2-D1], [P2-C3], [P2-B1], [P2-B2] all remain OPEN; companion [P1-01], [P1-03], [P1-04] unchanged.

## IDEA -> SEARCH -> ITERATE and prespecified falsifiers

Hypothesis: the global GF(2) addition of **affine equations containing paid, shared, nested extension variables** can be converted to source-only syntactic Res(PC_1/F_2) with O((b+1)2^b) paid inference nodes, provided b charges the **union of complete original-variable ancestors of extension variables in both premises**, even if a wire cancels in the conclusion. This is a distinct calculus extending LSPV-1/502, not an alteration to historical R_mix341.

Falsifiers set before search: **F1** cancelled extension gates introduce an uncharged ancestor; **F2** substituting original variables into an affine row needs non-native semantic inference; **F3** omitted complementary branches yield a spurious output; **F4** the target lacks syntactic Boolean axioms, linear combination, contraction, weakening or false-constant deletion.

SEARCH: Both complete root trackers were read: `proof1.txt` SHA `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 chars) and `proof2.txt` SHA `9094495c3fdf031a3d6a44738cc97bfdd6fd9595` (403,806 chars) at research preflight. Read current coordination issue #3 and latest LSPV-5/433 comment, the governing five-role handoff, LSPV-1/502 report, AGENTS.md, CODEX.md, and repo pnp-research skill. Peer LSPV-5/433 composes contextual branching/extension-bearing Resolution in a distinct calculus, but does not handle extension-bearing global XOR. Examined Grok `GROKPROOF/2026-11-08_0320_PROGRESS.md` SHA `72edb3140d8ed798d0905a827f85d3428728e396`, Claude `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex` SHA `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`, and files `konard/p-vs-np/scripts/proof_status.json` SHA `93b77ed3d8fe456f81c690035f45f07910a247f2`, `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` SHA `18d693ea71dfa433370eb7afbebc3106e32f03e5`, `meelgroup/frat-xor/format.md` SHA `986a21aa92b62f844ef1fce852193142c41b2b1f`, `openai/math/README.md` SHA `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`. The latter material is background/control, not historical proof-system authority. Public web search located Pang arXiv:2610.00837v2, §1 (native syntax), Fact 7.1 (bounded-variable syntactic derivations), and Theorem 7.2(a); no separately branded Google client or historical checker was run.

ITERATE: Directly discarding guards fails when an auxiliary wire cancels but an original variable from its cone still occurs in the output affine row. Repair: specialize both parents on the combined ancestor cone using paid Boolean axioms, combine affine rows syntactically, then **restore and discharge both complementary cases** for every variable that no longer belongs to the conclusion's extension cone. Five edge fixtures and 4,096 exhaustive pair tests verified the repair. This is not a solution of historical R_mix341.

## New theorem (scoped syntactic macro)

Let F be a fixed binary-encoded CNF over original variables X, with an acyclic collection of globally fresh, paid, conservative Boolean gate definitions Z, complete defining facets and source authentication. A GF(2) row is

$$
E: \quad \alpha\cdot X \oplus \beta\cdot Z=c.
$$

Let S(E) be the full transitive original-variable ancestor union of every auxiliary with nonzero coefficient. For each a in {0,1}^{S(E)}, unfold the gates, evaluate original variables in S(E), and obtain a source-only affine equation L_E(X\\S(E))=h_E(a). Let D_a denote the ordinary clause falsified precisely by a. Translate E into the family

$$
\mathcal T(E)=\{D_a\vee (L_E=h_E(a)):\ a\in\{0,1\}^{S(E)}\}.
$$

The conjunction of these lines is equivalent to E after uniquely extending every original assignment by the conservative definitions. The original clauses of F remain the sole input-source axioms. All target output variables are original.

**Claim:** For every legal binary extension-bearing global XOR step E_1,E_2 -> E_3=E_1 XOR E_2, put V=S(E_1) union S(E_2), b=|V|. There is an explicit syntactic derivation of the whole family T(E_3) from T(E_1) and T(E_2) using O((b+1)2^b) target nodes in Pang's **syntactic** Res(PC_1/F_2). This holds for globally shared and nested gates, arbitrary original-only affine guards and cancellations.

**Proof:** For each full a on V, specialize each parent row outside its own support. Use the Boolean axiom (x=0) OR (x=1), plus two-premise linear combination, to replace x by the chosen bit whenever x occurs in an affine row; otherwise use paid weakening. The result for each parent has exclusion guard D_a and an affine equation on X\\V. Apply the native linear-combination rule to these two guarded equations, then pay contractions of duplicate guards. This derives the substituted XOR result under D_a. For each x in V\\S(E_3), **both** x=0 and x=1 results exist. If x does not appear in the remaining affine output, resolve the two guards and delete the resulting false constant. If it still appears as an original variable, combine each case with its matching Boolean axiom to restore the coefficient of x, then resolve the complementary guards, delete the false constant, and contract duplicates. Repeat until the exact target line for each assignment to S(E_3) remains. All steps are syntactic and acyclic; references to already derived target nodes are shared. There are 2^b leaves and O(b2^b) paid steps. TRUE and FALSE constant equations use respectively the target Boolean axiom and paid false deletion as needed. No semantic implication oracle, assumption leakage or uncharged case rule is used.

Together with the already *scoped* LSPV-1/502 simulations for original-only Resolution/GF(2), shared gate definitions, arbitrary extension-bearing ordinary Resolution and locally checked conversions, this constructs a **distinct** fixed calculus R_wire+RES+extXOR with

$$
S_{\mathrm{Res}(\mathrm{PC}_1/\mathbb F_2)}(F)
\le C(m+n+q(\pi)+1)(b(\pi)+1)2^{b(\pi)}.
$$

Here b(pi) charges the maximum union of original ancestors across the *premises* of each extension-bearing XOR/Resolution/LOCAL step, including disappeared pivots. The new theorem is **not** an authenticated native R_mix341 certificate. An actual full checker-accepted construction remains OPEN.

## Established hard family and remaining transfer

Pang's `F(n,3,8n)` consists of 8n independently sampled proper signed 3-clauses uniformly from `8 binom(n,3)`, permitting repeated clause draws. Its explicit ordinary binary encoding uses N=Theta(n log n) bits. Pang arXiv:2610.00837v2 (24 Oct 2026), Theorem 7.2(a), reports high-probability exp(Omega(n)) DAG proof-size hardness in the **distinct** syntactic Res(PC_1/F_2). The exact same original F is used here. Under that preprint theorem,

$$
\log(q+m+n+1)+b\ln 2+\log(b+1)\ge \kappa n-O(1).
$$

Therefore a polynomial-node refutation in the **new restricted calculus** must have an inference with b=Omega(n), and b=o(n) forces q=exp(Omega(n)). These are proof-size/source-support tradeoffs, *not* computational lower bounds. Large-cone short proofs remain possible, so no historical all-rule lower bound [P2-B1] follows. Nor does SAT in P -> same-calculus polynomial refutations [P2-B2] follow. Haken ordinary Resolution, Cook extended Resolution, and odd Tseitin GF(2) remain mandatory legal shortcut controls.

## Finite reproducibility, search and resource ledger

A separately executed independent Python **paid syntactic DAG** checker covered five targeted cases, including cancelled wire z=x AND y, w=y XOR t, and the nested shared r=z AND t: **185 target nodes** (including explicit paid contractions), **5 corrupted non-axiom steps rejected**, all 32 original assignments per fixture checked. Exhaustive independent row-sweep: all 64 rows over original x,y,t, auxiliary subsets of {z,w}, and both constants, tested in all **4,096 ordered input pairs**; **181,776 syntactic nodes rechecked** and **393,216** semantic projection comparisons, all passed. Basic SAT/UNSAT sources (x) and (x),(NOT x) checked. Standalone Python source and exact raw output are preserved in the run artifacts; the published independent JS file checks the same 4,096 ordered pairs and 393,216 equivalences, plus five malformed controls. Neither program is the historical checker and neither independently reproves Pang's asymptotic lower bound.

Ideal minimum work is distinct paid nodes in a source-authenticated shared DAG, optimized with free best-derivation selection. Actual proof construction must charge input parsing, source/index/head reads, gate dependency expansion, 2^b assignments, conversion, line and reference encoding, verification, failed policies/restarts, retention/recomputation, output and full simultaneous peak space. Conservative explicit producer upper bounds are O((m+n+q)(b+1)2^b poly(n+q)) in time and output bits. The weighted critical-path depth and time-space recomputation schedule were not independently optimized. The ideal translation is not an all-input SAT algorithm and does not imply FLMV contraction.

## Publication guard and handoff

Root `main.tex` returned blob `68188a24badda635a5983fda1c381cdb694fd497` but zero content bytes even for a line-bounded read. It was **not** modified. The historical grammar/weights, five existing roles/IDs/titles/schedules/enabled states and the two Route A/three Route B allocation are unchanged. Full historical proof-system authentication [P2-D1], unrestricted mixed-rule transfer [P2-C3], all-rule superpolynomial minimum [P2-B1], noncircular B3 [P2-B2], and P versus NP remain OPEN.

**Next exact target:** inspect real historical extension-bearing GF(2) and AND3/LOCAL-CONVERT production and acceptance rules, and either replay an authenticated typed witness or find a legal counterexample to this translation. Composition with LSPV-5/433's context AND obligations is promising but distinct and NOT yet declared historical.


## Post-publication tracker/readback reconciliation (2026-11-08 PST)

Both **complete** trackers were read again from current `main`. `proof1.txt` remained unchanged at blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 characters). The material [P2-L1-503] scope and dependencies were appended to `proof2.txt` using current complete content and SHA `9094495c3fdf031a3d6a44738cc97bfdd6fd9595`. Update commit `5bea73c6ee3da6efb683d066f5793668b446b8cb`, new blob `3fd90ed88dc48c19976af2c0b0c376a1752553a8` (406,698 characters). Full readback was byte-exact, and the entire prior tracker content was verified to be an unchanged prefix. Issue [#3](https://github.com/j15marti/pnp/issues/3#issuecomment-6722049720) received the affected node ID and full caveats; comment body readback was exact. Report, independent JS audit, raw and handoff were all fetched and read back; the GitHub JS was independently replayed in V8 and passed. Root `main.tex` had zero readable content bytes and was intentionally untouched. No other agent-owned files or scheduler settings were edited. **P versus NP OPEN.**

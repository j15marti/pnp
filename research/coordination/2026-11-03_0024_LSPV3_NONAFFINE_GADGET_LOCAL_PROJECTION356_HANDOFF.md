# LSPV-3 NONAFFINE-GADGET-LOCAL-PROJECTION356 | November 3, 2026, 00:24 PST

**PROVED/EXACT local projection and source essentiality; COMPUTATIONAL independent controls; conditional R+ attack; Rmix341 global upper and B3 OPEN.** No task identity, schedule, enabled state, ownership, fixed rules or other governance changed.

## New load-bearing partial result

Start with connected cubic odd-charge Tseitin, substitute a surjective gadget g independently on every edge, and encode each vertex constraint canonically as general CNF on its gadget inputs. With conservative paid two-input gate definitions, each vertex's four parity clauses over fresh gate-output variables are derivable by **ordinary binary Resolution alone**. Complete Davis-Putnam variable elimination generates at most `3^M` different local non-tautological clauses on the M local input/gate/output variables. If g has O(k) Boolean gates and k=O(log h), this is polynomial in the number h of graph vertices. This theorem only compiles **local interfaces**, not the global UNSAT derivation.

For 2-vertex-connected cubic graphs every original lifted source clause is indispensable and every single sign flip makes SAT; the unchanged at-most-binary-premise Rmix341 has the universal calibration bound **W_R >= m-1**. For AND2 with one charge-one vertex, original variables n=3h, source clauses m=28h+8, encoded source bits N=Theta(h log h), hence **W_Rmix341 >= 28h+7**. This remains a *linear* bound, not a superpolynomial lower bound.

## Specific mixed rule obstruction (must not be silently repaired)

The unchanged Rmix341 **AND3 precondition says support of at most three original variables**. The local compiler extracts parity clauses on three *fresh VARDEF output variables* z_e, each depending on two original input variables, not a three-original-variable factor. It is therefore **NOT YET VERIFIED** that adding three AND3 steps at each vertex is legal. A strengthened system R+ that explicitly permits AND3 on the three new outputs has an exhibited proof using **(171h/2)+7** paid nodes for the fixed AND2 templates. This is **not** asserted as an upper bound for the preselected Rmix341. This distinction is the substantive new falsification target for SAT-Circuit Builder / Red Team.

## Independent finite data, source and evidence accounting

Python builds explicit source-indexed local Resolution nodes and checks pivots, terminal affine parity clauses, gate truth tables, 120 K4 original-clause deletions, 720 occurrence-sign-flip neighbors, all 4,096 K4 input assignments, even-charge controls, and corrupt RES rejection. Independently written standalone Node referee regenerates six fixtures with local RES counts **328/320, 488/480, 648/640** (odd/even K4, prism3, prism4); original source clauses **120/112, 176/168, 232/224**, respectively, and confirms 847 classified controls. The fixed local counts are 88 RES at the sole charge-one vertex and 80 at each zero-charge vertex. Conditional R+ totals are 349, 341, 520, 512, 691, 683. ASCII DIMACS source bits are 17,960; 17,064; 28,584; 27,560; 39,080; 38,056. Compact proof-JSON sizes for odd fixtures are 34,866, 52,540 and 70,076 bytes. **These are not minimum proof encodings or arbitrary-machine time/space bounds.**

## Literature and duplication

Read first the November 2 12:04 five-role directive, current issue #3, AGENTS.md, CODEX.md, pnp-research skill, LSPV-2 MIXED-TSEITIN341, LSPV-3 FEEDBACK-CYCLE355, LSPV-4 SOURCE-CYCLE-SLACK353 and newest LSPV-5 PHP32 exact referee307. Queried recent primary literature on lifted Tseitin, ResLin and Extended Frege proof analysis, with relevant GitHub/OpenAI discovery. Bhattacharya--Chattopadhyay ECCC TR25-106 (rev Dec 6 2025) gives depth-restricted Res(\oplus) lower bounds, not the mixed extended calculus; Arteche et al arXiv:2506.16956v2 (May 19 2026) treats proof analysis, not a completed local-to-global Rmix translation. The unlifted short affine Rmix proof and source-fan-in lower bound were previously known in the project; only the *nonaffine-lift local extraction and rule gap* is incremental. Independent originality review remains pending.

## Readback-verified outbox

- [Full formal report](../agents/lspv-3/2026-11-03_0024_LSPV-3_NONAFFINE_GADGET_LOCAL_PROJECTION356.tex)
- [Independent no-import Node.js reproducer](../../experiments/arc/lspv3_356_gadget_lift_independent.js)
- [Machine-readable six-fixture raw results](../../results/raw/arc/2026-11-03_0024_LSPV3_NONAFFINE_GADGET_LOCAL_PROJECTION356.json)
- Local conversation reproducibility ZIP includes complete Python RES DAG producer, K4 odd full certificate, independent Node checker and raw ledgers.

**Next exact obligation:** Builder and Red Team should check whether the original, preselected AND3/LOCAL-CONVERT grammar can legally normalize parity clauses over fresh DEF outputs without relabelling the rules. If so, record every conversion step and prove a polynomial full-Rmix bound for this **family**; if not, seek a truly rule-invariant lower potential. Independently B3 and unrestricted P vs NP remain OPEN. Full proof search, all-phase rho and time-space transfer still require separate accounting.

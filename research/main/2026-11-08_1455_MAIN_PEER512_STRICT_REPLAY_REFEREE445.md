# LSPV-5/445 | Independent strict replay of LSPV-3/512

**2026-11-08 14:55 PST, America/Los_Angeles | Route B red team | COMPUTATIONAL independent declared-semantic replay + PROVED/RESTRICTED evidence-scope refinement | P versus NP OPEN**

**Proof-chain IDs:** new `[P2-L5-445]`, refining `[P2-L3-512]` and the evidence boundary under `[P2-D1]` and `[P2-C3]`. `[P2-B1]`, `[P2-B2]`, `[P2-A2]`, `[P2-A5]`, `[P1-01]`, `[P1-03]`, and `[P1-04]` remain OPEN. Historical `R_mix341` grammar and weights are unchanged.

## IDEA before search

Hypothesis: a polynomial SAT decider's rejecting computation does not by itself yield a short refutation in the same fixed `R_mix341`; a system-specific, original-source-authenticated reflection/source-retraction theorem is still required.

Falsifiers fixed in advance:

1. the historical grammar natively accepts authenticated computation-trace steps;
2. a peer supplies accepted historical bytes deriving false from the original CNF for arbitrary decider runs;
3. a theorem gives a polynomial same-calculus retraction into historical `R_mix341`;
4. a uniform B3 proof avoids both short reflection and short certificates.

Exact target prefix: for one fixed historical calculus $R$, challenge any proposed implication
$$
\exists A\;[A\text{ is a uniform total polynomial SAT decider}]
\Longrightarrow
\exists p\;\forall F\in\mathrm{UNSAT},\;W_R(F)\le p(|F|).
$$
The same-realization target is the original source bytes plus the exact accepted historical proof bytes. A separately declared semantic trace is a control, not that object.

## SEARCH and continuity

Fresh complete reads used `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and then-current `proof2.txt` blob `8e8f04e7f4aa7b5ef11b2d92f3548ce504198e1c`; issue #3 through the newest LSPV-4/503 comment; the governing 2026-11-02 five-role handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`; `AGENTS.md`; `CODEX.md`; `.codex/skills/pnp-research/SKILL.md` and its red-team/protocol references; original `/341`; LSPV-1/516; LSPV-3/512; LSPV-4/503; Grok `GROKPROOF/2026-11-06_2316_PROGRESS.md`; and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`. The local preflight was actually run but correctly failed because this scratch directory is not a repository checkout and lacks root `main.tex`, `AGENTS.md`, `CODEX.md`, and the local skill file; those authoritative files were instead read from GitHub. This limitation is not disguised as a passing preflight.

Required change-aware repository reads:

- `konard/p-vs-np` head `ecedd2b45f1c524d85c00b2da27a9c140025550c`, `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`, unchanged from the prior pin; finite-model theorem/status index, no historical mixed-calculus bridge.
- `blkph0x/p-vs-np-proof-research` head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` and `REVIEW_ADDENDUM.md` blob `6a7cc2f8962d3fcfcfc1778b1d3d8f5dc8d56d70`, unchanged; scoped relaxation/rank barriers, not B3.
- `meelgroup/frat-xor` head `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, `format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; a different explicit CNF/XOR elaboration format.
- `tanyongkiam/cake_lpr` head `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`, `README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; verified checker/toolchain evidence, not proof-size transfer.
- `peitl/short-proof` head `2c524cfceecf68b56f51d23f6b63255b502856d3`, `README.md` blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab`; finite shortest Resolution/Q-resolution tooling only.
- `MassimoLauria/cnfgen` head `24e633bdbed0d0998493bee99c42faf480c7dc96`, exact Tseitin generator `cnfgen/families/tseitin.py` blob `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab`; family generator, not lower-bound certificate.
- `openai/math` head `4eaee87548250b2682affda7d05d947c05554bae`, `README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`; mixed research status, no `R_mix341` checker.
- `anthropics/formal-math` head `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`, `README.md` blob `1df53bfc14a022088d1b5757698f692bf79390b4`; project-level Lean artifacts, no same-calculus bridge.

Actual repository queries included `LSPV-4/503`, `completeness effectivity do not imply B3`, `polynomially bounded proof system same fixed calculus`, `Grok R_mix341`, `Claude R_mix341`, and `Tseitin formula generator`. General indexed web search was used; no separate Google-branded interface was available. Primary statements checked were Cook--Reckhow (JSL 1979, Proposition 1.4/1.6), Haken (TCS 1985), Urquhart (JACM 1987), Ben-Sasson--Wigderson (JACM 2001), Cook's 1976 ER PHP shortcut, and Krajicek (IPL 2012). Cook--Reckhow proves existence of *some* polynomially bounded system iff NP=coNP and preservation under p-simulation; it does not make every preselected system polynomially bounded. Krajicek's algorithm class explicitly requires polynomial proofs of the algorithm's soundness. Haken/Urquhart/Ben-Sasson--Wigderson are restricted Resolution controls; Cook ER and native affine/Tseitin elimination are shortcut controls.

## ITERATE: exact peer object and independent verifier

The audited peer artifacts are:

- report `research/agents/lspv-3/2026-11-08_1429_LSPV3_THREE_ARM_UNIQUE_CORE_LOCAL_RES_PORT512.md`, blob `9dddd8c343ffe5d086fc6a5128ca4931969fcc4d`;
- compact producer `experiments/arc/lspv3_512_three_arm_port.py`, blob `f0236cae5b337e0773e70c6335ea02b00d82d4c5`;
- peer raw summary `results/raw/arc/2026-11-08_1429_LSPV3_512_THREE_ARM_RAW.json`, blob `c8893495855c05adc6af35599f7fbec5d04f1e14`;
- handoff `research/coordination/2026-11-08_1429_LSPV3_THREE_ARM_PORT512_FIVE_ROLE_HANDOFF.md`, blob `ca6ba18c45e858f98dd5512732aa4e30cb46a537`.

The producer emits a 10,156-byte packet for a 16-vertex cubic three-arm odd Tseitin graph: 24 original edge variables, 64 strict signed 3-clauses and source SHA-256 `dc62a4995250bb6922d31e711562fa7408e67968e097289fe8a5cb8c9c55dc20`. The packet declares `Rmix341-DECLARED-SEMANTIC-SUBLANGUAGE; NOT HISTORICAL BYTE CHECKER` and contains 57 sequential paid nodes: 42 `AND3`, 9 `XOR`, 3 `LOCAL`, and 3 oriented `RES`; root `N56`; weighted depth 9.

I wrote a separate closed-schema verifier, blob `67c9daa98f2d20d9c07dcf37b1a0b568be090734`. It does not import the peer producer. It checks canonical DIMACS bytes and SHA, reconstructs the cubic graph and charges, regenerates every source clause in canonical order, enforces acyclic sequential IDs and exact arities, evaluates every `AND3` truth table on at most three original variables, authenticates exact affine rows before `XOR`, checks every `LOCAL` semantic implication, checks correctly oriented exact Resolution, requires the authenticated empty root, recomputes the distinct-node ledger, traverses source ancestry, and independently solves all 64 single-clause deletions by GF(2).

Baseline result: PASS with paid work 57, depth 9, 55 used source clauses, and exactly the same 55 independently recomputed indispensable source clauses. This independently corroborates the declared-semantic construction and its source-use count. It is not execution of an authoritative historical checker and is not a proof that 57 is the full mixed minimum.

Fifteen targeted mutations all rejected:

| Class | Rejected mutation |
|---|---|
| Source/authentication | same-hash byte edit, re-encoded and rehashed noncanonical source, false SHA |
| Grammar/schema | false calculus tag, unknown top-level field, duplicate node ID, forward parent, missing source |
| Algebra/local | flipped row RHS, XOR from non-row source, false LOCAL literal |
| Resolution/root/cost | wrong pivot, wrong resolvent, wrong root, false paid ledger |

The initial verifier version accepted a whitespace-reencoded source after recomputing its hash. Because `/512` calls the source canonical ASCII, I tightened the checker to exact canonical bytes; the final `source_reencoded_rehashed` control rejects. This is a verifier repair, not a change to the calculus.

## Family/theorem/encoding/known-method ledger

| Family | Exact encoding and parameter | Established theorem/model | Known shortcut/control | Remaining transfer |
|---|---|---|---|---|
| Cubic expander odd Tseitin | one edge variable per edge; at degree 3, four forbidden-parity strict 3-clauses per vertex; $h$ vertices, $3h/2$ variables, $4h$ clauses | Urquhart/Ben-Sasson--Wigderson: exponential ordinary shared-DAG Resolution size on appropriate expanders; restricted proof system | Gaussian elimination/native GF(2) gives linear row cancellation in the declared mixed core | lower bound against every legal historical mixed rule remains OPEN |
| Three-arm bridge-star `/512` | $h=16$, 24 variables, 64 canonical strict 3-clauses; 55 unique essential source clauses | exact finite minimal-UNSAT source result plus independently replayed 57-node declared-semantic derivation | paid `LOCAL` bridge units and oriented `RES` hub refutation; source floor 54, construction 57 | historical accepted bytes, exact full-mixed optimum, asymptotic hard family and B3 remain OPEN |
| Haken PHP | standard pigeonhole CNF; Haken ordinary Resolution lower bound | exponential ordinary Resolution only | Cook extended Resolution has polynomial proofs | no transfer to all mixed rules or all algorithms |

Certified UNSAT, certified restricted proof-size hardness and empirical/finite checker difficulty remain distinct. No equisatisfiable reduction is used to transport a lower bound here.

## Shared-DAG, branching and resource audit

The `/512` packet is an acyclic shared DAG without case-split/discharge nodes. Each multi-premise inference is an AND obligation; the union contains 57 distinct paid nodes and is charged once. Its weighted critical path is 9, distinct-node work is 57, and the explicit packet is 10,156 bytes. No branch-local lemma, assumption discharge, weakening or cross-context reuse is present. Hence this run tests sharing and reconvergence semantics but does not authorize a branching rule in historical `R_mix341`.

Measured replay: 0.0156 seconds and 11,648 KiB maximum RSS in the recorded run. Separate charged phases were: peer packet construction; 10,156-byte output; JSON parse; canonical source/index regeneration; 57-node verification; 64 GF(2) deletion solves; 15 mutation replays; result serialization; GitHub reads/writes/readback. Discovery/search time is not part of $W_R$ but is part of this implemented audit. The verifier retains the packet, source factors and mutation copy, so its measured peak is not a logarithmic-space proof schedule. No parallel physical schedule is claimed from depth 9.

## Duplication, contradiction and status audit

The general same-calculus B3 firewall is already present in REFEREE356 and LSPV-1/385: completeness/effectivity or existence of another polynomially bounded system does not imply B3 for an arbitrary fixed calculus. It is adopted, not claimed new. `/512` itself explicitly denies historical-byte and B3 scope, so it does not trigger any initial falsifier. The new evidence is narrower: the compact committed producer suffices to reconstruct and independently verify its declared semantics, but the peer report's claimed two full independent checkers and complete certificate were not themselves committed. The generated packet blob `62d008c49ada54773e2a520e6b4efe9a8692383a` (SHA-256 `7b26cb9480b91b9e2a2eb35c7948a75225e486c34be54a907540f39d0a21c969`) and this verifier close that reproducibility gap for the declared packet only.

**What changed relative to root `main.tex`:** add a bounded LSPV-5 referee record that independently corroborates `/512`'s declared 57-node trace and records the missing-published-checker distinction. No executive status, historical grammar, theorem scope, role, schedule, title, enabled state or allocation changes. No stale stronger claim was found in the audited `/512` report.

**Status:** COMPUTATIONAL independent replay; PROVED/RESTRICTED evidence-scope refinement. `[P2-D1]`, `[P2-C3]`, `[P2-B1]` and `[P2-B2]` remain OPEN. P versus NP remains OPEN.

## Artifacts and next target

- verifier: `experiments/review/lspv5_445_peer512_strict_replay.py`, blob `67c9daa98f2d20d9c07dcf37b1a0b568be090734`;
- raw result: `experiments/review/raw/2026-11-08_1455_LSPV5_445_PEER512_STRICT_REPLAY_RAW.json`, blob `6f94062c8a3f47b75a712436483c71e21a1f0dd2`;
- generated exact packet: `experiments/review/raw/2026-11-08_1455_LSPV5_445_PEER512_PACKET.json`, blob `62d008c49ada54773e2a520e6b4efe9a8692383a`.

Next target: replay a genuinely historical accepted-byte `LOCAL`/`RES` certificate bound to original source bytes, or produce a minimal byte-level counterexample showing why the declared `/512` semantics cannot be realized in the frozen grammar. Separately, B3 still needs a noncircular system-specific short reflection/p-simulation theorem.

<!-- END_OF_VERIFIED_REPORT::LSPV-5::PEER512-STRICT-REPLAY-REFEREE445 -->

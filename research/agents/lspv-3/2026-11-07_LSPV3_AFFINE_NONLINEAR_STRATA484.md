# LSPV-3/484: Nonlinear-gate affine stratification and a precise missing proof-transfer hypothesis

**2026-11-07 PST | Route B | KNOWN general technique / independently proved specialization | COMPUTATIONAL verification | P vs NP OPEN.**

**Tracker IDs:** [P2-L3-483], [P2-F12], [P2-C3], [P2-D1], [P2-B1], [P2-B2]. The theorem below is about a separately declared conservative binary-gate circuit, NOT an authenticated historical R_mix341 refutation. No weight, rule, or agent allocation changed.

## IDEA and falsifiers (fixed before search)

Hypothesis: the coordinate-pinning factor `2^s` in the *conditional* LSPV-1/483 mixed-to-Res(XOR) compiler can often be replaced by an affine guard tree having at most `2^nu` leaves, where `nu` is the number of syntactically nonlinear two-input DEF gates. This should retain all gates as affine functions of ORIGINAL source coordinates on each leaf, including with shared gates and reconvergence.

Precommitted falsifiers:
1. Some binary truth table fails to become affine when one already-affine input is fixed.
2. A nested/shared, globally fresh gate DAG forces nonlinear output on some feasible leaf despite the guard decisions.
3. Two leaf contexts both contain one original assignment, or a feasible original assignment is omitted.
4. A proposed whole-proof transfer uses an original-relative support-three truth-table step after affine substitution without a *syntactic* Res(XOR) derivation, or assumes historical native ports that have not been authenticated.

Falsifiers 1–3 are excluded in the declared circuit model by the proof and independent finite checks. Falsifier 4 is **OPEN** and prevents promotion of the circuit result into an unconditional proof-size compiler.

## SEARCH and continuity

Read complete `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and `proof2.txt` pre-run blob `159dbd30b59db8175ec1cbcf9e577ae6670dc93d`, issue #3 and recent peer updates. Read the November 2 five-role handoff, `AGENTS.md`, `CODEX.md`, research skill, historical `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`), LSPV-1/483 report `research/agents/lspv-1/2026-11-07_1100_LSPV1_DEF_BUDGET_GUARD483.md` (blob `929cabe8dee7a57aaa7e58e4398e8daa9737103d`), LSPV-1/488 (blob `4481c9a978ce907fac10c789f756c41d9b252426`), LSPV-3/483 (blob `b94dcf1dad2aef841f7b885f7728e0deb4b41f6e`), Grok `GROKPROOF/2026-11-07_1920_PROGRESS.md` (blob `231561ce216699f286b705a0056584789ba9ee99`) and Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`). Also examined `konard/p-vs-np/scripts/proof_status.json` (blob `93b77ed3d8fe456f81c690035f45f07910a247f2`), `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` (blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`), `meelgroup/frat-xor/format.md` (blob `986a21aa92b62f844ef1fce852193142c41b2b1f`), `tanyongkiam/cake_lpr/README.md` (blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`), `peitl/short-proof/README.md` (blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab`) and `openai/math/README.md` (blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`). No audited source supplies the missing historical DEF/LOCAL conversion grammar. Searches used public indexed web and GitHub code/repository search; a separate Google-branded UI was not available.

**Prior art authenticated:** Chistopolskaya and Podolskii, *Parity Decision Tree Complexity is Greater Than Granularity*, arXiv:1810.08668 (2018), §2.3 Lemma 5, proves the underlying parity-decision-tree vs AND-gate argument. This is **NOT** a novel general circuit theorem. Soeken, arXiv:2005.01778 (2020), formalizes multiplicative complexity as minimal AND count in XOR-AND-inverter networks. Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (24 October 2026), §7.1 Theorem 7.2(a), is a lower bound in syntactic Res(PC_r/F_p), not in historical R_mix341. In particular Pang Fact 7.1 has a bound exponential in the number of ORIGINAL variables involved; it cannot silently be applied at constant cost to three high-width affine forms.

## PROVED/RESTRICTED: exact affine-guard stratification

Take a finite acyclic DAG of `d` globally fresh two-input *conservative* Boolean definitions, where each input is an ORIGINAL source variable or an earlier gate. Each of the 16 two-input Boolean operations has unique algebraic normal form over GF(2):

$$
f(u,v)=a_0\oplus a_1u\oplus a_2v\oplus a_3uv.
$$

Let `nu` count gate nodes with `a_3=1`, even if coincident operands make one gate semantically affine. **Theorem:** There is an effective binary decision tree of depth at most `nu`, with at most `2^nu` formal leaves, whose path guards are affine equations over ORIGINAL inputs; on every feasible leaf, **every** derived gate output equals an affine function of the original inputs. Every original assignment reaches exactly one leaf. Empty guards can be discarded; reconvergence and sharing are preserved.

**Proof:** Process the gates topologically. An affine gate of previously affine signals stays affine. For the next syntactically nonlinear gate, its inputs `u=L(x)` and `v=M(x)` are already affine under the current guard. Branch on the affine equation `L(x)=b`, `b in {0,1}`. On that branch,

$$
f(b,M(x))=a_0\oplus a_1b\oplus(a_2\oplus a_3b)M(x),
$$

which is affine. The two equations partition the current guard exactly. Repeat once per nonlinear gate. A gate with both inputs equal or a contradictory guard causes no unsoundness; it may create an empty leaf. At every join, retain the corresponding guard; do not reuse a branch-only conclusion globally without discharging it. QED.

In particular, **one large XOR-only network** involving `s` original inputs has `nu=0` and only one affine leaf, whereas direct original-coordinate pinning has `2^s` cases. A single binary AND can raise the formal leaf bound only by a factor of two even when its input is a parity of many original coordinates. This is a representation-sensitive upper-bound control, not a proof of efficient proof discovery.

## CONDITIONAL whole-proof compiler proposal and precise obstruction

LSPV-1/483 established, **under separately stated assumptions**, a source-preserving Res(XOR) translation by fixing all `s` original DEF input coordinates, with size `K 2^s(m+q+1)`, refined in [P2-L3-483] using `s=d+c-r-delta`. Replacing coordinate pinning by the affine decision tree would give a bound of the following form **ONLY IF** every legal proof line and inference is syntactically compilable after substituting branch-dependent affine expressions into its named ports, with total per-branch overhead polynomial `P(N+B_pi+q+m)` and **ONLY IF** affine guard joins are legal with explicit paid target certificates:

$$
S_{\mathrm{Res}(\oplus)}(F)\ \le\ 2^{\nu}\,P(N+B_\pi+q+m).
$$

This display is **CONDITIONAL**, not a result already supplied by LSPV-1/481 or Pang Fact 7.1. Source-relative three-named-variable locality does NOT imply three ORIGINAL variables after arbitrary affine substitution. Each affine guard can have width `n`; its explicit equation mask, proof of local entailment and certificate references must be paid. The original source must remain F rather than a merely equisatisfiable augmented CNF. No new native R_mix341 SPLIT/WEAKEN/DEF/PORT rule is assumed.

On Pang's established `F(n,3,8n)` family, with independent uniform signed proper triples from `8*binom(n,3)`, ordinary encoded bit length `N=Theta(n log n)`, Theorem 7.2(a) gives exp(Omega(n)) syntactic Res(XOR) lower bounds **with high probability**, but this only forces `nu=Omega(n)` for a polynomial-size mixed proof **IF** the displayed compiler is actually proved for the chosen mixed calculus. Since `nu<=q`, such a linear gate budget is perfectly compatible with polynomial mixed work. It does not establish [P2-B1] or [P2-B2]. Haken ordinary Resolution PHP bounds, Cook Extended Resolution shortcuts and easy GF(2) odd-Tseitin contradictions remain mandatory distinct controls.

## ITERATE: finite independent reproducibility

Deterministic Python producer (seed `48420261107`) generated **120** circuits, `n=3..8`, `d=1..11`, covering all-affine, mixed and nonlinear gates; **715** total gate occurrences, of which 352 nonlinear; 14,707 formal leaves, 848 feasible leaves, 79,448 producer assertions, three invalid circuits rejected. The producer evaluated all original assignments for each circuit and checked unique matching guard and every gate output. A separately coded Node.js verifier uses direct truth-table cofactors (not ANF) and independently checks exact gate-output affine expressions and each feasible leaf, reporting **95,921 assertions** and three invalid-circuit rejections. A separate wide control uses **20 original coordinates, 19 XOR gates and two AND gates**, giving exactly **four formal affine branches** versus `2^20` coordinate-pinning branches; 522 deterministic assignment samples passed independent replay. Original-source odd and even charge `K4` cubic Tseitin controls have 16 proper 3-clauses and respectively 0 and 8 models.

These controls establish finite correctness, not historical byte acceptance, global minimum proof size, asymptotic hardness, or a machine resource theorem. Python tracemalloc peak 29,649,223 bytes, producer wall 4.39228s; independent Node host RSS 104,472,576 bytes. Full fixture JSON occupies 2,731,149 bytes; this is **not** the proof-certificate cost of an optimum mixed DAG. The archive contains full independent implementations, fixtures, outputs and hashes. All generated leaf records are charged as output bits in any actual compiler. Source parsing, graph reads, acquisition, caches, failed searches, reference joins, verification, recomputation and all-phase simultaneous peak space must still be charged.

## Exact next obligations and status

**Material refinement:** `nu` (nonaffine paid gates) is a better potential structural branching parameter than `s` (all original coordinates entering DEF). **New missing bridge:** prove a fully **syntactic** affine-substitution-stable and source-retracting Res(XOR) compiler for every accepted historical LOCAL-CONVERT/AND3/RES/GF(2)/DEF edge, including affine guards of unbounded original support, reconvergence, owner-facet identities and paid branch joins. An unauthenticated checker or convenient completed grammar does not suffice. Native byte grammar [P2-D1], unrestricted normalization [P2-C3], all-rule superpolynomial minimum [P2-B1] and noncircular same-calculus B3 [P2-B2] remain OPEN. Root main.tex returned empty content at blob `68188a24badda635a5983fda1c381cdb694fd497`, so protected manuscript regions were not edited.

### Primary references
[1] A. Chistopolskaya and V. Podolskii, *Parity Decision Tree Complexity is Greater Than Granularity*, arXiv:1810.08668 (2018), §2.3 Lemma 5. https://arxiv.org/abs/1810.08668
[2] M. Soeken, *Determining the Multiplicative Complexity of Boolean Functions using SAT*, arXiv:2005.01778 (2020). https://arxiv.org/abs/2005.01778
[3] S. Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (24 Oct 2026), Fact 7.1 and Theorem 7.2(a). https://arxiv.org/html/2610.00837v2
[4] `meelgroup/frat-xor/format.md`, verified external XLRUP provenance specification, NOT a native rule specification.
[5] `j15marti/pnp`, historical /341, LSPV-1/483, LSPV-3/483, LSPV-1/488.

## Publication / final proof-chain reconciliation (readback)

GitHub publication and complete readback verified for the mathematical report, executable, raw summary and five-role handoff. The precise published compact JavaScript (blob `dd43eaca9f95d9a423cb28dafef262c5040b8cb9`) was independently evaluated from GitHub-fetched bytes in a V8 isolate: PASS 16 truth tables, 612 assertions, 20-variable wide case with four leaves, and three malformed controls rejected. The full 120-circuit Python/Node fixture and both independent implementations are preserved in the accompanying conversation reproducibility ZIP.

At tracker-commit time another role had advanced `proof2.txt` after the initial review. The **current** full prewrite blob was `22333923e16964b1d14b6536b2d06bf0140dccb2`, preserved as a complete content-identical outbox at `research/agents/lspv-3/outbox/2026-11-07_LSPV3_PROOF2_PREWRITE484.txt`. The optimistic-concurrency update appended **[P2-L3-484]** with zero modification to prior bytes, commit `9dfe2e3c576f922b1599334c0d3f9f62d32666bb`; complete readback gave blob `7f819167a911a1fba2a6561fb99d9a374b06c332`. `proof1.txt` was independently reread unchanged at blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`.

This update does not certify historical R_mix341 accepted-byte proofs, unrestricted proof-size hardness, noncircular B3, or a P-versus-NP result.

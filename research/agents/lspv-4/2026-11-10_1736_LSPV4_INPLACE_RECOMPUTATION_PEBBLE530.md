# LSPV-4/530: In-place GF(2) proof-DAG scheduling and arbitrary recomputation

**2026-11-10 17:36 PST | PNP Time-Space Resource Auditor | historical Route A retained | PROVED/EXACT in a restricted complete-value-slot model, COMPUTATIONAL independent audit. P versus NP OPEN.**

Material evidence **[P2-L4-530]** refines [P2-L4-529], [P2-L4-525], [P2-L4-528]. Main pathway [P2-D1] -> [P2-C3] -> [P2-B1] OPEN; separate [P2-B2]/B3 OPEN.

## IDEA -> SEARCH -> ITERATE

**Candidate:** Destructive output updates reduce the exact paid-value retention optimum of the fixed source-authenticated K4 shared-XOR occurrence DAG by one slot relative to /529. Under the explicitly declared simultaneous **whole-value** binary operand semantics, even arbitrary eviction and physically charged recomputation cannot reduce it further.

**Falsifiers:** (F1) 2-slot valid execution for k>=1 shared XOR pairs; (F2) 1-slot execution for k=0; (F3) a fixed-k in-place no-recomputation schedule needing >3 slots; (F4) an abstract path that charges a reused paid ID twice or forces /529's no-overwrite physical policy as universal. F1-F3 are excluded by constructive and symbolic arguments plus independent exhaustive enumeration. F4 is excluded only by using distinct logical-occurrence payments and a separate physical runtime ledger, not by any new native tariff.

**Corpus:** Complete root proof1.txt and proof2.txt, issue #3 and recent comments, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, November 9 abstract-interpretation handoff; original LSPV-2/341 producer and partial checker; LSPV-4/523-529, /529 handoff, LSPV-2/539 source-bound checker and /544 UTF-8 replayer, LSPV-3/556 RES-byte counterexample, LSPV-1/559 soundness guard from issue #3, GROKPROOF 2026-11-06 progress and Claude 2026-10-28 one-tape analysis. There is no recovered complete historical R_mix341 checker.

Native pins: original /341 producer SHA 4081022e8a3841d79f751a3d3a7a10decbb026da; partial /341 checker SHA fcb7d4ced8f922de14c0bda16263a8cc7853e8e0; declared /341 semantics SHA c87acd11d32ccfc3b7acd3667ef11daeb60079cb; separate /539 strict checker SHA fc91a6f33d0d010d6225365a3d9ce72a090af21f.

**Change-aware external repo checks:** konard/p-vs-np scripts/proof_status.json SHA 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research METHOD_INDEX.md SHA 18d693ea71dfa433370eb7afbebc3106e32f03e5; meelgroup/frat-xor format.md SHA 986a21aa92b62f844ef1fce852193142c41b2b1f; tanyongkiam/cake_lpr README.md SHA e94f45e9aa000cd9ada12f4c771ac9daf28fe53c; MassimoLauria/cnfgen cnfgen/families/tseitin.py SHA 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab. These are distinct hypotheses, encodings and proof formats, not authentication of missing native R_mix341 rules. Google-platform and OpenAI-code-repository audits were not completed independently this run.

Primary references: Cook and Reckhow, *J. Symbolic Logic* 44 (1979) 36-50, DOI 10.2307/2273702; Nordström and Håstad, *Theory of Computing* 9 (2013) 471-557, DOI 10.4086/toc.2013.v009a014. Neither proves the project-specific exact optimum.

## Original source and occurrence DAG

The externally reconstructed signed proper strict K4 odd-charge Tseitin 3-CNF has 6 edge variables, 16 original width-3 clauses, 163 ASCII DIMACS bytes, SHA-256 861b38239ec08050a7b38b3da04fd79c17d43624a8f755be5a1417d8f01745c8. Independent complete 64-assignment verification gives **0** satisfying assignments, whereas even charge gives **8**. This is a finite control, NOT an asymptotic hardness family.

For each vertex v, three binary AND3 nodes d_(3v), d_(3v+1), d_(3v+2) combine four original clauses into parity row f_v=d_(3v+2). Paid XOR nodes: a=d12=XOR(f0,f1), b=d13=XOR(a,f2), z0=d14=XOR(b,f3)=0=1. For i>=1 append u_i=XOR(z_(i-1),a) and z_i=XOR(u_i,a), each with fresh distinct paid inference ID. The original 15-node derivation remains a cheaper legal refutation than its expanded detour.

$$
W(k)=15+2k,\qquad R(k)=30+4k,\qquad D(k)=6+2k.
$$

W counts distinct unit-paid inference occurrences; R counts premise references without a newly invented native tariff; D counts ideal parallel dependency depth, not machine-time.

## Theorem 530.1: exact destructive-value peak

**Defined model:** SOURCE is read-only; each paid-result slot stores one **entire** typed derived factor/affine row, regardless of bit width. Every binary inference requires both paid operands simultaneously available *before* execution. In a no-recomputation schedule, a result may overwrite a paid operand at its last use; physical cache values may be discarded after their last use. The stronger adversarial model permits arbitrary eviction and later reexecution. Every reexecution pays an additional **physical evaluation** but not another *logical proof creation* for the same already-paid occurrence.

For the above fixed DAG and this model:

$$
\boxed{
P_{\min}^{\mathrm{inplace+recompute}}(k)
=P_{\min}^{\mathrm{inplace,\ no\ recompute}}(k)
=\begin{cases}2,&k=0,\\3,&k\ge1.\end{cases}}
$$

**Upper bound:** Compute f0 and f1 in two slots (each three-step local AND3 chain overwrites its last-used result), then XOR to a, overwriting a spent operand. Compute f2 in a second slot, then b=XOR(a,f2), overwriting f2 and retaining a if k>=1. Compute f3 in a third slot, then z0=XOR(b,f3), overwriting b; retain (a,z0). Every subsequent u_i,z_i overwrites a last-used z/u result while a remains live, at most three slots. If k=0, discard a after b; the whole schedule needs at most two. No recomputation is used.

**Lower bound, k=0:** Creating a requires its two different paid f0 and f1 operands resident together, so one slot is impossible.

**Lower bound, k>=1 even with arbitrary recomputation:** To create u1, a and z0 must coexist physically. At the FIRST moment they coexist, whichever is computed last requires TWO OTHER distinct paid inputs: f0,f1 for a, or b,f3 for z0. The already resident first value plus these two simultaneously required premises force at least three slots. Destructive overwrite occurs only after the premises are read. Thus no two-slot execution is possible. QED.

**Scope caution:** This is an exact whole-value *abstract physical execution model*, NOT a native indexed-machine bit-space theorem. Bit-streaming an XOR without whole-row materialization, alternate representation or special-purpose hardware may violate this model's simultaneous whole-value assumption. This theorem neither adds an in-place proof inference nor declares deletion free in historical R_mix341.

## Executed finite audits

A new standalone Node.js BigInt-set BFS enumerated every reachable paid-value cache with arbitrary evictions and recomputation. Independent Python BFS reproduced its reachable state counts, physical evaluations, and source SHA; Python also exhausted all topological orders by order-ideal DP for the fresh-output and in-place no-recomputation cases. The two languages agreed for k=0,1,2,4,8,16. Python additionally checked k=3. All source/parity and hostile controls passed.

| k | W | /529 fresh peak | In-place peak | Cap=2 reachable states | Cap=3 reachable states |
|---:|---:|---:|---:|---:|---:|
| 0 | 15 | 3 | **2** | 109, reachable | 510 |
| 1 | 17 | 4 | **3** | 120, unreachable | 652 |
| 2 | 19 | 4 | **3** | 120, unreachable | 881 |
| 4 | 23 | 4 | **3** | 120, unreachable | 1613 |
| 8 | 31 | 4 | **3** | 120, unreachable | 3853 |
| 16 | 47 | 4 | **3** | 120, unreachable | 11405 |

For k=0 capacity two reaches the sink in 15 physical evaluations. For k>=1 capacity three reaches it in exactly W physical evaluations with no recomputation. Capacity one cannot reach the sink. Hostile controls: SAT even-charge flip, forward-reference mutant, bad k, absence of too-cheap states and cross-language exact matching. The programs are NOT a full historical R_mix341 verifier; /529 separately replayed the fixed typed proof against the **distinct** /539 source-bound fragment checker.

Code: experiments/arc/lspv4_530_inplace_recompute.mjs (executed in V8 and readback verified). Raw: results/raw/arc/2026-11-10_1736_LSPV4_530_INPLACE_RECOMPUTATION_RAW.json. Independent Python source and raw results are provided in the attached reproducibility archive.

## Full resource firewall and outstanding gaps

For the *recovered* SOURCE/AND3/XOR fragment: SOURCE has zero paid **logical derivation** charge; every distinct paid AND3 or XOR has weight one, references are tracked independently. Declared historical RES, LOCAL-CONVERT and DEF also have unit charges in /341 prose, but their historical byte grammar, defining facets, private/exported wires, cases, weakening, context/discharge, joins/deletions, and reference tariffs have **not been authenticated** [P2-D1]. Never infer their implementation from this slot experiment.

The 163 source bytes, all proof records, IDs, 2W references, affine masks, evidence bits, input reads, parsing, index/head updates, lookup, cache memory, guest simulation, possible reexecution, and output must be charged under an explicit physical machine. Actual JSON checker memory is NOT the 2/3 semantic slots. The compact and extended proof alternatives remain eligible for W_R(F); no component lower bound may count a shared paid occurrence twice. Physical recomputation can incur time while **not** creating a second logical proof node. D is merely ideal unit-operator span, not a native parallel bit-time bound. No cost-favorable universal algorithm or superpolynomial lower bound follows.

**Material advance:** exact stronger destructive-update and recomputation test of /529, independently enumerated and with symbolic proof. **OPEN:** [P2-D1] complete historical native accepted-byte grammar; [P2-C3] all-rule cost-sound, goal-preserving abstraction; [P2-B1] unrestricted superpolynomial mixed-calculus minimum; [P2-B2]/B3 separate. P versus NP OPEN.

Root main.tex returned empty content with SHA 8f22f92be2b321e9f9f9a6a58cc319ce6af05a2b and was left unchanged to preserve ownership. All five research roles and titles, Pacific schedules, exact historical R_mix341 weights and the TWO Route A/THREE Route B labels were left untouched.

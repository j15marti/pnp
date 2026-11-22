# Restart audit of first-read replay

22 November 2026, 01:15:02 PST. PNP Independent Counterexamples.
**DYNAMIC-REPLAY-RESTART-AUDIT1**, within DYNAMIC-COMPATIBILITY-OBLIGATION1.
Snapshot: 12da5f0cf86d3b5d0c1e808f7a1adeee6eab472d.
**PROVED/EXACT restricted counterexample; COMPUTATIONAL transition audit. External independent review pending. P versus NP OPEN.**

The initial-state replay proof in [1] survives this audit on the authenticated cycle solver. Resetting its record at a later checkpoint while retaining the definition “first scan of an original input cell during the whole run” does not. Bounds already excludes unknown restart configurations: this report tests that boundary, not a claim that Bounds made the invalid extension. This is a separately implemented audit in the same conversation, not independent external certification.

## Named claim and counterexample

The rejected extension says: for every fixed deterministic one-writable-tape Boolean SAT decider A and a publicly selected later phase, the output D is decodable from public A,N, phase control/head and the symbols at original-input cells first scanned globally during that phase. It omits the checkpoint tape and all earlier records.

Fix A first. Use the exactly authenticated cycle solver in [2,3], with exhaustive fallback on valid nonmembers. It scans every original input bit, discovers the two marks by exact regeneration, computes the Boolean label, and erases source and scratch while carrying the label in finite control. It writes D at the origin and merges control to READY, head at origin, all other cells blank. Then it reads D and writes the terminated output. This is a legal offline solver, not an online service.

For every even k>=6 choose equiprobably the same-length compiled cycle instances (p,q)=(1,2) and (2,2). Their labels are SAT and UNSAT. Let U=D and let B specify A,k,N, that two-point distribution and the READY rule, but not the sampled input, label or absolute checkpoint time. In the suffix the proposed global-first-read event set E is empty on both inputs, hence Pi is the empty word and H(D|B,Pi)=H(D|B)=1. No exact decoder exists. With b=1,h=0,rho=1, the attempted zero-length exact encoding fails at its decoder premise, not at the entropy inequality. The all-UNSAT promise loophole is absent.

Four concrete falsifiers delimit the audit: omit the checkpoint cache despite no new global first scans; provide that cache or absolute time freely; repeat the same acquisition events while retaining rho=1; treat source clause stages as compulsory execution phases. The first is realized here. The others remain invalid ways to repair it.

The smallest correction is to include the actual origin-cache read in E, with Pi=D. Its two one-bit records are prefix-free, its position is public, h=0,b=1,rho=1, and the identity decoder proves E[T]>=H(D|B)=1. Alternatively reconstruct the checkpoint from the previously charged initial record. If that full record is included in B, this particular D has zero remaining entropy. Reusing it for several unconditioned obligations requires accounting for event overlap. None of these choices creates compulsory repeated work.

## Explicit transition evidence

The new script gives a read-before-write finite-state machine computing p OR q from two bits. START reads/erases p and moves right; S_p reads/erases q and moves left; W_D writes D and merges to READY; READY rereads D and moves right; OUT writes # and halts. Only the first two transitions are global first scans. The five transitions use two tape cells. Pretransition cell spans are 2,2,1,1,2, so cell-span CM=8. Fixed finite control contributes only a constant, not measured by this cell statistic.

All four inputs were executed. Initial replay from only the two-bit record exactly reproduces every transition and output. Restart replay from only the one cache bit also succeeds. Restart with an empty record raises a missing-checkpoint error. Inputs 00 and 10 have opposite outputs and identical empty suffix global-first-read records. These finite checks test the replay implementation and overwritten cells; they do not simulate the complete SAT prefix or prove an asymptotic bound. This is a new test of the first-read interface, not a rerun of the earlier abstract branch-equivocation enumeration.

[Code](../../../experiments/dynamic_redteam_restart_audit_20261122.py), [raw evidence](../../../results/raw/dynamic_redteam_restart_audit_20261122.json). Run `python experiments/dynamic_redteam_restart_audit_20261122.py`.
Script SHA256: c459742d31d3cf723bf0f38031020dfa22f125ae52fb83143051fc4d8705b5c4.
No randomness. All four cases pass. Hashes identify artifacts, not semantic equality.

## Same-execution encoding and costs

The SAT integration uses the existing compiler, not the two-bit input length. Set c=4k+4,d=k+1,r=c+1,
n0=d+(10c+1)r+2, m0=(20c+4)r, n=n0+m0+3, m=2m0+4,
w=ceil(log2(n+1)), and
N=3n+2+2 floor(log2(m+1))+3m(w+1)+w=Theta(k² log k).
Layout is unary n plus delimiter, gamma(m+1), signed width-w clause triples, two explicit n-bit local assignments and a w-bit release ID. Compiler equivalence and adjacent local witnesses retain their peer-review status. No separated-input cut layout is inferred.

For each gate, the two marked zero-degree vertices force zeros; propagation through the remaining degree-one vertices alternates bits. The branch exists exactly when its mark index is odd. Hence D=(p mod2) OR (q mod2), including both labels. This independently reconstructs the scalar rule from the source generator; the original 74 source cases and two compiled-image records were read, not rerun.

| Stage of the fixed authenticated solver | Charged conservative cost |
|---|---|
| Parse, validate, extract source, regenerate target and compare all fields | O(N³) time, O(N) span |
| Discover marks, including failed pairs | O(k²) pairs times O(k) source comparisons |
| Physical access, IDs, counters, copies, representation changes | O(N²) per comparison; retained input and addresses included |
| Cache, erase through high-water delimiter, return to origin | O(N) additional time |
| Actual cache read and terminated Boolean output | O(1) time |
| Recognition failure | Paid prefix then exact exhaustive fallback; UNKNOWN is not UNSAT |

Thus admitted-family T=O(N³+k³N²)=O(N^(7/2)), peak physical S=O(N), CM_phys=O(N^(9/2)). These are symbolic inherited implementation bounds, not measured TM timings. Separately parameters k,p,q and time t describe the same configuration, giving CM_min=O(T log N). This is a minimum-description bound, not a free physical compressor. The general fallback can be exponential; the bypass is not a uniform polynomial SAT algorithm. Arbitrary global preprocessing, relocation, sharing, algebra and recomputation remain permitted and charged.

For any fixed cap T<=KN^a preserve S=O(N^a), CM_phys=O(N^(2a)), CM_min=O(N^(a+1)), and the distinct count-map circuit ceiling O(N^a log N). No exponent is excluded here. The internally reviewed static permutation family remains a single-tape polynomial calibration, with matching quadratic-time/cubic-CM bounds and ceilings Dh<=N²/8, Dh²<=N³/27. Boolean, strict T5, symmetric C and ordered R claims are not exchanged.

## Sources and fresh searches

1. [Bounds first-read lemma, pinned 12da5f0](https://github.com/j15marti/pnp/blob/12da5f0cf86d3b5d0c1e808f7a1adeee6eab472d/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-22_005702_First_Read_Replay.md). Exact initial replay and its stated exclusion of unknown starting scratch.
2. [Construction, pinned 3757eba](https://github.com/j15marti/pnp/blob/3757eba746904cbe2983b6cbdda9f8a3bf9b0f07/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_003353_Factor_Backdoor_Acquisition.md). Original generator blob 0366756ac45450760fefef2cf3e11808e8df84b6 and raw blob bdc8f154a8cd9ea4c93a51627c81db4240b35a0a inspected.
3. [Accounting, pinned 4ed0e24](https://github.com/j15marti/pnp/blob/4ed0e245baadd5e7a41a82d979fa77056e8428dd/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-22_004337_Branch_Equivocation.md). Exact erased-cache construction, residual uncertainty and same-execution ledger.
4. Shannon, *A Mathematical Theory of Communication* (1948), 1949 collected reprint, section 6 pp.11-12. [Primary text](https://rarebooksocietyofindia.org/book_archive/shannon1948.pdf). Fresh query “Shannon mathematical theory communication 1948 conditional entropy joint entropy pdf”; read finite discrete conditional entropy and H(X,Y)=H(X)+H(Y|X). Only that finite identity is used; no asymptotic coding theorem is transferred to SAT.
5. Fresh six-org GitHub query `"Turing" "simulator"`: anthropics yielded a sandbox-config substring match (0bbebed0aa9a8e628dc4df8bc30293550a1988eb); openai yielded TapeFolding.lean (4eaee87548250b2682affda7d05d947c05554bae); xai-org no hits; google yielded XLS module simulation (b16df3edaebcfe6ef760fb5cb5a318d55a96e881); google-research retried once after 429 and returned vocabulary words (87e25a5ba04d2c4cf0108f0cec96d648fe2b945a); google-deepmind yielded a robotics README substring match (0ce4c2b9589101d239cc833c92dd5f7c8da67b9e). The [OpenAI file](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/lean/OAI/Computability/FiniteCompiler/TapeFolding.lean) was read: its one-sided step reads c.cell c.pos before updating it, and its simulation relation includes the tape. This is a relevant model-checking clue, not a proved compulsory-work transfer. No Lean build or theorem import.
6. Web fallback queries paired anthropics/openai, xai-org/google and google-research/google-deepmind with “Turing simulator”. Results included unrelated simulators and Anthropic formal-math documentation; no additional decoder theorem verified. Official ownership checked through [Anthropic](https://github.com/anthropics), [OpenAI](https://github.com/openai), [xAI release](https://x.ai/news/grok-os), [Google guidance](https://opensource.google/documentation/reference/github/where), [Google Research](https://research.google/resources/) and [DeepMind](https://github.com/google-deepmind). Bounded search results are not an absence proof.

Current directive, transport, governance, research instructions, relevant T5 definitions, own latest blossom report/code/raw and issue324 were recovered. No full checkout is present, so repository preflight and LaTeX compilation were not run. No historical TMR manuscript or agent setting changed.

DISJ/equality sanity PASS within scope; same-execution DTISP PASS; deterministic replay PASS for the specified known-start execution, with restart restriction exposed. Relativization remains OPEN for unrestricted promotion. No Natural Proofs/algebrization bypass. Affine/Tseitin, complements, private leaves, forced domains, decision witnesses and full-state entropy controls remain valid.

**One next dependency, Bounds and Accounting:** supply a later local decoder whose starting information is reconstructible from charged records and whose remaining demand survives conditioning, endpoint debit and reuse. Synthesis receives the explicit restart obstruction; Construction retains its constructive scalar fast path. The failed reset claim is retired; compulsory superpolynomial work and general polynomial SAT remain OPEN.

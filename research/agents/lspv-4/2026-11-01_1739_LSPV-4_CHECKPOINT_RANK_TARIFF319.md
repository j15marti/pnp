# LSPV-4: CHECKPOINT-RANK-TARIFF319
**2026-11-01 17:39 PST. PROVED exact restricted source-indexed checkpoint schedule; COMPUTATIONAL independently checked both-label original controls; strict FLMV and P-vs-NP OPEN. External review pending.**

## Obstruction and four falsifiers
Only all valid duplicate-free proper Döcker monotone 3-SAT-(2,2) originals form the NP-complete target. Malformed strings reject. BRIDGE317 first produces signed balanced pure-3 CNF from promised signed balanced width-(2,3) CNF using 1,064 output clauses per input clause, with 792/789 private names depending on binary/ternary source width. MIXED316 produces 131 canonical monotone clauses per signed input clause. UNTAGGED-RANK-PARITY318 proved that one canonical output bit can depend on an unpreprocessed prefix parity of r independently swappable source records. Fixed clause slots alone do not give polylog arbitrary-bit access.

F1 fixed clause slots give polylog bit access: FALSIFIED in 318.
F2 PAID checkpoint ranks can lower arbitrary output-bit access cost within a bounded index: PROVED below.
F3 sqrt(N) rank-index space entails N^{o(1)} bit-access work: FALSIFIED for this predecessor-checkpoint implementation; worst queries still access Theta(sqrt(N)) source tags.
F4 this restricted improvement proves a universal ARC/FLMV contradiction or P!=NP: INVALID; the ordinary-SAT first leg, exact native guest execution and all-input contraction are unproved.

## Theorem 319A: charged rank-checkpoint upper bound
For a valid signed 2P2N width-(2,3) source with n names, m clauses and indicators w_i=[|C_i|=2], the BRIDGE317 private-name base for clause j is

    a(j) = 12n + 789j + 3 rank2(j),
    rank2(j) = sum_{i<j} w_i.

The MIXED316 second stage preserves the designated first variable identifier in a pure-positive copied clause.

For integer B>=1, make one paid sequential pass across ALL m source width tags. At every positive multiple kB<m store the exact count c_k=sum_{i<kB} w_i. There are h=floor((m-1)/B) checkpoint counts, requiring at most h*ceil(log2(m+1)) **retained data bits** (plus parser, counter, index and head tapes). To answer an arbitrary j, read the stored count at floor(j/B)B, then read only the source width tags in [floor(j/B)B,j). This gives EXACT rank2(j) from at most B-1 additional source width probes. Address construction, indexed jumps, head motions, index erasure and work-tape checkpoint lookup remain separately charged. The initial pass costs m source width reads. Under a single-head writable-tape realization, locating a checkpoint also costs up to O(h log m) head motions, NOT O(1).

Choose B=ceil(sqrt(m ceil(log2(m+1)))). Then checkpoint data bits and per-query source width probes are each O(sqrt(m log m)), and therefore N^{1/2+o(1)} on the established fixed-width N=Theta(m log m) adversarial source family. This is a **constructive upper bound for the specified architecture**, NOT a lower bound on all source-indexed algorithms or all compilers. A neighboring-checkpoint scan, a different namespace, a pre-tagged generated source, caching or width-sorted inputs may do better.

Proof: split [0,j) into the complete prefix through floor(j/B)B (stored exactly) and a remaining suffix of size <B (read exactly). Counts never exceed m, so the stated bit width suffices. The number of nonzero full B-boundaries strictly before m is floor((m-1)/B). The square-root choice balances O(m log m/B) checkpoint bits and O(B) source reads. QED.

## Independent both-label controls and counted work
Producer and no-import verifier each checked all 1,022 valid signed-balanced F_(r,z) permutations for r=1..9, 8,194 record-pair flips, 958,308 exact prefix-rank requests and 8,616,486 explicitly counted source-width probes across multiple B values. F9 remains valid canonical n=9,m=12 with 70 models; its SAME-original coherent pins give SAT 3 versus UNSAT 0 extensions. The comparative signed-balanced mixed-width H has 37 models and same-original pins 6 versus 0. Y6 has 20 models. Original F9 S/U extreme compatibility: 264 verified clause-pair modes; 6,144 complement identities; six malformed canonical examples rejected. For m=130: B=16 stores 8 8-bit rank words (64 **data** bits) and reads at most 15 suffix tags; B=32 stores four words (32 data bits) and reads at most 31. These data-bit sizes omit necessary index/head/control workspace.

U198/V198 original certificates and the MIXED316 512-input-port proof are already verified dependencies but were NOT freshly replayed in run 319. The 318 permutation sources themselves are SAT, and opposite-label assertions concern separate same-original F9/H pinned-residual tests. No enormous final canonical output was materialized. There is NO native FLMV machine benchmark here.

## Fully charged recurrence, FLMV numerical firewall and peak space
For each executed adaptive state z,

    W(z) <= C_grammar,source,index,head(z)
          + SUM_attempted_policies C_acquire,select,switch,fail,verify(z,p)
          + C_signed,cycles,K4,matroid,GE,proof,rank,cache(z)
          + SUM_executed_children (C_encode,child,bit,guest(z,y)+W(y)).

Peak writable space is the maximum simultaneous retained ancestor+source/index/head+proof/GE/cut+rank+cache/translator+child+guest state. Full Shannon fallback decreases the free-variable count, but can use 2^{Theta(n)} time; delta can increase. Logical XOR remains OFFLINE unless charged.

FLMV Theorem 5.7 reference: d*(6/5)=23/45 and d*(241/200)=11642479/23232400. With hypothetical target time/space exponents (6/5,1/2), a=1 length exponent, the strict reference comparison requires multiplicative bit-access rho<1/200 **plus all setup and peak-space obligations**. The checkpoint schedule supplies only a worst-query upper bound rho≈1/2, so it does NOT establish strict numerical transport. It also spends N^{1/2+o(1)} rank bits before guest/ancestor/index/matrix space, without proving the strict space margin. A faithful guest with arbitrary indexed queries must pay the actual translator and no repeated identical query may be charged twice without modeling caching. DELAY/COPY/RECOMP remain hostile controls. A faster compiler might evade this tariff. No ordinary-SAT-to-signed first stage, no all-input polynomial total work, and no arbitrary-A hereditary power-short transformation are proved.

## Preflight and scope firewall
Read FIRST published integrated five-role handoff blob 2b0daece3f69708d7ed0bce1f06e8cbed98d11de and delta-zero formal theorem blob 3c05146b10ffd597f922f395c967dd4b2dd89875. Then read 318,317,316, latest LSPV-1 DECISION-WITNESS-MINIMAX313, LSPV-2 SOURCE-COVER-GUARD318, LSPV-3 FIRST-ORDER-COLLISION-GATE314, LSPV-5 RANDOMIZED-PIN-QUERY-REFEREE276, issue #3, AGENTS, CODEX and pnp-research skill. This is classical checkpoint prefix-summing and no new broad data-structure lower bound is claimed. Web queries: Döcker 2019 gadget, FLMV 2005 indexed read-only model, static succinct rank/select. GitHub queries: j15marti/pnp BRIDGE317, UNTAGGED-RANK-PARITY318, Y6 padding; separately github.com/openai bit-local SAT reduction and rank index (no directly applicable implementation). Primary [1] Döcker 2019 arXiv:1912.08032; [2] Fortnow et al. JACM 2005 DOI 10.1145/1101821.1101822; [3] Laws et al. SPIDER arXiv:2405.05214, context only.

**Safeguard:** main.tex fetch reports nonempty blob 4e909a098a968a43b0202b3035f66e4b9446d9d9 but ZERO returned content bytes. Root-owned-marker reconciliation PENDING; no unsafe root overwrite. Preserve all five task identities, enabled states and hourly Pacific stagger. Full producer, independent verifier, raw JSON and hash manifest are in the current-conversation reproducibility ZIP. This restricted schedule does not solve the all-input theorem. **P versus NP OPEN.**

END_OF_VERIFIED_REPORT::LSPV-4::CHECKPOINT_RANK_TARIFF319::P_VS_NP_OPEN

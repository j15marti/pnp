# LSPV-4 DECISION-WORK-ONLY307
**2026-11-01, 10:10 PST. Status: PROVED/EXACT restricted known decision-tree adversary application; COMPUTATIONAL no-import controls; all-input P-vs-NP OPEN. External review pending.**

## Exact obstruction
CUBEKEY-RESOURCE306 counts 84^t distinct source-safe syntactic pinned-variable cubes and proves that a LOSSLESS SELF-CONTAINED key capable of reconstructing the names and values needs ceil(t log2 84) bits. It does **not** lower-bound space or time for a decision-only SAT solver. This user-requested work-only formulation removes that recovery premise.

## Representation-independent *input-query* lemma
For an exact deterministic decision algorithm on fixed-length binary inputs, let B(F) be a set of all allowed opposite-label inputs G and let D(F,G) be the set of physical bit positions where F and G differ. Every accepting execution on F must query a set meeting D(F,G) for every opposite-label G. Otherwise its adaptive transcript and output would be identical on F and G. Hence Q(F)>=tau({D(F,G)}) where tau is minimum hitting-set cardinality. **KNOWN METHOD:** standard deterministic certificate/block-sensitivity adversary, not a new universal SAT lower bound. It requires neither exact pin recovery nor a particular state encoding.

## Proved same-canonical-original residual-SAT family
Use LSPV-2's connected valid canonical G_t from cyclically cross-linked F9 blocks. Every block pins x1=1,x4=0,x8=0 and either A=(x2=0,x3=1) or B=(x2=1,x3=0), all other values as in the published five-pin contexts. Exact local boundary count matrices independently recomputed here:
W=[[34,47],[23,36]], WA=[[1,1],[0,0]], WB=[[0,0],[0,0]].
The all-A coherent pin input has trace(WA^t)=1 satisfying completion, while replacing just one block with B gives zero completions, for any t>=1. Each one-B input differs from all-A in just the two pin-value positions x2_i,x3_i, and these t pairs of positions are disjoint. **Therefore on the all-A input, ANY deterministic exact residual-SAT decider that handles these t+1 inputs must read >=t pin-value bits**, irrespective of storage/recovery and adaptive policy. Under this declared PROMISE one can attain t probes by reading x2_i once per block and output SAT iff all are zero. The original source G_t is held fixed; this is not a source-only lower bound for the full canonical language. For valid target originals alone one can analogously use disjoint equal-length U198/V198 opposite-label blocks, but those source certificates were not independently replayed in this run.

## Reproducible checks and competing inexpensive strategy
The expanded independent standard-library Python file reconstructs and validates G1 and G2 from original source clauses, verifies matrices W/WA/WB by brute force, counts G1=70 and G2=4614 models, explicitly checks both labels on G1/G2 coherent original pins, all 264 F9 original-clause pair SS/SU/US/UU modes, and 512 complete assignment/complement identities. For t=1,2,3,4,8,16,128 the exact t distinct pin-difference regions and the transfer-matrix all-A/one-B counts are checked; for t<=4 the minimum hitting set is brute enumerated. Fully specified results and checksums are in the expanded conversation ZIP.

| blocks | lossless syntactic key lower bits | minimum required decision-only pin probes |
|---:|---:|---:|
|1|7|1|
|2|13|2|
|8|52|8|
|16|103|16|
|128|819|128|

The decision-only work lower bound is **linear** and tight ON THIS PROMISE. A general N-bit input can always be read in at most N bit probes; input-query lower bounds alone cannot establish superpolynomial SAT time, even if the bit observations are distributed over different source blocks. The necessary work to discover/apply a semantic quotient, a small boundary matrix, or a certified transfer rule is NOT free.

## Work and space charge
For a uniform all-input controller, total work is the sum of actual grammar/source/pin input reads, head/index/address moves, every policy acquisition and failed option, switching, cache matching and replay, cycle/K4/GF(2)/matroid proof steps, output/witness/UNSAT verification, child translation, and guest DELAY/COPY/RECOMP. Peak writable/index storage is maximum simultaneous live state including ancestors, proofs, child buffers and guests; logical XOR is offline unless fully charged. Query count is a lower bound on work in the declared bit-reading model, not the entire FLMV transition count. Decision-only completed states may have two semantic outcome classes, but obtaining the correct one-bit label can require computation; supplying it in advance is circular. With future boundary contexts, semantic equivalence must preserve the complete continuation behavior, not just current SAT label.

## Literature and project audit
Read FIRST integrated handoff SHA b11a6f22315cdaf0d303fe193edf9713d9b9bef9 and saturated-cycle theorem SHA 3c05146b10ffd597f922f395c967dd4b2dd89875; reviewed LSPV-4 CUBEKEY306, LSPV-2 transfer305, LSPV-5 REFEREE269, governance, AGENTS/CODEX and pnp-research skill, and active issue #3. Historical project DOUBLE_WRAPPER_2026-10-07 already distinguishes decision-only from recoverable transcript. Searches: Google/web "deterministic decision tree certificate complexity sensitivity block sensitivity lower bound input queries", "Nisan CREW PRAMs and decision trees", "Fortnow Lipton van Melkebeek Viglas indexed input"; primary Nisan, SIAM J Comput 20(6), 1991, DOI 10.1137/0220062; FLMV, JACM 52, 2005 DOI 10.1145/1101821.1101822; Döcker arXiv:1912.08032. Separately GitHub searched j15marti/pnp "decision-only semantic memo", "CUBEKEY RESOURCE" and github.com/openai "branching program SAT", "decision tree complexity". No novelty inference from search absences.

## Firewall and next lemma
This note does not promote an Ω(t) pin-probe bound to an Ω(t) writable-memory bound or a superpolynomial SAT time bound. The all-valid-target polynomial total adaptive work theorem, universal arbitrary-decider power-short hereditary ARC and quantitative same-machine SAT-to-Döcker FLMV transfer remain OPEN. Next: find a genuinely superlinear/all-input computation adversary surviving semantic compression, source rereads and all adaptive parameter policies; direct input-probe counting alone cannot suffice. No tasks, schedules, ownership or root main.tex changed. **P versus NP OPEN.**

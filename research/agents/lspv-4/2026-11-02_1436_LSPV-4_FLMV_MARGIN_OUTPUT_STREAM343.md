# LSPV-4: FLMV-MARGIN-OUTPUT-STREAM343
2026-11-02 14:36 PST. PNP Time-Space Resource Auditor.
STATUS: PROVED conditional exponent-envelope and declared-buffer implications; independent finite SAT controls; B1/B2/B3 and P vs NP OPEN.

## Quantitative theorem (conditional on a real iterable reduction)
Fix general CNF-SAT and the pre-existing mixed proof calculus Rmix341, with W_R(F) the minimum source-authenticated shared inference-DAG node weight and Wbar_R(N) its worst-case over UNSAT input encodings of length <=N. This theorem is about a hypothetical native-machine SAT solver transform, not about compulsory W_R work.

Suppose for each fixed correct polynomial-time SAT decider A, an ITERABLE correct transform makes <=N^(a+o(1)) SEQUENTIAL child calls of encoded length <=N^(b+o(1)); charges <=N^(d+o(1)) AGGREGATE local time (including input and index access, all failed policies, conversion and combination), <=N^(rho+o(1)) writable peak in EVERY local phase and <=N^(eta+o(1)) retained writable ancestor/results space. Materialized child uses N^(b+o(1)) writable bits. Assume 0<b<1, fully charged code/guest access and a separately proved same-machine FLMV numerical transfer.

Then transformed time/space exponent envelopes satisfy t'<=max(d,a+b*t), s'<=max(rho,eta,b,b*s). Iteration yields fixed-point upper envelopes t*=max(d,a/(1-b)), s*=max(rho,eta,b). Proof: both monotone max-affine exponent maps are b-contractions on their nonconstant branches.

For FLMV candidate beta(c)=((c+2)/c^2-c)/2, the conditional strict exclusion requires s*<beta(t*). At the user-proposed a=3/5,b=1/2,d=11/10,rho=eta=1/2:
 t*=6/5, s*=1/2, beta(6/5)=23/45, strict margin=1/90.
At c=241/200, exact beta=11642479/23232400, half-space margin=26279/23232400.

The unique ccrit>1 with beta(ccrit)=1/2 solves c^3+c^2-c-2=0:
 ccrit=1.2055694304005903...
With all other exponents held at baseline, sharp separate positive increment thresholds:
 fanout a: delta_a < ccrit/2-3/5 = 0.002784715200295156...
 child length b: delta_b < 1/2-(3/5)/ccrit = 0.002309875424901776...
 aggregate local time d: delta_d < ccrit-11/10 = 0.1055694304005903...
 per-child source accessor N^gamma (charged q*N^gamma local work): gamma < ccrit-3/5 = 0.6055694304005903...
 all-phase rho, if user baseline relaxed: rho-1/2 < beta(6/5)-1/2=1/90.
These are algebraic MARGINS, NOT an implemented splitter and NOT a proved application of FLMV.

## Four falsifiers
F1 FALSIFIED for eager answer retention: q=N^.6 independent child answer bits stored in a q-bit array force eta>=.6 and s*>=.6; fails strict half-space criterion. Streaming OR/AND or XOR uses O(1) result bits plus O(log N) index, but may not evaluate arbitrary child-answer predicates and must charge generation/combination.
F2 FALSIFIED for simultaneous child materialization: q*N^.5=N^1.1 writable child bits, whereas one reused buffer costs N^.5 bits if other live structures fit.
F3 FALSIFIED for naive source reread/copy: reading all N input bits once per q children takes N^1.6 probes; copying N bits to writable memory even briefly forces all-phase rho>=1. Neither represents a universal lower bound on local addressable or lazy alternatives.
F4 OPEN: neither these representation-specific costs nor any finite W_R optimum proves a superpolynomial Wbar_R or the weakest bridge B3 (SAT in P implies Wbar_R polynomial) for the SAME fixed calculus.

## Reproducibility controls
A pure-Python producer and an independent no-import Node referee ran. Node: 78 assertions PASS. Exact two-inference resolution DAG for F=(x)&(~x|y)&(~y): all 3 clauses indispensable (each deletion leaves one model), and q>=m-1=2 for sound conservative at-most-binary-premise source proof; source q=2 refutation witnesses matching Rmix341 optimum. SAT one-literal-neighbor has one model. Odd K4 Tseitin 6-variable 16-clause source has 0 models, even K4 has 8. Eight malformed declared DIMACS strings rejected; corrupted resolution inference rejected.
Declared allocation for N=10^6: q=3982 children, length 1000 bits; all descriptions live 3,982,000 bits; eager one-bit answers 3982 bits; one sequential child buffer 1000 bits; online OR result 1 bit plus 12-bit counter. These are abstract bit capacities, NOT Python heap or native FLMV traces.
Previous LSPV-4 342 proof/evidence polynomial domination is retained only for encoded Rmix341 certificates, not arbitrary solver runtime. Wbar_R(N) B3 remains OPEN. P versus NP OPEN.

## Sources / access
Read 2026-11-02 12:04 five-role GitHub handoff FIRST, then active issue #3 and 2026-11-02 peers LSPV-2 343, LSPV-3 342-343, LSPV-4 342, LSPV-5 296; searched project code and github.com/openai. Web opening GitHub handoff failed DisabledError; connected GitHub fetch succeeded. Primary reference: Fortnow, Lipton, van Melkebeek, Viglas, JACM 52 (2005) 835-865 DOI:10.1145/1101821.1101822; Cook-Reckhow JSL 44 (1979) 36-50. Avoid novelty inference from search absence.

Full local archive includes report, Python producer, no-import Node verifier, raw JSON, independent JSON, SHA256 hashes. No root manuscript or automation changed.

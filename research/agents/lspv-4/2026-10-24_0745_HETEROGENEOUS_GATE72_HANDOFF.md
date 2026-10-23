# LSPV-4 HETEROGENEOUS-GATE72: Role 5 and Roles 1-3 handoff

P versus NP remains OPEN. Independent review and consumption have not been confirmed. The existing five scheduled tasks have not been changed.

## Exact construction (Role 5 independent check)

For every even q>=4, source two independent blocks:
A_beta = AND_{i mod q} [ e_{i-1} XOR e_i XOR h = beta_i ],  q ternary XOR equations;
B_b = F_b, the original (q+4)-binary-clause implication chain on z_0,...,z_q,u,v.

Encode each XOR3 equation as its FOUR proper ternary CNF clauses. For each XOR clause C=(l1 OR l2 OR l3), add fresh X_C,t_C and:
(-X_C OR t_C), (-l1 OR t_C), (X_C OR l1 OR -t_C), (t_C OR l2 OR l3).
This forces t_C = X_C OR l1 and encodes X_C OR C.
For each B_b binary clause (a OR b), add a fresh Y_C and ternary (-Y_C OR a OR b).
Tie switch x and all 4q X_C and q+4 Y_C via one directed binary implication cycle x -> G1 -> ... -> G_(5q+4) -> x.

Exact counts: n=11q+9, m2=13q+5, k=9q+4, M=22q+9. Original variables 2q+5; auxiliaries 9q+4, all functional when originals are fixed. Every satisfying original assignment has exactly one target extension, and no rejecting original assignment has a satisfying target extension.

Exact SAT iff parity(beta)=0 OR b != 1^q.
For even q, rank(A_beta)=q-1 on q+1 variables; if consistent exactly four affine models. Target counting identity:
#SAT(D)= [parity(beta)=0] 2^(q+5) + [b != 1^q] 2^(q+1) #SAT(F_b).

The raw strong *syntactic* 2CNF backdoor has size >=q/2: choose one top (t_C OR +/-e_(i-1) OR +/-e_i) clause for each even i, pairwise variable-disjoint. No claim of exact h2.

All guarded switches are in a single binary SCC equivalence class of size 5q+5. No initial binary-only unit or forced literal; no initial ternary is shortened. The SCC quotient exposes one switch, not a 2CNF one-variable backdoor. Its two branches are DIFFERENT:
x=0: normalize t_C=l1; B disappears; residual contains 4q 3-CNF parity clauses, translated into q XOR3 equations, decided by GF(2).
x=1: all XOR gates disappear; residual is precisely F_b 2CNF, decided by SCC.

The direct recognized source scan computes parity(beta) OR (exists zero in b) in linear time, so no mandatory continuation is inferred.

## Explicit both-label controls (Roles 1-3)

UNSAT: beta=100...0, b=111...1.
Affine-SAT: beta=000...0, b=111...1. An x=0 witness exists.
Binary-SAT: beta=100...0, b=011...1. The x=0 branch fails; an x=1 witness exists.
All inputs have identical n,m2,k,M,N, and unsigned literal IDs. Flipping ANY single one of 2q beta/b fields from designated UNSAT yields SAT. Changed signed-literal words occupy disjoint per-coordinate clause groups. Thus arbitrary total exact deterministic deciders of the canonical full language must make >=2q addressed-word reads at the designated UNSAT input, corresponding to Omega(N/log N). This is input acquisition only.

## State-adaptive and charged ledger

S0 parse explicit fixed-width records, discover q and vectors, reconstruct grammar and check every record: O(q) word time and O(q) space.
S1 run actual binary SCC, discover guard class; q/2 <= raw h2, k=9q+4 unchanged: O(q).
S2 try x=0 without knowing label; normalize OR gates; affine equation count q, rank q-1, k remaining 4q: O(q) rank/syndrome and possibly witness.
S3 if parity inconsistency, charge failed attempt and switch to x=1; residual k=0, run SCC on F_b: O(q).
S4 output one bit; SAT optional target witness replay O(n+M); UNSAT two exact child-negative decisions.
Fallback on unrecognized CNF uses complete DPLL, so the policy is total exact with no general polynomial guarantee.
Charge grammar recognition, all source reads, rule selection, both branches when needed, switch, replay, output and O(n+M) peak live words.

## Known NP-complete interaction boundary

Schaefer 1978 applies to Gamma={positive OR2, even XOR3}. The union is not 0-valid, 1-valid, Horn, dual-Horn, bijunctive or affine, even though each sublanguage is polynomial. Therefore arbitrary conjunctions of these two relation types are NP-complete. This is a KNOWN THEOREM endpoint, not a new proof of P != NP.

## Reproducibility

Report: research/agents/lspv-4/2026-10-24_0745_LSPV-4_HETEROGENEOUS_GATE72.tex
Mini: research/agents/lspv-4/2026-10-24_0745_HETEROGENEOUS_GATE72_MINI.py
Raw summary: research/agents/lspv-4/2026-10-24_0745_HETEROGENEOUS_GATE72_RESULTS.json
Local extended full audit is separately supplied as a package; its availability to other scheduled runtimes is NOT presumed.
Audit seed 202610232233; 25,195 named checks, zero failures. 28 canonical records q=4..12; 21 extra scaling records q=16..1024; 3*8192 complete source-assignment checks q=4. Independent generic DPLL, original 2SAT baseline, signed permutations, Horn/XOR/padding/fallback controls passed.
At q=8, the deliberately non-pruning, no-reuse fixed enumerator considers 2^(q+1)=512 leaves, versus at most two tractable-branch attempts for the hybrid. This comparison is RESTRICTED-POLICY ONLY.

## First missing lemma and peer requests

Role 5: audit all construction clauses and q count, source cycles, exact rank and parity consistency, disjoint top-clause packing, Schaefer closure tests, and input-query transcript. Confirm no accidental claim of a generic affine/2SAT backdoor finder or polynomial time for arbitrary CNF.

Roles 1-3: feed the UNSAT and two SAT controls to mandatory-compression/continuation measures. The initial residual and raw backdoor are large yet the runtime-relevant representation changes by verified SCC and XOR/2SAT switches. Any source-aware all-decider lower bound must survive the direct O(q) parser.

Next candidate amplification: allow genuinely interacting non-affine relations without a cheaply recognizable global switch; separately establish source-independent semantic obstruction, a work inequality for every total uniform exact decider, and coverage. All three obligations remain OPEN. ETH/SETH and cryptographic assumptions are not admitted as unconditional proof.

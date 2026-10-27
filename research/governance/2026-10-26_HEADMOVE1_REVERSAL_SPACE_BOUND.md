# HEADMOVE-1: Input-head movement/reversal/workspace forbidden surfaces
Date 2026-10-26. Status: mathematical theorem in an EXACTLY declared one-input-head deterministic model, with finite verification; restricted SAT subfamily EASY, no P != NP claim. Additive to active LSPV-1..LSPV-5.

## Model and result
Use ONE sequential two-way read-only input head and fixed k>=1 sequential read/write work heads with finite alphabets. S(N) counts *all visited work cells* (blank included), not the N input cells and not merely currently nonblank cells. H(N) counts only input-head one-cell moves, R(N) counts sign reversals in nonzero input-head movements, T(N) total bit-time. An output tape is write-only and cannot store readable information outside S. These are worst-case ceilings of ONE total deterministic exact signed 2P2N 3SAT decider.

Start with the verified 15-variable/20-clause W1 gadget from BINARY-WORK-SAT4; opposite-sign paired A and B literal swaps give 772,272,272,0 satisfying models for (a,b)=00,01,10,11, hence UNSAT(H(a,b))=a AND b with exact occurrence balance and unchanged supports. Put m disjoint copies in one standard fixed-width binary clause-list encoding, ordered ALL 2m Alice-sign clauses, then ALL 16m fixed clauses, then ALL 2m Bob-sign clauses. This gives V=15m, C=20m, N=Theta(m log m), central fixed gap G=4N/5 (apart from a fixed header), and SAT(F_m(a,b)) iff a and b are disjoint.

For each a in {0,1}^m, F_m(a,NOT a) is SAT. For a!=b, at least one mixed pair (a,NOT b), (b,NOT a) is UNSAT. For every cut c in the fixed gap, the COMPLETE work-configuration crossing transcripts on those 2^m SAT instances must be pairwise different (standard deterministic splicing). A crossing label includes control, crossing direction, all visited work contents and all work-head positions. Its length is O_k(S+1) BITS since visited work intervals are contiguous and k is fixed. Counting 2^m different transcripts shows mean crossings Omega(m/(S+1)) at EVERY central cut. Sum over G cuts, average over a, then choose a single SAT instance witnessing large total crossings: H(S+1)=Omega(Gm)=Omega(N^2/log N). On that same input, one cut has Omega(m/(S+1)) crossings; consecutive crossings alternate direction, hence (R+1)(S+1)=Omega(m)=Omega(N/log N).

EXACT exponent-space lower bounds for uniform polynomial ceilings:
  h+s>=2,     r+s>=1,     t+s>=2,
where H=N^{h+o(1)}, R+1=N^{r+o(1)}, S=N^{s+o(1)}, T=N^{t+o(1)}, all for ONE machine. This is a new REVERSAL/SPACE axis on top of the earlier tape time/space diagonal: for example t=5,s=0.5,r=0.25 is forbidden despite ample total time. It is not a RAM SAT bound.

For the ordinary SINGLE SHARED writable input/work tape, complete-state stationary intervals have constant bounded length; total head moves H_all=Theta(T) on any halting run, and the finite-state crossing sequence alone forces R=Omega(m) and H=Omega(Nm) for this family independent of extra writable footprint. For k fixed work tapes, total moves over ALL heads are likewise Theta(T), but input-head moves are not.

## Saturation on the easy promise
A B-bit buffer, p=ceil(m/B) sequential input passes, O(log N) address/counter bits yields T=O(Np polylogN), H=O(Np), R=O(p), S=O(B+logN). With B=m^alpha, 0<=alpha<=1, the exponents are s=alpha,r=1-alpha,h=t=2-alpha. Both slope -1 faces r+s=1 and h+s=2 are tight up to subpolynomial factors ON THIS EASY PROMISE family.

## Bounded jump-radius interpolation
Clearly label a DIFFERENT augmented machine M_J: one read-only input head, with a charged binary-offset command that may jump at most J(N) cells per access. It reads only the target symbol. Work tapes remain sequential. Simulating each jump on an ordinary one-input-head machine costs O(J+polylogN) time and O(logN) extra work cells. If J=N^{j+o(1)}, the necessary hybrid exponent inequality is
  t+s+j>=2.
On the easy exact22 promise, skip irrelevant input cells and use a B=m^s buffer, giving an explicit matching upper time exponent
  t=minimum possible for this promise = max(1, 2-s-j), 0<=s,j<=1. The t>=1 term follows independently from input-bit sensitivity: on Alice a=0^m, Bob b=1^m, flipping any single Alice bit changes SAT to UNSAT, so a deterministic one-probe-per-step solver must inspect Omega(m) separate Alice-controlled sign locations even with unlimited head reach.
The 'minimum' is only relative to defined model and family, not general SAT. For J=N, t=1,s=0 is achievable on this promise by direct indexed reads; unrestricted RAM also allows indexed WORK accesses, which this hybrid does not. Do not impose tape-head transport restrictions on standard random-access RAM computations.

## Verification
Standalone /mnt/data/head_movement_exact22_audit.py and JSON check gadget counts, 1364 explicit fixed-length encoded signed exact22 formulas (m=1..5), 43,435 DISJ fooling pairs, and real input-head itineraries on m=4..64 with B capacities and J jumps. The itinerary counts every selected source-sign read; it is a PROMISE-comparison algorithm, not a general 3SAT solver. Complete formal note /mnt/data/head_movement_resource_regions_2026-10-26.md, PNG diagram (true alpha) and source ZIP are user artifacts of this turn; do NOT assume cross-run /mnt/data persists without GitHub publication.

## Priority for five active agents
LSPV-1: integrate h+s>=2 and r+s>=1 in a native one-input-head atlas, avoiding resource mixing with RAT.
LSPV-2: independently verify the jump-radius simulator, direct promises, and head itinerary; test O(logN) indexing.
LSPV-3: analyze whether adaptive source-authenticated certificate discovery can limit R for any correct solver, rather than assuming it.
LSPV-4: verify the complete-work crossing-sequence injectivity argument, space definition, averaging to SAME YES input, and jumps.
LSPV-5: falsify with 2 input heads, a RAM, inconsistent input framing, nonvisited-cell accounting, or alternative promise shortcuts; keep restricted/conditional statuses.

Do not infer P != NP: P=NP gives no a priori bound on input-head reversals or workspace exponent of hypothetical A. A reversal cap is a *new model assumption*, not something derived from SAT. Do not create/reconfigure agents; all five active role schedules remain :00,:12,:24,:36,:48.

Background: Hennie (1965) crossing sequences; Santhanam (2001) SAT tape bounds; Kushilevitz-Nisan (1997), Communication Complexity, time-space chapter; 1978 Visits, Crosses, Reversals for off-line machines; BINARY-WORK-SAT4.

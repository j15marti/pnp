MIXEDRANK-CLOSE59 | 2026-10-17
STATUS: scoped exact theorem, independent review pending. P versus NP OPEN.

TRACK B. Combine RANK2-CLOSE57 and RANK34-CLOSE58 in one simple active mixed support hypergraph H with representative resolved supports of rank 2,3,4.

Rank-specific favorable-branch cutoffs:
r2: degree >=274, otherwise <=273.
r3: degree >=1,001,089, otherwise <=1,001,088.
r4: degree >=38,686,455,361, otherwise <=38,686,455,360.

If some vertex exceeds one layer cutoff, invoke that layer's existing favorable concentration theorem. Otherwise total mixed degree is at most
Dmix=273+1,001,088+38,686,455,360=38,687,456,721.

If nu_act active chains remain, every active vertex lies in a support edge and all edges have rank <=4, so |E|>=nu_act/4. A selected edge intersects at most 4Dmix-3 mixed edges. Hence a greedy maximal hypermatching has
|M| >= nu_act / 618,999,307,524.

Existing exact resolved-block DLS factors are
g2=440/441, g3=9236/9261, g4=193856/194481,
and g_r <= g2 <1. Disjoint supports therefore give
DLS ratio <= (440/441)^(nu_act/618,999,307,524).
At least a 1/309,499,653,762 fraction of active chains is covered.

ACTIVE-DENSITY COROLLARY: if nu_act >= delta*nu for any fixed delta>0, the declared mixed resolved subsystem receives exp(-Omega_delta(nu)) strict DLS gain. Thus within this model the only asymptotic way the resolved-core gain vanishes is nu_act/nu ->0.

NEXT TRACK B TARGET: classify the inactive-dominant case. Prove inactive chains are product/separable, locally pruned, or else some actual residual clause generates a resolved relation and contradicts inactivity. Then integrate with Liu Algorithm 4, corrected chain catalogue, and stopping/overshoot. No improved general 3-SAT base claimed yet.

TRACK A. New Sigma/QBF audits reinforce that challenge-count is not strategy complexity: affine response sets may have exponentially large hitting number but compact linear response circuits. Parent-size SAT/QBF compilation also retains coefficient >=1 on the unknown solver exponent. Therefore target compact solver-dependent response/commitment circuits acquired only through genuinely smaller encoded SAT calls, with hereditary charged reuse. This remains OPEN.

END_MIXEDRANK_CLOSE59_READBACK
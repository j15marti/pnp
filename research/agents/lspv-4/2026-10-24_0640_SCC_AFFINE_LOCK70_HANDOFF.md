# SCC-AFFINE-LOCK70: verified construction and five-role handoff

**P versus NP remains OPEN.** This is a source-specific counterexample to initial-parameter lower bounds, not a uniform all-decider lower-bound proof. No schedules, role prompts or other agents' files were changed.

## Exact SAT/UNSAT pair

For integer q>=1 and orientation string b in {0,1}^q, start with z_0,...,z_q. Add central variables a,beta,c,d and local u_i,v_i,w_i for every i=0,...,q. All binary clauses are Horn: (not a OR beta), (not beta OR a), and (not z_{i-1} OR z_i) if b_i=1, otherwise (not z_{i-1} OR not z_i).

Use a four-clause proper ternary XOR encoding Q(x,y,z;e) for every equation x XOR y XOR z=e. Central constraints: (a,c,z_0;1), (a,c,z_q;0), (a,d,z_0;1), (beta,c,d;0), (c,z_0,z_q;1). For every i, local constraints (z_i,u_i,v_i;0), (z_i,u_i,w_i;0), (u_i,v_i,w_i;0).

The exact ledger is n=4q+8, m2=q+2, k=12q+32, M=13q+34. In 4-word clause records with two header words and w=ceil(log2(64(17q+43))), N=(52q+138)w encoded bits. Changing one orientation changes only one signed consequent word.

The formula is UNSAT exactly when b=1^q; a first zero permits SAT. A satisfying original z-vector with z0=1,zq=0 extends uniquely via a=beta=c=d=0, u_i=0, v_i=w_i=z_i. No free auxiliaries for a fixed source vector.

## Specific independent-review requests for Role 5

1. Central XOR rank five and exact central solution beta=c=d=0, z0=1 XOR a, zq=a. The SCC equality a=beta is the single rank-increasing row and forces a=0.
2. Every local block uniquely enforces u_i=0 and v_i=w_i=z_i. Overall affine rank is 3q+8 and affine rank with SCC equality is 3q+9, leaving q-1 free original interior z bits.
3. The exact raw strong 2CNF backdoor h=q+3. An optimal set is {u_0,...,u_q,a,c}; prove minimality while accounting for central/local sharing at z0,zq.
4. SCC on the initial binary-only CNF is SAT and discovers a=beta, but ZERO genuine ternaries shorten, because none contains an SCC-equivalent pair. Affine-only CNF is SAT on both labels and does not force z endpoints.
5. After charged SCC-equivalence import, sparse Gaussian derives exactly q+11 forced variable values, reducing all k ternaries to width <=2. The final SCC returns SAT witness or UNSAT conflict without being supplied the label.
6. Check q=1 and q=1024 encoded field lengths, witness map and exact sign-word sensitivity.

## Roles 1-3: common hostile control

This example is stronger than the immediately prior Role 4 ADAPTIVE69 binary-unit-trigger family. It contains no original units or binary-only forced literals. It also differs from Role 2 QUIET-EQUIV67: initial SCC substitution alone shortens NO ternaries. Affine recognition plus one SCC rank row, and then a return to 2CNF, gives a linear-word decision on the whole matched-label family.

A candidate machine-universal lower bound based only on initial k=Theta(q), initial h=Theta(q), source residual, absence of binary units, or absence of immediate SCC shrinking is **FALSIFIED/RETIRED as an inference**. The only unconditional all-decider lower bound transported by this family is q=Omega(N/log N) word acquisition on b=1^q; direct source-aware recognition matches this order. It is not a post-acquisition time bound.

## Adaptive and static experiment

Both labels at q=1024 have n=4104, M=13346, k=12320, h=1027, N=1,121,106 bits; the verified adaptive run derives 1035 units and leaves zero ternaries. It counts 319,237 abstract events on UNSAT and 358,245 on SAT, including parsing, source reads, recognition, SCC, Gaussian, switching, restriction and witness replay. On q=8, a deliberately restricted static algorithm given an optimal h=11 backdoor and configured not to prune evaluates all 2048 branches at 1,738,752 events on both labels; the hybrid costs 3,261 (UNSAT) and 3,661 (SAT). This is only a finite-menu policy comparison. Fallback complete DPLL makes the hybrid exact on arbitrary CNF, with no general polynomial bound.

Checks: all 62 orientations q=1..5, exact backdoor minima q<=4, independent GF(2) rank, eight scaling sizes to q=1024 on both labels, seven hand-picked Horn/2SAT/XOR/padding/component controls, 120 independently exhaustively labeled small random CNFs (48 SAT,72 UNSAT), and 60 signed-permutation/ordering controls. Zero discrepancies. Full multi-mode Python auditor SHA-256: 61ee7906c3a4a66d00471445d18709a88548c1e860e5802c690656c424ad0911.

## Related work and next missing lemma

Role 4 COLLAPSE69 used a unit-propagation trigger; Role 2 QUIET-EQUIV67 used an SCC substitution that directly collapsed ternaries. An initial local-SCC-collapse variant of this run duplicated the latter and was retired. The present test creates a rank bridge rather than immediate syntactic shrinkage.

The next discriminating family should use genuinely non-affine coupling, then audit charged SCC/Horn/Gaussian/CDCL/caching/portfolio/direct recognition on both labels. A proof for every total uniform deterministic exact SAT decider remains OPEN.

## Published files

Report: research/agents/lspv-4/2026-10-24_0640_LSPV-4_SCC_AFFINE_LOCK70.tex

Compact independent reproducer: research/agents/lspv-4/2026-10-24_0640_SCC_AFFINE_LOCK70_MINI.py

Raw-results summary: research/agents/lspv-4/2026-10-24_0640_SCC_AFFINE_LOCK70_RAW.json

Bibliography: research/agents/lspv-4/2026-10-24_0640_SCC_AFFINE_LOCK70.bib

The full auditor, all detailed JSON files and longer report are in the user-delivered package, which is not assumed present in other agents' isolated runtimes. Peer reading/independent review is NOT yet confirmed. Publication readback and root ownership reconciliation must be checked independently.

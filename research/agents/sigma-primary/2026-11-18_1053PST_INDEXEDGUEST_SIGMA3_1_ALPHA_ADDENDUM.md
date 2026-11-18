# INDEXEDGUEST-SIGMA3-1 | Unknown-K input-expansion firewall
Date: November 18, 2026, 10:53 PST. P versus NP OPEN.

**New elementary necessary condition for the reached padded-guest architecture.**
Suppose an arbitrary n-bit ordinary Circuit-SAT source is converted to a tagged source of physical length N=n^(alpha+o(1)), and a compiler on some input is obliged to run an arbitrary correct Circuit-SAT algorithm A_D on a physical ordinary Circuit-SAT guest of size m=N^(lambda+o(1)). Here A_D may be a legitimate correct SAT decider that deliberately performs Theta(m^D) steps on every guest before returning. The parameter D is an arbitrary fixed time exponent.

The guest call alone costs n^(alpha*lambda*D+o(1)). To guarantee the requested upper exponent max(11/10,3/5+D/2) uniformly for arbitrarily large fixed D, it is therefore NECESSARY that

alpha * lambda <= 1/2.

For the INDEXEDGUEST lambda=1/2 architecture, this forces alpha<=1. Any constant expansion exponent alpha>1 eventually defeats the desired K-recurrence when such a padded call is reached. This is NOT a lower bound against other code-aware transformations that avoid the padded call or choose smaller lambda; it is a quantitative firewall for the specified guest-call implementation only.

Finite example D=3, lambda=.5: target exponent=2.1. If alpha=1.5, the reached padded call alone costs exponent 2.25 (>2.1). The *full upper ledger* alpha*max(1,.02+1.5)=2.28, also outside target. For the complete N-ledger bound 1.52, alpha<=2.1/1.52=105/76 is necessary to retain that particular advertised bound; this latter condition on an upper ledger is not an impossibility proof for other implementations.

The recurrence against an unknown K makes strict near-linear n-to-N size preservation a substantive proof obligation, not merely a convenient optimization. This is a restriction on input expansion and ordinary SAT guest calls, not a general circuit lower bound.

Status: exact algebraic accounting lemma, not P != NP. Parent-guest reachability, arbitrary input representation, hereditary ordinary Circuit-SAT closure and FLMV same-machine transfer remain OPEN.

VERIFICATION_SENTINEL_INDEXEDGUEST_ALPHA_20261118_1053PST
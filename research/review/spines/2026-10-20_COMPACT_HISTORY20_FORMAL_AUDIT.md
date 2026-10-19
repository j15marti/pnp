# COMPACT-HISTORY20: exact black-box history lower bound, explicit-circuit firewall
Date 2026-10-20. Independently checked finite audit. **P vs NP OPEN**. This is not a new unrestricted time lower bound.

## Relationship to COMPACT WITNESS BRIDGE
Earlier supplied note constructs diagonal language D with superpolynomial clock tau(n)=(n+2)^g(n), g(n)=max(1,floor(log2(log2(n+4)))). Conditional on a tau(n)^o(1)-size *one common assignment circuit* W for the locally specified correct-outcome computation CNF on suitably long self-padded YES inputs, P=NP implies Sigma2^P=P, permitting polynomial-cost-for-unary-s bounded search for W. A fixed resulting decider q would run faster than tau on its self-padded inputs, contradicting the diagonal rule. The compactness hypothesis remains OPEN. The source circuit and all simulated oracle/model costs must be charged.

## Theorem 1: black-box iteration
For integers t>=1, m>=t+1, let f:[m]->[m] be an unknown arbitrary deterministic function, accessible only by value queries f(v). Computing f^t(0) exactly for every f requires **exactly t deterministic worst-case queries**.

Upper bound: query successive states. Lower bound: adversary maintains an injective acyclic partial function, answering each query with a state whose outgoing edge has not been queried, avoiding premature closure of the chain from 0. At most t-1 distinct query addresses are learned. Let v_r be the first state on the induced forward path with unknown outgoing edge; r<t. At least two states have unknown outgoing edges. Complete the oracle two ways, setting f(v_r) to distinct such states a or b and fixing each chosen state thereafter. Both completions agree with the entire transcript but produce different time-t endpoints. Thus no algorithm with fewer than t queries succeeds on both. The m>=t+1 hypothesis provides two free continuation choices. **This is a query theorem for arbitrary unknown functions, not a bound for explicitly given circuits.**

## Theorem 2: nonuniform circuit-size control
Let m=4t. A time-index circuit W with binary time input 0<=i<=t and ceil(log2 m)-bit output must return f^i(0). W may be chosen separately after seeing the complete table f, can hardwire data, but has only ordinary fanin-two Boolean gates (no oracle gates). For sufficiently large t, some f requires **Omega(t) gates**.

Proof: At least (m-1)_t >= (3t)^t distinct injective paths starting at 0 can be realized by f. Each path demands a different time-indexed output vector. The number of s-gate finite-basis circuits with k=ceil(log2(t+1)) inputs and ell=ceil(log2 m) outputs is at most sum_{j<=s} 16^j (j+k)^(2j+ell), whose logarithm is O((s+ell)log(s+k)). For sufficiently small absolute c, s<=ct gives fewer circuits than paths. Some path requires more than ct gates. The full transition truth-table encoding costs Theta(t log t) bits, so this Omega(t) bound is NOT superpolynomial in encoded input length, nor does it establish the corresponding property for a compact transition circuit.

## Counterexample / shortcut
Explicit transition f(v)=(v+1) mod m has a poly(log m)-size circuit and f^t(0)=t mod m computable in poly(log m+log t) bit operations, bypassing t sequential oracle queries. A short program for a long trajectory can still take t steps to evaluate state t. Do not conflate source code, trajectory circuit size, single endpoint, or one circuit W for all indexed clauses.

## Conditional relativization firewall
Baker-Gill-Solovay supply recursive O with P^O=NP^O. The diagonal self-input contradiction applies to oracle programs. If the local succinct clause encoding and verifier can be relativized uniformly, and a universal oracle compactness statement guaranteed tau(n)^o(1)-size oracle assignment circuits on every relevant self-padded YES input, then P^O=NP^O would collapse Sigma2^{P,O} and yield the forbidden fast self-decider, contradiction. Therefore under those matched relativizing conventions the compactness theorem cannot hold for all oracles. A successful ordinary-world proof needs a genuinely nonrelativizing property of its explicit computation representation.

## Exact executed audit
Independent Python minimax over partial oracle maps enumerated all states in ([m] union {*} )^m for m=3,4,5, up to 6^5=7,776 states. Every 1<=t<m yielded exact optimal worst-case depth t, matching the theorem. Finite cases test definitions and the implementation, not the unbounded proof. Local PDF/TeX and code are in this conversation's COMPACT_HISTORY20 bundle; use independent expert review before any stronger claim.

## Programmatic research handoff
Read governance/2026-10-20_COMPACT_HISTORY20_ADDENDUM.md and retain only two active priority tracks, MCSP/MKTP and ARC/FLMV. :00 audit ordinary-KT proof-of-work vs oracle behavior; :12 analyze Sigma2 search with unknown verifier exponent and T-provably correct portfolios; :24 charge compressed tableaux against same-realization FLMV resource ledger; :36 falsify witness size, relative-oracle and nonuniform hardwiring claims; :48 reconcile exact proof DAG. Each run PROPOSE ideas -> SEARCH primary sources -> BUILD/test one lemma. Do not elevate communication / oracle / counting lower bounds into SAT runtime. 

## References
[1] Ponzio, Radhakrishnan, Venkatesh, *The Communication Complexity of Pointer Chasing*, JCSS 62(2), 2001, doi:10.1006/jcss.2000.1731 (different communication model).
[2] Fischer, Oshman, Rosen, Roth, *Pointer Chasing with Unlimited Interaction*, TCS 1083:116134, 2026, doi:10.1016/j.tcs.2026.116134 (different model).
[3] Papadimitriou and Yannakakis, *A Note on Succinct Representations of Graphs*, Information and Control 71(3), 1986, doi:10.1016/S0019-9958(86)80009-2.
[4] Jahanjou, Miles, Viola, *Local Reduction*, Information and Computation 261, 2018, doi:10.1016/j.ic.2018.02.009.
[5] Baker, Gill, Solovay, *Relativizations of the P=?NP Question*, SICOMP 4(4), 1975, doi:10.1137/0204037.

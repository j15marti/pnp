# MAGRED-TAPEFUSION3 | 2026-10-18 13:40 KST

STATUS: PROVED/EXACT under specified compiler model, COMPUTATIONAL arithmetic controls, unrestricted MCSP threshold transport and P versus NP remain OPEN.

## IDEAS PROPOSED BEFORE LITERATURE
A. Audit whether composing a one-work-tape reduction with a one-work-tape target solver creates two independent work heads.
B. Introduce an explicit one-tape simulation exponent theta before transporting the N^1.99 MCSP lower bound.
C. Build a counterexample to the inference that near-full source-bit query coverage implies superlinear time.
D. Check oracle query lengths, randomization, and promise preservation.

## LITERATURE CHECK
Cheraghchi-Hirahara-Myrisiotis-Yoshida, STACS 2021, DOI 10.4230/LIPIcs.STACS.2021.23, use one two-way work tape plus a one-way input tape. Hennie-Stearns, JACM 1966, DOI 10.1145/321356.321362, give a generic quadratic one-tape simulation, whereas their faster O(T log T) simulation uses two tapes. Maass, STOC 1984, DOI 10.1145/800057.808706, provides quadratic one-tape simulation lower bounds in specified models. A specialized fusion may still be faster.

## CONSTRUCTION AND PROOF
Suppose the source bound is N^(1+g-o(1)), 0<g<1. A transducer outputs target length N'=N^(a+o(1)) in source time N^(b+o(1)). Target algorithm time is N'^(1+h+o(1)). If and ONLY if a model-matched composition theorem gives source time bounded by N^(theta*max(b,a*(1+h)+v)+o(1)), then its source lower bound can exclude target exponents h below

h_crit = (1+g)/(theta*a)-1-v/a,

provided theta*b<1+g and h_crit>0. Here v is replay, target access, or materialization exponent and theta is a certified one-work-tape fusion penalty. Proof: require each term under max to be strictly below 1+g, then rearrange.

For theta=2 and a>=1, h_crit <= (g-1)/2 < 0. Thus the generic square simulation cannot certify any positive target exponent margin from the published one-work-tape MCSP bound, including N^1.99. For a deterministic exact standalone two-sided reduction, prior LOSSY-PROBE-NOGO2 forces N-o(N) source-bit reads along the zero table, so b>=1 and theta=2 violates theta*b<1+g even for a<1. This is a no-go for the generic proof ledger, NOT for every special compiler.

Zero-transcript query upper: If s>=n, t=floor((s-n+1)/n), t<N, an exact deterministic MCSP[s] bit-query decision tree probes only N-t positions on the zero truth table. If all are zero, all completions have <=t positive entries, each represented by a point DNF of <=n+n*t-1<=s gates. Otherwise inspect the rest and use unlimited computation to decide exactly. Hence source-probe coverage cannot by itself provide a superlinear one-tape time lower bound.

## TESTS AND OUTCOME
Exact Python arithmetic tested 60 rational (g,a,theta) regimes: theta=2 has zero viable positive-excess transports. Exhaustive Boolean controls: 1,920 point-DNF identities. Literal two-head shuttling test shows q^2 travel for q=16,32,64,128,256; not a universal lower bound. Randomized reduction success 2/3 followed by independent solver success 2/3 guarantees only 4/9; amplify solver error to <=1/12 then whole composition (with repeated-call cost charged).

NEXT: ONE-TAPE-STREAM-FUSION1, a single one-way-input one-work-tape source implementation of a genuine threshold descent with verified theta sufficiently near 1, b/a/v costs, correct promises, and iterative slope gain. P versus NP remains OPEN.

END_OF_VERIFIED_REPORT::MAGRED::TAPEFUSION3::P_VS_NP_OPEN
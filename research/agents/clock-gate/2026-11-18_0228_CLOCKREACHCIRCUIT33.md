# CLOCKREACHCIRCUIT33: Quantitative circuit bottleneck for terminal-state streaming quotients

2026-11-18 02:28 PST. PROVED/EXACT restricted mathematical theorem; COMPUTATIONAL controls; independent review OPEN. P versus NP OPEN.

## Named dependency, scope, and four falsifiers

The unfinished end-to-end chain is authentic N=2^n source truth table -> fixed source-independent lossy stream -> YES-only short witnesses and universal NO exclusion -> uniform fixed-PH supplied-circuit verifier -> fully charged headerless one-way-input/one-work-tape compiler -> appropriate MCSP one-tape lower-bound transfer.

Predeclared tests: (A) small joint dyadic reachability circuits may produce globally consistent cheap source sections; falsifiers: inconsistent independently chosen leaf witnesses, incompatible midpoints, and omitted leaf transition cost. (B) cheap reachability alone may suffice; falsifier: high-advice two-state equality scanner with trivial reachability. (C) exact MCSP promise purity may force one of large state count, hard local transition, or hard joint reachability; falsifier: a pure counterexample avoiding these three. (D) PH-low output equality may imply PH-low interval reachability; prior CLOCKSTATEINVERSE21 already FALSIFIES this inference and is cited, not republished as new.

## Theorem DYADIC-REACHABILITY-CIRCUIT-SECTION33

Fix n>=1, N=2^n, a state set Q=[K] with start p0, an arbitrary source-independent total indexed transition delta_n(i,p,b), and terminal-only label H_n(f)=F_n(p_N), where p_{i+1}=delta_n(i,p_i,f_i) on the actual original N source bits. For every dyadic interval I(d,a)=[a2^(n-d),(a+1)2^(n-d)), define the *joint* predicate R_n(d,a,p,q)=1 iff SOME word on I carries p to q. Let w=max(1,ceil(log2 K)), let L_n be the Boolean circuit size of a single jointly defined R_n on the encoded block/state inputs, and U_n be the circuit size of the indexed local delta_n(i,p,0), including all w output bits. Invalid state/block encodings may be extended totally at charged circuit cost.

For EVERY reachable terminal q, there exists a single globally consistent source g_{n,q}, ending at q, with

    CC(g_{n,q}) <= C [ n K (L_n+w+1) + U_n + n^2+w ],

for a universal basis-dependent C. In particular H_n(g_{n,q})=H_n(f) for any original f ending at q.

Proof: For a reachable block with endpoints (p,q), select the *least* midpoint r for which R(left,p,r) AND R(right,r,q). Recurse consistently into each half. At length one select input bit 0 if delta(i,p,0)=q, else input bit 1. Feasibility guarantees one exists. By induction the entire reconstructed word follows the designated endpoints. To evaluate g at an arbitrary n-bit address i, follow its n dyadic ancestors, evaluate at most 2K copies of the joint R circuit at each level, select the first feasible midpoint with a priority encoder and retain the appropriate pair of endpoints. This costs O(nK(L_n+w+1)+n^2) gates; the final local transition and equality test cost O(U_n+w). All output bits come from the SAME recursively specified word. This is a nonuniform circuit existence proof, not an efficient uniform source inverter.

Consequently, if Y_s={f:CC(f)<=s}, NO_t={f:CC(f)>t}, s<=t, NO_t nonempty, and s exceeds the bound, then H_n(Y_s)=im(H_n), so the YES and NO target images intersect. Thus exact two-sided promise purity NECESSARILY entails

    n K (L_n+w+1)+U_n+n^2+w = Omega(s).

For K<=N^(kappa+o(1)), U_n<=N^(delta+o(1)) and s=N^beta, if max(kappa,delta)<beta, this forces L_n>=N^(beta-kappa-o(1)). This is a conditional circuit lower bound on the reachability function OF AN ASSUMED PURE QUOTIENT, NOT on arbitrary SAT or MCSP circuits.

Under P=NP, a jointly fixed-PH R with uniform polynomial state count/transition time gives poly(n) R circuits and saturation for s=N^beta. The qualitative collapse boundary was already established in project CLOCKSTATEINVERSE21; this report refines its quantitative nonuniform resource dependence and isolates the missing local-leaf guard. Joint PH target-image equality does NOT imply joint PH interval reachability.

## Hostile local-leaf counterexample

For ANY N-bit pattern h, use K=2 states good/dead. Dead absorbs both bits; good remains good at i iff the source bit equals h_i. Exactly the source h ends in good. For every NONEMPTY interval and every h, R is the constant relation

    good->good YES; good->dead YES;
    dead->good NO; dead->dead YES.

So L_n=O(1), while the one-bit good-to-good leaf witness is exactly h_i. Circuit counting guarantees the existence of nonuniform h with CC(h)=Omega(N/n). Consequently the local transition/leaf witness cost U_n cannot be omitted, even though interval reachability is trivial. This example contains N bits of nonuniform positional advice, and is NOT an efficiently uniform hard family. It also FAILS MCSP promise purity because the dead fiber contains both easy and hard original sources. It is a falsifier for the R-only lemma, not a construction for P != NP.

## Tests and provenance

Full executed CPython standard-library audit, seed 202611180228. Full-source SHA256 f4ef5d4ba1a70c8b9663385455fe47acf383b2af283d2ec510f7ec1003faee73; full raw SHA256 daa28b21d48273fcd38598cb1fd81cf4621a26bdb429bb0f4d87e4a7e5700a58. Evaluated 204 models, 44,736 authentic source cases, 11,532 independently calculated interval-reachability rows, 1,474 reconstructed endpoints and 17,136 reconstructed bits; also 3,248 pattern-checker interval invariants, 896 local bit witnesses and a deliberately invalid left-only midpoint choice. Zero failures. The independently executed COMPACT subset, published separately, passed 4,352 checks. The complete executed audit source, raw JSON, expanded proof and BibTeX are preserved in the local research bundle. No physical one-tape microstep simulation or measured asymptotic circuit complexity lower bound was executed. Overlapping counters are not summed into a fabricated unique assertion total.

## Ledger, gates, literature and scope

The theorem charges nK joint-reachability circuit copies, priority encoding, address routing, U_n transition circuit and final bit output in ONE nonuniform source-function circuit. A real machine must separately charge all N source reads, source authentication/EOF, index increments, work-tape head motion, state updates, output storage/serialization and the target decoder. A nonuniform circuit bound does NOT supply a uniform physical compiler. Extra source-bound provenance must reside in the counted state; unretained output and independently selected source-adaptive transition programs are excluded.

DISJ: NOT APPLICABLE; no rank-to-hardness inference. Relativization: RESTRICTED combinatorial lemma only, unrestricted separation OPEN. Simultaneous DTISP: FAIL/OPEN for an MCSP transfer, no promise-pure quotient or same-machine decoder. Deterministic configuration counting: PASS as upper-bound sanity, not a lower bound. Algebrization and Natural Proofs not bypassed. Prior Partial-MCSP O(mn), free-seed, hash, parity, affine/field, histogram, Chevalley-Warning, adaptive-probe, certificate, mixed-core and alternative-decoder guards remain.

Project: followed current END_TO_END_AGENT_MANUSCRIPTS, AGENTS.md, CODEX.md and pnp-research skill; recovered main LOSSY_PROMISE_CASCADE6, PARTIAL_SAMPLE_WEDGE7, PROMISE_CASCADE_FIXEDPOINT8, K_ELIMINATION_TRANSFER4, SOURCEQUERY_SYNTHESIS10, PUBLICSEED_PLOTKIN14; inspected CLOCKTRIANGULAR32 and CLOCKSTATEINVERSE21 and cross-agent issue #3. No TMR-owned manuscript/schedule touched. No local Git checkout/preflight available. Qualitative balanced-path inversion and PSPACE/PH caveat are explicitly prior work; the novel scoped component is the quantitative circuit accounting and leaf witness firewall.

Primary sources: Savitch, JCSS 1970, https://doi.org/10.1016/S0022-0000(70)80006-X ; Galperin and Wigderson, Information and Control 1983, https://doi.org/10.1016/S0019-9958(83)80004-7 ; Cheraghchi, Hirahara, Myrisiotis and Yoshida, STACS 2021, https://doi.org/10.4230/LIPIcs.STACS.2021.23 .

ONE NEXT: REACHABILITY-TO-PURITY-INTERFACE34. Construct or falsify a charged terminal-state quotient satisfying BOTH short YES-image witnesses and universal NO-image exclusion, with joint fixed-PH equality and a fully model-matched one-way-input one-work-tape compiler. High dyadic reachability complexity, alone, is not sufficient. P versus NP OPEN.
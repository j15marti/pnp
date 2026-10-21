# RP EARLY-AFFINE19 | 2026-10-22 02:36 Asia/Seoul
Proof status: ESTABLISHED RESTRICTED, not P=RP or P!=RP.

Uniform model: R(x,r) is an RP verifier whose source-visible polynomial-size branching program tests explicit affine systems A_v r=b_v over GF(2) on ONE original random tape r of polynomial length m. Truncate execution after k tests, forcing REJECT beyond k, obtaining D_k<=R pointwise. Let A_k count tapes accepted by D_k; U_k count tapes still unresolved.

**Lemma 19A (exact prefix count).** A_k,U_k are computable in 3^k poly(n,m,|R|) time and polynomial space: each path specifies positive affine systems and excluded affine systems; expand excluded systems by inclusion-exclusion, count each intersection using Gaussian elimination. Across all paths of a depth-k binary tree, sum of 2^(number of NO branches) is <=3^k. If A_k>0, m further conditional counts construct a genuine accepting primary tape. The decision YES when A_k>0; NO when A_k=0 and U_k<2^(m-1); UNKNOWN otherwise is always sound for RP. In particular every YES input with even one accepting path of <=O(log n) affine tests is in P for this restricted verifier family.

**Lemma 19B (universal hitting for early density).** If all YES inputs have A_k/2^m >= delta >=1/poly(n), and k=O(log n), then ||Fourier(D_k)||_1<=3^k (affine subspace indicator has norm <=1, its complement <=2). The finite-field trace small-bias multiset r_i(a,z)=Tr(a z^i) for (a,z) in GF(q)^2, q>=4m3^k/delta, has size O(m^2 9^k/delta^2), is verifier independent, and contains an original tape accepted by R on every YES input. All NO tapes reject.

**Hostile controls.** Sequential rank-one zero-test chain has polynomial worst-case depth but early accepted mass 15/16 by cutoff 4; each individual test is NOT globally rare. Original :12 DENSE-BYPASS14 has ANF degree n+1 but b=1 yields early accepted mass 1/2 at depth one. Conversely, sequential parity acceptance has density 1/2 but NO early leaf before depth m; dummy identical-child queries destroy shallow acceptance without changing the language. One global m-bit parity affine query accepts half tapes at depth one, but has no short positive coordinate certificate, distinguishing :12 POSITIVE-CERT17. Parsimonious gate traces preserve primary counts; independent sampling of g gate auxiliaries dilutes RP density by 2^-g.

**Executable local audit.** 260 random shared affine-DAG cases; 40,600 brute-forced tape outcomes; 3,541 GF2 systems; 65,536 explicit GF(256) seed pairs; 337,519 assertion-accounted checks, 0 failures. Sample: uniform accept 20/32, generator accept 40,832/65,536, maximum character bias 1/64, actual spectral norm 1.75. No executable or raw files committed in this handoff.

**Sources actually reviewed.** :12 POSITIVE-CERT17 blob 83935cd1; :12 DENSE-BYPASS14 blob 7d3cf314; parsimonious 3CNF47 blob 0c970fa9. Literature: Naor-Naor 1993 DOI 10.1137/0222053, Nisan-Wigderson 1994, Impagliazzo-Wigderson 1997. WRAPPER gate DAG and unpublished :12 remain unreviewed.

**OPEN arrow:** no uniform polynomial-time source-preserving compilation of arbitrary RP computations into a form with logarithmic-depth early affine acceptance. P=RP, P!=RP, P vs NP all remain OPEN. Next: load an original WRAPPER circuit and separate primary random wires from deterministic gate traces; measure early affine depth and dummy-padded bypass.

END EARLY-AFFINE19
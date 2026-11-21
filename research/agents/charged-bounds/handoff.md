# charged-bounds handoff
Updated 2026-11-21 10:59 PST, America/Los_Angeles.
Current [T5-ZERO-ATOM-MINENTROPY1](PNP_Charged_bounds_2026-11-21_105900_Zero_Atom_Minentropy.md).
Base1274ba70556d11dcea569a65b728ba256f5f6f07. Previous split-residue report preserved.

PROVED/EXACT, external review pending: for ANY distribution on valid N-bit strict-C instances with UNSAT mass p0, any fake of average conditional min-entropy >=k has Adv_B>=max(0,p0-2^-k) for B>=3N. Zero-test uses ell-1 OR plus NOT with ell3N; no SAT solver, source parser or quotient conversion. Indistinguishability epsilon<p0 requires k<=-log2(p0-epsilon). Balanced p0=1/2 allows at most1+o(1) bits for epsilon=o(1); this does NOT exclude one bit or Shannon pseudoentropy.

FALSIFIED/RETIRED specific full-multiplier pair: new unweighted B*_G, X uniform on K23+r isolates / K4+(r+1) isolates. v5+r,e6,E82+9v,n433+48v,m527+58v, exact N unchanged. Fake10*2^E*6R with R uniform v bits has entropy v, passes full multiplier and6, stays in alphabet, but zero advantage1/2-2^-v. r0:N25203,k5,adv15/32,budget75609. No unrestricted lower bound.

COMPUTATIONAL: experiments/t5_bounds_zero_atom1_20261121.py and results/raw/t5_bounds_zero_atom1_20261121.json;8160 fake values,1125 exact probability tables, two base graph color counts. No expanded T5 enumeration. Code hash0d8bd7bc0823c50c0779da1e674f79ad7252da1dda77c364922d254f5a6d2676. Construction c5d8802 full proof/code/raw recovered; source reduction remains scoped premise.

Correct-label fake control: zero onUNSAT, uniform positive6M multiples onSAT has Shannon v/2 but average-min<1; zero test passes, other tests unproved. Do not conflate entropy types or say all full-multiplier pairs fail. Same-execution cap ledger unchanged; no excluded exponent or decision separation.

ONE next dependency T5-SAT-SLICE-PAIR1, Bounds owner, Redteam review/Synthesis tracking: explicit positive-output full-multiplier pair on a specified SAT-supported distribution, with independently proved cap-sized indistinguishability or a small falsifier. Conditioning/sampling not free; SAT-only counting is not decision separation.
Fresh literature/official six-org searches with fallback and429 retry recorded. No TMR/preflight/LaTeX/schedule changes. External independent review pending. P versus NP OPEN.

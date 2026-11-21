# PNP Charged bounds | 2026-11-21 09:11:46 PST | T5-ORBIT-PSEUDOENTROPY1

**Status:** PROVED/EXACT for the orbit/divisibility and explicit fake-distribution falsifier; independent review PENDING. No general pseudoentropy lower bound. P versus NP OPEN.

## Exact claim and quantifiers
For every n>=3,m>=1 and every valid encoded strict symmetric C instance x with three distinct variable names per clause, let F_N(x)=Z(x), using the repository encoding 1^n 0 gamma(m+1) followed by m triples of w=ceil(log2(n+1)) bits; N=n+1+2 floor(log2(m+1))+1+3mw. Then F_N(x) is divisible by 10. For **every** distribution X_N supported on such valid inputs, set Y=F_N(X_N) and fake Ytilde=Y+1. Both are in the padded output alphabet {0,...,5^n}, and H(Ytilde|X_N)=0. A deterministic distinguisher D(x,z)=[z mod 10 !=0] has distinguishing advantage exactly 1 and needs no counting oracle. Consequently the particular +1 fake cannot satisfy epsilon-indistinguishability for any epsilon<1 even against polynomial-size nonuniform fan-in-two AND/OR/NOT circuits. The same holds for any fake with probability q of nonmultiples of ten: advantage q. This is a **necessary support filter**, not a hardness result.

## Proof
C is invariant under the ten maps g_{s,d}(v)=s+d v mod 5, s in Z5,d in {+1,-1}: its allowed unordered triples are {i,i+1,i+2} modulo 5, which rotation preserves and reflection maps to another such triple. Apply a map simultaneously to all variable values. Any nonidentity rotation fixes no domain element. A reflection fixes exactly one domain element. A satisfying assignment fixed by such a reflection would have all its variable values equal to that one fixed element, contradicting the distinct-value requirement of any one C-clause. Thus the group action is free on satisfying assignments; each orbit has size 10. Zero counts also satisfy the divisibility assertion.

Since m>=1, Z<=30*5^(n-3)<5^n, so Z+1 is in the declared count alphabet. True count pairs always have z mod 10=0 and fake pairs always have z mod 10=1. D therefore separates with advantage 1. The modular test on an ell=ceil(log2(5^n+1))-bit z can be implemented by a uniform O(ell)-gate bounded-fan-in circuit: scan high to low with ten constant states and transition r -> (2r+b) mod 10, each transition constant Boolean cost; ell=O(n)<=O(N). It does not inspect x. For general fake, its acceptance probability is exactly the mass outside 10Z, giving advantage q.

This establishes no positive conditional entropy gap for the deterministic +1 fake. A random fake may have large H(Ytilde|X), but it still fails indistinguishability if it leaks residue. Conditioning the fake on multiples of ten defeats THIS test and remains open against other tests.

## Resource ledger and cap
For one fixed correct deterministic sole-tape solver A and fixed K,a>=1 with T_A(N)<=K N^a, the baseline ceilings are S=O_A(N^a), physical CM=O_A(N^(2a)), self-contained minimum-description CM=O_A(N^(a+1)), and unrestricted count-circuit gates O_A(N^a log N). The distinguisher above instead has O(n) Boolean gates, O(log n) finite-state streaming work bits (or constant residue state plus input bit addressing), O(n) sequential time over its ell-bit z input, and no source parsing, queries, representation discovery, cache, switching, recomputation or access to x. Input z is supplied as a pair component, not generated for free by a counting solver. The pair generator's computation of Y is NOT claimed cheap. This is a distributional indistinguishability falsifier, not an algorithm for producing the fake pairs efficiently. All input, output, addresses and comparison costs are explicit. No lower bound exceeds any cap ceiling.

## Falsifiers and controls
1. A valid C-clause satisfying assignment stabilized by a nonidentity dihedral element would refute freeness.
2. A valid m>=1 encoded instance whose count is not divisible by ten would refute the claim.
3. A purported counterexample using ordered R without the C-to-R two-clause conversion is out of scope.
4. A fake supported entirely on multiples of ten defeats this particular distinguisher and blocks generalization.

Controls: empty clause lists excluded; UNSAT count zero allowed; connected/shared-variable, affine/Tseitin, complement, private-leaf tree, forced-domain, relocation, caching and algebraic shortcuts do not affect the group action. DISJ: no direct-sum inference; PASS. Relativization: no oracle lower-bound inference; NOT APPLICABLE. Simultaneous DTISP: no time-space separation; NOT APPLICABLE. Deterministic configuration counting: compatible, no lower-bound inference; PASS. Natural Proofs/algebrization: no unrestricted circuit lower bound; NOT APPLICABLE.

## Literature search and scope
Queries (fresh this run): 'Vadhan Zheng characterizing pseudoentropy conditional pseudoentropy STOC 2012 full version'; 'Pippenger Fischer relations among complexity measures 1979 circuits time simulation'. Primary: Vadhan and Zheng, STOC 2012 / ECCC TR11-141 (https://salil.seas.harvard.edu/publications/characterizing-pseudoentropy-and-simplifying-pseudorandom-generator-constructions), conditional pseudoentropy; its stated sampling equivalence uses polynomial-size output alphabet and is NOT imported for exponential-range T5 counts. Pippenger and Fischer, JACM 1979 (https://scholarship.claremont.edu/hmc_fac_pub/597/), O(T log T) network simulation; cited only for the baseline cap. The orbit proof is self-contained, not imported.

Official GitHub repository discovery queries: 'org:anthropics theorem', 'org:openai formal', 'org:xai-org grok', 'org:google-deepmind theorem', 'org:google-research sat'. Connector search returned sparse/empty repository metadata and no inspected commit; no theorem or code imported, and official ownership/commit verification was not possible from returned fields. Do not infer negative search completeness.

## Evidence and execution
Symbolic proof above, no experimental code required. No finite experiment, local checkout, preflight or manuscript build executed. No TMR manuscript ownership. Previous Bounds parity restriction is distinct and remains valid only within its stated scope. Recent Construction 3COL private-leaf and Synthesis terminal-defect issue #324 reports are compatible but not imported as proof.

**ONE next dependency (Bounds):** T5-ORBIT-QUOTIENT-PSEUDOENTROPY2: investigate fake normalized counts Wtilde in {0,...,floor(5^n/10)} with Ytilde=10 Wtilde, proving or falsifying a nontrivial indistinguishability/entropy gap against a stated polynomial circuit budget; audit further efficiently computable count congruences before asserting pseudoentropy.

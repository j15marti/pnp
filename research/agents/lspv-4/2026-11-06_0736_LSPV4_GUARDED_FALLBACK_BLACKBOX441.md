# LSPV-4/441: Guarded SAT fast paths do not contract a full-length black-box fallback

**2026-11-06 07:36 PST. Route A primary. CONDITIONAL/PROVED-RESTRICTED plus COMPUTATIONAL. P versus NP OPEN.**

## IDEA, falsifiers, revision

Hypothesis: LSPV-4/440's correct source-authenticated Hamiltonian Tseitin parity shortcut cannot be promoted to an ALL-INPUT FLMV contraction by simply invoking the original unmodified polynomial SAT guest on every source outside its narrow language. Four falsifiers: (1) the wrapper has no infinite fallback input sequence; (2) the fallback already generates genuinely shorter guest inputs; (3) the compiler inspects and rewrites guest code, deleting artificial padding; (4) nominal child calls are cached, shared or omitted by legal short-circuiting. The theorem below assumes none of these escapes is present.

The search changed the focus. LSPV-2/438 and LSPV-4/440 already note qualitative non-contraction of unchanged fallback, and LSPV-2/441 already supplies a stronger standard-logspace source-only Tseitin recognizer. The present increment formalizes the **for every polynomial SAT decider** quantifier using padded deciders, derives a necessary black-box guest-length exponent, and tests canonical source permutation controls.

## Established family and exact original 3-CNF

Use the **unchanged** LSPV-4/440 binary source language: even H vertices in a cubic Hamiltonian graph, Hamilton-cycle edge IDs 1,...,H and matching edge ID H+1+uH+v for u<v. For each vertex with incident variables a_v,b_v,c_v and charge chi_v, the original strict three-CNF contains all four clauses

$$
C_{v,p,r}=\ell_p(a_v)\lor\ell_r(b_v)\lor\ell_{p\oplus r\oplus1\oplus\chi_v}(c_v),\quad p,r\in\{0,1\},
$$

where ell_0(z)=z and ell_1(z)=not z. The exact canonical packet length is

$$
N=12H(w+1)+H+w+12,\quad w=\lfloor\log_2(H^2)\rfloor+1.
$$

There are 4H original clauses and 3H/2 variables. For growing cubic expanders with odd charge, Urquhart's 1987 theorem gives exponential **ordinary shared-DAG Resolution** lower bounds. Hamiltonian random cubic expanders provide members of this language; this statement is not a certificate for our small instances. The authenticated global charge-XOR algorithm is a legitimate near-linear-time, logarithmic-workspace SAT/UNSAT shortcut. Resolution hardness does NOT transfer automatically to arbitrary SAT algorithms, Extended Resolution, GF(2), or the full historical mixed R_mix341.

## Theorem 441.1: original-length guest fallback (CONDITIONAL, PROVED/RESTRICTED)

Assume SAT in P. Let B be a fixed uniform total correct binary CNF SAT decider, including malformed inputs, running in O(n^b) time on the fixed indexed-input machine. For every integer d>max(2,b), construct a uniform total correct polynomial decider A_d that first executes n^d dummy counted transitions and then calls B on the original input. Thus the actual worst-case running-time exponent of A_d is d.

Consider a fixed black-box transformation Pi^A that applies a correct source recognizer and shortcut, but on at least one length-n input x_n for infinitely many n, runs the **unchanged supplied A on the same complete n-bit input** and returns its answer. Then on A_d,

$$
T_{\Pi^{A_d}}^{wc}(n)\ge n^d,\qquad t'\ge d.
$$

But for every d>6/5,

$$
d>\max(11/10,\;3/5+d/2).
$$

Therefore that guarded-full-length-fallback architecture **fails** the required Route A time contraction for these correct padded SAT deciders. This is conditional on SAT in P and restricted to the specified unchanged-guest fallback architecture. It is **not** a lower bound against all SAT solvers. A compiler that removes the padding, transforms all fallback inputs to genuinely shorter guest inputs, or never makes an original-length call is outside this result.

## Theorem 441.2: black-box guest-length necessity (CONDITIONAL, PROVED/RESTRICTED)

Consider a uniform oracle-style compiler whose guest query geometry depends on input and previous SAT/UNSAT answers, not on the guest program code or timing. Along an infinite input sequence, suppose it actually performs at least N^(mu-o(1)) sequential guest calls, each on an input of length at least N^(lambda-o(1)), with mu>=0 and lambda>0 independent of padded guest exponent d. Padded A_d returns the same labels as B, so it induces the same guest-call schedule. Each query costs at least its length to the d-th power. Consequently,

$$
t'\ge\mu+\lambda d.
$$

Demanding t'<=max(11/10,3/5+d/2) for **all arbitrarily large** padded d forces

$$
\boxed{\lambda\le1/2}.
$$

For mu=3/5, lambda=1/2 matches the desired guest-work exponent exactly, leaving zero automatic allowance for uncharged preprocessing, failed policies or join costs. This is necessary, not sufficient. Count **executed** calls, not nominal proof branches; common inputs may be cached and SAT OR search may short-circuit. For space, A_{d,s} can additionally touch and later erase n^s distinct work cells with d>max(b,s), s exceeding B's space exponent. An actual guest query of length N^lambda has peak space Omega(N^(lambda*s)), so the all-input space target s'<=max(1/2,s/2) again requires lambda<=1/2 for arbitrarily large polynomial s.

## Constructed original-source hostile control

The verified LSPV-4/440 Python generator and recognizer were reused with no grammar change. For each H=6,8,10,12,24,64,128 and two charge patterns, swap either the first two full signed clauses in the first quartet or one full signed clause across vertex groups. This changes the canonical packet but preserves the complete multiset of 3-CNF source clauses and its SAT/UNSAT truth value. The exact /440 packet recognizer returns OUTSIDE in all 28 cases. This is an intentional **canonical syntax** false negative, not a semantic SAT error; the permuted packet need not be a valid encoding under the separate global CNF grammar. Under a general CNF format that permits clause permutations the two presentations represent equivalent valid CNFs, so source normalization must not be treated as free.

Executed Python producer: 28 source/permutation pairs, 12 SAT and 16 UNSAT, 28/28 equivalent clause multisets and 28/28 OUTSIDE classifications. Independently authored Node.js referee: **25,242** assertions passed, including raw bit parsing, independent SHA-256, exhaustive small-instance SAT checks, corrupt-source rejection, 15 symbolic padded-time and 30 fanout-exponent controls. These are finite host tests, not native FLMV machine traces and not independent growing-family proof-size certificates.

## All-phase resource and proof accounting

Guard membership pays original-source reads and validation, all input/index/head operations, fixed-width parsing, source provenance, output and all-phase workspace. On fallback, guest simulation charges **all** transitions, guest work-tape high-water, parsing, failed policies, conversions, buffers, caches, retrieval, replay and recomputation. An n^s-sized scratch allocation still charges peak n^s after it is erased. Explicitly storing q children of length L simultaneously costs Omega(qL) bits; streaming can avoid this particular space peak but not guest query time or output. Retain the full envelope s'<=max(rho,eta,lambda,lambda*s), with rho covering every local phase.

No split/discharge/weakening or GF(2) rule has been added to historical R_mix341. For an UNSAT proof by split, **both** cases are AND obligations unless a different legal proof avoids the split. Shared DAG inference nodes count once, while physical storage and replay are separately charged; proof-minimum work is not guest time, and work/span/space remain distinct. This result is not a mixed-calculus lower bound or noncircular B3.

Independent numerical check: beta(6/5)=23/45, gap beta(6/5)-1/2=1/90; threshold beta(c)=1/2 is c=1.2055694304005903... . Finite entry follows **conditionally** from the hypothesized exponent recurrence, not from a constructed universal compiler.

## Source authentication and exact audit

Project: governing handoff 2026-11-02 at historical commit 4e29ed7646f484707767acb6e63ec5f38afd98a8, blob 033b54b8; current issue #3, 1074 comments at read; AGENTS.md 19656af1; CODEX.md 754999f5; pnp-research skill b8df83a7; LSPV-2/439 b98d6e84, /441 1ca86432; LSPV-4/440 515f20fb; LSPV-5 REFEREE387 06c7e1db; GROKPROOF/2026-11-06_1220_PROGRESS.md 5c4fbf8f; Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex 1f9fc727.

Required outside repositories: konard/p-vs-np/proofs/complexity/README.md blob 7ee9a11e (one-tape model, not FLMV); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md 18d693ea and CERTIFIED_RESIDUAL_QUOTIENT_REPORT.md b37da20a (incomplete residual quotient with UNKNOWN outcomes); MassimoLauria/cnfgen/cnfgen/families/tseitin.py 4bb5fd19 (standard source generator); meelgroup/frat-xor/README.md 38a137bc (XLRUP checked proof elaboration, not mixed calculus); openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean 1ced21f4 (a particular driver, not arbitrary guest). Read primary article pages for FLMV 2005, Reingold 2008, Robinson/Wormald 1992/1994 and Kolesnik/Wormald 2014. No Google-branded direct search or external code execution was claimed. No PDFs were analyzed.

Root main.tex fetched SHA 6a6a23494708a47ad856865c61131aeccd8e9ea3 but zero content bytes; therefore **unchanged**. Full repository preflight/CI not run: shell has no GitHub DNS and no complete repository checkout. Independent mathematical peer review pending.

Sources: Fortnow et al., JACM 2005 DOI 10.1145/1101821.1101822; Urquhart JACM 1987 DOI 10.1145/7531.8928; Ben-Sasson/Wigderson JACM 2001 DOI 10.1145/375827.375835; Robinson/Wormald RSA 1992 DOI 10.1002/rsa.3240030202; Kolesnik/Wormald SIAM JDM 2014 DOI 10.1137/120891265; Reingold JACM 2008 DOI 10.1145/1391289.1391291.

**Actual advance:** conditional quantified black-box fallback obstruction and lambda<=1/2 guest-length necessity, independently tested source-permutation controls. **Remaining gap:** an effective all-input, both-label malformed-aware recursively iterable SAT contraction with true guest-facing shorter inputs and fully charged same-machine construction, join and peak space. Route B full mixed minimum and noncircular B3 remain OPEN. **P versus NP OPEN.**
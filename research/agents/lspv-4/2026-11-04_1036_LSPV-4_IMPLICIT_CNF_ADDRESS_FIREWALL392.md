# LSPV-4/392: The lazy-CNF address and materialization firewall

November 4, 2026, 10:36 PST. **PROVED/EXACT within the declared virtual-input/index representation; independent specialist review pending. COMPUTATIONAL finite controls.** B1/B2/B3 and P versus NP OPEN. No changes to the fixed R_mix341 rules or weights.

## IDEA -> SEARCH -> ITERATE

**IDEA (before search):** LSPV-3/398 established that the nonaffine inner-product predicate $I_m=\bigoplus_{i=1}^m(a_i\land b_i)$ requires at least $2^m$ clauses in every explicit auxiliary-free CNF, despite $2m-1$ conservative circuit gates. Predict that its exponential *output* cost is avoidable by a lazy per-bit oracle, although a fully general binary guest address will exceed a sublinear live-space budget. Falsifiers: wrong SAT/UNSAT label; corrupted guard; source syntax error; illegal refutation pivot; arbitrary high-index bit query.

**SEARCH:** Cook and Reckhow (1979), Journal of Symbolic Logic 44:36-50, https://doi.org/10.2307/2273702 , explicitly discuss polynomial savings from iterated abbreviations. Haken (1985), *The Intractability of Resolution*, establishes the restricted ordinary Resolution PHP lower bound; Cook (1976) gives polynomial Extended Resolution PHP refutations. Derkinderen (2024), https://arxiv.org/abs/2407.17951 , discusses Tseitin circuit artifacts, an implementation comparison rather than a lower-bound theorem. Actual general web queries: "succinct representation CNF exponential size compared to circuits Tseitin transformation knowledge compilation implicit truth table input", "Cook Reckhow 1979 relative efficiency propositional proof systems proof complexity pdf", "Haken 1985 intractability resolution pigeonhole lower bound original theorem", "site:github.com/openai/math SubexponentialSAT". Direct Google-branded interface unavailable. OpenAI GitHub connector search "SAT proof checker LRAT Lean" returned no matches; no general B3 method identified.

Authenticated project review: research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md; issue #3; AGENTS.md and CODEX.md; project pnp-research SKILL; LSPV-2/341 (blob c87acd11), LSPV-3/398 (blob 9e4c9b95), LSPV-4/391 (blob a4b146f5). Grok review: GROKPROOF/2026-11-04_1518_PROGRESS.md (blob 4e2bb9d9). Claude: research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727), 2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (blob 9a5b05d6). Their restricted cost observations do not establish B3; LSPV-3 had already proved the erasure lower bound. This result does not claim its rediscovery.

**ITERATE:** Fix the entire virtual CNF grammar, indexed bit oracle, authenticated short Resolution path, and separate output and guest-address ledgers.

## Exact theorem and proof

For integer $m\ge1$, set
$$I_m(z)=\bigoplus_{i=1}^m(z_{2i-1}\land z_{2i}).$$
The virtual CNF $D_m$ has $4^m$ ordered width-$2m$ clause slots, indexed by each $z\in\{0,1\}^{2m}$. When $I_m(z)=0$, slot $z$ is the clause $C_z$ blocking exactly assignment $z$. When $I_m(z)=1$, slot $z$ is a fixed tautology with literals $x_1,\neg x_1$ and fixed padding. Consequently for every assignment $x$,
$$D_m(x)=I_m(x),$$
since every zero-input $x$ is rejected by slot $x$, while every one-input $x$ satisfies all blocking clauses and the tautologies.

Fix any explicit $2m$-bit guard vector $b$ through $2m$ unit clauses, giving $J_{m,b}$. It is SAT exactly when $I_m(b)=1$; then $b$ is its only model. The compressed record has $N=2m+O(\log(m+2))$ bytes/bits up to a fixed encoding constant and syntax overhead. With signed fixed-width literal IDs, $w=1+\lceil\log_2(2m+1)\rceil$, the *exact virtual bit-body length* is
$$L=(4^m+1)\,2m\,w=\Theta(4^m m\log(m+2)).$$

**(A) Lazy upper bound.** From query position $0\le p<L$ decode slot, literal, and bit offsets by binary arithmetic. Compute $I_m(z)$, return the requested signed literal bit. One uniform algorithm has per-query time $O(m^2)$ bit operations and peak scratch $O(m)$ bits on a conventional bit machine with charged binary address. It never writes the virtual body.

**(B) Explicit-output lower bound.** Any native machine that actually writes the $L$-bit body at $O(1)$ output bits per step needs $\Omega(L)$ steps. A streamed writer may use $O(m)$ counters; no exponential peak-space lower bound is asserted.

**(C) Guest-index limitation.** A *direct conventional* binary guest index capable of storing each address $p<L$ requires $\lceil\log_2 L\rceil=2m+\Theta(\log m)=\Theta(N)$ writable index bits. Therefore direct full-range indexed guest simulation on the compact representation does **not** meet $N^{1/2+o(1)}$ or $N^{1/5+o(1)}$ space. This does not claim that all algorithms must store such an address, nor prohibit nonstandard free-oracle addressing. The corrected all-phase space exponent must include preprocessing, source/index tape, guest simulation, failed conversions and retained parents in $\rho$.

**(D) Short sound proof.** If $I_m(b)=0$, source clause slot $C_b$ exists and is exactly the disjunction of literals contradicted by the $2m$ unit guards. Resolving once per unit derives the empty clause after $2m$ genuine binary Resolution inferences. Thus
$$W_{R_{\mathrm{mix341}}}(J_{m,b})\le 2m.$$
This is an exhibited **upper bound, not a certified minimum**. For odd $I_m(b)$ the formula has a model and no sound refutation. The short source-clause pointer requires $O(m)$ address bits; serializing $2m$ inference references takes polynomial bit output.

**Representation firewall.** The short generator record is NOT an ordinary explicit DIMACS source. A claimed general-CNF solver must authenticate all source clauses, including adversarially changed ones. Replacing such authentication with a trusted canonical generator silently changes the input promise/model; emitting the explicit CNF would restore the $\Omega(L)$ time cost. The compact family's direct uniform decision algorithm uses an $O(N)$ parsing pass and $O(\log N)$ working bits, but does NOT solve arbitrary CNF-SAT.

**XOR adjunct:** changing one unit from $(a_1,b_1)=(1,0)$ to $(1,1)$, with other AND pairs zero, flips UNSAT to SAT while changing just one aligned virtual unit sign bit. Its huge unchanged clause section supplies no necessary physical write lower bound. Conversely a materializer that rewrites the unchanged section still pays all output steps.

## Exact source and quantifiers of the hard-family starting point

Haken (1985) proves that for all large $h$, every ordinary **shared-DAG Resolution** proof of explicitly signed unary $PHP_{h+1}^{h}$ has $2^{\Omega(h)}$ lines. The family has $h(h+1)$ variables, $(h+1)+h\binom{h+1}{2}$ clauses and signed binary-index length $\Theta(h^3\log(h+2))$. This is a bound on Resolution proofs, NOT arbitrary correct uniform SAT algorithms, not GF(2), not Extended Resolution and not the stronger unchanged R_mix341. Cook (1976) polynomial Extended Resolution PHP proofs are mandatory countercontrols.

B1: $\forall A\exists p_A\forall F$ UNSAT, $W_R(F)\le p_A(|F|+T_A(F))$. B2: $\forall A\exists p_A\forall N$, $\overline W_R(N)\le p_A(N+T_A^{wc}(N))$ with worst case over *all* binary inputs. B3: $\mathrm{SAT}\in P\implies\overline W_R(N)=N^{O(1)}$ for the same preselected R. All are OPEN, along with a superpolynomial full-mixed minimum and P versus NP.

## Evidence and charge

Local expanded JavaScript producer: 73,180 assertions, 340 exact compact sources (155 SAT, 185 UNSAT), 69,904 assignment/source pairs, 2,735,992 virtual bit checks, 185 real 2m-step Resolution refutations comprising 1,350 charged inference nodes, 340 source-unit mutation tests, 9 malformed controls, and enormous-index spot checks at m=8,16,32,64. Independent Python brute-force referee checked 69,904 pairs. Separately published GitHub compact JS checks 72,954 conditions on 340 sources and 185 refutations. Expanded producer SHA256 8209933f965fc1f68dd82d72608918f6a5bf79adcd746f7b7caafeac21bf3581; independent Python SHA256 29c345747a4699ee3a491098330cc4454f3696f199a101560e880fca62dc9f54. Source/random-access bit upper bounds are symbolic, not native FLMV timing measurements.

The next missing link is a *fully authenticated*, all-input, same-machine lazy conversion/guest simulation for each actual R_mix341 inference that neither emits exponentially many bits nor stores forbidden long guest indexes. Even that would not automatically prove B3.

**Result status: PROVED/EXACT restricted, specialist review pending. B1/B2/B3 OPEN. P versus NP OPEN.**

# LSPV-3/445: four paid DEF facets admit polynomial prefix-port reconstruction by ordinary Resolution

**2026-11-06 03:31 PST | Route B | PROVED/RESTRICTED conditional on explicit FACET-4 grammar; COMPUTATIONAL independent finite replay.** P versus NP OPEN.

## Falsifiable hypothesis and scope

LSPV-3/444 showed that a fully inlined length-d address prefix has support d, so for d>=4 its exact relation cannot be introduced by one historical LOCAL-CONVERT restricted to three **original** variables. A different route may exist: an explicitly charged DEF node exposes four position-qualified forbidden-row clauses, and ordinary RES reconstructs all longer prefix ports. Falsifiers: (1) actual historical byte grammar forbids the owner/facet selector, still OPEN; (2) an implicit weakening, uncharged inference or illegal pivot is used, ruled out **within FACET-4**; (3) some derived long-prefix clause is incorrect, ruled out symbolically and by independently replayed finite controls; (4) charged work or explicit certificate length is superpolynomial in the size of the published bit-PHP source, ruled out for this construction. This is not an accepted historical R_mix341 proof, nor a full refutation.

## Exact family ledger

Cubic odd-charge Tseitin on a cubic expander has 3h/2 edge variables and 4h directly proper signed 3-clauses, ordinary shared-DAG Resolution lower bound 2^Omega(h) on suitable graphs (Urquhart 1987), and the known mixed AND3/GF(2) 4h-1 refutation from LSPV-2/341, which defeats transfer. Random 8n-clause proper signed 3-CNF (with replacement) has Chvátal-Szemerédi (1988) exponential Resolution hardness with high probability; Pang arXiv:2610.00837v2 reports stronger Res(PC_r/F_p) bounds but is a recent preprint and excludes arbitrary ER-style definitions. LSPV-3/443 obtains only linear all-binary-premise source-core work.

**Current control: Braun bit-PHP.** For n=2^ell holes and m=n+1 pigeons, use original binary address bits b_(i,t), and one clause for each pair i<j and address a:
$$
C_{ij,a}=\bigvee_{t=1}^{\ell}[b_{i,t}\ne a_t]\ \vee\ \bigvee_{t=1}^{\ell}[b_{j,t}\ne a_t].
$$
There are M=n*binom(n+1,2) clauses of width 2ell. Braun arXiv:2609.23015v2 (Oct. 22, 2026) reports a >exp(n/(32768 ell^2)) shared-DAG Res(XOR) lower bound for ell>=32 **without extension axioms**. The standard private-chain strict-3 encoding has M(2ell-2) clauses; equisatisfiability does not establish that the lower bound survives the conversion, and no such reverse simulation is claimed.

## Complete conditional port theorem

Define a separate **FACET-4** interface, whose one paid conservative Boolean owner y=p AND b makes four tagged forbidden-row clauses available to later *paid ordinary Resolution*:
$$
T_{00}=p\vee b\vee\neg y,\quad
T_{01}=p\vee\neg b\vee\neg y,\quad
T_{10}=\neg p\vee b\vee\neg y,\quad
T_{11}=\neg p\vee\neg b\vee y.
$$
Here p and b may be signed earlier input wires, and y is globally fresh. This represents exactly y=p AND b. One paid RES on b between T00,T01 derives A=(not y OR p); a second paid RES on p between T00,T10 derives B=(not y OR b); C=(y OR not p OR not b) is T11. The four owner facets are references to *one* paid DEF node, not four free source axioms. This four-facet selector itself is **not authenticated** in historical R_mix341.

For every prefix of length d, let signed originals l_1,...,l_d, y_1=l_1 and y_d=y_(d-1) AND l_d. Its exact full original-bit relation is equivalent to d+1 clauses:
$$
P_{d,i}=\neg y_d\vee l_i\quad (1\le i\le d),
\qquad Q_d=y_d\vee\neg l_1\vee\cdots\vee\neg l_d.
$$
At d=2, A,B,C are these clauses. For every d>=3 derive P_(d,i) for i<d by RES on y_(d-1) between A_d and P_(d-1,i), take P_(d,d)=B_d, and derive Q_d by RES on y_(d-1) between Q_(d-1) and C_d. Exactly d further paid RES nodes suffice per depth-d prefix. Every pivot is correctly oriented, each resolvent exact, and all output clauses follow solely from conservative definitions. No LOCAL-CONVERT, AND3 on fresh wires, case-split/discharge, weakening, source-relative implication oracle, or incompatible-branch lemma reuse occurs. Shared prefix outputs are charged once.

There are D=m(2n-4) paid owners, R_prefix=m(2n(ell-1)-8) additional prefix RES, and R_facet=2D normalization RES. Hence:
$$
\boxed{W_{\mathrm{FACET4}}^{\rm exhibited}=(n+1)(2n\ell+4n-20)=O(n^2\ell).}
$$
There are (n+1)(2n ell-4) exact exported prefix clauses. These are **paid upper-bound witnesses, not certified minima**. Explicit proofs with materialized wide clauses use O(n^2 ell^2 log(n ell)) bits apart from the original source; ideal weighted dependency depth at most ell+1 under unbounded parallelism. Actual machine search, generation, reading, storage, retrieval, serialization, verification and cache/peak-space costs are separate.

**Important source-scope limit:** Although each certificate is bound to the SHA-256 of its exact bit-PHP DIMACS input, no original source clause is an ancestor of these *conservative gate-definition consequences*. This certificate is **not an UNSAT refutation**, and cannot by itself establish an R_mix341 upper bound or B3. A complete proof needs valid original source inference and an authenticated historical facet interface.

## Independent verification

An independent Node verifier reconstructed the exact original signed bit-PHP bytes and source SHA, every owner/input/sign, all eight truth assignments of every 3-wire gate, every oriented binary RES, each exported port's full Boolean semantics over its original bit coordinates and both output labels, the acyclic forward ancestry, charges, and 10 deliberate corruption controls (all rejected). It also checked the ell=2 pigeonhole UNSAT condition over 4^5 address tuples.

| ell | Original clauses | DEF | RES | total paid | port clauses | JSON proof bytes | independent assertions / truth rows |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 40 | 20 | 40 | 60 | 60 | 10,305 | 849 / 1,344 |
| 3 | 288 | 108 | 432 | 540 | 396 | 78,162 | 6,344 / 2,304 |
| 4 | 2,176 | 476 | 2,448 | 2,924 | 2,108 | 445,726 | 36,184 / 15,232 |

Original SHA-256: ell=2 6334798ff59a2ced4187871bd9bc38d20829bd7c7b394596d189fa054aca4db7; ell=3 d9dfb9643b8ca83487ff83261fc01fb0c1b219e7b500e28413b2544156154c1a; ell=4 327c03a357abe18b1115d929da1e586a621fc19ee73c2b91b01b0b00ce05ee0b. Measured host producer wall/RSS: 0.82 seconds/99,976 KiB; independent verifier: 0.13 seconds/49,120 KiB. These are observations, not same-machine FLMV exponents.

## Idea -> search -> iteration and exact obstacle

Reviewed current project issue #3, governing five-role handoff, native /341 (blob c87acd11), LSPV-3/436 and /439-/444, LSPV-5/REFEREE383, recent LSPV-1 work, actual Grok and Claude source files, AGENTS/CODEX/research skill; both required repositories konard/p-vs-np (README blob 0e0ec77f) and blkph0x/p-vs-np-proof-research (METHOD_INDEX blob 18d693ea, proof portfolio bridge blob 22215cec); FRAT-XOR format blob 986a21aa, cake_xlrup, cake_lpr and openai/math README. Primary sources included Urquhart (1987), Chvátal-Szemerédi (1988), Braun (2026) and Pang (2026). General indexed web and GitHub queries were used; direct Google-branded search and a historical accepted-byte R_mix341 parser were unavailable. FRAT-XOR/XLRUP is a concrete alternative checked CNF/XOR provenance format, **not** evidence licensing our native DEF selector.

**Revision from /444:** high original support blocks one LOCAL inference, not a multi-step paid Resolution derivation. With owner-qualified four-facet references, there is a fully explicit polynomial expansion into exact original-coordinate clauses. The irreducible OPEN issue is whether the actual historical R_mix341 grammar permits those owner-to-RES references, and, independently, whether arbitrary mixed proofs can be normalized with polynomial overhead. No superpolynomial full-mixed Wbar lower bound and no noncircular B3 were proved. P versus NP OPEN.

**Reproducibility:** complete producer, independent verifier, raw typed traces for ell=2,3,4, full mathematical report, SHA-256 manifest, Linux resource logs and hostile checks in the role-owned downloadable reproducibility archive. GitHub files include this report, compact code and raw summary; the full 445,726-byte trace is archived separately. Root main.tex was not touched because authenticated fetch returned SHA 9685121992dad48c459079e4d91bb63831e2df76 with zero readable bytes. All existing five role assignments and schedules remain unchanged.

**References:** [1] Urquhart (1987), JACM, DOI 10.1145/7531.8928. [2] Chvátal & Szemerédi (1988), JACM, DOI 10.1145/48014.48016. [3] Braun (2026), arXiv:2609.23015v2. [4] Pang (2026), arXiv:2610.00837v2. [5] Project LSPV-2/341, LSPV-3/436 and /439-/444, LSPV-5/REFEREE383.

## Supplemental charge ledger and alternate facet presentation (03:35 PST)

The fully measured **implementation** is not the ideal free-choice minimum. Distinct phase upper bounds for the explicit construction, with $M=n\binom{n+1}{2}$ original width-$2\ell$ clauses, $D=(n+1)(2n-4)$ gate owners and $R=(n+1)(2n(\ell-1)-8)+2D$ paid RES nodes, are:

| Charged phase | Actual mechanism and bounded cost |
| --- | --- |
| Original input acquisition | The producer **generates**, rather than reads, the original canonical source in $O(M\ell\log(n\ell))$ character/ID operations; a future external-source reader must also pay input parsing and validation. Input SHA-256 is computed over every literal byte. |
| Signed owner creation | All $D$ fresh gate variables, input links, facet truth tables and owner IDs are allocated, verified and retained; $O(D\log(D+n\ell))$ identifier bits, aside from 4 constant-width facets per owner. |
| Port derivation | Exactly $R$ paid strict RES inferences, with per-inference actual set creation, literal comparisons, duplicate normalization, orientation checking, and a stored clause of width at most $\ell+1$. A conservative implementation bound is $O(R\ell\log(\ell+2))$ comparisons plus the identifier bit cost. |
| Saved proof and retrieval | Every output port, clause tuple, facet ID, owner reference and proof edge is retained, not magically discarded. Number of literal/ID entries $O(n^2\ell^2)$, each up to $O(\log(n\ell+n^2))$ bits. No duplicate shared inference is charged to the *logical work* measure, but each reference costs encoded bits and dictionary/map access on the machine. |
| Independent validation | Original source is regenerated and byte-compared; each gate has 8 truth rows, each RES has orientation and exact-clause checks; each prefix of length $d$ is checked for both labels on $2^d$ original bit assignments. Thus this exhaustive finite verifier alone incurs $O((n+1)\sum_{d=2}^{\ell} 2^d 2^d\,d)$ literal checks, potentially much greater than the charged $O(n^2\ell)$ logical work. |
| Output, failed checks, peak | JSON serialization writes **10,305 / 78,162 / 445,726 bytes** in the three fixtures, and ten independent forgery controls are intentionally run. The Linux *whole-process* peak, not merely retained proof nodes, was 99,976 KiB for production and 49,120 KiB for replay. Directory, connector, source/index/head and GitHub publication calls are external phases not included in either machine timing; no FLMV exponent is inferred from these incomplete end-to-end measurements. |

For comparison, an expressly declared **three-conventional-facet** owner model has $D=20/108/476$, prefix RES $0/216/1496$, and exhibited work $20/324/1972$ at $\ell=2,3,4$. Reconstructing those three facets from four truth-table facets costs exactly **$2D$ additional paid RES nodes**: $40/216/952$ respectively. Both representations are conditional; no historical byte accepted-selector or implicit reference-application weight was authenticated. Source-level semantic equivalence, paid extended-gate acceptance and native historical certificate acceptance must not be conflated.
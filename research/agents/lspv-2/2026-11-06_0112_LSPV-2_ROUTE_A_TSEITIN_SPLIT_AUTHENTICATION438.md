# LSPV-2/438: Exact Tseitin source authentication, deterministic streaming barrier and indexed repair

**2026-11-06 01:12 PST. Route A primary. PROVED/RESTRICTED; COMPUTATIONAL finite controls; every-A FLMV contraction and P versus NP OPEN.**

## Initial hypothesis and four falsifiers
Existing LSPV-2/435-437 and LSPV-4/434 exact Tseitin child ports assume authenticated source structure. Test whether a deterministic exact verifier of the *actual signed 3-CNF* requires a costly streaming message, and whether the FLMV indexed input model escapes that cost. F1: block charges are not independent; F2: membership does not require comparing blocks; F3: streaming lower bound incorrectly applies to indexed FLMV; F4: valid but non-template CNF is misclassified as malformed. F1-F2 are resolved by the encoding; F3 is a real model escape; F4 is addressed by an OUT_OF_FAMILY result, distinct from MALFORMED.

**Duplication check:** LSPV-2/425 (blob adb44cd7) and LSPV-4/421 (blob a3610cde) already prove deterministic multipass barriers using a separate set-intersection 3-CNF gadget. The following is an **established-family specialization and physical authenticated-source repair**, not a claim of a new communication-complexity method.

## Exact source, theorem, encoding and shortcut ledger
For a public connected simple cubic graph $G_H$ on $H$ vertices and $M=3H/2$ numbered edges, let $a_v<b_v<c_v$ be the incident edge IDs at vertex $v$. For charges $\chi_v\in\{0,1\}$ encode
$$
C_{v,p,r}(\chi)=\ell_p(x_{a_v})\lor\ell_r(x_{b_v})\lor\ell_{p\oplus r\oplus1\oplus\chi_v}(x_{c_v}),
\qquad \ell_0(x)=x,\;\ell_1(x)=\neg x,\quad (p,r)\in\{0,1\}^2.
$$
These are the four *original* parity-forbidding proper 3-clauses per vertex, without extension variables, for $4H$ clauses and $M$ variables. Encode first the two $p=0$ clauses for every $v$, then the two $p=1$ clauses; each literal is a $w=\lceil\log_2(M+1)\rceil$-bit ID followed by one polarity bit; prefix $1^H0$. Bit length:
$$
N_H=H+1+12H(w+1)=\Theta(H\log H).
$$
This is a special fixed-field source serialization, not the universal CNF parser. Clause reordering does not change the signed clause multiset, so ordinary Resolution proof sizes are identical in either order. For connected $G_H$, SAT iff $\bigoplus_v\chi_v=0$; odd charges are certified UNSAT. On suitable growing expander Tseitin instances, Urquhart (JACM 1987) and Ben-Sasson/Wigderson (JACM 2001) give $2^{\Omega(H)}$ **ordinary shared-DAG Resolution** size lower bounds. Do not transfer these to arbitrary algorithms, Extended Resolution, or historical mixed $R_{\rm mix341}$; its documented AND3/GF(2) parity shortcut is a mandatory upper control. Finite K4/cube/Petersen tests are not an expander-family lower-bound certificate.

## Theorem A (PROVED/RESTRICTED): exact membership is binary equality
Let $X_H(a,b)$ have first-block clauses charged by $a\in\{0,1\}^H$ and second-block clauses charged by $b\in\{0,1\}^H$. Every individual clause is proper signed 3-CNF. Then
$$
X_H(a,b)\in\{F_\chi:\chi\in\{0,1\}^H\}\quad\Longleftrightarrow\quad a=b.
$$
**Proof.** For each $(v,p,r)$, its third literal sign gives the unique charge $\chi_v=s_3\oplus p\oplus r\oplus1$. The two halves agree with one four-clause family template precisely when every $a_v=b_v$.

## Theorem B (PROVED/RESTRICTED): full-pass deterministic streaming barrier
A correct deterministic $p$-pass full left-to-right source-family recognizer, which may rewind only between full passes and retains at most $S$ bits of configuration (including caches and externally readable state) across the half boundary, satisfies
$$
(2p-1)S\ge H,\qquad T S\ge \tfrac12 N_HH=\Omega(N_H^2/\log N_H).
$$
**Proof.** Alice holds the first half encoded from $a$, Bob the second from $b$. Simulating $p$ passes sends at most $2p-1$ $S$-bit state messages and computes deterministic equality on $H$ bits. Its $2^H$ accepting pairs $(a,a)$ form a fooling set; distinct diagonal pairs cannot yield the same complete transcript since a crossed unequal pair would be accepted. Hence at least $H$ communicated bits. Complete scans cost $T\ge pN_H$.

The proposed local $T=N^{11/10+o(1)},S=N^{1/2+o(1)}$ pair is incompatible with **this streaming recognizer only**. The result concerns family-source authentication, not arbitrary SAT decision, and does not apply to indexed FLMV machines. This special case is conceptually subsumed by the earlier project streaming communication results.

## Theorem C (PROVED/RESTRICTED): indexed input authentication escape
Assume the public family $(H,v,j)\mapsto$ the $j$th incident edge ID is computable in polylogarithmic bit time using $O(\log N)$ writable bits. The actual FLMV indexed *read-only input* model can parse and check every signed literal, its ID and all four copies of every vertex charge, while retaining only $O(\log N)$ work/index bits. Every indexed address is constructed and its index tape erased; high-water counts the full highest work/index position. Thus source recognition uses $O(N\operatorname{polylog}N)$ time and $O(\log N)$ writable high-water, and emits IN_FAMILY_SAT or IN_FAMILY_UNSAT using global charge parity. Invalid encoded grammar is MALFORMED; a syntactically valid 3-CNF not matching the public template is OUT_OF_FAMILY, **not** MALFORMED. The input is not copied onto work tape. This upper bound assumes a *uniform public graph oracle* and does not establish one for an arbitrary expander family or graph supplied as part of the source. A universal SAT wrapper must correctly process OUT_OF_FAMILY through an independently bounded fallback.

## Computation and resource ledger
Full local Python producer: **4,207 checks**, **4,096** charge-pair cases on K4, cube, Petersen (256 exhaustive K4, 768 cube, 3,072 Petersen), with eight invalid controls, selected original-clause brute force, index read/write/erase counters. Separate independent Node verifier: **500 assertions**; standalone compact checker: **65,794** exhaustive K4/cube tests. Bit lengths 197, 489, 611. Host tests materialize sources and are **not native FLMV traces** or proof-size lower bounds.

The positive method uses a one-bit parity accumulator, a current charge, and $O(\log N)$ counters and head/index scratch, one output label, no guest calls, no materialized child formulas, and no retained branching DAG. Source authentication, index writing/erasing, family checking, lookup, and output are explicitly charged. If OUT_OF_FAMILY falls back unchanged to guest $A$, there is **no** claimed contraction; the all-input generator, shorter ordinary-CNF children, join, recursion and same-machine upper bound remain OPEN. No new $R_{\rm mix341}$ rule or weights, cross-branch lemma reuse or noncircular B3 is claimed.

## Sources actually read and continuity
Governing Nov 2 five-role handoff (blob c3889a3e), issue #3 through LSPV-1/440, AGENTS.md (19656af1), CODEX.md (754999f5), skill (b8df83a7); LSPV-2/425, /432, /437; LSPV-4/421, /423, /434; GROKPROOF/2026-11-06_0515_PROGRESS.md (93f9202); Claude 2026-10-28_1326_CLAUDE_TPORT-0001.tex (b7150bb). Repositories: konard/p-vs-np/proofs/complexity/README.md (7ee9a11, different one-tape machine); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693e) and AFFINE_BOUNDARY_DESIGN.md (ed4f4a9); MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd1); meelgroup/frat-xor/README.md (38a137b); openai/math/README.md (cc5b0a0); berkeley-abc/abc root tree. Primary: Urquhart 1987 DOI 10.1145/7531.8928; Ben-Sasson/Wigderson 2001 DOI 10.1145/375827.375835; FLMV JACM 2005 DOI 10.1145/1101821.1101822; Capponi ECCC TR03-075 deterministic communication tutorial. Indexed web and authenticated GitHub search used; Google-branded search unavailable. Source files are evidence, not authority to change proof models. Previous five-agent 2 Route A / 3 Route B allocation, task schedules and historical mixed calculus unchanged; root main.tex untouched without complete owner-region read.

**Advance:** precise hard-family source-authentication firewall and its charged indexed escape with correct malformed-versus-nonfamily classification. **OPEN:** every-total-polynomial-$A$ recursively iterable all-input $A\mapsto\Phi(A)$ with $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$; Route B's same-R B3; P versus NP.

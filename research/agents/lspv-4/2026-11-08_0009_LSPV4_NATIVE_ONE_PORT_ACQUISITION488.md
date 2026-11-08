# LSPV-4/488 | Native FLMV resource firewall for unconditional one-port projection acquisition

**November 8, 2026 00:09 PST | LSPV-4 Route A resource auditor | PROVED/RESTRICTED derived consequence + COMPUTATIONAL controls. P versus NP OPEN.**

**Affected chains:** [P2-A4] quantitative source-only port acquisition cost; [P2-A2] unrestricted compiler OPEN; [P2-A5] recursive closure OPEN; [P1-01], [P1-03], [P1-04] OPEN. Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN. Fixed historical R_mix341 grammar/weights untouched.

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis:** Even on a family of *guaranteed satisfiable*, proper strict-3CNF sources with one exposed Boolean port, no deterministic **solver-independent** routine can acquire the exact existential port table for every source within native FLMV time $O(M^{6/5})$ and peak space $O(M^{1/2})$. The reason is that port membership encodes unrestricted 3SAT. This is a quantitative FLMV audit of a previously known guarded clause split, not a novel NP-completeness gadget or an arbitrary-machine proof of P versus NP.

**Falsifiers specified first:** F1, the guarded source can be UNSAT; F2, projection when $z=0$ does not coincide with $F$ or the new source has nonproper clauses; F3, an input-indexed virtual generator incurs an $N^\alpha$ per-read cost or $\Omega(N)$ writable buffer, destroying quantitative transfer; F4, the FLMV threshold cannot be transported through the chosen exact proper-3CNF source encoding with only polylogarithmic exponent slack. F1/F2 have exact local proof and exhaustive controls; F3 has an explicit fixed-record virtual bit mapping, not native executed; F4 invokes the *standard locally computable quasilinear 3SAT reduction* as an explicit required encoding/simulation premise, rather than asserting equisatisfiability alone or treating an unknown encoding as free.

**Sources actually read:** both complete root trackers (initial proof1 blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; proof2 blob ad652f69558e3f87a6fcef02d2f9ba61e11117f7), current issue #3 and latest peer comments, Nov 2 five-role refocus historical commit 4e29ed7646f484707767acb6e63ec5f38afd98a8; AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md. Read LSPV-2/486, /485, /480; LSPV-3/481, /491; LSPV-4/460, /487; GROKPROOF/2026-11-08_0320_PROGRESS.md; Claude ONETAPE-0001. This exact guarded source equivalence was ALREADY proved by LSPV-3/481. The change here is its quantitative cost obstruction on the native time-space pair. No invented novelty.

**Primary literature:** Fortnow, Lipton, van Melkebeek, Viglas (2005), *Time-Space Lower Bounds for Satisfiability*, author PDF https://lance.fortnow.com/papers/files/tst.pdf, Sections 2.1 and 3.1, Theorem 3.1, Corollaries 3.2 and 5.8 (printed p.18 Cor. 5.8 inspected). Also Urquhart (1987) and Ben-Sasson/Wigderson (2001) for *ordinary shared-DAG Resolution*, not general computation. Public web search used, not a distinct Google-branded client. Actual external path/hash checks: konard/p-vs-np/scripts/proof_status.json 93b77ed3d8fe456f81c690035f45f07910a247f2 (no unrestricted result); blkph0x/p-vs-np-proof-research/projection_discovery_barrier.py 3ea94ff951916665e12dc8e0bb8221f4f5e49be5 (pre-existing GENERAL-CNF unit-port reduction), METHOD_INDEX.md 18d693ea71dfa433370eb7afbebc3106e32f03e5 and INDEPENDENT_AUDIT.md b30515cced93d8911a6415555ee9ec1444502d93; MassimoLauria/cnfgen/cnfgen/families/tseitin.py 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab; meelgroup/frat-xor/format.md 986a21aa92b62f844ef1fce852193142c41b2b1f (not R_mix341); openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean 1ced21f44ad49370d1b812e862c03c3a91d7f836 (specific execution costs, not generic projection).

## Exact proved source relation (previous LSPV-3/481, reused)

Take any source proper strict-3CNF $F(x)=\bigwedge_{j=1}^m(\ell_{j1}\vee\ell_{j2}\vee\ell_{j3})$, with three pairwise distinct original variable IDs per clause. Introduce fresh $z$ and pairwise distinct $a_j$, and output *actual original* proper strict-three clauses
$$
G(F,z,a)=\bigwedge_{j=1}^{m}
  [(\ell_{j1}\vee\ell_{j2}\vee a_j)
  \wedge(\neg a_j\vee\ell_{j3}\vee z)].
$$
There are exactly $2m$ original clauses and $n+m+1$ variable IDs. Clause-local existential elimination yields, pointwise for every $x,z$,
$$
\exists a\, G(F,z,a) \iff z\vee F(x).
$$
Therefore $G$ is ALWAYS SAT (set $z=1$), but its exact one-port existential relation is
$$
P_G(0)=\mathbf{1}[\mathrm{SAT}(F)],\qquad P_G(1)=1.
$$
A false claim of unconditional constant-time, constant-interface semantic projection would have hidden the entire original SAT decision in acquiring $P_G(0)$.

## Quantitative same-machine proposition (PROVED/RESTRICTED consequence of published FLMV)

For the usual indexable fixed-record proper-3CNF encoding, write $N=|F|$ and $M=|G(F)|$. With dense bounded numeric identifiers and binary self-delimiting headers,
$$
M=O(N\log(N+2)).
$$
Each requested guest bit of $G$ can be determined without materializing $G$: decode the guest header, identify $(j,\text{first/second clause},\text{literal field},\text{bit position})$, fetch the corresponding original source sign/ID bits through the FLMV INPUT INDEX, or generate the fresh auxiliary/guard field. A fixed source parser rejects malformed original records. Both have $O(\log N)$ WORK+INDEX and at most $O(\log^2 N)$ time per virtual bit; every index fill/erasure and head restoration is charged. This is a *symbolic bit-transducer construction*, not an executed native instruction trace. Different encodings require an independently charged conversion.

If a **stand-alone, source-only, uniform** deterministic routine computed $P_G(0)$ correctly for every authentic promised $G(F)$, with time $O(M^{6/5})$ and peak WORK+INDEX space $O(M^{1/2})$ on the same native FLMV machine, simulate it on virtual $G(F)$. Including malformed-source parsing, source-address construction and output, this decides $F$ in
$$
T(N)=N^{6/5+o(1)},\qquad S(N)=N^{1/2+o(1)}.
$$
Choose explicit exponents $c=601/500$ and $d=251/500$. Then
$$
\beta(c)=\frac{183168199}{361201000},
\quad\beta(c)-d=\frac{1845297}{361201000}>0.
$$
By FLMV Corollary 5.8, combined with its Section 3 source-encoding transfer and the standard locally-bit-computable quasilinear 3CNF encoding, these simultaneous uniform resource bounds are forbidden. **Thus such an unconditional resource-bounded exact one-port acquisition algorithm cannot exist.**

**Scope:** A quantitative lower bound on a PROMISE projection task under the stated source encoding and native machine. It does NOT prohibit using a hypothetical arbitrary polynomial SAT solver $A$ as a paid oracle/guest, semantic shortcuts on recognized easy families, a larger time or space budget, or any universally correct $A\mapsto\Phi(A)$ transformation. In particular the user-requested Route A contradiction and the all-input compiler remain OPEN. It gives no lower bound in R_mix341, even though its one-port interface is constant.

## FINITE verification and independent controls

Original signed proper 3-clause test corpus: all 256 subsets of the eight forbidden triples on three variables (255 SAT and 1 UNSAT). Python tested 2,048 original assignments, 4,096 $(x,z)$ projection conditions, 104,976 explicit auxiliary assignments, **33,786 virtual guest bit probes** agreeing with fully materialized authentic signed guest encodings, and 10 source malformed controls (five structural/five binary); all passed. Independent Node.js independently tested the 256 original signed sources, 4,096 projection conditions and 104,976 auxiliary assignments, including an adversarial flipped guard sign; all passed. Python and JS results are FINITE evidence only. No native FLMV emulator, third-party checker, or historical R_mix341 verifier was executed.

Source-bit, inference/work/span and full-resource ledger: virtual input conversion costs $O(\log^2N)$ time and $O(\log N)$ WORK+INDEX per guest bit; source recognition $O(N\operatorname{polylog}N)$ time and $O(\log N)$ writable; hypothesized Q time $O(M^{6/5})$ and simultaneous peak $O(M^{1/2})$, with exactly one Q call and no retained child array; no uncharged failures, caches or optimizer. The whole parent/child source is NOT allocated on WORK; its bits are regenerated. Clause output length, header and variable-ID arithmetic are included. No proof DAG, inference bits or shared lemma work claimed. The quantitative impossibility is for unconditional source-only Q, not for a concrete implementation passing an actual native trace.

## Established family / theorem / encoding / known-method / transfer ledger

**Odd-charge cubic-expander Tseitin:** H vertices, 4H original proper signed clauses, 3H/2 edge variables, encoded $N=\Theta(H\log H)$ for dense IDs; under established expansion conditions $2^{\Omega(H)}$ lower bound in ordinary shared-DAG Resolution (Urquhart; Ben-Sasson/Wigderson), *not* mixed R_mix341 or computational time. GF(2) charge sum is a genuine fast algorithmic shortcut. This remains a CONTROL for overgeneralization.

**Guarded strict-3CNF G(F):** 2m clauses, n+m+1 variables, guaranteed SAT; one-bit projected source decision is exactly SAT(F). Its intrinsic uniform time/space obstruction comes from the FLMV computation model plus indexed source reduction, NOT from preservation of any proof-size hardness. No reverse proof-size simulation asserted. The projection relation source is reused exactly from LSPV-3/481 and blkph0x's more permissive general-CNF variant. No novelty claim.

**Final:** Quantitative one-port acquisition cost firewall for the exact source-only architecture, independently verified finite semantics and source-bit mapping. Remaining gap [P2-A2]/[P2-A5] is an effective all-input recursively iterable solver-dependent A->Phi(A) with complete native machine accounting; [P2-B1]/[P2-B2] still OPEN. P versus NP OPEN.

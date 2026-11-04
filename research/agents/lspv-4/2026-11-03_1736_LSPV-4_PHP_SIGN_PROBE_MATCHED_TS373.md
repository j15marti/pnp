# LSPV-4/373: Unconditional Haken PHP machine-resource calibration

**November 3, 2026, 17:36 PST.** PROVED/EXACT in the specified indexed-input model, independent specialist review pending; COMPUTATIONAL for finite controls; B1/B2/B3 for fixed Rmix341 and P versus NP OPEN.

## Exact fixed systems and published theorem

Preserve **Rmix341** with free authenticated CNF source leaves, unit-cost distinct RES, bounded-support AND3, binary GF(2), justified LOCAL-CONVERT and conservative paid two-input DEF nodes, and shared logical proof DAGs. The theorem here concerns the **separate ordinary unrestricted DAG Resolution calculus Q** with derived RES nodes paid one each. It does not alter or lower-bound Rmix341.

Let P_h be canonical unary PHP for h+1 pigeons and h holes. It has v=h(h+1) variables, m=(h+1)+h binom(h+1,2) clauses and L=h(h+1)^2 literal occurrences. The signed ASCII encoding with an **explicit + or - character on every literal** (plus decimal variable IDs) has length N=Theta(h^3 log(h+2)). Haken (1985) proves: there exist c>0,h0 such that for every h>=h0 and **every unrestricted shared-DAG Resolution refutation** of P_h, the proof has at least 2^(c h) lines. Thus W_Q(P_h)>=2^(c h)-m. Cook (1976) provides polynomial Extended Resolution proofs of PHP, so neither arbitrary SAT machine hardness nor full Rmix341 hardness follows. Odd expander Tseitin formulas also have exponential ordinary Resolution complexity but an exact 4h-1 mixed proof by authenticated GF(2) (prior LSPV-2/341).

## PROVED/EXACT: same-input source-probe floor and low-space upper bound

Every correct deterministic total all-CNF SAT decider B, with a one-symbol random-access read-only input, must read **every** one of the L sign characters on canonical P_h:

$$
\forall B\,\forall h\ge1:\quad T_B(P_h)\ge L_h
=\Omega(N_h/\log(N_h+2)).
$$

For a sign in a positive pigeon clause, flip it and assign that pigeon no hole while bijecting the other h pigeons with the h holes. For a sign in a negative collision clause, flip it and assign that pair to the same hole while bijecting the remaining h-1 pigeons to the remaining holes. Each changed string is a valid SAT CNF of **identical length differing in exactly one sign character**. A deterministic decider skipping that position would produce the same transcript and wrong label on one of the two inputs. On a packed w-bit input-word model, the proven bound is ceil(L/w) distinct word probes.

Conversely, **one uniform, total, correct all-CNF decider A_stream** can recognize *every* canonical P_h by parsing its header, deriving h, and lazily generating and comparing the exact expected signed clause stream. It uses O(log N) simultaneously live writable counter/index bits and O(N log^2 N) bit-time, including source access, header calculation, complete sign checking and EOF. It rejects the recognized formulas by the pigeonhole principle. On any nonmatch it performs a separate complete strict parse and exhaustive assignment search, rejecting malformed binary strings. Thus

$$
T_{A_{stream}}(P_h)=O(N_h\log^2 N_h),
\qquad S_{A_{stream}}(P_h)=O(\log N_h).
$$

The fallback may be exponential in time and use linear or greater space, so **no worst-case global polynomial-time or small-space algorithm** is claimed. This is a restricted-language, same-input **near-tight all-algorithm input-probe bound** and a decisive counterexample to inferring exponential arbitrary machine time or space from Haken's exponential proof size.

For **ordinary Resolution Q**, B1 (the per-input arbitrary-decider bound) fails unconditionally because A_stream is fast on a family with exponentially large W_Q. It does **not** refute B1 for Rmix341, B2 for Q (whose T_A^wc includes all valid/malformed inputs), or any fixed-R B3. No free SAT oracle, nonuniform per-instance advice, or per-length algorithm is used.

## Falsifiers and status

F1, PROVED: Every PHP occurrence sign, not only every source clause, is individually opposite-label sensitive. F2, FALSIFIED as a transfer: Exponential unrestricted ordinary Resolution size forces exponential time/space for all uniform deciders on the same formula. F3, FALSIFIED as a promotion: Small-space recognized-family behavior gives a small-space worst-case algorithm; exhaustive fallback remains fully charged. F4, OPEN: A full mixed LOCAL-CONVERT/DEF proof-cost simulation and the weakest sufficient B3 bridge, with correctness and typed source verification.

## Evidence and physical ledger

Python producer: **374 assertions**, 70 independently signed one-character SAT flips, 34 source-deletion SAT witnesses, 12 malformed rejections (including non-ASCII), odd/even K4 parity with 0/8 models. Independent no-import JavaScript: **187 assertions**, independently exhaustively evaluating PHP h=1,2,3, all 70 sign flips and all 34 deletions; K4 counts 8/0. Additional successful exact expected-source comparisons for h=4,8,16,32 consumed 457,3118,25685,206432 source bytes, respectively. Host Python RSS roughly 100 MiB is **not** an indexed TM workspace bound.

Model costs: fully charged header parsing, symbol probes, index/head writes, lazy literal construction, validation, EOF and output; no dense relation or proof DAG is required on recognized inputs. Proof-node minima, encoded proof bits, optimizer discovery, physical proof construction/verification, source reads and peak writable space are separate. A materialized child must still satisfy the corrected s'<=max(rho,eta,lambda,lambda*s), with rho including every local phase. The recognized-family O(log N) peak is **not** a bound on all-input rho.

## Corpus, duplication, Grok/Claude, and next gap

Read November 2 12:04 five-role directive, issue #3, AGENTS.md, CODEX.md, pnp-research skill, original LSPV-2/341, LSPV-1/374 and /375, LSPV-2/375, LSPV-3/378-/379, Red Team/324, and LSPV-4/341, /345, /371, /372. **Nearest predecessor:** `research/agents/lspv-4/2026-11-02_1643_LSPV-4_BPHP_STREAM_TIME_SPACE_ATLAS345.md` (blob 8f596fa2) established a similar low-space recognizer for *bit*-PHP with a **2026 Res(oplus) preprint** lower-bound anchor. LSPV-4/341 already had a canonical PHP recognizer without this matched all-algorithm sign-probe versus low-space calibration. This run replaces that conditional model comparison with **unconditional Haken ordinary-Resolution hardness** and an explicit opposite-label source-sensitivity lower bound in the *same input encoding*. Academic novelty is not claimed.

Grok checked: `GROKPROOF/2026-11-04_0116_PROGRESS.md`, SHA ca5a8353. Its all-input arbitrary-decider FLMV contraction is OPEN. Claude checked: `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, SHA 9a5b05d6, and `2026-10-28_1452_CLAUDE_TPORT-0002.tex`, SHA 1f9fc727. These are sequential-input or alternation-trading restricted bounds, not B3. A github.com/openai proof-checker search found no grammar-matched fixed-R compiler; absence was not inferred. Primary literature: Haken 1985, Cook 1976, Cook-Reckhow 1979, Urquhart 1987, Buss 1987. Full checkout/preflight unavailable; root main.tex is not overwritten without complete authenticated readback.

**Next:** A source-rooted uniformly cost-reflecting invariant robust to *every* permitted mixed inference, plus an independently justified nonrelativizing B3 bridge. Superpolynomial Wbar_Rmix341 and P versus NP remain OPEN.

References: Haken, *The Intractability of Resolution*, TCS 39 (1985) 297-308, DOI 10.1016/0304-3975(85)90144-6; Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4) (1976) 28-32; Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44(1) (1979) 36-50; Urquhart, *Hard Examples for Resolution*, JACM 34(1) (1987) 209-219; Buss, *Polynomial Size Proofs of the Propositional Pigeonhole Principle*, JSL 52(4) (1987) 916-927.

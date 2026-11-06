# LSPV-4/452: bounded-edit one-pass state lower bound
**2026-11-06 15:45 PST | Route A primary | PROVED/RESTRICTED and COMPUTATIONAL | P versus NP OPEN**

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis:** LSPV-2/454's first-`k` moments, using `O(k log m)` bits, are nearly memory-optimal among deterministic, uniform, read-once recognizers on a stream of `m` authenticated clause IDs promised to be either an exact permutation or at most `k` omissions/duplications. Prespecified falsifiers: (F1) two distinct half-prefixes with one common suffix both give accepted permutations; (F2) a crossed prefix/suffix makes more than `k` replacements; (F3) an uncharged source header/machine state encodes the chosen prefix; (F4) a claim improperly extends to unrestricted malformed inputs or random-access/multipass machines. The proof excludes F1-F2, explicitly charges all streaming state for F3, and does not make the extensions in F4.

**Source-state reconciliation:** LSPV-4/451 corrected the previously false one-swap `Omega(m)` lower bound to `Theta(log m)`. LSPV-2/454, blob `7e2d916ad5e01eb9e7c89494ee804f7322a953a6`, obtained a first-`k` power-sum promised upper bound and general Prouhet collisions beyond the promise. The present contribution is the matching **general `k` lower bound**. Its fooling-set method is standard communication-complexity mathematics; no claim of precedence or novelty beyond this application is made.

## Certified 3-CNF family and exact encoding ledger

For connected simple cubic `G=(V,E)`, `H=|V|`, `|E|=3H/2`, Boolean edge variables and charges `chi_v`, let `a<b<c` be the incident edge IDs at vertex `v`. Its four **original proper signed 3-CNF clauses** are

$$
C_{v,p,q}=\ell_p(x_a)\vee\ell_q(x_b)\vee
\ell_{p\oplus q\oplus1\oplus\chi_v}(x_c),
\qquad p,q\in\{0,1\},\quad\ell_0(x)=x,\;\ell_1(x)=\neg x.
$$

These are `m=4H` distinct clauses, `12H` signed literals, and `N=Theta(H log H)=Theta(m log m)` binary source bits using fixed-width original edge IDs. Odd total charge is certified UNSAT; even charge SAT. The Urquhart 1987 and Ben-Sasson–Wigderson 2001 exponential hardness results concern suitable growing expander members **in ordinary shared-DAG Resolution only**. They do not establish hardness in ER, GF(2), full historical `R_mix341`, or against all algorithms. A connected-source GF(2) parity test is an efficient legal shortcut. Finite K4 and cube controls used here are not asymptotically hard families.

Assume an already authenticated indexed reference maps each original signed clause locally to one unique ID in `[m]`. **The cost of obtaining/authenticating this reference is not waived for universal SAT.** The verifier receives exactly `m` locally legitimate clause IDs in arbitrary order. It is promised that the sequence is either an exact permutation of `[m]`, or differs by `r` missing distinct IDs and `r` extra duplicate records, `1 <= r <= k`. The deterministic **read-once** machine has fixed uniform finite control and accounts for all retained work registers and head positions.

## Theorem 452.1, PROVED/RESTRICTED

For even `m >= 4` and `1 <= k <= m/2`, the worst-case number of retained state bits `S` of any such exact deterministic one-pass algorithm is at least

$$
\boxed{S(m,k)\ge\left\lceil\log_2\binom{m/2+k}{k}\right\rceil-O(1)
=\Omega\left(k\log\frac{m}{k}\right).}
$$

The fixed `O(1)` allows the control-state label to be held outside the work registers. If it is counted, the exact ceiling is the lower bound.

**Proof.** Put `h=m/2`, fix `A={1,...,h-k}`, and `P=[m] setminus A` so `|P|=h+k`. For each `k`-subset `U` of `P`, feed the same-length first-half prefix `A union U`, canonically ordered. There are exactly `binom(h+k,k)` such prefixes. Fix one `U`, and append the complement `[m] setminus (A union U)` as a common second-half suffix. Prefix `U` plus that suffix is a valid permutation. Any different prefix `V` plus the **same** suffix has exactly `r=k-|U intersect V|` missing IDs (`U setminus V`) and the same number of duplicates (`V setminus U`). Therefore `1 <= r <= k`, so it is a promised negative. Identical complete machine states after prefixes `U` and `V` would imply identical results on the common suffix, contradiction. All `binom(h+k,k)` prefix states are distinct. Counting states and applying `binom(h+k,k) >= ((h+k)/k)^k` proves the result. QED.

**Matching restricted upper bound:** The first `k` power sums `sum_i id_i^j mod p` for `j=1..k`, with an authenticated suitable prime `p>max(m,k)`, distinguish all promised negative streams by Newton identities. A trusted locally decodable source-ID reference and a prime with `log p = Theta(log m)` yield `O(k log m)` retained bit space. Thus for any fixed `epsilon>0`, the upper and lower bounds agree up to constants when `k<=m^(1-epsilon)`. Prime acquisition/certification, header verification, and fallback are additional real machine costs. The finite host program uses p=65537 only for m=16,32, retaining full lists; it is not a native FLMV machine.

**Out-of-promise falsifier:** Prouhet's even/odd digit-parity partition of `[2^(k+1)]` yields two sets of size `2^k` with identical power sums through `k`. Replacing one set by duplicates of the other passes all `k` moment tests despite being malformed. General input still needs an exact charged fallback. A stronger all-corruptions one-pass `Omega(m)` bound, properly qualified in LSPV-4/451, remains separate.

## Computational controls and resource audit

The local Python producer built actual signed original cubic-Tseitin formulas on K4 and the cube, with even and odd charge, and verified exact source SHA-256 signatures and SAT labels for K4 by brute force. For `(m,k)=(16,1..4),(32,1..3)`, it exhaustively or deterministically sampled crossing pairs from the fooling-set family and checked the number of replacements and the exact moment verifier. It included Prouhet false-acceptance controls for `k=1,2,3` outside the promise. Results: **383,841 Python assertions PASS; 5,832,920 independently implemented JavaScript assertions PASS.** This is finite computational validation, not native machine measurements, a proof certificate, or evidence for unrestricted SAT hardness.

| Resource | Promised one-pass ID check | Full Route A compiler still needed |
| --- | --- | --- |
| Native `R_mix341` nodes, evidence bits | 0 / 0 | Full accepted-rule grammar, bit charges, and any needed proof conversion |
| Source, reference, prime | Reference and prime conditional, not free universally | Authenticate all original bits, malformed and corrupted sources, all index/head reads |
| Input work | One scan, at least Omega(N) bit reads | Charge all input/source and child ports |
| Retained state | Lower Omega(k log(m/k)); conditional upper O(k log m) | All-phase peak including all temporary work |
| Child materialization / guest / join | None | Charge every child, guest, joining, cache, reference and recomputation |
| DAG work/span / machine time-space | Different measures | Do not infer runtime from weighted distinct-node proof costs |

For `k=N^delta`, `0<delta<1/10`, the restricted storage cost is `Theta(N^delta log N)`; conditional moment scan work is `O(N^(1+delta) polylog N)`. Neither supplies a universal all-input solver contraction or smaller guest formulas.

**OPEN:** The exact required Route A transform for every uniform total correct polynomial SAT decider, including malformed inputs and recursively iterable same-machine execution, must satisfy

$$
t'\le\max\left(\frac{11}{10},\frac35+\frac t2\right),
\qquad
s'\le\max\left(\frac12,\frac s2\right).
$$

No native `R_mix341` rule/weight, branching assumption or Route B B3 status changes. P versus NP OPEN.

## Literature, repositories, reproducibility limits

Read exact LSPV-4/451 report/handoff, LSPV-2/453 and /454, historical five-role refocus, current issue #3, AGENTS.md, CODEX.md, repository research skill, Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, and Grok `research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex`. Checked required `konard/p-vs-np/ISSUE_27_ANALYSIS.md` (blob `a58e3a10`) and `blkph0x/p-vs-np-proof-research/AFFINE_CANCELLATION_LITERATURE_SCOPE.md` (blob `c4b47e6a`); neither supplies the missing transfer. Also checked `meelgroup/frat-xor/README.md` (blob `38a137bc`), `peitl/short-proof/README.md` (blob `93d2090d`) and `openai/math/README.md` (blob `cc5b0a03`). Web searches checked the primary FLMV JACM 2005 DOI 10.1145/1101821.1101822, Urquhart 1987, Ben-Sasson/Wigderson 2001 and classical deterministic-streaming fooling sets (Best-Order Streaming Model, section 3.1; Chakrabarti/Kale FOCS 2016 ECCC TR16-111). No separately authenticated Google-branded search or formal proof assistant replay. Repository-root `main.tex` returned a SHA but zero readable content, so it was not edited. No schedules, identities or prior artifacts modified.

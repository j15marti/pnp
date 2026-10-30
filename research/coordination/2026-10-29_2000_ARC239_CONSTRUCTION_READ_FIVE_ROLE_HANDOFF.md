# ARC239 construction/read triple frontier, LSPV-1, 2026-10-29 20:00 PDT

Status: **PROVED/EXACT under restricted two-stage source-bit-probe assumptions**, independent referee review pending. Finite tests **COMPUTATIONAL**. General SAT and P versus NP remain **OPEN**.

## New claim

Let a source contain independent unary sign fields `a in GF(2)^b`. A fixed deterministic offline preprocessor reads at most `p` named original source bits, possibly adaptively, then retains precisely `L` source-dependent bits. For each later parity mask `w`, an exact deterministic online procedure may adaptively probe at most `Q` source sign fields. Original source retention is legal and its reads are counted.

1. For **every adaptive nonlinear preprocessor**, `p+Q >= b`. Strong same-source form: for each source input `a`, an adversarial future parity mask forces online access to every sign field not read on that input's offline transcript. The proof uses a free subcube and a one-bit flip adversary.
2. If, in addition, all offline source dependence comes from a **public fixed set of `p` named fields**, write `u=b-p`, `q=Q-u`. Every arbitrary nonlinear L-bit encoder and adaptive exact online decoder satisfies `Q>=u` and `2^L * sum_{j=0}^q binom(p,j) >= 2^p`. This combines a forced-unread-coordinate lemma with ARC238's Fourier-dimension result. **Do not transfer this sharper inequality to adaptively selected offline read coordinates without proof.**
3. For `q=0` the sharp point is `(p,L,Q)=(p,p,b-p)`. For `q=1` the exact sharp nonlinear lower/constructive upper bound is `L=p-floor(log2(p+1))`, `Q=b-p+1`. The Hamming encoder is **known** from ARC237; the simultaneous constrained acquisition/continuation composition is the new claim.
4. Concrete point `(b,p,L,Q)=(15,11,8,5)` is attainable with exact source read counting, nonlinear lower bound 8; 2^8 * 12 > 2^11, so the unrounded volume inequality itself is not met at equality.

## Reproducible tests

Code: `research/agents/lspv-1/2026-10-29_2000_ARC239_construction_read_frontier.py`. Raw: `research/agents/lspv-1/2026-10-29_2000_ARC239_raw.json`. Deterministic enumeration, no randomness. 44 `(b,p)` parameter combinations for `1<=b<=8`, 757,304 exhaustive source/mask pairs. An additional 1,081,344 `(b,p)=(15,11)` source/mask pairs. Exact nonlinear fixed-read encoder enumeration: all 16 at `(3,2,1)`, all 256 at `(4,3,1)`. One adaptive preprocessor control and XOR-value/redundancy/negative-realized-entropy controls. All assertions passed. These are not asymptotic proofs.

## Role targets

LSPV-1: prove or falsify the stronger triple bound with **adaptive choice of offline read coordinates**, including all retained source-dependent transcript bits. LSPV-2: seek sparse linear-code representations with low exact update/write costs and compare covering-radius upper points. LSPV-3: test whether authentic moving SAT interfaces fit a separately justified offline-before-continuation model; do not assume source bits independent. LSPV-4: charge native single-tape, two-tape, read-only-input multitape and indexed RAM operations without exponent borrowing. LSPV-5: independently referee the forced-read and Fourier composition quantifiers; root manuscript integrity and ownership preservation remain with LSPV-5.

## Source provenance

ARC237 blob `673bd7b4e72892646a76f2d57760e602d7bcb384`; ARC238 blob `529fbe875fdcf0ddd91d91968c8b37df8d046f7f`; LSPV-2 HAMMING235 blob `b4a1a846dab97bd02691578d9abe5a081890d8b7`; Sage Hamming source blob `431e660fae77184147230223f66c76f2d5f04b38`. Primary sources: Hamming (1950), Gál-Miltersen (2003), Fredman-Saks (1989), Darwiche-Marquis (2002). Independent mathematics is in the LaTeX report. No code from Sage was executed.

No new tasks or schedule changes; P=NP and P!=NP remain OPEN.

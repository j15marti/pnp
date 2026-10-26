# LSPV-4 signed cost audit: ARC-R15-LENGTH-AUDIT126

Date: 2026-10-26 00:36 America/Los_Angeles. Owner: LSPV-4. Scientific status: PROVED/EXACT arithmetic conditional on adopted LSPV-2 one-level gadget counts; computational arithmetic 95/95 assertions; unrestricted contractor OPEN. Signed off by **LSPV-4**, role-owned audit 126. The signed-off attribution is a research authorship sign-off, not a cryptographic personal signature.

## Content-addressed, independently fetched source manifest

- Report: `research/agents/lspv-4/2026-10-26_0036_LSPV-4_ARC_R15_LENGTH_AUDIT126.tex` (Git blob SHA `8c5db505ec83ebe165d48218387d5e2df875dda0`).
- Reproducer: `research/agents/lspv-4/2026-10-26_0036_ARC_R15_LENGTH_AUDIT126_repro.py` (Git blob SHA `67945c0515a0df03434b42e62773ac37e9579472`).
- Raw JSON: `research/agents/lspv-4/2026-10-26_0036_ARC_R15_LENGTH_AUDIT126_raw.json` (Git blob SHA `fef6d806ce9bdb7612c336edfd2482bdf022ce22`).

## Exact resource delta

LSPV-2 original signed exact-(2P,2N) regularizer (R_{15}) sends count pair ((n,m)) to ((48n+33m,64n+44m)). Its matrix (A=left(\begin{smallmatrix}48&33\\64&44\end{smallmatrix}\right)) obeys **(A^2=92A)**, hence (A^h=92^{h-1}A) for every fixed (h\ge1). For already balanced sources (3m=4n), each iteration multiplies *both* counts by exactly 92. Two levels give ((4416n+3036m,5888n+4048m)). A complete target binary encoding (B(n,m)=4+2\lceil\log_2(\max(n,m)+1)\rceil+3m(1+\lceil\log_2(n+1)\rceil)) consequently remains **Theta(N)** on a cofinal dense fixed-incidence source family, not (N^{1/4}) or (N^{1/2}). The local virtual literal accessor may remain polylogarithmic; this does NOT change fully encoded input length or the worst-case guest bound. An eager materialized grandchild is linear-size writable storage; a lazy guest must pay every nested virtual bit request.

For real adaptive children, (\sum_i m_i^d\le (\max_i m_i)^{d-1}\sum_i m_i). With volume (V\le N^b), maximum length (M\le N^\lambda), and guest exponent (d\ge1), the *upper* guest budget is (b+\lambda(d-1)); an (N^u) cost **per guest step** adds (u), whereas (u) defined as **total aggregate accessor exponent** enters the maximum as a separate term. Both interpretations include source reads, index/control, headers, validated joins, certificate bytes, failed routes, retained ancestors and simultaneous writable peaks. For the actual R15^2 output, (b=\lambda=1) for one grandchild and no upper-bound improvement follows.

## Published strict limits (model-checked)

FLMV: (t<241/200), (s<11642479/23232400); point ((6/5,1/2)) has exact positive margins (1/200) and (26279/23232400). Under the extra, unproved (d=901/500) small-space seed only, van Melkebeek Thm 1.3's coNTIME condition gives (c<651000/361301); Thm 6.3's **full all-input nonuniform decision-circuit** condition plus a separate small-space Sigma2SAT simulator (D=d^2) yields (q<811801/561801). Not implied by P=NP. NAND formula-depth, threshold wire counts and explicit circuit evaluation stay within their precise model and cannot be combined across different machines.

## Peer actions, without any schedule/task change

**LSPV-1**: In the certificate contraction proof, distinguish a polylog-addressable grammar adaptor from genuine *power-short eligible ordinary children* in the exact input-bit metric. An UNSAT tree may be nondeterministically **guessed** for coNTIME, but every bit and coverage check is charged and no free deterministic selection follows. Find a genuinely shrinking all-input constructor and complete all-UNSAT cover, or mark those exact arrows OPEN.

**LSPV-5**: Independently multiply the matrix, check (B(A^h(n,m))=\Theta(B(n,m))) for fixed (h), verify the 95-assertion raw/code reproducibility, the strict source theorem quantifiers and the distinction between a full SAT decision circuit and one encoded instance. Preserve all peer text and root executive OPEN statuses. Note the older executive (R\le2) statement applies only to **final labels**, not query transcripts (see LSPV-1 ARC181).

## Hostile controls and exact next arrow

All-count lemma applies even to easily recognized repeated UNSAT / parity / Horn / affine examples; it is not a SAT lower bound and does not refute alternative shorter reductions. The peer Q15/J gadget's own semantic proof and unrestricted raw-ID Rank/Select remain separate audit obligations. Next missing implication: noncircular, all-ordinary-input, two-level exact SAT/UNSAT compiler producing honestly (N^{\lambda<1}) ordinary children with all access/discovery/streaming memory costs charged, or a verified coNTIME all-UNSAT complete proof tree together with the separately required deterministic small-space seed. ARC-EDGE-90 and P vs NP remain OPEN. No external messaging; no automation modifications.

END_HANDOFF::ARC_R15_LENGTH_AUDIT126

# TMR-1/031: Local-input-prefix plus Pippenger-Fischer circuit composition

**Pacific timestamp:** November 14, 2026, 17:04 PST (America/Los_Angeles). **Role:** TMR-1, Machine Model Lead. **Status:** LOCALPF045 **CANDIDATE/RESTRICTED**, complete symbolic argument supplied below, **independent mathematical review OPEN**. Published finite tests are **COMPUTATIONAL**. P versus NP **OPEN**.

## 1. What is new relative to the existing corpus

TMR-4/032 proved the full-copy indexed evaluator bound
$$
CC_n(Y_{F})\le K_E H\log_2(2H),\quad H=L+n+t+2.
$$
TMR-5/028 separately exploited locally moving, left-initialized input heads to prove the length-independent but quadratic bound
$$
CC_n(Y_F)\le K_E(t+2)^2.
$$
**LOCALPF045 composes the two ideas**, using only the *reachable physical input prefixes* in the input-copy adapter before applying Pippenger-Fischer's original near-linear circuit simulation. This removes the $L+n$ term **without** reverting to quadratic unrolling:
$$
\boxed{CC_n(Y_F)\le K_E(t+2)\log_2(2(t+2)).}
$$
The point is an **explicit bridge**, not a new theorem of Pippenger and Fischer, and not a claim that input prefixes are sufficient for arbitrary RAM/random-access machines. I found no earlier corpus entry stating this combined bound.

This repairs the threshold window left between TMR-4/032 and TMR-5/028: if $N=L^{a+o(1)}$, $t\le L^{d+o(1)}$, and $a\mu>d$, all outputs eventually belong to ordinary MCSP at threshold $\lfloor N^\mu\rfloor$ for fixed $\mu>0$. TMR-4/032 required $a\mu>\max(1,d)$; TMR-5/028 required $a\mu>2d$.

## 2. Exact model and claim

Fix **one** finite total deterministic evaluator $E$ for **all** source descriptions $F\in\{0,1\}^{L}$, target arities $n$, and indices $i\in\{0,1\}^{n}$. It has a constant number of finite-alphabet, one-dimensional locally moving read-only input heads, each initially at its conventional fixed left origin, and a constant number of standard local read/write work heads. It reads explicitly delimited $F$ and $i$ and emits exactly one bit. Each head moves at most one cell per transition. No prepositioned head, free random access, oracle, advice, or unbounded-word primitive is permitted. Malformed encodings are handled by the same fixed total $E$.

Define $Y_{E,F,n}(i)$ as the output of $E(F,i)$ and
$$
t=t_{E,F,n}:=\max_{i\in\{0,1\}^n}T_E(F,i).
$$
Truth-table length is $N=2^n$; $L$ is source-description bit length. $CC_n$ is fan-in-two AND/OR/NOT circuit gate count with free constants, unrestricted fanout, and a standard fixed universal basis.

**LOCALPF045 (CANDIDATE/RESTRICTED, peer review OPEN).** There is a fixed constant $K_E$ depending only on $E$, tape conventions and gate basis such that for every $L,F,n$ with finite $t$,
$$
CC_n(Y_{E,F,n})\le K_E(t+2)\log_2(2(t+2)).
$$
This is a **nonuniform upper bound** on the generated $n$-input Boolean function. Its proof does not give a uniform algorithm to *find* a small circuit from $F$ in polynomial $L$ time and does not implement MCSP.

## 3. Proof, including the input interface

**Reachability.** In at most $t$ transitions, every initially left-positioned head visits only cells at physical distance at most $t$ from its start, including an endmarker iff that endmarker lies in the reachable interval. For each read-only source/index tape, replace the original contents beyond distance $t+1$ by arbitrary filler, leaving a correct length/endmarker symbol **when physically reachable**. Every actual $t$-step execution (including adaptive head moves, input rereads, branching and work updates) is unchanged. No source-/index-dependent *far* cell is observed. If $L$ or $n$ is shorter than the bound, encode the genuine endmarker within the retained prefix. If longer, use a tagged no-endmarker-within-reach convention. These tags depend only on the fixed lengths, not on unobserved index bits.

**Charged fixed-machine adapter.** Consider one **fixed** sequential-input transducer $U_E$, with a fixed finite program independent of $F,n,t$. For a selected horizon $t$, feed $U_E$ a self-delimiting stream consisting of (i) unary $t$ or an equivalent $O(t)$-bit horizon record, (ii) the tagged source prefix of length at most $t+1$, and (iii) the tagged index prefix of length at most $t+1$. Each input field is at most $O(t+1)$ bits, so the stream has length $O(t+2)$. The parser copies these two prefixes, including any real endmarkers, onto distinct ordinary writable one-dimensional tracks in $O(t+2)$ steps. In the subsequent simulation $U_E$ uses separate native local work heads as necessary to emulate every concrete $E$ transition at constant-factor cost. It never needs a remote source symbol because no original head travels beyond the copied reachable region during the first $t$ steps. An already halted simulated evaluator latches its output; otherwise the machine simulates exactly $t$ steps and reads the resulting terminal bit. Total transducer steps are at most $c_E(t+2)$ on every stream of the declared shape, for a constant $c_E$ independent of the lengths and the source contents.

Importantly, $U_E$ does **not** receive the source prefix as free advice or as preinstalled work-tape contents. Copying every retained source bit is paid within the $O(t)$ adapter bound. The prefix may be *hardwired* only after constructing a nonuniform circuit, because $F$ is fixed in the definition of $Y_{E,F,n}$.

**Circuit conversion.** Pippenger and Fischer (JACM 26(2), 1979), Theorem 4, printed page 379, supplies a cost $O(h\log h)$ combinational circuit simulating $h$ steps of a **fixed** transducer with one-dimensional tapes and a one-way input stream. Apply it to the fixed $U_E$ with $h=c_E(t+2)$. Its source-field input wires become constants encoding the retained prefix and its length tags; the index-field input wires connect to the corresponding original $i_j$ inputs; horizon/length tags become constants. Arbitrarily many unused high-index wires need no gates. The resulting circuit computes $Y_{E,F,n}(i)$ on **every** $i$, not just a selected execution. The number of gates is at most $K_E(t+2)\log_2(2(t+2))$ after fixed-basis conversion. This completes the scoped symbolic argument. Independent peer audit of the exact PF input-stream translation remains requested.

**What this does not assume:** The adapter is a conceptual existence construction used to upper-bound nonuniform circuit size. It is not a polynomial-time explicit-output SAT-to-MCSP reduction, and is not available as advice to a uniform 3-SAT decider. The proof would fail for arbitrary-cost indexed source probes or free input-head initial positioning.

## 4. Exact quantitative consequences

For fixed $0<\mu<1$, $s=\lfloor N^\mu\rfloor$, if
$$
K_E(t+2)\log_2(2(t+2))\le s,
$$
then **every** indexed table generated by $E$ at that $(F,n)$ is ordinary MCSP YES. Therefore an MCSP NO output at this threshold requires $t=\Omega_E(s/\log(2s))=\Omega_E(N^\mu/\log N)$, with constants depending on $E,\mu$. This is a **lower bound on how quickly a given table with large circuit complexity can be indexed-evaluated**, not a lower bound on deciding MCSP or 3-SAT.

If $N=L^{a+o(1)}$ and $t\le L^{d+o(1)}$, $a\mu>d$ suffices for eventual YES collapse. A strict gap is required; equality requires keeping constants and logarithms. Example: $a=2,\mu=2/5,d=3/10$ gives $a\mu=4/5>d=3/10$ but $a\mu<1$, so old full-copy PF gives no YES conclusion from its displayed bound. Source lengths and target truth-table lengths must not be conflated.

The bound is not contradicted by an $O(L)$ evaluator that returns $F[i]$ when $L=N$: here $t$ may be $\Theta(N)$, while $N^\mu$ is sublinear. Nor does it imply NP-hardness of ordinary MCSP.

## 5. Primary-source theorem and hypothesis matrix

| Source and theorem | Exact decision/operation, input measure | Model and hypothesis | Output/conclusion | Transfer status |
|---|---|---|---|---|
| Pippenger and Fischer, JACM 1979, Theorem 4, p.379 | First $h$ steps of a fixed one-dimensional-tape transducer with sequential input symbols | Combinational finite-gate network, bounded tape alphabet, standard local head movement | Network cost $O(h\log h)$, depth $O(h)$ | **KNOWN THEOREM**, used in LOCALPF045 with an explicit $O(t)$ copy adapter |
| Cheraghchi, Hirahara, Myrisiotis and Yoshida, STACS 2021, Theorem 1, p.23:3 | **Ordinary** $\mathrm{MCSP}[2^{\mu_1 n}]$ on an explicit $N=2^n$-bit truth table, some sufficiently small $\mu_1>0$ | Deterministic machine with **one** two-way read/write work tape plus **one-way** read-only input tape; antecedent not in $\mathrm{DTIME}_1[N^{1.01}]$ | $P\ne NP$, **conditional** on the unproved antecedent | **OPEN** at the requisite small threshold |
| CHMY STACS 2021, Theorem 2, p.23:3 | Ordinary $\mathrm{MCSP}[2^{\mu_2 n}]$ with larger $\mu_2$ near 1, explicit $N$ bits | Randomized, two-sided error, same one-work-tape and one-way input model; not in $\mathrm{BPTIME}_1[N^{1.99}]$ | **KNOWN lower bound**, at its own larger threshold | Does **not** instantiate Theorem 1 |
| McKay, Murray and Williams, STOC 2019, accepted manuscript, streaming result as summarized by CHMY p.23:2 | Search-MCSP with oracle-gate generalizations, complete truth table $N=2^n$, explicit size parameter $s(n)$ | One-pass streaming, $\operatorname{poly}(s(n))$ state and update-time premise | Conditional $P\ne NP$ via resource-bounded compression | Do not silently interchange search and ordinary decision versions |

For Theorem 1 versus Theorem 2, exponent $1.99>1.01$ **does not compensate** for the changed threshold. $\mu_1,\mu_2$ are paper-dependent existential constants, not arbitrary user-selected thresholds. Gap-MCSP, MKTP, partial and succinct variants are not silently equated. No unproved ETH, SETH or cryptographic assumption enters LOCALPF045.

## 6. Evidence and original-work ledger

- **TMR-4/032**, \`research/agents/tmr-4/2026-11-14_1650_TMR4_PF_LINEARLOG_INDEX_FIREWALL032.md\`, native Python \`experiments/tmr/tmr4_pf_index_lift044.py\`: full-copy $O((L+n+t)\log(L+n+t))$ restricted theorem; independent review open.
- **TMR-5/028**, \`research/agents/tmr-5/2026-11-14_1650_TMR5_LOCALHEAD_AND_SPARSE_TAIL_AUDIT028.md\`, native Python \`experiments/tmr/tmr5_locality_tail_audit044.py\`: local-head $O(t^2)$ theorem; independent review open.
- **TMR-1/030**, \`research/agents/tmr-1/2026-11-14_1605_TMR1_SHORT_HEADER_CONSTRUCTOR_SIMULATION030.md\`: charged network constructor for high-threshold MCSP, does not reach magnification.
- **TMR-3/031**, \`research/agents/tmr-3/2026-11-14_1635_TMR3_SHARP_SPARSE_NETWORK_SOURCE_FRONTIER031.md\`: $\Omega(N^{1-\mu})$ point-query bound, restricted, below superlinear time target.
- **Historical controls:** \`research/agents/claude/onetape/README.md\` for sequential crossing arguments; \`research/agents/claude/tport/README.md\` for portfolio barriers; \`research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex\` for direct-product caveats; \`research/agents/tmr-2/2026-11-14_0823_TMR2_MAXSAT_WALSH_SIGN_ROBUSTNESS022.md\` for compact Walsh/affine controls; \`GROKPROOF/2026-10-31_0522_GROK_PROGRESS.md\` for still-open all-input resource transfer. None is an unrestricted MCSP or SAT time lower bound.
- **Current preflight:** November 14 MCSP directive (SHA \`1e11aa64a0b0d635a65cea58500b09f2b0fe010a\`), November 13 TMR directive, full root \`proof1.txt\` (28,714 chars, SHA \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`), **authentic full Git blob** \`proof2.txt\` (1,051,196 chars, SHA \`930c5eeddafce656717f28055a7a9a755f44737c\`), **authentic full Git blob** \`main.tex\` (2,545,859 chars, SHA \`6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34\`), AGENTS.md, CODEX.md, research skill, newest five handoffs, issue #3 through comment 6886983597. Ordinary file-fetch returned blank for the huge two blobs; full content was recovered via Git blob. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** No shared tracker or canonical \`main.tex\` modified.

## 7. Reproducible finite checks and limits

Native CPython original source \`experiments/tmr/tmr1_localpf_prefix045.py\` and separate immutable raw JSON \`results/raw/tmr/2026-11-14_1704_TMR1_LOCALPF045_RAW.json\`. Seed 202611141704. Checks: **5,760** paired full/truncated finite-machine traces, **43,200** identical physical transitions, **43,008** exhaustive index-prefix combinations, **9** exponent windows, **zero failures**. Source SHA256 \`2f112cb5ee101e865158f915bbc015c0f4b223134be636da4b2560f41a729afe\`; raw SHA256 \`ed9983d38def2ea132432308d81a1872d04e2bd4ee2062894f10db14c00676cc\`. Tests check reachability, not the general PF circuit compiler. Finite experiments are **COMPUTATIONAL**, never asymptotic proofs.

**Next concrete target / peer request:** TMR-4 independently audit the sequential-input adapter and exact $O(t)$ copying bound for every read-only tape and both length/endmarker regimes. TMR-5 independently audit the threshold $a\mu>d$ and supply a hostile indexed counterexample for malformed inputs, prepositioned heads or exotic tape delimiters. TMR-2/3 should separate the proved circuit-complexity generation bound from any proposed MCSP *decision* time lower bound. The genuine magnification hypothesis and the unrestricted all-polynomial 3-SAT time lower bound remain **OPEN**.

## Primary references

[1] Pippenger, N., and Fischer, M. J. (1979), *Relations Among Complexity Measures*, JACM 26(2), Theorem 4, p.379, https://doi.org/10.1145/322123.322138 (primary PDF https://www.ccs.neu.edu/home/viola/classes/papers/PippengerF-Oblivious.pdf).

[2] Cheraghchi, M., Hirahara, S., Myrisiotis, D., and Yoshida, Y. (2021), *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*, STACS, printed p.23:3, Theorems 1 and 2, https://doi.org/10.4230/LIPIcs.STACS.2021.23 .

[3] McKay, D. M., Murray, C. D., and Williams, R. R. (2019), *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*, STOC 2019, accepted author version https://hdl.handle.net/1721.1/137518 .

END_OF_REPORT::TMR1::LOCALPF045::2026-11-14_1704_PST

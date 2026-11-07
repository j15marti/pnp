# LSPV-1/478 | Positive-alias 3-CNF split: sparse polynomial-calculus certificate transfer

**2026-11-07 07:55 PST | Route B | PROVED/RESTRICTED symbolic theorem; COMPUTATIONAL finite controls | P versus NP OPEN.**

**Exact tracker nodes:** new [P2-B19] (restricted encoding/transfer evidence), building on [P2-B18] and [P2-B17]. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain **OPEN**. Route A [P1-01], [P1-03], [P1-04] remain OPEN.

## IDEA: predeclared falsifiers

Hypothesis: a polarity-normalized variant of the exact clause-split gadget from LSPV-1/477 admits a **positive-variable identification** for every new auxiliary variable, eliminating the exponential sparse-monomial expansion that blocked a certificate-bit claim in /477. Falsifiers: (F1) any signed clause has an incorrect existential projection or original clause-image; (F2) a projected source or inference needs an inadmissible PC rule/Boolean-quotient shortcut; (F3) the certificate compiler can create more monomials than the input proof; (F4) the fixed encoding introduces a hidden change to historical R_mix341 or invalidates the existing Resolution/Tseitin controls.

## SEARCH: actual predecessor and external evidence

Read BOTH complete living proof trackers, coordination issue #3 and recent comments, governing five-role handoff, AGENTS.md, CODEX.md and repo skill. Reused original LSPV-1/477 (blob a7959a9d), LSPV-3/475 (3a8da052), Grok actual GROKPROOF/2026-11-07_1119_PROGRESS.md (d87fcb3a), and Claude actual research/agents/claude/world-ledger/README.md (de75a371). Reviewed konard/p-vs-np/proofs/complexity/README.md (7ee9a11e; finite-machine P subset NP, no unrestricted P/NP resolution), blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693ea; bounded claims), meelgroup/frat-xor/format.md (986a21aa; separate accepted grammar), peitl/short-proof/README.md (93d2090d; minimum Resolution search), and openai/math/README.md (cc5b0a03; verification qualifications). Primary theory checked: Buss–Grigoriev–Impagliazzo–Pitassi (2001) for characteristic-dependent Tseitin PC degree; Impagliazzo–Pudlák–Sgall (1999) for size/degree; Urquhart (1987) for expander Tseitin Resolution. Pang arXiv:2610.00837 (2026 preprint) is a separate Res(PC_r) control. No independent Google-branded interface used. No mathematical novelty claim is made.

The root main.tex returned SHA 68188a24 but **zero content bytes** through the GitHub connector and is not edited. Native R_mix341 checker and full repository preflight were not executed; only documented current governance/peer files were read.

## ITERATE: polynomial-bit transfer for a different but explicit proper 3-CNF

Fix a finite prime field $K=\mathbb F_p$. Let $F$ be an original signed proper 3-CNF. Each original clause has pairwise distinct underlying variables:
$$
C_i=\ell_{i1}\lor\ell_{i2}\lor\ell_{i3}.
$$
Let $x_{j(i)}$ be the **positive underlying variable** of $\ell_{i3}$. Introduce one globally fresh auxiliary variable $a_i$, and define
$$
\alpha_i=\begin{cases}a_i,&\ell_{i3}=x_{j(i)},\\ \neg a_i,&\ell_{i3}=\neg x_{j(i)}.\end{cases}
$$
Replace $C_i$ by two strictly proper signed ternary clauses
$$
P_i=\ell_{i1}\lor\ell_{i2}\lor\alpha_i,\qquad
Q_i=\ell_{i1}\lor\ell_{i3}\lor\neg\alpha_i.
$$
Write $S^+(F)$ for the $2m$-clause formula and $q_C=\prod_{\ell\in C}(1-\operatorname{val}(\ell))$ for the **formal unreduced-ring** clause polynomial. The **positive** ring homomorphism
$$
\sigma(a_i)=x_{j(i)},\quad \sigma(x_j)=x_j
$$
gives **exactly**
$$
\sigma(q_{P_i})=q_{C_i},\qquad
\sigma(q_{Q_i})=-(1-\ell_{i1})(x_{j(i)}^2-x_{j(i)}).
$$
Thus the image of $P_i$ is an **original source axiom** and the image of $Q_i$ has a two-or-three-step legal derivation from an original Boolean axiom. Both images are formal polynomial identities, not merely Boolean-cube equalities. Every multiplication-by-auxiliary inference in a PC refutation becomes one permitted multiplication by the corresponding **positive** original variable; linear combinations map directly. Each projected monomial maps to exactly one monomial, possibly with cancellation; it **never expands**.

Conversely, the exact formal identity
$$
q_{C_i}=q_{P_i}(1-\ell_{i3})+q_{Q_i}(1-\ell_{i2})
$$
reconstructs each original clause polynomial from two split sources using O(1) native PC steps of degree at most four. It is valid for either literal polarity and all fields.

**Theorem 478.1 (PROVED/RESTRICTED).** For every fixed finite prime field, ordinary *sparse, explicit-monomial polynomial calculus* over these original clause polynomials and Boolean axioms has polynomial-bit refutation translations **in both directions** between $F$ and $S^+(F)$. With $s$ proof inference lines, $M$ total explicitly represented monomial occurrences, and $m$ original source clauses, the reverse compiler uses $O(s+m)$ lines and at most $O(M+m)$ monomial occurrences, ignoring bounded constant-size source-axiom expansions; indexed evidence bits and deterministic construction time are polynomial in the input proof, source encoding and indices. The forward compiler adds $O(m)$ lines and $O(m)$ constant-width source-derivation monomial occurrences, then replays all original lines. Degree satisfies
$$
D_K(F)\le D_K(S^+(F))\le\max\{D_K(F),4\}.
$$
Here the bounds refer to a **fixed declared PC system**, not R_mix341. An arbitrary syntactic sparse-PC proof may contain huge identifiers/coefficients; the compiler parses and charges their actual encoded sizes, so polynomial input-relative overhead is preserved without treating huge values as free. The statement neither certifies the historical native grammar nor establishes computational hardness for SAT.

The standard split $S(F)$ of /477 always uses $\alpha_i=a_i$ and may require $\sigma(a_i)=1-x_j$, expanding a single monomial into $2^d$ terms under a degree-$d$ substitution. **That earlier bit-cost caveat still applies to the standard split**. $S^+(F)$ changes only the signs of certain *fresh* auxiliary occurrences. This is a variable-complement renaming, so ordinary Resolution hardness is identical, while the new positive-alias explicit PC projector is size controlled. Do not infer a polynomial sparse-PC variable-complement compiler for the older encoding.

## Established hard family, precise encoding and controls

For connected cubic expander graphs $G_h$ with $h$ vertices and $3h/2$ edge variables, choose odd total vertex charge. Each three-edge parity equation is encoded by the four signed proper ternary clauses falsifying its opposite-parity assignments. Original $F_h$ has $4h$ clauses, encoded length $\Theta(h\log(h+2))$ under indexed encoding, and is certified UNSAT by summing charges. $S^+(F_h)$ has $8h$ clauses, $11h/2$ variables and the same $\Theta(h\log(h+2))$ encoded-size order. Established ordinary unrestricted shared-DAG Resolution lower bound $2^{\Omega(h)}$ for suitable cubic expanders transfers by the exact substitution/projection already audited in [P2-B17]. Published characteristic-$\ne2$ polynomial-calculus **degree** $\Omega(h)$ transfers by Theorem 478.1; the standard PC degree/size relation additionally yields exponential **sparse-PC size** for that precisely specified model. These are NOT known lower bounds for historical R_mix341: on these same formulas the declared semantic AND3/GF(2) shortcut gives $O(h)$ paid mixed work, pending historical native-byte legality. Cook Extended Resolution remains a mandatory stronger-system control.

## Independent finite evidence and full-resource caveat

The Python producer and local step-by-step ordinary-PC replay verifier passed **39,688 assertions** across $\mathbb F_2,\mathbb F_3,\mathbb F_5,\mathbb F_7$, including 55-step constructed split refutations and 75-step explicit original-source projections per field, 16 wrong-polarity rejections, and exhaustive original signed cubic odd-Tseitin controls on $K_4$, $K_{3,3}$, the cube and Petersen (0 odd-charge models; 8,16,32,64 even-charge parity models). Independent JavaScript polynomial identities and Boolean tests passed **396 checks**, rejecting **32** polarity mutations. Complement products expand from one monomial to $2^d$ monomials for $d=1,\ldots,12$; positive aliases keep one. Python recorded 0.178 seconds and 97,552 KiB peak host RSS in the final test. These are finite validations, not certified asymptotic family hardness. No authoritative historical checker, formal theorem prover, or same-machine FLMV execution was used.

The executed and byte-identical published independent JavaScript checker is `experiments/arc/lspv1_478_independent.js` (Git blob `948ce41e3abeba7028aa6f9de232976043c766c3`, independently matched to the local executed file). Structured evidence is in `results/raw/arc/2026-11-07_0755_LSPV1_478_PC_POS_ALIAS_PY.json` (explicitly a transcription of the local machine JSON) and `results/raw/arc/2026-11-07_0755_LSPV1_478_PC_POS_ALIAS_JS.json`. The complete executed Python original-source PC proof producer, its unabridged raw output, and both checkers are available in the separate local reproducibility archive; its Python source has NOT been pushed to GitHub. The full original-source PC replay was executed locally, whereas the published JavaScript covers independent identities/Boolean controls. The historical R_mix341 witness checker remains unauthenticated.

**TRACKER:** [P2-B19] is an additional proof-system-specific certificate-size transport. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN; P versus NP OPEN. No task, schedule, weight, route allocation or main.tex modification.

## References

[1] Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), 209–219, DOI 10.1145/7531.8928.

[2] Buss, Grigoriev, Impagliazzo, Pitassi, *Linear Gaps Between Degrees for the Polynomial Calculus Modulo Distinct Primes*, JCSS 62 (2001), 267–289, https://mathweb.ucsd.edu/~sbuss/ResearchWeb/lineargaps/index.html.

[3] Impagliazzo, Pudlák, Sgall, *Lower Bounds for the Polynomial Calculus and the Gröbner Basis Algorithm*, Computational Complexity 8 (1999), 127–144, DOI 10.1007/S000370050024.

[4] Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837 (2026 preprint), https://arxiv.org/abs/2610.00837.


## Charged execution and publication addendum (post-publication reconciliation)

The finite **explicit sparse-PC certificate upper-bound** control has 55 paid split-proof instructions (16 source uses plus explicit multiplication/linear-combination steps, reusing earlier lines) and a 75-instruction original-source projected proof per field. The Python JSON evidence serializes to 3,344 bytes for the split proof and 4,049 / 4,145 bytes for the projected proof in F2 / F3,F5,F7. These are constructed upper bounds, **not minimum** proofs. The reverse symbolic compiler handles arbitrary DAG references and charges the exact proof record, including cached/reused lines, as explicit evidence. No branching/split/discharge rule is introduced.

For actual finite execution, source parsing, original/source-index building, constructing all output proofs, formal-ring operations, local replay verification, original SAT and even-parity controls, corrupted polarity tests, serialization, disk output and Python interpreter startup were all incurred inside the measured Python run (0.177219 seconds, host peak 97,552 KiB RSS). No separate individual-phase timers or same-machine tape counters were instrumented, so no phase-resolved numerical claims are made. The independent JavaScript witness checks used the published byte-identical script SHA-256 `35114fe364c8dc5f9133cc956ab4e55c71c6f1eb435599d2b1e0523febfca333`; its Git blob is `948ce41e3abeba7028aa6f9de232976043c766c3`. The local full Python executed source SHA-256 is `532b0286f108886d3784b4b663b161578e37fd0dd30a7f8febbda161891d5d3b`. Inference-node count is not real machine time; free after-the-fact choice affects the ideal minimum only. Each actual compiler input parse, source/head read, coefficient arithmetic, output reference, disk read/write, any failed candidate, and peak retained proof storage is chargeable in the claimed polynomial-overhead translation. No hardware-level/FLMV-specific numerical time-space exponent was established.

Publication status: the proof2.txt optimistic update used full preceding blob `7b3808f351a8c303a030d181e0f07eb46a91ba76` and yielded complete verified new blob `390b55471df24fb20c0a49879da1f9ee41717e55`, commit `59bb68fb31bf7130bcf497a89c8b94b9c2b9b751`. The preceding complete blob was preserved as `research/agents/lspv-1/outbox/2026-11-07_0755_LSPV1_478_PROOF2_PREWRITE_EXACT.txt` with identical blob SHA; candidly, this immutable outbox was recovered and uploaded **after**, not before, the guarded tracker write. The update itself was conflict-safe and its entire postwrite readback matched exactly; the historical prefix survived unchanged. proof1.txt was fully reviewed and unchanged at blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`. Coordination issue #3 comment `6709619529` was read back exactly. All five supporting GitHub artifacts (report, JS, both raw records, and handoff) were verified by complete readback; main.tex returned only a SHA and was not touched. Publication remains intentionally limited to the narrow calculus and the status of P versus NP is OPEN.

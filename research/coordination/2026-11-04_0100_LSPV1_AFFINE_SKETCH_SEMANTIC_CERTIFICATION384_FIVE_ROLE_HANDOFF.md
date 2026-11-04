# LSPV-1/384 Five-Role Handoff: Rank-One Sketch Certification Barrier

2026-11-04 01:00 PST. **B1/B2/B3, superpolynomial full $R_{\mathrm{mix341}}$ minimum and P versus NP OPEN.** Preserve exact five roles, identities, enabled states, hourly offsets, fixed weights, source grammar, and all verified results. No task mutation authorized or performed.

## Precisely proved restricted theorem

Given arbitrary explicit bounded-fanin circuit $C(u)$ and supplied affine sketch $L(u)$, recognizing whether $C=f\circ L$ for *some* $f$ is **coNP-complete even when the sketch is one fresh input bit** and the public output is one bit. More sharply, checking the explicitly supplied two-entry bank $f\equiv0$ remains coNP-complete. Uniform reduction from CNF-UNSAT $D(x)$:

$$
C_D(x,z,y)=z\wedge D(x),\qquad L(x,z,y)=y.
$$

When $D$ is UNSAT, $C_D$ is constant zero; when SAT, a witness assignment $a$ yields $(a,0,0)$ and $(a,1,0)$ in the same sketch fiber and with opposite outputs. Complement witness is polynomially checkable, establishing coNP membership. Consequently a polynomially bounded, uniformly polynomial-time-checkable proof language for *every* such semantic-positive claim implies NP=coNP. This is an explicitly scoped instance of earlier MAIN AFFINE-LUMPABILITY-RANK-GATE55, not a newly discovered coNP phenomenon.

**Critical firewall:** LSPV-1/381's original claim requires a **syntactically typed** sketch cut and is not refuted; checking its source wires is straightforward and the $2^k$-enumeration compiler is polynomial in **supplied circuit size** for $k=O(\log L)$. The theorem does not apply to a fully specified LOCAL-CONVERT on only three original inputs, whose semantic truth vector can be tested in $O(8L)$; nor does it establish any lower bound on uniform SAT decision or $W_{R_{\mathrm{mix341}}}$.

**Finite evidence:** 285 signed CNF instances (276 SAT, 9 UNSAT), producer 10,091 checks, independent verifier 1,142, 276 SAT witnesses, 10 malformed rejections in each implementation, corrupted gate rejection in producer, even/odd $K_4$ 8/0. Both executables were reconstructed and run **from exact connected GitHub readback**. Raw output and blob versions are cited in the main report. No randomness or optimizer extrapolation.

## Assignments to existing roles, without task changes

**LSPV-1:** maintain exact B1/B2/B3 quantifiers and distinguish a coNP semantic-validation barrier from proof-system minimum; inspect original LOCAL-CONVERT and decide whether fully typed source-authentication can avoid arbitrary semantic FACTOR recognition.

**LSPV-2:** analyze whether the actual unchanged original-support-three LOCAL-CONVERT can *expose* an unbounded named derived-wire boundary and how signed conservative DEF gates are charged; seek compact affine/circuit escapes rather than rebuilding hard SAT families.

**LSPV-3:** define an explicit, proof-checkable public interface in the signed-hypergraph/DAG state and a compositional equivalence certificate; insist on authentic source IDs, full public output vector and no hidden private aliases. Test the pair $(a,0,0),(a,1,0)$ against any proposed semantic shortcut.

**LSPV-4:** account for $L$ bits of supplied circuit payload and all-phase scratch memory, evaluation, gate reading, proof checking and output. Distinguish the $O(2^kL)$ typed compiler from a polynomial-$(N+q)$ machine trace. Fixed $B\le3$ avoids coNP complexity but not missing syntactic authentication.

**LSPV-5:** red-team the reduction and conditional NP=coNP certificate barrier; verify that no unauthorized semantic equivalence/UNSAT oracle slips into unchanged $R_{\mathrm{mix341}}$. Cross-check MAIN55C prior duplication, user-requested Grok/Claude folders, and peer handoffs.

## Original references and paths

**Formal report:** [research/agents/lspv-1/2026-11-04_0100_LSPV-1_AFFINE_SKETCH_SEMANTIC_CERTIFICATION384.md](../agents/lspv-1/2026-11-04_0100_LSPV-1_AFFINE_SKETCH_SEMANTIC_CERTIFICATION384.md).

**Producer:** [experiments/arc/lspv1_384_affine_sketch_semantic_audit.js](../../experiments/arc/lspv1_384_affine_sketch_semantic_audit.js).

**Independent verifier:** [experiments/arc/lspv1_384_independent_verify.js](../../experiments/arc/lspv1_384_independent_verify.js).

**Machine-readable raw:** [results/raw/arc/2026-11-04_0100_LSPV1_AFFINE_SKETCH_SEMANTIC_CERTIFICATION384.json](../../results/raw/arc/2026-11-04_0100_LSPV1_AFFINE_SKETCH_SEMANTIC_CERTIFICATION384.json).

**Established lower bound:** Haken (1985) exponential ordinary shared-DAG Resolution refutations of explicit unary PHP: input bit length $\Theta(h^3\log h)$; does *not* imply arbitrary machine hardness. Cook (1976) polynomial ER pigeonhole proofs and paid GF(2) Tseitin escape defeat an unwarranted same-family mixed-calculus transfer.

**Grok and Claude inspected:** \`GROKPROOF/2026-11-02_0617_GROK_CONTRIBUTION.tex\`, \`research/agents/grok/2026-10-12_1859_GROK_FL2.tex\`, \`research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex\`, and \`research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex\`, exact blobs in report. Each preserves an unresolved uniform transfer; none certifies B3.

**Next weakest sufficient step:** read and quote the immutable original \`R_{\mathrm{mix341}}\` LOCAL-CONVERT syntax and establish a **polynomially checkable, source-authenticated, charge-preserving** semantic cut at all legal interfaces; if not possible, present an admissible counterexample under precisely those rules. No new proof-system axioms or weights.

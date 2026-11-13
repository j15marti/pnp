# LSPV-1/611: complete Array/String carrier dichotomy and exact shadow-coordinate semantics of the recovered /341 AND3 transition

**November 12, 2026, 23:00 PST | LSPV-1 General SAT Lower-Bound Lead | historical Route B | PROVED/RESTRICTED source-level lemma + COMPUTATIONAL V8 differential | P versus NP OPEN.**

## Predeclared candidate and four falsifiers

**Candidate 611.1.** For every JSON packet accepted by the **unchanged recovered /341 fixture verifier** with standard, unmodified ECMAScript intrinsics, every AND3 \`support\` is necessarily either a JSON Array or a JSON String. The Array case enumerates its genuine numeric support coordinates. The String case admits an *exact* shadow-coordinate transformer: if the support is a length-three UTF-16 string, the loop can write assignment bits only to numeric edge indices 0 through 9, at character positions that are precisely ASCII digits. A string may nevertheless pass the checker's **substring** membership gate for an edge index 10 or higher; those edges remain zero in all its local table and affine-row evaluations. This describes the recovered checker, not a sound intended rule or the missing full $R_{\mathrm{mix341}}$.

Falsifiers registered for this focused test: **F1** a parsed JSON value other than Array/String can satisfy the original three AND3 support predicates and permit a complete step; **F2** an accepted String support can cause the loop to write numeric edge index 10 or higher; **F3** code-point iteration in \`new Set(s)\` versus UTF-16 indexing invalidates the derived three-coordinate shadow mapping; **F4** an original row mask/RHS checker admits a local step not captured by the shadow-row transformer. The proof excludes F1-F4 under the pinned execution assumptions, and the executed controls attempt to falsify each. Changes to global prototypes, external source binding, the full historical grammar and native cost interpretation are explicitly outside these quantifiers.

## Exact original-checker program surface

Original recovered verifier file: \`experiments/arc/lspv2_341_independent_verify.js\`; Git blob \`fcb7d4ced8f922de14c0bda16263a8cc7853e8e0\`. In its AND3 branch it computes

\`\`\`js
const sup=[...new Set([...a.support,...b.support])];
assert(sup.length<=3 &&
       p.support?.length===sup.length &&
       new Set(p.support).size===sup.length,"AND3 support size");
assert(sup.every(x=>p.support.includes(x)),"AND3 support names");
let bits=Array(E).fill(0);
for(let j=0;j<p.support.length;j++)
  bits[p.support[j]]=(m>>j)&1;
\`\`\`

It then checks that the computed conjunction table matches \`p.table\`; an optional \`p.row\` undergoes a numeric-\`BigInt\` mask/bit-parity check on the **same** \`bits\` vector, with \`p.support.includes(e)\` deciding which numeric mask coordinates are in scope. All factor SOURCES start with three distinct numeric edge indices, AND3 parent factors have such three-index support, and the checker permits only AND3 and XOR paid opcodes. In any accepted reachable AND3 step the union therefore has size exactly 3.

This is a native recovered-subprogram statement, *not* an assertion about an authoritative accepted-byte grammar for RES, DEF, LOCAL-CONVERT, contexts, discharge, joins or the whole mixed calculus.

## Theorem 611.1 (exact recovered AND3 type partition)

For each reachable accepted AND3 record after \`JSON.parse\`, with the unmodified built-ins used by the pinned standalone verifier, \`p.support\` has type **Array or String**. If Array, it is exactly a permutation of its parents' three numeric support edge indices. If String, it has exactly three UTF-16 code units with three distinct iterated Unicode code points; therefore the three code units are distinct and none can be paired as a valid supplementary-plane surrogate pair.

**Proof.** \`JSON.parse\` without a reviver returns only null, Boolean, Number, String, Array, and plain Object structures. The support-length equality demands \`length===3\`. Null/Boolean/Number lack that length. An Object may have an ordinary \`length\` property but is not iterable by \`new Set(object)\`; JSON provides no callable \`Symbol.iterator\` or custom method. The only surviving built-in iterable types with length 3 are String and Array. For Array, the original strict numeric \`includes\`, distinctness and length-three checks force the three numeric parent-support members, so the array is a permutation. For String, \`length\` counts UTF-16 code units while \`new Set\` iterates code points. Equality of both counts to three rules out supplementary pairs and duplicate code points. QED.

## Theorem 611.2 (exact String shadow transformer, including the affine alias)

Let an accepted candidate String support be $s=s_0s_1s_2$ (the three UTF-16 code units) and $m\in\{0,\ldots,7\}$ its table-loop assignment index. Define for every numeric edge index $e\in\{0,\ldots,E-1\}$:

$$
b_s(e,m)=
\begin{cases}
(m\mathbin{\gg}j)\mathbin{\&}1, & e\in\{0,\ldots,9\},\ s_j=\mathrm{ASCII}(\text{digit }e),\\
0, &\text{otherwise}.
\end{cases}
$$

The index $j$ is unique by Theorem 611.1. Let $T_a,T_b$ be the stored parent factor tables and $U_a,U_b$ their numeric ordered support arrays. The local checker's computed AND3 table bit is **exactly**

$$
T_{\mathrm{AND3}}(m)=T_a((b_s(e,m))_{e\in U_a})
\wedge T_b((b_s(e,m))_{e\in U_b}).
$$

Its optional row \((M,r)\) passes exactly when (a) \(r\in\{0,1\}\) as a numeric JSON value; (b) every low-$E$ nonzero mask coordinate \(e\) satisfies \(\mathrm{String}(e)\) is a substring of \(s\); and (c), for all eight \(m\),

$$
T_{\mathrm{AND3}}(m)=
\left[\bigoplus_{e<E:\,M_e=1} b_s(e,m)=r\right].
$$

High signed \`BigInt\` mask bits are inert for this local equality; if later XOR records carry them, the recorded exact \`BigInt\` XOR and terminal zero check still apply separately.

**Proof.** The original loop writes \`bits[s[j]]\` for one UTF-16 code unit \(s_j\). For a JavaScript Array, a one-character key names an existing numeric slot exactly when it is the canonical decimal character for indices 0 through 9. Other keys are named object properties, not numeric edge slots, so \`bits[e]\` stays at its zero initialization for all \(e\ge10\). The parent \`evalTable\` reads only numeric \`bits[e]\`; replacing those reads with \(b_s\) yields the displayed formula. The original row mask scope uses String \`.includes(Number)\`, which converts the Number to its decimal string, so a substring such as \`"10"\` admits coefficient 10 even though \`bits[10]\` is always zero. The original row evaluator uses the same \`bits\` vector, giving the exact parity equality. QED.

**Minimal local falsifier of an unsound "String means ordered numeric support" normalization.** With numeric parent support \(U_a=U_b=(0,1,10)\), String carrier \`"10A"\` passes all support-name gates: it contains decimal substrings \`"0"\`, \`"1"\`, \`"10"\`, has length 3 and 3 distinct characters. Yet the loop writes only indices 1 and 0, never index 10. The original mask-scope gate **allows** bit 10 by substring. For parent tables \`0x96\` and \`0xe7\`, the computed table is 102 (\`0b01100110\`); carrier \`"A10"\` yields table 60 (\`0b00111100\`). A correct three-coordinate enumeration over \(0,1,10\) is a distinct operation. These are **accepted local gate shapes**, not claims that a complete standalone /341 terminal refutation of those exact tables was checked.

## Reproducible computational falsification

Published executable \`experiments/arc/lspv1_611_native341_shadow_transformer.cjs\` (Git blob \`40e24d0ec7f6a388ccae04a4b05c4079d2590d1a\`) independently implements (i) the verbatim material original local JavaScript operations and (ii) the mathematical shadow coordinate map and row scope. An **exact readback** of the committed script was executed in hosted V8 with dummy CommonJS module bindings; no content change except stripping its \`#!\` shell header. Input support triples are all 35 three-subsets of \(\{0,1,2,9,10,11,12\}\) with \(E=13\); carrier candidates are all length-three words over 14 selected UTF-16 units (digits 0-9, A, Z and lone high/low surrogate) plus six specific word/surrogate controls. Parent tables use \`0x96\` and \`0xe7\`. Additional exhaustive checks vary **all 65,536 ordered eight-bit parent-table pairs** for the carrier \`"10A"\`, and test signed/high \`BigInt\` row masks and both RHS labels.

- 96,250 candidate String/triple pairs inspected, **92** matching accepted local name/length gates.
- **65,628** differential table checks, **1,840** independent affine-row comparisons, **210** valid Array permutation checks.
- **7/7** non-Array/non-String JSON type controls rejected at local support gate; **92/92** eligible String cases confirmed numeric high-edge slots stay zero.
- All comparisons PASS. The supplementary Unicode string \`"😀0"\` has UTF-16 length 3 but code-point Set size 2 and is rejected, confirming the two iteration models are intentionally distinguished.

Raw machine-readable hosted-V8 results: \`results/raw/arc/2026-11-12_2300_LSPV1_611_NATIVE341_SHADOW_TRANSFORMER_RAW.json\`; Git blob readback to be recorded in issue #3. This is a **finite regression and source-level proof**, not an exhaustive test of all Unicode strings, all valid graphs, or all terminal packets. Independent native Node OS execution of the new script and full original checker is outstanding.

## Dependency, provenance and nonpromotion ledger

**Adopted prior:** LSPV-1/609 establishes a checker-accepted SAT-source packet with a malformed String support, LSPV-1/610 proves the all-Array sufficient source-soundness boundary, LSPV-3/606 classifies the exact 131,068-member accepted String cloud at one fixed d17, LSPV-4/578 gives its UTF-8 evidence histogram, and LSPV-5/518 independently verifies the peer packet in Node. This run generalizes their *specific local carrier* observation to **all reachable /341 AND3 String steps**, including the row alias test, without claiming a new full accepted SAT packet. LSPV-2/591's exponential Horn provenance antichain also shows why explicit support enumeration is not a lower bound on symbolic state, memory or discovery.

**P2-D1 remains OPEN:** this closes only an exact typing/transition-semantics subquestion for the identified buggy **/341 fixture**. All true historical accepted opcodes, external signed SOURCE binding, fixed full mixed tariff, paid DEF/facets, fresh/exported/private wires, legal RES, LOCAL-CONVERT, branches, contexts, weakening, joins, deletion and discharge remain unauthenticated. The sibling /386 RES/DEF checker cannot be fused into /341 or substituted as historical authority. Unknown transitions must remain in any sound full-calculus MAY abstraction.

**P2-C3 remains OPEN:** a cost-sound abstraction over actual /341 bytes must include String carriers as real concrete paths, with an exact shadow transformer or safe overapproximation. Array-only is a sound *subdomain* but not full MAY coverage. At every whole-proof state retain raw/parsed source, full shared DAG and paid owner identities, antecedents, active/discharged assumptions, definition provenance, accepted/rejected terminal state and exact charges. An accepted buggy false refutation is not evidence that the source is actually UNSAT. The new local transformer has no global cost-bound conclusion.

**P2-B1 remains OPEN:** no superpolynomial all-rule minimum lower bound for a published hard 3-SAT family; all GF(2), extensions, preprocessing, branches, reconvergence and algebraic shortcuts remain available. **P2-B2/B3 separately OPEN:** neither a native-checker result nor published restricted proof-size lower bounds supplies the noncircular same-calculus transfer from SAT in P. No shortcut is declared illegal without its authentic historical semantics. Logical paid work, raw evidence bits, proof search, verifier time, machine time, span and simultaneous peak memory are different resources.

## Literature and required corpus

Primary proof-system scope: Cook and Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems*, DOI 10.2307/2273702. Abstract soundness: P. Cousot and R. Cousot (POPL 1977), DOI 10.1145/512950.512973. CEGAR: Clarke et al., CAV 2000, DOI 10.1007/10722167_15. Hard-family scope: S. Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837 (submitted September 30, 2026), fixed constant-degree polynomial proof lines, not unrestricted extension/branching or native /341. Verified modern mixed-proof comparison: meelgroup/frat-xor, \`format.md\`, defines a distinct FRAT-XOR/XLRUP language, not recovered historical bytes. No cited paper supplies the missing native grammar.

Preflight source read: root \`proof1.txt\` SHA \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`, root \`proof2.txt\` immutable blob \`f678f707880da4dfc97dabf778430c6dc816cb1f\`, issue #3 through LSPV-4/578, \`AGENTS.md\`, \`CODEX.md\`, \`.codex/skills/pnp-research/SKILL.md\`, LSPV-2/341, LSPV-1/539,/549,/609,/610, relevant peer /539-549 in issue/tracker and updated /591,/606,/578,/518 plus five-role handoffs. Root \`proof2.txt\` via contents API falsely appeared empty; its **complete 1,049,641-character immutable blob** was recovered and indexed. Full repository preflight and report-check scripts were not executed in a local checkout; GitHub blob readback verifies only committed contents.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1, P2-C3, P2-B1 and independent P2-B2/B3 remain OPEN; P1-01/03/04 OPEN. No role title, task, enabled state, route labels, schedule, historical weights or ownership changed. LSPV-5 independent falsification is requested, particularly using Unicode malformed surrogate carriers and typed-vs-string row-mask scope. The next load-bearing action is still recovering an authoritative single historical checker for genuine externally source-bound RES-to-AND3 or DEF-to-LOCAL-CONVERT, not declaring a repaired /341 parser as authority. **P versus NP remains OPEN.**

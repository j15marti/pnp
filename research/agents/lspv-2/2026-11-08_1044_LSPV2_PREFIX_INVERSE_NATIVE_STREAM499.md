# LSPV-2/499 | Linear-bit inverse and indexed-source resource ledger for explicit cubic Tseitin

**2026-11-08 10:44 PST | Route A primary | PROVED/RESTRICTED + COMPUTATIONAL; P versus NP OPEN.**

**Exact tracker nodes:** [P2-A2], [P2-A4], [P2-A5]; cross-controls [P1-01], [P1-03], [P1-04]. Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] unchanged and OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both complete trackers were retrieved and examined, not inferred from summaries. The new result tightens the resource accounting of the already documented restricted family but does not change an OPEN status, prerequisite, exponent class, or transfer gap. No edits to either root tracker.

## IDEA -> SEARCH -> ITERATE

**Initial IDEA.** LSPV-2/498 uses an explicit local cubic Ramanujan graph but the verifier materializes a host graph and input strings. Directly implement its source checker without an H-entry graph or H-bit saved matching array. Try to replace its apparent dense inverse scalar $(1+x)^{-1}$ by a two-pass XOR recurrence, and derive an explicit input-bit and indexed-head ledger in the *FLMV tape model*. This is a restricted implementation theorem, not a universal SAT accelerator.

**Falsifiers declared before testing:** (F1) the proposed two-pass inverse fails for some even field degree or input vector; (F2) a valid original signed strict-3CNF source needs a saved H-bit a/b table or full graph to classify; (F3) any one-bit mutation of a valid original is accepted; (F4) random-access return addresses, auxiliary index tapes, construction, or malformed inputs invalidate logarithmic work/high-water or the stated polylog-factor time bound.

**SEARCH actually performed.** Both complete root trackers; issue #3 and latest peer comments; governing five-role handoff; AGENTS.md, CODEX.md, repo skill; LSPV-2/478,/481,/497,/498, LSPV-4/498 and Route B LSPV-1/510 and LSPV-3/507 handoffs; actual GROKPROOF/2026-11-08_1130_PROGRESS.md (blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70) and Claude world-ledger README (blob de75a371ce3143a4495e6892df7fb04794a6b708). Required external source files inspected: konard/p-vs-np README.md (blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95; finite-machine P subset NP only), blkph0x/p-vs-np-proof-research METHOD_INDEX.md (blob 18d693ea71dfa433370eb7afbebc3106e32f03e5; scoped results), MassimoLauria/cnfgen/cnfgen/families/tseitin.py (blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab), meelgroup/frat-xor/format.md (blob 986a21aa92b62f844ef1fce852193142c41b2b1f, separate proof format), openai/math CONTENTS.md (blob 7e1ed90ac5a666f1bbecb22027387c4ad79e9d03; unrelated research index). No separate Google-branded search client; public web search was used. Direct repository git cloning from the local runtime failed due DNS, so authenticated GitHub connector source reads were used. No external claim is treated as a P-vs-NP proof.

**Primary research:** Viola and Wigderson, *Local Expanders*, Computational Complexity 27 (2018), Theorem 1.2 and Sec. 4.1-4.2, DOI 10.1007/s00037-018-0155-1, https://www.math.ias.edu/~avi/PUBLICATIONS/ViolaWi2018.pdf ; exact matrices on paper p.236 and special field polynomial/invertibility on pp.238-239. Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6) (2005), Sec. 2.1, DOI 10.1145/1101821.1101822, https://lance.fortnow.com/papers/files/tst.pdf ; exact model has read-only indexed input, write-only output, finite non-index WORK tapes with index tapes, and charges the highest touched non-index work address. The earlier LSPV-2/498 graph selection and odd-charge Tseitin rank proof are reused. The original signed family is known to be exponentially hard in **ordinary DAG Resolution**, not in unrestricted SAT computation or the fixed R_mix341.

## Theorem 499.1: two-pass inverse of the dense scalar, PROVED/EXACT algebra in declared quotient

Let $d=2m\ge2$, $g(x)=x^d+x^m+1$, and identify $v(x)=\sum_{i=0}^{d-1}v_i x^i$ with a $d$-bit vector. Define $u=D(v)$ by

$$
u_i=\begin{cases}
\bigoplus_{j=i+1}^{d-1}v_j,&0\le i<m,\\
\bigoplus_{j=0}^{i}v_j,&m\le i<d.
\end{cases}
$$

Then for **every even** $d\ge2$, even without assuming $g$ irreducible,

$$
(1+x)D(v)\equiv v\pmod{g(x)}.
$$

Moreover $g(1)=1$ in GF(2), hence $\gcd(1+x,g)=1$, so the inverse is unique and $D((1+x)u\bmod g)=u$.

**Proof.** In the coefficient vector of $(1+x)u\bmod g$, reduction $x^d=x^m+1$ gives $v_0=u_0\oplus u_{d-1}$, $v_m=u_m\oplus u_{m-1}\oplus u_{d-1}$, and $v_i=u_i\oplus u_{i-1}$ for the other $i\ge1$. On $1\le i<m$, adjacent suffix XORs cancel except $v_i$; on $m<i<d$, adjacent prefixes cancel except $v_i$. The special equations hold because $u_0=\oplus_{j=1}^{d-1}v_j$, $u_{d-1}=\oplus_{j=0}^{d-1}v_j$ and the three terms at $m$ leave $v_m$ after cancellation. Thus all coefficients agree. The low-half suffix XORs and high-half prefix XORs are computed by two scans, with $O(d)$ XOR operations and no general dense polynomial multiplication. QED.

For the locally explicit Viola-Wigderson graphs the polynomial is irreducible at $d=2\cdot3^t$, and the published sparse 2-by-2 matrices satisfy $M_i^2=(1+x)I$. Therefore $M_i^{-1}=D\circ M_i$ coordinatewise. Multiplication by $x$, $x^m$, or $x^{m+1}$ modulo the trinomial is a shift/XOR transform in $O(d)$ bit operations. **Both forward and reverse matching neighbor maps admit $O(d)$ bit-XOR circuits and $O(d)$ working bits**. This avoids treating a dense inverse as an uncharged constant-time oracle.

## Theorem 499.2: restricted indexed-source recognizer, symbolic FLMV-machine bound

Use exactly LSPV-2/495,/497,/498's binary source grammar, no modifications: $n=2d=4\cdot3^t$, $Q=2^n-1$, $H=2Q$, $W=\lceil\log_2(2H+1)\rceil$, $4H$ original signed proper 3-CNF clauses, literal sign plus W-bit ID, eight-bit magic, unary H and 2H, and final 10 bits. Thus

$$
N=3H+12+12H(W+1)=\Theta(H\log H).
$$

The algorithm (i) streams and validates the exact header, the permitted size shape and every original clause bit; (ii) recomputes each packet's three graph IDs by the local $M_i/M_i^{-1}$ maps; (iii) reads the first matching ID in the current packet, recovering its unique bit without an a/b array; (iv) on right-side packet $r$, uses a paid indexed lookup and return to read the matching bit from the already authenticated left packet $j=M_1^{-1}(r+1)-1$; (v) outputs MEMBER_SAT iff any such bit differs, otherwise MEMBER_UNSAT; and (vi) outputs OUTSIDE on an invalid source, including corrupt header or trailer. OUTSIDE is **not** a general-CNF MALFORMED classification.

**Exact bit-probe ledger on every recognized source for the published independent verifier:**

$$
R=N+HW+QW=N+\frac{3H}{2}W.
$$

The first term validates every source bit once. The next HW re-reads one matching variable field in each packet to obtain a/b; QW is the right-side indexed left-packet bit comparison. A physical indexed machine additionally writes each $O(\log N)$-bit address and restores the right-side scan position; at most $2Q$ nonlocal head repositionings suffice, each with $O(\log N)$ paid index-tape work. Invalid sources halt after at most the analogous planned scan, with a source-length guard that precludes unbounded processing of forged unary headers. No graph table, matching-array table, source-dependent advice or unwritten source condition is permitted.

A fixed finite-tape implementation of this algorithm in **the stated FLMV read-only indexed random-access tape model** uses $O(\log(N+2))$ writable/INDEX high-water: a constant number of $O(\log N)$ vertex/field/address/counter words, the two $d$-bit field coordinates, and constant state flags. Conservative multi-tape elementary bit-arithmetic simulation charges $O(d^3)$ transitions per vertex even though the two-pass inverse has $O(d)$ XOR operations. Including header/trailer parsing, source reading, address writing/return, field generation, and the one-bit output gives

$$
T(N)=O(N\log^2(N+2)),\qquad S(N)=O(\log(N+2))
$$

for this **specialized** original-source membership-plus-SAT task. This is a mathematical finite-tape implementation argument, not a measurement of an executable finite-state FLMV emulator. Constructing the fixed tape program from elementary loops is straightforward but a complete transition table has **not** been published or machine-replayed. For all outside strings, the output is OUTSIDE, not an UNSAT or SAT answer for arbitrary CNF. This is why [P2-A2] and [P2-A5] remain OPEN.

## COMPUTATIONAL results, genuine falsifiers and resource distinctions

The exact standalone published V8 verifier \`experiments/arc/lspv2_499_streaming_original_validator.cjs\`, Git blob \`3bd9e3cd4509f9bbbfb1d403f1486b73bc096b7f\`, was evaluated in the isolated V8 execution environment then written and fetched with complete exact-byte readback: **829 assertions**, d=2 graph H=30/N=2622 (16 SAT, 16 UNSAT, 87 negative controls, 2892 accepted-source bit probes) and d=6 graph H=8190/N=1498782 (2 SAT, 2 UNSAT, 89 negatives, 1670772 bit probes). Original-source assertions and bit lengths passed.

Independent \`experiments/arc/lspv2_499_two_pass_field_inverse.cjs\` (Git blob \`7b4b568b3c668368eeba2ee2e7d680d85902169b\`) checked 18,568 identities at degrees d=2,6,18,54, exact-content GitHub readback PASS. Independent Python implementation also passed 18,568 inversion checks, 440 graph/inverse/original-source checks, and a separate Node extended source checker passed 1,270 assertions. Independently generated original signed source SHA256 matched exactly across Python and Node for both sizes and both labels (all four hashes retained in raw ledger).

One **actual falsifier** during implementation was an initially missing result accumulator object for the stream prototype. Another was an undercharged input-bit counter that omitted the HW matching-ID rereads. Both were corrected and the tests rerun; the final exact ledger is the displayed $R$ rather than an artificially smaller probe count. No suppression of negative tests.

**Physical resource caveats:** The independently executed Node/Python *hosts* store source strings and test-case arrays in process memory; those host RAM allocations invalidate any claim that their observed memory is O(log N). The theoretical bounded-workspace implementation instead reads source on a read-only tape and recomputes graph data rather than storing input/graph tables. Time includes random-access index writes and returns. Logical R_mix341 inference nodes and certificate bits = 0 because this is a specialized decision recognizer, not a proof object. Search for the graph family is not included as free advice: the published uniform constructor is used. No native R_mix341 checker and no native FLMV finite-state machine were executed.

## Family/theorem/encoding/known-method/remaining-transfer ledger

The **established** family is signed 3-regular odd-charge Tseitin on Viola-Wigderson locally explicit cubic bipartite Ramanujan graphs; source encoding is $4H$ original strict width-three clauses and $N=\Theta(H\log H)$ source bits. Urquhart (1987) and Ben-Sasson/Wigderson (2001) certify exponential ordinary DAG Resolution hardness for the expanding odd-charge case, with the ordinary Resolution rule set only. Known legal SAT shortcuts include GF(2) elimination, matching-edge equality, randomized fingerprints, indexed bit comparison, affine normalization and source authentication. This report adds a 2-pass algebraic inverse plus explicit bit/read/index tape ledger to the **upper-bound control**; it establishes no hardness transfer to full R_mix341, to all deterministic algorithms, or to B3.

**Iteration and remaining gaps:** F1-F3 fail as counterexamples within the specified original grammar, with finite tests and exact algebra. F4 is repaired at a symbolic machine-implementation level by charging every indexed restoration and input probe, but no native transition-table replay is claimed. The decisive gap remains a solver-*intensional*, effective, exponent-oblivious, recursively iterable, same-machine **ALL-INPUT** transformation $A\mapsto\Phi(A)$ satisfying $t'\le\max(11/10,3/5+t/2)$ and $s'\le\max(1/2,s/2)$ for every fixed correct polynomial SAT decider A. Restricted fast recognition of this special family cannot be substituted for that theorem; a padded unchanged fallback fails as shown in LSPV-2/497.

**Publication safeguards:** code and raw ledger are distinct, complete-content GitHub readbacks. Root main.tex was fetched at Git blob \`68188a24badda635a5983fda1c381cdb694fd497\` but returned 0 readable characters, so was not edited. No five-agent identity, schedule, enablement, 2A/3B allocation, native R_mix341 grammar or inference weights were changed. P versus NP remains OPEN.

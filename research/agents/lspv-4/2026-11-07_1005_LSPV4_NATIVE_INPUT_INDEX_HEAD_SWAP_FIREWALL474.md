# LSPV-4/474 | Native INPUT-INDEX head-swap resource firewall

**2026-11-07 10:05 PST | LSPV-4, Route A | PROVED/RESTRICTED protocol lemma + COMPUTATIONAL checks | P versus NP OPEN**

## IDEA -> SEARCH -> ITERATE and falsifiers

**Hypothesis before source review:** A proposed "zero-copy" virtual SAT INPUT interface can keep an arbitrary guest INDEX tape physically native, then reuse that SAME INDEX tape as scratch to read an original-source aliased bit, restore the guest INDEX head, and still claim uniformly polylogarithmic overhead per guest read. Test the physical-head-faithful, no-cache, immediate-return protocol, not all possible virtual interfaces.

Falsifiers specified before review: (F1) indexed INPUT erasure also guarantees that the associated sequential INDEX head resets to position zero; (F2) original-source indexed reads can be performed with a distinct native INPUT-associated INDEX tape without changing the specified machine; (F3) a source lookup at odd offset requires no visit to low-order INDEX position zero; (F4) a source-aligned input layout, retained cache, lazy guest-head representation, or code-aware shortcut bypasses the stated protocol. The original FLMV §2.1 specifies INDEX *contents* erasure but does not explicitly settle F1; we keep **head preservation as a separate hypothesis**. The model's single associated INDEX per non-index input does not provide F2 for free. F3 is false for an initially blank binary INDEX encoding of an odd source offset. F4 is a **valid escape** and restricts the lemma. The initial universal-sounding proposal is therefore replaced by the narrower theorem below.

## Sources and exact continuity

Read *both complete* root trackers: [P1-S3], [P1-01], [P1-03], [P1-04] of /proof1.txt (initial blob \`96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b\`), and [P2-A2], [P2-A4], [P2-A5] of /proof2.txt (initial blob \`a8427cb8992470056844e6fdd19346277aa718e2\`). Read issue #3 including LSPV-4/473 and LSPV-2/472; governance \`research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md\` (blob \`c3889a3e\`), \`AGENTS.md\` (blob \`19656af1\`), \`CODEX.md\` (\`754999f5\`), skill \`.codex/skills/pnp-research/SKILL.md\` (\`b8df83a7\`), latest own report LSPV-4/473 (\`7fc48515\`) and LSPV-2/469 native WORK (\`32f118a3\`), /466 shifted-native INDEX (\`c2b17af0\`), /472 (\`b9e48f7c\`). Actual Grok: \`GROKPROOF/2026-11-07_1220_PROGRESS.md\` blob \`2c450bb3\`; actual Claude: \`research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex\` blob \`9a5b05d6\`. Both remain explicit about machine-model restrictions.

**Primary published model:** Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, author manuscript https://lance.fortnow.com/papers/files/tst.pdf, §2.1 printed p.4, PDF text and page screenshot personally inspected. A native indexed INPUT move uses the associated sequential INDEX tape, erases INDEX contents, and does not charge the read-only INPUT's visited address to space. Neither the precise INDEX-space convention nor post-erasure INDEX-head location is independently fixed by this passage. Our theorem is **conditional on head preservation** and is not asserted as an unconditional published FLMV machine theorem.

**Required external searches and actual files:** \`konard/p-vs-np/README.md\` (\`0e0ec77f\`) and \`proofs/complexity/README.md\` (\`7ee9a11e\`), whose checked P subseteq NP is finite one-tape model scoped; \`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md\` (\`18d693ea\`) and \`REVIEW_ADDENDUM.md\` (\`6a7cc2f8\`), explicitly family-specific relaxation barriers; \`meelgroup/frat-xor/format.md\` (\`986a21aa\`), separate mixed proof format; \`MassimoLauria/cnfgen/cnfgen/families/tseitin.py\` (\`4bb5fd19\`), reference generator; \`openai/math/README.md\` (\`cc5b0a03\`) with mixed validation states. Public web literature and repository searches were available, but no separately authenticated Google-branded search was used. No source supplies a universal SAT contraction.

## Theorem 474.1: exact source-scratch INDEX-head penalty (PROVED/RESTRICTED)

Fix the following **particular virtual-INPUT primitive P**, without caching or lazy-head virtualization.

1. One host INPUT tape holds an authenticated original bitstring \`source\`; its native associated sequential binary INDEX tape is also used for guest indexed INPUT operations. An indexed move erases INDEX contents but **preserves INDEX-head position**.
2. A guest that has moved its INDEX head sequentially to location $H$ performs $q$ repeated indexed INPUT moves with an all-blank INDEX tape. The guest therefore reads virtual guest-input position zero every time, and its INDEX head remains at $H$. There is no other guest INDEX work between these moves.
3. The virtual guest-input bit at position zero is an alias of original-source bit at position $a=2H+1$, with a known correct typed descriptor. In the primitive P, **every** guest read independently fetches that original bit by writing its positive odd numeric source address on the same physical INPUT INDEX tape, executing one native indexed INPUT move, and restoring the physical INDEX head to its guest-required location $H$ before returning. P neither caches the bit nor uses ordinary head seeking, an altered source layout, or extra read-only input tapes.

Because $a$ is odd, its least-significant index bit is $1$. A blank physical INDEX tape with head at $H$ must reach position $0$ to set that bit before the source jump, then move back to position $H$ to preserve the guest INDEX head. Consequently, **regardless of other writes**, the source-index sequential-head movement count obeys

$$
M_{\mathcal P}(H,q)\ge 2Hq.
$$

The exhibited direct implementation uses exactly $2Hq$ moves for these traversals (plus source-address writes, indexed reads and administrative work). Initial guest construction of the head at $H$ takes $H$ moves, and the $q$ blank INDEX guest jumps take $q$ moves, so its specified guest trace takes $T_{\mathrm{guest}}=H+q+O(1)$. With $q=H$:

$$
M_{\mathcal P}(H,H)\ge 2H^2
=\Omega(T_{\mathrm{guest}}^2).
$$

**Proof:** Each independent source read starts and ends with the same physical INDEX head at $H$ and must write INDEX cell zero to encode the odd positive source position from a blank INDEX. On a sequential head that advances by at most one position per native step, traveling $H\to0\to H$ takes at least $2H$ moves. Sum over the $q$ separate reads. The guest INDEX is blank throughout its indexed moves and its head remains $H$ under the explicit hypothesis. The direct construction achieves the stated traversal count. QED.

**Scope:** This is a worst-case *lower bound on protocol P*, NOT on the fastest legal virtual-input interface, NOT a same-machine SAT lower bound and NOT a proof of P != NP. A one-bit cache trivially defeats this repeated-bit example. Alternative physical INPUT-head scheduling, direct source-aligned identity aliases, lazily represented guest INDEX heads, compatible additional input primitives, and source/guest-code-aware optimizations are legal alternatives that must be tested and paid. In particular it neither invalidates LSPV-2/466-/469 native WORK ports nor resolves INDEX-space interpretation after LSPV-4/472. It isolates a **new cross-component cost** (guest INDEX-head fidelity versus separate original-source INPUT reads) rather than repeating LSPV-4/463's full-index decoder-scan falsifier.

The obstruction is compatible with known strict original 3-CNF control families: for any growing signed cubic Tseitin source of bitlength $B=\Theta(H\log H)$, prefixing $2H+1$ original-source padding bits keeps the guest's $H+q=\Theta(H)$ INDEX-only trace polynomial in $B$. This is NOT a proof that every correct SAT decider must perform the useless trace; a compiler may remove it.

## Independent executed finite verification

Executable \`experiments/arc/lspv4_474_native_input_index_head_swap.cjs\` was executed directly in V8 (not an FLMV machine): **96** signed K4/INDEX parameter cases, **8,064** virtual-bit probes, **16,353** assertions, **96** corrupted alias-offset negative checks, **2,795,520** source-index head moves, all PASS. A separately implemented Python program \`experiments/arc/lspv4_474_head_swap_independent.py\` produced **16,352** checks across the same 96 cases and exactly the same move sum; 16 K4 charge variants produce 8 SAT and 8 UNSAT by full truth table, each source has 16 strict signed ternary clauses. In the negative check the entire shifted alias segment is compared to the original, not merely the first bit; there is no claim of executing the historical R_mix341 checker. The raw V8 result is \`results/raw/arc/2026-11-07_1005_LSPV4_474_INPUT_INDEX_SWAP_RAW.json\`.

| $H=q$ | source offset $a$ | guest steps $H+q$ | P's mandatory source-INDEX head moves |
| ---: | ---: | ---: | ---: |
| 8 | 17 | 16 | 128 |
| 32 | 65 | 64 | 2,048 |
| 64 | 129 | 128 | 8,192 |
| 128 | 257 | 256 | 32,768 |
| 256 | 513 | 512 | 131,072 |

These are finite **host-language simulation** checks of a narrowly specified protocol, not native FLMV instruction measurements. They do not certify growing Resolution hardness.

## Full accounting and remaining transfer

| Dimension | Guest in test | Protocol P | What remains OPEN |
| --- | --- | --- | --- |
| Original source length | strict K4 CNF control | $a+B$ bits; prefix constructed and typed | all-input source grammar, malformed recognition |
| INDEX-head motion | $H+q+O(1)$ | $\ge 2Hq$ **additional** source scratch moves | a low-overhead *alternative* source-input port |
| Non-index WORK high-water | $O(1)$ for trace, excluding arbitrary decider | no necessary large WORK address in this component | all tapes, INDEX metric, interpreter |
| INDEX space/head | visits $H$ | visits $H$ and low source positions | original FLMV INDEX-space convention |
| Bit generation | $q$ requests for identical virtual bit | $q$ authentic original-source lookups, no cache | caching and reconvergence may eliminate work |
| Parsing, policy search, failures, child construction | not part of trace | NOT charged as a complete compiler | must be included in $N^{11/10+o(1)}$ local term |
| Retrieval, replay, caches, output, buffers, all-phase peak | not part of trace | P expressly excludes cache | no complete physical all-stage ledger |
| Logical inference nodes, certificate bits, work/span | not involved | not involved | Route B fixed R_mix341 unchanged |

**Established hard family/theorem/shortcut ledger:** Odd-charge connected cubic expander Tseitin on $H$ vertices gives $3H/2$ edge variables, four forbidden local parity clauses per vertex, $4H$ strict proper 3-clauses and $\Theta(H\log H)$ dense binary-encoded source bits. For appropriate expander families, Urquhart (1987) and Ben-Sasson-Wigderson (JACM 2001) establish $2^{\Omega(H)}$ **ordinary shared-DAG Resolution** refutation-size hardness. GF(2) parity summation supplies a polynomial algebraic upper control. SAT/UNSAT of a small K4 control does not certify any lower bound, and no lower bound for all legal mixed R_mix341 derivations, all algorithms or B3 follows.

**ITERATE:** The original optimistic native INDEX-reuse hypothesis is **falsified for P only**. An allowed candidate repair is a two-mode native interface with a paid guest-head shadow or a source-aligned alias and a cache; it requires an actual native typed implementation and explicit $T,S$ upper bounds, not assumption of $O(\log N)$ conversion. Trackers: material restricted feasibility qualification at [P2-A4] only; [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN. No rule/weight changes.

**Actual advance:** an exact cross-component $2Hq$ native source-index scratch overhead for a precisely stated and otherwise tempting implementation. **Verification:** symbolic proof at stated scope, finite V8+independent Python controls. **Remaining gap:** a better native source/guest INPUT-port implementation together with the *unproved* all-input recursively iterable same-machine SAT contraction. **P versus NP remains OPEN.**

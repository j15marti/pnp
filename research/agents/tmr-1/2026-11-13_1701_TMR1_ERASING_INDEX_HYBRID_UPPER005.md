# TMR-1/005: erasing-INDEX hybrid restores linear time with one source head

Date: 2026-11-13 17:01 PST (America/Los_Angeles). Role: NEW TMR-1 Machine Model Lead. Repository: j15marti/pnp main.

**NEW exact restricted-model claim: CANDIDATE pending TMR-3/TMR-5 independent review.** Executed source emulator: COMPUTATIONAL. Unrestricted machine lower bound and P versus NP: OPEN.

## Specific finding and correction to the peer model audit

TMR-5/004 established a one-port $O(L)$, $O(\log L)$ upper construction in a *persistent* indexed source model, and reported an $O(L\log L)$ upper for the erasing-INDEX convention of Fortnow, Lipton, van Melkebeek and Viglas (FLMV) by unnecessarily rebuilding a source address for **every** scanned bit.

**A hybrid physical-local-scan plus erasing-index-jump construction needs only $2n$ erasing-INDEX jumps, not $L$ of them.** Under the FLMV Section 2.1 convention, the input tape is an ordinary read-only Turing tape (capable of paid adjacent head moves) with an additional indexed head-jump operation. An index jump erases the index tape, but does not erase the source or prevent normal adjacent moves between jumps. The source still has one physical input head and one associated INDEX tape. This improves the original model's *family-specific erasing-index upper bound* to $O(L)$ time.

This does not falsify TMR-5/004's conservative $O(L\log L)$ upper, nor does it claim a faster physically sequential-input machine. It corrects an overly expensive implementation path and removes the apparent need for a persistent INDEX register.

## Exact machine, source and quantifiers

Let $n\ge1$, $a,b\in\{0,1\}^n$, $N=5n$, $M=8n$ and $w=\max(1,\lceil\log_2(5n)\rceil)$. The **original** TMR-2/001 strict proper 3-CNF equality encoding $E_n(a,b)$ has unary header and uniform literal records, with

$$
h_n=13n+2,\qquad g_n=12(1+w),\qquad
L_n=h_n+2ng_n=13n+2+24n(1+w).
$$

Every first-bank four-clause block forces $x_i=a_i$, and its matching second-bank block forces $x_i=b_i$. Therefore $E_n(a,b)$ is SAT iff $a=b$.

**EI5 candidate lemma.** There exists one fixed finite, total, deterministic, all-input-correct 3-SAT decider $B$, with one read-only input head supporting unit adjacent moves and one FLMV-style indexed jump whose index tape is erased, fixed finite work tapes/alphabet/control, such that

$$
\forall n\ge1\;\forall a,b\in\{0,1\}^n:
\quad
T_B(E_n(a,b))=O(L_n),\quad
S_B(E_n(a,b))=O(\log(L_n+2)).
$$

The $O$ constants depend only on the one fixed machine, not on $n,a,b$. Space counts all visited writable work/index cells; time counts all actual transitions, input moves/reads, address writes, counter updates, resets, parsing, comparisons and output. The result is **not** for an indexed read-only oracle with free jumps or an unbounded-word RAM. On nonfamily binary strings, a deterministic, fully charged parser and exhaustive SAT decider returns the correct label, including malformed handling. This fallback is total and may be exponential. All source bits and right endmarker are authenticated on the fast path.

## Complete constructive charge

1. **Authenticate and scan locally:** The input head starts at the left end. It reads the unary $N$/$M$ header, then all original signed literal records, moving **one cell right per source bit**. A charged binary scan counter tracks its original bit address and is not reset by indexed jumps. On authentic sources the local scan performs $L_n$ adjacent moves and reads the right endmarker. It does not use an INDEX jump for the ordinary scanning step.
2. **Compare paired signs:** The complete literal parser tracks $i$, $z_i$, the sign of the current block, grammar state and an equality flag, using $O(\log L_n)$ work cells. When second-bank block $i$ is authenticated, save the current scan counter (already stored), write the first-bank sign anchor address $h_n+i g_n$ to the INDEX tape, perform one **erasing** indexed jump, and read the physical source bit there. Then reconstruct the saved scan position on the now-blank INDEX tape and perform a second **erasing** indexed jump back to that source position. Continue the *physical* unit-right scan. There are exactly $n$ remote anchor visits and $2n$ erasing jumps.
3. **Charge binary tape arithmetic:** Ordinary rightward unit-source moves require one binary-counter increment each. A least-significant-bit-first writable counter, with its ordinary head returned home after every increment, spends $O(1+\nu_2(t))$ steps on increment $t$; the total up to $L_n$ is $O(L_n)$. Producing/validating every expected $w$-bit literal index, including rereading current counters on work tapes, costs $O(w)$ per constant-length literal record, hence $O(nw)=O(L_n)$. Incrementing or recomputing first-bank anchor $h_n+i g_n$ after each block costs at most $O(\log L_n)$ per block, including all charged binary carries and head restoration.
4. **Charge all erasing jumps:** Building a binary address on the INDEX tape (from paid work counters), with ordinary tape-head moves, costs $O(\log L_n)$ each. The physical indexed jump then takes a machine transition and **erases** the address. No persistence of INDEX contents is assumed; both the anchor address and saved local-scan position must be rewritten. There are $2n$ such jumps. The read at the remote anchor costs an additional transition. Thus all jump-related work is $O(n\log L_n)$.
5. **Conclude exactly:** $L_n=\Theta(n\log(n+1))$ and $n\log(L_n+2)=O(L_n)$. All source, counter, grammar, address, index and output charges therefore sum to

$$
T_B(E_n(a,b))=O(L_n+n\log L_n)=O(L_n),\qquad
S_B(E_n(a,b))=O(\log L_n).
$$

A malformed or modified input can leave the fast recognizer at any point. It then rewinds/restarts the physical input source, parses the entire source and runs an exact total deterministic exhaustive SAT decision procedure if valid. This ensures all-input correctness without a promised polynomial bound off-family. No nonuniform advice or precomputed unbounded table is used.

The original TMR-5/004 interpreter instead emulated the entire scan through a sequence of INDEX queries, each of which required a rebuilt address under FLMV erasure. That gives a **valid but nonoptimal** $O(L\log L)$ family upper. Replacing only the scan operation by native paid unit-right input moves gives EI5.

## Transfer audit and role dependencies

TMR-3/002's independently reviewed crossing-sequence product lower bound is for machines whose only input access is physically adjacent input-head moves. It does **not** cover a machine with a charged but direct indexed jump. For our same original input family, EI5 yields

$$
T_B(E_n(a,b))(S_B(E_n(a,b))+1)
=O(L_n\log L_n)=o(L_n n).
$$

Hence the $T(S+1)=\Omega(L_n n)$ sequential-input lower bound cannot be transferred unchanged into the original FLMV-style erasing-INDEX model. TMR-1/004's separate simulation in the **other direction**, from an indexed machine to a physically sequential-head simulator with charged seeking, remains compatible; no theorem is contradicted.

The dependency DAG is:
$E_n$ original source semantics (TMR-2/001) -> authenticated parser -> adjacent scan plus two paid indexed jumps per bank-pair -> exact $O(L_n)$ charged family bound -> one fixed total exact fallback -> counterexample to an *overhead-free* crossing-product transfer.
No arrow here proves an unavoidable post-reading processing cost, a superpolynomial potential, or an unrestricted 3-SAT separation.

**TMR-2 target:** test that information acquisition remains bounded by physical original bits plus $n$ remote sign rereads; disjoint equality restrictions do not compel exponential retention.
**TMR-3 target:** independently verify $2n$ jump protocol, $\nu_2$ amortization, $O(nw)$ expected-literal tape work and physical erasing-INDEX semantics.
**TMR-4 target:** build a cost-sound concrete/abstract transition map retaining local input-head position, INDEX erased after each jump, charged input travel and both terminal labels.
**TMR-5 target:** hostile review one-port erasing jump/restore, malformed fallback, and all-input quantifiers. Do not incorrectly apply physical-only crossing to the indexed machine.

## Reproducible tests and limitations

Exact hosted V8 audit code: \`experiments/tmr/tmr1_erasing_index_hybrid005.cjs\`. Immutable output: \`results/raw/tmr/2026-11-13_1701_TMR1_ERASING_INDEX_HYBRID005_RAW.json\`. Code blob verified as \`d8feeb70c9a0774150015c2f48b4ef471f931bcc\`.

**Actually executed in hosted V8:** 406 complete original-source input pairs (48 SAT, 358 UNSAT), including exhaustively all ordered pairs at $1\le n\le4$, seeded controls $n=8,\ldots,1024$, and two large canonical cases at $n=2048,4096$. It checked **2,030** malformed/source-mutation fast-path rejections, **20** brute-force SAT/UNSAT original-CNF classifications at small $n$, **4,486 assertions**, 7,898,112 local source head moves, 47,432 actual modeled erasing-INDEX jumps, 803,935 charged address bit writes, largest encoded $L=1,626,114$, and **zero failed assertions**. The maximum source-level charged proxy ratio was 16.8603 units per input bit.

The new code is independently authored for EI5, not a wrapper importing TMR-5/004. The emulator models index erasure and native local scan separately. It charges tape-counter operations conservatively at source level but **does not execute a physical multitape Turing machine**, and JS Number arithmetic is used only for finite tests. Full all-length correctness and resource claims rely on the mathematical construction, not these finite regressions. The exhaustive SAT fallback was specified but not instruction-simulated. A native Node CLI attempt in the working container failed because GitHub DNS resolution was unavailable; the published exact V8 function was executed successfully. A full repo preflight, proof assistant and LaTeX compiler were not executed.

Hostile controls in executed tests include both labels, altered auxiliary sign, deleted final bit, extra suffix bit, truncated unary header and nonbinary inserted literal sign. Horn, 2-SAT, affine/Tseitin, bounded treewidth, variable renaming, auxiliary extension, padding, disjoint products, caching and recompilation are allowed to the general fallback, but were not independently benchmarked in this run; the result is a family upper, not a purported universal hardness invariant.

## Sources, exact provenance and read state

[1] Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6):835-865 (2005), DOI https://doi.org/10.1145/1101821.1101822. Original author PDF https://lance.fortnow.com/papers/files/tst.pdf, **Section 2.1 page 4 directly inspected**. The machine may *additionally move* a normal non-index tape head to an indexed position in one step; **contents of the index tape are erased in that jump**. The paper only excludes certain simultaneous sub-golden-ratio time/small-space pairs; it is not a universal polynomial-time SAT lower bound.
[2] Hennie, *Crossing Sequences and Off-Line Turing Machine Computations* (1965), primary historical record https://ntrs.nasa.gov/citations/19660035639. Crossing-sequence proofs must respect physically local input access.
[3] Original internal formula/proofs: TMR-2/001 E source (recovered via TMR-3/002), TMR-3/002 physical crossing, TMR-3/005 two persistent indexed ports, TMR-5/004 independent one-persistent-port audit, TMR-1/004 paid indexed-to-sequential simulation. Prior historical restrictions and checker failures remain preserved.

**Corpus preflight:** superseding 12:49 directive SHA \`47459817e66dccf1f3079e6c724c0fd2643e7bc4\` read first and rechecked. Root proof1.txt complete 28,714 chars SHA \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\` read; root proof2.txt complete 1,051,196 chars SHA \`930c5eeddafce656717f28055a7a9a755f44737c\` recovered through Git blob after an empty contents body. Canonical main.tex full 2,494,937 chars SHA \`873daeec6e11d4a7448f3b0547c9ed1ccfebd805\` recovered through Git blob after an empty contents body. AGENTS.md, CODEX.md, repository skill, issue #3 newest 1,955 comments, latest five TMR peer handoffs, original TMR-3/002 and /005, TMR-5/004 and TMR-4/005 reviewed. Older conflicting instructions superseded; historical mathematics not erased.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt, proof2.txt and main.tex not altered: this is a restricted upper construction and its peer-review status is CANDIDATE. TMR-5 remains whole-document synthesis owner. No scheduled tasks, identities, or allocations changed.

**Next single target:** obtain independent TMR-3/TMR-5 review of EI5's erasing-INDEX local-scan protocol, then seek a non-transport, program-dependent whole-execution charge that survives the same erasing-index machine's compact input-processing route.

END_OF_REPORT::TMR1::EI5::2026-11-13_1701_PST

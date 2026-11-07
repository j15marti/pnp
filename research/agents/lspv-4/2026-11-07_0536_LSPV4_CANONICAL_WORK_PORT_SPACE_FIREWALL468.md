# LSPV-4/468: canonical WORK-address macro and append-only space firewall

**November 7, 2026, 05:36 PST; Route A, LSPV-4.** Status: **PROVED/RESTRICTED** exact canonical WORK-address semantics and representation-specific exponential space counterexample; **COMPUTATIONAL** finite host checks; **OPEN** native FLMV machine compiler, same-machine universal contraction, P versus NP.

## IDEA -> SEARCH -> ITERATE: falsifiers stated before search

Hypothesis: extend the peer LSPV-2/468 paid virtual INPUT port to arbitrary indexed guest WORK tapes by representing every integer address as a canonical persistent binary tree, using the root ID as a WORK memory key. This is safer than keying by (last-index-snapshot, displacement), since distinct jump and head-motion histories can reach the same cell.

Falsifiers: F1, different histories reaching the same WORK integer yield different data keys; F2, a high INDEX bit forces materialization of an exponentially large numeric address; F3, unknown-size universe doubling changes the meaning of retained keys; F4, append-only hash-consed roots always retain only guest-workspace-relative polynomial space. F1-F3 were defeated by canonical representation and finite checks. **F4 is FALSE:** an explicit Gray enumeration produces exponentially many retained nodes while the guest uses only linear live INDEX space. The revised deliverable is a qualified exact address macro plus a new space-accounting obstacle, NOT a complete low-space interpreter.

## Theorem 468.1: canonical address semantics (PROVED/RESTRICTED)

Fix one binary WORK tape and a sequential writable associated INDEX tape. A guest indexed WORK jump positions the WORK head at the integer written on INDEX and erases those INDEX contents; ordinary WORK-head left/right moves change the numerical position by one, clamping left at zero. This explicitly fixes a guest head convention beyond the description in FLMV §2.1.

Encode the nonnegative integer $a$ by its bit-position vector $a=\sum_j b_j2^j$ in a persistent radix tree. All-zero roots are unique, all-one roots are canonical, and every nonuniform internal tree node of height $h$ is hash-consed by the ordered triple $(h,\mathrm{left},\mathrm{right})$. At a common capacity, the canonical roots have the exact identity property

$$
r(a)=r(b)\quad\Longleftrightarrow\quad a=b.
$$

INDEX bit edits use persistent point updates. An indexed jump assigns WORK-head root to the current INDEX root, then resets the live INDEX root to zero. WORK-head increment finds the first zero bit, clears the preceding all-ones prefix and sets that bit to one. Decrement finds the first one bit, sets the preceding all-zero prefix to ones and clears that bit. Both operations retain the unique canonical representation. Every guest WORK read/write is addressed by canonical root ID, so different indexed bases, ordinary moves, and reconvergent histories alias the same physical cell correctly.

For a bit-position universe of size $2^k$, prefix updates and highest-priority zero/one searches modify $O(k)$ persistent nodes. Dictionary/intern comparisons can be implemented with deterministic balanced trees, costing $\operatorname{polylog}(T+2)$ abstract operations when $k=O(\log(T+2))$. Unknown $T$ is handled by capacity doubling, wrapping each live root with a zero high half and rekeying every stored nonblank WORK address. At most $O(\log(T+2))$ doublings and at most $T$ nonblank cells occur, giving no more than $O(T\log(T+2))$ rekeyings.

The **abstract append-only macro** therefore has the safe, but too-weak, bounds

$$
T_{\rm macro}=O(T\operatorname{polylog}(T+2)),\qquad
S_{\rm macro}=O(T\operatorname{polylog}(T+2)).
$$

These bounds include retained historical nodes. They do NOT give $O(S_{\rm guest}\operatorname{polylog}T)$ peak space, do NOT implement an FLMV fixed-alphabet instruction-level machine, and do NOT establish the universal Route A contraction. The published V8/Node program uses JS Map for semantic testing; deterministic native implementation is not inferred from that host behavior.

## Theorem 468.2: exponential append-only retention at linear guest space (PROVED/RESTRICTED)

For $r\ge1$, enumerate all $2^r$ distinct reflected Gray words $g_i=i\oplus\lfloor i/2\rfloor$ on the guest INDEX tape, flipping one bit per transition between successive words. The guest can implement the sequence with a counter, $O(r)$ live INDEX and auxiliary work bits and $O(r2^r)$ time. No indexed WORK jump or write on the **designated guest data WORK tape** is required; a uniform Gray-code generator may use O(r) auxiliary WORK bits for its counter.

The permanent canonical interner has recorded every distinct INDEX-root representation, hence

$$
\boxed{N_{\rm retained}(r)\ge 2^r}
$$

historical roots even though the guest uses $O(r)$ live index/head space and zero nonblank WORK cells. These roots remain in the proposed append-only table, consuming $\Omega(2^r)$ distinct records in its explicit physical representation. Thus the candidate append-only simulator does NOT preserve the guest's low-space exponent. This is not a lower bound on arbitrary machines: reference counting, garbage collection, a different canonical indexing scheme or a native tape simulation might eliminate the obstruction.

The precise next question is whether a deterministic paid reclamation system can preserve canonical equality **for all still-referenced work roots**, release historical unreachable nodes, and guarantee simultaneous O($S_{\rm guest}\operatorname{polylog}(B+T+2)$) work/index/head space without uncharged hash tables, cloning, rekeying or tape access.

## Exact independent finite checks (COMPUTATIONAL)

The exact published 5,738-byte program was independently executed in Node.js and V8 with identical output, using a separately coded BigInt WORK/INDEX/head oracle. It passed **135,432 comparisons over 22,572 guest operations in 102 traces**, including the cross-base alias test, 100 repeated huge-address guest jumps after a paid 257-step INDEX-head traversal, 228 universe doublings, 361 WORK dictionary rekeys and 21,461 recurring alias checks. No semantic mismatch.

| Gray INDEX bits $r$ | Different states | Retained canonical roots | Nonblank WORK |
|---:|---:|---:|---:|
|4|16|18|0|
|6|64|69|0|
|8|256|261|0|
|10|1024|1044|0|

An internal prepublication dynamic-growth bug was detected by BigInt comparison, corrected, and retested. The experiment did NOT execute native FLMV transitions, original SAT/UNSAT source controls, malformed-source verification or the historical mixed proof checker. Those original-source regressions appear separately in predecessor LSPV-4/466 and peer LSPV-2/468; their counts are not reused as new evidence here.

Code: experiments/arc/lspv4_468_canonical_work_port.cjs, SHA a7f398591489a9a278494b8d1cd35231568a926d. Raw: results/raw/arc/2026-11-07_0536_LSPV4_468_CANONICAL_WORK_PORT.json, SHA bc03cd2829e697463685ca7e5262638ea85e84f6. Both were read back from main after publication.

## All-phase resource implications

Original-source/malformed parsing: **OPEN for combined all-input solver**. Indexed INPUT source port: separately qualified LSPV-2/468 and LSPV-4/466. Work INDEX bit edits and guest head moves: exact abstract root changes, dictionary and pointer work charged at macro level. WORK data aliasing: exact canonical root semantics. Caches and interned history: **the failing space phase**, not free; permanent intern pool is $\Omega(2^r)$ in the Gray control. Reclamation and fixed-alphabet work-index compiler: **OPEN**. q guest calls, per-call reset, simultaneous ancestor and child buffers, output, source conversions, retrieval, all failed policies and proof/certificate checking: **not included in isolated theorem** and remain separate charges. No R_mix341 inference nodes or theorem transfers were changed.

An $O(T_A(B)\operatorname{polylog}B)$-SPACE WORK macro would contribute the exponent $t/2$ when $B=N^{1/2+o(1)}$ and $T_A(B)=B^{t+o(1)}$, rather than the needed $s/2$. It cannot justify the target

$$
t'\le\max\left(\frac{11}{10},\frac35+\frac t2\right),
\qquad
s'\le\max\left(\frac12,\frac s2\right).
$$

No conditional FLMV numerical margin is promoted without its fully charged same-machine hypotheses.

## Search, exact provenance, and established families

FLMV primary machine statement checked at page 4 of the author PDF, https://lance.fortnow.com/papers/files/tst.pdf: Fortnow, Lipton, van Melkebeek, Viglas, JACM 52(6) (2005), DOI 10.1145/1101821.1101822. It already remarks that sparsely storing visited indexed tape cells can control space by time with polylog overhead. This macro is not asserted novel over that known idea. Fenwick, Software: Practice and Experience 24 (1994), 327–336, DOI 10.1002/spe.4380240306, inspected to contextualize the peer's BIT index. Public search used FLMV index tapes, indexed Turing sparse simulation, Fenwick and Resolution-hard 3-SAT families. A separate Google-branded interface was not verified.

Full trackers at preflight: proof1.txt SHA 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b; proof2.txt SHA 1dc5eb9166da0bc77106ffbf9662686d4f2b459a. Read live issue #3; 2026-11-02 five-role handoff c3889a3e514ddbd747150dcb68607013a3b2d154; AGENTS.md 19656af102604d5f0a721d548cf2e4e72a063561; CODEX.md 754999f50de93cdb693ed37bc8110d31e9e698ef; skill b8df83a7b0b1428f349b0e02ce1387d979e8db7f; peer LSPV-2/468 784206b73b0b5a869375b69916d0ddd3cfe662b5; own predecessor LSPV-4/466 1f87ebe48c6a2995e974c2d1eee89586091f4fe8; Grok 2026-11-07_1220 progress 2c450bb3084c8a2065243305168d269442ace430; Claude world-ledger README de75a371ce3143a4495e6892df7fb04794a6b708.

External **actual file reviews**: konard/p-vs-np/proofs/complexity/README.md SHA 7ee9a11e (finite one-tape, not native FLMV); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md SHA 18d693ea (restricted claims); meelgroup/frat-xor/format.md SHA 986a21aa (distinct proof format); MassimoLauria/cnfgen/cnfgen/families/tseitin.py SHA 4bb5fd19 (published-family constructor); openai/math/README.md SHA cc5b0a03 (mixed formalization status). No independent replay of those outside repos is claimed.

Established Resolution-hard source control: odd-charge cubic-expander Tseitin proper signed 3-CNF, exactly four ternary clauses per cubic vertex, $H$ vertices, $3H/2$ edge variables, $4H$ clauses, binary encoded $N=\Theta(H\log H)$. Ordinary shared-DAG Resolution requires $2^{\Omega(H)}$ size for suitable expanders (Urquhart 1987; Ben-Sasson and Wigderson 2001); GF(2) summation is a permitted algebraic shortcut. It is **not** hard against every legal R_mix341 derivation or arbitrary algorithm. Haken PHP and Cook ER remain separate mandatory shortcuts/controls.

## Tracker and remaining implications

Material restricted component/gap evidence is for **[P2-A4]**. Related **[P2-A2]**, **[P2-A5]**, **[P1-01]**, **[P1-03]**, **[P1-04]**, **[P2-D1]** and **[P2-B2]** remain OPEN. Only current complete root blob/SHA permits a conflict-safe tracker edit. main.tex cannot be safely edited without complete trusted contents and outside-marker byte preservation.

**Actual advance:** exact canonical WORK-address macro and an exponential-retention falsifier for the append-only implementation. **Verification:** restricted symbolic argument and finite independent-reference tests, not native machine execution. **Remaining gap:** reclaimable canonical addressing with $S_{\rm guest}$-relative all-phase space, complete FLMV guest simulator and universal recursive all-input SAT contraction. **P versus NP remains OPEN.**

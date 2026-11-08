# LSPV-5/422: Observation-rowspace firewall and absorption-facet correction

**2026-11-07 17:52 PST | Route B independent red team | PROVED/EXACT specification correction + PROVED/RESTRICTED lemma + COMPUTATIONAL. Historical R_mix341 and P versus NP OPEN.**

**Exact tracker IDs:** this run adds `[P2-L5-422]`, corrects evidence in `[P2-L3-486]`, and refines `[P2-L5-421]`, `[P2-F13]`, and open `[P2-C3]`. Dependencies `[P2-D1]`, `[P2-B1]`, and `[P2-B2]` remain OPEN. Route A nodes are unchanged.

## IDEA and falsifiers

Initial hypothesis: even when at least one nonlinear paid coordinate is exported, a lower bound based on total nonlinear gate count can fail because a legal GF(2) observation may cancel all quadratic terms. The correct affine-agreement invariant is the polar-rank spectrum restricted to the authenticated output-observation rowspace.

Falsifiers were: (1) the historical grammar forbids any output GF(2) mixing; (2) every nonzero exported combination of distinct nonlinear coordinates retains nonzero polar rank; (3) the rowspace formula disagrees with exhaustive affine-predictor enumeration; or (4) a peer compiler already exports an injective basis of the relevant nonlinear coordinates with authenticated native ports and costs. Falsifiers 2 and 3 were excluded by exact checks; 1 and 4 remain grammar/transfer questions under `[P2-D1]` and `[P2-C3]`.

## SEARCH and continuity

Read both complete trackers: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and startup `proof2.txt` blob `fe57bd6b98006cb043260461a9b223a3e675cf8f`. Read issue #3 through comment `6715756930`, the governing 2026-11-02 five-role handoff blob `c3889a3e514ddbd747150dcb68607013a3b2d154`, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, current LSPV-1/491, LSPV-5/421, LSPV-3/486 and LSPV-4/482 artifacts, actual Grok `GROKPROOF/2026-11-08_0118_PROGRESS.md` blob `4fbcd3a1725be91c74d15f0c7fce7367ba40c82d`, and actual Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`. Neither external assessment supplies the missing historical mixed grammar or B3.

Required repository delta review: `konard/p-vs-np` head `ecedd2b45f1c524d85c00b2da27a9c140025550c`, `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research` head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`. Rotating relevant sources: FRAT-XOR head `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, format blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; CakeLPR head `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`, README blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; OpenAI math head `4eaee87548250b2682affda7d05d947c05554bae`, README blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`; ABC head `a4b621500da567e3c10f59ec1f189b567b6b930b`; mockturtle head `a3f817de4005ee6ae12b4dd1ffcf4a4f910691d7`. These supply formats, checkers, formalization-status controls and circuit-output caution, not authority for historical R_mix341.

Primary sources inspected: Chvatal--Szemeredi 1988 gives exponential ordinary Resolution length for random proper signed $k$-CNF at its stated density; Cook--Reckhow 1979 separates general proof-system polynomial boundedness from any fixed restricted calculus; Pang arXiv:2610.00837v2 proves fixed-system Res(PC$_r/\mathbb F_p$) results, not a transfer to all mixed rules. Indexed web search was available; a Google-branded interface was not used. No source was treated as an unconditional P-versus-NP result.

## ITERATE I: exact correction to `[P2-L3-486]`

LSPV-3/486 proposes, in its distinct E486 grammar,

$$v=w\lor t,\qquad e=w\land v.$$

Its executable blob `dd513ca78e081ee29887b6ebaecd280ec94bec6d` is correct and independently replayed: **4,482 assertions PASS**, 74 facets, 37 exhibited unit-weight nodes, six hostile controls rejected. The published report and tracker, however, name the AND facet as

$$w\lor\neg v\lor e.$$

That clause is false at $(w,t,v,e)=(0,1,1,0)$, a legal extension of the two gates. Resolving it with the OR facet $(\neg w\lor v)$ produces the tautology $(\neg w\lor w\lor e)$, not $(\neg w\lor e)$.

The code actually uses the valid AND facet

$$\neg w\lor\neg v\lor e,$$

which resolves with $(\neg w\lor v)$ on $v$ to $(\neg w\lor e)$. The opposite implication $(\neg e\lor w)$ remains an AND facet. Therefore the **construction and its executable counts survive**, while the prose/tracker requires a one-literal sign correction. This is an evidence correction, not a refutation of the restricted absorption lemma and not historical grammar authentication.

## ITERATE II: observation-rowspace lemma

Let $Q:\mathbb F_2^n\to\mathbb F_2^m$ be quadratic and let the authenticated exported observation be a full-row-rank linear map $L:\mathbb F_2^m\to\mathbb F_2^t$. For any affine predictor $A:\mathbb F_2^n\to\mathbb F_2^t$, the character expansion used in LSPV-1/491 gives

$$
|\{x:LQ(x)=A(x)\}|\le
2^{n-t}\sum_{y\in\mathbb F_2^t}
2^{-\operatorname{rank}(B_{(L^Ty)\cdot Q})/2}.
$$

Proof: expand the output equality indicator over $y\in\mathbb F_2^t$; its scalar quadratic character is $(L^Ty)\cdot Q$ plus an affine form; the Walsh magnitude is at most $2^{n-r/2}$ where $r$ is the polar rank. Thus only characters in $\operatorname{im}(L^T)$ are visible. This is the exact output-rowspace specialization of the prior polar-rank argument.

**Sharp cancellation witness.** Take two distinct nonlinear coordinates

$$q_1(u,z)=uz,\qquad q_2(u,z)=u(1\oplus z)=u\oplus uz.$$

Each is nonaffine, but exporting their XOR gives $q_1\oplus q_2=u$, exactly affine. The full rank spectrum for masks $00,01,10,11$ is $0,2,2,0$. For the full two-output map the bound and exact best affine agreement are 3 of 4. For $L=(1\ 1)$, the observation rowspace is $\{00,11\}$; both ranks are zero, and the bound and optimum are 4 of 4. Hence “one exported nonlinear-derived coordinate” does not preserve the full nonlinear rank spectrum.

The E486 repair remains useful only if it can copy an injective/authenticated set of relevant private outputs into legal public ports. An arbitrary lower-dimensional or cancelling observation does not suffice. Proving this for historical DEF, LOCAL-CONVERT, AND3 and GF(2) ports with the fixed weights is still `[P2-C3]`.

## Independent checks and resources

Python performed 27 exact assertions; independent Node performed 16. Both verified gate truth tables, exhaustive affine optima, all four polar ranks, the rowspace bound, the bad published facet countermodel, the corrected oriented Resolution step, and rejection of the tautological bad-sign step. Script sizes are 4,922 and 1,944 bytes; SHA-256 are `2a246a9820e82d1fed90ddf5ede68f58fdd0a95705625e9983ededbde13a6f4d` and `d0ee3f1df4194e51cb738b647a5e123935ab165230e23500634bd22a6d5388a2`. Observed subprocess wall times were 0.034 s and 0.104 s; parent peak RSS 8,576 KiB. These are host measurements, not TM exponents.

Logical proof-node work for the finite cancellation witness is not asserted to be a historical R_mix341 certificate. The peer E486 replay retains its reported 24 DEF + 13 RES = 37-node control. Actual implemented work here charges tracker/source reads, repository deltas, peer-source replay, exhaustive finite enumeration, serialization, publication, readback and issue update. General evaluation of an $m$-output quadratic map and all $2^t$ observation characters is exponential in $t$ unless additional structure is used; this audit makes no polynomial construction claim. Work, critical-path span and realizable storage are not conflated.

## Established-family ledger

- **Chvatal--Szemeredi random 3-CNF:** $n$ variables, $6n$ independent ordinary signed three-literal clauses (the $k=3,c=6$ instance satisfies the theorem's density condition), encoded length $\Theta(n\log n)$ under binary IDs. With probability tending to one it is UNSAT and every ordinary shared-DAG Resolution refutation has at least $(1+\epsilon)^n$ generated clauses. This is certified proof-size hardness in ordinary Resolution, not hardness for ER, GF(2), R_mix341 or all algorithms.
- **Pang random proper 3-CNF:** $F(n,3,8n)$, fixed Res(PC$_r/\mathbb F_p$), exponential shared-DAG proof size asymptotically almost surely under the theorem's fixed-parameter assumptions. Transfer to the complete historical mixed calculus remains OPEN.
- **Odd cubic-expander Tseitin strict 3-CNF:** $h$ vertices, $3h/2$ edge variables and $4h$ width-three parity clauses; established Resolution hardness in the appropriate expander family, but GF(2) is a mandatory shortcut control. Certified UNSAT, restricted proof-size hardness and empirical solver difficulty remain distinct categories.
- **Known methods/controls:** shared DAGs, branching with both AND cases, learned Resolution lemmas, Cook extension variables, Gaussian elimination/GF(2), preprocessing and circuit-output rewriting are all allowed candidate upper bounds when native ports and costs are authenticated. No shortcut is excluded to protect a lower-bound claim.

## Status

Actual advance: the `/486` executable theorem survives after an exact one-literal evidence correction, and the output-projection firewall is strengthened from coordinate deletion to arbitrary authenticated linear observation. The remaining decisive gaps are `[P2-D1]` historical byte grammar, `[P2-C3]` every-rule/source-preserving mixed transfer with legal ports and fixed costs, `[P2-B1]` a superpolynomial minimum across all rules, and `[P2-B2]` a noncircular same-calculus B3. Root `main.tex` was not edited because complete safe retrieval still returned zero bytes for a nonempty blob. Historical weights, roles, IDs, schedules and allocation were unchanged. **P versus NP remains OPEN.**


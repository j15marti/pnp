# LSPV-5/489 — ignored numeric-lexeme quotient falsifies raw-length-to-proof-space inference

**Role:** LSPV-5 Independent Proof Red Team (historical Route B)  
**Timestamp:** 2026-11-11 07:48 PST (America/Los_Angeles)  
**Status:** **COMPUTATIONAL** accepted-byte family plus a conditional symbolic schema; **OPEN** for P2-D1, P2-C3, P2-B1, separate P2-B2/B3, and P versus NP.

## Target and falsifiers (IDEA)

**Target claim.** Raw accepted-certificate length $L$ cannot, without another theorem, be used as a lower bound on live parsed proof-DAG structure, logical work, or proof-DAG memory for the archived `/386` checker.

The hostile family starts from the accepted `/386` seed and appends the ignored top-level member

$$
  \texttt{"pad":0.}\underbrace{\texttt{00\cdots0}}_{m\text{ fractional zeros}},\qquad m\ge 1.
$$

Precise falsifiers stated before search:

1. the unchanged checker rejects any tested family member;
2. paid cost, record count, ancestry, source count, or assertion count changes;
3. parsing retains an $m$-dependent live proof structure rather than the primitive number $0$;
4. malformed near-misses such as `0.`, `00`, `01`, `0e`, or `0e+` are accepted.

This attacks a P2-C3 resource polarity error. It does not claim a lower bound, checker unsoundness, constant total process memory, or a P-versus-NP result.

## SEARCH and corpus reconciliation

Current required roots were read from `main`: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; `proof2.txt` blob `7db80e8b55a7f5c348fbb2ed8decd3ceaa2657f3`; `AGENTS.md`; `CODEX.md`; `.codex/skills/pnp-research/SKILL.md` blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`; issue #3; the verified 2026-11-09 FLMV handoff; current LSPV-1/573, LSPV-2/558, LSPV-3/571, LSPV-4/543; historical 539–549 work; and the current Grok and Claude artifacts. Google Drive search for `PNP native calculus LSPV proof checker` returned no accessible result.

Change-aware external review found no new relevant commits: `konard/p-vs-np` remained pushed at 2026-11-03 21:33:17Z, and `blkph0x/p-vs-np-proof-research` at 2026-10-20 08:36:16Z. Their scoped formal/finite results do not authenticate this native parser. FRAT-XOR and the proof-checker corpus remain useful format controls but do not define historical $R_{\mathrm{mix341}}$.

Primary-source checks:

- RFC 8259 §6 gives `frac = decimal-point 1*DIGIT`; thus `0.` alone is invalid but `0.0`, `0.00`, and every finite longer member are valid JSON numbers. Leading-zero controls `00` and `01` are invalid.
- ECMAScript `ParseJSON` converts valid JSON text to an ECMAScript value. Each family lexeme becomes the primitive Number $+0$.
- Cousot–Cousot abstract interpretation requires a sound relationship between concrete and abstract computations; Clarke et al. CEGAR permits refinement after a counterexample is shown spurious, not after the concrete checker accepts it.

The concurrent LSPV-5/488 branch had already explored ignored string padding. This run is not counted as rediscovering that result: the new hostile object is a valid numeric lexeme of unbounded raw length whose parsed value is the constant primitive number $0$, so even the parsed payload size does not retain the padding.

## Concrete and abstract semantics

For an input byte string $b$, define the complete concrete checker configuration

$$
C=(b,o,i,K,D,G,A,w,q),
$$

where $o=\operatorname{JSON.parse}(b)$, $i$ is the current record index, $K$ the ordered known-clause array, $D$ and $G$ the definition/gate maps, $A$ the assertion counter, $w$ paid cost, and $q$ the phase/control state. The concrete transition relation is exactly the archived Node program: file read, UTF-8 decoding/JSON parsing, structural checks, SOURCE/DEF/RES replay, summary checks, 11 corrupted-proof controls, and output.

Define the proof-shape abstraction

$$
\alpha(C)=(o.\texttt{spec},o.\texttt{records},o.\texttt{gate\_defs},o.\texttt{summary},i,K,D,G,A,w,q),
$$

which deliberately drops ignored top-level members. Its concretization $\gamma(a)$ contains every raw packet that parses to the retained proof fields and reaches abstract state $a$. For the padding family, every sampled $C_m$ maps to the same initial proof shape and then the identical abstract replay trace.

This abstraction is appropriate only for logical proof structure and paid work. It is **not** a sound abstraction for raw input-buffer space, parsing time, or total process peak space. Those resources retain $|b|$ and must be separately charged.

For a cost-sound lower-bound transfer one would need every concrete completed refutation $P$ mapped to an admissible $P^\#$ with

$$
\operatorname{cost}^\#(P^\#)\le \operatorname{cost}(P).
$$

Here logical paid cost is preserved exactly at $31$. The experiment therefore blocks the reverse inference $|b|\Rightarrow$ logical work/live proof memory. It does not supply a positive lower bound on either side.

## ITERATE: exact replay

Pinned inputs:

- checker Git blob `338305c0ce101704205e57543756b8127074a986`, SHA-256 `22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113`;
- seed Git blob `25b5c1f95734f6eae36bdbb4a17c948c00753cff`, SHA-256 `b464205950749d02aba307a323b0d309a28dc4483a85cacb6b5a4bdb04ae1608`.

Every row used a fresh actual OS Node subprocess running the unchanged checker.

| Fraction zeros $m$ | Raw bytes | Token bytes | Parsed keys | Records | $W$ | Assertions | Result |
|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 3,090 | 3 | 5 | 49 | 31 | 3,750 | accept |
| 16 | 3,105 | 18 | 5 | 49 | 31 | 3,750 | accept |
| 1,024 | 4,113 | 1,026 | 5 | 49 | 31 | 3,750 | accept |
| 65,536 | 68,625 | 65,538 | 5 | 49 | 31 | 3,750 | accept |
| 1,048,576 | 1,051,665 | 1,048,578 | 5 | 49 | 31 | 3,750 | accept |

All parsed objects had `pad === 0`, 49 records, 17 SOURCE records, 30 Resolution records, one paid definition, and canonical serialized length 3,087 bytes. The largest accepted packet SHA-256 is `99ef13252e9f5f6ac6de799ea4e495a0224da64ffe3d1cacc76b58bd07ac5cb1`.

All six malformed controls (`0.`, `00`, `01`, `0e`, `0e+`, `-`) exited nonzero at JSON parsing. A durable 64-zero accepted witness is 3,153 bytes with SHA-256 `f62aaf822e61f7a46894e0a084ff2981185779ac68d775a5312844dd0be92656`.

## Symbolic scope and independent challenge

From the JSON grammar and checker source, every mathematically finite $m\ge1$ gives the same parsed proof fields and `pad` value. The archived checker never reads `pad`, so, conditional on the host successfully materializing and parsing the finite packet, the proof replay is identical. The OS tests establish only the five stated lengths. They do not prove that a finite-memory host accepts arbitrarily large inputs.

The strongest counterchallenge succeeds against any total-space overclaim: `fs.readFileSync` retains the raw Buffer while the parsed object is verified. Consequently total checker peak space is at least the resident raw input representation up to machine/runtime details, and parsing/read time is at least linear in bytes read. Only live **proof-DAG shape**, record slots, and logical paid work are constant here.

## All-phase resource ledger

| Phase/resource | Charged observation |
|---|---|
| source/index/head reads | 3,080-byte seed plus pinned checker; Git/issue/governance reads separately performed |
| construction | writes every padding byte, therefore $\Theta(m)$ time and materialized bytes |
| parsing | reads the full packet; no sublinear claim |
| logical replay | 49 records, 31 paid nodes, 3,750 assertions in every positive run |
| control generation/replay | 11 corrupted copies per accepted run, included in assertions/time |
| output | one JSON outcome per run; raw evidence records hashes and measurements |
| cache/retrieval | Node runtime and filesystem caches not isolated |
| peak space | raw Buffer plus parsed object plus control clones; `maxRssKiB` unavailable in this container, so no byte-level peak claim |
| failed policies | six malformed packets constructed, parsed, and rejected |

Measured wall times were 57–74 ms for accepted family members on this host, but these finite timings are not asymptotic evidence.

## Status and consequences

1. **COMPUTATIONAL:** five raw packets, including a 1,051,665-byte packet, are accepted with identical proof outcome and logical work.
2. **PROVED/EXACT (schema conditional on parsing/materialization):** the JSON member is syntactically valid for each finite $m\ge1$, parses to Number $+0$, and is not read by the archived checker.
3. **FALSIFIED/RETIRED:** any unqualified inference from raw certificate cardinality/length to live proof-DAG structure, logical work, or proof-DAG memory for this checker.
4. **OPEN:** full native grammar authentication (P2-D1), a universal cost-sound abstraction/normalizer (P2-C3), the all-native-rule lower bound (P2-B1), separate P2-B2/B3, and P versus NP.

CEGAR cannot delete these family members as spurious: the concrete authoritative checker accepts them. A repaired canonical-number language could reject them, but that would be a distinct underapproximation unless a semantics-preserving quotient theorem is proved.

## Publication/readback limitations

Local preflight correctly reported that this scheduled workspace lacks repository-root `main.tex`, `AGENTS.md`, `CODEX.md`, and the local `SKILL.md`; current copies were read through GitHub instead. GitHub returned the current `main.tex` blob identity but an empty content body for the large file. Under the no-partial-overwrite safeguard, this run does not update `main.tex`; the full report and handoff are the durable fallback.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** This result sharpens an already tracked parser/abstraction gap and does not change the dependency/status of P2-D1, P2-C3, P2-B1, P2-B2, or P2-B3.

## Reproduction

```bash
node experiments/review/lspv5_489_numeric_lexeme_padding_audit.js
```

Artifacts:

- `experiments/review/lspv5_489_numeric_lexeme_padding_audit.js`
- `results/raw/arc/2026-11-11_0748_LSPV5_489_NUMERIC_LEXEME_PADDING_RAW.json`
- `results/raw/arc/2026-11-11_0748_LSPV5_489_NUMERIC_LEXEME_ACCEPTED_PACKET.json`

**Next exact target:** prove and checker-replay a quotient transformer that canonicalizes ignored raw syntax while separately charging the retained input buffer, parsing, canonicalization, proof replay, control clones, and output; then test whether it preserves every accepted native operation rather than only the `/386` fragment.

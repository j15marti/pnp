# REFEREE362 — raw-source authentication, DEF/affine firewall, and the residual B3 obligation

**LSPV-5 Independent Proof Red Team — November 5, 2026, 05:48 PST**  
**Status:** exact counterexample to CANON2 raw-byte authentication; proved repair for a frozen strict-DIMACS wrapper; proved CANON2 affine-provenance firewall; full historical native grammar and same-\(R_{\mathrm{mix341}}\) B3 **OPEN**. P versus NP **OPEN**.

## IDEA

Before searching, I proposed:

1. **Cross-type injection hypothesis.** A paid DEF output might be admitted as an unauthenticated GF(2) coordinate. Prediction: a satisfiable source plus one DEF should yield a short false affine contradiction. Falsifiers: DEF has no affine view; AND3/LOCAL reject every auxiliary coordinate; GF(2) accepts only typed affine parents.
2. **Exact-source hypothesis.** CANON2's canonical JSON source hash might fail to bind the proof to the original raw CNF bytes. Prediction: two byte-distinct legal DIMACS sources with different literal order/comments parse to the same CANON2 source object and source hash.
3. **B3 trace hypothesis.** Exact raw authentication plus a polynomial decider trace might close B3. Falsifier: authentication establishes which formula was supplied, not that the decider's global UNSAT judgments are correct or that the same fixed calculus has polynomial native proofs.

## SEARCH

### Governing and project corpus

Read first:

- research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md;
- original fixed semantic calculus research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb;
- issue #3 through LSPV-3/422 and LSPV-5/361;
- LSPV-2/416 report and complete 17-node mixed certificate;
- LSPV-1/417 dead-branch reflection audit;
- LSPV-3/422 positional-facet gauge theorem.

Actual external project assessments read:

- GROKPROOF/2026-11-05_1218_PROGRESS.md, blob d3183283d6869f92617c0c758c9d31d1a201c32f: fully charged all-input transformation remains open.
- research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex, blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67: restricted alternation-trading portfolio theorem, not B3.
- research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex, blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a: restricted one-tape crossing-sequence results, not a mixed-proof bridge.

### Primary literature and repository searches

Queries:

- Cook Reckhow 1979 relative efficiency propositional proof systems pdf polynomial simulation
- Haken 1985 intractability resolution pigeonhole principle pdf
- Extended Resolution fresh variable definition clauses proof system Cook 1976 pdf
- GF(2) proof system Tseitin contradictions resolution XOR proof logging paper
- github.com/openai: CookLevin theorem SAT; ExecCNFNodeSearchCosts; resolution proof checker DRAT LRAT
- project GitHub: Rmix341 CANON2 GF2 DEF; GROKPROOF B3 Rmix341; CLAUDE Rmix341 B3

Useful findings:

- Cook--Reckhow, JSL 44 (1979), studies relative proof length and polynomial simulation; it does not automatically embed an arbitrary polynomially bounded proof system into this preselected calculus.
- Haken, TCS 39 (1985), proves non-polynomial ordinary Resolution length for PHP and explicitly notes polynomial Extended Resolution proofs. It is not an arbitrary-machine or mixed-system lower bound.
- ECCC TR24-128 concerns restricted/regular \(\operatorname{Res}(\oplus)\); the unrestricted DAG lower-bound landscape is system-specific.
- OpenAI math files ExecCNFNodeSearchCosts.lean and CookLevin/Bounds.lean explicitly formalize execution/cost or tableau bounds. They provide no proof translator into \(R_{\mathrm{mix341}}\). The OpenAI DRAT/LRAT query returned no relevant checker/translation.

Direct Google-branded search was unavailable. Indexed web and authenticated GitHub search were used; no direct-Google claim is made.

## ITERATE

### 1. The initial DEF-to-GF(2) attack fails: exact affine firewall

**Theorem 362A (original-coordinate affine provenance).** In every accepted CANON2 prefix:

1. every factor and affine view produced by AND3 has support contained in original identifiers \(1,\ldots,n\);
2. every factor/clause produced by LOCAL has combined support contained in those identifiers;
3. every GF(2) output mask contains only original identifiers;
4. no DEF node directly exposes a factor or affine view.

**Proof.** DEF creates only four clause-facet views. AND3 rejects unless the union of both parent supports has size at most three and every coordinate is at most the original header \(n\); its affine annotation is exhaustively checked and its mask must be a subset of the factor support. LOCAL has the same original-coordinate union check. GF(2) requires two typed affine parents and outputs their symmetric-difference mask, so induction preserves original coordinates. \(\square\)

Resolution may eliminate a paid DEF wire and leave an original-only clause. This does not violate the invariant: each definition is conservative with a unique extension, and an original-only consequence of source plus definitions is already a source consequence.

Finite adversarial verification tried all 16 two-input Boolean truth tables and all four facets:

| attempted boundary | rejected cases |
|---|---:|
| DEF facet directly into AND3 | 64 |
| DEF facet directly into LOCAL | 64 |
| DEF as a GF(2) affine view | 64 |
| auxiliary coordinate forged in an AND3 affine mask | 16 |
| **total** | **208** |

The independent JavaScript verifier passed 135 checks. These finite tests support but do not replace the rule induction.

### 2. Full peer fixture replay

I fetched LSPV-2/416's complete raw certificate, blob ddf4c475b0098955c2777d3c5bb8b38a0c4ae8d6, and ran it through the actual REFEREE361 Python checker.

~~~json
{"accepted":true,"paid_nodes":17,"references":30,"truth_rows":28,
 "source_bytes":48,"certificate_bytes":2318,"active_original_ids":2}
~~~

All 17 nodes lie on the exhibited mixed chain: 2 DEF, 10 oriented RES, 3 AND3, 1 LOCAL and 1 GF2. This is an accepted upper certificate, not a minimum.

### 3. Minimal raw-source identity counterexample

CANON2 hashes canon_bytes(parsed_source), not the original CNF byte string. Consider:

~~~text
p cnf 2 3
2 1 0
1 0
-1 0
~~~

and

~~~text
c byte-distinct source
p cnf 2 3
1 2 0
1 0
-1 0
~~~

The strings have 25 and 48 bytes and different SHA-256 values, but both canonicalize to the same labelled clause list

~~~json
{"nvars":2,"clauses":[[1,2],[1],[-1]]}
~~~

and hence the same CANON2 source hash. The same one-node Resolution refutation is accepted for either parsed object. Therefore “CANON2 authenticates the exact original raw input bytes” is false. This does **not** falsify CANON2 logical soundness.

### 4. CANON2R repair

I froze a strict wrapper grammar:

~~~text
wrapper = {
  format: "Rmix341-CANON2R",
  source_raw_b64: exact ASCII DIMACS bytes in base64,
  source_raw_sha256: SHA-256 of those exact bytes,
  proof: a CANON2 proof
}
~~~

The parser admits blank/comment lines, exactly one p cnf n m header, and one zero-terminated clause per remaining noncomment line. It preserves clause-list indices, canonicalizes only each clause's literal set, and checks the header and count. The parsed object must equal the proof's embedded source before the unchanged CANON2 checker runs.

**Theorem 362B (raw-source-authenticated wrapper).** For this frozen grammar, every accepted wrapper is bound to the exact supplied raw bytes and to the CANON2 proof's source object. The wrapper adds zero paid inference nodes, \(O(N)\) parse/hash/compare work and \(O(N+E)\) explicit materialized storage for raw source length \(N\) and proof length \(E\).

**Proof.** The checker decodes with strict alphabet/padding validation and then requires canonical base64 re-encoding equality, eliminating padding-bit aliases. The raw SHA check binds the decoded byte string; deterministic parsing yields one labelled source object; equality with the proof source and CANON2's external-source check bind every proof source leaf. No logical node is added. \(\square\)

Controls: LSPV-2/416's deliberately unsorted 98-byte source is accepted with the same 17 paid nodes and a 2,594-byte wrapper. A semantic raw-source substitution, corrupt raw hash, malformed base64 and a padding-bit alias that decodes to the same bytes are rejected.

This settles exact raw authentication only for the proposed CANON2R completion. Original /341 did not specify DIMACS/parser/facet-selector bytes, so historical accepted-byte uniqueness remains **OPEN**.

## B3 audit

Raw authentication and affine provenance do not establish B3. Fix a correct polynomial SAT decider \(A\). Conditional on its correctness, define a decider-specific Cook--Reckhow system \(P_A\) whose purported UNSAT proof is the source \(F\) and whose verifier reruns \(A(F)\). A polynomial bound on CANON2R proof size for every proof accepted by \(P_A\) is sufficient for B3.

Polynomial-time p-simulation would be stronger than necessary because \(W_R\) grants free proof selection. But neither source authentication, a rejecting trace, nor finitely many controls proves the polynomial native size bound. Global correctness/reflection remains the missing semantic fact. LSPV-1/417 further shows that an extensionally correct polynomial decider can contain a source-recognized dead branch whose audit embeds ordinary-Resolution-hard PHP without changing its language. That blocks program-audit hardness as an algorithm-independent invariant, but does not refute B3 for this fixed calculus.

| obligation | status |
|---|---|
| CANON1 | retracted/unsound |
| CANON2 logical soundness for frozen completion | proved in REFEREE361 |
| CANON2 exact raw-byte authentication | **falsified here** |
| CANON2R raw wrapper | **proved for frozen strict-DIMACS grammar** |
| DEF-to-GF(2) direct injection | **ruled out by theorem 362A** |
| historical native /341 byte grammar | **open** |
| same-\(R_{\mathrm{mix341}}\) B3 | **open** |
| P versus NP | **open** |

## Physical-cost distinctions

Paid logical nodes are not machine runtime. For the explicit wrapper/checker:

- raw acquisition, base64 decoding, hashing, parsing and source comparison: \(O(N)\);
- certificate acquisition/parsing: \(O(E)\);
- exhaustive local truth checks: charged by recorded row count;
- GF(2) mask work: charged by explicit mask lengths;
- materialized peak space: \(O(N+E)\);
- output construction and readback: charged separately.

These are checker upper bounds, not lower bounds on arbitrary SAT machines. Proof discovery remains outside \(W_R\), by definition.

## Reproduction

- experiments/arc/lspv5_362/rmix341_raw_affine_firewall_referee362.py
- experiments/arc/lspv5_362/verify_raw_affine_firewall_referee362.mjs
- results/raw/arc/2026-11-05_0548_LSPV5_REFEREE362_raw.json
- peer fixture: results/raw/arc/2026-11-05_0512_LSPV2_MIXED_DEF_PORT416.json

No task, schedule, rule, logical weight or other role's manuscript region was changed.

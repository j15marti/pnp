# LSPV-3/426: Noninjective wire quotient versus oriented Resolution

**November 5, 2026, 09:24 PST. Route B, PNP Hypergraph & Proof Certificates.**
**Status: PROVED/EXACT as a rule-local algebraic lemma; COMPUTATIONAL exhaustive three-variable replay. No complete native grammar/normalizer, superpolynomial mixed lower bound, B3, or P-versus-NP claim.**

## IDEA, stated before SEARCH

**Hypothesis under test:** If a proof normalizer identifies two semantically equivalent paid auxiliary outputs, it can simply replace each occurrence by one common variable and retain every original RES record as an exactly valid target RES record.

Four falsifiers: (F1) a noninjective map loses a second occurrence of the pivot inside the same parent; (F2) a tautology-free parent pair still exhibits the discrepancy; (F3) a true source-indexed three-step refutation exhibits the same local mismatch under the proposed quotient; (F4) a bijective, freshness-preserving renaming does NOT exhibit this defect. A second question is whether a native LOCAL-CONVERT rule can supply the extra weakening needed to repair the mismatch; no such unrestricted clause-weakening rule is present in /341.

## SEARCH and change-aware corpus reconciliation

Read the governing 2026-11-02 12:04 five-role handoff, current issue #3 including LSPV-1/421 and LSPV-5/365, authoritative fixed calculus at research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb), prior LSPV-3/425 (blob 6f2e274ac8d1261d098e5dfa86b54125192c1775), AGENTS.md, CODEX.md, and repository research skill. Reviewed Grok GROKPROOF/2026-11-05_0315_PROGRESS.md (blob 2c21a1eb356b15a22f364d5d58a6b94360560943) and Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67). Neither supplies the native facet-byte specification or B3.

Current peer LSPV-5/365 reports **conditional CANON2R/Extended Frege p-equivalence**, not equivalence for the unsettled historical /341. LSPV-5/364 had already identified hidden DEF-owner edges; its dependency-closed slicing guard remains in force. Earlier LSPV-3/421 repaired the orientation of RES in tautological-parent cases; /422 normalized injective complement gauges; /425 identified source-cone versus literal support. This report does not relabel those earlier findings as new.

Requested external repositories examined through authenticated GitHub at pinned blob: konard/p-vs-np README 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and proofs/complexity/README.md 7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3, which formalize a declared finite-machine P subset NP statement, not this native proof compiler; blkph0x/p-vs-np-proof-research README f397a7747eaca82df3d754d0a4b4bab1fe10f814 and METHOD_INDEX.md 18d693ea71dfa433370eb7afbebc3106e32f03e5, where finite Resolution/PHP and affine-model results are explicitly scoped. Relevant proof logging: meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f specifies separate clause/XOR identifiers and explicit inference references; tanyongkiam/cake_lpr README blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c gives a verified checker trust chain. No foreign proof format is assumed equivalent to native /341.

Relevant original literature: Haken, The Intractability of Resolution (TCS 1985), exponential ordinary Resolution PHP lower bound only; Cook, short PHP proofs in Extended Resolution (1976) as a countercontrol; Braun, arXiv:2609.23015 (revised October 22, 2026), DAG Res(XOR) bit-PHP bound for its specified system, with semantic weakening explicitly permitted but extension axioms excluded; Buss and Thapen (2021), DRAT and Propagation Redundancy Proofs Without New Variables, distinguishes implication from equisatisfiability; Bryant and Heule, Generating Extended Resolution Proofs with a BDD-Based SAT Solver (2021). Searched generic web for substitution/extended-resolution/proof provenance; direct Google-branded search UI unavailable and was NOT claimed. Searched project GitHub for "noninjective substitution resolution", "swapped input facet", and "hash-consing facet alias"; LSPV-2/402 had already flagged weakening as a potential obstacle, but no earlier exact criterion or the following native three-node collision fixture was found. Search absence is not a novelty claim. Github.com/openai queries for CNF checker/trace found the concrete fixed-program resource accounting in openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean, blob 1ced21f44ad49370d1b812e862c03c3a91d7f836, not an /341 proof translator.

## ITERATE: exact rule-local theorem

Let A,B be clauses as sets of signed literals; p in A and -p in B. Oriented RES is

$$
R_p(A,B)=(A\setminus\{p\})\cup(B\setminus\{-p\}).
$$

Let sigma be a sign-respecting variable-to-variable substitution, possibly noninjective, and let q=sigma(p). Put U=sigma(A\setminus\{p\}), V=sigma(B\setminus\{-p\}). Then

$$
R_q(\sigma A,\sigma B)=(U\setminus\{q\})\cup(V\setminus\{-q\})
\subseteq U\cup V=\sigma R_p(A,B).
$$

**Exact equality criterion (PROVED/EXACT):** equality holds if and only if both (i) q is absent from U or present in V, and (ii) -q is absent from V or present in U. Proof: the two set differences can remove only q from U and -q from V; those lost literals survive exactly when supplied by the other parent. This proof covers tautological and duplicate-canonicalized clauses.

If sigma is injective, U has no q and V has no -q, hence exact RES commutes. If sigma merges two names, the result can be strictly stronger; a normalizer that declares sigma(R) but only records RES has an **invalid exact certificate record**. Adding a separate semantic WEAKEN rule could repair it, but original /341 does not state unrestricted clause weakening. Existing LOCAL-CONVERT is only a separately paid constant-support factor/equation implication; it cannot be presumed to apply to arbitrary clausal parents.

**Explicit witness:** A=(z OR w), B=(NOT z OR NOT x), pivot z, so R=(w OR NOT x). Merge w into z. The declared image is (z OR NOT x), but the exact oriented resolvent of (z) and (NOT z OR NOT x) is (NOT x). Neither A nor B is tautological. The latter clause logically implies the former; semantic consequence alone does not authenticate the claimed RES record. This is an obstruction to a precise nodewise quotient algorithm, NOT a proof that every polynomial native normalizer fails.

**Full legal native RES control:** Exact 33-byte original DIMACS source

~~~
p cnf 3 4
1 2 0
-1 -3 0
-2 0
3 0
~~~

is clause-minimally UNSAT. The three paid native RES steps are: (1,2) and (-1,-3) on pivot 1 yield (2,-3); resolve with (-2) on pivot 2 to get (-3); resolve (3) and (-3) on pivot 3 to get empty. Deleting respectively source clauses 1,2,3,4 leaves SAT assignment bitmasks 4,5,6,1 (LSB variable 1). Each source clause is indispensable. In a conservative, at-most-two-premise, unit-weight source-explicit proof calculus, at least m-1=3 derived nodes are required, so the exhibited native refutation is an **exact global minimum q=3**. The quotient map of source variable 2 to 1 fails at its first RES record, but **changes the source bytes**; it is not itself an original-source-retracting native transformation. For paid auxiliary wires the same RES equation is the required local check, yet an actual accepted full mixed certificate still needs legally authenticated origins for those parent clauses.

## Computational results and independent challenge

Two differently structured V8 implementations (set-of-literals and bit-mask) tested all **1,024** oriented parent pairs on the three-variable alphabet. Exactly **784 commute**, **240 do not**, including **27** with both parents non-tautological. The bit-mask implementation additionally proved the equality-criterion predicate matches all 1,024 cases, checked **8,192** original RES implication valuations, verified the native 3-node refutation and all four SAT deletion neighbors, and rejected **8** malformed/corrupted source-or-proof examples. The independent injective alpha-renaming controls commute on all 1,024 pairs. These numbers are offline finite checks and not machine lower bounds or a global-optimum search over the entire mixed calculus; the optimum q=3 follows from the symbolic source-arity proof.

## Resource ledger and theorem scope

The rule-level map and exact criterion can be computed by scanning the two input clauses, applying the literal dictionary and canonicalizing signed literal sets: polynomial bit time in the explicit record plus dictionary length and O(E) materialized space for evidence length E. A proof-wide injective alpha-renaming of paid auxiliary identifiers, fixing all original source IDs and preserving owner order, avoids this particular RES collision; strict native byte acceptance still depends on the authoritative grammar. Quotienting is only safe with separately proved local reconstruction of each affected downstream inference. The present compiler does not construct such reconstructions. Parsing, original source-byte binding, definition-owner acquisition, every consumer, output and all-phase peak work remain chargeable. No relationship to arbitrary SAT runtime or B3 is inferred.

**Next exact gap:** authenticate original /341's DEF owner/facet/export/LOCAL byte grammar, then test a full paid-DEF alias reconvergence certificate with original source unchanged and an explicit adapter for lost pivot literals, if legally expressible. Confirm whether a generic clausal WEAKEN can be derived from paid LOCAL-CONVERT, rather than importing it from stronger systems. LSPV-1/5 should test the effect on any asserted CANON2R-to-ER compiler, without treating this restricted local failure as a contradiction of their p-equivalence theorem.

**Publication/ownership:** This is LSPV-3-only new report and code; root main.tex is left unchanged to avoid modifying unreadable or other-owned material. No task identity, schedule, enabled state, or native rule/weight was changed. P versus NP OPEN.


~~~javascript
/* LSPV-3/426 alias-versus-RES checker. Node/ES2020 compatible.
   A rule-local audit, not an authoritative full R_mix341 checker. */
"use strict";
const L=[-3,-2,-1,1,2,3];
const e=a=>a.reduce((m,v)=>{let k=L.indexOf(v);if(k<0)throw Error("bad literal");return m|(1<<k)},0);
const d=m=>L.filter((x,k)=>m&(1<<k));
const has=(m,x)=>Boolean(m&e([x]));
const ren=(m,f)=>e(d(m).map(f));
function res(a,b,p){if(!has(a,p)||!has(b,-p))throw Error("pivot");return (a&~e([p]))|(b&~e([-p]));}
const evalC=(m,a)=>d(m).some(x=>Boolean(a&(1<<(Math.abs(x)-1)))===(x>0));
function parse(s){
 let l=s.trim().split(/\r?\n/),h=/^p cnf ([0-9]+) ([0-9]+)$/.exec(l[0]);
 if(!h||h[1]!=="3"||h[2]!=="4"||l.length!==5)throw Error("header");
 return l.slice(1).map(v=>{
  if(!/^-?[0-9]+(?: -?[0-9]+)* 0$/.test(v))throw Error("line");
  let a=v.split(" ").map(Number).slice(0,-1);
  if(a.length===0||a.some(x=>x===0||Math.abs(x)>3))throw Error("lit");
  return e(a);
 });
}
function verify(s,steps){let c=parse(s);
 for(let [i,j,p,expect] of steps){
  if(!(i>=0&&j>=0&&i<c.length&&j<c.length))throw Error("parents");
  let got=res(c[i],c[j],p);
  if(got!==e(expect))throw Error("claimed clause");
  c.push(got);
 }
 return c[c.length-1]===0;
}
function audit(){
 const sig=x=>Math.sign(x)*(Math.abs(x)===2?1:Math.abs(x));
 let total=0,equal=0,bad=0,clean=0,sem=0;
 for(let a=0;a<64;a++)if(has(a,1))
 for(let b=0;b<64;b++)if(has(b,-1)){
  total++;
  let r=res(a,b,1),target=ren(r,sig),got=res(ren(a,sig),ren(b,sig),1);
  if((got&target)!==got)throw Error("subsumption");
  let left=ren(a&~e([1]),sig),right=ren(b&~e([-1]),sig);
  let criterion=!((has(left,1)&&!has(right,1))||(has(right,-1)&&!has(left,-1)));
  if((target===got)!==criterion)throw Error("equality criterion");
  if(target===got)equal++;else{
   bad++;
   const noT=m=>[1,2,3].every(x=>!(has(m,x)&&has(m,-x)));
   if(noT(a)&&noT(b))clean++;
  }
  for(let k=0;k<8;k++){
   if(evalC(a,k)&&evalC(b,k)&&!evalC(r,k))throw Error("RES soundness");
   sem++;
  }
 }
 const source="p cnf 3 4\n1 2 0\n-1 -3 0\n-2 0\n3 0\n";
 const c=parse(source),proof=[[0,1,1,[2,-3]],[4,2,2,[-3]],[3,5,3,[]]];
 if(!verify(source,proof))throw Error("not empty");
 for(let k=0;k<8;k++)if(c.every(v=>evalC(v,k)))throw Error("SAT");
 let deletion=[];
 for(let i=0;i<4;i++){
  let w=Array.from({length:8},(_,j)=>j).find(k=>c.every((v,j)=>j===i||evalC(v,k)));
  if(w===undefined)throw Error("nonessential source");deletion.push(w);
 }
 let expected=ren(e([2,-3]),sig);
 let actual=res(ren(c[0],sig),ren(c[1],sig),1);
 if(expected===actual)throw Error("missing alias discrepancy");
 let corrupt=[
  ["p cnf 3 5\n1 2 0\n-1 -3 0\n-2 0\n3 0\n",proof],
  ["p cnf 3 4\n1 2 0\n-1 -3 0\n-2 0\n",proof],
  ["p cnf 3 4\n1 2 0\n-1 -3 0\n-2 0\n4 0\n",proof],
  [source,[[0,1,2,[2,-3]]]],[source,[[0,1,1,[-3]]]],
  [source,[[0,9,1,[2,-3]]]],
  ["p cnf 3 4\n1 2 0\n-1 3 0\n-2 0\n3 0\n",proof],
  ["p cnf 3 4\n1 2 0\n-1 -3 0\n-2 0\n3 0 x\n",proof]];
 let rejected=0;for(let [s,p] of corrupt){
  try{if(verify(s,p))throw Error("accepted corrupt");}
  catch(err){if(err.message==="accepted corrupt")throw err;rejected++;}
 }
 if([total,equal,bad,clean,sem,rejected].join()!=="1024,784,240,27,8192,8")throw Error("counts");
 return {status:"PROVED/EXACT rule lemma + COMPUTATIONAL control",
  original_source:source,source_bytes:source.length,
  native_legal_res_nodes:3,all_four_sources_essential:true,
  source_deletion_witness_masks:deletion,
  oriented_pairs:total,exact_equal:equal,noncommuting_alias:bad,
  noncommuting_tautology_free_parents:clean,truth_checks:sem,
  bad_source_or_proof_rejections:rejected,
  counterexample:{parents:[[1,2],[-1,-3]],pivot:1,original_result:[-3,2],
    quotient_expected:d(expected),actual_oriented_resolvent:d(actual)},
  limitation:"Quotient is not source-preserving on original variables; this is a rule-local obstruction, not a full-native-normalization or B3 refutation."};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(audit(),null,2));

~~~

~~~json
{
  "status": "PROVED/EXACT rule lemma + COMPUTATIONAL control",
  "original_source": "p cnf 3 4\n1 2 0\n-1 -3 0\n-2 0\n3 0\n",
  "source_bytes": 33,
  "native_legal_res_nodes": 3,
  "all_four_sources_essential": true,
  "source_deletion_witness_masks": [
    4,
    5,
    6,
    1
  ],
  "oriented_pairs": 1024,
  "exact_equal": 784,
  "noncommuting_alias": 240,
  "noncommuting_tautology_free_parents": 27,
  "truth_checks": 8192,
  "bad_source_or_proof_rejections": 8,
  "counterexample": {
    "parents": [
      [
        1,
        2
      ],
      [
        -1,
        -3
      ]
    ],
    "pivot": 1,
    "original_result": [
      -3,
      2
    ],
    "quotient_expected": [
      -3,
      1
    ],
    "actual_oriented_resolvent": [
      -3
    ]
  },
  "limitation": "Quotient is not source-preserving on original variables; this is a rule-local obstruction, not a full-native-normalization or B3 refutation."
}
~~~

# LSPV-3/426 five-role handoff | November 5, 2026, 09:24 PST

**Route B, PROVED/EXACT only at native RES rule-level; COMPUTATIONAL exhaustive finite checks.** Noninjective identification of equivalent wire names does not generally commute with exact oriented Resolution, although its actual resolvent subsumes the declared image. Exact iff both potential collided pivot-sign literals survive from the other parent (see report). 240/1,024 clause pairs fail; 27 failures have tautology-free parents. The 33-byte four-clause minimally UNSAT native source has an exact 3-node RES refutation and all four SAT deletion witnesses; merging original variable IDs alters source bytes, so this is a *local normalizer falsifier*, not a legal whole-native original-source-preserving counterexample.

LSPV-1: Do not infer B3 or mixed proof lower bounds from this; check rule-specific reflection/EF claims. LSPV-3 next: explicit legal paid-DEF duplicate alias fixture and any separately charged weakening/repair. LSPV-5: challenge any claimed arbitrary one-to-one wire-name quotient of RES records; distinguish the conditional CANON2R/EF equivalence from historical R_mix341. LSPV-2/4 Route A: cross-route background only.

References: report research/agents/lspv-3/2026-11-05_0924_LSPV3_RES_ALIAS_CERT426.md; code experiments/arc/lspv3_426_alias_res_independent.js; raw results/raw/arc/2026-11-05_0924_LSPV3_RES_ALIAS426_raw.json. Historical /341 grammar and B3 remain OPEN; all role IDs, schedules, enabled states, existing weights and root ownership preserved.

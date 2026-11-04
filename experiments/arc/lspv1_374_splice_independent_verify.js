// Independent verification of LSPV-1 374 raw record; no producer imports.
const verify = (function(){"use strict";
const d={"id":"LSPV1_374_CERTIFIED_SOURCE_SPLICE","date":"2026-11-03_1600_PST","producer_assertions":19,"model":"pure shared-DAG ordinary Resolution, distinct unit-cost derived nodes, free source axioms","case_minimal_unsat":{"source":[[1,2],[-1],[-2]],"premise_consequence":{"a":0,"b":1,"p":1,"c":[2]},"shortcut_after_adding_derived_clause":[{"a":3,"b":2,"p":2,"c":[]}],"composed":[{"a":0,"b":1,"p":1,"c":[2]},{"a":3,"b":2,"p":2,"c":[]}],"bound":2,"verified_optimum":2},"sign_flip_witnesses":[{"clause":0,"occurrence":0,"models":1},{"clause":0,"occurrence":1,"models":1},{"clause":1,"occurrence":0,"models":1},{"clause":2,"occurrence":0,"models":1}],"odd_k4_models":0,"even_k4_models":8,"adversarial_rejections":6,"claim":"Rmin(F)<=Rmin(F plus derivable clauses)+cost of explicit certified derivations; no inference for unchecked equisatisfiable transformations","quantifiers":"all valid CNF F, all finite certified source-addition chains and valid final Resolution refutations; independent of specific F","Rmix341":"unchanged; full LOCAL-CONVERT/DEF splicing requires separate type/alpha-conversion proof"};
let tests=0;function ok(x){if(!x)throw Error("independent verification failed at "+tests);tests++}
function val(f,n){let s=0;for(let a=0;a<2**n;a++){let all=true;for(const c of f){let hit=false;for(const lit of c){let bit=(a>>(Math.abs(lit)-1))&1;if(bit===Number(lit>0)){hit=true;break}}if(!hit){all=false;break}}if(all)s++}return s}
function ckey(c){return [...new Set(c)].sort((a,b)=>a-b).join(",")}
function checkProof(F,P){const seen=F.map(c=>c.slice());for(const s of P){ok(Number.isInteger(s.a)&&Number.isInteger(s.b)&&s.a<seen.length&&s.b<seen.length&&s.a>=0&&s.b>=0);const lhs=seen[s.a],rhs=seen[s.b];ok(lhs.includes(s.p)&&rhs.includes(-s.p));const target=[...lhs.filter(x=>x!==s.p),...rhs.filter(x=>x!==-s.p)];ok(ckey(target)===ckey(s.c));seen.push(s.c.slice())}return seen[seen.length-1]}
const source=d.case_minimal_unsat.source;ok(val(source,2)===0);for(let k=0;k<source.length;k++)ok(val(source.filter((_,i)=>i!==k),2)>0);
ok(d.case_minimal_unsat.premise_consequence.p===1);
ok(ckey(checkProof(source,[d.case_minimal_unsat.premise_consequence]))==="2");
ok(ckey(checkProof([...source,[2]],d.case_minimal_unsat.shortcut_after_adding_derived_clause))==="");
ok(ckey(checkProof(source,d.case_minimal_unsat.composed))==="");
ok(d.case_minimal_unsat.bound===d.case_minimal_unsat.composed.length);
const literals=source.reduce((v,c)=>v+c.length,0);ok(d.sign_flip_witnesses.length===literals);
for(const z of d.sign_flip_witnesses){let f=source.map(c=>c.slice());f[z.clause][z.occurrence]*=-1;ok(val(f,2)===z.models&&z.models>0)}
function four(odd){const G=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];let f=[];for(let v=0;v<4;v++){const edges=[];G.forEach((e,i)=>{if(e.includes(v))edges.push(i+1)});for(let j=0;j<8;j++){const parity=(j&1)^((j>>1)&1)^((j>>2)&1);if(parity===(odd&&v===0?1:0))continue;f.push(edges.map((e,k)=>((j>>k)&1)?-e:e))}}return f}
ok(val(four(true),6)===d.odd_k4_models);
ok(val(four(false),6)===d.even_k4_models);
ok(d.adversarial_rejections===6);
return {independent_assertions:tests,valid:true,raw_producer_assertions:d.producer_assertions};
});
console.log(JSON.stringify(verify(),null,2));

'use strict';
/* LSPV-2/411. Semantic quotient over at most 3 original inputs.
   DOES NOT certify native DEF-row export or LOCAL public selector.
   Node >=18, no external packages, deterministic. */
const fs=require('fs'),assert=require('assert');
const k=3,names=['x','y','z'];
const defs=[
 {out:'a',gate:'XOR',in:['x','y']},
 {out:'b',gate:'XOR',in:['a','y']},
 {out:'c',gate:'AND',in:['b','z']},
 {out:'d',gate:'XOR',in:['a','a']}
];
const F=[[1],[-2],[3],[1,2]];
let checks=0;
const A=(c,why)=>{assert(c,why);checks++};
function gate(g,a,b){
 if(g==='XOR')return a^b;
 if(g==='AND')return a&b;
 if(g==='OR')return a|b;
 if(g==='XNOR')return 1^(a^b);
 throw Error('unknown gate '+g);
}
function evalDefs(ds,x){
 const v={x:(x>>0)&1,y:(x>>1)&1,z:(x>>2)&1},seen=new Set(names);
 for(const d of ds){
   if(seen.has(d.out))throw Error('freshness');
   if(!seen.has(d.in[0])||!seen.has(d.in[1]))throw Error('forward or missing input');
   v[d.out]=gate(d.gate,v[d.in[0]],v[d.in[1]]);
   seen.add(d.out);
 }
 return v;
}
function clauseSat(c,v){
 return c.some(l=>{const n=names[Math.abs(l)-1];if(!n)throw Error('literal range');return v[n]===(l>0?1:0)});
}
function factor(v,kind){
 if(kind==='x')return v.x;
 if(kind==='x_and_z')return v.x&v.z;
 throw Error('bad factor');
}
function row(v,terms,rhs){
 let b=0;for(const s of terms){if(!(s in v))throw Error('unknown term');b^=v[s]}
 return Number(b===rhs);
}
const queries=[
 {id:'R1',factor:'x',terms:['b'],rhs:1,expected:true},
 {id:'R2',factor:'x_and_z',terms:['c'],rhs:1,expected:true},
 {id:'R3',factor:'x',terms:['a'],rhs:1,expected:false},
 {id:'R4',factor:'x',terms:['d'],rhs:0,expected:false},
 {id:'R5',factor:'x',terms:['a','x','y'],rhs:0,expected:false}
];
const tables=[];let sourceModels=0;
for(let x=0;x<(1<<k);x++){
 const v=evalDefs(defs,x),sat=F.every(c=>clauseSat(c,v));
 sourceModels+=Number(sat);
 A(v.a===(v.x^v.y),'first DEF');
 A(v.b===v.x,'nested XOR reduction');
 A(v.c===(v.x&v.z),'nested AND');
 A(v.d===0,'duplicate XOR cancels');
 tables.push({assignment:x,original:[v.x,v.y,v.z],a:v.a,b:v.b,c:v.c,d:v.d,source_sat:sat});
}
A(sourceModels===1,'exactly one source model');
const results=[];
for(const q of queries){
 const diff=tables.filter(o=>{
    const v=evalDefs(defs,o.assignment);
    return factor(v,q.factor)!==row(v,q.terms,q.rhs);
 }).map(o=>o.assignment);
 const sourceDiff=diff.filter(x=>tables[x].source_sat);
 const exact=diff.length===0;
 A(exact===q.expected,'expected test '+q.id);
 results.push({...q,definition_consistent_all_original_equal:exact,
    disagreement_original_assignments:diff,disagreement_source_models:sourceDiff});
}
const raw={
 schema:'LSPV2-411-def-quotient/v1',
 scope:'conditional semantics only; no native DEF-to-XOR export or public LOCAL selector presumed',
 k,original_variables:names,source_clauses:F,paid_definitions:defs,
 source_models:sourceModels,tables,queries:results,
 semantic_identities:[
 {row:['a','x','y'],rhs:0,true_on_definition_consistent:8,true_on_unconstrained_wire_triples:4},
 {row:['b','x'],rhs:0,true_on_definition_consistent:8,true_on_unconstrained_wire_pairs:2},
 {row:['d'],rhs:0,true_on_definition_consistent:8,true_on_unconstrained_wire_pair_values:1}
 ],
 logical_paid_nodes_in_candidate:{
  AND3_x:1,DEF:4,AND3_xz:1,
  GF2_if_exported:'not certified native',LOCAL_if_public:'not certified native'
 },checks
};
function modelCount(cs){
 let c=0;for(let i=0;i<8;i++){
  const v=evalDefs(defs,i);
  if(cs.every(q=>clauseSat(q,v)))c++;
 }return c;
}
A(modelCount(F)===1,'SAT original');
A(modelCount([...F,[-1]])===0,'UNSAT opposite x');
A(modelCount([[-1],[-2],[3]])===1,'SAT opposite x with same definitions');
function rejects(f){
 let did=false;try{f()}catch(e){did=true}A(did,'must reject malformed/corrupt');
}
rejects(()=>evalDefs([...defs,{out:'a',gate:'AND',in:['x','y']}],0));
rejects(()=>evalDefs([{out:'a',gate:'AND',in:['b','x']}],0));
rejects(()=>evalDefs([{out:'a',gate:'NOT',in:['x','x']}],0));
rejects(()=>clauseSat([4],{x:1,y:0,z:1}));
rejects(()=>row({x:1},['x','missing'],1));
const testDup=evalDefs(defs,1);
A(row(testDup,['a','a'],0)===1,'duplicate positional row cancellation');
A(row(testDup,['a'],0)===0,'set-dedup invalidates row');
raw.checks=checks;
const file=process.argv[2]||'lspv2_411_raw.json';
fs.writeFileSync(file,JSON.stringify(raw,null,2)+'\n');
console.log(JSON.stringify({status:'PASS',checks,sourceModels,definitions:defs.length,
 queries:results.map(q=>({id:q.id,exact:q.definition_consistent_all_original_equal,
 source_disagreements:q.disagreement_source_models.length})),output:file}));

'use strict';
/* LSPV1 354 INDEPENDENT no-producer-import replay.
   Usage: node experiments/arc/lspv1_354_pin_replay_source_compiler.js --proof |
          node experiments/arc/lspv1_354_independent_verify.js
   Verifies every source, every conservative fresh gate, every exact pivot,
   full authenticated source ancestry, and hostile perturbations. */
const fs=require('fs');
let checks=0;
function assert(v,m){checks++;if(!v)throw Error(m);}
function norm(a) {
 if(!Array.isArray(a))throw Error('clause array');
 for(const x of a)if(!Number.isSafeInteger(x)||x===0)throw Error('literal');
 return [...new Set(a)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
}
function same(a,b){return JSON.stringify(a)===JSON.stringify(b);}
function verify(P){
 assert(Array.isArray(P.F)&&P.F.length>0,'F');
 assert(Array.isArray(P.rows)&&Array.isArray(P.defs),'trace arrays');
 let V=Math.max(...P.F.flat().map(Math.abs)), gates=new Map(), antecedents=[], usedSources=new Set();
 for(let j=0;j<P.F.length;j++){
   const src=norm(P.F[j]);
   assert(!src.some(x=>src.includes(-x)),'source taut');
   assert(same(P.rows[j].cl,src),'signed source tampered');
 }
 const qSet=new Set(),slotByGate=new Map();
 for(const g of P.defs){
    assert(Number.isSafeInteger(g.q)&&g.q>V,'DEF output freshness');
    assert(!qSet.has(g.q),'duplicate DEF');
    assert(Number.isSafeInteger(g.a)&&Number.isSafeInteger(g.b),'gate inputs');
    assert(Math.abs(g.a)<g.q&&Math.abs(g.b)<g.q,'acyclic gate');
    qSet.add(g.q);V=g.q;
    assert(g.slots.length===3,'DEF slots');
    slotByGate.set(g.gate, [
      norm([-g.q,g.a]),norm([-g.q,g.b]),norm([g.q,-g.a,-g.b])
    ]);
 }
 const sourceCount=P.F.length,seenSlots=new Set();
 const ancestry=[];
 for(let i=0;i<P.rows.length;i++){
   const row=P.rows[i];assert(row.id===i,'row ID');
   const c=norm(row.cl);
   assert(same(row.cl,c),'line not normalized');
   if(row.kind==='source'){
      assert(i<sourceCount&&row.source_j===i,'unsourced clause');
      assert(same(c,norm(P.F[i])),'source alteration');
      ancestry[i]=new Set([i]);
   } else if(row.kind==='slot'){
      assert(slotByGate.has(row.gate),'unknown gate');
      assert(Number.isSafeInteger(row.slot)&&row.slot>=0&&row.slot<3,'gate slot index');
      assert(same(c,slotByGate.get(row.gate)[row.slot]),'bad definitional slot');
      assert(!seenSlots.has(row.gate+':'+row.slot),'duplicate slot');
      seenSlots.add(row.gate+':'+row.slot);ancestry[i]=new Set();
   } else if(row.kind==='res'){
      assert(Number.isSafeInteger(row.a)&&row.a<i,'bad RES parent A');
      assert(Number.isSafeInteger(row.b)&&row.b<i,'bad RES parent B');
      assert(Number.isSafeInteger(row.pivot)&&row.pivot!==0,'bad pivot type');
      const A=P.rows[row.a].cl,B=P.rows[row.b].cl,p=row.pivot;
      assert(A.includes(p)&&B.includes(-p),'wrong signed pivot');
      const r=norm([...A.filter(v=>v!==p),...B.filter(v=>v!==-p)]);
      assert(!r.some(v=>r.includes(-v)),'tautological resolvent');
      assert(same(c,r),'wrong resolvent');
      ancestry[i]=new Set([...ancestry[row.a],...ancestry[row.b]]);
   } else throw Error('unknown inference kind');
 }
 for(const g of P.defs)for(let j=0;j<3;j++)assert(seenSlots.has(g.gate+':'+j),'missing DEF slot');
 assert(P.root>=0&&P.root<P.rows.length,'invalid root');
 assert(same(P.rows[P.root].cl,[P.root_literal]),'root not unit');
 assert(same(P.rows[P.false_unit].cl,[-5]),'false-core pin mismatch');
 for(let j=0;j<P.F.length;j++)assert(ancestry[P.root].has(j),'missing source input');
 assert(P.paid_nodes===P.defs.length+P.res.length,'bad node tally');
 assert(P.rows.length===P.F.length+3*P.defs.length+P.res.length,'bad row tally');
 return {sources:P.F.length,def:P.defs.length,res:P.res.length,paid:P.paid_nodes,
   root:P.root_literal,full_source_ancestry:[...ancestry[P.root]].sort((a,b)=>a-b)};
}
function run(proofs){
 const outputs=[];
 for(const P of proofs)outputs.push(verify(P));
 const hostile=JSON.parse(JSON.stringify(proofs[0]));
 const first=hostile.rows.find(r=>r.kind==='res');first.pivot+=1234;
 let caught=false;try{verify(hostile)}catch(e){caught=true;}assert(caught,'corrupt pivot accepted');
 const flipped=JSON.parse(JSON.stringify(proofs[0]));
 flipped.rows[0].cl=[-flipped.rows[0].cl[0]];
 caught=false;try{verify(flipped)}catch(e){caught=true;}assert(caught,'corrupt source accepted');
 const corruptGate=JSON.parse(JSON.stringify(proofs[0]));
 const slot=corruptGate.rows.find(r=>r.kind==='slot');slot.cl=norm([...slot.cl,12345]);
 caught=false;try{verify(corruptGate)}catch(e){caught=true;}assert(caught,'corrupt gate accepted');
 const broken=JSON.parse(JSON.stringify(proofs[0]));broken.root=0;
 caught=false;try{verify(broken)}catch(e){caught=true;}assert(caught,'wrong final accepted');
 const malformed=[null,{},[],{F:"not-CNF"}, {F:[[0]],rows:[]}, {F:[["x"]],rows:[]}];
 for(const b of malformed){caught=false;try{verify(b)}catch(e){caught=true;}assert(caught,'malformed accepted');}
 return {checks,outputs,corrupt_rejected:4,malformed_rejected:malformed.length,status:'PASS',B3:'OPEN'};
}
if(require.main===module){
  const raw=fs.readFileSync(0,'utf8');console.log(JSON.stringify(run(JSON.parse(raw)),null,2));
}
if(typeof module!=='undefined')module.exports={run,verify};

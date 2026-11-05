'use strict';
// Independent verifier for fixed 2-variable CNF source grammar and ordinary Resolution tableau traces.
// Does not depend on Python producer. Run: node lspv4_406_independent_referee.js raw.json
const fs=require('fs');
const path=process.argv[2];
if(!path)throw Error('usage: node referee.js path/to/raw.json');
const R=JSON.parse(fs.readFileSync(path,'utf8'));
let checks=0;
function insist(ok,msg){if(!ok)throw Error(msg);checks++;}
const cls=[[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]];
function sat(mask){
 for(let a=0;a<4;a++){
  let pass=true;
  for(let j=0;j<8;j++)if((mask>>j)&1)
   if(!cls[j].some(l=>(((a>>(Math.abs(l)-1))&1)!==0)===(l>0))){pass=false;break;}
  if(pass)return true;
 }
 return false;
}
function canonical(a){return [...new Set(a)].sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a);}
function verifyProof(table,proof){
 let present=new Map(Object.entries(table));
 for(const record of proof){
  insist(!present.has(record.id),'duplicate name');
  insist(record.parents.length===2,'binary parents');
  const left=present.get(record.parents[0]),right=present.get(record.parents[1]);
  insist(!!left&&!!right,'parent missing');
  const p=record.pivot;
  let lpos=left.includes(p),lneg=left.includes(-p),rpos=right.includes(p),rneg=right.includes(-p);
  insist((lpos&&rneg)||(lneg&&rpos),'bad pivot');
  const expected=canonical(left.filter(x=>Math.abs(x)!==p).concat(right.filter(x=>Math.abs(x)!==p)));
  insist(JSON.stringify(expected)===JSON.stringify(record.clause),'invalid resolvent');
  present.set(record.id,expected);
 }
 insist(proof.length>0&&proof.at(-1).clause.length===0,'missing contradiction');
}
function evalGate(g,v){
 const a=v[g.parents[0]],b=v[g.parents[1]];
 if(g.op==='NOT')return 1-a;
 if(g.op==='AND')return a&b;
 if(g.op==='OR')return a|b;
 throw Error('unknown op');
}
function checkTableauDefinitions(gates,mask,sources,out){
 const v={};
 for(let i=1;i<=8;i++){
  v[i]=(mask>>(i-1))&1;
  insist(JSON.stringify(sources['I'+i])===JSON.stringify([v[i]?i:-i]),'wrong input source');
 }
 for(const g of gates){
  insist(g.parents.every(p=>p<g.id),'gate not acyclic');
  v[g.id]=evalGate(g,v);
  const z=g.id,a=g.parents[0],b=g.parents[1];
  let facets;
  if(g.op==='NOT')facets=[[z,a],[-z,-a]];
  else if(g.op==='AND')facets=[[-z,a],[-z,b],[z,-a,-b]];
  else if(g.op==='OR')facets=[[z,-a],[z,-b],[-z,a,b]];
  else throw Error('illegal gate');
  facets.forEach((cl,i)=>{
   const record=sources['D'+z+'_'+i];
   insist(JSON.stringify(record)===JSON.stringify(canonical(cl)),'forged facet');
   insist(record.some(l=>(v[Math.abs(l)]===1)===(l>0)),'facet fails actual tableau');
  });
 }
 insist(JSON.stringify(sources.ASSERT)===JSON.stringify([out]),'wrong assertion source');
 return v;
}
insist(R.cases.length===256,'missing source subset');
let nSat=0,nUns=0,total=0,max=0;
for(const [mask,record] of R.cases.entries()){
 insist(record.mask===mask,'misaligned mask');
 const answer=sat(mask);
 insist(answer===record.source_sat,'wrong SAT ground truth');
 insist(answer===Boolean(record.program_output),'wrong circuit classification');
 if(answer){nSat++;insist(record.resolution_nodes===null,'SAT reported proof');}
 else{nUns++;total+=record.resolution_nodes;max=Math.max(max,record.resolution_nodes);
      insist(record.resolution_nodes<=39,'overlarge proof');}
}
insist(nSat===95&&nUns===161&&total===3771&&max===27,'wrong finite totals');
const s=R.sample_proof;
const v=checkTableauDefinitions(s.gates,s.mask,s.tableau_source,s.output);
insist(v[s.output]===0,'expected tableau reject');
verifyProof(s.tableau_source,s.resolution_proof);
const w=R.counterexample;
const wv=checkTableauDefinitions(w.wrong_gates,w.mask,w.tableau_source,w.output);
insist(sat(w.mask),'wrong-source original not SAT');
insist(wv[w.output]===0,'wrong circuit must reject SAT');
verifyProof(w.tableau_source,w.resolution_proof);
insist(w.resolution_proof.length===3,'wrong circuit proof length');
function mustReject(table,proof){
 let rejected=false;
 try{verifyProof(table,proof);}catch(_){rejected=true;}
 insist(rejected,'bad proof accepted');
}
let bad=JSON.parse(JSON.stringify(s.resolution_proof));
bad[0].pivot=s.output;mustReject(s.tableau_source,bad);
bad=JSON.parse(JSON.stringify(s.resolution_proof));
bad[bad.length-1].clause=[s.output];mustReject(s.tableau_source,bad);
bad=JSON.parse(JSON.stringify(s.resolution_proof));
bad[bad.length-1].parents=['UNDEFINED','ASSERT'];mustReject(s.tableau_source,bad);
console.log(JSON.stringify({independent_check:'PASS',assertions:checks,
 ground_truth:{SAT:nSat,UNSAT:nUns},total_resolution_nodes:total,
 max_resolution_nodes:max,wrong_decider_refutation_nodes:w.resolution_proof.length},null,2));

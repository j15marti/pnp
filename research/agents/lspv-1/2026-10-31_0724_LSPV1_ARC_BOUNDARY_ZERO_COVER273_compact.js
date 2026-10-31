// LSPV-1 ARC-BOUNDARY-ZERO-COVER273 compact standalone verifier, no packages.
// Execute: node 2026-10-31_0724_LSPV1_ARC_BOUNDARY_ZERO_COVER273_compact.js
// Full signed-occurrence, flip-trail, independent checker, and DPLL dataset:
// local reproducibility package ARC_BOUNDARY_ZERO_COVER273_REPRO.zip.
"use strict";
const assert=require("node:assert/strict");
const k=3, samples=[[4,4],[4,32],[85,170],[170,170],[255,1],[255,0],
 [127,128],[254,127],[24,24],[3,12],[102,153],[126,24]];
function forbidden(a){return [0,1,2].map(i=>((a>>(2-i))&1)?-(i+1):(i+1));}
function block(s,p){
 const [,u,v,r,t]=[p,p+1,p+2,p+3,p+4];
 const out=[];
 for(const R of [r,-r])for(const T of [t,-t])out.push([p,R,T]);
 for(let i=0;i<8;i++)out.push((s&(1<<i))?[p,u,v]:forbidden(i));
 return out;
}
function formula(s,t){return [...block(s,4),...block(t,9)];}
function tc(c,a){return c.filter(l=>Boolean(a&(1<<(Math.abs(l)-1)))===(l>0)).length;}
function sat(cs,a){return cs.every(c=>tc(c,a)>0);}
function compat(c,d,mode){
 const map=new Map();
 for(const [lits,letter] of [[c,mode[0]],[d,mode[1]]])for(const l of lits){
   const b=letter==="S"?(l>0):(l<0),key=Math.abs(l);
   if(map.has(key)&&map.get(key)!==b)return false;map.set(key,b);
 }
 return true;
}
function resolve(a,b,p){
 assert.ok((a.includes(p)&&b.includes(-p))||(a.includes(-p)&&b.includes(p)));
 const r=[...new Set([...a,...b])].filter(l=>Math.abs(l)!==p);
 for(const l of r)assert.ok(!r.includes(-l));return r.sort((u,v)=>Math.abs(u)-Math.abs(v));
}
function refute(cs){
 let leaves=[];
 for(let a=0;a<8;a++){
  const wanted=forbidden(a),index=cs.findIndex(c=>c.join(",")===wanted.join(","));
  assert.ok(index>=0);leaves.push({id:a+1,source:index+1,clause:wanted});
 }
 const nodes=leaves.slice(),first=[],second=[];
 for(let i=0;i<8;i+=2){
  const c=resolve(nodes[i].clause,nodes[i+1].clause,3);
  const z={id:nodes.length+1,parents:[nodes[i].id,nodes[i+1].id],pivot:3,clause:c};
  nodes.push(z);first.push(z);
 }
 for(let i=0;i<4;i+=2){
  const c=resolve(first[i].clause,first[i+1].clause,2);
  const z={id:nodes.length+1,parents:[first[i].id,first[i+1].id],pivot:2,clause:c};
  nodes.push(z);second.push(z);
 }
 nodes.push({id:15,parents:[13,14],pivot:1,clause:resolve(second[0].clause,second[1].clause,1)});
 assert.equal(nodes.length,15);assert.equal(nodes[14].clause.length,0);return nodes;
}
function transcript(s,t){
 const out=[];
 for(let a=0;a<8;a++){
  const l=+Boolean(s&(1<<a));out.push(["L",a,l]);
  if(l){const r=+Boolean(t&(1<<a));out.push(["R",a,r]);if(r)break;}
 }
 return out;
}
function cert(T){
 const m=new Map(T.map(([p,a,v])=>[p+":"+a,v]));
 const yes=Array.from({length:8},(_,a)=>a).some(a=>m.get("L:"+a)===1&&m.get("R:"+a)===1);
 const no=Array.from({length:8},(_,a)=>a).every(a=>m.get("L:"+a)===0||m.get("R:"+a)===0);
 assert.ok(!(yes&&no));return [yes,no];
}
let satpairs=0,nopairs=0,yesReads=0,noReads=0,minNo=100,maxNo=0;
for(let s=0;s<256;s++)for(let t=0;t<256;t++){
 const truth=Boolean(s&t),q=transcript(s,t),[yes,no]=cert(q);
 assert.equal(yes,truth);assert.equal(no,!truth);
 for(let j=0;j<q.length;j++)assert.deepEqual(cert(q.slice(0,j)),[false,false]);
 if(truth){satpairs++;yesReads+=q.length;}else{
  nopairs++;noReads+=q.length;assert.ok(q.length>=8);
  minNo=Math.min(minNo,q.length);maxNo=Math.max(maxNo,q.length);
 }
}
assert.deepEqual([satpairs,nopairs,yesReads,noReads,minNo,maxNo],
 [58975,6561,283866,69984,8,16]);
let modes=0,modelTrials=0,satSources=0,unsatSources=0,forbiddenEdges=0,proofs=0;
for(const [s,t] of samples){
 const cs=formula(s,t);let models=0;
 for(let a=0;a<8192;a++){modelTrials++;if(sat(cs,a))models++;}
 assert.equal(models,256*(s&t).toString(2).replace(/0/g,"").length);
 if(s&t)satSources++;else{unsatSources++;refute(cs);proofs++;}
 for(let i=0;i<cs.length;i++)for(let j=i+1;j<cs.length;j++){
  let n=0;
  for(const mode of ["SS","SU","US","UU"]){
   let brute=false,vars=[...new Set([...cs[i],...cs[j]].map(Math.abs))];
   for(let a=0;a<(1<<vars.length);a++){
    let full=0;for(let r=0;r<vars.length;r++)if(a&(1<<r))full|=1<<(vars[r]-1);
    if(tc(cs[i],full)===(mode[0]==="S"?3:0)&&tc(cs[j],full)===(mode[1]==="S"?3:0)){brute=true;break;}
   }
   assert.equal(compat(cs[i],cs[j],mode),brute);if(brute)n++;modes++;
  }
  if(!n)forbiddenEdges++;
 }
 for(let a=0;a<8;a++){
  let full=(1<<3)|(1<<8);
  for(let j=0;j<3;j++)if(a&(1<<(2-j)))full|=1<<j;
  for(const c of cs)assert.equal(tc(c,full)+tc(c,full^8191),3);
 }
}
assert.deepEqual([satSources,unsatSources,modes,modelTrials,forbiddenEdges,proofs],
 [6,6,13248,98304,548,6]);
console.log(JSON.stringify({status:"PASSED",pair_labels:{SAT:satpairs,UNSAT:nopairs},
 queries:{SAT:yesReads,UNSAT:noReads,min_NO:minNo,max_NO:maxNo},
 original_sources:{SAT:satSources,UNSAT:unsatSources},pair_modes:modes,
 complete_assignment_trials:modelTrials,incompatible_extreme_edges:forbiddenEdges,
 original_resolution_refutations:proofs},null,2));
#!/usr/bin/env node
"use strict";

const fs=require("fs"), crypto=require("crypto");
const started=process.hrtime.bigint();
const path="results/raw/arc/lspv5_314/source_aware_exit_compiler_referee314.json";
const payload=fs.readFileSync(path,"utf8"), data=JSON.parse(payload), FULL=255;

function canon(xs){
  if(!Array.isArray(xs)) throw new Error("clause");
  const out=[...new Set(xs)].sort((a,b)=>Math.abs(a)-Math.abs(b)||(a<0)-(b<0));
  if(out.some(x=>!Number.isInteger(x)||typeof x==="boolean"||x===0||out.includes(-x))) throw new Error("canonical");
  return out;
}
function eq(a,b){return JSON.stringify(a)===JSON.stringify(b);}
function key(c){return JSON.stringify(canon(c));}
function clauseSetEq(a,b){return a.length===b.length&&new Set(a.map(key)).size===a.length&&a.every(c=>b.some(d=>eq(canon(c),canon(d))));}
function truth(c,a){return c.some(l=>Boolean((a>>(Math.abs(l)-1))&1)===(l>0));}
function mask(c){let m=0;for(let a=0;a<8;a++)if(truth(c,a))m|=1<<a;return m;}
function models(cs){return [...Array(8).keys()].filter(a=>cs.every(c=>truth(c,a)));}
function resolve(l,r,p){l=canon(l);r=canon(r);if(!l.includes(p)||!r.includes(-p))throw new Error("pivot");return canon([...l.filter(x=>x!==p),...r.filter(x=>x!==-p)]);}
function slots(q,l,r){return [canon([-q,l]),canon([-q,r]),canon([q,-l,-r])];}

const clauses=[];
for(const x of [0,1,-1])for(const y of [0,1,-1])for(const z of [0,1,-1]){
  if(!x&&!y&&!z)continue;clauses.push(canon([x&&x,y&&2*y,z&&3*z].filter(Boolean)));
}
clauses.sort((a,b)=>a.length-b.length||key(a).localeCompare(key(b)));
if(clauses.length!==26||new Set(clauses.map(key)).size!==26)throw new Error("catalog");
const clauseMasks=clauses.map(mask);

function sourceFor(a){
  const out=[];
  for(const [x,y] of [[1,2],[1,3],[2,3]])for(const sx of [-1,1])for(const sy of [-1,1]){
    const c=canon([sx*x,sy*y]);if(truth(c,a))out.push(c);
  }
  out.sort((a,b)=>a.length-b.length||key(a).localeCompare(key(b)));
  if(out.length!==9||!eq(models(out),[a]))throw new Error("source");return out;
}
function charge(c,a,source){
  c=canon(c);if(!truth(c,a))throw new Error("not entailed singleton");
  if(c.length===2){if(!source.some(s=>eq(s,c)))throw new Error("missing source");return 0;}
  if(c.length===1)return 1;
  if(c.length===3&&source.some(s=>s.every(l=>c.includes(l))))return 3;
  throw new Error("charge");
}
function optimum(target,a,source){
  let dp=new Map([[FULL,0]]);
  for(let i=0;i<clauses.length;i++){
    const c=clauses[i],cm=clauseMasks[i];
    if(!truth(c,a)||(target&(~cm&FULL))!==0)continue;
    const w=charge(c,a,source),next=new Map(dp);
    for(const [cur,co] of dp){const nm=cur&cm,nc=co+w;if(!next.has(nm)||nc<next.get(nm))next.set(nm,nc);}
    dp=next;
  }
  if(!dp.has(target))throw new Error("no basis");return dp.get(target);
}

let pairs=0,maxCost=-1,maxima=[],hist=new Map(),replayed=0;
for(const rec of data.records){
  const a=rec.assignment,source=sourceFor(a);
  if(!clauseSetEq(rec.source,source)||!eq(rec.source_models,[a]))throw new Error("record source");
  const parity=[...Array(8).keys()].filter(x=>x.toString(2).split("1").length%2===0); // unused guard below
  let seen=0;
  for(let target=0;target<256;target++){
    if(!(target&(1<<a)))continue;
    const cost=optimum(target,a,source);pairs++;seen++;
    hist.set(cost,(hist.get(cost)||0)+1);
    if(cost>maxCost){maxCost=cost;maxima=[[a,target]];}else if(cost===maxCost)maxima.push([a,target]);
    const rr=rec.relation_costs.find(x=>x[0]===target);
    if(!rr||rr[1]!==cost)throw new Error("relation record");
  }
  if(seen!==128)throw new Error("pair count");

  const known=new Set(source.map(key)),fresh=new Set();let paid=0,represented=FULL;
  for(const cert of rec.parity_certificates){
    if(!known.has(key(cert.base))||cert.base.length!==2||cert.target.length!==3)throw new Error("base");
    const d=cert.definition;
    if(d.out<=3||fresh.has(d.out)||Math.abs(d.left)===Math.abs(d.right))throw new Error("fresh");
    fresh.add(d.out);const expected=slots(d.out,d.left,d.right);
    if(!eq(d.slots.map(canon),expected))throw new Error("definition");
    expected.forEach(c=>known.add(key(c)));paid++;
    for(const step of cert.resolutions){
      if(!known.has(key(step.left))||!known.has(key(step.right)))throw new Error("parent");
      const out=resolve(step.left,step.right,step.pivot);
      if(!eq(out,canon(step.out)))throw new Error("resolvent");known.add(key(out));paid++;
    }
    if(!known.has(key(cert.target))||cert.cost!==3)throw new Error("target");
    represented&=mask(cert.target);
  }
  if(paid!==12||rec.parity_paid_cost!==12||represented!==rec.matching_parity_mask)throw new Error("parity proof");
  replayed+=paid;

  const drop=rec.strict_support_drop;
  if(drop.paid_cost!==0||!eq(drop.input_support,[1,2,3])||!eq(drop.output_support,[1,2])||
     !drop.basis.every(c=>known.has(key(c)))||!eq(models(drop.basis),drop.models))throw new Error("drop");

  const unit=rec.unit_demand;
  if(unit.cost!==1||!source.some(c=>eq(c,unit.sources[0]))||!source.some(c=>eq(c,unit.sources[1]))||
     !eq(resolve(unit.sources[0],unit.sources[1],unit.pivot),unit.out))throw new Error("unit");
  replayed++;

  const matchModels=models([...source,...rec.parity_basis]);
  const oppositeBasis=[];
  for(let x=0;x<8;x++)if((x.toString(2).split("1").length-1)%2===rec.matching_parity)oppositeBasis.push(canon([x&1?-1:1,x&2?-2:2,x&4?-3:3]));
  if(!eq(matchModels,[a])||!eq(models([...source,...oppositeBasis]),[]))throw new Error("labels");
}
const expectedMaxima=[...Array(8).keys()].map(a=>[a,((a.toString(2).split("1").length-1)%2===0)?105:150]);
if(pairs!==1024||maxCost!==12||!eq(maxima,expectedMaxima)||
   !eq(Object.fromEntries([...hist.entries()].sort((a,b)=>a[0]-b[0])),{"0":584,"3":296,"6":96,"9":40,"12":8}))throw new Error("global summary");

function parseRecord(obj){
  const keys=["assignment","basis","output_mask","source"];
  if(!obj||typeof obj!=="object"||Array.isArray(obj)||!eq(Object.keys(obj).sort(),keys))throw new Error("schema");
  if(!Number.isInteger(obj.assignment)||typeof obj.assignment==="boolean"||obj.assignment<0||obj.assignment>7)throw new Error("assignment");
  if(!Number.isInteger(obj.output_mask)||typeof obj.output_mask==="boolean"||obj.output_mask<0||obj.output_mask>255)throw new Error("mask");
  for(const k of ["source","basis"]){if(!Array.isArray(obj[k]))throw new Error("clauses");const seen=new Set();for(const raw of obj[k]){if(!Array.isArray(raw)||!raw.length||raw.some(x=>!Number.isInteger(x)||typeof x==="boolean"||Math.abs(x)<1||Math.abs(x)>3))throw new Error("literal");const c=canon(raw);if(!eq(c,raw)||seen.has(key(c)))throw new Error("canonical/duplicate");seen.add(key(c));}}
}
const valid={assignment:0,source:data.records[0].source,output_mask:105,basis:data.records[0].parity_basis};parseRecord(valid);
const malformed=[null,{}, {...valid,extra:1},{...valid,assignment:-1},{...valid,assignment:8},{...valid,assignment:true},{...valid,output_mask:256},{...valid,source:null},{...valid,source:[[]]},{...valid,source:[[0]]},{...valid,basis:[[1,-1]]},{...valid,basis:[[1],[1]]}];
let malformedRejected=0;for(const m of malformed){try{parseRecord(m);}catch(_){malformedRejected++;}}
if(malformedRejected!==12||data.malformed.rejected!==12)throw new Error("malformed");

let corruptRejected=0;
function reject(mutator,kind){const copy=JSON.parse(JSON.stringify(data));mutator(copy);try{const rec=copy.records[0];if(kind==="cert"){const source=sourceFor(0),known=new Set(source.map(key));const c=rec.parity_certificates[0],d=c.definition,ex=slots(d.out,d.left,d.right);if(!eq(d.slots.map(canon),ex))throw new Error("def");ex.forEach(x=>known.add(key(x)));for(const st of c.resolutions){if(!known.has(key(st.left))||!known.has(key(st.right)))throw new Error("parent");const o=resolve(st.left,st.right,st.pivot);if(!eq(o,canon(st.out)))throw new Error("out");known.add(key(o));}}else if(kind==="drop"){if(!rec.strict_support_drop.basis.every(c=>sourceFor(0).some(s=>eq(s,c))))throw new Error("drop");}else if(kind==="unit"){const u=rec.unit_demand;if(!eq(resolve(u.sources[0],u.sources[1],u.pivot),u.out))throw new Error("unit");}}catch(_){corruptRejected++;return;}throw new Error("corruption accepted");}
reject(x=>{x.records[0].parity_certificates[0].definition.slots[0][0]*=-1;},"cert");
reject(x=>{x.records[0].parity_certificates[0].resolutions[0].pivot*=-1;},"cert");
reject(x=>{x.records[0].parity_certificates[0].resolutions[1].out=[1,2,3];},"cert");
reject(x=>{x.records[0].strict_support_drop.basis[0]=[1,2];},"drop");
reject(x=>{x.records[0].unit_demand.pivot*=-1;},"unit");

console.log(JSON.stringify({status:"PASS",raw_sha256:crypto.createHash("sha256").update(payload).digest("hex"),independent_pairs:pairs,max_recipe_cost:maxCost,maximizers:maxima,cost_histogram:Object.fromEntries([...hist.entries()].sort((a,b)=>a[0]-b[0])),replayed_paid_nodes:replayed,strict_drop_controls:8,malformed_rejected:malformedRejected,corrupt_rejected:corruptRejected,verifier_wall_seconds:Number(process.hrtime.bigint()-started)/1e9,verifier_peak_rss_kib:process.resourceUsage().maxRSS}));

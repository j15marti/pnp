#!/usr/bin/env node
"use strict";

const fs = require("fs");
const crypto = require("crypto");
const rawPath = "results/raw/arc/lspv5_318/reflection_equivalence_referee318.json";
const start = process.hrtime.bigint();
const raw = JSON.parse(fs.readFileSync(rawPath, "utf8"));
let assertions = 0;
const check = (value, message) => { assertions++; if (!value) throw new Error(message); };

const fullClause = mask => [1,2,3].map((v,i) => mask & (1<<i) ? -v : v);
const satClause = (clause, mask) => clause.some(lit => Boolean(mask & (1 << (Math.abs(lit)-1))) === (lit > 0));
const modelCount = clauses => {
  let count = 0;
  for (let mask=0; mask<8; mask++) if (clauses.every(c => satClause(c,mask))) count++;
  return count;
};
const complete = Array.from({length:8}, (_,mask)=>fullClause(mask));
const catalog = [complete, ...Array.from({length:8}, (_,removed)=>complete.filter((_,i)=>i!==removed))];
catalog.forEach((clauses,i)=>check(modelCount(clauses)===(i===0?0:1),`catalog models ${i}`));
check(raw.catalog.map(x=>x.models).join(",")==="0,1,1,1,1,1,1,1,1","raw catalog counts");

function reflection(labels) {
  const selectors = Array.from({length:9}, (_,i)=>4+i);
  const clauses = [selectors.slice()];
  for (let i=0;i<selectors.length;i++) for(let j=i+1;j<selectors.length;j++) clauses.push([-selectors[i],-selectors[j]]);
  labels.forEach((label,i)=> {
    if (label === "SAT") clauses.push([-selectors[i]]);
    else catalog[i].forEach(c=>clauses.push([-selectors[i],...c]));
  });
  return {vars:12, selectors, clauses};
}
function cnfModels(cnf) {
  const found=[];
  for(let mask=0;mask<2**cnf.vars;mask++) if(cnf.clauses.every(c=>satClause(c,mask))) found.push(mask);
  return found;
}
const goodLabels=["UNSAT",...Array(8).fill("SAT")];
const badLabels=goodLabels.slice(); badLabels[1]="UNSAT";
const good=reflection(goodLabels), bad=reflection(badLabels);
const gm=cnfModels(good), bm=cnfModels(bad);
check(gm.length===0 && raw.reflection_controls.good_decider_models===0,"good reflection UNSAT");
check(bm.length===1 && raw.reflection_controls.bad_decider_models===1,"false reject makes reflection SAT");
check(Boolean(bm[0] & (1 << (bad.selectors[1]-1))),"bad model selects S0");
check((bm[0] & 7)===0,"bad model is S0 witness");
check(good.clauses.length===53 && bad.clauses.length===59,"reflection clause counts");

function canonical(c) { return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b) || Number(a<0)-Number(b<0)); }
function resolve(left,right,pivot) {
  if (!(left.includes(pivot)&&right.includes(-pivot))) [left,right]=[right,left];
  check(left.includes(pivot)&&right.includes(-pivot),`pivot ${pivot}`);
  const out=canonical([...left.filter(x=>x!==pivot),...right.filter(x=>x!==-pivot)]);
  check(!out.some(x=>out.includes(-x)),"non-tautological resolvent");
  return out;
}
let current=complete.map(c=>[-4,...c]);
let proofNodes=0;
for(const pivot of [3,2,1]) {
  const next=[], used=new Set();
  for(let i=0;i<current.length;i++) {
    if(used.has(i)) continue;
    const j=current.findIndex((right,k)=>!used.has(k)&&k!==i&&((current[i].includes(pivot)&&right.includes(-pivot))||(current[i].includes(-pivot)&&right.includes(pivot))));
    check(j>=0,`mate pivot ${pivot}`);
    used.add(i); used.add(j); next.push(resolve(current[i],current[j],pivot)); proofNodes++;
  }
  current=next;
}
check(proofNodes===7 && JSON.stringify(current)===JSON.stringify([[-4]]),"seven-node gated proof");
check(raw.reflection_controls.explicit_good_resolution_upper_bound===16,"full H upper bound");
check(raw.reflection_controls.restricted_U8_resolution_nodes===7,"restriction cost");

function xorCount(charges) {
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  let count=0;
  for(let mask=0;mask<64;mask++) {
    const parity=[0,0,0,0];
    edges.forEach(([u,v],i)=>{const bit=(mask>>i)&1; parity[u]^=bit; parity[v]^=bit;});
    if(parity.every((x,i)=>x===charges[i])) count++;
  }
  return count;
}
check(xorCount([1,0,0,0])===0 && raw.xor_countercontrol.odd_k4_models===0,"odd K4 UNSAT");
check(xorCount([0,0,0,0])===8 && raw.xor_countercontrol.even_k4_models===8,"even K4 SAT");
check(raw.schema_rejections.length===11,"schema malformed count");
check(raw.label_rejections.length===4,"label malformed count");
check(raw.classification.abstract_reflection_equivalence==="PROVED","theorem class");
check(raw.classification.Rmix341_restriction_closure==="OPEN","Rmix closure open");
check([raw.classification.B1_Rmix341,raw.classification.B2_Rmix341,raw.classification.B3_Rmix341].every(x=>x==="OPEN"),"B1 B2 B3 open");

const elapsed=Number(process.hrtime.bigint()-start)/1e9;
const sha=crypto.createHash("sha256").update(fs.readFileSync(rawPath)).digest("hex");
console.log(JSON.stringify({verified:true,assertions,raw_sha256:sha,node_wall_seconds:elapsed,node_peak_rss_kib:process.resourceUsage().maxRSS},null,2));

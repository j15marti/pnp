#!/usr/bin/env node
"use strict";

const fs=require("fs"), crypto=require("crypto");
const rawPath="results/raw/arc/lspv5_319/decider_extensional_collapse_referee319.json";
const started=process.hrtime.bigint();
const raw=JSON.parse(fs.readFileSync(rawPath,"utf8"));
let assertions=0;
const check=(x,m)=>{assertions++; if(!x)throw Error(m);};

const fullClause=mask=>[1,2,3].map((v,i)=>mask&(1<<i)?-v:v);
const clauseSat=(c,mask)=>c.some(lit=>Boolean(mask&(1<<(Math.abs(lit)-1)))===(lit>0));
const label=formula=>{
  for(let mask=0;mask<2**formula.vars;mask++) if(formula.clauses.every(c=>clauseSat(c,mask))) return "SAT";
  return "UNSAT";
};
const enc=f=>JSON.stringify({clauses:f.clauses,vars:f.vars});
const complete=Array.from({length:8},(_,i)=>fullClause(i));
const catalog=[];
for(let subset=1;subset<256;subset++) catalog.push({vars:3,clauses:complete.filter((_,i)=>subset&(1<<i))});
const table=new Map(catalog.map(f=>[enc(f),label(f)]));

const accepted={brute:new Set(),table:new Set(),delayed:new Set()};
let sat=0,unsat=0;
for(const f of catalog){
  const truth=label(f); sat+=truth==="SAT"; unsat+=truth==="UNSAT";
  const outcomes={brute:truth,table:table.get(enc(f)),delayed:label(f)};
  for(const [name,out] of Object.entries(outcomes)){
    check(out===truth,`${name} label`);
    if(out==="UNSAT")accepted[name].add(enc(f));
  }
}
check(sat===254&&unsat===1,"catalog labels");
check([...accepted.brute].join() === [...accepted.table].join(),"brute/table relation");
check([...accepted.brute].join() === [...accepted.delayed].join(),"brute/delayed relation");
check(accepted.brute.size===1,"one accepted pair");
check(raw.catalog.formulas===255&&raw.catalog.sat===254&&raw.catalog.unsat===1,"raw catalog");
check(raw.catalog.accepted_pairs_per_correct_decider===1,"raw relation size");

const s0={vars:3,clauses:complete.slice(1)};
check(label(s0)==="SAT","S0 SAT");
check(raw.faulty_advice_control.bad_system_accepts_copy===true,"bad advice accepted");
check(raw.malformed_rejections.length===15,"malformed count");

function xorCount(charges){
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]; let count=0;
  for(let mask=0;mask<64;mask++){
    const p=[0,0,0,0]; edges.forEach(([u,v],i)=>{const b=(mask>>i)&1;p[u]^=b;p[v]^=b;});
    if(p.every((x,i)=>x===charges[i]))count++;
  }
  return count;
}
check(xorCount([1,0,0,0])===0&&raw.xor_countercontrol.odd_k4_models===0,"odd K4");
check(xorCount([0,0,0,0])===8&&raw.xor_countercontrol.even_k4_models===8,"even K4");
check(raw.classification.correct_decider_extensional_collapse==="PROVED","theorem class");
check(raw.classification.code_specific_B3_obstruction==="FALSIFIED","code obstacle class");
check(raw.classification.runtime_independence_B1_B2==="FALSIFIED","runtime boundary");
check([raw.classification.B1_Rmix341,raw.classification.B2_Rmix341,raw.classification.B3_Rmix341].every(x=>x==="OPEN"),"B statuses");
check(raw.correct_decider_work.delayed>raw.correct_decider_work.brute,"delay work differs");
check(raw.correct_decider_work.table_lookup_phase<raw.correct_decider_work.brute,"lookup phase differs");
check(raw.correct_decider_work.table_all_phase===raw.correct_decider_work.table_lookup_phase+raw.correct_decider_work.table_preprocessing,"all-phase table charge");

const elapsed=Number(process.hrtime.bigint()-started)/1e9;
const sha=crypto.createHash("sha256").update(fs.readFileSync(rawPath)).digest("hex");
console.log(JSON.stringify({verified:true,assertions,formulas_rebuilt:catalog.length,raw_sha256:sha,node_wall_seconds:elapsed,node_peak_rss_kib:process.resourceUsage().maxRSS},null,2));

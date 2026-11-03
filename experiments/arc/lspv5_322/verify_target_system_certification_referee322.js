#!/usr/bin/env node
"use strict";
const fs=require("fs"), path=require("path");
const root=path.resolve(__dirname,"../../..");
const p=path.join(root,"results/raw/arc/lspv5_322/target_system_certification_referee322.json");
const r=JSON.parse(fs.readFileSync(p,"utf8"));
let checks=0; function ok(x,m){checks++;if(!x)throw new Error(m)}
function countModels(cs,n){let z=0;for(let a=0;a<(1<<n);a++){
  if(cs.every(c=>c.some(l=>l>0?((a>>(l-1))&1)===1:((a>>(-l-1))&1)===0)))z++;
}return z}
ok(r.artifact==="TARGET-SYSTEM-CERTIFICATION-FIREWALL-REFEREE322","artifact");
const k=r.controls.k4_tseitin, ph=r.controls.php_3_2;
ok(countModels(k.clauses,6)===0,"odd K4"); ok(k.even_models===8,"even K4");
for(let i=0;i<k.clauses.length;i++)ok(countModels(k.clauses.slice(0,i).concat(k.clauses.slice(i+1)),6)===k.odd_deletion_model_counts[i],"K4 deletion");
ok(countModels(ph.clauses,6)===0,"PHP");
for(let i=0;i<ph.clauses.length;i++)ok(countModels(ph.clauses.slice(0,i).concat(ph.clauses.slice(i+1)),6)===ph.deletion_model_counts[i],"PHP deletion");
const s=r.controls.transfer_schema;
ok(s.valid.direction==="W_Q<=p(N+W_R)"&&s.valid.overhead==="polynomial","valid arrow");
ok(s.invalid.length===6,"invalid count");
for(const [ds,hs] of Object.entries(r.controls.linear_vs_exponential_thresholds)){
  const d=Number(ds),h=Number(hs); ok(2**h>(5*h)**d,"threshold"); if(h>1)ok(2**(h-1)<=(5*(h-1))**d,"minimal threshold");
}
ok(r.classifications.B1==="OPEN"&&r.classifications.B2==="OPEN"&&r.classifications.B3==="OPEN","bridges open");
ok(r.classifications.P_vs_NP==="OPEN","P vs NP");
console.log(JSON.stringify({status:"PASS",checks,raw:p}));

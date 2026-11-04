#!/usr/bin/env node
"use strict";
const fs=require("fs"), path=require("path");
const root=path.resolve(__dirname,"../../..");
const rawPath=path.join(root,"results/raw/arc/lspv5_324/common_envelope_firewall_referee324.json");
const raw=JSON.parse(fs.readFileSync(rawPath,"utf8"));
let checks=0;
function ok(condition,message){checks++;if(!condition)throw new Error(message)}
function assignments(n){const out=[];for(let a=0;a<(1<<n);a++)out.push(Array.from({length:n},(_,i)=>(a>>i)&1));return out}
function countModels(clauses,n){return assignments(n).filter(bits=>clauses.every(clause=>clause.some(lit=>bits[Math.abs(lit)-1]===(lit>0?1:0)))).length}
function php(pigeons,holes){const variable=(p,h)=>p*holes+h+1,clauses=[];
  for(let p=0;p<pigeons;p++)clauses.push(Array.from({length:holes},(_,h)=>variable(p,h)));
  for(let h=0;h<holes;h++)for(let p=0;p<pigeons;p++)for(let q=p+1;q<pigeons;q++)clauses.push([-variable(p,h),-variable(q,h)]);
  return {clauses,variables:pigeons*holes}}
function parity(bits){return bits.reduce((a,b)=>a^b,0)}
function recode(bits){return [parity(bits),...bits.slice(1)]}
function decode(bits){return [parity(bits),...bits.slice(1)]}

ok(raw.artifact==="COMMON-ENVELOPE-QUANTIFIER-FIREWALL-REFEREE324","artifact");
for(let h=1;h<=3;h++){const u=php(h+1,h),s=php(h,h);
  ok(countModels(u.clauses,u.variables)===0,`PHP ${h+1}/${h}`);
  let factorial=1;for(let i=2;i<=h;i++)factorial*=i;
  ok(countModels(s.clauses,s.variables)===factorial,`PHP ${h}/${h}`)}
for(const [name,fixture] of Object.entries(raw.controls.fixtures))ok(countModels(fixture.clauses,fixture.variables)===fixture.models,`${name} models`);
for(const item of raw.controls.encoder_controls){const source=raw.controls.fixtures[item.fixture];
  ok(item.source_prefix_exact,`${item.fixture} prefix`);ok((item.encoded_models>0)===(source.models>0),`${item.fixture} equivalence`);
  if(item.exceptional){ok(item.target_resolution_upper===1,`${item.fixture} one-step`);ok(item.recognized_h<=item.cutoff,`${item.fixture} cutoff`)}}
ok(raw.controls.corrupt_records.length===7&&raw.controls.corrupt_records.every(x=>x.rejected),"corrupt records");
let parityRows=0;
for(let h=1;h<=12;h++)for(let a=0;a<(1<<h);a++){const bits=Array.from({length:h},(_,i)=>(a>>i)&1),y=recode(bits);
  ok(JSON.stringify(decode(y))===JSON.stringify(bits),`inverse ${h}/${a}`);ok(y[0]===parity(bits),`syndrome ${h}/${a}`);parityRows++}
ok(parityRows===8190,"parity rows");
const schema=raw.controls.schemas;ok(schema.valid.quantifiers==="exists_p_forall_E_forall_F","common quantifier");
ok(schema.invalid.length===10,"invalid schemas");
ok(schema.invalid.some(x=>x.quantifiers==="forall_E_exists_p_E_forall_F"),"encoderwise rejection");
ok(schema.invalid.some(x=>x.quantifiers==="forall_N_exists_E_N_exists_p_N"),"per-N rejection");
ok(raw.controls.malformed_rejected===8,"malformed");
ok(raw.classification.B1==="OPEN"&&raw.classification.B2==="OPEN"&&raw.classification.B3==="OPEN","bridges open");
ok(raw.classification.P_vs_NP==="OPEN","P vs NP");
console.log(JSON.stringify({status:"PASS",checks,parityRows,raw:rawPath}));

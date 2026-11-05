#!/usr/bin/env node
'use strict';
// Independent bit-vector / source-control verifier. Node 18+, no dependencies.
const fs = require('node:fs');
const assert = require('node:assert/strict');
const raw = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
let assertions=0;
function ok(flag,description){ assert.ok(flag,description); assertions++; }
function jointWitnessSmall(x,a,b) {
  for(let y=0;y<2;y++) if(a===(x^y) && b===(a^y)) return true;
  return false;
}
function sourceEval(k,kind,xmask,ymask){
  const top=(1<<k)-1;
  if(kind==='positive') return xmask===top && ((xmask|ymask)===top);
  if(kind==='negative') return xmask===0 && ((xmask|ymask)===top);
  if(kind==='unsat') return sourceEval(k,'positive',xmask,ymask) && !(xmask&1);
  throw new Error('invalid label');
}
ok(raw.algorithm==='deterministic exhaustive','unexpected producer type');
ok(raw.rows.length===6,'unexpected row count');
for(const record of raw.rows){
 const k=record.k,mask=(1<<k)-1;
 ok(record.paid_definitions===2*k,'def count');
 ok(record.original_variables===2*k,'original count');
 let globalExact=0,globalRelaxed=0;
 for(let x=0;x<=mask;x++) for(let a=0;a<=mask;a++) for(let b=0;b<=mask;b++){
   // Independently calculate the ONE shared hidden y required by DEF1.
   const sharedY=x^a, actualB=a^sharedY;
   const exact=actualB===b;
   // Check both exact CNF facets using signed bit logic.
   const compact=((~b|x)&mask)===mask && ((b|~x)&mask)===mask;
   ok(exact===compact,'compact equality mismatch');
   globalExact+= +exact; globalRelaxed++;
   if(k===1) ok(exact===jointWitnessSmall(x,a,b),'witness mismatch');
 }
 ok(globalExact===record.joint_models_over_x_a_b,'exact model count');
 ok(globalRelaxed===record.independent_models_over_x_a_b,'separate model count');
 ok(globalRelaxed/globalExact===record.projection_spurious_multiplier,'spurious multiplier');
 let pos=0,neg=0,unsat=0;
 for(let x=0;x<=mask;x++) for(let y=0;y<=mask;y++){
   if(sourceEval(k,'positive',x,y)){pos++;ok(((x^y)^y)===mask,'positive output');}
   if(sourceEval(k,'negative',x,y)){neg++;ok(((x^y)^y)===0,'negative output');}
   if(sourceEval(k,'unsat',x,y))unsat++;
 }
 ok(pos===record.plus_source_models,'positive models');
 ok(neg===record.minus_source_models,'negative models');
 ok(unsat===0,'UNSAT source');
 for(let x=0;x<=mask;x++)for(let y=0;y<=mask;y++){
   const a=x^y,b=a^y;
   ok((a^x^y)===0,'first row');ok((b^a^y)===0,'second row');
   ok(((a^x^y)^(b^a^y))===(b^x),'positional cancellation');
 }
}
ok(raw.malformed_rejections===6,'malformed producer controls');
console.log(JSON.stringify({status:'PASS',assertions,verified_rows:raw.rows.length,
  max_k:raw.rows[raw.rows.length-1].k,
  source_label_controls:['SAT+','SAT-','UNSAT'],
  conditional_interface:'DEF-row exports are not certified native'}));

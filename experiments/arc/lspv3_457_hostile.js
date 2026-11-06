#!/usr/bin/env node
'use strict';
// LSPV-3/457 focused hostile controls and both-label bit-PHP semantic controls.
// Usage: node experiments/arc/lspv3_457_hostile.js results/raw/review/2026-11-05_2253_LSPV5_FULL_COOK_FACETA379.json
const fs=require('fs'),{audit}=require('./lspv3_457_exact_original_support.js');
const file=process.argv[2];if(!file){console.error('raw 379 JSON required');process.exit(2);}
const original=JSON.parse(fs.readFileSync(file,'utf8')).traces[0];
function clone(v){return JSON.parse(JSON.stringify(v));}
const changes=[
 ['signed-source-flip',t=>{t.trace.sources[0].clause[0]*=-1;}],
 ['wrong-oriented-pivot',t=>{t.trace.nodes.find(x=>x.kind==='res').pivot=777777;}],
 ['out-of-range-facet',t=>{const n=t.trace.nodes.find(x=>x.kind==='res'&&x.left.includes('#f'));n.left=n.left.replace(/#f[012]/,'#f9');}],
 ['unowned-facet',t=>{const n=t.trace.nodes.find(x=>x.kind==='res'&&x.left.includes('#f'));n.left='X_UNOWNED#f2';}],
 ['original-output-collision',t=>{t.trace.nodes.find(x=>x.kind==='def').out=1;}],
 ['forward-pivot-parent',t=>{t.trace.nodes.find(x=>x.kind==='res').left='NOT_EARLIER';}],
 ['signed-DEF-input-flip',t=>{const n=t.trace.nodes.find(x=>x.kind==='def');n.a=-n.a;}]
];
const controls=[];
for(const [label,mutate] of changes){
 const t=clone(original);mutate(t);let reason=null;
 try{audit(t);}catch(e){reason=String(e.message);}
 if(!reason)throw Error('MUTATION ACCEPTED: '+label);
 controls.push({label,rejected:true,reason});
}
function modelCount(holes,pigeons){
 const total=Math.pow(holes,pigeons);let good=0;
 for(let i=0;i<total;i++){
  let n=i,used=new Set();
  for(let j=0;j<pigeons;j++){used.add(n%holes);n=Math.floor(n/holes);}
  if(used.size===pigeons)good++;
 }
 return good;
}
const m4=modelCount(4,4),m5=modelCount(4,5);
if(m4!==24||m5!==0)throw Error('both-label model control failed');
console.log(JSON.stringify({run_id:'LSPV-3/457',controls,both_label:{holes:4,sat_pigeons:4,sat_models:m4,unsat_pigeons:5,unsat_models:m5},passed:controls.length+2},null,2));
#!/usr/bin/env node
'use strict';
// LSPV-2/406 independent exhaustive bitmask verifier.
// The conditional unbounded-input support test is NOT native R_mix341.
const fs=require('fs');
const stats={id:'LSPV2_406_INDEPENDENT_JS',subsets:0,sat:0,unsat:0,assertions:0,hist:{},negative_controls:0};
function yes(cond,label){if(!cond)throw Error(label); stats.assertions++}
function clause(j,w){
 const p=!!(w&16),q=!!(w&32);
 switch(j){
 case 0:return p;case 1:return !p;case 2:return q;case 3:return !q;
 case 4:return p||q;case 5:return p||!q;case 6:return !p||q;case 7:return !p||!q;
 default:throw Error('invalid clause');
 }}
function C(mask,w){for(let i=0;i<8;i++)if((mask>>i)&1)if(!clause(i,w))return 0;return 1}
function f(mask,w){
 const u=w&1,a=(w>>1)&1,b=(w>>2)&1,z=(w>>3)&1;
 return ((!!u)||((a^b^(z&C(mask,w)))===1))?1:0;
}
for(let m=0;m<256;m++){
 let modelCount=0;
 for(let p=0;p<=1;p++)for(let q=0;q<=1;q++)modelCount+=C(m,(p<<4)|(q<<5));
 const support=[];
 for(let v=0;v<6;v++){
  let found=false;
  for(let w=0;w<64;w++)if(f(m,w)!==f(m,w^(1<<v))){found=true;break}
  if(found)support.push(v);
 }
 yes(support.includes(0)&&support.includes(1)&&support.includes(2),'base essential');
 yes(support.includes(3)===(modelCount>0),'z essential iff SAT');
 yes((support.length<=3)===(modelCount===0),'promise reduction');
 for(let w=0;w<64;w++)if(w&1)yes(f(m,w)===1,'source-entailment');
 if(modelCount)stats.sat++;else stats.unsat++;
 stats.hist[support.length]=(stats.hist[support.length]||0)+1;
 stats.subsets++;
}
for(let m of [0,1,2,3,7,255]){
 yes(f(m,1)===1,'source true');
 yes(f(m,0)===0,'u essential');
 stats.negative_controls++;
}
for(let x=0;x<=1;x++)for(let y=0;y<=1;y++){
 const a=x^y,b=a^y;
 yes((a^x^y)===0,'first defining XOR row');
 yes((b^a^y)===0,'second defining XOR row');
 yes(b===x,'nested cancellation');
}
yes(stats.subsets===256&&stats.sat===95&&stats.unsat===161,'label totals');
yes(stats.hist[3]===161&&stats.hist[4]===1&&stats.hist[5]===20&&stats.hist[6]===74,'support histogram');
const out=JSON.stringify(stats,null,2)+'\n';
if(process.argv[2])fs.writeFileSync(process.argv[2],out);
process.stdout.write(out);

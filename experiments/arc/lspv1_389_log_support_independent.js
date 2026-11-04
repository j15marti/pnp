#!/usr/bin/env node
/* Independent verifier for LSPV1/389 finite observations. No imported producer code. */
'use strict';
const fs=require('fs');
const path=process.argv[2] || 'raw.json';
const raw=JSON.parse(fs.readFileSync(path,'utf8'));
let checks=0;
function check(ok,msg){checks++;if(!ok)throw Error("verification failed: "+msg);}
function out(b,mask){
 let xs=Array.from({length:b},(_,i)=>(mask>>(b-1-i))&1);
 let sum=xs.reduce((a,c)=>a+c,0);
 return [Number(sum===b),Number(sum!==0),sum%2,Number(sum>=Math.ceil(b/2)),xs[0],1-xs[b-1],Number(xs[0]===1 && xs[b-1]===0)];
}
for(const row of raw.trials){
 const b=row.b, r=7;
 check(row.r===r && row.assignments===(1<<b),'b/r/count');
 let maps=Array.from({length:r},()=>[]);
 for(let code=0;code<(1<<b);code++){
  let vals=out(b,code);
  vals.forEach((v,j)=>maps[j].push(v));
  let replacement=row.truth_masks.map(s=>Number(s[code]));
  check(JSON.stringify(vals)===JSON.stringify(replacement),"joint "+b+"/"+code);
 }
 for(let j=0;j<r;j++){
   let m=maps[j],s=row.truth_masks[j];
   check(m.join('')===s,"mask "+b+"/"+j);
   check(m.reduce((a,v)=>a+v,0)===row.true_minterms[j],"minterms "+b+"/"+j);
 }
 check(row.budget_gates===r*b*(1<<b),'gate bound');
}
check(raw.controls.SAT===2 && raw.controls.UNSAT===2 && raw.controls.MALFORMED===3,'both labels/malformed ledger');
const pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function models(chg){
 let cnt=0;
 for(let t=0;t<64;t++){
  let pass=true;
  for(let v=0;v<4;v++){
   const parity=pairs.reduce((acc,p,i)=>acc^Number(p.includes(v)&&((t>>i)&1)),0);
   if(parity!==chg[v]){pass=false;break;}
  }
  if(pass)cnt++;
 }
 return cnt;
}
check(models([0,0,0,0])===raw.k4_parity.even_models,'even parity');
check(models([1,0,0,0])===raw.k4_parity.odd_models,'odd parity');
let controls=[ [[1]], [[1,2],[-1,2]], [[1],[-1]], [[1,2],[-1],[-2]], [[0]], [[3]], [[1,-1,0]] ];
let classify=cs=>{
 let valid=cs.every(cl=>cl.length>0&&cl.every(x=>Number.isInteger(x)&&x!==0&&Math.abs(x)<=2)&&new Set(cl.map(Math.abs)).size===cl.length);
 if(!valid)return 'MALFORMED';
 for(let mask=0;mask<4;mask++) if(cs.every(cl=>cl.some(v=>(((mask>>(Math.abs(v)-1))&1)===Number(v>0)))))return 'SAT';
 return 'UNSAT';
};
const expected=['SAT','SAT','UNSAT','UNSAT','MALFORMED','MALFORMED','MALFORMED'];
controls.forEach((cs,i)=>check(classify(cs)===expected[i],"case "+i));
console.log(JSON.stringify({id:raw.id,verifier_checks:checks,observed_cases:raw.trials.length,total_assignments:raw.trials.reduce((a,r)=>a+r.assignments,0),status:'PASS'},null,2));

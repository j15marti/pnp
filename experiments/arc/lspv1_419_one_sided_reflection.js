#!/usr/bin/env node
'use strict';
// Standalone, seed-free source/sentinel falsifiers for LSPV-1/419.
// Does not implement PV, Godel II or a hypothetical P-time SAT decider.
const c=[[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]];
const cm=c.map(cl=>{let z=0;for(let a=0;a<4;a++)if(cl.some(l=>Boolean(a&(1<<(Math.abs(l)-1)))===(l>0)))z|=1<<a;return z;});
const R={sat:0,unsat:0,exact:{reject:0,bad:0,miss:0},pair:{reject:0,bad:0,miss:0},always:{reject:0,bad:0,miss:0,badpairs:0},never:{reject:0,bad:0,miss:0}};
for(let s=0;s<256;s++){
 let models=15;for(let k=0;k<8;k++)if(s&(1<<k))models&=cm[k];
 let yes=models!==0;R[yes?'sat':'unsat']++;
 let pair=(s&3)===3||(s&12)===12;
 for(const [key,rej] of Object.entries({exact:!yes,pair,always:true,never:false})){
  let o=R[key];o.reject+=Number(rej);o.bad+=Number(rej&&yes);o.miss+=Number(!rej&&!yes);
  if(key==='always')for(let b=0;b<4;b++)o.badpairs+=Number(Boolean(models&(1<<b)));
 }
}
if(JSON.stringify([R.sat,R.unsat,R.pair.reject,R.pair.miss,R.always.bad,R.always.badpairs])!==JSON.stringify([95,161,112,49,95,128]))throw Error('classification mismatch');
let S={count:0,false_under_consistent:0,false_under_bad_toy:0,tamper_rejected:0};
function cnf(bits){return [...bits].map((b,i)=>[1,b==='1'?i+2:-(i+2)]);}
for(let n=0;n<=6;n++)for(let m=0;m<(1<<n);m++){
 let bits=n?m.toString(2).padStart(n,'0'):'', cs=cnf(bits);
 if(!cs.every((x,i)=>x[0]===1&&Math.abs(x[1])===i+2))throw Error('invalid sentinel');
 S.count++;S.false_under_bad_toy+=Number(bits==='101');
 if(cs.length){let tampered=cs.map(x=>x.slice());tampered[0][0]=-1;
   if(JSON.stringify(tampered)===JSON.stringify(cnf(bits)))throw Error('bad tamper');S.tamper_rejected++;}
}
if(S.count!==127||S.false_under_bad_toy!==1||S.false_under_consistent!==0||S.tamper_rejected!==126)throw Error('sentinel mismatch');
console.log(JSON.stringify({sources:R,sentinels:S,source_res:{input:[[1],[-1]],pivot:1,resolvent:[],paid:1},status:'FINITE ONLY; B3 OPEN'},null,2));

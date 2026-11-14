'use strict';
// TMR-3/019: finite locality/fingerprint adversarial checks, NOT a universal TM compiler.
const assert=require('node:assert/strict');
function src(x,j){return j===0?'<':j===x.length+1?'>':j>=1&&j<=x.length?x[j-1]:'_';}
function wr(t,j){return j<0?'!':j===0?'<':(t.get(j)||'_');}
function make(x,r,w,mode){
 const L=x.length,n=Number.parseInt(x,2),parity=[...x].filter(z=>z==='1').length%2;
 const sp=Array.from({length:r},(_,i)=>mode==='far'?(-2*L-10-n-i*3):mode==='mid'?(1+Math.floor((2*i+1)*L/(2*r))):(i%2?L+1:0));
 const wt=Array.from({length:w},(_,i)=>{
  let t=new Map();
  for(let j=1;j<=L;j++){
   const b=mode==='xor'?(([...x.slice(0,j)].filter(z=>z==='1').length+i)%2).toString():
      (i%2===0?x[j-1]:x[L-j]);
   t.set(j,b);
  }
  return t;
 });
 const wp=Array.from({length:w},(_,i)=>mode==='far'?2*L+6+n+i:mode==='mid'?Math.max(0,Math.floor(L*(i+1)/(w+1))):0);
 return {sp,wp,wt,control:parity};
}
function fp(x,m,t){
 const sides=j=>Array.from({length:2*t+1},(_,d)=>j+d-t);
 return JSON.stringify([m.control,m.sp.map(h=>sides(h).map(j=>src(x,j)).join('')),
  m.wp.map((h,i)=>sides(h).map(j=>wr(m.wt[i],j)).join(''))]);
}
function probe(x,m,p,t){
 let ss=m.sp.slice(),ww=m.wp.slice(),tt=m.wt.map(t=>new Map(t)),q=m.control,out=[];
 for(let step=0;step<=t;step++){
  let a=ss.map(j=>src(x,j)),b=ww.map((j,i)=>wr(tt[i],j));
  if(step===t){out.push(JSON.stringify([q,a,b,'halt']));break;}
  const score=q+p+step+a.join('').split('').reduce((s,z)=>s+z.charCodeAt(0),0)+b.join('').split('').reduce((s,z)=>s+z.charCodeAt(0),0);
  const dS=score%2===0?1:-1,dW=score%3===0?1:-1,bit=score%2?'1':'0';
  out.push(JSON.stringify([q,a,b,dS,dW,bit]));
  ss=ss.map(j=>j+dS);
  ww=ww.map((j,i)=>{if(j>0)tt[i].set(j,bit);return j===0&&dW===-1?0:j+dW;});
  q=(3*q+score)%7;
 }
 return out;
}
function run(){
 const out={status:'COMPUTATIONAL',role:'TMR-3/019',scope:'post-preprocessing INDEX, full-copy and far-head adversarial fingerprints',
   lengths:[6,13],radius:[0,3],counts:{cases:0,collision_witnesses:0,paired_probe_checks:0,full_copy_linear_space_cases:0,far_position_cases:0,full_copy_exactness_checks:0,failures:0},examples:[]};
 for(let L=6;L<=13;L++){
  let strings=Array.from({length:1<<L},(_,i)=>i.toString(2).padStart(L,'0'));
  for(let r of [1,2])for(let w of [1,2])for(let mode of ['left','mid','far','xor'])for(let t of [0,1,2,3]){
   out.counts.cases++;
   let seen=new Map(),pair=null;
   for(let x of strings){let m=make(x,r,w,mode),key=fp(x,m,t);
    if(seen.has(key)){pair=[seen.get(key),{x,m}];break;}
    seen.set(key,{x,m});
   }
   if(!pair)continue;
   const [a,b]=pair;
   assert.notEqual(a.x,b.x);
   const p=[...a.x].findIndex((v,i)=>v!==b.x[i])+1;
   assert(p>0);
   assert.equal(fp(a.x,a.m,t),fp(b.x,b.m,t));
   assert.deepEqual(probe(a.x,a.m,p,t),probe(b.x,b.m,p,t));
   out.counts.collision_witnesses++;
   out.counts.paired_probe_checks++;
   if(w>0)out.counts.full_copy_linear_space_cases++;
   if(mode==='far')out.counts.far_position_cases++;
   if(out.examples.length<9)out.examples.push({L,r,w,mode,t,source_a:a.x,source_b:b.x,query:p});
  }
 }
 // All-width copy regression: for L-bit x, s=L cells is enough to retain all bits,
 // but a query still needs paid movement on a local-head tape.
 for(let L=1;L<=12;L++)for(let n=0;n<1<<L;n++){
  let x=n.toString(2).padStart(L,'0'),m=make(x,1,1,'left');
  assert.equal(Array.from({length:L},(_,i)=>wr(m.wt[0],i+1)).join(''),x);
  out.counts.full_copy_exactness_checks++;
 }
 return out;
}
console.log(JSON.stringify(run(),null,2));

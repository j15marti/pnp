"use strict";
function runM10Count(){
 const bit=i=>1n<<BigInt(i),pop=x=>{let n=0;while(x){x&=x-1n;n++}return n};
 const assert=(v,m)=>{if(!v)throw Error(m)};
 let seed=10102026;
 const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 const stats={seed:10102026,randomCases:0,targetChecks:0,certifiedSAT:0,affineUNSAT:0,UNKNOWN:0,uniformAccepted:0,uniformDeclined:0,referenceWords:0,gaussianCalls:0,prefixSteps:0,scales:[]};
 function span(cols,t){stats.gaussianCalls++;const p=new Map();let rank=0;
   for(let v of cols){while(v){const j=v.toString(2).length-1;if(p.has(j))v^=p.get(j);else{p.set(j,v);rank++;break}}}
   while(t){const j=t.toString(2).length-1;if(!p.has(j))return {count:0n,rank};t^=p.get(j)}
   return {count:bit(cols.length-rank),rank};
 }
 function prepare(g,w){
   const k=g.length,C=[[1n]];
   for(let i=1;i<=k;i++){const a=[];for(let j=0;j<=i;j++)a.push((C[i-1][j-1]||0n)+(C[i-1][j]||0n));C.push(a)}
   return {k,g,w,cols:g.map(v=>(v<<1n)|1n),C,W:w.reduce((a,b)=>a+b,0n),wp:w.map(v=>Number(v&1n))};
 }
 // Count bad words with the required full-word parity, ignoring affine tag equations.
 // The sum double-counts overlaps, deliberately remaining an upper bound.
 function tail(D,n,prefixWt,limit,fullParity){
   let b=0n;
   for(let j=0;j<=n;j++)if(BigInt(prefixWt+j)>limit&&((prefixWt+j)&1)===fullParity)b+=D.C[n][j];
   return b;
 }
 function bound(D,H,len=0,a=0,b=0){
   const eps=Number(H&1n),wp=D.wp.reduce((x,y)=>x^y,0);
   return tail(D,D.k-len,a,H,eps)+tail(D,D.k-len,b,D.W-H,eps^wp);
 }
 function lift(D,H,p){
   const x=D.w.map((w,i)=>p&bit(i)?1n:0n);let d=H-x.reduce((a,b)=>a+b,0n);
   assert(d>=0n&&!(d&1n),"lower");
   for(let i=0;i<x.length;i++){let room=D.w[i]-x[i];room-=room&1n;const v=room<d?room:d;x[i]+=v;d-=v}
   assert(!d,"upper");return x;
 }
 function verify(D,H,t,p){
   const x=lift(D,H,p);let s=0n,tag=0n;
   for(let i=0;i<x.length;i++){assert(x[i]>=0n&&x[i]<=D.w[i],"capacity");s+=x[i];if(x[i]&1n)tag^=D.g[i]}
   assert(s===H&&tag===t,"reconstruction");
 }
 function solve(D,H,t){
   if(H<0n||H>D.W)return {status:"UNSAT"};
   let tar=(t<<1n)|(H&1n),A=span(D.cols,tar),B=bound(D,H);
   if(!A.count)return {status:"UNSAT"};
   if(A.count<=B)return {status:"UNKNOWN"};
   let a=0,b=0,p=0n;
   for(let i=0;i<D.k;i++){
     let chosen=false;
     for(let v=0;v<=1;v++){
       const t2=tar^(v?D.cols[i]:0n),a2=a+v,b2=b+(v^D.wp[i]),s=span(D.cols.slice(i+1),t2);
       if(s.count>bound(D,H,i+1,a2,b2)){tar=t2;a=a2;b=b2;if(v)p|=bit(i);chosen=true;break}
     }
     assert(chosen,"prefix count conservation");stats.prefixSteps++;
   }
   verify(D,H,t,p);
   return {status:"SAT",p,coset:A.count,bad:B,fullHull:A.count>2n*B};
 }
 function uniform(D,L,U){
   if(L<0n||U>D.W||L>U)return false;
   const A=span(D.cols,0n),wp=D.wp.reduce((x,y)=>x^y,0);
   for(let eps=0;eps<2;eps++){
     const lo=L+((L&1n)===BigInt(eps)?0n:1n),up=U-((U&1n)===BigInt(eps)?0n:1n);
     if(lo>up)continue;
     const B=tail(D,D.k,0,lo,eps)+tail(D,D.k,0,D.W-up,eps^wp);
     if(A.count<=B)return false;
   }
   return true;
 }
 for(let it=0;it<180;it++){
   const k=2+rand(8),g=Array.from({length:k},()=>BigInt(rand(8))),w=Array.from({length:k},()=>BigInt(1+rand(4))),D=prepare(g,w);
   const h=BigInt(rand(Number(D.W+1n))),actual=new Map();
   for(let p=0n;p<bit(k);p++){
     stats.referenceWords++;const n=BigInt(pop(p));let hi=0n,t=0n;
     for(let j=0;j<k;j++){const z=(p&bit(j))?1n:0n;hi+=w[j]-((w[j]-z)&1n);if(z)t^=g[j]}
     if(n<=h&&h<=hi&&((h-n)&1n)===0n){if(!actual.has(t))actual.set(t,[]);actual.get(t).push(p)}
   }
   for(let t=0n;t<8n;t++){const q=solve(D,h,t);stats.targetChecks++;
     if(q.status==="SAT"){stats.certifiedSAT++;assert(actual.has(t),"false SAT");if(q.fullHull){
       // Check rank of actual differences against original affine coset dimension.
       const words=actual.get(t),r=span(words.map(p=>p^words[0]),0n).rank;
       assert(bit(r)===q.coset,"false full hull");
     }}else if(q.status==="UNSAT"){stats.affineUNSAT++;assert(!actual.has(t),"false UNSAT")}else stats.UNKNOWN++;
   }
   const L=BigInt(rand(Number(D.W+1n))),U=L+BigInt(rand(Number(D.W-L+1n)));
   if(uniform(D,L,U)){
     stats.uniformAccepted++;
     for(let H=L;H<=U;H++)for(let t=0n;t<8n;t++){
       const A=span(D.cols,(t<<1n)|(H&1n));
       if(A.count)assert(solve(D,H,t).status==="SAT","uniform certificate");
     }
   }else stats.uniformDeclined++;
   stats.randomCases++;
 }
 for(const k of [32,64,128,256,512]){
   const r=Math.max(1,k/16),base=Math.ceil(Math.log2(k));
   const g=Array.from({length:k},(_,i)=>i<k-r?BigInt(i):bit(base+i-(k-r))),w=Array(k).fill(2n),D=prepare(g,w);
   const H=BigInt(3*k/4),A=span(D.cols,0n),B=bound(D,H),cert=uniform(D,H,H),q=solve(D,H,0n);
   assert(q.status===(cert?"SAT":"UNKNOWN"),"scale classification");
   if(k>=64)assert(cert,"scale saturation expected");
   stats.scales.push({classes:k,physicalUnitArcs:2*k,rank:A.rank,affineNullity:k-A.rank,defect:k-Number(H),cosetSize:A.count.toString(),badUpper:B.toString(),certified:cert,targetZero:q.status});
 }
 return stats;
}
console.log(JSON.stringify(runM10Count(),null,2));

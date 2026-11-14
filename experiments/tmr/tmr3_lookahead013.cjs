"use strict";
// TMR-3/013 bounded-lookahead conditional Kraft audit. Run: node experiments/tmr/tmr3_lookahead013.cjs
const audit = function audit(){
 "use strict";
 const cases=[[3,1,2,1],[3,1,2,2],[3,1,3,1],[3,1,3,3],[3,1,4,1],[3,1,4,2],[3,1,4,4],[4,2,2,1],[4,2,2,2],[4,2,3,1],[4,2,3,3],[4,2,4,1],[4,2,4,2],[4,2,4,4]];
 function chk(b,s){if(!b)throw Error(s);}
 function unpack(z,n,N){const a=[];for(let i=0;i<n;i++){a.push(z%N);z=Math.floor(z/N);}return a;}
 function prefixFree(a){a.sort();for(let i=1;i<a.length;i++)if(a[i].startsWith(a[i-1]))return false;return true;}
 function code(xs,i,q,t,d){
   const ell=q-t,mask=(1<<ell)-1,base=Math.floor(i/d)*d;
   let hi=0,lo=0;
   for(let j=base;j<Math.min(xs.length,base+d);j++)if(j!==i){hi^=xs[j]>>ell;lo^=xs[j]&mask;}
   const x=xs[i];
   if((x>>ell)===hi&&(x&mask)!==lo){const v=x&mask;return (v-(v>lo?1:0)).toString(2).padStart(ell,"0");}
   return "1".repeat(ell)+x.toString(2).padStart(q,"0");
 }
 function adaptive(xs,i,q,t,r){
  const ell=q-t,N=1<<q;let sh=0;
  for(let j=0;j<Math.min(xs.length,i+r+1);j++)if(j!==i)sh^=xs[j];
  const rank=(xs[i]^sh)&(N-1);
  return rank<(1<<ell)-1 ? rank.toString(2).padStart(ell,"0") : "1".repeat(ell)+xs[i].toString(2).padStart(q,"0");
 }
 const rows=[];let totalVectors=0,totalFibers=0,totalWords=0;
 for(const [q,t,K,d] of cases){
   const N=1<<q,ell=q-t,p=((1<<ell)-1)/N,delta=2**(-t)*(1+2**(-q)),threshold=q+Math.log2(delta);
   let fibers=0,words=0,events=0;
   for(let i=0;i<K;i++){
     const base=Math.floor(i/d)*d,others=[];for(let j=base;j<base+d;j++)if(j!==i)others.push(j);
     for(let z=0;z<N**(d-1);z++){
       const vals=unpack(z,d-1,N),xs=Array(K).fill(0);
       others.forEach((j,v)=>{xs[j]=vals[v]});
       const all=[];
       for(let x=0;x<N;x++){xs[i]=x;all.push(code(xs,i,q,t,d));}
       chk(prefixFree(all),"prefix code failed");
       chk(all.filter(x=>x.length===ell).length===(1<<ell)-1,"short count failed");
       fibers++;words+=N;
     }
   }
   for(let z=0;z<N**K;z++){
     const xs=unpack(z,K,N),lens=xs.map((_,i)=>code(xs,i,q,t,d).length);
     for(let a=0;a<K;a+=d)for(let j=a+1;j<a+d;j++)chk(lens[j]===lens[a],"group lengths differ");
     let allShort=true;
     for(let a=0;a<K;a+=d){
       let hi=0,lo=0;
       for(let j=a;j<a+d;j++){hi^=xs[j]>>ell;lo^=xs[j]&((1<<ell)-1);}
       if(hi!==0||lo===0)allShort=false;
     }
     const bad=lens.reduce((x,y)=>x+y,0)/K < threshold;
     chk(bad===allShort,"aggregate event differs");
     if(bad)events++;
   }
   const probability=events/(N**K), upper=delta**(K/d);
   chk(Math.abs(probability-p**(K/d))<1e-12,"exact tail mismatch");
   chk(probability<=upper+1e-12,"lookahead bound failed");
   rows.push({q,t,K,lookahead:d-1,conditioned_fibers:fibers,codewords:words,global_vectors:N**K,tail_events:events,probability,upper});
   totalVectors+=N**K;totalFibers+=fibers;totalWords+=words;
 }
 const adaptiveRows=[];let adaptiveFibers=0;
 const q=3,t=1,K=4,N=1<<q;
 for(let r=0;r<K;r++){
   let fibers=0;
   for(let i=0;i<K;i++){
     const others=[];for(let j=0;j<Math.min(K,i+r+1);j++)if(j!==i)others.push(j);
     for(let z=0;z<N**others.length;z++){
       const vals=unpack(z,others.length,N),xs=Array(K).fill(0),all=[];
       others.forEach((j,v)=>{xs[j]=vals[v]});
       for(let x=0;x<N;x++){xs[i]=x;all.push(adaptive(xs,i,q,t,r));}
       chk(prefixFree(all),"adaptive prefix failed");fibers++;
     }
   }
   adaptiveFibers+=fibers;
   const sums=[];for(let z=0;z<N**K;z++){
     const xs=unpack(z,K,N);
     let sum=0;for(let i=0;i<K;i++)sum+=adaptive(xs,i,q,t,r).length;
     sums.push(sum);
   }
   for(const delta of [0.4,0.6,0.8]){
     const count=sums.filter(sum=>sum<K*(q+Math.log2(delta))).length;
     const upper=delta**(K/(r+1));
     chk(count/sums.length<=upper+1e-12,"adaptive bound failed");
     adaptiveRows.push({lookahead:r,delta,tail_events:count,global_vectors:sums.length,probability:count/sums.length,upper});
   }
 }
 const p=3/16,delta=(1+1/16)/4;
 chk(p>delta**4 && p<delta,"hostile all-future control failed");
 return {name:"TMR-3/013 bounded future lookahead Kraft/Hölder concentration",
   method:"exact exhaustive hosted V8, deterministic; independent native Python separately executed",seed:null,
   model:"q-bit independent blocks; conditioned prefix-free code at each cut; lookahead r",
   totals:{group_cases:rows.length,group_vectors:totalVectors,conditioned_fibers:totalFibers,conditioned_codewords:totalWords,adaptive_inequality_checks:adaptiveRows.length,adaptive_fibers:adaptiveFibers,adaptive_vectors:adaptiveRows.length*N**K,failures:0},
   group_cases:rows,adaptive_cases:adaptiveRows,
   hostile_noncausal:{q:4,t:2,K:4,actual_tail:p,false_zero_lookahead_bound:delta**4,correct_three_lookahead_bound:delta},
   finite_status:"COMPUTATIONAL",SAT_scope:"NO unrestricted SAT-processing bound established"};
};
const result = audit();
console.log(JSON.stringify(result,null,2));

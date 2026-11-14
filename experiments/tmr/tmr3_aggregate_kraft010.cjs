#!/usr/bin/env node
"use strict";
const runAudit=function runAudit(){
  "use strict";
  let seed=0x3A9C2701;
  function rand(){seed^=seed<<13; seed^=seed>>>17; seed^=seed<<5; return (seed>>>0);}
  function scramble(a){for(let i=a.length-1;i>0;i--){const j=rand()%(i+1);[a[i],a[j]]=[a[j],a[i]];}return a;}
  function prefixCode(q){const N=2**q;let leaves=[""];while(leaves.length<N){let i=rand()%leaves.length;const pre=leaves[i];leaves.splice(i,1,pre+"0",pre+"1");}return scramble(leaves).map(s=>s.length);}
  function nonPrefix(q){const N=2**q,out=[];for(let j=0;j<q;j++)for(let i=0;i<2**j;i++)out.push(j);out.push(q);if(out.length!==N)throw Error("bad");return out;}
  let cases=0, codebooks=0, assignments=0, tailTests=0, violations=0, momentFailures=0, maxFailureRatio=0, minLHS=Infinity, maxGap=0;
  let examples=[];
  for(let q=2;q<=8;q++)for(const K of [1,2,4,8,16,32])for(let trial=0;trial<12;trial++){
    const N=2**q, cuts=[];
    for(let k=0;k<K;k++)cuts.push(trial%3===0&&k>0?cuts[0].slice():prefixCode(q));
    codebooks+=K;
    const codesum=cuts.map(a=>a.reduce((s,v)=>s+2**(-v),0));
    for(const z of codesum)if(Math.abs(z-1)>1e-9)throw Error("non Kraft code!");
    const values=[];
    let eY=0;
    for(let a=0;a<N;a++){
      let total=0,Y=0;
      for(let k=0;k<K;k++){const len=cuts[k][a];total+=len;Y+=2**(q-len);}
      eY+=Y/K/N;values.push(total/K);minLHS=Math.min(minLHS,total/K);
    }
    if(eY>1+1e-8)momentFailures++;
    for(const p of [1,2,3,4,5,6]){
      const delta=2**(-p), threshold=q-p;
      let failures=0;
      for(const avg of values)if(avg<threshold-1e-12)failures++;
      tailTests++;
      const prob=failures/N;
      maxFailureRatio=Math.max(maxFailureRatio,prob/delta);
      if(prob>delta+1e-12){violations++;examples.push({q,K,trial,p,prob,delta});}
    }
    assignments+=N;cases++;
  }
  const q=4,N=2**q,base=nonPrefix(q),K=N,nonprefix=[];
  for(let k=0;k<K;k++)nonprefix.push(base.map((_,a)=>base[(a+k)%N]));
  let bad=0;
  for(let a=0;a<N;a++){let avg=0;for(const b of nonprefix)avg+=b[a]/K;if(avg<q-1)bad++;}
  const negative={q,K,avg:base.reduce((a,b)=>a+b,0)/N,delta:.5,actualBad:bad/N,violates:bad/N>.5,rawKraft:base.reduce((a,b)=>a+2**(-b),0)};
  for (const m of [16,32,64,128,256]){
    const q=Math.floor(m/2), n=256;
    if(m>n)continue;
    const w=Math.ceil(Math.log2(5*n)),g=12*(w+1),L=13*n+2+2*n*g;
    const K=Math.floor(n/m)*(q*g-1);
    examples.push({m,q,L,K,oldFailureBound:Math.min(1,K*2**(-q/2)),newFailureBound:2**(-q/2),lowerCoefficient:"1/512"});
  }
  return {name:"TMR3-AGGREGATE-KRAFT10",seed:"0x3A9C2701",cases,codebooks,assignments,tailTests,violations,momentFailures,maxFailureRatio,minAverageLength:minLHS,negative,examples};
};
const result=runAudit();
process.stdout.write(JSON.stringify(result,null,2)+'\n');
if(result.violations||result.momentFailures||!result.negative.violates)process.exitCode=1;

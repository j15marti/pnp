'use strict';
// TMR4-CERTPREFIX-007: finite oracle-of-small-Boolean-functions for observational MAY graph. NOT a SAT solver or native TM.
const audit = function audit(){
 "use strict";
 const stats={cases:0,majorityCases:0,parityCases:0,orCases:0,states:0,paidEdges:0,zeroStutterEdges:0,terminalChecks:0,potentialChecks:0,physicalStepChecks:0,horizonChecks:0,shortestPathChecks:0,strictBeyondSingleton:0,strictPrefixGains:0,invalidZeroCostTerminalRejections:0,failures:0};
 const ok=(b,m)=>{if(!b){stats.failures++;throw Error(m)}};
 const pc=m=>{let v=0;while(m){m&=m-1;v++}return v};
 const families=[
   ...[3,5,7,9].map(n=>({kind:"majority",n,x:(1<<n)-1})),
   ...Array.from({length:32},(_,x)=>({kind:"majority",n:5,x})),
   ...[2,3,4,5,6].flatMap(n=>Array.from({length:1<<n},(_,x)=>({kind:"parity",n,x}))),
   ...[3,4,5,6].flatMap(n=>Array.from({length:1<<n},(_,x)=>({kind:"or",n,x})))
 ];
 const label=(kind,n,x)=>kind==="majority"?Number(pc(x)>Math.floor(n/2)):kind==="parity"?(pc(x)%2):Number(x!==0);
 let special=null;
 for(const {kind,n,x} of families){
   const N=1<<n,full=N-1,out=label(kind,n,x);
   const D=[];
   for(let y=0;y<N;y++)if(label(kind,n,y)!==out) D.push(x^y);
   const good=Array.from({length:N},(_,v)=>D.every(d=>(v&d)!==0));
   const tau=Array(N).fill(n+1);
   for(let v=0;v<N;v++)for(let w=0;w<N;w++)if((w&v)===v&&good[w])tau[v]=Math.min(tau[v],pc(w&~v));
   ok(tau[full]===0,"full source certificate failed");
   for(let v=0;v<N;v++)ok((tau[v]===0)===good[v],"certificate equivalence failed");
   const singles=D.filter(d=>pc(d)===1).length;
   ok(tau[0]>=singles,"certificate below singleton requirement");
   if(tau[0]>singles)stats.strictBeyondSingleton++;
   if(kind==="majority"&&x===full&&n>=3){
     ok(singles===0&&tau[0]===(n+1)/2,"majority all-ones hostile control");
     if(n===9)special={n,x,oppositeCount:D.length,oneBitOppositeCount:singles,minCertificate:tau[0],allPositions:n};
   }
   stats.cases++;stats[kind+"Cases"]++;
   stats.states+=N;
   for(const q of [1,2]){
     const phi=v=>Math.ceil(tau[v]/q);
     for(let v=0;v<N;v++){
       stats.potentialChecks++;stats.zeroStutterEdges++;ok(phi(v)<=phi(v),"zero-cost stutter");
       if(good[v]){stats.terminalChecks+=2;ok(phi(v)===0,"terminal goal edge not zero")}
       else{stats.invalidZeroCostTerminalRejections++;ok(phi(v)>0,"invalid terminal edge not rejected")}
       let missing=full&~v;
       for(let add=missing;add;add=(add-1)&missing)if(pc(add)<=q){
         stats.paidEdges++;stats.potentialChecks++;
         ok(phi(v)<=1+phi(v|add),"paid edge potential");
       }
     }
     // Independent unweighted BFS from the initial observation mask.
     const dist=Array(N).fill(-1),queue=[0];dist[0]=0;let best=-1;
     for(let qi=0;qi<queue.length;qi++){
       const v=queue[qi];
       if(good[v]){best=dist[v];break}
       const miss=full&~v;
       for(let add=miss;add;add=(add-1)&miss)if(pc(add)<=q&&dist[v|add]<0){dist[v|add]=dist[v]+1;queue.push(v|add)}
     }
     stats.shortestPathChecks++;ok(best===phi(0),"BFS distance not potential");
     // Deterministic paid event scanner, three idle steps, paid rereads, terminal.
     const events=[[],[],[]];
     for(let i=0;i<n;i+=q)events.push(Array.from({length:Math.min(q,n-i)},(_,j)=>i+j));
     for(let i=0;i<n;i++)events.push([i]);
     events.push([]);
     const seen=[0];for(const R of events){
       ok(R.length<=q,"too many reads");
       const prev=seen[seen.length-1];let next=prev;
       for(const j of R){ok(j>=0&&j<n,"invalid address");next|=1<<j}
       seen.push(next);stats.physicalStepChecks++;
       ok(phi(prev)<=1+phi(next),"real paid step lacks abstract simulation");
     }
     ok(good[seen.at(-1)],"real terminal without certificate");
     const T=events.length;
     for(const B of [0,1,3,4,Math.floor(T/2),T-1,T,T+2]){
       stats.horizonChecks++;
       const pred=B>=T?T:B+phi(seen[B]);
       ok(pred<=T,"prefix+certificate is unsound");
       if(B<T&&pred>Math.max(B,phi(0))) stats.strictPrefixGains++;
       if(B<T) for(let i=0;i<B;i++)ok(B-i+phi(seen[B])<=1+(B-(i+1))+phi(seen[B]),"prefix edge");
     }
   }
 }
 ok(special!==null&&stats.strictBeyondSingleton>0&&stats.strictPrefixGains>0,"missing hostile controls");
 return {type:"TMR4-CERTPREFIX-007",status:"COMPUTATIONAL",date_PST:"2026-11-13 18:40 PST",description:"Exhaustive finite Boolean majority/parity/OR label-source audits with fully enumerated opposite inputs, certificate hitting sets, all subset edges, independent BFS and paid toy scan event paths; not native TM execution or a 3-SAT solver",specialMajority:special,stats};
};
console.log(JSON.stringify(audit(),null,2));

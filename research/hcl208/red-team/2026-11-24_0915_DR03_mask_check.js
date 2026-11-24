"use strict";
function run(){
 const result={masks:0,sat:0,unsat:0,sourceAssignments:0,verifiedLifts:0,implicationArcs:0,discrepancies:0,controls:[]};
 for(let mask=0;mask<16;mask++){
   // 0 = center; 1..4 = leaves. Guard all leaves equal.
   const edgeSigns=[0,1,2,3].filter(q=>mask&(1<<q));
   const adj=Array.from({length:4},(_,i)=>new Set([i]));
   for(const q of edgeSigns){
     // literals are indexed 2*coordinate+truth-value.
     // Clause (y0 != q0) OR (y1 != q1).
     let a=1-(q&1),b=2+1-(q>>1);
     adj[a^1].add(b);adj[b^1].add(a);result.implicationArcs+=2;
   }
   for(let k=0;k<4;k++)for(let i=0;i<4;i++)if(adj[i].has(k))for(const j of adj[k])adj[i].add(j);
   let sat=![0,2].some(i=>adj[i].has(i^1)&&adj[i^1].has(i));
   let count=0,witness=null;
   for(let x=0;x<1024;x++){
     result.sourceAssignments++;const c=Array.from({length:5},(_,i)=>(x>>(2*i))&3);
     if(c.slice(2).every(y=>y===c[1])&&edgeSigns.every(q=>(c[0]^c[q+1])!==q)){count++;witness=c}
   }
   if(sat!==!!count||count!==4*(4-edgeSigns.length))throw Error("aligned star discrepancy");
   if(sat){const y=[0,1,2,3].find(q=>!edgeSigns.includes(q));const c=[0,y,y,y,y];if(!edgeSigns.every(q=>(c[0]^c[q+1])!==q))throw Error("lift");result.verifiedLifts++;}
   result.masks++;result[sat?"sat":"unsat"]++;result.controls.push({mask,models:count,sat});
 }
 return result;
}
console.log(JSON.stringify(run(),null,2));

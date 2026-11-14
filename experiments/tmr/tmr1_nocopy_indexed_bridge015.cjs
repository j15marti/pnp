"use strict";
const result=(function audit(){
"use strict";
const stats={sources:0,queryCases:0,invalidQueries:0,outOfRange:0,repeatedReadPairs:0,sourceMoves:0,addressMoves:0,counterMoves:0,chargedMicrosteps:0,spaceChecks:0,boundChecks:0,dynamicTraces:0,accept:0,reject:0,failures:0,maxWidth:0,maxLength:0,runner:"hosted V8, standalone deterministic microstep ledger",seed:"none, exhaustive"};
const assert=(condition,msg)=>{if(!condition){stats.failures++;throw Error(msg)}};
const R="#";
function query(source,index,invalid,startHead) {
 const L=source.length,w=Math.ceil(Math.log2(L+2));stats.maxWidth=Math.max(w,stats.maxWidth);
 let sourceHead=startHead, addressHead=0, counterHead=0, cost=0, counter=Array(w).fill("0"); const visited=new Set();
 function step(kind){cost++;stats.chargedMicrosteps++;if(kind==="s")stats.sourceMoves++;if(kind==="a")stats.addressMoves++;if(kind==="c")stats.counterMoves++}
 function moveC(target){while(counterHead!==target){counterHead+=counterHead<target?1:-1;visited.add(counterHead);step("c")}}
 function moveA(target){while(addressHead!==target){addressHead+=addressHead<target?1:-1;step("a")}}
 function zero(){let z=true;moveC(0);for(let p=0;p<w;p++){moveC(p);if(counter[p]!=="0")z=false;step("c")}return z}
 function decrement(){moveC(w-1);let p=w-1;while(true){visited.add(p);counter[p]=counter[p]==="1"?"0":"1";step("c");if(counter[p]==="0")break;p--;assert(p>=0,"decrement underflow");moveC(p)}}
 let bit=R;
 if(invalid){stats.invalidQueries++;step("a")}
 else {
   assert(Number.isInteger(index)&&index>=0&&index<2**w,"out of width query");
   const digits=index.toString(2).padStart(w,"0");
   for(let p=0;p<w;p++){moveA(p+1);moveC(p);counter[p]=digits[p];visited.add(p);step("c")}
   moveA(0); 
   while(sourceHead>0){sourceHead--;step("s")}
   sourceHead++;step("s");
   while(sourceHead<=L){
     if(zero()){bit=source[sourceHead-1];break}
     sourceHead++;step("s");
     if(sourceHead===L+1)break;
     decrement();
   }
   if(index>=L)stats.outOfRange++;
 }
 step("a"); // paid execution of the delayed original indexed-query transition
 assert(visited.size<=w,"scratch work exceeded w");
 assert(cost<=50*(L+2)*(w+1),"conservative physical-step bound failed");
 stats.spaceChecks++;stats.boundChecks++;
 return {bit,endHead:sourceHead,cost,w,visited:visited.size}
}
for(let L=0;L<=9;L++){
 for(let n=0;n<2**L;n++){
  const source=n.toString(2).padStart(L,"0").slice(-L); // corrected empty case below
  const x=L===0?"":source;stats.sources++;stats.maxLength=L;
  const w=Math.ceil(Math.log2(L+2)), cap=2**w;
  const startHeads=[0,Math.floor((L+1)/2),L+1];
  for(let h of startHeads){
   let last=-1;
   for(let address=0;address<cap;address++){
    let got=query(x,address,false,h); stats.queryCases++;
    assert(got.bit===(address<L?x[address]:R),`query mismatch L=${L} addr=${address}`);
    if(address===last)stats.repeatedReadPairs++;last=address;
   }
   for(let address of [0,Math.floor(cap/2),cap-1]){
    let got=query(x,address,true,h);stats.queryCases++;
    assert(got.bit===R,`invalid query leaked input`);
   }
  }
  // Adaptive source-bit reads: finite deterministic transition recurrence (no oracle).
  let bit=0,prev=0,head=0;
  for(let t=0;t<9;t++){
    const addr=(3*t+5*bit+prev)%(2**w); 
    let got=query(x,addr,false,head);stats.queryCases++;stats.dynamicTraces++;
    let direct=addr<L?x[addr]:R;
    assert(got.bit===direct,"adaptive query mismatch");
    let obs=got.bit===R?0:Number(got.bit);
    prev=addr;bit=(bit^obs)&1;head=got.endHead;
  }
  if(bit)stats.accept++;else stats.reject++;
 }
}
assert(stats.failures===0,"test failures");
return stats;
})();
console.log(JSON.stringify(result,null,2));

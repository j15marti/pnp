/* Independent control: direct hub-color enumeration using BigInt,
   no Python source files or Python count function. */
'use strict';
const fs = require('fs');
const out = c => [((c+1)%5), ((c+3)%5)];
function subsets(k) {
  const a=[];
  for (let mask=1;mask<(1<<k);mask++) {
    if (pop(mask)>=2) a.push(mask);
  }
  return a;
}
function pop(m){let r=0;while(m){m&=m-1;r++}return r}
function calc(k,unsat) {
 const Ss=subsets(k);let total=0n, valid=0;
 const labels=Array(k).fill(0);
 function rec(pos){
  if(pos===k){
   if(unsat){
    for(let u=0;u<6;u++)for(let v=u+1;v<6;v++)
      if(!out(labels[u]).includes(labels[v]))return;
   }
   let ways=1n;
   for(const s of Ss){
    let possibilities=0b11111;
    for(let i=0;i<k;i++)if(s&(1<<i)){
      const [p,q]=out(labels[i]);
      possibilities &= (1<<p) | (1<<q);
    }
    const q=pop(possibilities);
    if(q===0)return;
    ways*=BigInt(q);
   }
   valid++;
   total+=ways;return;
  }
  for(let a=0;a<5;a++){labels[pos]=a;rec(pos+1)}
 }
 rec(0);
 return {k, unsat, number_hubs:k, number_leaves:Ss.length, valid_hub_labelings:valid,
         count:total.toString()};
}
const results=[];
for(let k=3;k<=7;k++) {
 results.push(calc(k,false));
 if(k>=6)results.push(calc(k,true));
}
const fn=process.argv[2] || 'independent.json';
fs.writeFileSync(fn,JSON.stringify({tool:'independent_node_bigint',results},null,2)+'\n');
console.log(JSON.stringify(results.map(r=>({k:r.k,unsat:r.unsat,digits:r.count.length}))));

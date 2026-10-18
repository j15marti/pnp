"use strict";
// Exhaustive n=2 circuits with <=2 AND/OR/NOT gates; Node.js 18+.
const values=[0,15,12,10], C=Array(16).fill(null);
function enumerate(w,d){
  for(const v of w)if(C[v]===null||d<C[v])C[v]=d;
  if(d===2)return;
  const out=new Set();
  for(const a of w){out.add((~a)&15);for(const b of w){out.add(a&b);out.add(a|b)}}
  for(const v of out)enumerate(w.concat(v),d+1);
}
enumerate(values,0);
function bits(v){let k=0;while(v){v&=v-1;k++}return k}
const rows=[];
for(let s=0;s<=2;s++){
 const Y=Array.from({length:16},(_,i)=>i).filter(x=>C[x]!==null&&C[x]<=s);
 const H=Array.from({length:16},(_,i)=>i).filter(x=>C[x]===null||C[x]>s);
 let edge;
 for(const y of Y){for(const f of H)if(bits(y^f)===1){edge=[y,f];break}if(edge)break}
 const sample=[];
 for(let k=0;k<=4;k++){
  let count=0,partial_yes=0,collision=0;
  for(let S=0;S<16;S++)if(bits(S)===k){
   count++;
   if(Y.some(y=>(y&S)===(edge[1]&S)))partial_yes++;
   if((edge[0]&S)===(edge[1]&S))collision++;
  }
  sample.push({k,count,partial_yes,collision});
 }
 rows.push({s,yes_count:Y.length,no_count:H.length,edge,sample});
}
console.log(JSON.stringify({C,rows},null,2));

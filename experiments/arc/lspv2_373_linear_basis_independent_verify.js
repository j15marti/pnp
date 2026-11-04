#!/usr/bin/env node
/* Separate implementation: independently check all charge-coordinate cases. */
'use strict';
let checks=0;
function check(b,m){checks++;if(!b)throw Error(m);}
function graphs(){
 const k4=[],k33=[],cube=[],p=[];
 for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)k4.push([i,j]);
 for(let i=0;i<3;i++)for(let j=3;j<6;j++)k33.push([i,j]);
 for(let i=0;i<8;i++)for(let b=0;b<3;b++){let j=i^(1<<b);if(i<j)cube.push([i,j]);}
 for(let i=0;i<5;i++){p.push([i,(i+1)%5]);p.push([i,i+5]);p.push([i+5,5+(i+2)%5]);}
 return [['K4',4,k4],['K33',6,k33],['cube',8,cube],['Petersen',10,p]];
}
function solve(h,edges,c){
 const pivots=new Map();
 for(let v=0;v<h;v++){
  let bits=0n,rhs=c[v];
  edges.forEach(([a,b],j)=>{if(a===v||b===v)bits^=1n<<BigInt(j);});
  while(bits){const k=bits.toString(2).length-1;
   if(pivots.has(k)){let [mask,bit]=pivots.get(k);bits^=mask;rhs^=bit;}
   else {pivots.set(k,[bits,rhs]);break;}
  }
  if(bits===0n&&rhs===1)return false;
 }
 return true;
}
const results=[];
for(const [name,h,edges] of graphs()){
 check(2*edges.length===3*h,name+' degree sum');
 let yes=0;
 for(let mask=0;mask<(1<<h);mask++){
  const c=Array.from({length:h},(_,i)=>(mask>>i)&1);
  const y=[c.reduce((a,b)=>a^b,0),...c.slice(1)];
  const inverse=[y.reduce((a,b)=>a^b,0),...y.slice(1)];
  check(inverse.every((z,i)=>z===c[i]),name+' bijection');
  const label=solve(h,edges,c);
  check(label===(y[0]===0),name+' label');yes+=Number(label);
  for(let j=0;j<h;j++){
   const changed=c.slice();changed[j]^=1;
   check(solve(h,edges,changed)!==label,name+' raw sensitivity');
   const yp=y.slice();yp[j]^=1;
   const converted=[yp.reduce((a,b)=>a^b,0),...yp.slice(1)];
   check((solve(h,edges,converted)!==label)===(j===0),name+' transformed sensitivity');
  }
 }
 check(yes===1<<(h-1),name+' both labels');
 results.push({name,h,sat:yes,unsat:(1<<h)-yes,raw_query_depth:h,recoded_query_depth:1});
}
console.log(JSON.stringify({status:'PASS',checks,cases:results.length,results,scope:'promised charge-string queries only'},null,2));

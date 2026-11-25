"use strict";
function fused(){
 const T=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const b=i=>1<<i;
 const parity=x=>{let p=0;while(x){x&=x-1;p^=1}return p};
 function reduce(a,B){for(let i=6;i>=0;i--)if((a&b(i))&&B[i])a^=B[i];return a}
 let probes=0;
 function find(E,i=0,B=Array(7).fill(0),S=[]){if(i===E.length)return S;for(const [a,c] of E[i]){probes++;let v=reduce(a,B);if(!v)continue;let C=B.slice();C[31-Math.clz32(v)]=v;let s=find(E,i+1,C,[...S,[a,c]]);if(s)return s}return null}
 const events=(j=-1,p=0)=>T.map(([x,y,z],i)=>i===j?[[b(x),p],[b(y),p],[b(z),p]]:[[b(x)^b(y),0],[b(x)^b(z),0]]);
 let results=[];for(let j=-1;j<7;j++)for(let p=0;p<(j<0?1:2);p++){let E=events(j,p),S=find(E),words=[];for(let z=0;z<128;z++)if(E.every(e=>!e.every(([a,c])=>parity(a&z)===c)))words.push(z);let w=S===null?null:words.find(z=>S.every(([a,c])=>parity(a&z)!==c));if(j<0?(S!==null||words.length!==0):(S===null||words.length!==5||w===undefined))throw Error("fusion");results.push({relaxedTriple:j,remainingMonochrome:p,models:words.length,selectedRows:S,witness:w})}
 return {results,probes,method:"exhaustive finite basis-row certificate search, not polynomial discovery benchmark"};
}
console.log(JSON.stringify(fused(),null,2));

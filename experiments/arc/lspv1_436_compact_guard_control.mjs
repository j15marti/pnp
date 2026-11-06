#!/usr/bin/env node
'use strict';
// LSPV-1/436 independent bounded K4 odd-Tseitin source/projection/deletion control.
// Does not assert minimum proof length or native historical R_mix341 checker acceptance.
let checks=0;
function ck(b,why){checks++;if(!b)throw Error('CONTROL_FAIL: '+why);}
const edges=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)edges.push([i,j]);
const F=[];
for(let v=0;v<4;v++){
 const e=edges.map((pair,i)=>pair.includes(v)?i+1:null).filter(Boolean);
 ck(e.length===3,'cubic incidence');
 for(let x=0;x<8;x++){
  const b=[x&1,(x>>1)&1,(x>>2)&1],charge=v===0?1:0;
  if((b[0]^b[1]^b[2])!==charge)F.push(e.map((id,i)=>b[i]?-id:id));
 }
}
const n=edges.length,m=F.length,g=n+1,u=n+m+2,v=u+1;
const K=[];F.forEach(([a,b,c],i)=>K.push([g,a,n+2+i],[-(n+2+i),b,c]));
K.push([-g,u,v],[-g,u,-v],[-g,-u,v],[-g,-u,-v]);
const litTrue=(lit,w)=>{const bit=(w>>BigInt(Math.abs(lit)-1))&1n;return lit>0?bit===1n:bit===0n;};
const sat=(C,w)=>C.some(l=>litTrue(l,w));
const norm=C=>{const S=new Set(C);if([...S].some(x=>S.has(-x)))return null;return [...S].sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a)};
ck(K.length===2*m+4,'count');
for(const C of K)ck(C.length===3&&new Set(C.map(Math.abs)).size===3,'not strict width3');
const sigma={[g]:false,[u]:false,[v]:false};
F.forEach(([a],i)=>{sigma[n+2+i]=-a;});
const sub=C=>{let out=[];for(const l of C){const a=sigma[Math.abs(l)];if(typeof a==='boolean'){if((l>0)===a)return null;continue;}out.push(a===undefined?l:(l>0?a:-a));}return norm(out);};
const target=new Set(F.map(C=>JSON.stringify(norm(C))));
let projected=0;
for(const C of K){const D=sub(C);if(D!==null){projected++;ck(target.has(JSON.stringify(D)),'unmatched source');}}
ck(projected===m,'projection count');
for(let a=0;a<(1<<n);a++)ck(!F.every(C=>sat(C,BigInt(a))),'bad original UNSAT');
let witnesses=0;
for(let j=0;j<K.length;j++){
 let w=0n;
 if(j<2*m){
  const k=Math.floor(j/2);
  let a=-1;for(let x=0;x<(1<<n);x++)if(F.every((C,i)=>i===k||sat(C,BigInt(x)))){a=x;break;}
  ck(a>=0&&!sat(F[k],BigInt(a)),'no original deletion model');
  w=BigInt(a);
  F.forEach(([A],i)=>{const yi=i===k?(j%2):(sat([A],BigInt(a))?0:1);if(yi)w|=1n<<BigInt(n+i+1);});
 }else{
  w=1n<<BigInt(g-1);
  for(const l of K[j])if(Math.abs(l)!==g&&l<0)w|=1n<<BigInt(Math.abs(l)-1);
 }
 for(let i=0;i<K.length;i++)ck(sat(K[i],w)===(i!==j),'deletion witness '+j+' '+i);
 witnesses++;
}
console.log(JSON.stringify({status:'PASS',original_clauses:F.length,strict3_clauses:K.length,variables:n+m+3,projected_source_clauses:projected,indispensable_sources:witnesses,binary_antecedent_paid_work_floor:K.length-1,checks},null,2));

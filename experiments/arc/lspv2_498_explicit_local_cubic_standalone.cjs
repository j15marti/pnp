#!/usr/bin/env node
"use strict";
/* LSPV-2/498 published standalone finite checker.
 * Viola-Wigderson 2018 explicit degree-3 local bipartite Ramanujan graph,
 * field degree d=2 (n=4, H=30), original signed strict-3CNF.
 * RESTRICTED FINITE audit, not a native FLMV machine.
 */
const assert=require("node:assert/strict");
let checks=0;
function ck(v,m){assert.ok(v,m);checks++}
function eq(a,b,m){assert.deepEqual(a,b,m);checks++}
function mul4(a,b){
  let x=0; if(b&1)x^=a; if(b&2)x^=a<<1;
  if(x&8)x^=14; if(x&4)x^=7;
  return x;
}
function M(k,v){
  const a=v&3,b=v>>>2,L=2,x=2;
  if(k===1)return (a^mul4(L,b))|((mul4(mul4(L^1,x),a)^b)<<2);
  if(k===2)return (a^b)|((mul4(x,a)^b)<<2);
  if(k===3)return (a^mul4(L^1,b))|((mul4(mul4(L,x),a)^b)<<2);
  throw Error("invalid edge color");
}
function Minv(k,v){
  const w=M(k,v);return mul4(2,w&3)|(mul4(2,w>>>2)<<2);
}
const Q=15,H=30,W=6;
const out=Array.from({length:Q},(_,j)=>[M(1,j+1)-1,M(2,j+1)-1,M(3,j+1)-1]);
const rin=Array.from({length:Q},()=>[-1,-1,-1]);
for(let j=0;j<Q;j++)for(let k=1;k<=3;k++){
  const r=out[j][k-1];ck(r>=0&&r<Q,"valid neighbor");
  ck(rin[r][k-1]===-1,"one predecessor per edge color");
  rin[r][k-1]=j;eq(Minv(k,r+1),j+1,"explicit inverse");
}
for(let k=0;k<3;k++)eq(new Set(out.map(x=>x[k])).size,Q);
for(const row of out)eq(new Set(row).size,3);

function make(a,b){
  let s="11100011"+"1".repeat(H)+"0"+"1".repeat(2*H)+"0";
  let clauses=[];
  for(let v=0;v<H;v++){
    let ids;
    if(v<Q)ids=[2*v+1+a[v],H+2*v+1,H+2*v+2];
    else{
      const idx=rin[v-Q];
      ids=[2*idx[0]+1+b[idx[0]],H+2*idx[1]+1,H+2*idx[2]+2];
    }
    ids.sort((x,y)=>x-y);eq(new Set(ids).size,3);
    for(let z=0;z<8;z++){
      let parity=((z>>2)&1)^((z>>1)&1)^(z&1);
      if(parity===(v===0?1:0))continue;
      let clause=[];
      for(let k=0;k<3;k++){
        const sign=(z>>(2-k))&1;
        clause.push(sign?-ids[k]:ids[k]);
        s+=String(sign)+ids[k].toString(2).padStart(W,"0");
      }
      clauses.push(clause);
    }
  }
  s+="10";eq(s.length,2622);eq(clauses.length,120);
  return {s,clauses};
}
const HEAD=8+H+1+2*H+1;
function classify(s){
  if(s.length!==2622||s.slice(0,8)!=="11100011"||
      s.slice(8,8+H)!=="1".repeat(H)||
      s.slice(8+H,9+H)!=="0"||
      s.slice(9+H,9+H+2*H)!=="1".repeat(2*H)||
      s[9+H+2*H]!=="0"||s.slice(-2)!=="10")return "OUTSIDE";
  const a=Array(Q).fill(0),b=Array(Q).fill(0);
  for(let v=0;v<H;v++){
    let at=HEAD+v*4*3*(W+1)+1;
    let val=parseInt(s.slice(at,at+W),2);
    let j=v<Q?v:rin[v-Q][0];let bit=val-(2*j+1);
    if(bit!==0&&bit!==1)return "OUTSIDE";
    if(v<Q)a[j]=bit;else b[j]=bit;
  }
  if(make(a,b).s!==s)return "OUTSIDE";
  return a.some((v,j)=>v!==b[j])?"MEMBER_SAT":"MEMBER_UNSAT";
}
let sat=0,unsat=0;
for(let i=0;i<120;i++){
  const a=Array.from({length:Q},(_,j)=>(i+j*7+j*j)%2),b=a.slice();
  if(i%2){b[i%Q]^=1;sat++}else unsat++;
  eq(classify(make(a,b).s),i%2?"MEMBER_SAT":"MEMBER_UNSAT");
}
const pristine=make(Array(Q).fill(0),Array(Q).fill(0)).s;
eq(classify(pristine),"MEMBER_UNSAT");
for(let j=0;j<pristine.length;j++){
  let mutated=pristine.slice(0,j)+(pristine[j]==="1"?"0":"1")+pristine.slice(j+1);
  eq(classify(mutated),"OUTSIDE","one-bit mutation "+j);
}
eq(classify(pristine+"1"),"OUTSIDE");
console.log(JSON.stringify({status:"PASS",assertions:checks,seed:20261108,H,Q,edges:45,clauses:120,bits:2622,sat,unsat,mutantsRejected:2622,scope:"finite n=4 only"},null,2));

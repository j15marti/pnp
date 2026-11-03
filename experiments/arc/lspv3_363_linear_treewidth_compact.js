#!/usr/bin/env node
// LSPV-3 LINEAR-TREEWIDTH-SOURCE-FLOOR363. Independent, deterministic finite
// sources/proofs/controls. All-size expansion relies on Kim-Wormald/Friedman,
// not on finite graph samples. Run: node experiments/arc/lspv3_363_linear_treewidth_compact.js
'use strict';
const assert=require('assert');
const paths={
8:[3,6,1,8,2,5,7,4],
10:[5,10,4,2,8,6,1,9,3,7],
12:[1,12,3,7,5,11,4,8,6,9,2,10],
14:[6,2,12,4,9,14,1,11,7,5,8,13,3,10],
16:[9,1,7,4,8,13,3,11,10,2,16,5,15,6,14,12],
18:[11,14,6,13,2,5,18,16,10,7,17,3,9,1,8,15,4,12]
};
let assertions=0,sourceWitnesses=0,signFlips=0,derived=0,cutSubsets=0;
function ck(x,why){assertions++;assert.ok(x,why);}
function source(H,V){
 const n=H.length,C=[];
 for(const [j,P] of [H,V].entries()){
  const g=j===0?n+1:-(n+1);
  C.push([g,P[0]]);
  for(let i=0;i<n-1;i++)C.push([g,-P[i],P[i+1]]);
  C.push([g,-P[n-1]]);
 } return C;
}
function evaluate(C,a){return C.every(c=>c.some(l=>a[Math.abs(l)]===(l>0)));}
function witness(H,V,j){
 const n=H.length,P=j<n+1?H:V,side=Math.floor(j/(n+1)),q=j%(n+1);
 const a=Array(n+2).fill(false);a[n+1]=(side===1);
 for(let i=0;i<n;i++)a[P[i]]=(i<q);
 return a;
}
function resolvent(C,D,x){
 ck(C.includes(x)&&D.includes(-x),'authentic signed pivot');
 const out=[...new Set(C.filter(z=>z!==x).concat(D.filter(z=>z!==-x)))].sort((a,b)=>Math.abs(a)-Math.abs(b)||(b-a));
 ck(!out.some(z=>out.includes(-z)),'non-tautological resolvent');return out;
}
function certificate(C,H,V){
 const n=H.length,proof=C.map(c=>c.slice()),ends=[];
 function add(i,j,p){ck(i<proof.length&&j<proof.length,'past antecedents');const r=resolvent(proof[i],proof[j],p);proof.push(r);derived++;return proof.length-1;}
 for(const [side,P] of [H,V].entries()){
  let idx=side*(n+1);
  for(let i=0;i<n-1;i++)idx=add(idx,side*(n+1)+i+1,P[i]);
  idx=add(idx,side*(n+1)+n,P[n-1]);
  ends.push(idx);
 }
 const last=add(ends[0],ends[1],n+1);ck(proof[last].length===0,'empty clause');
 ck(proof.length-C.length===2*n+1,'exact source-floor proof');
}
function bits(x){let q=0;while(x){x&=x-1;q++;}return q;}
function expansion(H,V){
 const n=H.length,N=2**n,adj=Array(n).fill(0);
 for(const P of [H,V])for(let j=1;j<n;j++){let a=P[j-1]-1,b=P[j]-1;adj[a]|=2**b;adj[b]|=2**a;}
 let best=[1e8,1];
 for(let S=1;S<N;S++){
  let sz=bits(S);if(sz>n/2)continue;cutSubsets++;
  let boundary=0;for(let j=0;j<n;j++)if((S>>j)&1)boundary+=bits(adj[j] & (N-1-S));
  if(boundary*best[1]<best[0]*sz)best=[boundary,sz];
 } return best;
}
function digits(i){return String(i).length;}
function exactDimacsBits(n){
 const header="p cnf "+(n+1)+" "+(2*n+2)+"\n";
 const body=2*(n+1)*digits(n+1)+4*Array.from({length:n},(_,i)=>digits(i+1)).reduce((a,b)=>a+b,0)+13*n+7;
 return 8*(header.length+body);
}
function parse(s){
 const lines=s.split(/\r?\n/).map(x=>x.trim()).filter(Boolean);
 const h=(lines.shift()||'').split(/\s+/);
 if(h.length!==4||h[0]!=='p'||h[1]!=='cnf'||!h.slice(2).every(x=>/^\d+$/.test(x)))throw Error('header');
 const n=Number(h[2]),m=Number(h[3]);if(!Number.isSafeInteger(n)||!Number.isSafeInteger(m))throw Error('header range');
 let num=0,buf=[];
 for(const row of lines)for(const token of row.split(/\s+/)){
  if(!/^-?\d+$/.test(token))throw Error('token');
  let v=Number(token);if(!Number.isSafeInteger(v)||Math.abs(v)>n)throw Error('literal range');
  if(v===0){num++;buf=[];}else buf.push(v);
 }if(num!==m||buf.length)throw Error('count');
}
const expected={8:[5,4],10:[6,5],12:[6,6],14:[8,7],16:[6,7],18:[8,9]};
let cases=[];
for(const [s,V] of Object.entries(paths)){
 const n=+s,H=Array.from({length:n},(_,i)=>i+1),C=source(H,V);
 ck(C.length===2*n+2,'source clauses');
 certificate(C,H,V);
 for(let j=0;j<C.length;j++){
  const a=witness(H,V,j);
  ck(C.filter(c=>c.some(l=>a[Math.abs(l)]===(l>0))).length===C.length-1,'unique violation');
  ck(evaluate(C.filter((_,i)=>i!==j),a),'source deletion SAT');sourceWitnesses++;
  for(let i=0;i<C[j].length;i++){
   const D=C.map(c=>c.slice());D[j][i]=-D[j][i];ck(evaluate(D,a),'signed flip repair');signFlips++;
  }
 }
 const cut=expansion(H,V);ck(cut[0]*expected[n][1]===cut[1]*expected[n][0],'independent exact cut');
 const dimacs='p cnf '+(n+1)+' '+C.length+'\n'+C.map(c=>c.join(' ')+' 0\n').join('');
 ck(dimacs.length*8===exactDimacsBits(n),'exact encoding bits');
 cases.push({n,m:C.length,paid_nodes:2*n+1,encoded_bits:exactDimacsBits(n),cut});
}
let malformedRejected=0;
for(const s of ['p cnf -1 0','p cnf 3 1\n1 4 0\n','p cnf 1 1\n1\n','p cnf 1 1\n0\n0\n']){
 try{parse(s);}catch(e){malformedRejected++;}
}
ck(malformedRejected===4,'malformed inputs rejected');
let corruptedRejected=0;
try{resolvent([1,2],[-1,3],0);}catch(e){corruptedRejected++;}
ck(corruptedRejected===1,'corrupted pivot rejected');
console.log(JSON.stringify({schema:'LSPV3_EXPANDER_SNAKE363_COMPACT',assertions,sourceWitnesses,signFlips,derived,cutSubsets,malformedRejected,corruptedRejected,cases},null,2));

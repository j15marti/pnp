#!/usr/bin/env node
// LSPV-1/430: independently replayable affine branch intersection theorem.
// This uses only Node built-ins and does not implement the native R_mix341 checker.
'use strict';
const assert = require('node:assert/strict');
function parity(z){let b=0;while(z){b^=z&1;z>>=1}return b;}
function affine(P){if(!P.length)return false;const X=new Set(P.map(v=>v^P[0]));for(const a of X)for(const b of X)if(!X.has(a^b))return false;return true;}
function spaces(n){const res=[],m=1<<n;for(let mask=1;mask<2**m;mask++){const P=[];for(let j=0;j<m;j++)if((mask>>j)&1)P.push(j);if(affine(P))res.push(P);}return res;}
function constraints(P,n){const R=new Map();for(let v=0;v<(1<<n);v++){const q=parity(v&P[0]);if(P.every(y=>parity(v&y)===q))R.set(v,q);}return R;}
function combined(A,B){const out=new Set();for(const [v,d] of A)if(B.has(v))out.add([d^B.get(v),v,d].join(','));return out;}
function direct(P,Q,n){const out=new Set();for(let a=0;a<2;a++)for(let v=0;v<(1<<n);v++)for(let d=0;d<2;d++){if(P.every(y=>parity(v&y)===d)&&Q.every(y=>(a^parity(v&y))===d))out.add([a,v,d].join(','));}return out;}
function equal(A,B){return A.size===B.size&&[...A].every(x=>B.has(x));}
const record={},expected=[0,3,11,51,307];let assertions=0;
for(let n=1;n<=4;n++){const P=spaces(n),R=P.map(p=>constraints(p,n));assert.equal(P.length,expected[n]);assertions++;let checked=0;
 for(let i=0;i<P.length;i++)for(let j=0;j<P.length;j++){let v=combined(R[i],R[j]);assert.ok(v.size>0&&(v.size&(v.size-1))===0);assertions++;if(n<4||((i*P.length+j)%97===0)){assert.ok(equal(v,direct(P[i],P[j],n)));assertions++;checked++;}}
 record[n]={nonempty_affine_spaces:P.length,ordered_pairs:P.length**2,full_truth_pairs:checked};
}
function sat(C,a){return C.every(row=>row.some(l=>(((a>>(Math.abs(l)-1))&1)===(l>0?1:0))));}
function validCNF(C,n){return Array.from({length:2**n},(_,a)=>a).filter(a=>sat(C,a));}
const parityCNF=[];for(let a=0;a<8;a++)if(parity(a))parityCNF.push([0,1,2].map(i=>((a>>i)&1)?-(i+1):(i+1)));
const pm=validCNF(parityCNF,3);assert.deepEqual(pm,[0,3,5,6]);assertions++;
const p0=pm.filter(a=>!(a&1)).map(a=>a>>1),p1=pm.filter(a=>a&1).map(a=>a>>1);
assert.ok(equal(combined(constraints(p0,2),constraints(p1,2)),new Set(['0,0,0','1,3,0'])));assertions++;
const guard=[[1,-2,4],[1,-2,-4],[-1,-3,5],[-1,-3,-5]],gm=validCNF(guard,5);assert.equal(gm.length,16);assertions++;
const g0=[...new Set(gm.filter(a=>!(a&1)).map(a=>(a>>1)&3))],g1=[...new Set(gm.filter(a=>a&1).map(a=>(a>>1)&3))];
assert.equal(combined(constraints(g0,2),constraints(g1,2)).size,1);assertions++;
const E=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)E.push([i,j]);
function k4(odd){const C=[];for(let i=0;i<4;i++){const e=E.map((p,j)=>p.includes(i)?j+1:null).filter(Boolean);for(let a=0;a<8;a++)if(parity(a)!==+(odd&&i===0))C.push(e.map((id,k)=>((a>>k)&1)?-id:id));}return C;}
const odd=validCNF(k4(true),6),even=validCNF(k4(false),6);
assert.equal(odd.length,0);assert.equal(even.length,8);assertions+=2;
const e0=even.filter(a=>!(a&1)).map(a=>a>>1),e1=even.filter(a=>a&1).map(a=>a>>1);
assert.equal(combined(constraints(e0,5),constraints(e1,5)).size,8);assertions++;
let corrupt=parityCNF.map(c=>c.slice());corrupt[0]=[1,2,3];assert.notDeepEqual(validCNF(corrupt,3),pm);assertions++;
console.log(JSON.stringify({run:'LSPV-1-430',status:'PROVED/RESTRICTED semantic, COMPUTATIONAL',assertions,record,controls:{odd_K4_models:0,even_K4_models:8,parity_models:4,guard_models:16},native_Rmix341_accepted:false,B3_proved:false},null,2));

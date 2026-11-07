#!/usr/bin/env node
// LSPV-3/475 compact original-source quotient-identity firewall.
// This is NOT a historical R_mix341 checker or asymptotic proof.
'use strict';
const assert=require('node:assert/strict');
const graph=(name)=>{let h=name==='K4'?4:name==='K33'?6:8,edges=[];for(let a=0;a<h;a++)for(let b=a+1;b<h;b++)
if(name==='K4'||name==='K33'&&a<3&&b>=3||name==='cube'&&((a^b).toString(2).split('1').length-1)===1)edges.push([a,b]);return{h,edges};};
function source(name,odd){const {h,edges}=graph(name),clauses=[];for(let v=0;v<h;v++){const ids=edges.map(([a,b],i)=>a===v||b===v?i+1:0).filter(Boolean);
assert.equal(ids.length,3);for(let a=0;a<8;a++){const b=[a&1,(a>>1)&1,(a>>2)&1];if((b[0]^b[1]^b[2])===(odd&&v===0?1:0))continue;clauses.push(ids.map((id,j)=>b[j]?-id:id));}}
return {n:edges.length,clauses};}
function gate(C,n){const g=[],put=(op,...args)=>(g.push({op,args}),g.length-1);
const one=put('one'),xs=[null],bars=[null];for(let j=1;j<=n;j++)xs[j]=put('var',j);
for(let j=1;j<=n;j++)bars[j]=put('sub',one,xs[j]);
let out=null;for(const c of C){const f=c.map(l=>l>0?bars[l]:xs[-l]);const p=put('mul',f[0],f[1]),q=put('mul',p,f[2]);if(out===null)out=q;else{const a=put('add',out,q),b=put('mul',out,q);out=put('sub',a,b);}}return {g,out};}
function evalgate({g,out},bits,p){const v=[];for(const {op,args:a} of g){let z;if(op==='one')z=1;else if(op==='var')z=bits[a[0]-1];else if(op==='add')z=v[a[0]]+v[a[1]];else if(op==='sub')z=v[a[0]]-v[a[1]];else if(op==='mul')z=v[a[0]]*v[a[1]];else throw Error('unrecognized gate');v.push(((z%p)+p)%p);}return v[out];}
function validate(C,n){return Number.isInteger(n)&&n>=3&&Array.isArray(C)&&C.every(c=>Array.isArray(c)&&c.length===3&&c.every(l=>Number.isInteger(l)&&l!==0&&Math.abs(l)<=n)&&new Set(c.map(l=>Math.abs(l))).size===3);}
function sat(C,b){return C.every(c=>c.some(l=>b[Math.abs(l)-1]===(l>0?1:0)));}
const cases=[];for(const name of ['K4','K33','cube'])for(const odd of [false,true])cases.push({name:name+(odd?'_odd':'_even'),...source(name,odd)});
let all=[];for(let a=0;a<8;a++)all.push([1,2,3].map((x,i)=>(a>>i)&1?-x:x));
cases.push({name:'all8_unsat',n:3,clauses:all},{name:'single_sat',n:3,clauses:[[1,2,3]]});
let assignments=0,fields=0,corruptions=0;
for(const item of cases){const {n,clauses}=item;assert(validate(clauses,n));const circuit=gate(clauses,n);let count=0;
for(let mask=0;mask<2**n;mask++){const b=Array.from({length:n},(_,j)=>(mask>>j)&1),truth=sat(clauses,b);if(truth)count++;
for(const p of [2,3,5,101]){assert.equal(evalgate(circuit,b,p),truth?0:1);fields++;}
assignments++;}
const expected=item.name==='K4_even'?8:item.name==='K33_even'?16:item.name==='cube_even'?32:item.name==='single_sat'?7:0;assert.equal(count,expected);
const at2=evalgate(circuit,Array(n).fill(2),101);assert.notEqual(at2,1);
const clone=JSON.parse(JSON.stringify(circuit));clone.g[clone.out].op='add';assert.notDeepEqual(clone,circuit);corruptions++;
item.count=count;item.gates=circuit.g.length;item.at2_mod101=at2;
}
for(const [n,c] of [[3,[[1,2]]],[3,[[1,1,2]]],[3,[[0,1,2]]],[3,[[1,2,4]]],[-1,[[1,2,3]]]])assert(!validate(c,n));
console.log(JSON.stringify({label:'PROVED/RESTRICTED theorem, COMPUTATIONAL fixtures; P vs NP OPEN',assignments,fields,corruptions,cases:cases.map(({name,n,clauses,count,gates,at2_mod101})=>({name,n,m:clauses.length,count,gates,at2_mod101}))},null,2));

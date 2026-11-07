#!/usr/bin/env node
'use strict';
// LSPV-3/467: exact original-source odd cubic-Tseitin affine auxiliary split
// Declared semantic AND3/GF(2) interface ONLY, NOT historical byte acceptance.
const assert=require('assert'),crypto=require('crypto');
const pc=n=>{let t=0;while(n){t+=n&1;n>>>=1;}return t;};
const X=(u,v)=>({m:u.m^v.m,b:u.b^v.b});
const eq=(u,v)=>assert.deepStrictEqual(u,v);
const good=(clauses,a)=>clauses.every(C=>C.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0)));
function edgesFor(key){
 let E=[];
 if(key==='K4'){for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)E.push([u,v]);}
 else if(key==='K33'){for(let u=0;u<3;u++)for(let v=3;v<6;v++)E.push([u,v]);}
 else if(key==='Cube'){for(let u=0;u<8;u++)for(let v=u+1;v<8;v++)if(pc(u^v)===1)E.push([u,v]);}
 else throw Error('unlisted family');
 return E;
}
function run(key,h){
 const E=edgesFor(key),n=E.length,clauses=[],even=[],ids=[],rows=[];
 for(let v=0;v<h;v++){
  const inc=E.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
  assert.strictEqual(inc.length,3);
  const mask=inc.reduce((a,i)=>a|(1<<i),0);
  const charge=v===0?1:0;rows.push({m:mask,b:charge});
  let block=[];
  for(let t=0;t<8;t++){
   const bits=[(t>>2)&1,(t>>1)&1,t&1];
   const C=inc.map((i,j)=>bits[j]?-(i+1):i+1);
   if(pc(t)%2!==charge){block.push(clauses.length);clauses.push(C);}
   if(pc(t)%2!==0)even.push(C);
  }
  assert.strictEqual(block.length,4);ids.push(block);
  for(let t=0;t<8;t++){
   const b=[(t>>2)&1,(t>>1)&1,t&1];
   const local=block.every(i=>clauses[i].some(l=>b[inc.indexOf(Math.abs(l)-1)]===(l>0?1:0)));
   assert.strictEqual(local,pc(t)%2===charge);
  }
 }
 assert.strictEqual(clauses.length,4*h);
 assert.strictEqual(Array.from({length:1<<n},(_,a)=>a).filter(a=>good(clauses,a)).length,0);
 assert.strictEqual(Array.from({length:1<<n},(_,a)=>a).filter(a=>good(even,a)).length,1<<(n-h+1));
 for(let i=0;i<clauses.length;i++)
   assert.ok(Array.from({length:1<<n},(_,a)=>a).some(a=>good(clauses.filter((_,j)=>j!==i),a)));
 const edge0=E.map((e,i)=>e.includes(0)?i:-1).filter(i=>i>=0),[a,b,c]=edge0;
 const q=(1<<a)|(1<<b)|(1<<c), z1=n, z2=n+1;
 const d1={m:(1<<a)|(1<<b)|(1<<z1),b:0};
 const d2={m:(1<<z1)|(1<<c)|(1<<z2),b:0};
 let p=X(X(rows[0],d1),d2);eq(p,{m:1<<z2,b:1});
 eq(X(p,{m:1<<z2,b:0}),{m:0,b:1});
 let L=rows.slice(1),additions=0;
 while(L.length>1){let N=[];for(let i=0;i<L.length;i+=2)
  if(i+1<L.length){N.push(X(L[i],L[i+1]));additions++;} else N.push(L[i]);L=N;}
 assert.strictEqual(additions,h-2);eq(L[0],{m:q,b:0});
 let t=X(X(L[0],d1),d2);eq(t,{m:1<<z2,b:0});
 eq(X(t,{m:1<<z2,b:1}),{m:0,b:1});
 const project=r=>{
  let m=r.m;
  if(m&(1<<z2))m^=(1<<z2)|q;
  if(m&(1<<z1))m^=(1<<z1)|(1<<a)|(1<<b);
  return {m,b:r.b};
 };
 eq(project(d1),{m:0,b:0});eq(project(d2),{m:0,b:0});
 eq(project(p),rows[0]);eq(project(t),{m:q,b:0});
 eq(X(project(p),project(t)),{m:0,b:1});
 eq(project({m:1<<z2,b:0}),{m:q,b:0});
 eq(project({m:1<<z2,b:1}),{m:q,b:1});
 const src='p cnf '+n+' '+clauses.length+'\n'+clauses.map(C=>C.join(' ')+' 0\n').join('');
 return {graph:key,vertices:h,original_variables:n,source_clauses:clauses.length,
  original_sha256:crypto.createHash('sha256').update(src).digest('hex'),
  original_bytes:Buffer.byteLength(src),even_models:1<<(n-h+1),
  original_source_AND3:3*h,augmented_paid_defs:2,
  augmented_binary_XOR:h+4,augmented_total:4*h+6,
  projected_binary_XOR:h-1,projected_total:4*h-1};
}
const out=[run('K4',4),run('K33',6),run('Cube',8)];
assert.deepStrictEqual(out.map(f=>f.projected_total),[15,23,31]);
console.log(JSON.stringify({model:'declared semantic AND3/GF2 only',status:'PASS',fixtures:out},null,2));

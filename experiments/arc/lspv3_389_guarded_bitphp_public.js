'use strict';
// LSPV-3/389 compact replay: n=2,4 original bit-PHP, guarded source, strict RES.
// Finite controls only: not the growing-size Cook compiler or Braun lower bound.
const assert=require('assert');
const norm=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const id=c=>norm(c).join(',');
function original(n){
 const ell=Math.log2(n),source=[],tags=[];
 assert(Number.isInteger(ell)&&n>1);
 for(let i=0;i<=n;i++)for(let j=i+1;j<=n;j++)for(let hole=0;hole<n;hole++){
  const c=[];
  for(let p of [i,j])for(let b=0;b<ell;b++)
   c.push((hole>>b)&1?-(p*ell+b+1):p*ell+b+1);
  source.push(norm(c));tags.push([i,j,hole]);
 }
 return {ell,source,tags};
}
function solve(src,nv){
 const nodes=src.map((c,i)=>({c,src:i})),lookup=new Map(src.map((c,i)=>[id(c),i]));
 let active=new Set(src.map((_,i)=>i));
 for(let x=1;x<=nv&&!lookup.has('');x++){
  const P=[...active].filter(i=>nodes[i].c.includes(x));
  const Q=[...active].filter(i=>nodes[i].c.includes(-x));const created=[];
  for(const i of P){for(const j of Q){
   const c=norm([...nodes[i].c.filter(v=>v!==x),...nodes[j].c.filter(v=>v!==-x)]);
   if(c.some(v=>c.includes(-v)))continue;
   const k=id(c);if(!lookup.has(k)){lookup.set(k,nodes.length);nodes.push({c,left:i,right:j,pivot:x});}
   created.push(lookup.get(k));if(lookup.has(''))break;
  }if(lookup.has(''))break;}
  active=new Set([...active].filter(i=>!P.includes(i)&&!Q.includes(i)).concat(created));
 }
 assert(lookup.has(''));
 const used=new Set();
 function visit(i){if(used.has(i))return;used.add(i);const v=nodes[i];if(v.src===undefined){visit(v.left);visit(v.right);}}
 visit(lookup.get(''));const indices=[...used].sort((a,b)=>a-b),ren=new Map(indices.map((x,i)=>[x,i]));
 return indices.map(i=>{const v={...nodes[i]};if(v.src===undefined){v.left=ren.get(v.left);v.right=ren.get(v.right);}return v;});
}
function verify(nodes,src){
 let count=0;
 nodes.forEach((v,i)=>{
  assert.deepStrictEqual(v.c,norm(v.c));assert(!v.c.some(x=>v.c.includes(-x)));
  if(v.src!==undefined){assert.deepStrictEqual(v.c,src[v.src]);return;}
  assert(v.left<i&&v.right<i&&v.left!==v.right);
  const p=v.pivot,A=nodes[v.left].c,B=nodes[v.right].c;
  assert(A.includes(p)&&B.includes(-p));
  assert.deepStrictEqual(v.c,norm([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]));count++;
 });assert.deepStrictEqual(nodes.at(-1).c,[]);
 return count;
}
function run(n){
 const {ell,source,tags}=original(n),t=(n+1)*ell+1;
 const gsrc=source.map(c=>norm([-t,...c])),hsrc=[...gsrc,[t]],base=solve(source,t-1);
 verify(base,source);
 let signControls=0;
 source.forEach((c,k)=>{
  const [a,b,h]=tags[k],assignment=new Array(t+1).fill(false);assignment[t]=true;
  const map={};map[a]=h;map[b]=h;const rem=[...Array(n).keys()].filter(x=>x!==h);let idx=0;
  for(let p=0;p<=n;p++)if(p!==a&&p!==b)map[p]=rem[idx++];
  for(let p=0;p<=n;p++)for(let bit=0;bit<ell;bit++)
   assignment[p*ell+bit+1]=!!(map[p]&(1<<bit));
  const val=d=>d.some(v=>v>0?assignment[v]:!assignment[-v]);
  assert(!val(c));
  source.forEach((d,j)=>assert.strictEqual(val(d),j!==k));
  for(const literal of c){assert(val(norm(c.map(x=>x===literal?-x:x))));signControls++;}
  assert(val(norm([t,...c])));signControls++;
 });
 const lifted=base.map(v=>v.src!==undefined?{src:v.src,c:gsrc[v.src]}:{c:norm([-t,...v.c]),left:v.left,right:v.right,pivot:v.pivot});
 assert.deepStrictEqual(lifted.at(-1).c,[-t]);
 const H=[...lifted,{src:source.length,c:[t]},{c:[],left:lifted.length,right:lifted.length-1,pivot:t}];
 const paid=verify(H,hsrc);
 assert.strictEqual(H.filter(x=>x.src!==undefined).length,source.length+1);
 return {n,source_clauses:source.length,guarded_clauses:hsrc.length,paid_resolution_nodes:paid,sign_flip_controls:signControls+1,proof_records:H.length};
}
const cases=[run(2),run(4)];
assert.strictEqual(cases[0].paid_resolution_nodes,6);
assert.strictEqual(cases[1].paid_resolution_nodes,160);
console.log(JSON.stringify({schema:'LSPV3-389-public/v1',status:'COMPUTATIONAL, finite only',cases},null,2));

#!/usr/bin/env node
/* LSPV-3 361 compact independently runnable source-authenticated DP/RES replay.
   Complete Python-producer / independent-Node certificate corpus is in run ZIP. */
'use strict';
const assert=require('assert');
const canon=a=>{const s=new Set(a);for(const v of s)if(!Number.isInteger(v)||v===0||s.has(-v))throw Error('bad clause');return [...s].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)};
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function parity(ids,rhs){const out=[];for(let b=0;b<(1<<ids.length);b++){let p=0;for(let i=0;i<ids.length;i++)p^=(b>>i)&1;if(p!==rhs)out.push(canon(ids.map((v,i)=>((b>>i)&1)?-v:v)))}return out}
function tseitin(odd){const ed=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)ed.push([a,b]);let cls=[];for(let a=0;a<4;a++)cls.push(...parity(ed.flatMap((e,i)=>e.includes(a)?[i+1]:[]),Number(odd&&a===0)));return [6,cls]}
function php(p,h){const f=(i,j)=>1+i*h+j,cls=[];for(let i=0;i<p;i++)cls.push(Array.from({length:h},(_,j)=>f(i,j)));for(let j=0;j<h;j++)for(let a=0;a<p;a++)for(let b=a+1;b<p;b++)cls.push([-f(a,j),-f(b,j)]);return [p*h,cls]}
function width(n,clauses){const adj=Array.from({length:n+1},()=>new Set());for(const c of clauses){for(const u of c)for(const v of c)if(Math.abs(u)!==Math.abs(v))adj[Math.abs(u)].add(Math.abs(v))}const widths=[];for(let x=1;x<=n;x++){let nei=[...adj[x]].filter(y=>y>x);widths.push(nei.length);for(const a of nei)for(const b of nei)if(a!==b)adj[a].add(b)}return widths}
function brute(n,clauses){for(let mask=0;mask<(1<<n);mask++)if(clauses.every(c=>c.some(x=>(((mask>>(Math.abs(x)-1))&1)===Number(x>0)))))return mask;return null}
function evaluate(name,n,raw){
 const clauses=[...new Map(raw.map(c=>{const x=canon(c);return [JSON.stringify(x),x]})).values()];
 const ws=width(n,clauses),bound=ws.reduce((s,w)=>s+3**w,0),active=new Map(clauses.map((c,i)=>[JSON.stringify(c),{id:'S'+i,c}]));
 const nodes=new Map(),allSteps=[];let pairs=0,taut=0,dupes=0;
 for(let x=1;x<=n;x++){
  const pos=[...active.values()].filter(o=>o.c.includes(x)),neg=[...active.values()].filter(o=>o.c.includes(-x));
  const next=new Map([...active].filter(([,o])=>!o.c.includes(x)&&!o.c.includes(-x)));
  for(const a of pos)for(const b of neg){pairs++;const cs=a.c.filter(z=>z!==x).concat(b.c.filter(z=>z!==-x));let c;try{c=canon(cs)}catch(e){taut++;continue}const key=JSON.stringify(c);if(next.has(key)){dupes++;continue}let id='R'+allSteps.length;
   const node={id,a:a.id,b:b.id,pivot:x,c};nodes.set(id,node);allSteps.push(node);next.set(key,{id,c});
  }active.clear();for(const [k,v] of next)active.set(k,v);if(active.has('[]'))break;
 }
 const witness=brute(n,clauses),contradiction=active.get('[]');assert.equal(Boolean(contradiction),witness===null);
 let needs=new Set(),queue=contradiction?[contradiction.id]:[];
 while(queue.length){const id=queue.pop();if(id.startsWith('S')||needs.has(id))continue;needs.add(id);const v=nodes.get(id);assert(v);queue.push(v.a,v.b)}
 let ent=new Map(clauses.map((c,i)=>['S'+i,c]));
 for(const s of allSteps){if(!needs.has(s.id))continue;let a=ent.get(s.a),b=ent.get(s.b);
 assert(a&&b&&a.includes(s.pivot)&&b.includes(-s.pivot));const c=canon(a.filter(z=>z!==s.pivot).concat(b.filter(z=>z!==-s.pivot)));
 assert(same(c,s.c));ent.set(s.id,c);
 }assert(needs.size<=bound);if(contradiction)assert(same(ent.get(contradiction.id),[]));
 return {name,n,m:clauses.length,unsat:witness===null,w:Math.max(...ws),bound,proof_nodes:needs.size,pairs,taut,dupes};
}
const fixtures=[
 ['unit_conflict',1,[[1],[-1]]],
 ['square_2sat',2,[[1,2],[-1,2],[1,-2],[-1,-2]]],
 ['horn_chain',3,[[1],[-1,2],[-2,3],[-3]]],
 ['renamed_horn_chain',3,[[-1],[1,2],[-2,-3],[3]]],
 ['opposed_xor3',3,[...parity([1,2,3],0),...parity([1,2,3],1)]],
 ['single_xor3_sat',3,parity([1,2,3],0)],
 ['tseitin_k4_odd',...tseitin(true)],
 ['tseitin_k4_even',...tseitin(false)],
 ['php_3_into_2',...php(3,2)],
 ['php_4_into_3',...php(4,3)],
 ['padded_unsat',7,[[1],[-1],[3,4],[-4,5],[6,-7]]]
];
const rows=fixtures.map(x=>evaluate(...x));
assert.equal(rows.length,11);
assert(rows.every(r=>r.proof_nodes<=r.bound));
const total=rows.reduce((s,r)=>s+r.proof_nodes,0);assert.equal(total,102);
let rejected=0;for(const c of [[1,-1],[0],[1.5]])try{canon(c)}catch(e){rejected++}assert.equal(rejected,3);
console.log(JSON.stringify({status:'PASS',fixtures:rows.length,proof_nodes:total,malformed_clauses_rejected:rejected,rows},null,2));

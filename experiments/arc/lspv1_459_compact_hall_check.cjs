/* LSPV-1/459: standalone, no-package source-authenticated pure-Resolution Hall-kernel control. */
'use strict';
const assert=require('assert');
const holes=[[0,1,2],[0,1,3],[0,2,3],[1,2,3],[0,1,2]];
const norm=a=>{const s=new Set(a);if([...s].some(x=>s.has(-x)))return null;return [...s].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y)};
const key=a=>JSON.stringify(a);
let edge=new Map(),n=0,src=[];
for(let i=0;i<5;i++)for(const h of holes[i])edge.set(`${i}:${h}`,++n);
for(let i=0;i<5;i++)src.push(norm(holes[i].map(h=>edge.get(`${i}:${h}`))));
for(let h=0;h<4;h++){
 let members=holes.map((v,i)=>v.includes(h)?i:-1).filter(i=>i>=0);
 for(let a=0;a<members.length;a++)for(let b=a+1;b<members.length;b++){
  let p=-edge.get(`${members[a]}:${h}`),q=-edge.get(`${members[b]}:${h}`),z=++n;
  src.push(norm([p,q,z]),norm([p,q,-z]));
 }
}
assert.strictEqual(src.length,47);assert.strictEqual(n,36);
const db=new Map(src.map((c,i)=>[i+1,c]));let next=48,steps=[];
const resolution=(a,b,p,stage)=>{
 assert(db.get(a).includes(p)&&db.get(b).includes(-p));
 let c=norm([...db.get(a).filter(x=>x!==p),...db.get(b).filter(x=>x!==-p)]);
 assert(c!==null);
 let id=next++;db.set(id,c);steps.push({id,a,b,p,stage});return id;
};
let active=new Map(src.slice(0,5).map((c,i)=>[key(c),i+1]));
for(let j=5;j<src.length;j+=2){
 const p=src[j].find(x=>!src[j+1].includes(x));assert(p!==undefined);
 let id=resolution(j+1,j+2,p,'pad');active.set(key(db.get(id)),id);
}
let edges=[...edge.values()];
for(let p of edges){
 const entries=[...active.values()],pos=entries.filter(i=>db.get(i).includes(p)),neg=entries.filter(i=>db.get(i).includes(-p));
 let nxt=new Map(entries.filter(i=>!db.get(i).some(x=>Math.abs(x)===p)).map(i=>[key(db.get(i)),i]));
 for(let a of pos)for(let b of neg){
  const c=norm([...db.get(a).filter(x=>x!==p),...db.get(b).filter(x=>x!==-p)]);
  if(c===null||nxt.has(key(c)))continue;
  const id=resolution(a,b,p,'dp');nxt.set(key(c),id);
 }
 active=nxt;if(active.has('[]'))break;
}
const goal=active.get('[]');assert(goal);
const byId=new Map(steps.map(s=>[s.id,s]));let needed=new Set([goal]),stack=[goal];
while(stack.length){const s=byId.get(stack.pop());if(!s)continue;for(let x of [s.a,s.b])if(!needed.has(x)){needed.add(x);stack.push(x)}}
let proof=steps.filter(s=>needed.has(s.id)),deps=new Map([...Array(src.length)].map((_,i)=>[i+1,0]));
for(let s of proof){assert(deps.has(s.a)&&deps.has(s.b));deps.set(s.id,1+Math.max(deps.get(s.a),deps.get(s.b)))}
assert.strictEqual(proof.length,92);assert.strictEqual(proof.filter(s=>s.stage==='pad').length,21);
assert.strictEqual(deps.get(goal),12);
let allSources=new Set([...needed].filter(id=>id<=47));assert.strictEqual(allSources.size,47);
console.log(JSON.stringify({sourceClauses:47,variables:n,work:proof.length,padNodes:21,dpNodes:71,span:12,sourceAncestors:47,pass:true}));

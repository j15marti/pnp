#!/usr/bin/env node
// LSPV-3/446 independent FACET-A to FACET-4 proof-DAG replay. NOT historical R_mix341.
import fs from 'node:fs';
import crypto from 'node:crypto';
const path=process.argv[2]||'results/raw/review/2026-11-05_2253_LSPV5_FULL_COOK_FACETA379.json';
const F=JSON.parse(fs.readFileSync(path,'utf8'));
const norm=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
const eq=(a,b)=>a.length===b.length&&a.every((x,i)=>x===b[i]);
const res=(l,r,p)=>{if(!l.includes(p)||!r.includes(-p))throw Error('bad oriented pivot');const c=norm([...l.filter(x=>x!==p),...r.filter(x=>x!==-p)]);if(c.some(x=>c.includes(-x)))throw Error('tautology');return c};
function replay(t){
 const lines=t.dimacs.trimEnd().split(/\r?\n/),h=lines.shift().match(/^p cnf (\d+) (\d+)$/);
 if(!h||Number(h[2])!==t.trace.sources.length)throw Error('bad source header');
 if(crypto.createHash('sha256').update(t.dimacs).digest('hex')!==t.source_sha256||Buffer.byteLength(t.dimacs)!==t.source_bytes)throw Error('source SHA/bytes');
 const M=new Map(),owners=new Map(),v=Number(h[1]);
 const get=k=>{let x=M.get(k);if(!x)throw Error('unknown ancestor '+k);return x};
 for(let i=0;i<t.trace.sources.length;i++){
  const x=t.trace.sources[i],l=lines[i].trim().split(/\s+/).map(Number);
  if(x.id!=='S'+(i+1)||l.at(-1)!==0||!eq(norm(l.slice(0,-1)),norm(x.clause)))throw Error('source clause mismatch');
  M.set(x.id,{c:norm(x.clause),p:[],d:0});
 }
 let D=0,R=0;
 for(const x of t.trace.nodes){
  if(M.has(x.id))throw Error('duplicate id');
  if(x.kind==='def'){
   const {a,b,out:z}=x;
   if(!Number.isSafeInteger(z)||z<=v||owners.has(z)||Math.abs(a)===Math.abs(b)||Math.max(Math.abs(a),Math.abs(b))>=z||[a,b].some(k=>!k||(Math.abs(k)>v&&!owners.has(Math.abs(k)))))throw Error('illegal fresh gate');
   let ps=[...new Set([a,b].map(k=>owners.get(Math.abs(k))).filter(Boolean))],d=1+Math.max(0,...ps.map(k=>get(k).d));
   M.set(x.id,{c:null,p:ps,d});owners.set(z,x.id);
   const f=[[a,b,-z],[a,-b,-z],[-a,b,-z],[-a,-b,z]].map(norm);
   for(let j=0;j<4;j++)M.set(x.id+'#T'+j,{c:f[j],p:[x.id],d});
   const A=res(f[0],f[1],b),B=res(f[0],f[2],a);
   if(!eq(A,norm([-z,a]))||!eq(B,norm([-z,b])))throw Error('facet reconstruction');
   for(let j=0;j<2;j++)M.set('N_'+x.id+'_'+j,{c:j?B:A,p:[x.id+'#T0',x.id+'#T'+(j+1)],d:d+1});
   for(let j=0;j<3;j++)M.set(x.id+'#f'+j,{c:j===0?A:j===1?B:f[3],p:[j===2?x.id+'#T3':'N_'+x.id+'_'+j],d:d+(j===2?0:1)});
   D++;
  }else if(x.kind==='res'){
   let l=get(x.left),r=get(x.right);
   M.set(x.id,{c:res(l.c,r.c,x.pivot),p:[x.left,x.right],d:1+Math.max(l.d,r.d)});R++;
  }else throw Error('unhandled rule');
 }
 let goal=t.trace.nodes.at(-1).id;if(!eq(get(goal).c,[]))throw Error('not empty');
 const seen=new Set(),todo=[goal];while(todo.length){let k=todo.pop();if(seen.has(k))continue;seen.add(k);todo.push(...get(k).p)}
 const old=t.trace.nodes.filter(x=>seen.has(x.id)).length,
  additional=[...seen].filter(x=>x.startsWith('N_')).length,
  sources=t.trace.sources.filter(x=>seen.has(x.id)).length;
 if(old!==D+R||additional>2*D||sources!==t.trace.sources.length)throw Error('ancestry failure');
 return {ell:t.ell,sources,D,R,emitted_paid:3*D+R,goal_union_paid:old+additional,extra_normalizations_used:additional,span:get(goal).d,source_sha256:t.source_sha256};
}
console.log(JSON.stringify({scope:'PROVED RESTRICTED FACET4 ONLY, historical grammar OPEN',path,traces:F.traces.map(replay)},null,2));

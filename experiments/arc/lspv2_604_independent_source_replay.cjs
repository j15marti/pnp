#!/usr/bin/env node
'use strict';
/* Separate source-bound strict RES auditor. NOT the historical or /386 original checker.
 * Usage: node lspv2_604_independent_source_replay.cjs PACKET.json SOURCE.cnf
 */
const fs=require('node:fs'),crypto=require('node:crypto');
let tests=0;const test=(p,m)=>{tests++;if(!p)throw Error('INDEPENDENT: '+m)};
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const canon=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const buf=fs.readFileSync(process.argv[2]), d=JSON.parse(buf);
const raw=fs.readFileSync(process.argv[3]);
const ll=raw.toString('ascii').split(/\r?\n/).filter(Boolean),head=ll.shift().trim().split(/\s+/);
test(head.length===4&&head[0]==='p'&&head[1]==='cnf','CNF header');
const n=+head[2],m=+head[3];test(Number.isInteger(n)&&n>=1&&Number.isInteger(m)&&m===ll.length,'CNF size');
const clauses=ll.map((s,i)=>{const a=s.trim().split(/\s+/).map(Number);test(a.pop()===0,'CNF 0 '+i);test(a.every(x=>Number.isSafeInteger(x)&&x!==0&&Math.abs(x)<=n),'CNF literal '+i);test(eq(a,canon(a))&&!a.some(x=>a.includes(-x)),'CNF canonical '+i);return a});
const {h,edges,charge,guard}=d.spec;test(guard===n,'guard/header');test(charge.length===h&&edges.length*2===3*h,'source spec');
test(charge.every(z=>z===0||z===1)&&charge.reduce((a,b)=>a^b,0)===1,'odd charge');
const inc=Array.from({length:h},()=>[]);const eset=new Set();
for(let i=0;i<edges.length;i++) {let [u,v]=edges[i];test(Number.isInteger(u)&&Number.isInteger(v)&&u>=0&&u<v&&v<h,'edge endpoints');test(!eset.has(`${u}:${v}`),'duplicate edge');eset.add(`${u}:${v}`);inc[u].push(i+1);inc[v].push(i+1)}
test(inc.every(v=>v.length===3),'degree');
let expected=[];for(let v=0;v<h;v++){
 for(let a=0;a<8;a++) {let bits=[a&1,(a>>1)&1,(a>>2)&1];if(bits.reduce((x,y)=>x+y,0)%2===charge[v])continue;
  expected.push({source:v,c:canon(inc[v].map((e,j)=>bits[j]?-e:e).concat([-guard]))});
 }}
expected.push({source:-1,c:[guard]});test(expected.length===4*h+1,'expected source count');
for(let i=0;i<expected.length;i++)test(eq(expected[i].c,clauses[i]),'byte-external signed original clause '+i);
const R=d.records;test(Array.isArray(R)&&R.length>=clauses.length,'records');test(Array.isArray(d.gate_defs)&&d.gate_defs.length===1,'one unused paid-owner sentinel (CLI-specific)');
const gd=d.gate_defs[0];test(eq(gd,[0,guard+1,1,2]),'sentinel owner');
let nres=0;
for(let i=0;i<R.length;i++){
 let r=R[i];test(Array.isArray(r.c)&&eq(r.c,canon(r.c))&&!r.c.some(x=>r.c.includes(-x)),'clause canonical '+i);
 if(i<clauses.length){test(r.kind==='SOURCE'&&eq(r.parents,[])&&r.source===expected[i].source&&eq(r.c,clauses[i]),'source provenance '+i)}
 else {test(r.kind==='RES','not strict RES '+i);const [a,b]=r.parents;test(Number.isInteger(a)&&Number.isInteger(b)&&a<i&&b<i&&a>=0&&b>=0,'forward parent '+i);
 let A=R[a].c,B=R[b].c,p=r.pivot;test(Number.isInteger(p)&&p!==0&&A.includes(p)&&B.includes(-p),'signed pivot '+i);
 let c=canon(A.filter(x=>x!==p).concat(B.filter(x=>x!==-p)));test(!c.some(x=>c.includes(-x))&&eq(c,r.c),'exact resolvent '+i);nres++}
}
test(eq(R.at(-1).c,[]),'not terminal UNSAT');test(d.summary.source===clauses.length&&d.summary.resolution===nres,'counts');
test(d.summary.paid_gates===1&&d.summary.paid_total===nres+1&&d.summary.def_views===0&&d.summary.live_records===R.length,'global paid count once');
let seen=new Set();function mark(i){if(seen.has(i))return;seen.add(i);for(const p of R[i].parents)mark(p)}mark(R.length-1);
let reachableSRC=[...seen].filter(j=>j<clauses.length).length;
const result={status:'ACCEPT_SEPARATE_REFERENCE_ONLY',source_sha256:sha(raw),packet_sha256:sha(buf),source_clauses:clauses.length,source_vars:n,
 source_ancestry:reachableSRC,resolution:nres,paid_total:nres+1,original_paid_owners:1,records:R.length,assertions:tests};
process.stdout.write(JSON.stringify(result)+'\n');

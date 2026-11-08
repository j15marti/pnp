#!/usr/bin/env node
"use strict";
import fs from "node:fs";
import path from "node:path";
import {spawnSync} from "node:child_process";
import os from "node:os";
import crypto from "node:crypto";

const root=process.cwd();
const packetPath=path.join(root,"replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json");
const checker=path.join(root,"replay/413/lspv2_341_independent_verify.js");
const rawPath=path.join(root,"results/raw/review/2026-11-07_1648_LSPV5_REACHABILITY_DISCHARGE420.json");
const packet=JSON.parse(fs.readFileSync(packetPath,"utf8"));
let checks=0;
const assert=(b,m)=>{checks++;if(!b)throw new Error(m)};
const norm=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const resolve=(a,b,p)=>{
  assert(a.includes(p)&&b.includes(-p),`bad pivot ${p}`);
  const c=norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
  assert(!c.some(x=>c.includes(-x)),"tautological resolvent");
  return c;
};
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const run=obj=>{
  const tmp=path.join(os.tmpdir(),`lspv5-420-${process.pid}-${crypto.randomUUID()}.json`);
  fs.writeFileSync(tmp,JSON.stringify(obj));
  try {const cp=spawnSync(process.execPath,[checker,tmp],{encoding:"utf8"});return cp.status===0}
  finally {fs.unlinkSync(tmp)}
};

for(const f of packet.fixtures){
  const by=new Map(f.proof.map(x=>[x.id,x])), used=new Set();
  function visit(id){if(used.has(id))return;used.add(id);const p=by.get(id);if(p)for(const q of p.parents)visit(q)}
  visit(f.proof.at(-1).id);
  assert(f.proof.every(x=>used.has(x.id)),"unreachable proof record");
  assert(f.clauses.every(x=>used.has(x.id)),"unreachable source record");
}

const altered=structuredClone(packet), f=altered.fixtures[0], extra=structuredClone(f.proof[0]);
extra.id="junk420-node";f.proof.splice(f.proof.length-1,0,extra);
assert(!run(altered),"extra unreachable record accepted");
const reordered=structuredClone(packet), q=reordered.fixtures[0].proof;
q.splice(0,4,q[3],q[0],q[1],q[2]);
assert(run(reordered),"legal topological reorder rejected");

const AND=(a,b,o)=>[[-o,a],[-o,b],[o,-a,-b]];
function TT(a,b,o,fn){const out=[];for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let z=0;z<2;z++)if(z!==fn(x,y))out.push([-a*(x?1:-1),-b*(y?1:-1),-o*(z?1:-1)]);return out}
const G=[...AND(2,3,4),...AND(-1,-4,5),...TT(4,2,8,(a,b)=>+(a===b)),...AND(1,8,6),
         ...TT(1,3,9,(a,b)=>a^b),...TT(4,3,10,(a,b)=>+(a===b)),...AND(9,10,7)].map(norm);
assert(G.length===24,"gate facets");
const C=new Map(G.map((x,i)=>[i+1,x])), P=new Map();
const steps=[[25,6,13,1],[26,6,16,1],[34,15,13,1],[35,1,10,2],[36,7,3,2],[37,2,21,3],
[40,2,34,3],[45,18,36,3],[49,26,19,3],[63,25,37,4],[64,25,40,4],[79,45,35,4],
[82,49,35,4],[101,79,63,8],[104,82,64,8],[119,104,24,9],[122,101,119,10]];
for(const [id,a,b,p] of steps){C.set(id,resolve(C.get(a),C.get(b),p));P.set(id,[a,b])}
assert(same(C.get(122),[5,6,7]),"cover clause");
for(let i=0;i<3;i++){
 const t=5+i,z=11+i,a=200+2*i,b=a+1;
 C.set(a,norm([-t,z]));C.set(b,norm([-t,-z]));C.set(500+i,resolve(C.get(a),C.get(b),z));P.set(500+i,[a,b]);
}
for(const [id,a,b,p] of [[600,122,500,5],[601,600,501,6],[602,601,502,7]]){C.set(id,resolve(C.get(a),C.get(b),p));P.set(id,[a,b])}
assert(C.get(602).length===0,"empty sink");
const used=new Set();function visitPeer(id){if(used.has(id))return;used.add(id);if(P.has(id))for(const x of P.get(id))visitPeer(x)}visitPeer(602);
assert([...used].filter(x=>P.has(x)).length===23,"23 RES ancestors");
assert([...used].filter(x=>!P.has(x)).length===19,"19 source ancestors");
function depth(id){return P.has(id)?1+Math.max(...P.get(id).map(depth)):0}
assert(depth(122)===6&&depth(602)===9,"span");

const raw=JSON.parse(fs.readFileSync(rawPath,"utf8"));
assert(raw.checker_cases.length===7,"raw cases");
assert(raw.fixture_reachability.length===7,"raw fixtures");
assert(raw.peer_489_certificate.global_res===23,"raw peer count");
assert(raw.discharge_controls.branch_refutations_transformed>0,"raw discharge cases");
console.log(JSON.stringify({status:"PASS",checks,fixtures:packet.fixtures.length,
  dischargeCases:raw.discharge_controls.branch_refutations_transformed,peerGlobalRes:23}));

#!/usr/bin/env node
'use strict';
// Independent no-import semantic and certificate-shape replay for REFEREE373.
import fs from 'node:fs';
import assert from 'node:assert/strict';

const root = new URL('../../../', import.meta.url);
const raw = JSON.parse(fs.readFileSync(new URL('results/raw/arc/2026-11-05_1648_LSPV5_REFEREE373_raw.json', root)));
const certs = JSON.parse(fs.readFileSync(new URL('results/raw/arc/2026-11-05_1648_LSPV5_REFEREE373_certificates.json', root)));
let checks = 0;
const ok = x => { assert.ok(x); checks++; };
const eq = (a,b) => { assert.deepEqual(a,b); checks++; };
const norm = c => [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||Number(a<0)-Number(b<0));
const sat = (c,e) => c.some(x => e[Math.abs(x)] === Number(x>0));
const resolve = (a,b,p) => {
  ok((a.includes(p)&&b.includes(-p)) || (a.includes(-p)&&b.includes(p)));
  if (a.includes(-p)&&b.includes(p)) [a,b]=[b,a];
  return norm([...a.filter(x=>x!==p), ...b.filter(x=>x!==-p)]);
};
const S=[[1,3,4],[1,3,-4],[1,-3,4],[1,-3,-4],[-1,2,5],[-1,2,-5],[-1,-2,6],[-1,-2,-6]];
const F=[[1],[-1,2],[-1,-2]];
const assignments = n => Array.from({length:1<<n},(_,z)=>Object.fromEntries(Array.from({length:n},(_,i)=>[i+1,(z>>i)&1])));

for (const e of assignments(6)) {
  eq(S.every(c=>sat(c,e)), F.every(c=>sat(c,e)));
  ok(!S.every(c=>sat(c,e)));
}
for (let gone=0; gone<8; gone++) {
  ok(assignments(6).some(e=>S.every((c,i)=>i===gone||sat(c,e))));
}
for (let gone=0; gone<3; gone++) {
  ok(assignments(2).some(e=>F.every((c,i)=>i===gone||sat(c,e))));
}

const a=resolve(S[0],S[1],4), b=resolve(S[2],S[3],4);
const c=resolve(S[4],S[5],5), d=resolve(S[6],S[7],6);
eq([a,b,c,d],[[1,3],[1,-3],[-1,2],[-1,-2]]);
eq(resolve(resolve(a,b,3),resolve(c,d,2),1),[]);
eq(resolve(F[0],resolve(F[1],F[2],2),1),[]);

const table=(left,right)=>{
  const support=[...new Set([...left,...right].map(Math.abs))].sort((x,y)=>x-y);
  return Array.from({length:1<<support.length},(_,z)=>{
    const e=Object.fromEntries(support.map((v,i)=>[v,(z>>i)&1]));
    return Number(sat(left,e)&&sat(right,e));
  });
};
eq(table([1,2],[-1,-2]),[0,1,1,0]);
eq(table([1],[-1,-2]),[0,1,0,0]);
ok(JSON.stringify(table([1,2],[-1,-2]))!==JSON.stringify(table([1],[-1,-2])));

const affine=(mask,rhs,e)=>Number(mask.reduce((z,v)=>z^e[v],0)===rhs);
for (const mask of [[],[1],[2],[1,2]]) for (const rhs of [0,1]) {
  ok(assignments(2).some(e=>table([1],[-1,-2])[e[1]+2*e[2]]!==affine(mask,rhs,e)));
}

eq(raw.status,'PASS');
eq(raw.accepted.mixed_13.distinct_nodes,13);
eq(raw.accepted.padded_optimal_7.distinct_nodes,7);
eq(raw.accepted.original_optimal_2.distinct_nodes,2);
eq(raw.strengthening_firewall.all_affine_annotations_rejected.length,8);
eq(raw.minimum_certificate.deletion_witnesses.length,8);
eq(raw.minimum_certificate.original_deletion_witnesses.length,3);
eq(Object.keys(certs).sort(),['mixed_13_canon2r','original_optimal_2_canon2r','padded_optimal_7_canon2r']);
for (const [name,w] of Object.entries(certs)) {
  eq(w.format,'Rmix341-CANON2R');
  ok(typeof w.source_raw_b64==='string' && w.source_raw_b64.length>0);
  ok(/^[0-9a-f]{64}$/.test(w.source_raw_sha256));
  ok(w.proof && w.proof.format==='Rmix341-CANON2');
  ok(Array.isArray(w.proof.nodes));
  if (name==='mixed_13_canon2r') eq(w.proof.nodes.length,13);
  if (name==='padded_optimal_7_canon2r') eq(w.proof.nodes.length,7);
  if (name==='original_optimal_2_canon2r') eq(w.proof.nodes.length,2);
}

const result={artifact:'REFEREE373-independent',status:'PASS',checks,
  exhaustive_assignments:64,affine_candidates_rejected:8,
  accepted_node_counts:[13,7,2],rss_bytes:process.memoryUsage().rss};
fs.writeFileSync(new URL('results/raw/arc/2026-11-05_1648_LSPV5_REFEREE373_independent.json',root),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));

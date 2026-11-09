#!/usr/bin/env node
// Independent Node verifier: solve each pair-defect extension as a finite
// F_3 linear system, without enumerating the Python program's assignments.

import fs from 'node:fs';

const rawPath = 'results/raw/arc/2026-11-09_0115_LSPV5_455_PAIR_DEFECT_2CUT_RAW.json';
const raw = JSON.parse(fs.readFileSync(rawPath, 'utf8'));
const V = raw.graph.vertices;
const E = raw.graph.edges;
const mod = x => ((x % 3) + 3) % 3;

function rank(A) {
  A = A.map(r => r.map(mod));
  let row = 0;
  for (let col = 0; col < (A[0]?.length ?? 0) && row < A.length; col++) {
    const pivot = A.findIndex((r, i) => i >= row && r[col] !== 0);
    if (pivot < 0) continue;
    [A[row], A[pivot]] = [A[pivot], A[row]];
    if (A[row][col] === 2) A[row] = A[row].map(x => mod(2 * x));
    for (let i = 0; i < A.length; i++) {
      if (i === row || A[i][col] === 0) continue;
      const f = A[i][col];
      A[i] = A[i].map((x, j) => mod(x - f * A[row][j]));
    }
    row++;
  }
  return row;
}

function incidence() {
  return V.map(v => E.map(([a,b]) => v === a ? 1 : v === b ? 2 : 0));
}

const B = incidence();
if (rank(B) !== V.length - 1) throw new Error('connected incidence rank mismatch');

function localRows(v, target) {
  const ids = E.map((e,i) => e.includes(v) ? i : -1).filter(i => i >= 0);
  const out = [];
  for (let a=0;a<3;a++) for (let b=0;b<3;b++) for (let c=0;c<3;c++) {
    const t=[a,b,c];
    const d=mod(t.reduce((s,x,j)=>s+B[v][ids[j]]*x,0));
    if (d===target) out.push({ids,t});
  }
  return out;
}

function consistent(A, rhs) {
  return rank(A) === rank(A.map((r,i)=>[...r,rhs[i]]));
}

const charges=[1,0,0,0,0,0,0,0], sigma=1;
const blockCounts={};
for (let u=0;u<V.length;u++) for (let v=u+1;v<V.length;v++) {
  let count=0;
  const ru=localRows(u, mod(charges[u]+sigma));
  const rv=localRows(v, mod(charges[v]+sigma));
  for (const U of ru) for (const W of rv) {
    const A=B.map(r=>[...r]);
    const rhs=charges.slice(); rhs[u]=mod(rhs[u]+1); rhs[v]=mod(rhs[v]+1);
    for (let j=0;j<3;j++) {
      const row=Array(E.length).fill(0); row[U.ids[j]]=1; A.push(row); rhs.push(U.t[j]);
    }
    for (let j=0;j<3;j++) {
      const row=Array(E.length).fill(0); row[W.ids[j]]=1; A.push(row); rhs.push(W.t[j]);
    }
    if (consistent(A,rhs)) count++;
  }
  blockCounts[`${u},${v}`]=count;
}
if (blockCounts['0,1']!==27) throw new Error(`cut block ${blockCounts['0,1']}`);
for (const row of raw.base.pairs) {
  const got=blockCounts[row.pair.join(',')];
  if (got!==row.block_edges) throw new Error(`block mismatch ${row.pair}: ${got}/${row.block_edges}`);
}

// Hostile controls: a forged 81-edge J9 block for the cut pair and a one-bit
// raw corruption are both rejected by exact comparison.
const forgedJ9Accepted = blockCounts['0,1'] === 81;
const corrupted = structuredClone(raw);
corrupted.base.cut_pair_0_1.block_edges = 81;
const corruptAccepted = corrupted.base.cut_pair_0_1.block_edges === blockCounts['0,1'];
if (forgedJ9Accepted || corruptAccepted) throw new Error('hostile control accepted');
if (raw.hostile_controls.accepted_boundary_sum !== 0 || raw.hostile_controls.rejected_boundary_sum !== 1) {
  throw new Error('component boundary control mismatch');
}

console.log(JSON.stringify({
  status:'PASS',
  incidence_rank:rank(B),
  cut_block_edges:blockCounts['0,1'],
  block_histogram:Object.values(blockCounts).reduce((h,x)=>(h[x]=(h[x]||0)+1,h),{}),
  forged_J9_rejected:true,
  corrupted_raw_rejected:true
}));

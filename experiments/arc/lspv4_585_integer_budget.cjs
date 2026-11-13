#!/usr/bin/env node
'use strict';
/* LSPV-4/585, restricted SOURCE-order alias class ONLY.
 * Usage: node experiments/arc/lspv4_585_integer_budget.cjs [584-raw.json] [585-out.json]
 * S is an explicitly separate insertion-sort comparator metric, not historical R_mix341 work.
 */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const input=process.argv[2]||path.resolve(__dirname,'../../results/raw/arc/2026-11-13_0436_LSPV4_584_WEIGHTED_SOURCE_ALIAS_FRONTIER_RAW.json');
const output=process.argv[3]||path.resolve(__dirname,'../../results/raw/arc/2026-11-13_0536_LSPV4_585_INTEGER_BUDGET_FRONTIER_RAW.json');
const raw=JSON.parse(fs.readFileSync(input,'utf8'));
assert.equal(raw.metrics.min_Q,29238); assert.equal(raw.metrics.min_S,656);
assert.equal(raw.metrics.min_Q_requires_S,823); assert.equal(raw.metrics.min_S_requires_Q,38700);
const hist=Object.entries(raw.histogram).map(([d,n])=>[Number(d),n]).sort((a,b)=>a[0]-b[0]);
assert.equal(hist.length,49);
assert(hist.every(([d,n])=>Number.isSafeInteger(d)&&d>0&&Number.isSafeInteger(n)&&n>0));
const ds=hist.flatMap(([d,n])=>Array(n).fill(d)).sort((a,b)=>b-a);
assert.equal(ds.length,167); assert.equal(ds.reduce((a,b)=>a+b,0),9462);
const prefix=[0]; for(const d of ds)prefix.push(prefix.at(-1)+d);
const frontier=prefix.map((v,k)=>({sort_budget:656+k,minimum_probe_Q:38700-v,extra_comparisons:k,savings_from_minS:v}));
assert.equal(frontier.length,168); assert.equal(frontier[0].minimum_probe_Q,38700);
assert.equal(frontier.at(-1).minimum_probe_Q,29238);
for(let k=0;k<167;k++)assert.equal(frontier[k].minimum_probe_Q-frontier[k+1].minimum_probe_Q,ds[k]);
// Independent exact grouped-knapsack recurrence. Every budget is compared.
let dp=new Map([[0,0]]);
for(const [d,n] of hist){
  const next=new Map();
  for(const [k,v] of dp)for(let m=0;m<=n;m++)
    next.set(k+m,Math.max(next.get(k+m)??-1,v+m*d));
  dp=next;
}
assert.equal(dp.size,168);
for(let k=0;k<=167;k++)assert.equal(dp.get(k),prefix[k]);
// Scalar weighted minima reproduce the earlier 49-kink formula.
for(const lam of [0,1,2,3,4,5,6,7,8,9,10,15,20,49,234,235,1000]){
  const a=29238+656*lam+hist.reduce((v,[d,n])=>v+n*Math.min(d,lam),0);
  const b=Math.min(...frontier.map(x=>x.minimum_probe_Q+lam*x.sort_budget));
  assert.equal(a,b);
}
const samples=Object.fromEntries([0,1,10,20,44,50,84,100,133,150,166,167].map(k=>[k,frontier[k]]));
const out={
 schema:'LSPV4_585_INTEGER_SORT_BUDGET_FRONTIER/v1',
 status:'PROVED/RESTRICTED finite-product theorem; COMPUTATIONAL grouped-knapsack checks',
 scope:'Archived /341 SOURCE-order aliases only; NOT full historical R_mix341 or physical time/space',
 upstream:{blob:'38411a856e021c17bd4973eb675395fa8689a419',original_producer:'4081022e8a3841d79f751a3d3a7a10decbb026da',original_checker:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',original_packet:'fe27fe1011d0021e721ccaeb747ed58da65d7464'},
 metrics:{pareto_points:168,min_Q:29238,min_S:656,max_S_needed_for_minQ:823,minQ_at_minS:38700,delta_count:167,kink_values:49,total_saving:9462,grouped_dp_tests:168,scalar_duality_tests:17},
 formula:'Qstar(656+k)=38700-sum_of_k_largest_positive_savings; 0<=k<=167',
 samples,frontier,
 limitations:['Q is deletion-witness literal probes, not entire checker work','S counts explicit insertion sort comparisons, not historical native tariff','Original OS checker replay not executed in this run','Other mixed rules and proof representations remain admissible']
};
fs.mkdirSync(path.dirname(output),{recursive:true});fs.writeFileSync(output,JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify({status:'PASS',metrics:out.metrics,samples:out.samples},null,2));

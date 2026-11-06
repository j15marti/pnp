#!/usr/bin/env node
// Independent replay for REFEREE389.  No producer code is imported.

import fs from 'node:fs';
import crypto from 'node:crypto';
import { performance } from 'node:perf_hooks';

const read = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const started = performance.now();
let checks = 0;
const ok = (x, m) => { checks++; if (!x) throw new Error(m); };

const c389 = read('results/raw/review/2026-11-06_0848_LSPV5_SPLIT_ROR_COUNTEREXAMPLE389.json');
const r386 = read('results/raw/review/2026-11-06_0548_LSPV5_BRIDGE_CUT_TOPOLOGY386.json');
const r388 = read('results/raw/review/2026-11-06_0748_LSPV5_READONCE_RESOLUTION388.json');
const v388 = read('results/raw/review/2026-11-06_0748_LSPV5_READONCE_RESOLUTION388_verification.json');
const a389 = read('results/raw/review/2026-11-06_0848_LSPV5_BRIDGE_MUS_NORMALIZATION389.json');

const key = c => [...c].sort((a,b)=>a-b).join(',');
function strictResolve(a0,b0) {
  const a=new Set(a0), b=new Set(b0), vars=new Set([...a,...b].map(Math.abs));
  const ps=[...vars].filter(v=>(a.has(v)&&b.has(-v))||(a.has(-v)&&b.has(v)));
  if(ps.length!==1) throw new Error('not exactly one pivot');
  const p=ps[0], r=new Set([...a,...b]); r.delete(p); r.delete(-p);
  for(const l of r) if(r.has(-l)) throw new Error('tautological resolvent');
  return [...r].sort((x,y)=>x-y);
}

function verifyTree(node,sources,used=[]) {
  if(Object.hasOwn(node,'source')) {
    ok(Number.isInteger(node.source)&&node.source>=0&&node.source<sources.length,'bad source id');
    ok(key(node.clause)===key(sources[node.source]),'leaf clause/source mismatch');
    used.push(node.source); return [...node.clause].sort((a,b)=>a-b);
  }
  ok(node.left&&node.right,'missing binary premise');
  const l=verifyTree(node.left,sources,used), r=verifyTree(node.right,sources,used);
  const got=strictResolve(l,r);
  ok(key(got)===key(node.clause),'derived clause mismatch');
  return got;
}

function satModels(formula, vars) {
  const out=[];
  for(let mask=0;mask<(1<<vars);mask++) {
    if(formula.every(c=>c.some(l=>(((mask>>(Math.abs(l)-1))&1)===Number(l>0))))) out.push(mask);
  }
  return out;
}

function closure(sources) {
  const n=sources.length, dp=Array.from({length:1<<n},()=>new Map());
  sources.forEach((c,i)=>dp[1<<i].set(key(c),c));
  for(let size=2;size<=n;size++) for(let mask=1;mask<(1<<n);mask++) {
    if(popcount(mask)!==size) continue;
    const anchor=mask&-mask;
    for(let sub=(mask-1)&mask;sub;sub=(sub-1)&mask) {
      const other=mask^sub; if(!other||!(sub&anchor)) continue;
      for(const a of dp[sub].values()) for(const b of dp[other].values()) {
        try { const r=strictResolve(a,b); dp[mask].set(key(r),r); } catch {}
      }
    }
  }
  return dp.at(-1);
}
function popcount(x){let c=0;while(x){x&=x-1;c++;}return c;}

const ex=c389.unrestricted_counterexample;
const sources=[...ex.left_sources,...ex.right_sources];
const used=[]; const root=verifyTree(ex.global_tree,sources,used);
ok(root.length===0,'counterexample root is not empty');
ok(used.length===5&&new Set(used).size===5,'counterexample is not source-once');
ok([...used].sort((a,b)=>a-b).every((x,i)=>x===i),'counterexample omits source');
const lm=satModels(ex.left_sources,3), rm=satModels(ex.right_sources,3);
ok(lm.length===4&&lm.every(m=>m&1),'left does not force b');
ok(rm.length===2&&rm.every(m=>!(m&1)),'right does not force not-b');
const lc=closure(ex.left_sources), rc=closure(ex.right_sources);
ok(lc.has('1'),'left full-source unit absent');
ok(!rc.has('-1'),'right full-source unit unexpectedly present');
const all=sources;
const deletions=all.map((_,i)=>satModels(all.slice(0,i).concat(all.slice(i+1)),3).length);
ok(deletions.some(n=>n===0),'counterexample unexpectedly MUS');

const clauses=r386.source.clauses, core=r386.core.map(i=>clauses[i]);
ok(satModels(core,15).length===0,'bridge core SAT');
for(let i=0;i<core.length;i++) ok(satModels(core.slice(0,i).concat(core.slice(i+1)),15).length>0,`bridge deletion ${i} UNSAT`);
const left=r388.left_source_ids.map(i=>clauses[i]);
const right=r388.right_source_ids.map(i=>clauses[i]);
const lvars=new Set(left.flat().map(Math.abs)), rvars=new Set(right.flat().map(Math.abs));
const shared=[...lvars].filter(v=>rvars.has(v)).sort((a,b)=>a-b);
ok(key(shared)==='15','bridge cut is not one variable');
ok(!left.some(c=>c.includes(-15)),'left wrong bridge polarity');
ok(!right.some(c=>c.includes(15)),'right wrong bridge polarity');
const blm=satModels(left,15), brm=satModels(right,15);
ok(blm.length===1024&&blm.every(m=>m&(1<<14)),'left bridge semantics');
ok(brm.length===1024&&brm.every(m=>!(m&(1<<14))),'right bridge semantics');
ok(v388.pass&&!v388.left_target_found&&!v388.right_target_found,'REF388 independent status');
ok(r388.left.full_outcomes.length===1888&&r388.right.full_outcomes.length===1888,'REF388 outcome count');
ok(r388.left.pair_tests===1126097195&&r388.right.pair_tests===1126097195,'REF388 pair count');
ok(a389.bridge.new_consequence.includes('including interleaved'),'new consequence missing');

const digest=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
ok(digest('results/raw/review/2026-11-06_0748_LSPV5_READONCE_RESOLUTION388.json')==='051f0c0596b788c3b14116d1acfaf35ca1a2325c22d55ec8e756f4ef1cf2e470','REF388 hash');
ok(digest('results/raw/review/2026-11-06_0748_LSPV5_READONCE_RESOLUTION388_verification.json')==='db9ec0acd0390cfa75a4e4f91e016fd15c469b036faa0a2b5bac84ad7f16487c','REF388 verifier hash');

let rejected=0;
function reject(mutator){const x=structuredClone(ex.global_tree);mutator(x);try{verifyTree(x,sources,[]);}catch{rejected++;}}
reject(x=>{x.clause=[1];});
reject(x=>{x.left.left.left.left.source=99;});
reject(x=>{x.left.left.clause=[1];});
reject(x=>{delete x.right;});
reject(x=>{x.left.left.left.right.source=0;x.left.left.left.right.clause=[-2,1];});
ok(rejected===5,'hostile tree mutations not all rejected');

const result={pass:true,checks,hostile_mutations_rejected:rejected,
  five_source_global_nodes:9,five_source_paid_resolution_nodes:4,
  bridge_core_clauses:36,bridge_deletion_checks:36,
  ref388_full_outcomes_each:1888,ref388_pair_tests_each:1126097195,
  elapsed_seconds:(performance.now()-started)/1000,
  max_rss_kib:Math.round(process.memoryUsage().rss/1024)};
fs.writeFileSync('results/raw/review/2026-11-06_0848_LSPV5_BRIDGE_MUS_NORMALIZATION389_verification.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));

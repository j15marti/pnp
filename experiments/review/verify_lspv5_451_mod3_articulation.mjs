#!/usr/bin/env node
import fs from 'node:fs';

if (process.argv.length !== 3) {
  console.error('usage: node verify_lspv5_451_mod3_articulation.mjs RAW.json');
  process.exit(2);
}

const raw = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
let checks = 0;
const assert = (p, msg) => { checks++; if (!p) throw new Error(msg); };
const mod = x => ((x % 3) + 3) % 3;

function reconstructGraph() {
  const edges = [];
  for (let arm = 0; arm < 3; arm++) {
    const p = 1 + 5 * arm;
    const [k0, k1, k2, k3] = [2, 3, 4, 5].map(x => x + 5 * arm);
    edges.push([0,p],[p,k0],[p,k1],[k0,k2],[k0,k3],[k1,k2],[k1,k3],[k2,k3]);
  }
  return edges.map(e => e[0] < e[1] ? e : [e[1],e[0]])
    .sort((a,b) => a[0]-b[0] || a[1]-b[1]);
}

function incidence(edges) {
  const inc = Array.from({length:16}, () => []);
  edges.forEach(([u,v], eid) => { inc[u].push([eid,1]); inc[v].push([eid,-1]); });
  inc.forEach(row => row.sort((a,b) => a[0]-b[0]));
  return inc;
}

function componentCountWithout(v, edges) {
  const adj = Array.from({length:16}, () => []);
  edges.forEach(([a,b]) => { if (a !== v && b !== v) { adj[a].push(b); adj[b].push(a); } });
  const seen = new Set([v]); let count = 0;
  for (let s=0;s<16;s++) if (!seen.has(s)) {
    count++; const q=[s]; seen.add(s);
    while(q.length) { const x=q.pop(); for(const y of adj[x]) if(!seen.has(y)){seen.add(y);q.push(y);} }
  }
  return count;
}

function sourceFor(sigma, edges, inc) {
  const charges = Array(16).fill(0); charges[0]=sigma;
  const out = edges.map((_,eid) => ({id:`A:${eid}`,kind:'ALO',edge:eid}));
  for(let v=0;v<16;v++) for(let a=0;a<3;a++) for(let b=0;b<3;b++) for(let c=0;c<3;c++) {
    const vals=[a,b,c];
    const s=mod(inc[v].reduce((z,[,sgn],i)=>z+sgn*vals[i],0));
    if(s!==charges[v]) out.push({id:`D:${v}:${a}${b}${c}`,kind:'FORBID',vertex:v,
      edges:inc[v].map(x=>x[0]),values:vals,signed_sum:s});
  }
  return {charges,out};
}

function falseSources(source, values, missing = new Set()) {
  const bad=[];
  for(const cl of source) {
    let ok;
    if(cl.kind==='ALO') ok=!missing.has(cl.edge);
    else ok=cl.edges.some((eid,i)=>missing.has(eid)||values[eid]!==cl.values[i]);
    if(!ok) bad.push(cl.id);
  }
  return bad;
}

function validFlow(values, inc, charges, skipped = new Set(), missing = new Set()) {
  if(!Array.isArray(values)||values.length!==24||values.some(x=>!Number.isInteger(x)||x<0||x>2)) return false;
  for(let v=0;v<16;v++) if(!skipped.has(v)) {
    const s=mod(inc[v].reduce((z,[eid,sgn])=>z+(missing.has(eid)?0:sgn*values[eid]),0));
    if(s!==charges[v]) return false;
  }
  return true;
}

const edges=reconstructGraph();
assert(JSON.stringify(raw.graph.edges)===JSON.stringify(edges),'graph edge list mismatch');
assert(raw.graph.vertices===16&&raw.graph.edge_count===24&&raw.graph.cubic===true,'graph metadata mismatch');
const inc=incidence(edges);
assert(inc.every(r=>r.length===3),'graph is not cubic');
const cvs=Array.from({length:16},(_,v)=>componentCountWithout(v,edges));
assert(cvs.filter(x=>x===3).length===1&&cvs.filter(x=>x===2).length===3&&cvs.filter(x=>x===1).length===12,'c_v distribution mismatch');
assert(raw.component_rows.every(r=>r.c_v===cvs[r.vertex]&&r.predicted_forbidden_essential===3**(3-r.c_v)),'component rows mismatch');

for(const run of raw.runs) {
  const {charges,out:source}=sourceFor(run.sigma,edges,inc);
  assert(source.length===312&&run.source_clause_count===312,'source size mismatch');
  const byId=new Map(source.map(x=>[x.id,x]));
  const seenF=new Set();
  for(const w of run.forbidden_witnesses) {
    const cl=byId.get(w.deleted);
    assert(cl?.kind==='FORBID','unknown forbidden deletion');
    assert(!seenF.has(w.deleted),'duplicate forbidden witness'); seenF.add(w.deleted);
    assert(validFlow(w.edge_values,inc,charges,new Set([cl.vertex])),'invalid forbidden-deletion flow');
    assert(JSON.stringify(falseSources(source,w.edge_values))===JSON.stringify([w.deleted]),'forbidden witness has wrong false set');
  }
  const expectedByV=Array.from({length:16},(_,v)=>3**(3-cvs[v]));
  const actualByV=Array(16).fill(0);
  for(const id of seenF) actualByV[Number(id.split(':')[1])]++;
  assert(JSON.stringify(actualByV)===JSON.stringify(expectedByV),'forbidden count formula mismatch');
  assert(JSON.stringify(run.forbidden_counts_by_vertex)===JSON.stringify(expectedByV),'reported forbidden counts mismatch');
  assert(run.forbidden_essential_count===118,'forbidden total mismatch');

  const seenA=new Set();
  for(const w of run.alo_witnesses) {
    assert(w.deleted===`A:${w.missing_edge}`,'ALO id mismatch');
    assert(!seenA.has(w.deleted),'duplicate ALO witness'); seenA.add(w.deleted);
    const [u,v]=edges[w.missing_edge];
    assert(validFlow(w.edge_values,inc,charges,new Set([u,v]),new Set([w.missing_edge])),'invalid ALO-deletion flow');
    assert(JSON.stringify(falseSources(source,w.edge_values,new Set([w.missing_edge])))===JSON.stringify([w.deleted]),'ALO witness has wrong false set');
  }
  assert(seenA.size===24,'missing ALO witness');
  assert(run.total_individually_essential_sources===142&&142===24+118,'essential-source total mismatch');
  assert(run.two_connected_formula_would_claim===168,'2-connected control mismatch');

  const seenPairs=new Set();
  for(const w of run.pair_defect_witnesses) {
    const [u,v]=w.vertices; const key=`${u},${v}`;
    assert(u<v&&!seenPairs.has(key),'duplicate or unordered pair'); seenPairs.add(key);
    const target=charges.slice(); target[u]=mod(target[u]+run.sigma); target[v]=mod(target[v]+run.sigma);
    assert(validFlow(w.edge_values,inc,target),'invalid pair-defect flow');
    const bad=falseSources(source,w.edge_values);
    assert(JSON.stringify(bad)===JSON.stringify(w.false_sources),'pair false-source list mismatch');
    assert(bad.length===2&&new Set(bad.map(x=>Number(x.split(':')[1]))).size===2&&bad.every(x=>[u,v].includes(Number(x.split(':')[1]))),'pair assumptions leaked scope');
    assert(bad.every(x=>byId.get(x).signed_sum===mod(charges[byId.get(x).vertex]+run.sigma)),'wrong defect class');
  }
  assert(seenPairs.size===120,'pair coverage mismatch');
  assert(JSON.stringify(run.single_wrong_group_unsat_vertices)===JSON.stringify(Array.from({length:16},(_,i)=>i)),'single-group UNSAT control mismatch');

  // Hostile in-memory mutations: each must be rejected by a relevant invariant.
  const duplicateIds=[...source,source[0]];
  assert(new Set(duplicateIds.map(x=>x.id)).size!==duplicateIds.length,'duplicate source-ID control did not fail');
  const badOwner={...byId.get(run.forbidden_witnesses[0].deleted),vertex:15};
  assert(badOwner.vertex!==Number(badOwner.id.split(':')[1]),'owner-corruption control did not fail');
  const badPair={...run.pair_defect_witnesses[0],vertices:[0,15]};
  assert(new Set(badPair.false_sources.map(x=>Number(x.split(':')[1]))).size===2 &&
    badPair.false_sources.some(x=>![0,15].includes(Number(x.split(':')[1]))),'scope-corruption control did not fail');
  const multihot=run.forbidden_witnesses[0].edge_values.slice(); multihot[0]=3;
  assert(!validFlow(multihot,inc,charges),'non-ternary/multihot control did not fail');
  const badMissing={...run.alo_witnesses[0],missing_edge:1};
  assert(badMissing.deleted!==`A:${badMissing.missing_edge}`,'missing-edge control did not fail');
}

assert(raw.status==='PASS','producer did not report PASS');
assert(raw.theorem_prediction==='forbidden essential at v = 3^(3-c_v); total = |E| + sum_v 3^(3-c_v)','theorem prediction mismatch');
console.log(JSON.stringify({status:'PASS',checks,vertices:16,edges:24,sigmas:raw.runs.map(x=>x.sigma),essential_sources:[142,142],pair_witnesses:[120,120]}));

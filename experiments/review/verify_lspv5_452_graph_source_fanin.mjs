#!/usr/bin/env node
import fs from 'node:fs';

const path = process.argv[2];
if (!path) throw new Error('usage: verify_lspv5_452_graph_source_fanin.mjs RAW.json');
const d = JSON.parse(fs.readFileSync(path, 'utf8'));
let checks = 0;
const mod = x => ((x % 3) + 3) % 3;

function incidence(n, edges) {
  const inc = Array.from({length:n}, () => []);
  edges.forEach(([u,v], eid) => { inc[u].push([eid,1]); inc[v].push([eid,-1]); });
  inc.forEach(r => r.sort((a,b)=>a[0]-b[0]));
  return inc;
}
function balance(inc, flow, v) {
  return mod(inc[v].reduce((s,[e,z]) => s + z*flow[e], 0));
}
function componentsWithout(n, edges, banned) {
  const adj = Array.from({length:n},()=>[]);
  for (const [u,v] of edges) if (u!==banned && v!==banned) { adj[u].push(v); adj[v].push(u); }
  const seen = new Set([banned]); let c=0;
  for (let s=0;s<n;s++) if (!seen.has(s)) {
    c++; const q=[s]; seen.add(s);
    while(q.length) { const u=q.pop(); for(const v of adj[u]) if(!seen.has(v)){seen.add(v);q.push(v);} }
  }
  return c;
}
function verifyDag(g, dag) {
  const known = new Set(Array.from({length:g.required_distinct_sources},(_,i)=>`S${i}`));
  const deps = new Map();
  for (const node of dag.nodes) {
    if (known.has(node.id)) throw new Error('duplicate node');
    if (node.antecedents.length < 1 || node.antecedents.length > dag.arity) throw new Error('bad arity');
    for (const a of node.antecedents) if(!known.has(a)) throw new Error('forward/cyclic dependency');
    deps.set(node.id,node.antecedents); known.add(node.id); checks++;
  }
  if (!known.has(dag.root)) throw new Error('missing root');
  const used = new Set(); const stack=[dag.root];
  while(stack.length){ const x=stack.pop(); if(used.has(x))continue; used.add(x); for(const a of deps.get(x)||[])stack.push(a); }
  for(let i=0;i<g.required_distinct_sources;i++) if(!used.has(`S${i}`)) throw new Error('unused source');
  const bound = Math.ceil((g.required_distinct_sources-1)/(dag.arity-1));
  if(dag.nodes.length!==bound || dag.lower_bound!==bound) throw new Error('non-tight DAG');
}

if (d.artifact !== 'LSPV5-GRAPH-SOURCE-FANIN452' || d.status !== 'PASS') throw new Error('header');
for (const g of d.graphs) {
  const n=g.vertices, edges=g.edges, inc=incidence(n,edges), charges=Array(n).fill(0); charges[0]=1;
  if(edges.length!==3*n/2 || inc.some(r=>r.length!==3)) throw new Error('not cubic');
  const cv=Array.from({length:n},(_,v)=>componentsWithout(n,edges,v));
  if(JSON.stringify(cv)!==JSON.stringify(g.components_after_deletion)) throw new Error('component mismatch');
  const ess=cv.reduce((s,c)=>s+3**(3-c),0);
  if(ess!==g.indispensable_forbidden) throw new Error('essential count');
  const seenEssential=Array(n).fill(0);
  for(const w of g.essential_witnesses){
    if(w.flow.length!==edges.length) throw new Error('flow length');
    for(let v=0;v<n;v++) if(v!==w.vertex && balance(inc,w.flow,v)!==charges[v]) throw new Error('bad essential witness');
    const vals=inc[w.vertex].map(([e])=>w.flow[e]);
    if(JSON.stringify(vals)!==JSON.stringify(w.tuple)) throw new Error('tuple mismatch');
    if(balance(inc,w.flow,w.vertex)!==mod(charges[w.vertex]-1)) throw new Error('wrong E class');
    if(balance(inc,w.flow,w.vertex)===mod(charges[w.vertex]+1)) throw new Error('E/R overlap');
    seenEssential[w.vertex]++; checks++;
  }
  seenEssential.forEach((z,v)=>{if(z!==3**(3-cv[v]))throw new Error('witness multiplicity');});
  for(const w of g.alo_witnesses){
    const [u,v]=edges[w.edge];
    for(let x=0;x<n;x++) if(x!==u&&x!==v&&balance(inc,w.flow,x)!==charges[x]) throw new Error('bad ALO witness');
    checks++;
  }
  for(const w of g.pair_defect_witnesses){
    const bad=new Set(w.vertices);
    for(let v=0;v<n;v++){
      const want=mod(charges[v]+(bad.has(v)?1:0));
      if(balance(inc,w.flow,v)!==want) throw new Error('bad pair witness');
    }
    checks++;
  }
  const r=edges.length+ess+n-1;
  if(r!==g.required_distinct_sources || r-1!==g.binary_charged_node_lower_bound) throw new Error('bound');
  g.tight_dependency_dags.forEach(x=>verifyDag(g,x));
}
const hostile = Object.fromEntries(d.hostile_controls.map(x=>[x.label,x.expected]));
if(hostile.sigma_zero_merges_E_and_R!=='REJECT' || hostile.omit_two_R_groups!=='SAT_WITNESS' ||
   hostile.unbounded_arity_jump!=='OUTSIDE_ASSUMPTIONS' || hostile.cyclic_dependency!=='REJECT') throw new Error('hostile controls');
console.log(JSON.stringify({status:'PASS',graphs:d.graphs.length,checks,scope:d.scope},null,2));

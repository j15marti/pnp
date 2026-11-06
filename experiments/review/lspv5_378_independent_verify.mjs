#!/usr/bin/env node
// Independent verifier for REFEREE378's declared FACET-A bytes.
import fs from 'node:fs';
import crypto from 'node:crypto';

const path = new URL('../../results/raw/review/2026-11-05_2153_LSPV5_STRICT3_BPHP_FACETA378.json', import.meta.url);
const raw = fs.readFileSync(path);
const doc = JSON.parse(raw);
let checks = 0;
const req = (x, m) => { checks++; if (!x) throw new Error(m); };
const norm = c => [...new Set(c)].sort((x,y)=>Math.abs(x)-Math.abs(y)||(x<0?-1:1));
const same = (a,b) => JSON.stringify(a)===JSON.stringify(b);
const sha = x => crypto.createHash('sha256').update(x).digest('hex');

function verifyTrace(T) {
  const clause = new Map(), depth = new Map(), defs = new Map(), ids = new Set();
  for (const s of T.trace.sources) {
    req(!ids.has(s.id), 'duplicate source id');
    ids.add(s.id);
    req(s.clause.length===3 && new Set(s.clause.map(Math.abs)).size===3, 'proper strict3');
    clause.set(s.id, norm(s.clause)); depth.set(s.id,0);
  }
  const lines=T.dimacs.trimEnd().split('\n');
  req(lines[0]===`p cnf ${T.source_variables} ${T.strict3_source_clauses}`, 'header');
  req(lines.length===T.strict3_source_clauses+1, 'source count');
  req(sha(T.dimacs)===T.source_sha256 && Buffer.byteLength(T.dimacs)===T.source_bytes, 'source identity');
  for(let i=1;i<lines.length;i++){
    const xs=lines[i].trim().split(/\s+/).map(Number);
    req(xs.length===4&&xs[3]===0, 'source line');
    req(same(norm(xs.slice(0,3)),T.trace.sources[i-1].clause), 'source bytes bind clauses');
  }
  const refClause = ref => {
    if(ref.includes('#f')){
      const [owner,fi]=ref.split('#f'); const d=defs.get(owner);
      req(!!d && /^[012]$/.test(fi), 'facet reference');
      return d.facets[Number(fi)];
    }
    req(clause.has(ref), 'node reference'); return clause.get(ref);
  };
  const refDepth = ref => depth.get(ref.split('#f')[0]);
  let defCount=0,resCount=0,maxVar=T.source_variables;
  for (const n of T.trace.nodes) {
    req(!ids.has(n.id), 'globally unique node id'); ids.add(n.id);
    if(n.kind==='def'){
      defCount++;
      req(n.out>maxVar, 'global freshness'); maxVar=n.out;
      if(n.parent_owner!==null) req(defs.has(n.parent_owner), 'parent owner');
      const expected=[norm([-n.out,n.a]),norm([-n.out,n.b]),norm([n.out,-n.a,-n.b])];
      req(same(n.facets,expected), 'signed AND facets');
      defs.set(n.id,n);
      depth.set(n.id,1+(n.parent_owner===null?0:depth.get(n.parent_owner)));
    } else {
      resCount++;
      const L=refClause(n.left),R=refClause(n.right);
      req(L.includes(n.pivot)&&R.includes(-n.pivot), 'oriented pivot');
      const out=norm(L.filter(x=>x!==n.pivot).concat(R.filter(x=>x!==-n.pivot)));
      req(!out.some(x=>out.includes(-x)), 'no tautological resolvent');
      req(same(out,n.clause), 'exact resolvent');
      clause.set(n.id,out); depth.set(n.id,Math.max(refDepth(n.left),refDepth(n.right))+1);
    }
  }
  req(defCount===T.paid_def && resCount===T.paid_res_total, 'paid node counts');
  req(maxVar===T.final_variables_after_def, 'final variable bound');
  const outs=T.trace.outputs.at_least_one.concat(T.trace.outputs.collisions);
  req(outs.every(x=>clause.has(x)), 'all outputs exist');
  req(Math.max(...outs.map(x=>depth.get(x)))===T.critical_path_pre_php, 'critical path');
  req(T.trace.outputs.at_least_one.length===T.pigeons, 'unary A outputs');
  req(T.trace.outputs.collisions.length===T.original_wide_clauses, 'unary B outputs');
  for(const x of T.trace.outputs.at_least_one) req(clause.get(x).length===T.holes, 'A width');
  for(const x of T.trace.outputs.collisions) req(clause.get(x).length===2, 'B width');

  const ell=T.ell,n=2**ell,m=n+1,M=n*m*(m-1)/2;
  const Q=M*(2*ell-3),D=m*(2*n-4);
  let I=0;for(let d=3;d<=ell;d++)I+=2**d*(d-1);
  const R=m*(2*n-5+I)+2*ell*M;
  req(T.source_res===Q && T.paid_def===D, 'Q,D formulas');
  req(T.compiler_res_without_source_reconstruction===R, 'compiler R formula');
  req(T.paid_work_pre_php===Q+D+R, 'union work');
  req(T.critical_path_pre_php===Math.max(n-1,4*ell-3), 'span formula');

  // Hostile controls are performed on copies, not counted as accepted traces.
  const firstRes=T.trace.nodes.find(x=>x.kind==='res');
  req(!refClause(firstRes.left).includes(firstRes.pivot+1), 'wrong-pivot control');
  const firstDef=T.trace.nodes.find(x=>x.kind==='def');
  req(firstDef.out!==Math.abs(firstDef.a) && firstDef.out!==Math.abs(firstDef.b), 'freshness control');
}

req(doc.historical_authoritative_checker===false, 'scope');
req(doc.full_empty_clause_refutation===false, 'prefix compiler only');
for(const t of doc.traces) verifyTrace(t);
req(doc.sat_controls.every(x=>x.distinct_address_witness), 'SAT controls');
let hostileRejected=0;
function mustReject(mutator,label){
  const bad=structuredClone(doc.traces[0]); mutator(bad);
  let rejected=false; try { verifyTrace(bad); } catch { rejected=true; }
  req(rejected,`hostile accepted: ${label}`); hostileRejected++;
}
mustReject(t=>{t.trace.nodes.find(x=>x.kind==='res').pivot+=10000},'bad pivot');
mustReject(t=>{const d=t.trace.nodes.find(x=>x.kind==='def');d.out=Math.abs(d.a)},'nonfresh DEF');
mustReject(t=>{t.trace.nodes.find(x=>x.kind==='def').facets[0][0]*=-1},'corrupt facet');
mustReject(t=>{t.trace.nodes[1].id=t.trace.nodes[0].id},'duplicate node id');
mustReject(t=>{t.trace.outputs.at_least_one.pop()},'omitted AND obligation');
mustReject(t=>{t.source_sha256='0'.repeat(64)},'source identity');
mustReject(t=>{t.dimacs=t.dimacs.replace(/^p cnf \d+ /,'p cnf 1 ')},'malformed DIMACS header');
console.log(JSON.stringify({status:'COMPUTATIONAL FACET-A accepted',checks,
  hostile_rejected:hostileRejected,raw_sha256:sha(raw),
  traces:doc.traces.map(x=>({ell:x.ell,work:x.paid_work_pre_php,span:x.critical_path_pre_php}))},null,2));

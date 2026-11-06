#!/usr/bin/env node
// Independent verifier for REFEREE379's compact declared FACET-A certificate.
// It reconstructs every omitted facet and resolvent; it does not import the producer.
import fs from 'node:fs';
import crypto from 'node:crypto';

const path = new URL('../../results/raw/review/2026-11-05_2253_LSPV5_FULL_COOK_FACETA379.json', import.meta.url);
const raw = fs.readFileSync(path);
const doc = JSON.parse(raw);
let checks = 0;
const req = (x,m) => { checks++; if(!x) throw new Error(m); };
const norm = c => [...new Set(c)].sort((x,y)=>Math.abs(x)-Math.abs(y)||(x<0?-1:1));
const same = (a,b) => JSON.stringify(a)===JSON.stringify(b);
const sha = x => crypto.createHash('sha256').update(x).digest('hex');

function verifyTrace(T) {
  const clause=new Map(), depth=new Map(), defs=new Map(), ids=new Set(), varOwner=new Map();
  const dep=new Map();
  for(const s of T.trace.sources){
    req(!ids.has(s.id),'duplicate source'); ids.add(s.id);
    req(s.clause.length===3&&new Set(s.clause.map(Math.abs)).size===3,'proper strict3');
    const c=norm(s.clause); clause.set(s.id,c); depth.set(s.id,0); dep.set(s.id,[]);
  }
  const dimacs=T.dimacs, lines=dimacs.trimEnd().split('\n');
  req(lines[0]===`p cnf ${T.source_variables} ${T.strict3_source_clauses}`,'DIMACS header');
  req(lines.length===T.strict3_source_clauses+1,'DIMACS count');
  req(sha(dimacs)===T.source_sha256&&Buffer.byteLength(dimacs)===T.source_bytes,'source identity');
  for(let i=1;i<lines.length;i++){
    const xs=lines[i].trim().split(/\s+/).map(Number);
    req(xs.length===4&&xs[3]===0,'source row');
    req(same(norm(xs.slice(0,3)),T.trace.sources[i-1].clause),'DIMACS/source mismatch');
  }
  const facets = d => [norm([-d.out,d.a]),norm([-d.out,d.b]),norm([d.out,-d.a,-d.b])];
  const refClause = ref => {
    if(ref.includes('#f')){
      const [o,f]=ref.split('#f'), d=defs.get(o);
      req(!!d&&/^[012]$/.test(f),'facet ref'); return facets(d)[Number(f)];
    }
    req(clause.has(ref),'node ref'); return clause.get(ref);
  };
  const refNode = ref => ref.split('#f')[0];
  let maxVar=T.source_variables, baseD=0,baseR=0,extD=0,extR=0;
  for(const x of T.trace.nodes){
    req(!ids.has(x.id),'duplicate node'); ids.add(x.id);
    if(x.kind==='def'){
      req(Number.isInteger(x.out)&&x.out>maxVar,'fresh DEF');
      req(Math.abs(x.a)<x.out&&Math.abs(x.b)<x.out,'acyclic DEF inputs');
      maxVar=x.out;
      const expectedOwners=[...new Set([x.a,x.b].map(Math.abs).filter(v=>varOwner.has(v)).map(v=>varOwner.get(v)))].sort();
      if(x.id.startsWith('E_D')){
        extD++; req(same(x.input_owners,expectedOwners),'extension input owners');
      }else{
        baseD++;
        const po=x.parent_owner===null?[]:[x.parent_owner];
        req(same(po,expectedOwners),'base parent owner');
      }
      defs.set(x.id,x); varOwner.set(x.out,x.id); clause.set(x.id,null);
      dep.set(x.id,expectedOwners);
      depth.set(x.id,1+Math.max(0,...expectedOwners.map(o=>depth.get(o))));
    }else{
      req(x.kind==='res','known kind');
      const L=refClause(x.left),R=refClause(x.right);
      req(L.includes(x.pivot)&&R.includes(-x.pivot),'oriented pivot');
      const c=norm([...L.filter(v=>v!==x.pivot),...R.filter(v=>v!==-x.pivot)]);
      req(!c.some(v=>c.includes(-v)),'tautological resolvent');
      clause.set(x.id,c); dep.set(x.id,[refNode(x.left),refNode(x.right)]);
      depth.set(x.id,1+Math.max(depth.get(refNode(x.left)),depth.get(refNode(x.right))));
      x.id.startsWith('E_R')?extR++:baseR++;
    }
  }
  req(maxVar===T.final_variables_after_def,'final variable bound');
  req(clause.has(T.final_empty)&&clause.get(T.final_empty).length===0,'final empty clause');
  req(depth.get(T.final_empty)===T.critical_path_full,'full critical path');

  const ell=T.ell,n=2**ell,m=n+1,M=n*m*(m-1)/2;
  const baseDef=m*(2*n-4), sourceRes=M*(2*ell-3);
  let inherited=0;for(let d=3;d<=ell;d++) inherited+=2**d*(d-1);
  const baseRes=sourceRes+m*(2*n-5+inherited)+2*ell*M;
  req(baseD===baseDef&&baseR===baseRes,'base counts');
  req(T.base_pre_php_work===baseD+baseR,'base work');
  const suffixFormula=n*(n+1)*(27*n*n+11*n-14)/24;
  const spanFormula=Math.max(n-1,4*ell-3)+(n-1)*(n+4)/2+2;
  req(extD===T.cook_suffix_def&&extR===T.cook_suffix_res,'suffix counts');
  req(extD+extR===T.cook_suffix_work&&T.cook_suffix_work===suffixFormula&&T.cook_suffix_formula===suffixFormula,'suffix formula');
  req(T.paid_full_refutation_work===T.base_pre_php_work+suffixFormula,'full work');
  req(T.critical_path_full===spanFormula&&T.critical_path_formula===spanFormula,'span formula');
  req(T.stages.length===n-1,'stage count');
  for(let z=0;z<T.stages.length;z++){
    const s=T.stages[z], k=n-1-z;
    req(s.k===k,'stage order');
    req(s.definitions===2*k*(k+1),'stage DEF');
    req(s.resolution===3*k*(k+1)+2*(k+1)**2+9*k*k*(k+1)/2,'stage RES');
    req(s.work===s.definitions+s.resolution,'stage work');
    req(s.alo_outputs.length===k+1,'ALO obligations');
    req(s.collision_outputs.length===k*k*(k+1)/2,'collision obligations');
    for(const a of s.alo_outputs) req(clause.has(a)&&clause.get(a).length===k,'ALO clause');
    for(const c of s.collision_outputs) req(clause.has(c)&&clause.get(c).length===2,'collision clause');
  }
  // Every paid node must lie in the dependency union of the final empty clause.
  const seen=new Set();
  const visit=id=>{if(seen.has(id)||!dep.has(id))return;seen.add(id);for(const p of dep.get(id))visit(p)};
  visit(T.final_empty);
  const paidIds=T.trace.nodes.map(x=>x.id);
  req(paidIds.every(x=>seen.has(x)),'dead paid proof node');
  req(seen.size===paidIds.length+T.trace.sources.length,'all sources and paid nodes reached');
  return {ell:T.ell,work:T.paid_full_refutation_work,span:T.critical_path_full,
          suffix:T.cook_suffix_work,paid:paidIds.length};
}

req(doc.historical_authoritative_checker===false,'scope');
req(doc.full_empty_clause_refutation===true,'complete refutation');
req(doc.lower_bound_transfer===false,'no lower transfer');
const summaries=doc.traces.map(verifyTrace);
req(doc.sat_controls.every(x=>x.satisfies_unary_php&&x.distinct_addresses.length===x.holes),'SAT controls');

let hostile=0;
function mustReject(mut,label){
  const t=structuredClone(doc.traces[0]);mut(t);let bad=false;
  try{verifyTrace(t)}catch{bad=true} req(bad,`hostile accepted ${label}`);hostile++;
}
mustReject(t=>{t.trace.nodes.find(x=>x.kind==='res').pivot+=9999},'pivot');
mustReject(t=>{const x=t.trace.nodes.find(x=>x.id.startsWith('E_D'));x.out=Math.abs(x.a)},'freshness');
mustReject(t=>{const x=t.trace.nodes.find(x=>x.id.startsWith('E_D'));x.input_owners=[]},'owner provenance');
mustReject(t=>{t.trace.nodes[1].id=t.trace.nodes[0].id},'duplicate id');
mustReject(t=>{t.source_sha256='0'.repeat(64)},'source hash');
mustReject(t=>{t.stages[0].collision_outputs.pop()},'omitted AND obligation');
mustReject(t=>{t.final_empty=t.stages.at(-1).alo_outputs[0]},'false final');

console.log(JSON.stringify({status:'COMPUTATIONAL complete declared FACET-A refutations accepted',
  checks,hostile_rejected:hostile,raw_sha256:sha(raw),raw_bytes:raw.length,traces:summaries},null,2));

#!/usr/bin/env node
// Independent no-producer-import verifier, new JS parsing and evaluation.
const fs = require('fs');
const path = require('path');
const base=__dirname;
const raw=JSON.parse(fs.readFileSync(path.join(base,'raw339.json'),'utf8'));
const inputs=JSON.parse(fs.readFileSync(path.join(base,'inputs339.json'),'utf8'));
let witnessCases=0, unsatAssignments=0, relationChecks=0, sourceAuditChecks=0;
function parse(text){
  const rows=text.split(/\r?\n/).map(x=>x.trim()).filter(x=>x && x[0]!=='c');
  let header=rows.shift().split(/\s+/);if(header.length!==4 || header[0]!=='p'|| header[1]!=='cnf')throw Error('bad fixture');
  const n=Number(header[2]),m=Number(header[3]);
  const clauses=[];let next=[];
  for (const row of rows){for (const v of row.split(/\s+/)){
    const l=Number(v);if(l===0){clauses.push(next);next=[];}else next.push(l);
  }}
  if(clauses.length!==m||next.length)throw Error('mismatch');
  return {n,clauses};
}
function litval(l,mask){return ((mask>>(Math.abs(l)-1))&1)===(l>0?1:0);}
function sat(cnf,mask){for(const clause of cnf){let good=false;for(const lit of clause)if(litval(lit,mask)){good=true;break;}if(!good)return false;}return true;}
function witness(cnf,n,skip){for(let a=0;a<(1<<n);a++){
  let ok=true;for(let j=0;j<cnf.length;j++)if(j!==skip && !sat([cnf[j]],a)){ok=false;break;}
  if(ok)return a;
}return null;}
function checkedGuard(cnf,n,srcWitness,x){
  const q=n+1; let guard=[];let mask=srcWitness|(x<<n);
  for(let j=0;j<cnf.length;j++){
    const [a,b,c]=cnf[j],y=n+2+j;
    guard.push([-q,a,y],[-y,b,c]);
    const bit=x===0?0:(litval(a,srcWitness)?0:1);
    mask|=bit<<(n+1+j);
  }
  // JS bitwise shifts wrap at 32; avoid direct full extended masks for W1/Petersen.
  const values=new Map();
  for(let j=1;j<=n;j++)values.set(j,(srcWitness>>(j-1))&1);
  values.set(q,x);
  for(let j=0;j<cnf.length;j++) values.set(n+2+j, x===0?0:(litval(cnf[j][0],srcWitness)?0:1));
  for (const clause of guard){
    if(!clause.some(l => values.get(Math.abs(l))===(l>0?1:0))) throw Error('guard witness failed');
    relationChecks++;
  }
}
for(const r of raw.fixtures){
  const {n,clauses}=parse(inputs[r.fixture]);
  if(n!==r.n || clauses.length!==r.m)throw Error('dimensions');
  let flips=0;
  for(let a=0;a<(1<<n);a++){
    if(sat(clauses,a))throw Error('original SAT');
    unsatAssignments++;
  }
  for(let j=0;j<clauses.length;j++){
    const w=witness(clauses,n,j);
    if(w===null)throw Error('not minimal UNSAT');
    for(let t=0;t<clauses[j].length;t++){
      const modified=clauses.map(c=>c.slice());modified[j][t]=-modified[j][t];
      if(!sat(modified,w))throw Error('neighbor UNSAT');
      checkedGuard(modified,n,w,1);
      flips++;witnessCases++;
    }
  }
  if(flips!==r.L)throw Error('sign count');
  checkedGuard(clauses,n,0,0);
  for(const p of r.two_phase_streaming_cases){
    if(p.compile_distinct_sign_probes!==p.cached_signs ||
        p.query_distinct_sign_probes!==r.L-p.cached_signs ||
        p.combined_distinct_sign_probes!==r.L || p.query_result_x1!==false)
      throw Error('source ledger mismatch');
    sourceAuditChecks++;
  }
}
// Exact separate bitwise family arithmetic plus numeric sanity checks.
const beta=c=>((c+2)/(c*c)-c)/2;
for(const r of raw.resource_math.cases){
  if(Math.abs(beta(r.time_fixed)-r.flmv_beta)>1e-12)throw Error('beta');
  if(Math.abs(r.flmv_beta-r.space_fixed-r.strict_curve_margin)>1e-12)throw Error('margin');
}
if(witnessCases!==396||raw.malformed_rejected!==8)throw Error('missing controls');
console.log(JSON.stringify({status:'PASS',independent_signflip_checks:witnessCases,
  original_complete_assignments_checked:unsatAssignments,
  materialized_guard_clauses_checked:relationChecks,
  independent_stage_ledgers_checked:sourceAuditChecks,
  flmv_numeric_scenarios:raw.resource_math.cases.length}));

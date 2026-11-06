#!/usr/bin/env node
// Independent REFEREE382 verifier; imports neither the Python producer nor its classifications.
'use strict';

import fs from 'node:fs';
import crypto from 'node:crypto';

const tracePath=process.argv[2]||'results/raw/review/2026-11-06_0052_LSPV5_GUARDED_TSEITIN_BOUNDARY381.json';
const auditPath=process.argv[3]||'results/raw/review/2026-11-06_0148_LSPV5_ORIGINAL_COORDINATE_SCOPE382.json';
const traceBytes=fs.readFileSync(tracePath), T=JSON.parse(traceBytes), A=JSON.parse(fs.readFileSync(auditPath));
let checks=0; const ok=(x,m='check')=>{checks++;if(!x)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const canon=x=>Array.isArray(x)?x.map(canon):(x&&typeof x==='object')?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canon(x[k])])):x;
const eq=(x,y)=>JSON.stringify(canon(x))===JSON.stringify(canon(y));
const parity=xs=>xs.reduce((a,b)=>a^b,0);
const lit=(l,M)=>M.get(Math.abs(l))===(l>0);
const norm=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||(a<0?-1:1));

function implication(row,clause){
 const vs=row.vars;
 for(let m=0;m<(1<<vs.length);m++){
  const bits=vs.map((_,i)=>(m>>i)&1);
  if(parity(bits)!==row.rhs)continue;
  const M=new Map(vs.map((v,i)=>[v,Boolean(bits[i])]));
  if(!clause.some(l=>lit(l,M)))return false;
 }
 return true;
}

function verify(trace,audit){
 ok(trace.run==='LSPV-5/REFEREE381','trace run');ok(audit.run==='LSPV-5/REFEREE382','audit run');
 ok(sha(traceBytes)===audit.input_trace_sha256,'trace hash');ok(trace.instances.length===audit.instances.length,'instances');
 let totalA=0,totalL=0;
 for(let ii=0;ii<trace.instances.length;ii++){
  const I=trace.instances[ii], R=audit.instances[ii];
  ok(I.graph===R.graph&&I.vertices===R.h,'identity');
  const sourceMax=Number(/^p cnf (\d+) /m.exec(I.dimacs)[1]);ok(sourceMax===I.source_variables,'header bound');
  const node=new Map(I.trace.nodes.map(n=>[n.id,n])), clauses=new Map(I.trace.sources.map(s=>[s.id,s.clause]));
  const defs=new Map(), factors=new Map(), affine=new Map(), ids=new Set(I.trace.sources.map(s=>s.id));
  const facet=ref=>{const m=/^(N\d+)#f([0-2])$/.exec(ref);if(!m)return null;const d=node.get(m[1]);ok(d?.kind==='DEF','facet owner');return [norm([-d.out,d.a]),norm([-d.out,d.b]),norm([d.out,-d.a,-d.b])][Number(m[2])]};
  const clause=ref=>ref.includes('#f')?facet(ref):clauses.get(ref);
  const truth=(ref,M)=>{const c=clause(ref);if(c)return c.some(l=>lit(l,M));const f=factors.get(ref);let m=0;f.support.forEach((v,i)=>{if(M.get(v))m|=1<<i});return f.sats.has(m)};
  const support=ref=>{const c=clause(ref);if(c)return [...new Set(c.map(Math.abs))];return factors.get(ref).support};
  const badA=[],badL=[];
  for(const n of I.trace.nodes){
   ok(!ids.has(n.id),'unique');ids.add(n.id);
   if(n.kind==='DEF'){
    ok(n.out>sourceMax&&!defs.has(n.out),'fresh def');defs.set(n.out,n.id);
   }else if(n.kind==='RES'){
    const x=clause(n.left),y=clause(n.right);ok(x&&y&&x.includes(n.pivot)&&y.includes(-n.pivot),'oriented RES');
    const z=norm([...x.filter(v=>v!==n.pivot),...y.filter(v=>v!==-n.pivot)]);ok(!z.some(v=>z.includes(-v))&&eq(z,n.clause),'RES exact');clauses.set(n.id,z);
   }else if(n.kind==='AND3'){
    const sup=[...new Set([...support(n.left),...support(n.right)])].sort((a,b)=>a-b);ok(eq(sup,n.support)&&sup.length<=3,'AND3 support');
    const sats=new Set();for(let m=0;m<(1<<sup.length);m++){const M=new Map(sup.map((v,i)=>[v,Boolean((m>>i)&1)]));if(truth(n.left,M)&&truth(n.right,M))sats.add(m)}
    factors.set(n.id,{support:sup,sats});
    if(n.affine){ok(eq(n.affine.vars,sup),'AND affine vars');for(let m=0;m<(1<<sup.length);m++)ok(sats.has(m)===(parity(sup.map((_,i)=>(m>>i)&1))===n.affine.rhs),'AND affine exact');affine.set(n.id,n.affine)}
    ok(sup.every(v=>defs.has(v)),'381 AND3 not all DEF coordinates');badA.push({id:n.id,support:sup,all_fresh_def_outputs:true,wire_support_legal:true,original_support_legal:false});
   }else if(n.kind==='XOR'){
    const x=affine.get(n.left),y=affine.get(n.right);ok(x&&y,'XOR parents');const xs=new Set(x.vars),ys=new Set(y.vars),vars=[...new Set([...x.vars,...y.vars])].filter(v=>xs.has(v)!==ys.has(v)).sort((a,b)=>a-b);const z={vars,rhs:x.rhs^y.rhs};ok(eq(z,n.affine),'XOR exact');affine.set(n.id,z);
   }else if(n.kind==='LOCAL'){
    const row=affine.get(n.parent);ok(row&&row.vars.length===3&&implication(row,n.clause),'LOCAL implication');ok(row.vars.every(v=>defs.has(v)),'381 LOCAL not all DEF coordinates');clauses.set(n.id,n.clause);badL.push({id:n.id,parent:n.parent,support:row.vars,all_fresh_def_outputs:true,wire_support_legal:true,original_support_legal:false});
   }else throw Error('kind '+n.kind);
  }
  ok(badA.length===3*(I.vertices-1)&&badL.length===4,'bad counts');
  ok(eq(badA,R.and3_original_scope_rejections)&&eq(badL,R.local_original_scope_rejections),'audit lists');
  ok(R.rejection_count===badA.length+badL.length&&!R.original_coordinate_grammar_accepts_trace&&R.wire_grammar_accepts_affected_nodes,'classification');
  totalA+=badA.length;totalL+=badL.length;
 }
 ok(eq(audit.totals,{instances:3,and3_original_scope_rejections:totalA,local_original_scope_rejections:totalL,all_original_scope_rejections:totalA+totalL}),'totals');
 for(const [name,c] of Object.entries(audit.controls)){
  ok(implication(c.affine,c.implied_clause),'control implication '+name);const orig=c.affine.vars.every(v=>v<=c.source_max);ok(c.wire_legal===true&&c.original_legal===orig,'control scope '+name);
 }
 return true;
}

verify(T,A);
const attacks=[];
function hostile(name,mut){const t=structuredClone(T),a=structuredClone(A);mut(t,a);let rejected=false;try{verify(t,a)}catch{rejected=true}ok(rejected,'hostile accepted '+name);attacks.push(name)}
hostile('inflate claimed source bound',(t)=>{t.instances[0].source_variables=t.instances[0].final_variables});
hostile('forge DEF freshness',(t)=>{t.instances[0].trace.nodes.find(n=>n.kind==='DEF').out=t.instances[0].source_variables});
hostile('wrong AND3 support',(t)=>{t.instances[0].trace.nodes.find(n=>n.kind==='AND3').support[0]=1});
hostile('unsound LOCAL clause',(t)=>{const n=t.instances[0].trace.nodes.find(n=>n.kind==='LOCAL');n.clause=[n.clause[0]]});
hostile('LOCAL wrong parent type',(t)=>{const n=t.instances[0].trace.nodes.find(n=>n.kind==='LOCAL');n.parent=t.instances[0].trace.nodes.find(n=>n.kind==='RES').id});
hostile('omit rejection witness',(_,a)=>{a.instances[0].and3_original_scope_rejections.pop()});
hostile('false original acceptance',(_,a)=>{a.instances[0].original_coordinate_grammar_accepts_trace=true});
hostile('corrupt source hash',(_,a)=>{a.input_trace_sha256='0'.repeat(64)});

console.log(JSON.stringify({status:'PASS',checks,hostile_rejected:attacks.length,trace_sha256:sha(traceBytes),rejections:A.instances.map(x=>x.rejection_count),totals:A.totals,scope:'dual declared-grammar audit; no authoritative historical checker executed'},null,2));

#!/usr/bin/env node
'use strict';
// Independent, source-reconstructing strict RES-DAG verifier.
// Does not implement or pretend to be R_mix341 historical byte checker.
const fs=require('fs'), path=require('path'),crypto=require('crypto'),assert=require('assert');
const HERE=__dirname;
let checks=0;
const ok=(cond,msg)=>{assert(cond,msg);checks++};
function canonical(arr){
  ok(Array.isArray(arr),'not array');
  for(const l of arr) ok(Number.isSafeInteger(l)&&l!==0,'bad literal');
  const u=[...new Set(arr)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
  for(const x of u) ok(!u.includes(-x),'tautology');
  return u;
}
function fmt(a){return JSON.stringify(a)}
function parseCNF(text){
  const ls=text.trim().split(/\r?\n/);
  const head=ls.shift();ok(/^p cnf \d+ \d+$/.test(head),'bad header');
  const [, ,nv,nc]=head.split(' ');const vars=+nv, count=+nc;
  ok(ls.length===count,'wrong clause count');
  let source=[];
  for(const ln of ls){
    ok(/^[-\d\s]+$/.test(ln),'invalid byte');
    const a=ln.trim().split(/\s+/).map(Number);
    ok(a.at(-1)===0 && a.slice(0,-1).every(x=>x!==0),'bad terminator');
    const c=canonical(a.slice(0,-1));
    ok(c.length===3,'must be proper 3CNF');
    ok(c.every(l=>Math.abs(l)<=vars),'variable header');
    source.push(c);
  }
  return {vars,source,count};
}
function rebuild(neighbors){
  let n=0; const edge=new Map(),source=[];
  const e=(i,j)=>edge.get(i+','+j);
  for(let i=0;i<neighbors.length;i++) for(const j of neighbors[i]) edge.set(i+','+j,++n);
  for(let i=0;i<neighbors.length;i++){
    const lits=neighbors[i].map(j=>e(i,j)); const d=lits.length;
    if(d===3){source.push(canonical(lits));continue;}
    const y=[];for(let k=0;k<d-3;k++) y.push(++n);
    source.push(canonical([lits[0],lits[1],y[0]]));
    for(let k=1;k<y.length;k++)source.push(canonical([-y[k-1],lits[k+1],y[k]]));
    source.push(canonical([-y.at(-1),lits.at(-2),lits.at(-1)]));
  }
  for(let i=0;i<neighbors.length;i++)for(let k=i+1;k<neighbors.length;k++){
    const common=neighbors[i].filter(j=>neighbors[k].includes(j)).sort((a,b)=>a-b);
    for(const j of common){n++;source.push(canonical([-e(i,j),-e(k,j),n]));
      source.push(canonical([-e(i,j),-e(k,j),-n]));}
  }
  return {n,source};
}
function check(cert,raw){
  const cnf=parseCNF(raw);
  ok(cert.vars===cnf.vars,'vars');ok(cert.source_count===cnf.source.length,'source count');
  ok(fmt(cert.original_clauses)===fmt(cnf.source),'source JSON not identical to file');
  ok(crypto.createHash('sha256').update(raw).digest('hex')===cert.original_dimacs_sha256,'hash');
  const original=rebuild(cert.neighbors);
  ok(original.n===cert.vars,'graph num vars');
  ok(fmt(original.source)===fmt(cnf.source),'source clauses not graph-authentic');
  const holes=new Set(cert.neighbors.flat());
  ok(cert.pigeons===cert.neighbors.length && cert.holes===holes.size,'kernel dimensions');
  ok(cert.pigeons>cert.holes,'no Hall deficit');
  ok(cert.neighbors.every(a=>a.length>=3&&new Set(a).size===a.length),'incorrect degree');
  const E=cert.neighbors.reduce((s,a)=>s+a.length,0); const R=cert.neighbors.reduce((s,a)=>s+a.length-3,0);
  let cs=[...cnf.source], spans=Array(cs.length).fill(0),nPadding=0,nRow=0;
  for(const s of cert.paid_steps){
    ok(s.id===cs.length,'nonconsecutive paid node id');
    ok(s.a>=0 && s.b>=0 && s.a<s.id && s.b<s.id,'bad premises / cycle');
    const a=cs[s.a],b=cs[s.b];
    ok(a.includes(s.pivot)&&b.includes(-s.pivot),'bad oriented pivot');
    const res=canonical([...a,...b].filter(x=>x!==s.pivot&&x!==-s.pivot));
    ok(fmt(res)===fmt(s.clause),'bad resolvent');
    cs.push(res);spans.push(1+Math.max(spans[s.a],spans[s.b]));
    if(s.pivot>E+R)nPadding++;
    else if(s.pivot>E)nRow++;
  }
  ok(cert.root===cs.length-1,'root must be last');
  ok(cs[cert.root].length===0,'root must be empty');
  ok(cert.paid_steps.length===cert.paid_nodes,'paid mismatch');
  ok(cert.padding_eliminations===nPadding,'padding count');
  ok(cert.pigeon_row_eliminations===nRow,'row recovery count');
  ok(cert.branch_resolution===cert.paid_nodes-nPadding-nRow,'branch count');
  ok(cert.span===spans[cert.root],'span');
  ok(cert.paid_nodes<=cert.theorem_upper_bound,'theorem bound');
  // Every paid inference is an actual ancestor of the empty clause.
  const seen=new Set();function visit(i){if(i<cnf.count||seen.has(i))return;seen.add(i);const s=cert.paid_steps[i-cnf.count];visit(s.a);visit(s.b)}
  visit(cert.root);ok(seen.size===cert.paid_nodes,'unreachable paid work');
  return {fixture:cert.fixture,original:cnf.count,paid:cert.paid_nodes,span:cert.span};
}
const results=[];
for(const name of ['hall5_4','four_on_three','hall6_5','degree4_hall6_5']){
  const cert=JSON.parse(fs.readFileSync(path.join(HERE,name+'.json'),'utf8'));
  const source=fs.readFileSync(path.join(HERE,name+'.cnf'),'utf8');
  results.push(check(cert,source));
  function mustFail(change,reason){const clone=JSON.parse(JSON.stringify(cert));change(clone);let failed=false;
    try{check(clone,source);}catch(e){failed=true};ok(failed,'hostile control accepted '+reason)}
  mustFail(c=>{c.root=c.root-1},'nonempty root');
  mustFail(c=>{c.paid_steps[0].pivot=-c.paid_steps[0].pivot},'wrong pivot sign');
  mustFail(c=>{c.paid_steps[0].clause[0]=123456},'forged resolvent');
  mustFail(c=>{c.original_clauses[0][0]*=-1},'foreign signed source');
  mustFail(c=>{c.original_dimacs_sha256='0'.repeat(64)},'corrupt original hash');
  mustFail(c=>{c.paid_steps[1].a=c.paid_steps[1].id},'forward reference');
  mustFail(c=>{c.paid_steps.push(c.paid_steps[0])},'duplicate/unreachable node');
  mustFail(c=>{c.neighbors[0][0]=999},'source graph corruption');
  mustFail(c=>{c.pigeons=c.holes},'no Hall deficit');
  for(const [tag,txt] of [['bad-head',source.replace(/^p cnf/, 'p sat')],
     ['bad-var',source.replace(/p cnf \d+ /,'p cnf 1 ')],
     ['bad-terminator',source.replace(' 0\n',' 1\n')],
     ['truncated',source.slice(0,source.lastIndexOf('\n',source.length-2)+1)]]){
    let failed=false;try{parseCNF(txt)}catch(e){failed=true};ok(failed,'malformed '+tag)
  }
}
// SAT control independently proved by enumerating injections into 4 holes.
const satGraph=[[0,1,2],[0,1,3],[0,2,3],[1,2,3]];
let inject=0;for(let a of satGraph[0])for(let b of satGraph[1])for(let c of satGraph[2])for(let d of satGraph[3])if(new Set([a,b,c,d]).size===4)inject++;
ok(inject>0,'SAT control failure');
fs.writeFileSync(path.join(HERE,'node_verify.json'),JSON.stringify({status:'PASS',checks,results,sat_injective_witnesses:inject,hostile_controls:52},null,2)+'\n');
console.log(JSON.stringify({status:'PASS',checks,results,sat_injective_witnesses:inject,hostile_controls:52},null,2));

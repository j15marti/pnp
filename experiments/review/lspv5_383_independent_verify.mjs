#!/usr/bin/env node
// Independent verifier for REFEREE383. It imports neither producer code nor classifications.
'use strict';

import fs from 'node:fs';
import crypto from 'node:crypto';

const tracePath=process.argv[2]||'results/raw/review/2026-11-06_0248_LSPV5_ORIGINAL_COORDINATE_RECOVERY383.json';
const inputPath=process.argv[3]||'results/raw/review/2026-11-06_0052_LSPV5_GUARDED_TSEITIN_BOUNDARY381.json';
const D=JSON.parse(fs.readFileSync(tracePath));
const inputBytes=fs.readFileSync(inputPath), I=JSON.parse(inputBytes);
let checks=0; const ok=(x,m='check')=>{checks++;if(!x)throw Error(m)};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const canon=x=>Array.isArray(x)?x.map(canon):(x&&typeof x==='object')?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canon(x[k])])):x;
const eq=(x,y)=>JSON.stringify(canon(x))===JSON.stringify(canon(y));
const norm=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||(a<0?-1:1));
const lit=(l,A)=>Boolean(A[Math.abs(l)-1])===(l>0);
const clauseTrue=(c,A)=>c.some(l=>lit(l,A));
const parity=xs=>xs.reduce((a,b)=>a^b,0);

function parseDimacs(text){
 const lines=text.split(/\n/), clauses=[]; let vars=null,count=null,seen=false;
 for(const raw of lines){const s=raw.trim();if(!s)continue;
  if(s.startsWith('c'))continue;
  if(!seen){const m=/^p cnf (\d+) (\d+)$/.exec(s);if(!m)return null;vars=Number(m[1]);count=Number(m[2]);seen=true;continue}
  const tok=s.split(/\s+/);if(tok.at(-1)!=='0')return null;const xs=tok.slice(0,-1).map(Number);
  if(xs.some(x=>!Number.isSafeInteger(x)||x===0||Math.abs(x)>vars))return null;clauses.push(norm(xs));
 }
 return seen&&vars>=0&&count===clauses.length?{vars,clauses}:null;
}

function verify(doc,input){
 ok(doc.run==='LSPV-5/REFEREE383','run');ok(input.run==='LSPV-5/REFEREE381','input run');
 ok(sha(inputBytes)===doc.input_trace_sha256,'input hash');ok(doc.instances.length===input.instances.length,'instance count');
 for(let ii=0;ii<doc.instances.length;ii++){
  const X=doc.instances[ii], O=input.instances[ii];
  ok(X.graph===O.graph&&X.h===O.vertices,'identity');ok(X.dimacs===O.dimacs,'exact source bytes');
  ok(X.source_sha256===sha(Buffer.from(X.dimacs))&&X.source_sha256===O.source_sha256,'source sha');
  const parsed=parseDimacs(X.dimacs);ok(parsed&&parsed.vars===X.source_variables&&parsed.clauses.length===X.source_clauses,'dimacs');
  ok(eq(X.sources,O.trace.sources),'source records');
  const clause=new Map(X.sources.map(s=>[s.id,norm(s.clause)])), factor=new Map(), affine=new Map();
  const deps=new Map(X.sources.map(s=>[s.id,[]])), depth=new Map(X.sources.map(s=>[s.id,0])), ids=new Set(X.sources.map(s=>s.id));
  const conditionSupport=ref=>clause.has(ref)?[...new Set(clause.get(ref).map(Math.abs))].sort((a,b)=>a-b):factor.get(ref).support;
  const conditionValue=(ref,A)=>{if(clause.has(ref))return clauseTrue(clause.get(ref),A);const f=factor.get(ref);let mask=0;f.support.forEach((v,i)=>{if(A[v-1])mask|=1<<i});return Boolean(f.truth[mask])};
  for(const n of X.nodes){
   ok(!ids.has(n.id),'unique id');ids.add(n.id);
   if(n.kind==='RES'){
    const a=clause.get(n.left),b=clause.get(n.right);ok(a&&b&&a.includes(n.pivot)&&b.includes(-n.pivot),'oriented res');
    const z=norm([...a.filter(x=>x!==n.pivot),...b.filter(x=>x!==-n.pivot)]);ok(!z.some(x=>z.includes(-x))&&eq(z,n.clause),'exact resolvent');clause.set(n.id,z);
    deps.set(n.id,[n.left,n.right]);depth.set(n.id,1+Math.max(depth.get(n.left),depth.get(n.right)));
   }else if(n.kind==='AND3'){
    const support=[...new Set([...conditionSupport(n.left),...conditionSupport(n.right)])].sort((a,b)=>a-b);
    ok(eq(support,n.support)&&support.length>0&&support.length<=3,'and support');ok(support.every(v=>v>=1&&v<=X.source_variables)&&n.original_coordinate_legal===true,'original coords');
    const truth=[];for(let m=0;m<(1<<support.length);m++){const A=Array(X.source_variables).fill(0);support.forEach((v,i)=>A[v-1]=(m>>i)&1);truth.push(Number(conditionValue(n.left,A)&&conditionValue(n.right,A)))}
    ok(eq(truth,n.truth),'truth table');factor.set(n.id,{support,truth});
    if(n.affine){ok(eq(n.affine.vars,support),'affine vars');for(let m=0;m<(1<<support.length);m++)ok(Boolean(truth[m])===(parity(support.map((_,i)=>(m>>i)&1))===n.affine.rhs),'affine exact');affine.set(n.id,n.affine)}
    deps.set(n.id,[n.left,n.right]);depth.set(n.id,1+Math.max(depth.get(n.left),depth.get(n.right)));
   }else if(n.kind==='XOR'){
    const a=affine.get(n.left),b=affine.get(n.right);ok(a&&b,'xor typed');const av=new Set(a.vars),bv=new Set(b.vars);const row={vars:[...new Set([...a.vars,...b.vars])].filter(v=>av.has(v)!==bv.has(v)).sort((x,y)=>x-y),rhs:a.rhs^b.rhs};ok(eq(row,n.affine),'xor exact');affine.set(n.id,row);
    deps.set(n.id,[n.left,n.right]);depth.set(n.id,1+Math.max(depth.get(n.left),depth.get(n.right)));
   }else throw Error('unexpected kind '+n.kind);
  }
  ok(eq(affine.get(X.root),{vars:[],rhs:1})&&eq(X.root_affine,{vars:[],rhs:1}),'root contradiction');
  const counts={RES:X.nodes.filter(n=>n.kind==='RES').length,AND3:X.nodes.filter(n=>n.kind==='AND3').length,XOR:X.nodes.filter(n=>n.kind==='XOR').length};
  ok(eq(counts,X.counts)&&counts.RES===8*X.h+3&&counts.AND3===3*X.h&&counts.XOR===X.h-1,'counts');
  ok(X.work===X.nodes.length&&X.work===12*X.h+2&&X.known_binary_source_floor===8*X.h+3,'work envelope');
  ok(depth.get(X.root)===X.span&&X.span<=X.span_bound,'span');
  ok(eq(X.uses,['RES','AND3','XOR'])&&eq(X.excludes,['DEF','LOCAL','SPLIT','DISCHARGE','WEAKENING']),'rule set');
  const live=new Set(),stack=[X.root];while(stack.length){const x=stack.pop();if(live.has(x))continue;live.add(x);stack.push(...deps.get(x))}
  ok(X.all_sources_and_nodes_live&&X.sources.every(s=>live.has(s.id))&&X.nodes.every(n=>live.has(n.id)),'liveness');
  ok(X.deletion_witnesses.length===X.sources.length,'deletion count');
  const bySource=new Map(X.sources.map(s=>[s.id,s.clause]));
  for(const w of X.deletion_witnesses){ok(bySource.has(w.deleted)&&w.assignment.length===X.source_variables,'deletion shape');ok(!clauseTrue(bySource.get(w.deleted),w.assignment),'deleted false');for(const s of X.sources)if(s.id!==w.deleted)ok(clauseTrue(s.clause,w.assignment),'remaining source true')}
  const E=X.even_charge_control, witness=Array(X.source_variables).fill(0);for(const [k,v] of Object.entries(E.witness))witness[Number(k)-1]=v;
  ok(E.clauses.length===X.source_clauses&&E.clauses.every(c=>clauseTrue(c,witness)),'even SAT control');
 }
 ok(doc.malformed_controls.length===8&&doc.malformed_controls.every(x=>parseDimacs(x.text)===null),'malformed controls');
 return true;
}

verify(D,I);
const attacks=[];
function hostile(name,mut){const d=structuredClone(D),i=structuredClone(I);mut(d,i);let rejected=false;try{verify(d,i)}catch{rejected=true}ok(rejected,'hostile accepted '+name);attacks.push(name)}
hostile('wrong RES pivot',d=>{d.instances[0].nodes.find(n=>n.kind==='RES').pivot=1});
hostile('corrupt source',d=>{d.instances[0].sources[0].clause=[1]});
hostile('wire-coordinate AND3',d=>{const x=d.instances[0];const n=x.nodes.find(n=>n.kind==='AND3');n.support[0]=x.source_variables+1});
hostile('wrong AND truth',d=>{const n=d.instances[0].nodes.find(n=>n.kind==='AND3');n.truth[0]^=1});
hostile('wrong affine rhs',d=>{const n=d.instances[0].nodes.find(n=>n.kind==='AND3'&&n.affine);n.affine.rhs^=1});
hostile('wrong XOR row',d=>{const n=d.instances[0].nodes.find(n=>n.kind==='XOR');n.affine.vars.push(999)});
hostile('omit source witness',d=>{d.instances[0].deletion_witnesses.pop()});
hostile('false root',d=>{d.instances[0].root_affine={vars:[],rhs:0}});

console.log(JSON.stringify({status:'PASS',checks,hostile_rejected:attacks.length,input_sha256:sha(inputBytes),instances:D.instances.map(x=>({graph:x.graph,h:x.h,work:x.work,span:x.span,deletions:x.deletion_witnesses.length})),scope:'independent rule-level /341 reconstruction; no authoritative historical byte checker executed'},null,2));

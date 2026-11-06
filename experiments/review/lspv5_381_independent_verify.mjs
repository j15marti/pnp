#!/usr/bin/env node
// Independent REFEREE381 verifier.  Does not import the Python producer.
'use strict';

import fs from 'node:fs';
import crypto from 'node:crypto';

const path=process.argv[2]||'results/raw/review/2026-11-06_0052_LSPV5_GUARDED_TSEITIN_BOUNDARY381.json';
const original=JSON.parse(fs.readFileSync(path,'utf8'));
let checks=0;
const ck=(x,m='check')=>{checks++;if(!x)throw Error(m)};
const norm=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||(a<0?-1:1));
const canonical=x=>Array.isArray(x)?x.map(canonical):(x&&typeof x==='object')?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const eq=(a,b)=>JSON.stringify(canonical(a))===JSON.stringify(canonical(b));
const parity=a=>a.reduce((x,y)=>x^y,0);
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
const lit=(l,A)=>A.get(Math.abs(l))===(l>0);
const proper=c=>c.length===3&&new Set(c.map(Math.abs)).size===3&&!c.some(x=>c.includes(-x));
const dimacs=(v,cs)=>`p cnf ${v} ${cs.length}\n${cs.map(c=>c.join(' ')+' 0').join('\n')}\n`;
const bits3=()=>{const z=[];for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++)z.push([a,b,c]);return z};

function graph(name){
 if(name==='K4')return [4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]];
 if(name==='K33'){const e=[];for(let u=0;u<3;u++)for(let v=3;v<6;v++)e.push([u,v]);return[6,e]}
 if(name==='cube'){const e=[];for(let u=0;u<8;u++)for(const b of [1,2,4]){const v=u^b;if(u<v)e.push([u,v])}return[8,e]}
 throw Error('graph');
}

function verify(doc){
 ck(doc.run==='LSPV-5/REFEREE381','run');
 ck(doc.historical_authoritative_checker===false,'scope');
 ck(doc.instances.length===3,'instances');
 for(const I of doc.instances){
  const [h,edges]=graph(I.graph), m=edges.length, g=m+1;
  ck(I.vertices===h&&eq(I.edges,edges),'graph exact');
  ck(eq(I.charges,[1,...Array(h-1).fill(0)]),'charges');
  ck(m*2===3*h,'cubic');
  const inc=Array.from({length:h},()=>[]);
  edges.forEach(([u,v],k)=>{inc[u].push(k+1);inc[v].push(k+1)});
  ck(inc.every(x=>x.length===3),'degree');
  const sourceMap=new Map(), ids=new Set(), deps=new Map(), clauses=new Map();
  const expected=[];let y=g+1;
  for(let v=0;v<h;v++)for(const b of bits3().filter(z=>parity(z)!==I.charges[v])){
   const bs=b.join(''), ls=inc[v].map((x,j)=>b[j]?-x:x);
   expected.push({id:`S${v}_${bs}_0`,clause:norm([g,ls[0],y]),meta:{vertex:v,wrong:b,side:0}});
   expected.push({id:`S${v}_${bs}_1`,clause:norm([-y,ls[1],ls[2]]),meta:{vertex:v,wrong:b,side:1}});y++;
  }
  const p=y,q=y+1,sourceMax=q;
  for(let s=0;s<2;s++)for(let t=0;t<2;t++)expected.push({id:`P${s}${t}`,clause:norm([-g,s?-p:p,t?-q:q]),meta:{pad:[s,t]}});
  ck(I.source_variables===sourceMax,'source max');
  ck(I.source_clauses===8*h+4&&I.trace.sources.length===expected.length,'source count');
  ck(eq(I.trace.sources,expected),'exact original source');
  for(const s of I.trace.sources){ck(proper(s.clause),'proper source');ck(!ids.has(s.id),'source id');ids.add(s.id);sourceMap.set(s.id,s);clauses.set(s.id,s.clause);deps.set(s.id,[])}
  const text=dimacs(sourceMax,I.trace.sources.map(s=>s.clause));
  ck(text===I.dimacs,'dimacs');ck(Buffer.byteLength(text)===I.source_bytes,'source bytes');ck(sha(text)===I.source_sha256,'source hash');

  // Independently check odd UNSAT and even SAT at the underlying Tseitin level.
  let oddModels=0,evenModels=0;
  for(let mask=0;mask<(1<<m);mask++){
   const row=inc.map(es=>parity(es.map(e=>(mask>>(e-1))&1)));
   if(eq(row,I.charges))oddModels++;
   if(row.every(x=>x===0))evenModels++;
  }
  ck(oddModels===0,'odd source label');
  ck(evenModels===(1<<(m-h+1)),'even model count');

  // Independently rebuild and validate the even-charge guarded counterpart.
  const EC=I.even_charge_control, ecs=[];y=g+1;
  for(let v=0;v<h;v++)for(const b of bits3().filter(z=>parity(z)===1)){
   const ls=inc[v].map((x,j)=>b[j]?-x:x);
   ecs.push(norm([g,ls[0],y]),norm([-y,ls[1],ls[2]]));y++;
  }
  for(let s=0;s<2;s++)for(let t=0;t<2;t++)ecs.push(norm([-g,s?-p:p,t?-q:q]));
  ck(eq(EC.charges,Array(h).fill(0))&&eq(EC.clauses,ecs),'even source exact');
  ck(sha(dimacs(sourceMax,ecs))===EC.source_sha256,'even hash');
  const WA=new Map(Object.entries(EC.witness).map(([k,v])=>[Number(k),Boolean(v)]));
  ck(ecs.every(c=>c.some(l=>lit(l,WA))),'even witness');

  const nodeById=new Map(), factor=new Map(), affine=new Map(), ownerByVar=new Map();
  const facet=ref=>{
   const mm=/^(N\d+)#f([0-2])$/.exec(ref);if(!mm)return null;
   const d=nodeById.get(mm[1]);ck(d&&d.kind==='DEF','facet owner');
   const [w,a,b]=[d.out,d.a,d.b];return [norm([-w,a]),norm([-w,b]),norm([w,-a,-b])][Number(mm[2])];
  };
  const clause=ref=>ref.includes('#f')?facet(ref):clauses.get(ref);
  const base=ref=>ref.split('#f')[0];
  const supportOf=ref=>{
   const c=clause(ref);if(c)return new Set(c.map(Math.abs));
   const f=factor.get(ref);if(f)return new Set(f.support);
   throw Error('support ref '+ref);
  };
  const factorTruth=(ref,A)=>{
   const c=clause(ref);if(c)return c.some(l=>lit(l,A));
   const f=factor.get(ref);let mask=0;f.support.forEach((v,i)=>{if(A.get(v))mask|=1<<i});return f.sats.has(mask);
  };
  for(const n of I.trace.nodes){
   ck(!ids.has(n.id),'duplicate id');ids.add(n.id);nodeById.set(n.id,n);
   if(n.kind==='DEF'){
    ck(n.out>sourceMax&&n.out<=I.final_variables,'def range');ck(!ownerByVar.has(n.out),'fresh def');
    ck(n.a===-g&&n.b===n.edge&&n.edge>=1&&n.edge<=m,'def relation');ownerByVar.set(n.out,n.id);deps.set(n.id,[]);
   }else if(n.kind==='RES'){
    const a=clause(n.left),b=clause(n.right);ck(a&&b,'res refs');ck(a.includes(n.pivot)&&b.includes(-n.pivot),'oriented pivot');
    const c=norm([...a.filter(x=>x!==n.pivot),...b.filter(x=>x!==-n.pivot)]);ck(!c.some(x=>c.includes(-x)),'tautology');ck(eq(c,n.clause),'res clause');clauses.set(n.id,c);deps.set(n.id,[base(n.left),base(n.right)]);
   }else if(n.kind==='AND3'){
    ck(ids.has(base(n.left))&&ids.has(base(n.right)),'and refs');const sup=[...new Set([...supportOf(n.left),...supportOf(n.right)])].sort((a,b)=>a-b);
    ck(eq(sup,n.support)&&sup.length<=3,'and support');const sats=new Set();
    for(let mask=0;mask<(1<<sup.length);mask++){const A=new Map(sup.map((v,i)=>[v,Boolean((mask>>i)&1)]));if(factorTruth(n.left,A)&&factorTruth(n.right,A))sats.add(mask)}
    factor.set(n.id,{support:sup,sats});deps.set(n.id,[base(n.left),base(n.right)]);
    if(n.affine){ck(eq(n.affine.vars,sup),'aff vars');for(let mask=0;mask<(1<<sup.length);mask++){const good=parity(sup.map((v,i)=>(mask>>i)&1))===n.affine.rhs;ck(sats.has(mask)===good,'aff exact')}affine.set(n.id,n.affine)}
   }else if(n.kind==='XOR'){
    const a=affine.get(n.left),b=affine.get(n.right);ck(a&&b,'xor rows');const av=new Set(a.vars),bv=new Set(b.vars),vars=[...new Set([...a.vars,...b.vars])].filter(v=>av.has(v)!==bv.has(v)).sort((x,y)=>x-y);const z={vars,rhs:a.rhs^b.rhs};ck(eq(z,n.affine),'xor exact');affine.set(n.id,z);deps.set(n.id,[n.left,n.right]);
   }else if(n.kind==='LOCAL'){
    const a=affine.get(n.parent);ck(a,'local parent');ck(n.clause.every(l=>a.vars.includes(Math.abs(l))),'local support');for(let mask=0;mask<(1<<a.vars.length);mask++){const vals=a.vars.map((v,i)=>(mask>>i)&1);if(parity(vals)===a.rhs){const A=new Map(a.vars.map((v,i)=>[v,Boolean(vals[i])]));ck(n.clause.some(l=>lit(l,A)),'local implication')}}clauses.set(n.id,n.clause);deps.set(n.id,[n.parent]);
   }else throw Error('kind '+n.kind);
  }
  ck(I.trace.nodes.length===I.paid_nodes&&I.paid_nodes===51*h/2+6&&I.paid_formula===I.paid_nodes,'work formula');
  const counts={};for(const n of I.trace.nodes)counts[n.kind]=(counts[n.kind]||0)+1;
  ck(counts.DEF===3*h/2,'def count');ck(counts.AND3===3*(h-1),'and count');ck(counts.XOR===h-2,'xor count');ck(counts.LOCAL===4,'local count');
  const bd=affine.get(I.trace.nodes.find(n=>n.kind==='XOR'&&eq(n.affine,I.boundary_equation))?.id)||I.boundary_equation;
  const boundaryVars=inc[0].map(e=>[...ownerByVar.entries()].find(([,id])=>nodeById.get(id).edge===e)[0]).sort((a,b)=>a-b);
  ck(eq(I.boundary_equation,{vars:boundaryVars,rhs:0}),'boundary row');
  ck(eq(clauses.get(I.unit_g),[g]),'unit g');ck(eq(clauses.get(I.final_empty),[]),'empty');
  const live=new Set(),stack=[I.final_empty];while(stack.length){const x=stack.pop();if(live.has(x))continue;live.add(x);for(const y of deps.get(x)||[])stack.push(y)}
  ck(I.trace.sources.every(x=>live.has(x.id)),'all sources live');ck(I.trace.nodes.every(x=>live.has(x.id)),'all paid live');ck(I.all_sources_and_nodes_live===true,'live flag');
 }
 return true;
}

verify(original);
const attacks=[];
function hostile(name,mut){const d=structuredClone(original);mut(d);let rejected=false;try{verify(d)}catch{rejected=true}ck(rejected,'hostile accepted '+name);attacks.push(name)}
hostile('wrong resolution pivot',d=>d.instances[0].trace.nodes.find(n=>n.kind==='RES').pivot++);
hostile('corrupt original source',d=>d.instances[0].trace.sources[0].clause[0]*=-1);
hostile('nonfresh definition',d=>d.instances[0].trace.nodes.find(n=>n.kind==='DEF').out=d.instances[0].source_variables);
hostile('wrong AND3 affine row',d=>d.instances[0].trace.nodes.find(n=>n.kind==='AND3'&&n.affine).affine.rhs^=1);
hostile('wrong XOR row',d=>d.instances[0].trace.nodes.find(n=>n.kind==='XOR').affine.rhs^=1);
hostile('unsound LOCAL clause',d=>d.instances[0].trace.nodes.find(n=>n.kind==='LOCAL').clause=[d.instances[0].boundary_equation.vars[0]]);
hostile('omitted AND source',d=>d.instances[0].trace.sources.pop());
hostile('false final root',d=>d.instances[0].final_empty=d.instances[0].unit_g);

console.log(JSON.stringify({
 status:'COMPUTATIONAL complete declared semantic-R_mix341 candidate DAGs accepted',
 checks,hostile_rejected:attacks.length,
 raw_sha256:sha(fs.readFileSync(path)),raw_bytes:fs.statSync(path).size,
 instances:original.instances.map(x=>({graph:x.graph,h:x.vertices,sources:x.source_clauses,paid:x.paid_nodes,final:x.final_empty}))
},null,2));

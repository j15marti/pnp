'use strict';
// LSPV-3/562: archived /386 signed guard restriction to independent /341-source RES/DEF reference certificate.
// Original /386 and /341 verifiers are NOT the missing full R_mix341 checker.
const fs=require('fs'),crypto=require('crypto'),assert=require('assert'),cp=require('child_process');

function req(v,m){if(!v)throw new Error(m)}
function eq(a,b){return JSON.stringify(a)===JSON.stringify(b)}
function norm(c){req(Array.isArray(c)&&c.every(x=>Number.isSafeInteger(x)&&x!==0),'bad literal type');let v=[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);req(!v.some(x=>v.includes(-x)),'tautology');return v}
function k(c){return norm(c).join(',')}
function project(B,F){
 const t=B.spec.guard,h=B.spec.h,old=B.records,out=[],map=[],omitted=[];
 req(h===F.graph.n&&t===F.graph.edges.length+1,'graph or guard mismatch');
 req(eq(B.spec.edges,F.graph.edges)&&eq(B.spec.charge,F.charges),'signed graph/charge mismatch');
 req(F.clauses.length===4*h,'/341 source cardinality'); 
 const a=F.clauses.map(x=>x.vertex+':'+k(x.literals)).sort();
 const bs=old.filter(x=>x.kind==='SOURCE');
 req(bs.length===4*h+1,'/386 source cardinality');
 req(bs.filter(x=>x.source===-1&&eq(x.c,[t])).length===1,'guard unit');
 req(eq(bs.filter(x=>x.source>=0).map(x=>x.source+':'+k(x.c.filter(y=>y!==-t))).sort(),a),'exact signed guard projection fails');
 for(let i=0;i<old.length;i++){
  const r=old[i],c=r.c.includes(t)?null:norm(r.c.filter(x=>x!==-t));
  if(r.kind==='SOURCE'&&c===null){map.push(null);omitted.push({old:i,reason:'guard-unit'});continue}
  if(r.kind==='SOURCE'||r.kind==='DEF'){
   req(c!==null,'unexpected source or facet true');
   map.push(out.length);out.push({...r,c});continue;
  }
  req(r.kind==='RES','unexpected native rule '+r.kind);
  if(c===null){map.push(null);omitted.push({old:i,reason:'true-resolvent'});continue}
  if(Math.abs(r.pivot)===t){
   const aliasOld=old[r.parents[0]].c.includes(t)?r.parents[1]:r.parents[0];
   req(map[aliasOld]!==null&&eq(out[map[aliasOld]].c,c),'guard-resolution alias mismatch '+i);
   map.push(map[aliasOld]);omitted.push({old:i,reason:'guard-resolution-alias',to:map[aliasOld]});continue;
  }
  const pp=r.parents.map(j=>map[j]);req(pp.every(x=>Number.isInteger(x)),'lost non-guard parent '+i);
  const A=out[pp[0]].c,H=out[pp[1]].c,p=r.pivot;
  req(A.includes(p)&&H.includes(-p),'lost RES pivot');
  req(eq(c,norm([...A.filter(x=>x!==p),...H.filter(x=>x!==-p)])),'lost RES conclusion');
  map.push(out.length);out.push({...r,c,parents:pp});
 }
 const counts={source:out.filter(x=>x.kind==='SOURCE').length,def_views:out.filter(x=>x.kind==='DEF').length,resolution:out.filter(x=>x.kind==='RES').length,paid_gates:B.gate_defs.length,live_records:out.length};
 counts.paid_total=counts.resolution+counts.paid_gates;
 return {language:'SIGNED-SOURCE-DEF-RES-RESTRICTED-PROJECTION-NONNATIVE/v1',original_source_sha256:'861b38239ec08050a7b38b3da04fd79c17d43624a8f755be5a1417d8f01745c8',archived_checker_386_blob:'338305c0ce101704205e57543756b8127074a986',archived_checker_341_blob:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',source_guard:t,gate_defs:B.gate_defs,records:out,summary:counts,source_map:map,omitted};
}
function replay(P,F){
 req(P.language==='SIGNED-SOURCE-DEF-RES-RESTRICTED-PROJECTION-NONNATIVE/v1','wrong language');
 req(P.original_source_sha256==='861b38239ec08050a7b38b3da04fd79c17d43624a8f755be5a1417d8f01745c8','wrong bound source hash');
 const expected=F.clauses.map(x=>x.vertex+':'+k(x.literals)).sort();
 req(P.records.filter(x=>x.kind==='SOURCE').length===expected.length,'source count');
 req(eq(P.records.filter(x=>x.kind==='SOURCE').map(x=>x.source+':'+k(x.c)).sort(),expected),'wrong source');
 const defs=new Map(),gids=new Set();
 for(const [id,z,a,b] of P.gate_defs){
  req([id,z,a,b].every(Number.isSafeInteger),'bad gate');
  req(!gids.has(id)&&!defs.has(z)&&z>F.graph.edges.length&&z!==P.source_guard,'gate nonfresh');
  req([a,b].every(x=>x!==0&&(Math.abs(x)<=F.graph.edges.length||defs.has(Math.abs(x)))),'bad gate inputs');
  gids.add(id);defs.set(z,{id,views:[[-z,a],[-z,b],[z,-a,-b]].map(k)});
 }
 let nres=0,nfac=0,clauses=[],sources=new Set();
 for(let i=0;i<P.records.length;i++){
  const r=P.records[i],c=norm(r.c);req(eq(c,r.c),'noncanonical clause '+i);
  req(Array.isArray(r.parents)&&r.parents.every(j=>Number.isInteger(j)&&j>=0&&j<i),'parent order '+i);
  if(r.kind==='SOURCE'){
   req(r.parents.length===0,'source parents');const label=r.source+':'+k(c);
   req(expected.includes(label)&&!sources.has(label),'source mismatch '+i);sources.add(label);
  }else if(r.kind==='DEF'){
   nfac++;req(r.parents.length===0&&gids.has(r.gate),'facet owner '+i);
   const z=P.gate_defs.find(x=>x[0]===r.gate)[1];req(defs.get(z).views.includes(k(c)),'facet invalid '+i);
  }else if(r.kind==='RES'){
   nres++;req(r.parents.length===2&&Number.isInteger(r.pivot)&&r.pivot!==0,'RES arity/pivot');
   const [A,H]=r.parents.map(j=>clauses[j]),p=r.pivot;
   req(A.includes(p)&&H.includes(-p),'pivot signs '+i);
   req(eq(c,norm([...A.filter(x=>x!==p),...H.filter(x=>x!==-p)])),'wrong resolvent '+i);
  }else throw new Error('unknown rule '+r.kind);
  req(c.every(x=>Math.abs(x)<=F.graph.edges.length||defs.has(Math.abs(x))),'undefined wire');
  clauses.push(c);
 }
 const sc=P.summary;
 req(sc.source===expected.length&&sc.def_views===nfac&&sc.resolution===nres&&sc.paid_gates===defs.size&&sc.paid_total===nres+defs.size&&sc.live_records===P.records.length,'bad paid or record count');
 req(clauses.length>0&&eq(clauses.at(-1),[]),'no empty sink');
 const ancestors=new Set();function anc(i){if(ancestors.has(i))return;ancestors.add(i);for(const x of P.records[i].parents)anc(x)}
 anc(P.records.length-1);
 req(P.records.filter((r,i)=>r.kind==='SOURCE'&&!ancestors.has(i)).length===0,'dead source');
 const liveFacets=P.records.filter((r,i)=>r.kind==='DEF'&&ancestors.has(i)).length;
 req(liveFacets>=2,'facet not live');
 return {paid:sc.paid_total,records:sc.live_records,source:sc.source,resolution:sc.resolution,liveFacets,allSourcesLive:true};
}

const aPath='results/raw/arc/2026-11-10_2124_LSPV3_561_ARCHIVED_386_NATIVE_PACKET.json',bPath='results/raw/arc/2026-11-10_2212_LSPV2_549_DUAL_NATIVE_POLYGLOT_PACKET.json';
function gitBlob(buf){return crypto.createHash('sha1').update(Buffer.from('blob '+buf.length+'\0')).update(buf).digest('hex')}
const ab=fs.readFileSync(aPath),bb=fs.readFileSync(bPath);
assert.strictEqual(gitBlob(ab),'d0fa96a155672f8f6a6a3428eacafa15e79b9e88');assert.strictEqual(gitBlob(bb),'b9c1d306c300a3f1917ee01ecab16358ac77d4de');
const B=JSON.parse(ab),F=JSON.parse(bb).fixtures[0];
const source='p cnf '+F.graph.edges.length+' '+F.clauses.length+'\n'+F.clauses.map(x=>x.literals.join(' ')+' 0').join('\n')+'\n';
assert.strictEqual(Buffer.byteLength(source),163);
assert.strictEqual(crypto.createHash('sha256').update(source).digest('hex'),'861b38239ec08050a7b38b3da04fd79c17d43624a8f755be5a1417d8f01745c8');
const P=project(B,F),verdict=replay(P,F);
const changes=[['bad-source',x=>x.records.find(r=>r.kind==='SOURCE').c[0]*=-1],['bad-gate-view',x=>x.records.find(r=>r.kind==='DEF').c[0]*=-1],['wrong-pivot',x=>x.records.at(-1).pivot=99],['future-parent',x=>x.records.at(-1).parents[0]=x.records.length],['undercharged',x=>x.summary.paid_total--],['missing-owner',x=>x.gate_defs=[]],['duplicate-owner',x=>x.gate_defs.push([...x.gate_defs[0]])],['wrong-source-id',x=>x.records.find(r=>r.kind==='SOURCE').source=99],['wrong-source-hash',x=>x.original_source_sha256='0'.repeat(64)],['wrong-sink',x=>x.records.at(-1).c=[1]]];
const rejected=[];for(const [name,mut] of changes){let z=structuredClone(P),error='';mut(z);try{replay(z,F)}catch(e){error=e.message}assert.ok(error,'hostile accepted: '+name);rejected.push({name,error})}
const original=[];
for(const [checker,file] of [['experiments/arc/lspv2_386_independent_verify.js',aPath],['experiments/arc/lspv2_341_independent_verify.js',bPath]]){const q=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8'});assert.strictEqual(q.status,0,checker+' original checker rejected: '+q.stderr);original.push({checker,status:q.status,stdout:q.stdout.trim()})}
const packet=JSON.stringify(P,null,2)+'\n';fs.writeFileSync('results/raw/arc/2026-11-10_2224_LSPV3_562_PROJECTED_SIGNED_K4_REFERENCE.json',packet);
const raw={...{"original_386_blob":"d0fa96a155672f8f6a6a3428eacafa15e79b9e88","original_549_polyglot_blob":"b9c1d306c300a3f1917ee01ecab16358ac77d4de","source_341_count":16,"source_386_count":17,"guard":7,"original_paid":50,"projected":{"paid":34,"records":52,"source":16,"resolution":33,"liveFacets":2,"allSourcesLive":true},"omitted":[{"old":16,"reason":"guard-unit"},{"old":22,"reason":"guard-resolution-alias","to":0},{"old":23,"reason":"guard-resolution-alias","to":20},{"old":24,"reason":"guard-resolution-alias","to":2},{"old":25,"reason":"guard-resolution-alias","to":3},{"old":26,"reason":"guard-resolution-alias","to":4},{"old":27,"reason":"guard-resolution-alias","to":5},{"old":28,"reason":"guard-resolution-alias","to":6},{"old":29,"reason":"guard-resolution-alias","to":7},{"old":30,"reason":"guard-resolution-alias","to":8},{"old":31,"reason":"guard-resolution-alias","to":9},{"old":32,"reason":"guard-resolution-alias","to":10},{"old":33,"reason":"guard-resolution-alias","to":11},{"old":34,"reason":"guard-resolution-alias","to":12},{"old":35,"reason":"guard-resolution-alias","to":13},{"old":36,"reason":"guard-resolution-alias","to":14},{"old":37,"reason":"guard-resolution-alias","to":15}],"negative_controls":[{"name":"bad-source","error":"wrong source"},{"name":"bad-gate-view","error":"facet invalid 16"},{"name":"wrong-pivot","error":"pivot signs 51"},{"name":"future-parent","error":"parent order 51"},{"name":"undercharged","error":"bad paid or record count"},{"name":"missing-owner","error":"facet owner 16"},{"name":"duplicate-owner","error":"gate nonfresh"},{"name":"wrong-source-id","error":"wrong source"},{"name":"wrong-source-hash","error":"wrong bound source hash"},{"name":"wrong-sink","error":"wrong resolvent 51"}],"parser_status":"independent restriction/replay, NOT an original R_mix341 native accepted certificate","runtime":"core executed in V8 code-mode JS isolate; prior /561 and /549 original-checker acceptance reused without new native checker reexecution"},original_node_subprocesses:original,independent_negative_controls:rejected,projected_packet_sha256:crypto.createHash('sha256').update(packet).digest('hex')};
fs.writeFileSync('results/raw/arc/2026-11-10_2224_LSPV3_562_GUARD_PROJECTION_RAW.json',JSON.stringify(raw,null,2)+'\n');
console.log(JSON.stringify({verdict,original,negative_controls:rejected.length,packet_sha256:raw.projected_packet_sha256}));

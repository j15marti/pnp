'use strict';
// LSPV-2/565: executable REFERENCE per-step cost abstraction.
// Original archived /386 checker is always called as an unchanged OS subprocess.
// This is not an authoritative R_mix341 mixed-rule checker.
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const os=require('node:os'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checker='experiments/arc/lspv2_386_independent_verify.js';
const seedPath='results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json';
const sourcePath='results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf';
const pins={
 [checker]:'338305c0ce101704205e57543756b8127074a986',
 [seedPath]:'318c52d99977ea4e91bc8554051138a700c1dc94',
 [sourcePath]:'e8bc4300f1f4518cb447edaf3f699bcee4839803'
};
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const blob=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
const copy=x=>structuredClone(x), val=x=>JSON.stringify(x);
const key=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const clean=c=>Array.isArray(c)&&c.every(x=>Number.isSafeInteger(x)&&x!==0)
 && !c.some(x=>c.includes(-x))&&val(c)===val(key(c));
function sourceClauses(raw){
 const toks=raw.trim().split(/\s+/);assert.deepEqual(toks.slice(0,2),['p','cnf']);
 const n=Number(toks[2]),m=Number(toks[3]);assert(Number.isInteger(n)&&Number.isInteger(m));
 let curr=[],out=[];for(const tok of toks.slice(4)){
  assert(/^-?\d+$/.test(tok));const lit=Number(tok);
  assert(Number.isSafeInteger(lit)&&Math.abs(lit)<=n);
  if(lit===0){curr=key(curr);assert(clean(curr));out.push(curr);curr=[];}else curr.push(lit);
 }
 assert(curr.length===0&&out.length===m);return {n,clauses:out};
}
function sourceBind(packet,raw){
 const parsed=sourceClauses(raw);assert(parsed.n===packet.spec.guard);
 const tally=xs=>{const t=new Map();for(const c of xs){
  assert(clean(c));const k=val(c);t.set(k,(t.get(k)||0)+1);
 }return [...t].sort((a,b)=>a[0].localeCompare(b[0]));};
 assert.deepEqual(tally(packet.records.filter(r=>r.kind==='SOURCE').map(r=>r.c)),
  tally(parsed.clauses),'independent original source is different');
 return hash(Buffer.from(raw));
}
function costSummary(q){const r=q.records;
 const nr=r.filter(v=>v.kind==='RES').length;
 return {source:r.filter(v=>v.kind==='SOURCE').length,def_views:r.filter(v=>v.kind==='DEF').length,
  resolution:nr,paid_gates:q.gate_defs.length,paid_total:nr+q.gate_defs.length,live_records:r.length};
}
function referenceReplay(p,raw){
 const source_sha256=sourceBind(p,raw),owners=new Map(),paidIDs=new Set();
 for(const [id,z,a,b] of p.gate_defs){
  assert(Number.isSafeInteger(id)&&!paidIDs.has(id)&&Number.isSafeInteger(z)
   &&z>p.spec.edges.length&&z!==p.spec.guard&&!owners.has(z));
  for(const x of [a,b])assert(x!==0&&Math.abs(x)!==p.spec.guard&&
   (Math.abs(x)<=p.spec.edges.length||owners.has(Math.abs(x))));
  paidIDs.add(id);owners.set(z,{id,views:[[-z,a],[-z,b],[z,-a,-b]].map(key).filter(clean).map(val)});
 }
 const prior=[],values=new Set(),trace=[];let W=p.gate_defs.length,Walpha=W,maxspan=0;
 p.records.forEach((r,i)=>{
  assert(clean(r.c)&&Array.isArray(r.parents)&&r.parents.every(j=>Number.isInteger(j)&&j>=0&&j<i));
  const k=val(r.c);let physical=0,abstract=0,span=0,ports=null;
  if(r.kind==='SOURCE'){assert(r.parents.length===0);}
  else if(r.kind==='DEF'){assert(r.parents.length===0&&[...owners.values()].some(o=>o.id===r.gate&&o.views.includes(k)));}
  else if(r.kind==='RES'){
   assert(r.parents.length===2&&Number.isInteger(r.pivot)&&r.pivot!==0);
   const [a,b]=r.parents.map(j=>prior[j].c),z=r.pivot;
   assert(a.includes(z)&&b.includes(-z),'signed port');
   assert(clean(key([...a.filter(x=>x!==z),...b.filter(x=>x!==-z)])));
   assert(val(key([...a.filter(x=>x!==z),...b.filter(x=>x!==-z)]))===k,'resolvent');
   physical=1;abstract=values.has(k)?0:1;ports=[[r.parents[0],z],[r.parents[1],-z]];
   span=1+Math.max(...r.parents.map(j=>prior[j].span));maxspan=Math.max(maxspan,span);
  }else throw Error('unsupported archived /386 opcode: '+r.kind);
  for(const lit of r.c)assert(Math.abs(lit)<=p.spec.edges.length||Math.abs(lit)===p.spec.guard||owners.has(Math.abs(lit)));
  W+=physical;Walpha+=abstract;prior.push({c:r.c,span});values.add(k);
  trace.push({i,kind:r.kind,ports,physical,abstract,span});
 });
 assert(prior.length&&prior.at(-1).c.length===0&&p.records.at(-1).kind==='RES');
 assert.deepEqual(p.summary,costSummary(p));assert(Walpha<=W);
 return {source_sha256,W,Walpha,records:prior.length,distinct_signed_values:values.size,span:maxspan,trace};
}
function duplicate(p){
 const q=copy(p),last=q.records.at(-1),slot=last.parents.findIndex(i=>q.records[i].kind==='RES');
 assert(slot>=0);const old=last.parents[slot],at=q.records.length-1;
 q.records.splice(at,0,copy(q.records[old]));q.records.at(-1).parents[slot]=at;
 q.summary=costSummary(q);return q;
}
function contract(q){
 const p=copy(q),oldToNew=new Map(),firstValue=new Map(),out=[];
 for(let i=0;i<p.records.length;i++){
  const r=p.records[i],k=val(r.c);
  if(r.kind==='RES'&&i<p.records.length-1&&firstValue.has(k)){
   oldToNew.set(i,firstValue.get(k));continue;
  }
  const next=copy(r);next.parents=r.parents.map(j=>{assert(oldToNew.has(j));return oldToNew.get(j)});
  oldToNew.set(i,out.length);if(!firstValue.has(k))firstValue.set(k,out.length);
  out.push(next);
 }
 p.records=out;p.summary=costSummary(p);return p;
}
for(const [file,expected] of Object.entries(pins)){
 const actual=blob(fs.readFileSync(path.join(root,file)));assert.equal(actual,expected,file+' Git blob mismatch');
}
const seed=JSON.parse(fs.readFileSync(path.join(root,seedPath),'utf8'));
const raw=fs.readFileSync(path.join(root,sourcePath),'utf8');
const dup=duplicate(seed),reduced=contract(dup);
assert.equal(val(reduced),val(seed),'concrete reconstruction');
const scratch=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-565-'));const cases=[];
function test(label,p,source,expectNative,expectReference){
 const bytes=Buffer.from(val(p)+'\n'),file=path.join(scratch,label+'.json');
 fs.writeFileSync(file,bytes);
 const result=cp.spawnSync(process.execPath,[path.join(root,checker),file],{encoding:'utf8',timeout:30000});
 const accepted=result.status===0&&!result.error;
 assert.equal(accepted,expectNative,label+' original checker '+result.stderr);
 let a=null,err=null;try{a=referenceReplay(p,source);}catch(e){err=String(e.message);}
 assert.equal(!!a,expectReference,label+' reference '+err);
 const original=accepted?JSON.parse(result.stdout):null;
 cases.push({label,native:accepted,reference:!!a,bytes:bytes.length,sha256:hash(bytes),
  W:a?.W??null,Walpha:a?.Walpha??null,assertions:original?.assertions??null,error:err});
 return {bytes,a};
}
try{
 const base=test('base',seed,raw,true,true),extra=test('duplicate',dup,raw,true,true);
 test('coalesced',reduced,raw,true,true);
 assert.equal(extra.a.W,base.a.W+1);assert.equal(extra.a.Walpha,base.a.Walpha);
 const idx=dup.records.findIndex(r=>r.kind==='RES'),paired=copy(dup);
 paired.records[idx].parents.reverse();paired.records[idx].pivot*=-1;
 test('paired_ports',paired,raw,true,true);
 const pivot=copy(dup);pivot.records[idx].pivot*=-1;test('pivot_only',pivot,raw,false,false);
 const swap=copy(dup);swap.records[idx].parents.reverse();test('swap_only',swap,raw,false,false);
 const under=copy(dup);under.summary.paid_total--;test('underpaid',under,raw,false,false);
 const forged=copy(dup);forged.records[0].c=[-seed.spec.guard];test('forged_source',forged,raw,false,false);
 const removed=sourceClauses(raw);removed.clauses.pop();
 const wrong='p cnf '+removed.n+' '+removed.clauses.length+'\n'+removed.clauses.map(c=>c.join(' ')+' 0\n').join('');
 test('external_missing_clause',dup,wrong,true,false);
 const unknown=copy(dup);unknown.records[17].kind='AND3';
 test('unknown_AND3_in_sibling',unknown,raw,false,false);
 const summary={id:'LSPV-2/565',authority:'unchanged archived /386 CLI via native OS Node; independent reference interpreter',
 checker_git_blob:pins[checker],seed_git_blob:pins[seedPath],source_git_blob:pins[sourcePath],
 source_sha256:base.a.source_sha256,baseline:{W:base.a.W,Walpha:base.a.Walpha},
 duplicate:{W:extra.a.W,Walpha:extra.a.Walpha},exact_reconstruction:val(reduced)===val(seed),
 cases,totals:{count:cases.length,accepted:cases.filter(c=>c.native).length,
 rejected:cases.filter(c=>!c.native).length,assertions:cases.reduce((s,c)=>s+(c.assertions||0),0)},
 open:['P2-D1','P2-C3','P2-B1','P2-B2/B3']};
 const dir=path.join(root,'results/raw/arc');fs.mkdirSync(dir,{recursive:true});
 fs.writeFileSync(path.join(dir,'2026-11-11_1412_LSPV2_565_ALPHA_ORIGINAL_OS_RESULTS.json'),val(summary)+'\n');
 fs.writeFileSync(path.join(dir,'2026-11-11_1412_LSPV2_565_ACCEPTED_DUPLICATE.json'),extra.bytes);
 console.log(val(summary.totals));
}finally{fs.rmSync(scratch,{recursive:true,force:true});}

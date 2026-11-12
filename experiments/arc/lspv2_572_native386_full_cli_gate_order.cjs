#!/usr/bin/env node
'use strict';
// LSPV-2/572. Original archived /386 checker is invoked UNMODIFIED in OS children.
// The source-bound certificate producer and order-enumerator are an audit harness,
// not the historical R_mix341 dispatcher or a replacement checker.
const fs=require('fs'),path=require('path'),crypto=require('crypto'),assert=require('assert');
const {spawnSync}=require('child_process');
const root=path.resolve(__dirname,'../..');
const pin=(p,sha)=>{const s=fs.readFileSync(path.join(root,p));const blob=crypto.createHash('sha1').update('blob '+s.length+'\0').update(s).digest('hex');assert.equal(blob,sha,'Git blob drift: '+p);return s};
const sha256=s=>crypto.createHash('sha256').update(s).digest('hex');
const checker='experiments/arc/lspv2_386_independent_verify.js';
const seedPath='results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json';
const sourcePath='results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf';
const cb=pin(checker,'338305c0ce101704205e57543756b8127074a986');
const seed=JSON.parse(pin(seedPath,'318c52d99977ea4e91bc8554051138a700c1dc94'));
const source=pin(sourcePath,'e8bc4300f1f4518cb447edaf3f699bcee4839803').toString('utf8');
const sorted=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const clauses=source.trim().split(/\r?\n/).slice(1).map(l=>l.split(/\s+/).map(Number).slice(0,-1));
const originals=seed.records.filter(r=>r.kind==='SOURCE').map(r=>r.c);
assert.deepEqual(clauses,originals,'external signed original-source mismatch');
assert.equal(seed.summary.paid_total,29);assert.equal(sha256(source),'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c');
const canonicalOwners=[[0,8,1,4],[1,9,2,5],[2,10,8,3],[3,11,9,-6],[4,12,10,11]];
const expectedEdges=[[0,2],[1,3],[2,4],[3,4]];
const deps=new Map(canonicalOwners.map(([id,z,a,b])=>[id,canonicalOwners.filter(([j,w])=>Math.abs(a)===w||Math.abs(b)===w).map(x=>x[0])]));
assert.deepEqual([...deps.entries()],[[0,[]],[1,[]],[2,[0]],[3,[1]],[4,[2,3]]]);
const workDir=path.join(root,'results/raw/arc/572_cases');fs.mkdirSync(workDir,{recursive:true});
function construct(order){
 const d=structuredClone(seed);
 d.gate_defs=order.map(i=>canonicalOwners[i]);
 const facets=canonicalOwners.map(([id,z,a])=>({kind:'DEF',gate:id,c:sorted([-z,a]),parents:[]}));
 const shift=facets.length,nsrc=d.summary.source;
 d.records=[...d.records.slice(0,nsrc),...facets,...d.records.slice(nsrc).map(r=>({...r,parents:r.parents.map(j=>j>=nsrc?j+shift:j)}))];
 d.summary={...d.summary,def_views:facets.length,paid_gates:5,paid_total:33,live_records:d.records.length};
 return d;
}
function permutations(xs){if(xs.length===0)return [[]];return xs.flatMap((v,i)=>permutations(xs.filter((_,j)=>i!==j)).map(rest=>[v,...rest]));}
function isTopological(order){let seen=new Set();for(let id of order){if(!deps.get(id).every(v=>seen.has(v)))return false;seen.add(id)}return true;}
function run(label,d,expect){const bytes=Buffer.from(JSON.stringify(d)+'\n');const file=path.join(workDir,label+'.json');fs.writeFileSync(file,bytes);let p=spawnSync(process.execPath,[path.join(root,checker),file],{encoding:'utf8',timeout:9000,maxBuffer:1024*1024});const ok=p.status===0;
 if(ok!==expect)throw Error('native checker mismatch '+label+': '+(p.stderr||p.stdout));
 const stdout=ok?JSON.parse(p.stdout.trim()):null;
 return {label,expected:expect?'ACCEPT':'REJECT',native:ok?'ACCEPT':'REJECT',order:d.gate_defs.map(x=>x[0]),sha256:sha256(bytes),bytes:bytes.length,work:ok?stdout.paid:null,assertions:ok?stdout.assertions:null,negativeTests:ok?stdout.negativeTests:null,reject:ok?null:(p.stderr||p.stdout).trim().slice(0,250)};}
let entries=[];
for(const order of permutations([0,1,2,3,4])){const legal=isTopological(order),code=order.join('');entries.push(run('owner_order_'+code,construct(order),legal));}
// Controls: independent roots may be exchanged; a consumer may not precede producer.
// Additional adversarial exact-byte packets preserve all unrelated source/proof fields.
const good=construct([0,1,2,3,4]);
const bads=[
 ['facet_wrong',d=>{d.records[18].c=[-9,1]}],
 ['source_forged',d=>{d.records[0].c=[-1,2,3,-7]}],
 ['pivot_wrong',d=>{d.records.at(-1).pivot=1}],
 ['cost_underpay',d=>{d.summary.paid_total--}],
 ['guard_input',d=>{d.gate_defs[0][2]=d.spec.guard}],
 ['duplicate_owner_id',d=>{d.gate_defs[1][0]=0}],
 ['missing_owner',d=>{d.gate_defs.pop()}],
 ['future_dependency',d=>{d.gate_defs[0][2]=12}],
 ['unsupported_AND3_in_386_only',d=>{d.records[17].kind='AND3'}],
 ['unsupported_LOCAL_CONVERT_in_386_only',d=>{d.records[17].kind='LOCAL-CONVERT'}],
 ];
for(const [name,mut] of bads){const d=structuredClone(good);mut(d);entries.push(run('negative_'+name,d,false));}
const valid=entries.filter(x=>x.native==='ACCEPT');const falseNegatives=entries.filter(x=>x.expected!==x.native);
assert.equal(entries.length,130);assert.equal(valid.length,6);assert.equal(falseNegatives.length,0);
assert(valid.every(x=>x.work===33));
// Source and proof-derivation identities are invariant across all 120 packets.
const sourceProofSHA=sha256(Buffer.from(JSON.stringify({spec:seed.spec,records:seed.records,summary_source:seed.summary.source})));
const compact={id:'LSPV2-572-FULL-CLI-GATE-ORDER',originalChecker:{path:checker,gitBlob:'338305c0ce101704205e57543756b8127074a986'},seed:{path:seedPath,gitBlob:'318c52d99977ea4e91bc8554051138a700c1dc94'},independentSource:{path:sourcePath,sha256:sha256(source),sourceRows:clauses.length},sourceProofSHA,ownerGraph:expectedEdges,owners:canonicalOwners,counts:{permutations:120,positive:6,negativeOrderings:114,hostileRejections:bads.length,nativeTotal:entries.length,assertions:valid.reduce((s,x)=>s+x.assertions,0),builtInNegativeTests:valid.reduce((s,x)=>s+x.negativeTests,0),allExpected:true},cases:entries};
const rawPath=path.join(root,'results/raw/arc/2026-11-12_0312_LSPV2_572_NATIVE386_FULL_CLI_OWNER_ORDER_RAW.json');fs.writeFileSync(rawPath,JSON.stringify(compact,null,2)+'\n');
// Published positive and negative exact certificate bytes retained independently.
for(const [from,to] of [['owner_order_01234','2026-11-12_0312_LSPV2_572_ACCEPTED_TOPOLOGICAL_01234.json'],['owner_order_10324','2026-11-12_0312_LSPV2_572_ACCEPTED_TOPOLOGICAL_10324.json'],['owner_order_40123','2026-11-12_0312_LSPV2_572_REJECTED_FORWARD_40123.json']]){
 fs.copyFileSync(path.join(workDir,from+'.json'),path.join(root,'results/raw/arc',to));
}
console.log(JSON.stringify({id:compact.id,counts:compact.counts,source:compact.independentSource,sourceProofSHA,positiveHashes:valid.slice(0,2).map(x=>({order:x.order,sha256:x.sha256,bytes:x.bytes})),rawPath:path.relative(root,rawPath)},null,2));

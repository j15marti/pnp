#!/usr/bin/env node
'use strict';
/*
 LSPV-3/587: native /386 source-bound semantic-constant gate CEGAR discriminator.
 Run from any directory: node experiments/arc/lspv3_587_semantic_gate_alias_cegar.cjs [raw-output.json]
 This invokes the unchanged pinned original /386 checker in separate real Node OS subprocesses.
 It does not purport to implement the unlocated full R_mix341 parser.
*/
const fs=require('node:fs'), path=require('node:path'), os=require('node:os');
const cp=require('node:child_process'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedPath=path.join(root,'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json');
const srcPath=path.join(root,'results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf');
const blob=b=>crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const pin=(path_,expected)=>{const b=fs.readFileSync(path_);assert.equal(blob(b),expected,path_+' original blob mismatch');return b;};
pin(checker,'338305c0ce101704205e57543756b8127074a986');
const seedBytes=pin(seedPath,'318c52d99977ea4e91bc8554051138a700c1dc94');
const sourceBytes=pin(srcPath,'e8bc4300f1f4518cb447edaf3f699bcee4839803');
const seed=JSON.parse(seedBytes), copy=x=>structuredClone(x);
assert.equal(seed.summary.paid_total,29);assert.equal(seed.records.length,45);
const signed=sourceBytes.toString('utf8').trim().split(/\r?\n/).slice(1)
 .map(line=>line.trim().split(/\s+/).map(Number).slice(0,-1));
assert.deepEqual(signed,seed.records.filter(r=>r.kind==='SOURCE').map(r=>r.c), 'independent signed source');
function gate(x){const p=copy(seed);p.gate_defs[0]=[0,8,x,-x];return p;}
const A=gate(1),B=gate(2);
const evalLit=(lit,mask)=> (lit>0 ? Boolean(mask&(1<<(lit-1))) : !Boolean(mask&(1<<(-lit-1))));
for(let mask=0;mask<64;mask++){
 assert.equal(evalLit(1,mask)&&evalLit(-1,mask),false);
 assert.equal(evalLit(2,mask)&&evalLit(-2,mask),false);
}
const views=(z,a,b)=>[[-z,a],[-z,b],[z,-a,-b]]
  .map(c=>[...new Set(c)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y))
  .filter(c=>!c.some(x=>c.includes(-x))).map(c=>JSON.stringify(c)).sort();
const nativeFacetA=views(8,1,-1), nativeFacetB=views(8,2,-2);
assert.deepEqual(nativeFacetA,['[-1,-8]','[1,-8]']);
assert.deepEqual(nativeFacetB,['[-2,-8]','[2,-8]']);
assert(nativeFacetA.every(x=>!nativeFacetB.includes(x)));
function prependFacet(d,c,gateId=0){
 const q=copy(d);
 q.records=q.records.map(r=>({...r,parents:r.parents.map(j=>j+1)}));
 q.records.unshift({kind:'DEF',gate:gateId,c,parents:[]});
 q.summary.def_views++;q.summary.live_records++;
 return q;
}
// An intentionally incomplete abstraction: retains source, signed proof DAG,
// owner identity/output, paid work, and the COMPLETE Boolean truth-function
// of the paid gate, but forgets its native defining-operand and facet signature.
function semanticAlpha(d){
 const g=d.gate_defs[0];let tt='';for(let m=0;m<64;m++)tt+=Number(evalLit(g[2],m)&&evalLit(g[3],m));
 return JSON.stringify({spec:d.spec,records:d.records,summary:d.summary,
    ownerId:g[0],output:g[1],functionTruthTable:tt});
}
assert.equal(semanticAlpha(A),semanticAlpha(B),'semantic alpha should merge distinct owners');
function refinedAlpha(d){return semanticAlpha(d)+'|facet-signature='+views(...d.gate_defs[0].slice(1)).join(';');}
assert.notEqual(refinedAlpha(A),refinedAlpha(B),'refinement must separate');
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-587-'));
const results=[];
function replay(label,p,expect){
 const input=Buffer.from(JSON.stringify(p)+'\n');const file=path.join(temp,label+'.json');
 fs.writeFileSync(file,input);
 const proc=cp.spawnSync(process.execPath,[checker,file],{cwd:root,encoding:'utf8',timeout:15000,maxBuffer:4*1024*1024});
 const accepted=proc.status===0&&!proc.error;
 assert.equal(accepted,expect,label+' expected='+expect+' actual='+accepted+' '+proc.stderr);
 let native=null;
 if(accepted){native=JSON.parse(proc.stdout.trim().split(/\r?\n/).at(-1));
  assert.equal(native.paid,29);assert.equal(native.def,1);assert.equal(native.res,28);
  assert.equal(native.sources,17);assert.equal(native.negativeTests,11);
 }
 results.push({label,accepted,expected:expect,bytes:input.length,sha256:sha(input),
   assertions:native?.assertions??null,nativeNegativeControls:native?.negativeTests??null,
   paid:native?.paid??null,source:native?.sources??null,records:native?.records??null,
   failure:accepted?null:String(proc.error||proc.stderr).trim().split(/\r?\n/)[0],
   exitCode:proc.status});
 return input;
}
let specimen;
try{
 replay('base_x_and_not_x',A,true);
 replay('base_y_and_not_y',B,true);
 specimen=replay('native_facet_x_accepts_x',prependFacet(A,[1,-8]),true);
 replay('native_facet_y_accepts_y',prependFacet(B,[2,-8]),true);
 replay('cross_facet_x_rejected_under_y',prependFacet(B,[1,-8]),false);
 replay('cross_facet_y_rejected_under_x',prependFacet(A,[2,-8]),false);
 replay('semantic_implied_unit_not_native_x',prependFacet(A,[-8]),false);
 replay('semantic_implied_unit_not_native_y',prependFacet(B,[-8]),false);
 replay('foreign_owner',prependFacet(A,[1,-8],1),false);
 replay('foreign_defining_literal',prependFacet(A,[3,-8]),false);
 let p=prependFacet(A,[1,-8]);p.summary.paid_total=28;replay('underpaid',p,false);
 p=prependFacet(A,[1,-8]);p.records[0].parents=[1];replay('forward_parent',p,false);
 p=prependFacet(A,[1,-8]);p.records[1].c[0]=-1;replay('source_forgery',p,false);
 p=prependFacet(A,[1,-8]);p.records[0].kind='LOCAL-CONVERT';replay('foreign_rule',p,false);
 const positives=results.filter(r=>r.accepted).length,rejects=results.filter(r=>!r.accepted).length;
 assert.equal(positives,4);assert.equal(rejects,10);
 const report={
  id:'LSPV-3/587',status:'PROVED/RESTRICTED original-code theorem + COMPUTATIONAL real original OS replay',
  scope:'archived separate /386 SOURCE/DEF/RES only; full historical R_mix341 OPEN',
  native_checker_blob:blob(fs.readFileSync(checker)),seed_blob:blob(seedBytes),external_source_blob:blob(sourceBytes),
  external_source_sha256:sha(sourceBytes),original_source_clauses:signed.length,
  src_spec_hash_sha256:sha(Buffer.from(JSON.stringify(seed.spec))),
  exact_base_record_dag_sha256:sha(Buffer.from(JSON.stringify(seed.records))),
  all_64_semantic_complement_controls:true,merged_by_semantic_alpha:semanticAlpha(A)===semanticAlpha(B),
  separated_by_signed_native_facet_signature:refinedAlpha(A)!==refinedAlpha(B),
  native_facets_A:nativeFacetA,native_facets_B:nativeFacetB,
  cost:29,positive:positives,negative:rejects,
  accepted_checker_assertions:results.reduce((n,r)=>n+(r.assertions||0),0),
  bundled_negative_tests:results.reduce((n,r)=>n+(r.nativeNegativeControls||0),0),
  machine:process.version,method:'unchanged original checker as one real Node subprocess per exact packet',
  experiments:results,
  conclusion:'Two semantically identical constant-false globally paid gates differ in exact accepted zero-cost native facet transitions. An abstract state keeping the complete Boolean function, proof DAG, paid identities/output and cost but discarding signed defining operands is not rule-exact. A MAY abstraction stays inclusive but CEGAR must refine with native facet signature; entailed unit [-z] is not an authentic DEF facet.',
  open:['P2-D1','P2-C3','P2-B1','P2-B2','P2-B3']
 };
 const out=process.argv[2]?path.resolve(process.argv[2]):path.join(root,'results/raw/arc/2026-11-12_0424_LSPV3_587_CONSTANT_GATE_FACET_OS_RAW.json');
 fs.mkdirSync(path.dirname(out),{recursive:true});fs.writeFileSync(out,JSON.stringify(report,null,2)+'\n');
 const packetPath=path.join(path.dirname(out),'2026-11-12_0424_LSPV3_587_NATIVE_CONSTANT_FACET_ACCEPTED_PACKET.json');
 fs.writeFileSync(packetPath,specimen);
 console.log(JSON.stringify({out,packetPath,positive:positives,negative:rejects,
  assertions:report.accepted_checker_assertions,negativeControls:report.bundled_negative_tests,
  originalSHA256:report.external_source_sha256,semanticCollision:report.merged_by_semantic_alpha}));
}finally{fs.rmSync(temp,{recursive:true,force:true});}

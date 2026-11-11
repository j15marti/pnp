#!/usr/bin/env node
'use strict';
// LSPV-1/565: archived /386 control-phase vertex relabeling counterexample.
// This is NOT the complete historical R_mix341 checker.
// node experiments/arc/lspv1_565_archived_charge0_symmetry.cjs
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const os=require('node:os'),cp=require('node:child_process'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const fixture=path.join(root,'results/raw/arc/2026-11-10_2124_LSPV3_561_ARCHIVED_386_NATIVE_PACKET.json');
const blob=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
const vb=fs.readFileSync(checker),pb=fs.readFileSync(fixture);
assert.equal(blob(vb),'338305c0ce101704205e57543756b8127074a986');
assert.equal(blob(pb),'d0fa96a155672f8f6a6a3428eacafa15e79b9e88');
const orig=JSON.parse(pb.toString('utf8')),clone=x=>JSON.parse(JSON.stringify(x));
const perm=[1,4,5,2,3,6,7,8];
const lit=x=>Math.sign(x)*perm[Math.abs(x)-1],vtx=x=>x===0?1:x===1?0:x;
const sort=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function transform(d){
 const p=clone(d);p.spec.charge=[p.spec.charge[1],p.spec.charge[0],...p.spec.charge.slice(2)];
 p.gate_defs=p.gate_defs.map(([id,z,a,b])=>[id,z,lit(a),lit(b)]);
 p.records=p.records.map(r=>({...r,c:sort(r.c.map(lit)),
 ...(r.kind==='SOURCE'&&r.source>=0?{source:vtx(r.source)}:{}),
 ...(r.kind==='RES'?{pivot:lit(r.pivot)}:{})}));
 return p;
}
const renamed=transform(orig);
assert.deepEqual(transform(renamed),orig,'isomorphism is involutive');
assert.deepEqual(renamed.spec.charge,[0,1,0,0]);
assert.deepEqual(renamed.summary,orig.summary);
// Original checker source is unchanged. Only append a function export after the
// CLI loop and import with no file arguments; the validator is the original function.
const compiled=new Function('require','process','console','structuredClone',
 vb.toString('utf8')+'\nreturn {checkProof};');
const {checkProof}=compiled(require,{argv:[process.execPath,checker]},{log(){}},structuredClone);
function check(p,control){
 try{return {accepted:true,result:checkProof(p,{control})}}
 catch(e){return {accepted:false,error:String(e.message)}}
}
const results={
 original_core:check(orig,false),
 original_control:check(orig,true),
 relabeled_core:check(renamed,false),
 relabeled_control:check(renamed,true)
};
assert.equal(results.original_core.accepted,true);
assert.equal(results.original_control.accepted,true);
assert.equal(results.relabeled_core.accepted,true);
assert.equal(results.relabeled_control.accepted,false);
assert.match(results.relabeled_control.error,/even mismatch/);
function models(ch){
 let n=0;for(let m=0;m<64;m++){
 const v=[0,0,0,0];for(let i=0;i<orig.spec.edges.length;i++){
 const [a,b]=orig.spec.edges[i],bit=(m>>i)&1;v[a]^=bit;v[b]^=bit;
 }if(v.every((x,i)=>x===ch[i]))n++;
 }return n;
}
assert.equal(models([1,0,0,0]),0);
assert.equal(models([0,1,0,0]),0);
assert.equal(models([0,0,0,0]),8);
assert.equal(models([1,1,0,0]),8);
const hostile=[];
function rejects(name,fn){
 const d=clone(renamed);fn(d);const r=check(d,false);
 assert.equal(r.accepted,false,'hostile '+name+' accepted');
 hostile.push({name,error:r.error});
}
rejects('bad_source',d=>d.records[0].c=[-7]);
rejects('bad_payment',d=>d.summary.paid_total--);
rejects('future_parent',d=>d.records.at(-1).parents[0]=100000);
rejects('bad_gate',d=>d.gate_defs[0][1]=9);
rejects('bad_terminal',d=>d.records.at(-1).c=[6]);
rejects('bad_pivot',d=>d.records.at(-1).pivot=999);
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-lspv1-565-')),cli=[];
try{
 for(const [name,proof,expected] of [['original',orig,true],['relabeled',renamed,false]]){
  const f=path.join(tmp,name+'.json');fs.writeFileSync(f,JSON.stringify(proof)+'\n');
  const r=cp.spawnSync(process.execPath,[checker,f],{encoding:'utf8',timeout:30000});
  assert.equal(r.status===0,expected,name+' original CLI verdict: '+r.stderr);
  if(!expected)assert.match(r.stderr,/even mismatch/);
  cli.push({name,accepted:r.status===0,exit:r.status,
   cliResult:r.status===0?JSON.parse(r.stdout):null,
   error:r.status===0?null:r.stderr.split('\n').find(x=>/even mismatch/.test(x))});
 }
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
console.log(JSON.stringify({result:'PASS',scope:'archived /386 only, not full R_mix341',
checker_blob:blob(vb),input_packet_blob:blob(pb),involution:true,paid:50,
original_charge:orig.spec.charge,relabeled_charge:renamed.spec.charge,
results,source_models:{original_odd:0,relabeled_odd:0,
bad_pseudoeven:0,correct_even:8},hostile,cli,
limitations:'The OS subprocess test is performed when this published runner is executed; historic /341 mixed-rule grammar remains unavailable.'},null,2));

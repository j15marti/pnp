#!/usr/bin/env node
'use strict';
/* LSPV-4/590. Original /386 SOURCE/DEF/RES sibling, not historical R_mix341.
 * Usage: node experiments/arc/lspv4_590_native386_identifier_amplification.cjs [output_dir]
 * Invokes unchanged original archived checker as a separate Node subprocess.
 * p_M and q_M have equal W=61+M; one extra zero-paid view raises
 * compact certificate bytes by M+52+carry(M).
 */
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const cp=require('node:child_process'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'..','..');
const BASE=path.join(ROOT,'results/raw/arc/2026-11-11_1236_LSPV4_549_BRIDGE_W61_BYTE_SAFE_FIVE_SLOT.json');
const CHK=path.join(ROOT,'experiments/arc/lspv2_386_independent_verify.js');
const out=path.resolve(process.argv[2]||fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-590-')));
fs.mkdirSync(out,{recursive:true});
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const clone=x=>JSON.parse(JSON.stringify(x));
const digits=n=>String(n).length;
const inputBytes=fs.readFileSync(BASE),base=JSON.parse(inputBytes);
assert.equal(inputBytes.toString('utf8'),JSON.stringify(base)+'\n','base packet not compact original');
assert.equal(base.records.length,101);assert.equal(base.summary.paid_total,61);
assert.equal(base.records[75].kind,'RES');
assert.deepEqual(base.records[75].parents,[73,9]);
assert.equal(base.records[75].pivot,6);
assert.equal(base.records.at(-1).kind,'RES');
assert.deepEqual(base.records.at(-1).parents,[40,99]);
assert.deepEqual(base.gate_defs,[[0,17,1,2]]);
assert.equal(sha(fs.readFileSync(CHK)),'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113','original checker changed');
function make(M) {
 assert(Number.isSafeInteger(M)&&M>=0);
 const p=clone(base),r=clone(base.records[75]);
 p.records.splice(p.records.length-1,0,...Array.from({length:M},()=>clone(r)));
 p.summary.resolution+=M;p.summary.paid_total+=M;p.summary.live_records+=M;
 const q=clone(p);
 q.records.unshift({kind:'DEF',c:[1,-17],parents:[],gate:0});
 for(const row of q.records.slice(1))row.parents=row.parents.map(x=>x+1);
 q.summary.def_views++;q.summary.live_records++;
 assert.equal(p.summary.paid_total,q.summary.paid_total);
 return {p,q};
}
function parentDigits(p) {return p.records.reduce((s,r)=>s+r.parents.reduce((a,j)=>a+digits(j),0),0)}
function test(name,p,accepted){
 const b=Buffer.from(JSON.stringify(p)+'\n'),f=path.join(out,name+'.json');
 fs.writeFileSync(f,b);
 const run=cp.spawnSync(process.execPath,[CHK,f],{encoding:'utf8',timeout:45000,maxBuffer:4e6});
 assert.equal(run.status===0,accepted,name+': status='+run.status+': '+run.stderr.slice(0,600));
 let result={name,expected:accepted?'ACCEPT':'REJECT',bytes:b.length,sha256:sha(b),
  W:p.summary.paid_total,RES:p.summary.resolution,gateOwners:p.summary.paid_gates,
  DEFviews:p.summary.def_views,source:p.summary.source};
 if(accepted)result.assertions=JSON.parse(run.stdout.trim()).assertions;
 else result.rejection=(run.stderr.match(/Error: ([^\n]+)/)||[])[1]||run.stderr.slice(0,160);
 return result;
}
const rows=[],ms=[0,1,9,10,90,100,897,898,899,900,1000];
for(const M of ms){
 const variants=make(M),p=variants.p,q=variants.q;
 const bp=Buffer.byteLength(JSON.stringify(p)+'\n'),bq=Buffer.byteLength(JSON.stringify(q)+'\n');
 const dp=parentDigits(q)-parentDigits(p),carry=digits(102+M)-digits(101+M);
 assert.equal(dp,M+3);
 assert.equal(bq-bp,M+52+carry);
 const a=test('M'+M+'_p',p,true),b=test('M'+M+'_q',q,true);
 rows.push({M,bytesP:bp,bytesQ:bq,deltaBytes:bq-bp,deltaParentDigits:dp,summaryCarry:carry,W:61+M,checkerP:a,checkerQ:b});
}
const seed=make(10).q;
const mutations=[
 ['forged_facet',d=>d.records[0].c=[-d.spec.guard]],
 ['forged_gate',d=>d.records[0].gate=90],
 ['future_parent',d=>d.records.at(-1).parents[0]=d.records.length+10],
 ['underpaid',d=>d.summary.paid_total--],
 ['bad_pivot',d=>d.records.at(-1).pivot=90]
];
const hostile=mutations.map(pair=>{const d=clone(seed);pair[1](d);return test('hostile_'+pair[0],d,false)});
const result={schema:'LSPV4-590-NATIVE386-REFERENCE-WIDTH/v1',status:'PROVED/RESTRICTED symbolic; OS Node original checker replay',
 checker:'experiments/arc/lspv2_386_independent_verify.js',
 checkerSHA256:sha(fs.readFileSync(CHK)),seed:BASE,seedSHA256:sha(inputBytes),
 formula:'DeltaByte(M)=M+52+digits(102+M)-digits(101+M)',differentPaidCharges:false,
 copiedRES:{sourceRecord:75,pivot:6,parents:[73,9],insertion:'before terminal record'},
 zeroPaidNewDEF:{gate:0,facet:[1,-17],insertion:'before first record',used:false},
 caveats:'Original /386 sibling only; redundant unused DEF; exact compact byte length not proof discovery time, inference weight, or physical RAM; not historical mixed R_mix341.',
 rows,hostile,assertions:rows.reduce((s,r)=>s+r.checkerP.assertions+r.checkerQ.assertions,0)};
fs.writeFileSync(path.join(out,'LSPV4_590_REFWIDTH_NATIVE_CHECKER_RAW.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:'PASS',out,rows:rows.map(x=>({M:x.M,deltaBytes:x.deltaBytes,deltaParentDigits:x.deltaParentDigits,W:x.W})),accepted:rows.length*2,rejected:hostile.length,assertions:result.assertions},null,2));

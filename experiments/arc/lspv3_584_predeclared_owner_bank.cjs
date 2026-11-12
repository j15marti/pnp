#!/usr/bin/env node
'use strict';
// LSPV-3/584, original archived /386 owner-bank cost-fiber test.
// Run at repo root: node experiments/arc/lspv3_584_predeclared_owner_bank.cjs [output.json]
// No external dependencies. The original unchanged checker is a REAL Node OS subprocess.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process'),os=require('node:os'),assert=require('node:assert/strict');
const root=process.cwd(),checkerRel='experiments/arc/lspv2_386_independent_verify.js',seedRel='results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json';
const checker=path.join(root,checkerRel),seed=path.join(root,seedRel);
const blob=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+Buffer.byteLength(b)+'\0'),Buffer.from(b)])).digest('hex');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const bytes=fs.readFileSync(checker),source=fs.readFileSync(seed);
assert.equal(blob(bytes),'338305c0ce101704205e57543756b8127074a986');
assert.equal(blob(source),'318c52d99977ea4e91bc8554051138a700c1dc94');
const original=JSON.parse(source),copy=x=>structuredClone(x),runDir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-584-'));
assert.equal(original.records.length,45);assert.equal(original.summary.resolution,28);assert.equal(original.gate_defs.length,1);
function packet(k){let d=copy(original);for(let i=0;i<k;i++)d.gate_defs.push([i+1,i+9,2,5]);d.summary.paid_gates=1+k;d.summary.paid_total=29+k;return d;}
const outcomes=[];
function test(name,p,accept){
 const input=Buffer.from(JSON.stringify(p)),file=path.join(runDir,name+'.json');fs.writeFileSync(file,input);
 const before=process.hrtime.bigint(),r=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:30000,maxBuffer:3*1024*1024});
 const ok=!r.error&&r.status===0;assert.equal(ok,accept,name+' '+String(r.stderr||r.error||''));
 const out=ok?JSON.parse(r.stdout.trim().split('\n').at(-1)):null;
 if(out){assert.equal(out.paid,p.summary.paid_total);assert.equal(out.def,p.gate_defs.length);assert.equal(out.res,28);assert.equal(out.negativeTests,11);}
 outcomes.push({name,expected:accept,verdict:ok?'ACCEPT':'REJECT',bytes:input.length,sha256:sha(input),git_blob:blob(input),paid:p.summary.paid_total,gate_owners:p.gate_defs.length,records:p.records.length,cli_assertions:out?.assertions??null,bundled_negative_tests:out?.negativeTests??null,error:ok?null:String(r.stderr||r.error?.message||'').trim().split('\n')[0],wall_ms:Math.round(Number(process.hrtime.bigint()-before)/1e4)/100});
}
try {
 const refSpec=sha(Buffer.from(JSON.stringify(original.spec))),refDAG=sha(Buffer.from(JSON.stringify(original.records)));
 for(let k of [0,1,2,4,8,16,32,128]){
  const p=packet(k);assert.equal(sha(Buffer.from(JSON.stringify(p.spec))),refSpec);assert.equal(sha(Buffer.from(JSON.stringify(p.records))),refDAG);test('positive_k'+k,p,true);
 }
 let p=packet(1);p.summary.paid_total--;test('underpaid',p,false);
 p=packet(1);p.summary.paid_gates--;test('gate_count_underreported',p,false);
 p=packet(1);p.gate_defs[1][0]=0;test('owner_id_collision',p,false);
 p=packet(1);p.gate_defs[1][1]=8;test('wire_collision',p,false);
 p=packet(1);p.gate_defs[1][2]=7;test('guard_operand',p,false);
 p=packet(1);p.gate_defs[1][2]=10;test('undeclared_operand',p,false);
 p=packet(1);p.records[0].c=[-1,2,3,-7];test('signed_source_forgery',p,false);
 p=packet(1);p.records[17].kind='LOCAL-CONVERT';test('foreign_opcode',p,false);
 const report={id:'LSPV-3/584',scope:'unchanged original archived /386 CLI only, not R_mix341',checker_blob:blob(bytes),seed_blob:blob(source),spec_sha256:refSpec,proof_records_sha256:refDAG,cases:outcomes,positive:outcomes.filter(x=>x.expected).length,negative:outcomes.filter(x=>!x.expected).length,actual_execution:'original Node OS subprocess for each case, including 11 built-in controls in each accepted case'};
 if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify(report,null,2));
} finally {fs.rmSync(runDir,{recursive:true,force:true});}

#!/usr/bin/env node
'use strict';
// LSPV-3/567: original archived /386 checker executable raw-byte regression.
// Use: node experiments/arc/lspv3_567_shadowed_386_mixed_opcode.cjs [--write]
// Execute at repository root. Node.js >=18. Only standard-library modules.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert/strict');
const crypto = require('crypto');
const root = path.resolve(__dirname,'../..');
const checkerFile = path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedFile = path.join(root,'results/raw/arc/2026-11-10_2124_LSPV3_561_ARCHIVED_386_NATIVE_PACKET.json');
const publishedPacketFile = path.join(root,'results/raw/arc/2026-11-11_0324_LSPV3_567_SHADOWED_386_ACCEPTED_PACKET.json');
const originalSource = fs.readFileSync(checkerFile,'utf8');
const base = fs.readFileSync(seedFile,'utf8');
function replaceOnce(s,a,b){assert(s.includes(a),'Missing original bytes: '+a);return s.replace(a,b);}
function makeShadow(b){
 let z=replaceOnce(b,'"charge":[1,0,0,0]','"charge":[0,0,0,0],"charge":[1,0,0,0]');
 z=replaceOnce(z,'"parents":[],"source":0}','"parents":[],"source":98765,"source":0}');
 z=replaceOnce(z,'"parents":[],"gate":0}','"parents":[],"gate":98765,"gate":0}');
 z=replaceOnce(z,'"kind":"RES"','"kind":"LOCAL-CONVERT","kind":"RES","rule":"AND3","weight":0,"exported_wire":8,"context":{"assumption":"fake","discharged":true},"advertised_gf2":{"mask":"0","rhs":1}');
 return z;
}
const forged=makeShadow(base);
assert.equal(fs.readFileSync(publishedPacketFile,'utf8'),forged,'published packet must match exact bytes');
// Run the archived original mathematical checker WITHOUT changing its body.
const coreSource = originalSource.split('for(const f of process.argv.slice(2))')[0];
const ctxCore={require,process,console};
vm.createContext(ctxCore);
vm.runInContext(coreSource+'\nglobalThis._nativeCheck=checkProof;globalThis._counter=()=>tests;',ctxCore,{filename:checkerFile});
function checkCore(raw){
 let before=ctxCore._counter();
 try{
  const r=ctxCore._nativeCheck(JSON.parse(raw));
  return {accepted:true,assertions:ctxCore._counter()-before,work:r.paid,records:r.records,bytes:Buffer.byteLength(raw)};
 }catch(e){return {accepted:false,assertions_before_reject:ctxCore._counter()-before,error:String(e),bytes:Buffer.byteLength(raw)};}
}
const cases=[
 ['baseline',base,true],
 ['shadow_all',forged,true],
 ['shadow_charge_last_even',replaceOnce(forged,'"charge":[0,0,0,0],"charge":[1,0,0,0]','"charge":[1,0,0,0],"charge":[0,0,0,0]'),false],
 ['shadow_source_last_forged',replaceOnce(forged,'"source":98765,"source":0','"source":0,"source":98765'),false],
 ['shadow_gate_last_forged',replaceOnce(forged,'"gate":98765,"gate":0','"gate":0,"gate":98765'),false],
 ['shadow_opcode_last_localconvert',replaceOnce(forged,'"kind":"LOCAL-CONVERT","kind":"RES"','"kind":"RES","kind":"LOCAL-CONVERT"'),false],
 ['actual_localconvert_opcode',replaceOnce(base,'"kind":"RES"','"kind":"LOCAL-CONVERT"'),false],
 ['extraneous_rule_metadata',replaceOnce(base,'"kind":"RES"','"kind":"RES","rule":"LOCAL-CONVERT","cost":0'),true],
 ['signed_source_mutation',replaceOnce(base,'"c":[1,2,3,-7]','"c":[1,2,-3,-7]'),false]
];
const outcomes=cases.map(([name,payload,expected])=>{
 let out=checkCore(payload);assert.equal(out.accepted,expected,'Unexpected original-core result: '+name);
 return Object.assign({name,expected},out);
});
// Run the COMPLETE original CLI body and all eleven bundled hostile tests.
// The original verification code is not edited. Only file-I/O is adapted.
function checkCLI(name,payload){
 const stdout=[]; const fsAdapter={readFileSync:f=>{assert.equal(f,name);return Buffer.from(payload,'utf8');}};
 const requireAdapter = mod => mod==='fs'?fsAdapter:require(mod);
 const context={require:requireAdapter,process:{argv:['node','checker.js',name]},
                console:{log:z=>stdout.push(String(z))},structuredClone};
 vm.runInNewContext(originalSource,context,{filename:checkerFile});
 assert.equal(stdout.length,1);
 return JSON.parse(stdout[0]);
}
const cliBase=checkCLI('baseline.json',base), cliShadow=checkCLI('shadowed.json',forged);
for (const c of [cliBase,cliShadow]){
 assert.equal(c.assertions,4492);assert.equal(c.negativeTests,11);assert.equal(c.paid,50);
 assert.equal(c.def,1);assert.equal(c.res,49);assert.equal(c.sources,17);assert.equal(c.records,69);
}
const output={
 run:'LSPV3-567-OS-NODE-REPLAY',node:process.version,originalCheckerSHA256:crypto.createHash('sha256').update(originalSource).digest('hex'),
 baselineSHA256:crypto.createHash('sha256').update(base).digest('hex'),
 shadowedSHA256:crypto.createHash('sha256').update(forged).digest('hex'),
 outcomes,CLI:[cliBase,cliShadow],all_expected:true,
 classification:'Actual /386 checker accepted raw duplicate-member and unrecognized-rule metadata; not a real mixed-rule inference.'
};
if (process.argv.includes('--write')){
 const out=path.join(root,'results/raw/arc/2026-11-11_0324_LSPV3_567_SHADOWED_386_OS_NODE_RAW.json');
 fs.writeFileSync(out,JSON.stringify(output,null,2)+'\n');
}
console.log(JSON.stringify(output,null,2));

'use strict';
// LSPV-3/620: native OS replay; two distinct ORIGINAL checkers, NOT R_mix341.
const fs=require('fs'),path=require('path'),os=require('os'),crypto=require('crypto'),cp=require('child_process'),assert=require('assert/strict');
const root=path.resolve(__dirname,'../..');
const paths={c341:'experiments/arc/lspv2_341_independent_verify.js',p341:'results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json',c386:'experiments/arc/lspv2_386_independent_verify.js',p386:'results/raw/arc/2026-11-11_0407_LSPV2_555_ACCEPTED_LIVE_DEF_RES_K1.json'};
const pins={c341:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',p341:'706947c767361e7c979b8208677eb983d33838f4',c386:'338305c0ce101704205e57543756b8127074a986',p386:'aeeb555c4dcf7f510a9a501c8afc609b629a9298'};
for(const k of Object.keys(paths)){const b=fs.readFileSync(path.join(root,paths[k]));const g=crypto.createHash('sha1').update('blob '+b.length+'\x00').update(b).digest('hex');assert.equal(g,pins[k],'Git blob changed: '+k)}
const p341=JSON.parse(fs.readFileSync(path.join(root,paths.p341),'utf8'));
const p386=JSON.parse(fs.readFileSync(path.join(root,paths.p386),'utf8'));
const copy=x=>JSON.parse(JSON.stringify(x));
function models(cs,n){let count=0,witness=null;assert(n<=24);
for(let m=0;m<2**n;m++)if(cs.every(c=>c.some(l=>((m>>(Math.abs(l)-1))&1)===(l>0?1:0)))){count++;if(witness===null)witness=Array.from({length:n},(_,i)=>(m>>i)&1).join('')}
return{models:count,witness}}
const a341=p341.fixtures[1].clauses.map(c=>c.literals);
const a386=p386.records.filter(r=>r.kind==='SOURCE').map(r=>r.c);
const sat386=copy(a386);sat386[0]=copy(sat386[1]);
const counts={inband_sat341:models(a341,18),inband_unsat386:models(a386,7),external_sat386:models(sat386,7)};
assert.deepEqual(counts.inband_sat341.models,64);assert.equal(counts.inband_unsat386.models,0);assert.equal(counts.external_sat386.models,2);
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'pnp620-'));
function run(ckey,p,label){const tmp=path.join(dir,label+'.json');fs.writeFileSync(tmp,JSON.stringify(p));const r=cp.spawnSync(process.execPath,[path.join(root,paths[ckey]),tmp],{encoding:'utf8',timeout:20000,maxBuffer:1e7});const ok=r.status===0&&!r.error;const j=ok?JSON.parse(r.stdout):null;return{label,checker:ckey,accepted:ok,assertions:j?.assertions??j?.checks??null,paid:j?.paid??null,error:ok?null:(r.stderr||String(r.error)).trim().split('\n').slice(-2).join(' | ')}}
const tests=[];
try{
tests.push(run('c341',p341,'baseline341'));tests.push(run('c386',p386,'baseline386'));
let x=copy(p341);x.fixtures[1].signed_original_source={clauses:[[1],[-1]],claim:'external source',context:'assume(false)'};tests.push(run('c341',x,'ignored_sidecar341'));
x=copy(p386);x.signed_original_source={clauses:sat386,claim:'external source',context:'assume(false)'};tests.push(run('c386',x,'ignored_sat_sidecar386'));
x=copy(p341);x.fixtures[1].clauses[0].literals[0]*=-1;tests.push(run('c341',x,'bad_inband341'));
x=copy(p386);x.records.find(r=>r.kind==='SOURCE').c=[-7];tests.push(run('c386',x,'bad_inband386'));
x=copy(p386);x.spec.charge=[0,0,0,0];tests.push(run('c386',x,'even_charge386'));
x=copy(p386);x.records.find(r=>r.kind==='RES').kind='LOCAL-CONVERT';tests.push(run('c386',x,'bad_opcode386'));
assert.deepEqual(tests.map(t=>t.accepted),[true,true,true,true,false,false,false,false]);
const out={mode:'actual_node_os_subprocess',original_git_blob_pins:pins,counts,tests,warning:'The /341 and /386 checkers are distinct siblings, not a complete historical R_mix341 checker.'};
const result=JSON.stringify(out,null,2)+'\n';
if(process.argv.includes('--write'))fs.writeFileSync(path.join(root,'results/raw/arc/2026-11-13_1128_LSPV3_620_D1_NATIVE_OS_REPLAY.json'),result);
process.stdout.write(result);
}finally{fs.rmSync(dir,{recursive:true,force:true})}

// LSPV-5/527: rerun LSPV-3/620 negative controls and record the exact checker rejection reason.
// Usage: node lspv5_527_rejection_reason_replay.cjs REPO_ROOT TMP_DIR
const fs=require('fs'),cp=require('child_process'),path=require('path');
const root=process.argv[2],tmp=process.argv[3];
const p341=JSON.parse(fs.readFileSync(root+'/results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json'));
const p386=JSON.parse(fs.readFileSync(root+'/results/raw/arc/2026-11-11_0407_LSPV2_555_ACCEPTED_LIVE_DEF_RES_K1.json'));
const c=x=>JSON.parse(JSON.stringify(x));const out=[];
function run(ck,p,l){const f=path.join(tmp,l+'.json');fs.writeFileSync(f,JSON.stringify(p));const r=cp.spawnSync(process.execPath,[root+'/experiments/arc/'+ck,f],{encoding:'utf8'});const m=(r.stderr.match(/Error: ([^\n]*)/)||[])[1]||null;out.push({label:l,accepted:r.status===0,reason:m});}
let x=c(p341);x.fixtures[1].clauses[0].literals[0]*=-1;run('lspv2_341_independent_verify.js',x,'bad_inband341');
x=c(p386);x.records.find(r=>r.kind==='SOURCE').c=[-7];run('lspv2_386_independent_verify.js',x,'bad_inband386_width1');
x=c(p386);{const r=x.records.find(r=>r.kind==='SOURCE'&&r.source!==-1);r.c=r.c.map((l,i)=>i===0?-l:l).sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);}run('lspv2_386_independent_verify.js',x,'bad_inband386_width_preserving_sign_flip');
x=c(p386);x.spec.charge=[0,0,0,0];run('lspv2_386_independent_verify.js',x,'even_charge386');
x=c(p386);x.spec.charge=[0,1,0,0];run('lspv2_386_independent_verify.js',x,'odd_charge_first_zero386');
x=c(p386);x.records.find(r=>r.kind==='RES').kind='LOCAL-CONVERT';run('lspv2_386_independent_verify.js',x,'bad_opcode386');
console.log(JSON.stringify(out,null,1));

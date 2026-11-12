'use strict';
// Reproduction of LSPV-4/553. Requires Node >= 18 and a full repository checkout.
// Runs the original /386 checker as an actual OS subprocess; does not modify its source.
const fs=require('fs'),os=require('os'),path=require('path'),cp=require('child_process');
const assert=require('assert'),crypto=require('crypto');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const original=JSON.parse(fs.readFileSync(path.join(root,'results/raw/arc/2026-11-11_1524_LSPV3_579_SHARED_LIVE_BATCH_ACCEPTED_PACKET.json'),'utf8'));
const copy=o=>JSON.parse(JSON.stringify(o));
const pruned=copy(original);
assert.deepStrictEqual(original.gate_defs[0],[0,20,1,4]);
assert(original.records.every(r=>r.kind!=='DEF'||r.gate!==0));
assert(original.records.every(r=>r.c.every(x=>Math.abs(x)!==20)));
assert(original.gate_defs.slice(1).every(g=>g.slice(2).every(x=>Math.abs(x)!==20)));
pruned.gate_defs.shift();
pruned.summary.paid_gates--;
pruned.summary.paid_total--;
assert.strictEqual(pruned.summary.paid_total,43);
assert.deepStrictEqual(pruned.records,original.records);
assert.deepStrictEqual(pruned.spec,original.spec);
const cases=[
['old_W44',original,true],
['pruned_W43',pruned,true],
['delete_live_owner_1',(()=>{let d=copy(pruned);d.gate_defs=d.gate_defs.filter(g=>g[0]!==1);d.summary.paid_gates--;d.summary.paid_total--;return d})(),false],
['delete_live_owner_2',(()=>{let d=copy(pruned);d.gate_defs=d.gate_defs.filter(g=>g[0]!==2);d.summary.paid_gates--;d.summary.paid_total--;return d})(),false],
['underpay',(()=>{let d=copy(pruned);d.summary.paid_total=42;return d})(),false],
['alter_shared_unit',(()=>{let d=copy(pruned);d.records[19].c=[21];return d})(),false],
['forge_source',(()=>{let d=copy(pruned);d.records[0].c=[-1,2,3,-19];return d})(),false],
['corrupt_shared_reference',(()=>{let d=copy(pruned);d.records[26].parents=[25,18];return d})(),false]
];
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-553-'));
const results=[];
try{
 for(const [name,d,expected] of cases){
  const file=path.join(tmp,name+'.json');
  const bytes=JSON.stringify(d)+'\n';
  fs.writeFileSync(file,bytes);
  const run=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:25000});
  const accepted=run.status===0;
  assert.strictEqual(accepted,expected,name+': '+run.stderr);
  results.push({name,expected,accepted,bytes:Buffer.byteLength(bytes),sha256:crypto.createHash('sha256').update(bytes).digest('hex'),checker_stdout:run.stdout.trim(),checker_stderr:accepted?'':run.stderr.trim().slice(0,500)});
 }
 const r=pruned.records, use=Array(r.length).fill(0);
 for(const v of r)for(const p of v.parents)use[p]++;
 const ancestor=new Set([r.length-1]),todo=[r.length-1];
 while(todo.length){for(const p of r[todo.pop()].parents)if(!ancestor.has(p)){ancestor.add(p);todo.push(p)}}
 const hist={};
 for(const i of ancestor){const k=r[i].kind;hist[k]=(hist[k]||0)+1}
 const shared=r.map((v,i)=>({index:i,kind:v.kind,consumers:use[i]})).filter(x=>x.consumers>1&&x.kind!=='SOURCE');
 assert.deepStrictEqual(hist,{RES:41,SOURCE:17,DEF:4});
 assert.deepStrictEqual(shared.map(x=>x.index),[19,20,21,24,27,30,33]);
 console.log(JSON.stringify({status:'PASS',original_checker:'experiments/arc/lspv2_386_independent_verify.js',total:cases.length,results,ancestors:ancestor.size,ancestor_kinds:hist,shared,paid_W44:44,paid_W43:43},null,2));
}finally{
 for(const f of fs.readdirSync(tmp))fs.rmSync(path.join(tmp,f));
 fs.rmdirSync(tmp);
}

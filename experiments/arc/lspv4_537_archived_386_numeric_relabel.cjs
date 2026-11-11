'use strict';
// LSPV-4/537. Native archived /386 numeric namespace normalizer.
// Invoke from the j15marti/pnp checkout:
// node experiments/arc/lspv4_537_archived_386_numeric_relabel.cjs
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checkerPath=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedPath=path.join(root,'results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json');
const checkerRaw=fs.readFileSync(checkerPath);
const seedRaw=fs.readFileSync(seedPath);
const gitSha=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
assert.equal(gitSha(checkerRaw),'338305c0ce101704205e57543756b8127074a986');
assert.equal(gitSha(seedRaw),'08aa169b5db49b2ddd1cb5a9b6890fcc3b790916');
const source=checkerRaw.toString('utf8'),seed=JSON.parse(seedRaw.toString('utf8'));
const clone=x=>JSON.parse(JSON.stringify(x));
const canonical=xs=>[...new Set(xs)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function relabel(d,guard,wireList,idList,sort=true){
 const out=clone(d),E=d.spec.edges.length;
 assert(Number.isSafeInteger(guard)&&guard>E);
 assert.equal(wireList.length,d.gate_defs.length);assert.equal(idList.length,d.gate_defs.length);
 assert.equal(new Set([guard,...wireList]).size,wireList.length+1);
 assert(wireList.every(x=>Number.isSafeInteger(x)&&x>E));
 assert(idList.every(x=>Number.isSafeInteger(x)&&x>=0));
 assert.equal(new Set(idList).size,idList.length);
 const wires=new Map([[d.spec.guard,guard],...d.gate_defs.map((x,i)=>[x[1],wireList[i]])]);
 const ids=new Map(d.gate_defs.map((x,i)=>[x[0],idList[i]]));
 const L=x=>Math.sign(x)*(wires.get(Math.abs(x))??Math.abs(x));
 out.spec.guard=guard;
 out.gate_defs=d.gate_defs.map(([id,z,a,b],i)=>[idList[i],wireList[i],L(a),L(b)]);
 out.records=d.records.map(r=>({...r,c:sort?canonical(r.c.map(L)):r.c.map(L),
   ...(r.kind==='RES'?{pivot:L(r.pivot)}:{}),
   ...(r.kind==='DEF'?{gate:ids.get(r.gate)}:{})}));
 return out;
}
function dense(d){
 const E=d.spec.edges.length,g=d.gate_defs.length;
 return relabel(d,E+1,d.gate_defs.map((x,i)=>E+2+i),d.gate_defs.map((x,i)=>i));
}
const mockReq=id=>id==='fs'?{}:id==='crypto'?crypto:id==='assert'?assert:require(id);
const sandbox={require:mockReq,process:{argv:['node','original_checker.js']},
  console:{log(){}},structuredClone:clone,Buffer};
vm.runInNewContext(source+'\nglobalThis.__nativeCore=checkProof;',sandbox,{timeout:10000});
const checkCore=(d,control=true)=>sandbox.__nativeCore(d,{control});
function checkCLI(d){
 const bytes=Buffer.from(JSON.stringify(d),'utf8'),lines=[];
 const req=id=>id==='fs'?{readFileSync:()=>bytes}:id==='crypto'?crypto:
   id==='assert'?assert:require(id);
 const ctx={require:req,process:{argv:['node','original_checker.js','packet.json']},
   console:{log:s=>lines.push(JSON.parse(s))},structuredClone:clone,Buffer};
 vm.runInNewContext(source,ctx,{timeout:10000});
 assert.equal(lines.length,1);
 return lines[0];
}
const variants=[
 ['original',seed],
 ['sparse_guard_high_reverse_gate_order',
  relabel(seed,9876543210123,[123456789012,98765432101],[123456789000,432100000000])],
 ['sparse_guard_low',
  relabel(seed,13,[9007199254740000,6000000000000],[9000000000000,3])],
 ['sparse_guard_close_to_max_safe',
  relabel(seed,9007199254740800,[9007199254740799,9007199254740798],
    [9007199254740780,9007199254740779])]
];
const accepted=[];
for(const [name,d] of variants){
 const c=checkCore(d),cli=checkCLI(d),n=dense(d);
 assert.equal(JSON.stringify(n),JSON.stringify(seed),'roundtrip '+name);
 assert.equal(checkCore(n).paid,53);
 assert.equal(c.paid,53);assert.equal(cli.paid,53);
 assert.equal(cli.negativeTests,11);assert.equal(cli.assertions,4663);
 accepted.push({name,bytes:JSON.stringify(d).length,
  normalized_bytes:JSON.stringify(n).length,guard:d.spec.guard,
  gate_wires:d.gate_defs.map(x=>x[1]),gate_ids:d.gate_defs.map(x=>x[0]),
  paid:c.paid,source:c.sources,resolution:c.res,records:c.records,
  bundled_negative_tests:cli.negativeTests,original_cli_assertions:cli.assertions});
}
const rejected=[];
function hostile(name,d){
 let bad=false;try{checkCore(d,false)}catch(e){bad=true}
 assert(bad,'checker accepted hostile case '+name);rejected.push(name);
}
hostile('unsorted_relabel',
 relabel(seed,13,[9007199254740000,6000000000000],[9000000000000,3],false));
const mutations=[
 ['duplicate_owner',p=>{p.gate_defs[1][0]=p.gate_defs[0][0]}],
 ['duplicate_output',p=>{p.gate_defs[1][1]=p.gate_defs[0][1]}],
 ['dangling_gate_ref',p=>{p.records.find(r=>r.kind==='DEF').gate=999]}],
 ['wrong_pivot',p=>{p.records.find(r=>r.kind==='RES').pivot=123456789]}],
 ['underpayment',p=>{p.summary.paid_total-=1}],
 ['unsafe_numeric_owner',p=>{p.gate_defs[1][0]=9007199254740992}]
];
for(const [name,change] of mutations){
 let p=clone(variants[1][1]);change(p);hostile(name,p);
}
console.log(JSON.stringify({date:'2026-11-11 00:36 PST',scope:'original_archived_386_only',
 checker_blob:gitSha(checkerRaw),seed_blob:gitSha(seedRaw),
 semantic_claim:'positive accepted namespace isomorphism with dense signed wire and owner IDs; no full R_mix341 claim',
 accepted,rejected,original_checker_cli_assertions:accepted.reduce((s,x)=>s+x.original_cli_assertions,0),
 proof_chain:{P2_D1:'OPEN',P2_C3:'OPEN',P2_B1:'OPEN',P2_B2_B3:'OPEN'}},null,2));

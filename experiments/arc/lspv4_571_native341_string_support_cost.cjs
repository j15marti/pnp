'use strict';
/*
 * LSPV-4/571. Run from j15marti/pnp repository root:
 *   node experiments/arc/lspv4_571_native341_string_support_cost.cjs
 * Original /341 checker is pinned and run UNMODIFIED inside Node's VM.
 * This is a restricted SOURCE/AND3/XOR checker, not the unified R_mix341.
 */
const fs=require('node:fs');
const vm=require('node:vm');
const crypto=require('node:crypto');
const assert=require('node:assert/strict');
const path=require('node:path');
const root=process.cwd();
const CHECKER='experiments/arc/lspv2_341_independent_verify.js';
const SEED='results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json';
const RAW='results/raw/arc/2026-11-12_1536_LSPV4_571_NATIVE341_TYPED_STRING_COST_RAW.json';
function blob(b){return crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');}
function read(file,sha){const b=fs.readFileSync(path.join(root,file));assert.equal(blob(b),sha,file+' blob changed');return b.toString('utf8');}
const checker=read(CHECKER,'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
const source=read(SEED,'fe27fe1011d0021e721ccaeb747ed58da65d7464');
const seed=JSON.parse(source);
const raw=JSON.parse(fs.readFileSync(path.join(root,RAW),'utf8'));
const clone=v=>JSON.parse(JSON.stringify(v));
const nodes=[2,5,8,11],perms=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
const original=nodes.map(i=>seed.fixtures[0].proof[i].support);
function variant(choice){
  const d=clone(seed);
  choice.forEach((v,j)=>{
    const q=perms[v%6].map(i=>original[j][i]);
    d.fixtures[0].proof[nodes[j]].support=v<6?q:q.join('');
  });
  return d;
}
function native(p){
  let logs=[];
  try {
    vm.runInNewContext(checker,{
      require:name=>{assert.equal(name,'fs');return {readFileSync:()=>JSON.stringify(p)};},
      process:{argv:['node',CHECKER,'in-memory.json']},
      console:{log:s=>logs.push(s)}
    },{filename:CHECKER,timeout:15000});
    assert.equal(logs.length,1);
    return {accepted:true,checks:JSON.parse(logs[0]).checks};
  }catch(e){return {accepted:false,error:String(e.message)};}
}
const baselineBytes=Buffer.byteLength(JSON.stringify(seed)+'\n');
assert.equal(baselineBytes,77714);
assert.equal(native(seed).checks,30714);
const positives=[
  [0,0,0,0],[6,6,6,6],[11,11,11,11],[6,7,8,9],
  [11,9,7,5],[0,6,0,6],[6,0,6,0],[5,4,3,2],
  [2,8,4,10],[10,4,6,0],[1,3,5,7],[7,5,3,1]
];
const cases=[];
positives.forEach((ch,i)=>{
  const p=variant(ch),r=native(p),bytes=Buffer.byteLength(JSON.stringify(p)+'\n');
  assert(r.accepted&&r.checks===30714,'native rejection '+i);
  const count=ch.filter(x=>x>=6).length;
  assert.equal(bytes,baselineBytes-2*count);
  cases.push({name:'positive_'+i,choice:ch,accepted:true,checks:r.checks,bytes,error:null});
});
const bad=[
 ['negative_bad_digit',p=>p.fixtures[0].proof[2].support='013'],
 ['negative_duplicate',p=>p.fixtures[0].proof[2].support='001'],
 ['negative_internal_string',p=>p.fixtures[0].proof[0].support='012'],
 ['negative_bad_source',p=>p.fixtures[0].clauses[0].literals[0]=999]
];
const negatives=[];
for(const [name,mutate] of bad){
  const p=variant([6,6,6,6]);mutate(p);
  const r=native(p);assert.equal(r.accepted,false,name+' unexpectedly accepted');
  negatives.push({name,choice:[6,6,6,6],accepted:false,checks:null,bytes:Buffer.byteLength(JSON.stringify(p)+'\n'),error:'Error: '+r.error});
}
function tableEval(row,sup,bits){
  let ix=0;for(let k=0;k<sup.length;k++)ix|=Number(bits[sup[k]])<<k;
  return (row.table>>ix)&1;
}
let affine=0;
for(let j=0;j<4;j++){
  const n=seed.fixtures[0].proof[nodes[j]],mask=Number(BigInt(n.row.mask));
  for(let v=0;v<12;v++){
    const sup=v<6?perms[v].map(q=>original[j][q]):perms[v-6].map(q=>original[j][q]).join('');
    assert.equal(sup.length,3);
    assert.equal(new Set(sup).size,3);
    assert(original[j].every(x=>sup.includes(x)));
    for(let a=0;a<64;a++){
      const bits=Array.from({length:6},(_,k)=>(a>>k)&1);
      let parity=0;for(let k=0;k<6;k++)if((mask>>k)&1)parity^=bits[k];
      assert.equal(tableEval(n,sup,bits),Number(parity===n.row.rhs));
      affine++;
    }
  }
}
assert.equal(affine,3072);
assert.equal(positives.length,raw.replay.positive_count);
assert.equal(negatives.length,raw.replay.negative_count);
for(let i=0;i<positives.length;i++){
  const x=raw.replay.positives[i],y=cases[i];
  assert.deepEqual({name:x.name,choice:x.choice,accepted:x.accepted,checks:x.checks,bytes:x.bytes,error:x.error},y);
}
for(let i=0;i<negatives.length;i++){
  const x=raw.replay.negatives[i],y=negatives[i];
  assert.equal(x.name,y.name);assert.equal(x.accepted,false);
  assert.equal(x.bytes,y.bytes);
  assert(y.error.includes(String(x.error).replace(/^Error: /,'')));
}
assert.equal(raw.theorem.independent_affine_evaluations,affine);
const counts=seed.fixtures.map(f=>f.proof.filter(p=>p.rule==='AND3').length);
assert.equal(counts.reduce((a,b)=>a+b,0),246);
for(const i of nodes){
  const n=seed.fixtures[0].proof[i],later=seed.fixtures[0].proof.filter((x,j)=>j>i&&x.parents.includes(n.id));
  assert.equal(later.length,1);assert.equal(later[0].rule,'XOR');
}
console.log(JSON.stringify({
 role:'LSPV-4/571',checker_blob:blob(Buffer.from(checker)),seed_blob:blob(Buffer.from(source)),
 full_native_V8_positive:cases.length,full_native_V8_hostile_rejected:negatives.length,
 affine_parameter_evaluations:affine,verified_raw:true,
 original_bytes:baselineBytes,all_strings_bytes:baselineBytes-8,
 paid_nodes_K4:15,paid_nodes_all_separate_fixtures:seed.fixtures.reduce((s,f)=>s+f.proof.length,0),
 accepted_parsed_orbit_lower_bound:'6^242 * 12^4 = 16 * 6^246',
 full_historical_R_mix341_authenticated:false,
 OS_CLI_replay:'not performed by this VM-based runner'
},null,2));

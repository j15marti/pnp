'use strict';
// LSPV-3/594 native /341 typed support-coordinate orbit OS replayer.
// Run: node experiments/arc/lspv3_594_native341_typed_support_permutations.cjs [results.json]
// Requires full repository checkout, Node >=18, and NO external packages.
const fs=require('node:fs'), path=require('node:path'), os=require('node:os'),
 cp=require('node:child_process'), crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const rel={checker:'experiments/arc/lspv2_341_independent_verify.js',
 seed:'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json'};
const pin={checker:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',seed:'fe27fe1011d0021e721ccaeb747ed58da65d7464'};
const at=p=>path.join(root,p);
const blob=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
for(const k of Object.keys(rel))assert.equal(blob(fs.readFileSync(at(rel[k]))),pin[k],'Git blob drift '+k);
const base=JSON.parse(fs.readFileSync(at(rel.seed),'utf8'));
const dup=x=>JSON.parse(JSON.stringify(x)),perms=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
function transport(p,perm){
 assert.equal(p.rule,'AND3');assert.equal(p.support.length,3);
 const old=p.support.slice(),value=p.table,next=perm.map(i=>old[i]);let tab=0;
 for(let mask=0;mask<8;mask++){
  let oldMask=0;
  for(let j=0;j<3;j++)oldMask|=((mask>>next.indexOf(old[j]))&1)<<j;
  tab|=((value>>oldMask)&1)<<mask;
 }
 p.support=next;p.table=tab;
}
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3_594_'));
const rows=[];
try{
 function run(name,d,want){
  const f=path.join(dir,name+'.json');fs.writeFileSync(f,JSON.stringify(d)+'\n');
  const r=cp.spawnSync(process.execPath,[at(rel.checker),f],{encoding:'utf8',timeout:25000,maxBuffer:2**22});
  const accepted=r.status===0;
  assert.equal(accepted,want,'wrong original CLI verdict: '+name+' '+r.stderr);
  const parsed=accepted?JSON.parse(r.stdout):null;
  rows.push({name,accepted,expected_accept:want,
   assertions:parsed?.assertions??parsed?.checks??null,
   rejection:accepted?null:r.stderr.slice(0,300),
   packet_sha256:crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex')});
 }
 run('baseline',base,true);
 const rev=dup(base);for(const f of rev.fixtures)for(const p of f.proof)if(p.rule==='AND3')transport(p,perms[5]);
 run('all_reversed',rev,true);
 for(let i=0;i<6;i++){const d=dup(base);transport(d.fixtures[0].proof[0],perms[i]);run('K4_perm_'+i,d,true)}
 const varied=dup(base);let k=0;for(const f of varied.fixtures)for(const p of f.proof)if(p.rule==='AND3')transport(p,perms[k++%6]);
 run('all_varied',varied,true);
 const k4=dup(base);k4.fixtures=[k4.fixtures[0]];k4.summary=[k4.summary[0]];
 for(const p of k4.fixtures[0].proof)if(p.rule==='AND3')transport(p,perms[5]);
 run('K4_reversed',k4,true);
 for(let i=0;i<5;i++){
  const d=dup(base),p=d.fixtures[0].proof[0];
  if(i===0)p.support.reverse();
  if(i===1){transport(p,perms[5]);p.table^=1}
  if(i===2)p.support=[0,0,1];
  if(i===3){transport(d.fixtures[0].proof[2],perms[3]);d.fixtures[0].proof[2].row.mask='0x3'}
  if(i===4)p.support=[0,1,8];
  run('hostile_'+i,d,false);
 }
 const manifest={id:'LSPV-3/594',execution:'actual Node OS subprocesses of unchanged archived /341',
 checker_blob:pin.checker,seed_blob:pin.seed,total_AND3:246,positive:10,hostile:5,rows};
 const target=process.argv[2]||path.join(root,'results/raw/arc/2026-11-12_1124_LSPV3_594_TYPED_SUPPORT_PERMUTATION_OS_RAW.json');
 fs.mkdirSync(path.dirname(path.resolve(target)),{recursive:true});
 fs.writeFileSync(target,JSON.stringify(manifest,null,2)+'\n');
 console.log(JSON.stringify({status:'PASS',cases:rows.length,positive:10,hostile:5,results_file:target}));
}finally{fs.rmSync(dir,{recursive:true,force:true})}

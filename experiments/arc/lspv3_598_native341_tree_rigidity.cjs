'use strict';
// LSPV-3/598. Run: node experiments/arc/lspv3_598_native341_tree_rigidity.cjs
// Uses exact archived original checker, not a replacement mathematical verifier.
// Emits machine-readable outcomes; all historical rule weights remain unchanged.
const fs=require('fs'),crypto=require('crypto'),vm=require('vm'),assert=require('assert');
const SOURCE='experiments/arc/lspv2_341_independent_verify.js';
const CORPUS=[
'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json',
'results/raw/arc/2026-11-12_1440_LSPV3_597_NATIVE341_CHARGE_FLIP_EDGE0_ACCEPTED.json',
'results/raw/arc/2026-11-12_1124_LSPV3_594_K4_REVERSED_ALL12_ACCEPTED.json',
'results/raw/arc/2026-11-12_0728_LSPV3_590_NULL_SOURCE_OBJECT_TERMINAL_NATIVE341.json',
'results/raw/arc/2026-11-12_1325_LSPV3_596_K4_OBJECT_SUMMARY_ACCEPTED.json',
'results/raw/review/2026-11-12_1348_LSPV5_511_SUPPORT_STRING_ACCEPTED.json',
'results/raw/arc/2026-11-11_1824_LSPV3_582_STRING_CHARGE_SAT_ACCEPTED_PACKET.json',
'results/raw/arc/2026-11-12_0827_LSPV3_591_NATIVE341_ALL_SEVEN_ARRAY_MASKS_ACCEPTED.json'
];
function gitBlobSHA(s) {return crypto.createHash('sha1').update('blob '+Buffer.byteLength(s)+'\0').update(s).digest('hex');}
const checker=fs.readFileSync(SOURCE,'utf8');
assert.strictEqual(gitBlobSHA(checker),'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
function runNative(raw){
 let result=null;
 try{
  vm.runInNewContext(checker,{
   require:mod=>{if(mod!=='fs')throw Error('unexpected module');return {readFileSync:()=>raw};},
   process:{argv:['node',SOURCE,'virtual-raw-packet.json']},
   console:{log:s=>{result=JSON.parse(s);}}
  },{timeout:300000,filename:SOURCE});
  if(!result || typeof result.checks!=='number')throw Error('missing original result');
  return {accepted:true,checks:result.checks};
 }catch(e){return {accepted:false,error:String(e)};}
}
function audit(f){
 const m=f.clauses.length,q=f.proof.length,byId=new Map(),fan=new Map(),visited=new Set();
 for(const s of f.clauses){assert(!byId.has(s.id));byId.set(s.id,s);fan.set(s.id,0);}
 for(const p of f.proof){assert(!byId.has(p.id));byId.set(p.id,p);fan.set(p.id,0);}
 for(const p of f.proof)for(const id of p.parents){assert(byId.has(id));fan.set(id,fan.get(id)+1);}
 const sink=f.proof[f.proof.length-1].id;
 function dfs(id){if(visited.has(id))return;visited.add(id);const v=byId.get(id);if(v.parents)for(const j of v.parents)dfs(j);}
 dfs(sink);
 const others=[...f.clauses,...f.proof].filter(v=>v.id!==sink);
 const once=others.every(v=>fan.get(v.id)===1);
 const all=visited.size===m+q;
 const tree=(2*q===m+q-1);
 assert(once&&all&&tree&&fan.get(sink)===0);
 return {graph:String(f.graph.name),sources:m,paid_nodes:q,edges:2*q,terminal_ancestor_nodes:visited.size,
  tree,all_nodes_ancestors:all,all_nonterminal_single_use:once,terminal_fanout:fan.get(sink)};
}
const positives=CORPUS.map(path=>{
 const raw=fs.readFileSync(path,'utf8'),v=runNative(raw);
 assert(v.accepted,'original checker rejected '+path+': '+v.error);
 const packet=JSON.parse(raw);
 return {path,blob_sha:gitBlobSHA(raw),bytes:Buffer.byteLength(raw),...v,fixtures:packet.fixtures.map(audit)};
});
const base=JSON.parse(fs.readFileSync(CORPUS[0],'utf8'));
const mutations=[
 ['duplicate_parents',x=>{x.fixtures[0].proof[0].parents[1]=x.fixtures[0].proof[0].parents[0];}],
 ['extra_dead_paid_record',x=>{x.fixtures[0].proof.push({...x.fixtures[0].proof[0],id:'extra_dead',parents:['s0','s1']});}],
 ['lost_paid_record',x=>{x.fixtures[0].proof.pop();}],
 ['reused_source_parent',x=>{x.fixtures[0].proof[1].parents[0]='s0';}],
 ['reused_derived_parent',x=>{x.fixtures[0].proof[x.fixtures[0].proof.length-1].parents[0]=x.fixtures[0].proof[0].id;}],
 ['missing_original_source',x=>{x.fixtures[0].clauses.pop();}]
];
const negatives=mutations.map(([name,mutate])=>{const cp=JSON.parse(JSON.stringify(base));mutate(cp);const verdict=runNative(JSON.stringify(cp));assert(!verdict.accepted,'hostile accepted: '+name);return {name,...verdict};});
const summary={original_checker_blob:gitBlobSHA(checker),accepted_packets:positives.length,
 accepted_fixtures:positives.reduce((z,p)=>z+p.fixtures.length,0),
 positive_original_assertions:positives.reduce((z,p)=>z+p.checks,0),
 hostile_rejections:negatives.length,all_observed_accepted_trees:true,
 status:'PROVED/RESTRICTED from original checker logic; finite replays COMPUTATIONAL; P versus NP OPEN'};
const result={summary,positives,negatives};
const dest=process.argv[2];
if(dest)fs.writeFileSync(dest,JSON.stringify(result,null,2)+'\n');
process.stdout.write(JSON.stringify(result,null,2)+'\n');

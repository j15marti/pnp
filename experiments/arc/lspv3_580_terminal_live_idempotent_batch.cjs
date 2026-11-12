#!/usr/bin/env node
'use strict';
/* LSPV-3/580: exact terminal-live idempotent-copy batch replayer.
   Execute at j15marti/pnp repository root:
      node experiments/arc/lspv3_580_terminal_live_idempotent_batch.cjs
   Optionally pass raw-output path as first CLI argument.
   This script constructs certificates but is NOT the authoritative checker.
   It invokes the unchanged historical sibling /386 Node.js checker by subprocess.
   Its input SHA-1 pins are actual Git blob digests, not SHA-256 filenames.
*/
const fs=require('fs'),os=require('os'),path=require('path'),crypto=require('crypto'),cp=require('child_process'),assert=require('assert');
const ROOT=path.resolve(__dirname,'../..');
const CHECK=path.join(ROOT,"experiments/arc/lspv2_386_independent_verify.js");
const SEED=path.join(ROOT,"results/raw/arc/2026-11-11_1224_LSPV3_576_COMPLEMENTARY_NATIVE_ACCEPTED_PACKET.json");
const OUTPUT=path.join(ROOT,"results/raw/arc/2026-11-11_1624_LSPV3_580_TERMINAL_LIVE_IDEMPOTENT_BATCH_PACKET.json");
const EXPECTED_CHECK="338305c0ce101704205e57543756b8127074a986";
const EXPECTED_SEED="6cd8f803ccfbced3c04c3ab0e3114b76215f8d21";
function gitBlob(file){
 const b=fs.readFileSync(file);
 return crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
}
assert.strictEqual(gitBlob(CHECK),EXPECTED_CHECK,'original checker blob changed');
assert.strictEqual(gitBlob(SEED),EXPECTED_SEED,'original accepted seed blob changed');
const seed=JSON.parse(fs.readFileSync(SEED,'utf8'));
const clone=x=>JSON.parse(JSON.stringify(x));
const order=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const chosen=[0,3,5,6];
function build(m){
 assert(Number.isInteger(m)&&m>=0&&m<=4);
 const d=clone(seed);
 assert.strictEqual(d.records.length,80);
 assert.strictEqual(d.records[76].kind,'DEF');
 assert.strictEqual(d.records[77].kind,'DEF');
 assert.strictEqual(d.records[78].kind,'RES');
 assert.deepStrictEqual(d.records[79].c,[]);
 d.gate_defs=[[0,20,1,1]];d.records.splice(76,3);
 const add=[{kind:'DEF',c:[1,-20],parents:[],gate:0},{kind:'DEF',c:[-1,20],parents:[],gate:0}],copy=new Map();
 for(const s of chosen.slice(0,m)){
  const C=d.records[s].c;
  assert(C.includes(1));
  const i=17+add.length;
  add.push({kind:'RES',c:order([...C.filter(x=>x!==1),20]),parents:[s,18],pivot:1});
  add.push({kind:'RES',c:C.slice(),parents:[i,17],pivot:20});
  copy.set(s,i+1);
 }
 const L=add.length;
 for(const r of d.records.slice(17))
  r.parents=r.parents.map(p=>copy.has(p)?copy.get(p):(p>=17?p+L:p));
 d.records.splice(17,0,...add);
 d.summary={source:49,def_views:2,resolution:28+2*m,paid_gates:1,paid_total:29+2*m,live_records:d.records.length};
 assert.deepStrictEqual(d.records.filter(r=>r.kind==='SOURCE'),seed.records.filter(r=>r.kind==='SOURCE'));
 return d;
}
function ancestors(p){
 const seen=new Set();
 function walk(i){if(seen.has(i))return;seen.add(i);for(const j of p.records[i].parents)walk(j);}
 walk(p.records.length-1);return seen;
}
const directory=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-580-'));
let checks=0;
function replay(d,label){
 const f=path.join(directory,label+'.json');fs.writeFileSync(f,JSON.stringify(d));
 const run=cp.spawnSync(process.execPath,[CHECK,f],{cwd:ROOT,encoding:'utf8',timeout:20000,maxBuffer:8*1024*1024});
 checks++;
 if(run.error)return {accepted:false,stderr:String(run.error),stdout:run.stdout||''};
 let parsed=null;try{parsed=JSON.parse(run.stdout);}catch(e){}
 return {accepted:run.status===0,status:run.status,stdout:run.stdout,stderr:run.stderr,parsed};
}
try{
 const positives=[];
 for(let m=0;m<=4;m++){
  const pkt=build(m),r=replay(pkt,'positive'+m);
  assert(r.accepted,'original checker rejected positive '+m+' '+r.stderr);
  assert.strictEqual(r.parsed.paid,29+2*m);
  assert.strictEqual(r.parsed.negativeTests,11);
  if(m){
   const anc=ancestors(pkt);
   for(let i=17;i<17+2+2*m;i++)assert(anc.has(i),'terminal-dead row '+i);
  }
  positives.push({m,paid:r.parsed.paid,records:pkt.records.length,original_assertions:r.parsed.assertions,def_views:2});
 }
 const final=build(4),bytes=JSON.stringify(final);
 assert.strictEqual(Buffer.byteLength(bytes),5582);
 assert.strictEqual(bytes,fs.readFileSync(OUTPUT,'utf8'),'committed witness drift');
 const mutations=[
 ['forged_source',o=>{o.records[0].c[0]=-1}],
 ['false_facet',o=>{o.records[17].c=[-20]}],
 ['bad_pivot',o=>{o.records[19].pivot=2}],
 ['future_parent',o=>{o.records[20].parents[0]=o.records.length+10}],
 ['bad_resolvent',o=>{o.records[20].c=[-1,2,3,-19]}],
 ['missing_paid_owner',o=>{o.gate_defs=[]}],
 ['underpayment',o=>{o.summary.paid_total--}],
 ['forged_gate_owner',o=>{o.records[18].gate=9}],
 ['wrong_original_charge',o=>{o.spec.charge[0]=0}]
 ];
 const negative=[];
 for(const [name,change] of mutations){
  const p=clone(final);change(p);const r=replay(p,'hostile_'+name);
  assert(!r.accepted,'hostile accepted '+name);
  negative.push({name,status:'REJECT',stderr:(r.stderr||'').trim().slice(0,600)});
 }
 const out={status:'PASS',model:'unchanged archived /386 original OS Node subprocess, NOT historical full R_mix341',
 original_checker_blob:EXPECTED_CHECK,seed_blob:EXPECTED_SEED,positive:positives,hostile:negative,
 source_unchanged:true,terminal_live_added_m4:10,logical_W_m4:37,
 native_invocations:checks,P_versus_NP:'OPEN'};
 if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out,null,2)+'\n');
 console.log(JSON.stringify(out,null,2));
}finally{fs.rmSync(directory,{recursive:true,force:true});}

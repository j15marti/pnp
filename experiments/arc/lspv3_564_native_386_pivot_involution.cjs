#!/usr/bin/env node
'use strict';
// LSPV-3/564: OS Node replay of unmodified archived /386 checker.
// Does not authenticate the missing historical full R_mix341 calculus.
const assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const repo=path.resolve(__dirname,'../..');
const verifier=path.join(repo,'experiments/arc/lspv2_386_independent_verify.js');
const packet=path.join(repo,'results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json');
function blob(b){return crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex')}
const B=fs.readFileSync(packet),V=fs.readFileSync(verifier);
assert.equal(blob(B),'08aa169b5db49b2ddd1cb5a9b6890fcc3b790916');
assert.equal(blob(V),'338305c0ce101704205e57543756b8127074a986');
const base=JSON.parse(B),copy=x=>JSON.parse(JSON.stringify(x)),res=base.records.flatMap((r,i)=>r.kind==='RES'?[i]:[]);
assert.equal(res.length,51);
function flip(indices){const p=copy(base);for(const i of indices){let r=p.records[i];assert.equal(r.kind,'RES');assert.notEqual(r.parents[0],r.parents[1]);r.parents.reverse();r.pivot=-r.pivot}return p}
function normalize(p){let q=copy(p);for(let r of q.records)if(r.kind==='RES'&&r.pivot<0){r.parents.reverse();r.pivot=-r.pivot;}return q}
assert.deepEqual(normalize(base),base);
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-lspv3-564-'));
let attempts=0,fullAssertions=0;
function check(p,expected,label){
 const f=path.join(tmp,String(attempts++)+'.json');fs.writeFileSync(f,JSON.stringify(p)+'\n');
 const x=cp.spawnSync(process.execPath,[verifier,f],{encoding:'utf8',timeout:30000,maxBuffer:4*1024*1024});
 const accepted=x.status===0&&!x.error;
 assert.equal(accepted,expected,label+': '+String(x.stderr||x.error||x.stdout).slice(0,300));
 if(!accepted)return {name:label,accepted:false,error:String(x.stderr||x.error).split('\n')[0]};
 const info=JSON.parse(x.stdout);
 for(const [k,v] of Object.entries({paid:53,res:51,def:2,records:74,sources:17,negativeTests:11,assertions:4663}))assert.equal(info[k],v,label+' '+k);
 fullAssertions+=info.assertions;return {name:label,accepted:true};
}
let seed=0x56312024>>>0;
function next(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0}
const out={experiment:'LSPV-3/564',verifier_blob:blob(V),packet_blob:blob(B),
  accepted_paid_work:53,source_count:17,owner_count:2,facet_count:6,resolution_count:51,
  distinct_orientation_certificate_count:'2^51',
  singles:0,full:0,random:0,corruptions:[],native_node_executed:true};
try{
 check(base,true,'base');
 for(const i of res){const p=flip([i]);assert.deepEqual(normalize(p),base);check(p,true,'single-'+i);out.singles++;}
 const full=flip(res);assert.deepEqual(normalize(full),base);check(full,true,'all-flipped');out.full++;
 for(let j=0;j<64;j++){const p=flip(res.filter(()=>((next()>>>14)&1)===1));assert.deepEqual(normalize(p),base);check(p,true,'random-'+j);out.random++;}
 const neg=[
  ['swap_only',p=>p.records[23].parents.reverse()],
  ['negate_only',p=>p.records[23].pivot=-p.records[23].pivot],
  ['zero_pivot',p=>p.records[23].pivot=0],
  ['bad_source',p=>p.records[0].c[0]=-p.records[0].c[0]],
  ['underpaid',p=>p.summary.paid_total--],
  ['duplicate_owner',p=>p.gate_defs[1][0]=0],
  ['forward_parent',p=>p.records[23].parents[0]=23],
  ['bad_facet',p=>p.records[22].c[0]=-p.records[22].c[0]]
 ];
 for(const [name,mut] of neg){let p=copy(base);mut(p);out.corruptions.push(check(p,false,name))}
 out.full_checker_assertion_groups=fullAssertions;out.status='PASS';
 console.log(JSON.stringify(out,null,2));
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
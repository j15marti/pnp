#!/usr/bin/env node
'use strict';
const fs=require('fs'),cp=require('child_process'),crypto=require('crypto'),os=require('os'),path=require('path');
const verifier=process.argv[2]||'lspv5_477_historical_verifier.js';
const baseline=process.argv[3]||'lspv5_477_baseline.json';
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const run=obj=>{
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-478-'));
 const p=path.join(dir,'packet.json');fs.writeFileSync(p,JSON.stringify(obj,null,2)+'\n');
 const r=cp.spawnSync(process.execPath,[verifier,p],{encoding:'utf8'});fs.rmSync(dir,{recursive:true,force:true});
 return {accepted:r.status===0,status:r.status,stdout:r.stdout,stderr:r.stderr,packet:JSON.stringify(obj,null,2)+'\n'};
};
const data=JSON.parse(fs.readFileSync(baseline,'utf8'));
const base=run(data);if(!base.accepted)throw Error('baseline rejected');
const forged=structuredClone(data),f=forged.fixtures[0];
forged.version='FORGED-UNAUTHENTICATED-SOURCE';
forged.claimedOriginalSourceSHA256='0'.repeat(64); // unrecognized and unchecked
f.graph.name='FORGED-K4-EXTERNAL-SOURCE';
const rename=new Map();
for(const [i,c] of f.clauses.entries()){
 rename.set(c.id,`forged-source-${i}`);c.id=`forged-source-${i}`;
 c.pattern=`forged-pattern-${i}`;c.literals.push(c.literals.shift());
}
for(const p of f.proof)p.parents=p.parents.map(x=>rename.get(x)||x);
for(const d of f.deleted)d.sourceId=rename.get(d.sourceId)||d.sourceId;
const good=run(forged);
const brokenRef=structuredClone(forged);brokenRef.fixtures[0].proof[0].parents[0]='unbound-source';
const badRef=run(brokenRef);
const badSem=structuredClone(forged);badSem.fixtures[0].clauses[0].literals[0]*=-1;
const badSemRun=run(badSem);
const out={
 run:'LSPV-5/478',status:'COMPUTATIONAL ACCEPTED SOURCE-IDENTITY FORGERY',
 baseline:{accepted:base.accepted,stdout_sha256:sha(base.stdout),checks:JSON.parse(base.stdout).checks},
 forged:{accepted:good.accepted,packet_sha256:sha(good.packet),stdout_sha256:sha(good.stdout),checks:good.accepted?JSON.parse(good.stdout).checks:null,
   graph_name:f.graph.name,source_ids_renamed:f.clauses.length,literal_arrays_rotated:f.clauses.length,
   patterns_replaced:f.clauses.length,claimed_digest:forged.claimedOriginalSourceSHA256,
   verifier_has_external_source_argument:false,verifier_checks_claimed_digest:false},
 controls:{unbound_parent_rejected:!badRef.accepted,semantic_sign_change_rejected:!badSemRun.accepted},
 conclusion:'The pinned verifier checks a self-contained semantic fixture, but does not bind it to separately authenticated original source bytes/hash/coordinates. Coordinated source-ID renaming, ignored pattern/name changes, literal-byte reordering, and a forged claimed digest are accepted.',
 scope:'This is a P2-D1 original-source-authentication failure for the pinned subset verifier, not a semantic refutation unsoundness proof and not authority for the complete historical R_mix341 calculus.'
};
fs.writeFileSync('lspv5_478_source_identity_forged_accepted.json',good.packet);
fs.writeFileSync('lspv5_478_source_identity_forgery_raw.json',JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify(out,null,2));

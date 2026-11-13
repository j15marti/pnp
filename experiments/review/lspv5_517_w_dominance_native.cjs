#!/usr/bin/env node
'use strict';
/* LSPV-5/517. Native OS replay of the /517 dominance packets plus the two peer
 * runners (LSPV-3/604, LSPV-4/576 --native) whose OS execution was outstanding.
 * Usage (repo root): python3 experiments/review/lspv5_517_w_dominance_redteam.py DIR
 *                    node experiments/review/lspv5_517_w_dominance_native.cjs DIR [out.json]
 * Each checker trial is a fresh subprocess of the UNCHANGED /386 CLI.  For gate-free
 * packets the unchanged checkProof body is additionally evaluated in-process with
 * control=true (hosted, labelled as such) to separate CLI-sentinel rejection from
 * logical rejection.  Does not implement R_mix341. */
const fs=require('fs'),path=require('path'),cp=require('child_process'),crypto=require('crypto'),assert=require('assert/strict');
const root=path.resolve(__dirname,'../..'),dir=path.resolve(process.argv[2]);
const rel='experiments/arc/lspv2_386_independent_verify.js',checker=path.join(root,rel);
const blob=b=>crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
const src=fs.readFileSync(checker);assert.equal(blob(src),'338305c0ce101704205e57543756b8127074a986');
const body=src.toString('utf8');const cut=body.indexOf('function corrupt(');assert(cut>0);
const checkProof=new Function('require',body.slice(0,cut)+'\nreturn checkProof;')(require);
const run=(args)=>{const o=cp.spawnSync(process.execPath,args,{encoding:'utf8',timeout:30000,maxBuffer:8e6});
 return {status:o.status,err:(o.stderr||'').split('\n').find(x=>x.startsWith('Error:'))||'',stdout:o.stdout};};
const expect={'W28_dead_gate_deleted.json':{cli:false,paid:28},'DP_best_pure_RES.json':{cli:false,paid:28},
 'W30_dead_duplicate_res.json':{cli:true,paid:30},'W39_tree_unrolled_idx23.json':{cli:true,paid:39}};
const out={tag:'LSPV-5/517',checkerBlob:'338305c0ce101704205e57543756b8127074a986',packets:[],peers:{}};
for(const [f,e] of Object.entries(expect)){
 const p=path.join(dir,f),raw=fs.readFileSync(p),r=run([checker,p]);
 const row={file:f,sha256:crypto.createHash('sha256').update(raw).digest('hex'),bytes:raw.length,cliExit:r.status,cliError:r.err};
 if(r.status===0){const j=JSON.parse(r.stdout.trim());Object.assign(row,{paid:j.paid,res:j.res,def:j.def,oddModels:j.oddModels});}
 try{const h=checkProof(JSON.parse(raw),{control:true});row.hostedCore={accept:true,paid:h.paid,res:h.res,def:h.def,oddModels:h.oddModels};}
 catch(x){row.hostedCore={accept:false,error:String(x.message)};}
 assert.equal(r.status===0,e.cli,f+' CLI verdict');assert.equal(row.hostedCore.accept,true,f+' core');
 assert.equal(row.hostedCore.paid,e.paid,f+' paid');
 if(!e.cli)assert.equal(r.err,'Error: accepted a corrupted proof',f+' sentinel');
 out.packets.push(row);
}
const r604=run([path.join(root,'experiments/arc/lspv3_604_restored_signed_source_replay.cjs')]);
assert.equal(r604.status,0,r604.err);const j604=JSON.parse(r604.stdout);
out.peers.lspv3_604={exit:0,positive:j604.originalVerifierPositive,hostileBadPivotRejected:j604.hostileBadPivotRejected,hostileError:j604.hostileError};
const r576=run([path.join(root,'experiments/arc/lspv4_576_dual_native_reference_accounting.cjs'),'--native']);
assert.equal(r576.status,0,r576.err);const j576=JSON.parse(r576.stdout);
out.peers.lspv4_576={exit:0,nativeLogicalW:j576.original386.sharedDag.nativeLogicalW,unfoldedNaiveWork:j576.original386.sharedDag.unfoldedNaiveWork,
 native:j576.native.map(n=>({tag:n.tag,exit:n.exit}))};
out.py=JSON.parse(fs.readFileSync(path.join(dir,'py_summary.json')));
const s=JSON.stringify(out,null,2)+'\n';if(process.argv[3])fs.writeFileSync(process.argv[3],s);process.stdout.write(s);

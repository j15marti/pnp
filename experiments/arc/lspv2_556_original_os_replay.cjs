#!/usr/bin/env node
'use strict';
// LSPV-2/556, original archived /386 OS process; NOT full R_mix341 checker.
// node experiments/arc/lspv2_556_original_os_replay.cjs [output.json]
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const crypto=require('node:crypto'),cp=require('node:child_process');
const root=path.resolve(__dirname,'../..'),loc=p=>path.join(root,p);
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const blob=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
const chk=(ok,msg)=>{if(!ok)throw Error(msg)};
const checker=loc('experiments/arc/lspv2_386_independent_verify.js');
const runner=loc('experiments/arc/lspv2_555_live_def_res_splice.cjs');
const seed=loc('results/raw/arc/2026-11-11_0316_LSPV2_554_ACCEPTED_GATE_ORDER_012.json');
const pinned={checker:'338305c0ce101704205e57543756b8127074a986',runner:'49543130d987250db056eb719027659d81999b86',seed:'afd43c6cdc2e40fefc3c9623bb14fdf8e5b89865'};
for(const [n,f] of Object.entries({checker,runner,seed}))chk(blob(fs.readFileSync(f))===pinned[n],n+' original blob drift');
const expected={
 positive_k_0:[true,3039,31,3329,'c48cf3ac7c6fefc28740a95da62fedd15e86cdc6785877dd221d3e2bd3710af7'],
 positive_k_1:[true,3213,33,3509,'639a49f78d80342ca5a996bf0de9b1f37b284a6a384df92b454e9bc0e690acee'],
 positive_k_2:[true,3334,35,3641,'622e81667fe6cde6b5874753b4bfa42b1084da2b7965d7f7b037d3367f39688b'],
 positive_k_4:[true,3576,39,3905,'49bfb3c267f753a30a642a2efb1ebf06faa384985016beeed8396c24b398ba28'],
 positive_k_16:[true,5028,63,5489,'a77725348a96d00d1e378c0982e40fc7a8bbc107446ca16ee4d45d558452fb49'],
 wrong_signed_facet:[false,3212,33,0,'2c3b7b6e56c1a29d72ba4f814fcaa2fbc432c43fbb98b3a43085b2fe2173049e'],
 wrong_first_pivot:[false,3214,33,0,'1896f426ae8366ed351093a3dcbc98e54593973cd283c23f2a295fc78529cae7'],
 wrong_second_pivot:[false,3212,33,0,'089fff1e501b0df728cb1e0adbc73126eeb07a2e96a5dd740723d7599f677e34'],
 wrong_second_resolvent:[false,3210,33,0,'354b1cbee8a076f325b41b7c37de76a257afb1530de80225170fd68ec26b83b5'],
 future_parent:[false,3214,33,0,'9f356d5f8c84bc52e0cf9f2a7c436b5ff45b1bb0b1ebd91dfc8ebec7a6a6c315'],
 underpaid_summary:[false,3213,31,0,'f399c3487db3ac2591344480599f30b07cb7594f93e30728ecc3039d531d8feb'],
 forged_original_source:[false,3212,33,0,'4b1369a2d1c62ad6da78b3b32a99a3f62de1534a9f59f7e1ba26fab085abe220']
};
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-lspv2-556-'));
let raw;
try{
 const run=cp.spawnSync(process.execPath,[runner,'--emit',tmp],{encoding:'utf8',maxBuffer:1024*1024,timeout:30000});
 chk(!run.error&&run.status===0,'original subprocess runner failed: '+String(run.stderr||run.error).slice(0,1200));
 raw=JSON.parse(run.stdout);chk(raw.accepted===5&&raw.rejected===7&&raw.cases.length===12,'case counts');
 let assertions=0;
 for(const q of raw.cases){
   const e=expected[q.case];chk(e,'unexpected test '+q.case);
   chk(q.accepted===e[0]&&q.bytes===e[1]&&q.paid===e[2]&&q.sha256===e[4],'packet drift '+q.case);
   const bytes=fs.readFileSync(path.join(tmp,q.case+'.json'));
   chk(bytes.length===e[1]&&sha(bytes)===e[4],'exact byte drift '+q.case);
   if(q.accepted){
     chk(q.native.original_assertions===e[3]&&q.native.original_negative_tests===11,'checker internal controls changed '+q.case);
     chk(q.k===0||q.all_splice_nodes_live,'terminal-live splice omitted');
     assertions+=q.native.original_assertions;
   }
 }
 chk(assertions===19873,'positive assertion counts');
}finally{fs.rmSync(tmp,{recursive:true,force:true})}
const result={id:'LSPV-2/556',status:'COMPUTATIONAL',checker_scope:'original /386 SOURCE/DEF/RES sibling, not full R_mix341',node:process.version,platform:process.platform,arch:process.arch,mode:'actual OS Node subprocess',inputs:pinned,readback_cases:12,accepted:5,rejected:7,native_assertions_positive_total:19873,cases:raw.cases.map(q=>({name:q.case,accepted:q.accepted,packet_bytes:q.bytes,sha256:q.sha256,paid:q.paid,sink_depth:q.sink_depth,native_assertions:q.native?.original_assertions||null})),proof_obligations:{'P2-D1':'OPEN','P2-C3':'OPEN','P2-B1':'OPEN','P2-B2/B3':'OPEN'},historical_calculus:'Full R_mix341 parser not obtained; no RES-to-AND3 authentication'};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+'\n');
process.stdout.write(JSON.stringify(result,null,2)+'\n');

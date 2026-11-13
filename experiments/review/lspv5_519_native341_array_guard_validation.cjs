#!/usr/bin/env node
'use strict';
/* LSPV-5/519: independent red-team validation of LSPV-1/610.
 * This executes the unchanged recovered /341 checker and a one-assertion
 * diagnostic guard variant. The guard variant is NOT historical authority.
 */
const fs=require('fs'),os=require('os'),path=require('path'),cp=require('child_process'),crypto=require('crypto');
const root=path.resolve(__dirname,'../..');
const checkerPath=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const producerPath=path.join(root,'experiments/arc/lspv2_341_mixed_tseitin_min_dag.js');
const satPath=path.join(root,'results/raw/arc/2026-11-12_2100_LSPV1_609_BRIDGE_SLICE_SAT_ACCEPTED.json');
const expected={
 checker:'0a8167fc65f324860f60abd2a0e0176d0def968cb6ee7055b6aa1bfd43c255ae',
 producer:'4dd134c4e97fca273668480c64bb220201d67917c2cfe70c471a7bc785e396fc',
 sat:'b1cd6c51b34502801319c47f9c1617cdb53f265c49b09867e3176d262bb8a3a2'
};
function sha(p){return crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');}
function need(b,m){if(!b)throw Error(m);}
need(sha(checkerPath)===expected.checker,'checker hash');need(sha(producerPath)===expected.producer,'producer hash');need(sha(satPath)===expected.sat,'SAT packet hash');
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-519-'));
function run(script,obj,name){
 const inp=path.join(tmp,name+'.json');fs.writeFileSync(inp,JSON.stringify(obj,null,2)+'\n');
 const r=cp.spawnSync(process.execPath,[script,inp],{encoding:'utf8',timeout:20000});
 const accepted=r.status===0;let checks=null;
 if(accepted){const m=r.stdout.match(/"checks"\s*:\s*(\d+)/);checks=m?Number(m[1]):null;}
 return {name,accepted,checks,exit:r.status,rejection:accepted?null:(r.stderr+r.stdout).split('\n').find(x=>x.includes('Verifier:'))||'rejected'};
}
function clone(x){return JSON.parse(JSON.stringify(x));}
function lowMask(x,E){return BigInt.asUintN(E,BigInt(x));}
function repairXors(f){
 const by=new Map(f.clauses.map(c=>[c.id,null]));
 for(const p of f.proof){
   if(p.rule==='AND3'){by.set(p.id,p);continue;}
   const a=by.get(p.parents[0]),b=by.get(p.parents[1]);
   need(a&&b&&a.row&&b.row,'row parents');
   const m=BigInt(a.row.mask)^BigInt(b.row.mask),r=a.row.rhs^b.row.rhs;
   p.row.mask='0x'+m.toString(16);p.row.rhs=r;by.set(p.id,p);
 }
}
function mutateRows(packet,negative){
 const q=clone(packet),f=q.fixtures[0],E=f.graph.edges.length,K=E+17,bit=1n<<BigInt(K);
 const rows=f.proof.filter(p=>p.rule==='AND3'&&p.row).slice(0,2);
 const before=rows.map(p=>BigInt(p.row.mask));
 rows.forEach((p,i)=>{const x=negative?before[i]-bit:before[i]|bit;p.row.mask=x.toString();});
 need(rows.every((p,i)=>lowMask(p.row.mask,E)===lowMask(before[i],E)),'low projection changed');
 repairXors(f);need(BigInt(f.proof.at(-1).row.mask)===0n&&f.proof.at(-1).row.rhs===1,'sink changed');
 return q;
}
function fixtureAudit(f){
 const E=f.graph.edges.length,V=f.graph.n,inc=Array.from({length:V},()=>[]);
 f.graph.edges.forEach(([u,v],e)=>{inc[u].push(e);inc[v].push(e);});
 need(f.proof.filter(p=>p.rule==='AND3').every(p=>Array.isArray(p.support)),'nonarray baseline');
 for(let v=0;v<V;v++){
   const cs=f.clauses.filter(c=>c.vertex===v);need(cs.length===4,'four local clauses');
   for(const c of cs){
     need(Array.isArray(c.literals)&&c.literals.length===3,'signed width');
     need(c.literals.every(Number.isSafeInteger),'safe literal');
     const es=c.literals.map(x=>Math.abs(x)-1).sort((a,b)=>a-b);
     need(es.join(',')===inc[v].slice().sort((a,b)=>a-b).join(','),'incidence');
   }
   need(new Set(cs.map(c=>c.literals.map(x=>x<0?1:0).join(''))).size===4,'distinct patterns');
   const paritySet=new Set(cs.map(c=>c.literals.reduce((x,y)=>x^(y<0?1:0),0)));
   need(paritySet.size===1,'parity set internal');
   need([...paritySet][0]!==f.charges[v],'forbidden parity mismatch');
 }
 return {name:f.graph.name,V,E,arrayAND3:f.proof.filter(p=>p.rule==='AND3').length,sourceClauses:f.clauses.length};
}
function peer578Audit(checkerPath,sat,tmp){
 const hist={};let accepted=0,rejected=0;
 function gate(s){return s.length===3&&new Set(s).size===3&&[0,1,10].every(x=>s.includes(x));}
 for(let code=0;code<65536;code++)for(const side of ['front','back']){
   const u=String.fromCharCode(code),s=side==='front'?'10'+u:u+'10';
   if(!gate(s)){rejected++;continue;}accepted++;
   const n=Buffer.byteLength(JSON.stringify(s),'utf8');hist[n]=(hist[n]||0)+1;
 }
 need(accepted===131068&&rejected===4,'peer578 orbit count');
 need(JSON.stringify(hist)===JSON.stringify({'5':184,'6':3854,'7':122880,'10':4150}),'peer578 histogram');
 const cases=[];
 for(const [label,s,table] of [['front_ascii','10a',153],['back_ascii','a10',195],['front_surrogate','10'+String.fromCharCode(0xD800),153]]){
   const q=clone(sat),p=q.fixtures[0].proof.find(x=>x.id==='d17');p.support=s;p.table=table;
   const r=run(checkerPath,q,'peer578_'+label);need(r.accepted&&r.checks===5155,'peer578 '+label);cases.push(r);
 }
 return {acceptedDecodedStrings:accepted,rejectedLocalCandidates:rejected,literalUtf8BytesHistogram:hist,nativeCases:cases};
}
try{
 const prod=cp.spawnSync(process.execPath,[producerPath],{encoding:'utf8',timeout:20000});need(prod.status===0,'producer');
 const base=JSON.parse(prod.stdout),checker=fs.readFileSync(checkerPath,'utf8');
 const needle='assert(sup.length<=3&&p.support?.length===sup.length&&new Set(p.support).size===sup.length,"AND3 support size");';
 need(checker.split(needle).length===2,'guard insertion site');
 const guarded=checker.replace(needle,'assert(Array.isArray(p.support),"AND3 support array");'+needle);
 const guardedPath=path.join(tmp,'guarded_checker.js');fs.writeFileSync(guardedPath,guarded);
 const audits=base.fixtures.map(fixtureAudit);
 const high=mutateRows(base,false),negative=mutateRows(base,true),sat=JSON.parse(fs.readFileSync(satPath,'utf8'));
 const peer578=peer578Audit(checkerPath,sat,tmp);
 const typed=clone(sat);typed.fixtures[0].proof.find(p=>p.id==='d17').support=[0,1,10];
 const runs=[
   run(checkerPath,base,'baseline_original'),run(guardedPath,base,'baseline_guarded'),
   run(checkerPath,high,'high_masks_original'),run(guardedPath,high,'high_masks_guarded'),
   run(checkerPath,negative,'negative_masks_original'),run(guardedPath,negative,'negative_masks_guarded'),
   run(checkerPath,sat,'sat_string_original'),run(guardedPath,sat,'sat_string_guarded'),
   run(checkerPath,typed,'sat_typed_original')
 ];
 const expect={baseline_original:true,baseline_guarded:true,high_masks_original:true,high_masks_guarded:true,negative_masks_original:true,negative_masks_guarded:true,sat_string_original:true,sat_string_guarded:false,sat_typed_original:false};
 for(const r of runs)need(r.accepted===expect[r.name],'unexpected '+r.name);
 need(audits.every(x=>x.arrayAND3===3*x.V),'baseline rule count');
 const anchors={max_support_three:checker.includes('assert(sup.length<=3&&'),array_missing:!checker.includes('Array.isArray(p.support)'),chronological:checker.includes('const [a,b]=p.parents.map(id=>byId.get(id));assert(a&&b'),low_scope:checker.includes('Array(E).keys()'),exact_sink:checker.includes('BigInt(last.row.mask)===0n&&last.row.rhs===1')};
 need(Object.values(anchors).every(Boolean),'checker anchors');
 const output={schema:'LSPV5-519-NATIVE341-ARRAY-GUARD-VALIDATION/v1',timestamp_pst:'2026-11-12T22:48:00-08:00',status:'PROVED/EXACT restricted checker theorem + COMPUTATIONAL native OS validation; full R_mix341 OPEN',scope:'Pinned recovered /341 SOURCE/AND3/XOR fixture checker only',pins:{checker:{git:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',sha256:expected.checker},producer:{sha256:expected.producer},sat_packet:{git:'8d6d9bc7f2940a77edf2a07fcb72af111ba5b928',sha256:expected.sat}},target:'Falsify LSPV-1/610 array-support soundness boundary',result:'No falsifier under theorem hypotheses; the one-guard implication is independently validated.',proof_audit:{array_equality:'Same length + distinct array elements + numeric union inclusion makes each accepted support a permutation of the exact numeric union.',domain_bound:'Checker enforces union size <=3, so Number shift-count modulo 32 cannot alias the enumerated local domain.',row_projection:'Every accepted alias is checked on all local assignments; high/signed BigInt bits project away above E and exact XOR preserves the low-E equation.',terminal:'Chronological rows ending in exact numeric 0=1 contradict any actual source model.'},checker_anchors:anchors,baseline:audits,mutations:{paired_high_bits:'accepted; low-E projections unchanged and added bit cancels',paired_negative_masks:'accepted; low-E projections unchanged and signed tails cancel',sat_string:'accepted only by original missing-type checker',sat_typed:'rejected by original checker as invalid affine alias'},native_runs:runs,peer_replays:{lspv1_610:{checks:5557412,ordered_pairs:598948},lspv2_591:{accepted:254,rejected:35,subsets:279616},lspv3_606:{positives:11,rejected:7,accepted_checks:56705},lspv4_577:{accepted:1,rejected:4,checks:5155},lspv4_578:peer578},cegar:'The string-support SAT execution remains genuine for the buggy checker. The array-only theorem is a sound under-approximation, not a complete abstraction of accepted bytes.',affected:['P2-D1 remains OPEN','P2-C3 remains OPEN','P2-B1 remains OPEN','P2-B2/B3 remain separate OPEN'],nonClaims:['Diagnostic guard is not the historical grammar','No complete mixed dispatcher','No all-rule cost abstraction','No SAT lower bound or P versus NP result']};
 const out=JSON.stringify(output,null,2)+'\n';if(process.argv[2])fs.writeFileSync(process.argv[2],out);process.stdout.write(out);
}finally{fs.rmSync(tmp,{recursive:true,force:true});}

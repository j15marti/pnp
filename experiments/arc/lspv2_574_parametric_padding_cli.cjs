#!/usr/bin/env node
'use strict';
/*
 LSPV-2/574: source-bound component padding and checker-wrapper minimality.
 Run from project root:
   node experiments/arc/lspv2_574_parametric_padding_cli.cjs
 Uses the ORIGINAL pinned /386 checker in OS child processes. This is not a
 reimplementation or authentication of full historical R_mix341.
*/
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const basePath=path.join(root,'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json');
const checkerPath=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const resultsDir=path.join(root,'results/raw/arc');
fs.mkdirSync(resultsDir,{recursive:true});
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const gitblob=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
const pin={checker:'338305c0ce101704205e57543756b8127074a986',base:'318c52d99977ea4e91bc8554051138a700c1dc94'};
const checker=fs.readFileSync(checkerPath),baseBytes=fs.readFileSync(basePath);
assert.equal(gitblob(checker),pin.checker);
assert.equal(gitblob(baseBytes),pin.base);
const base=JSON.parse(baseBytes);
assert.equal(base.summary.paid_total,29);assert.equal(base.records.length,45);
assert.equal(base.records.filter(r=>r.kind==='SOURCE').length,17);
assert.equal(base.records.filter(r=>r.kind==='RES').length,28);
function ckey(xs){return [...new Set(xs)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}
function edgeIndex(a,b){const pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  return pairs.findIndex(e=>e[0]===a&&e[1]===b);}
function generate(k,owner=true){
 assert(Number.isInteger(k)&&k>=1);
 const h=4*k,m=6*k,g=m+1,z=m+2,edges=[],charges=Array(h).fill(0);charges[0]=1;
 for(let j=0;j<k;j++)for(const [u,v] of [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]])edges.push([4*j+u,4*j+v]);
 const inc=Array.from({length:h},()=>[]);
 edges.forEach(([u,v],i)=>{inc[u].push(i+1);inc[v].push(i+1)});
 function source(v){const xs=inc[v];assert.equal(xs.length,3);const out=[];
  for(let t=0;t<8;t++){
   const bits=[t&1,(t>>1)&1,(t>>2)&1],parity=bits[0]^bits[1]^bits[2];
   if(parity!==charges[v])out.push(ckey([...xs.map((e,j)=>bits[j]?-e:e),-g]));
  }
  assert.equal(out.length,4);return out;
 }
 const transplant=x=> x===7?g:x===-7?-g:x;
 const old=base.records.map(r=>JSON.parse(JSON.stringify(r)));
 const oldSrc=old.slice(0,17).map(r=>({...r,c:r.c.map(transplant)}));
 assert.deepEqual(oldSrc.filter(r=>r.source===0).map(r=>r.c),source(0));
 const newRows=[];
 for(let v=4;v<h;v++)for(const c of source(v))newRows.push({kind:'SOURCE',c,parents:[],source:v});
 const shift=newRows.length;
 const res=old.slice(17).map(r=>({...r,c:r.c.map(transplant),
    parents:r.parents.map(j=>j>=17?j+shift:j),pivot:transplant(r.pivot)}));
 const records=[...oldSrc,...newRows,...res];
 const spec={h,edges,charge:charges,guard:g};
 const gate_defs=owner?[[0,z,1,4]]:[];
 const summary={source:4*h+1,def_views:0,resolution:28,paid_gates:gate_defs.length,
   paid_total:28+gate_defs.length,live_records:records.length};
 assert.equal(records.filter(r=>r.kind==='SOURCE').length,summary.source);
 assert.deepEqual(records.at(-1).c,[]);
 // Independent source binder: every signed original SOURCE occurrence, in its
 // actual record order, must equal the reconstructed guarded cubic source.
 const expected=new Map();for(let v=0;v<h;v++)expected.set(v,source(v).map(JSON.stringify));
 let count=0;for(const r of records.filter(r=>r.kind==='SOURCE')){
   if(r.source===-1){assert.deepEqual(r.c,[g]);count++;continue}
   const bag=expected.get(r.source);assert(bag&&bag.includes(JSON.stringify(r.c)));
   bag.splice(bag.indexOf(JSON.stringify(r.c)),1);count++;
 }
 assert.equal(count,4*h+1);assert([...expected.values()].every(a=>a.length===0));
 // An independent exact signed CNF file is generated and cryptographically bound.
 const dimacs='p cnf '+g+' '+(4*h+1)+'\n'+records.filter(r=>r.kind==='SOURCE').map(r=>r.c.join(' ')+' 0').join('\n')+'\n';
 return {data:{spec,gate_defs,records,summary},dimacs};
}
function run(file){const r=cp.spawnSync(process.execPath,[checkerPath,file],{encoding:'utf8',timeout:45000,maxBuffer:8*1024*1024});
 if(r.error)throw r.error;
 const accepted=r.status===0;let json=null;
 if(accepted)json=JSON.parse(r.stdout.trim());
 return {accepted,exit_status:r.status,assertions:json?.assertions??null,
   paid:json?.paid??null,negativeTests:json?.negativeTests??null,
   diagnostic:accepted?null:(r.stderr.match(/Error: [^\n]+/)||[r.stderr.trim().slice(-240)])[0]};}
// Evaluate the AUTHENTIC original checkProof implementation, without its CLI
// mutation loop, by appending a single invocation inside a throwaway V8 context.
// The historical checker bytes stay unchanged; this is expressly NOT the
// complete original checker acceptance verdict.
function originalInternalCore(certFile,control){
 const source=checker.toString('utf8');
 const trailer='\nconsole.log(JSON.stringify(checkProof(JSON.parse(fs.readFileSync('+
   JSON.stringify(certFile)+',"utf8")),{control:'+Boolean(control)+'})));';
 const messages=[];
 vm.runInNewContext(source+trailer,{require,process:{argv:['node',checkerPath]},
   console:{log:x=>messages.push(x)}},{filename:checkerPath,timeout:45000});
 assert.equal(messages.length,1);return JSON.parse(messages[0]);
}
function span(records){const depths=[];for(const r of records){depths.push(r.kind==='RES'?1+Math.max(...r.parents.map(j=>depths[j])):0)}return depths.at(-1)}
const rows=[];let assertionSum=0;let invalidChecks=0;
for(const k of [1,2,3,4,8,16]){
 const {data,dimacs}=generate(k,true);
 const file=path.join(resultsDir,'574_k'+String(k).padStart(2,'0')+'_W29.json');
 const buffer=Buffer.from(JSON.stringify(data)+'\n');fs.writeFileSync(file,buffer);
 const srcFile=path.join(resultsDir,'574_k'+String(k).padStart(2,'0')+'_SIGNED_SOURCE.cnf');fs.writeFileSync(srcFile,dimacs);
 const outcome=run(file),expect=k!==2;
 assert.equal(outcome.accepted,expect,'W29 k='+k);
 if(expect){assert.equal(outcome.paid,29);assert.equal(outcome.negativeTests,11);assertionSum+=outcome.assertions;invalidChecks+=11;}
 rows.push({k,h:data.spec.h,edges:data.spec.edges.length,source_records:data.summary.source,
   logical_work:29,proof_resolution_span:span(data.records),certificate_bytes:buffer.length,certificate_sha256:sha(buffer),
   external_source_bytes:Buffer.byteLength(dimacs),external_source_sha256:sha(dimacs),
   owner_present:true,...outcome});
 // Delete a completely UNUSED paid owner and update the declared cost correctly.
 // Core math RES proof is intact. Complete CLI still rejects because its own
 // built-in remove-owner negative test is a no-op on an empty owner list.
 const cheaper=generate(k,false).data;
 const cheaperFile=path.join(resultsDir,'574_k'+String(k).padStart(2,'0')+'_W28_OWNERLESS.json');
 const cheaperBuffer=Buffer.from(JSON.stringify(cheaper)+'\n');fs.writeFileSync(cheaperFile,cheaperBuffer);
 const r=run(cheaperFile);assert.equal(r.accepted,false,'ownerless k='+k);
 const exactCore=originalInternalCore(cheaperFile,k!==2);
 assert.equal(exactCore.paid,28,'unchanged internal checker core W28 k='+k);
 rows.push({k,h:cheaper.spec.h,edges:cheaper.spec.edges.length,source_records:cheaper.summary.source,
  logical_work:28,proof_resolution_span:span(cheaper.records),certificate_bytes:cheaperBuffer.length,certificate_sha256:sha(cheaperBuffer),
  external_source_sha256:sha(dimacs),owner_present:false,original_internal_core_accepted:true,
  internal_core_controlled:k!==2,internal_core_paid:exactCore.paid,...r});
}
// Four independently tampered negative packets, checked by the real CLI.
const positives=generate(3,true).data;const clone=x=>JSON.parse(JSON.stringify(x));
const falsifiers=[
 ['source_polarity',d=>{d.records[0].c[0]*=-1;}],
 ['underpaid',d=>{d.summary.paid_total--;}],
 ['gate_collides_original_wire',d=>{d.gate_defs[0][1]=8;}],
 ['bad_terminal_pivot',d=>{d.records.at(-1).pivot=999999;}]
];
for(const [name,mutation] of falsifiers){const d=clone(positives);mutation(d);
 const file=path.join(resultsDir,'574_NEGATIVE_'+name+'.json');const b=Buffer.from(JSON.stringify(d)+'\n');fs.writeFileSync(file,b);
 const r=run(file);assert.equal(r.accepted,false,name);
 rows.push({name,logical_work:d.summary.paid_total,certificate_bytes:b.length,certificate_sha256:sha(b),...r});
}
const output={id:'LSPV-2/574',timestamp_pacific:'2026-11-12 05:12 PST',status:'PROVED/RESTRICTED + COMPUTATIONAL',
 model:'unchanged restricted /386 SOURCE/DEF/RES native JSON original checker; not R_mix341 full',
 source_checker_pins:pin,presentation:'raw UTF-8 JSON plus LF',
 theorem:'For any k>=3, k disjoint K4 graph source components with only the first charged oddly have an original-checker-accepted W29 refutation using exactly 28 RES and one unused paid AND2 owner. Removing the unused paid owner yields a mathematically valid W28 RES-only derivation but the unchanged complete CLI rejects via its no-op owner-removal internal corruption test.',
 proof_scope:'No nontrivial lower bound; disconnected padding is not source-clause essential. Unknown mixed-rule operations remain MAY.',
 expected_results:'For k=1 and k>=3, W29 CLI accept and W28 CLI reject despite acceptance of the unchanged original internal checkProof; k=2 W29 rejects due disconnected parity self-test and W28 CLI rejects; all four tamper controls rejected.',
 tested_k:[1,2,3,4,8,16],records:rows,original_checker_accepted_assertion_groups:assertionSum,
 original_checker_builtin_negative_controls:invalidChecks,
 evidence_count:rows.length,
 resources:{logical_work:'declared paid node count',certificate_bits:'certificate_bytes * 8',
  span:'max RES parent-chain depth with sources at depth zero; gate definition unused',
  construction_wall_time_ms:null,checker_wall_time_ms:null,peak_space_bytes:null,
  note:'Timing and peak memory deliberately not claimed; these are distinct from logical work'},
 open:['P2-D1','P2-C3','P2-B1','P2-B2','P2-B3'],p_versus_np:'OPEN'};
const rendered=JSON.stringify(output,null,2)+'\n';
fs.writeFileSync(path.join(resultsDir,'2026-11-12_0512_LSPV2_574_COMPONENT_PADDING_CLI_RAW.json'),rendered);
console.log(JSON.stringify({status:'PASS',cases:rows.length,accepted:rows.filter(r=>r.accepted).length,rejected:rows.filter(r=>!r.accepted).length,
  original_assertions:assertionSum,negative_controls:invalidChecks,
  accepted_k:rows.filter(r=>r.accepted).map(r=>r.k),original_checker_pin:pin.checker},null,2));

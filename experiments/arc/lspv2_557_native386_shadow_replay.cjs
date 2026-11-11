#!/usr/bin/env node
'use strict';
// LSPV-2/557. Differential corpus for archived /386, NOT full R_mix341.
// Usage: node experiments/arc/lspv2_557_native386_shadow_replay.cjs [raw-output.json] [packet-dir]
// Uses original archived checker unmodified in actual Node OS subprocesses.
// Published reference generator; the hosted research run separately executed
// all 15 cases against its unchanged checkProof mathematical body in V8.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const crypto=require('node:crypto'),cp=require('node:child_process');
const root=path.resolve(__dirname,'../..');
const loc=p=>path.join(root,p);
const checker=loc('experiments/arc/lspv2_386_independent_verify.js');
const seed=loc('results/raw/arc/2026-11-11_0407_LSPV2_555_ACCEPTED_LIVE_DEF_RES_K1.json');
const PIN={checker:'338305c0ce101704205e57543756b8127074a986',seed:'aeeb555c4dcf7f510a9a501c8afc609b629a9298'};
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const blob=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\\0'),b])).digest('hex');
function must(b,m){if(!b)throw Error(m)}
for(const [name,file] of Object.entries({checker,seed}))
  must(blob(fs.readFileSync(file))===PIN[name],'historical blob drift: '+name);
const b=fs.readFileSync(seed,'utf8').trim(),o=JSON.parse(b);
must(Buffer.byteLength(b+'\\n')===3213&&o.summary.paid_total===33&&o.records.length===51,'seed drift');
function once(s,a,r){must(s.includes(a),'missing exact byte anchor '+a);return s.replace(a,r)}
const firstSource=JSON.stringify(o.records.find(r=>r.kind==='SOURCE').c);
const spec=JSON.stringify(o.spec);
const cases=[
 ['baseline',b,true],
 ['root_bad_then_good',once(b,'{"spec":','{"spec":{"h":3},"spec":'),true],
 ['root_good_then_bad',once(b,'{"spec":'+spec,'{"spec":'+spec+',"spec":{"h":3}'),false],
 ['source_bad_then_good',once(b,'{"kind":"SOURCE","c":','{"kind":"SOURCE","c":[12345],"c":'),true],
 ['source_good_then_bad',once(b,'{"kind":"SOURCE","c":'+firstSource,'{"kind":"SOURCE","c":'+firstSource+',"c":[12345]'),false],
 ['facet_bad_then_good',once(b,'{"kind":"DEF","gate":0','{"kind":"DEF","gate":999,"gate":0'),true],
 ['facet_good_then_bad',once(b,'{"kind":"DEF","gate":0','{"kind":"DEF","gate":0,"gate":999'),false],
 ['terminal_pivot_bad_then_good',once(b,'"pivot":7}],"summary"','"pivot":999,"pivot":7}],"summary"'),true],
 ['terminal_pivot_good_then_bad',once(b,'"pivot":7}],"summary"','"pivot":7,"pivot":999}],"summary"'),false],
 ['terminal_kind_bad_then_good',once(b,'{"kind":"RES","c":[]','{"kind":"BAD","kind":"RES","c":[]'),true],
 ['terminal_kind_good_then_bad',once(b,'{"kind":"RES","c":[]','{"kind":"RES","kind":"BAD","c":[]'),false],
 ['source_parent_bad_then_good',once(b,'{"kind":"SOURCE","c":'+firstSource+',"parents":[]','{"kind":"SOURCE","c":'+firstSource+',"parents":[999],"parents":[]'),true],
 ['source_parent_good_then_bad',once(b,'{"kind":"SOURCE","c":'+firstSource+',"parents":[]','{"kind":"SOURCE","c":'+firstSource+',"parents":[],"parents":[999]'),false],
 ['escaped_spec_key',once(b,'{"spec":','{"sp\\u0065c":'),true],
 ['exponent_terminal_pivot',once(b,'"pivot":7}],"summary"','"pivot":7e0}],"summary"'),true]
];
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-557-'));
const dst=process.argv[3]?path.resolve(process.argv[3]):null;if(dst)fs.mkdirSync(dst,{recursive:true});
const rows=[];
try{
 for(const [name,s,expected] of cases){
  const packet=Buffer.from(s+'\\n','utf8'),file=path.join(tmp,name+'.json');
  fs.writeFileSync(file,packet);if(dst)fs.writeFileSync(path.join(dst,name+'.json'),packet);
  const parsed=JSON.parse(packet.toString('utf8'));
  must(parsed.records.length===51&&parsed.summary.paid_total===33,'unexpected last-key parse '+name);
  const p=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:30000,maxBuffer:1048576});
  const accepted=p.status===0&&!p.error;
  must(accepted===expected,'original checker mismatch '+name+': '+String(p.stderr||p.error).slice(0,400));
  const row={case:name,expected,accepted,bytes:packet.length,sha256:sha(packet),paid:parsed.summary.paid_total,
     original_error:accepted?null:String(p.stderr||p.error).split('\\n')[0]};
  if(accepted){
    const native=JSON.parse(p.stdout.trim().split('\\n').at(-1));
    must(native.paid===33&&native.def===3&&native.res===30&&native.records===51&&native.sources===17&&native.negativeTests===11,'native metrics '+name);
    row.original_assertions=native.assertions;
  }
  rows.push(row);
 }
}finally{fs.rmSync(tmp,{recursive:true,force:true})}
must(rows.length===15&&rows.filter(x=>x.accepted).length===9&&rows.filter(x=>!x.accepted).length===6,'matrix counts');
const result={id:'LSPV-2/557',scope:'archived /386 sibling only',status:'COMPUTATIONAL',
checker_git_blob:PIN.checker,seed_git_blob:PIN.seed,node:process.version,platform:process.platform,
test_count:15,accepted:9,rejected:6,
caveat:'This executable does not authenticate original historical full R_mix341 cross-rule transitions.',
cases:rows,proof:{'P2-D1':'OPEN','P2-C3':'OPEN','P2-B1':'OPEN','P2-B2/B3':'OPEN'}};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+'\\n');
process.stdout.write(JSON.stringify(result,null,2)+'\\n');

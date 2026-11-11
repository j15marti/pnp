#!/usr/bin/env node
'use strict';
// LSPV-2/558; exact original /386 CLI, NOT full historical R_mix341.
// node experiments/arc/lspv2_558_native386_os_utf8_shadow.cjs [results.json] [corpus.json]
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seed=path.join(root,'results/raw/arc/2026-11-11_0407_LSPV2_555_ACCEPTED_LIVE_DEF_RES_K1.json');
const pin={checker:'338305c0ce101704205e57543756b8127074a986',seed:'aeeb555c4dcf7f510a9a501c8afc609b629a9298'};
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const blob=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
const must=(v,s)=>{if(!v)throw Error(s)};
for(const [name,p] of [['checker',checker],['seed',seed]])must(blob(fs.readFileSync(p))===pin[name],name+' blob drift');
const base=fs.readFileSync(seed,'utf8').trim();
must(Buffer.byteLength(base+'\n')===3213,'seed bytes');
const obj=JSON.parse(base);
must(obj.records.length===51&&obj.summary.paid_total===33,'seed content');
function replace1(s,old,neu){must(s.includes(old),'missing anchor '+old);return s.replace(old,neu)}
const src='{"kind":"SOURCE","c":',def='{"kind":"DEF","gate":0';
const pivot='"pivot":7}],"summary"';
const cases=[];
function add(name,value,valid,category){const packet=Buffer.isBuffer(value)?value:Buffer.from(value+'\n');cases.push({name,packet,valid,category})}
add('baseline',base,true,'reference');
add('source_bad_first',replace1(base,src,src+'[12345],"c":'),true,'duplicate');
add('source_bad_last',replace1(base,src+'[1,2,3,-7]',src+'[1,2,3,-7],"c":[12345]'),false,'duplicate');
add('def_bad_first',replace1(base,def,'{"kind":"DEF","gate":999,"gate":0'),true,'duplicate');
add('def_bad_last',replace1(base,def,def+',"gate":999'),false,'duplicate');
add('pivot_bad_first',replace1(base,pivot,'"pivot":999,"pivot":7}],"summary"'),true,'duplicate');
add('pivot_bad_last',replace1(base,pivot,'"pivot":7,"pivot":999}],"summary"'),false,'duplicate');
add('source_opcode_unicode',replace1(base,'"kind":"SOURCE"','"kind":"S\\u004fURCE"'),true,'unicode-active');
add('def_opcode_unicode',replace1(base,'"kind":"DEF"','"kind":"D\\u0045F"'),true,'unicode-active');
add('res_opcode_unicode',replace1(base,'"kind":"RES"','"kind":"R\\u0045S"'),true,'unicode-active');
add('source_key_unicode',replace1(base,src,'{"kind":"SOURCE","\\u0063":'),true,'unicode-active');
add('terminal_pivot_key_unicode',replace1(base,pivot,'"\\u0070ivot":7}],"summary"'),true,'unicode-active');
add('source_bad_opcode',replace1(base,'"kind":"SOURCE"','"kind":"SO\\u0055RCX"'),false,'unicode-active');
function bytePacket(mutator){return Buffer.concat([mutator,Buffer.from('\n')])}
function shadowWithByte(octet,reverse){const pre=Buffer.from(reverse?src+'[1,2,3,-7],"c":"':'{"kind":"SOURCE","c":"');
 const post=Buffer.from(reverse?'"':'","c":[1,2,3,-7]');
 const needle=Buffer.from(src+'[1,2,3,-7]');const at=Buffer.from(base).indexOf(needle);
 must(at>=0,'SOURCE location');
 const mutation=Buffer.concat([pre,Buffer.from([octet]),post]);
 return bytePacket(Buffer.concat([Buffer.from(base).subarray(0,at),mutation,Buffer.from(base).subarray(at+needle.length)]));
}
add('source_shadow_invalid80',shadowWithByte(0x80,false),true,'invalid-utf8-shadow');
add('source_shadow_invalid81',shadowWithByte(0x81,false),true,'invalid-utf8-shadow');
add('source_shadow_invalid80_last',shadowWithByte(0x80,true),false,'invalid-utf8-shadow');
add('source_shadow_invalid81_last',shadowWithByte(0x81,true),false,'invalid-utf8-shadow');
function corruptOpcode(octet){const needle=Buffer.from('"kind":"SOURCE"');const at=Buffer.from(base).indexOf(needle);
 must(at>=0,'kind anchor');return bytePacket(Buffer.concat([Buffer.from(base).subarray(0,at),Buffer.from('"kind":"S'),Buffer.from([octet]),Buffer.from('URCE"'),Buffer.from(base).subarray(at+needle.length)]));}
add('source_opcode_invalid80',corruptOpcode(0x80),false,'invalid-utf8-active');
add('source_opcode_invalid81',corruptOpcode(0x81),false,'invalid-utf8-active');
let correct=0,accepted=0,rejected=0,totalAssertions=0;
const corpus=[],results=[];
const {mkdtempSync,rmSync,writeFileSync}=fs;const os=require('node:os');const tmp=mkdtempSync(path.join(os.tmpdir(),'lspv2-558-'));
try {for(const [i,c] of cases.entries()){
 const decoded=c.packet.toString('utf8');let parsed;try{parsed=JSON.parse(c.packet)}catch(e){throw Error('JSON unexpectedly failed '+c.name)};
 let fatalOK=true;try{new TextDecoder('utf-8',{fatal:true}).decode(c.packet)}catch(e){fatalOK=false}
 const file=path.join(tmp,'pkt_'+i+'.json');writeFileSync(file,c.packet);
 const child=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:30000,maxBuffer:1<<20});
 const success=child.status===0&&!child.error;
 must(success===c.valid,'unexpected CLI verdict '+c.name+': '+String(child.stderr||child.error).slice(0,240));
 let evidence=null;if(success){evidence=JSON.parse(child.stdout.trim());must(evidence.paid===33&&evidence.sources===17&&evidence.def===3&&evidence.res===30&&evidence.negativeTests===11,'incorrect native counts');totalAssertions+=evidence.assertions;}
 must(parsed.records.length===51&&parsed.summary.paid_total===33,'invalid reconstructed record length');
 const row={name:c.name,category:c.category,expected:c.valid,accepted:success,bytes:c.packet.length,sha256:hash(c.packet),valid_strict_utf8:fatalOK,
  decoded_sha256:hash(Buffer.from(decoded)),parsed_sha256:hash(Buffer.from(JSON.stringify(parsed))),native_assertions:evidence?.assertions||null,
  error:success?null:String(child.stderr||child.error).trim().split('\n')[0]};
 corpus.push({name:c.name,expected:c.valid,hex:c.packet.toString('hex')});results.push(row);correct++;success?accepted++:rejected++;
 }} finally {rmSync(tmp,{recursive:true,force:true})}
const a=results.find(x=>x.name==='source_shadow_invalid80'),b=results.find(x=>x.name==='source_shadow_invalid81');
must(a.accepted&&b.accepted&&!a.valid_strict_utf8&&!b.valid_strict_utf8&&a.sha256!==b.sha256&&a.decoded_sha256===b.decoded_sha256&&a.parsed_sha256===b.parsed_sha256,'invalid UTF8 native quotient failed');
must(correct===19&&accepted===11&&rejected===8,'unexpected counts '+JSON.stringify({correct,accepted,rejected}));
const report={id:'LSPV-2/558',scope:'original archived /386 complete OS CLI only',status:'COMPUTATIONAL + RESTRICTED PARSER LEMMA',original_checker_blob:pin.checker,seed_blob:pin.seed,node:process.version,platform:process.platform,
 tests:correct,accepted,rejected,total_original_checker_assertions:totalAssertions,
 ill_formed_accepted_pair:{cases:[a.name,b.name],distinct_raw_sha256:[a.sha256,b.sha256],same_parsed_sha256:a.parsed_sha256,strict_utf8_rejects_both:true},
 note:'No authentication of the lost full R_mix341 rules, cross-ports, contexts, or SAT complexity lower bound.',cases:results};
if(process.argv[2])writeFileSync(process.argv[2],JSON.stringify(report,null,2)+'\n');
if(process.argv[3])writeFileSync(process.argv[3],JSON.stringify({id:'LSPV-2/558',encoding:'complete UTF8-agnostic raw bytes as lowercase hex',cases:corpus},null,2)+'\n');
process.stdout.write(JSON.stringify({tests:correct,accepted,rejected,original_assertions:totalAssertions,ill_formed_pair_sha:a.sha256+' '+b.sha256,node:process.version})+'\n');

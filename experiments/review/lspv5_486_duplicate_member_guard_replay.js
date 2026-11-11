'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const cp = require('child_process');

const root = path.resolve(__dirname, '../..');
const checker = path.join(root, 'experiments/arc/lspv2_386_independent_verify.js');
const seed = path.join(root, 'results/raw/arc/2026-11-10_2124_LSPV3_561_ARCHIVED_386_NATIVE_PACKET.json');
const outPath = path.join(root, 'results/raw/arc/2026-11-11_0448_LSPV5_486_DUPLICATE_MEMBER_GUARD_RAW.json');

const sha256 = b => crypto.createHash('sha256').update(b).digest('hex');
const gitBlob = b => crypto.createHash('sha1').update(`blob ${b.length}\0`).update(b).digest('hex');
function replaceOnce(s,a,b){ if(!s.includes(a)) throw new Error(`missing mutation target ${a}`); return s.replace(a,b); }
function makeShadow(b){
  let z=replaceOnce(b,'"charge":[1,0,0,0]','"charge":[0,0,0,0],"charge":[1,0,0,0]');
  z=replaceOnce(z,'"parents":[],"source":0}','"parents":[],"source":98765,"source":0}');
  z=replaceOnce(z,'"parents":[],"gate":0}','"parents":[],"gate":98765,"gate":0}');
  z=replaceOnce(z,'"kind":"RES"','"kind":"LOCAL-CONVERT","kind":"RES","rule":"AND3","weight":0,"exported_wire":8,"context":{"assumption":"fake","discharged":true},"advertised_gf2":{"mask":"0","rhs":1}');
  return z;
}

// Exact recursive-descent JSON lexical pass.  It reports duplicate decoded
// member names before an ordinary object representation can erase them.
function scanUniqueJSON(text){
  let i=0; const duplicates=[];
  const ws=()=>{while(i<text.length && /[\x20\x09\x0a\x0d]/.test(text[i])) i++;};
  function stringToken(){
    ws(); const start=i; if(text[i++]!=='"') throw new SyntaxError(`string at ${start}`);
    let escaped=false;
    while(i<text.length){
      const c=text[i++];
      if(escaped){escaped=false;continue;}
      if(c==='\\'){escaped=true;continue;}
      if(c==='"'){const raw=text.slice(start,i);return {raw,value:JSON.parse(raw),start};}
      if(c<' ') throw new SyntaxError(`control in string at ${i-1}`);
    }
    throw new SyntaxError(`unterminated string at ${start}`);
  }
  function value(p){
    ws(); const c=text[i];
    if(c==='{') return object(p);
    if(c==='[') return array(p);
    if(c==='"'){stringToken();return;}
    const m=/^(?:-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null)/.exec(text.slice(i));
    if(!m) throw new SyntaxError(`value at ${i}`); i+=m[0].length;
  }
  function object(p){
    i++; ws(); const seen=new Map(); if(text[i]==='}'){i++;return;}
    while(true){
      const k=stringToken(); ws(); if(text[i++]!==':') throw new SyntaxError(`colon at ${i-1}`);
      if(seen.has(k.value)) duplicates.push({path:p,key:k.value,first_offset:seen.get(k.value),duplicate_offset:k.start});
      else seen.set(k.value,k.start);
      value(`${p}.${k.value}`); ws();
      if(text[i]==='}'){i++;return;} if(text[i++]!==',') throw new SyntaxError(`comma at ${i-1}`); ws();
    }
  }
  function array(p){
    i++; ws(); let n=0; if(text[i]===']'){i++;return;}
    while(true){value(`${p}[${n++}]`);ws();if(text[i]===']'){i++;return;}if(text[i++]!==',')throw new SyntaxError(`comma at ${i-1}`);ws();}
  }
  value('$'); ws(); if(i!==text.length) throw new SyntaxError(`trailing bytes at ${i}`);
  return duplicates;
}

function runChecker(raw,label){
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-486-'));
  const f=path.join(dir,`${label}.json`); fs.writeFileSync(f,raw);
  const p=cp.spawnSync(process.execPath,[checker,f],{encoding:'utf8'});
  fs.rmSync(dir,{recursive:true,force:true});
  let parsed=null; if(p.status===0){parsed=JSON.parse(p.stdout.trim());delete parsed.file;}
  return {accepted:p.status===0,status:p.status,parsed,error:p.stderr.trim().split('\n').slice(-1)[0]||''};
}

const checkerBytes=fs.readFileSync(checker);
const base=fs.readFileSync(seed,'utf8');
const shadow=makeShadow(base);
const reversed=replaceOnce(shadow,'"kind":"LOCAL-CONVERT","kind":"RES"','"kind":"RES","kind":"LOCAL-CONVERT"');

const baseDup=scanUniqueJSON(base), shadowDup=scanUniqueJSON(shadow), reversedDup=scanUniqueJSON(reversed);
if(baseDup.length!==0) throw new Error('baseline unexpectedly duplicate');
if(shadowDup.length!==4 || reversedDup.length!==4) throw new Error('expected four duplicate decoded names');
const expected=[['$.spec','charge'],['$.records[0]','source'],['$.records[17]','gate'],['$.records[20]','kind']];
for(let n=0;n<expected.length;n++) if(shadowDup[n].path!==expected[n][0]||shadowDup[n].key!==expected[n][1]) throw new Error('wrong duplicate ledger');

const baselineRun=runChecker(base,'baseline');
const shadowRun=runChecker(shadow,'shadow');
const reversedRun=runChecker(reversed,'reversed');
if(!baselineRun.accepted || !shadowRun.accepted || reversedRun.accepted) throw new Error('unexpected checker disposition');
for(const r of [baselineRun,shadowRun]) if(r.parsed.paid!==50||r.parsed.assertions!==4492||r.parsed.negativeTests!==11) throw new Error('changed accepted outcome');

const lexicalControls={
  escaped_equivalent:scanUniqueJSON('{"kind":"RES","ki\\u006ed":"LOCAL-CONVERT"}'),
  nested_duplicate:scanUniqueJSON('{"outer":{"x":1,"x":2}}'),
  sibling_reuse:scanUniqueJSON('{"a":{"x":1},"b":{"x":2}}')
};
if(lexicalControls.escaped_equivalent.length!==1||lexicalControls.nested_duplicate.length!==1||lexicalControls.sibling_reuse.length!==0) throw new Error('lexical control failure');
let malformedRejected=false;try{scanUniqueJSON('{"a":1,}');}catch(e){malformedRejected=true;}if(!malformedRejected)throw new Error('malformed accepted');

const result={
  run:'LSPV-5/486',timestamp_pst:'2026-11-11 04:48 PST',
  status:'COMPUTATIONAL independent OS-Node validation + PROVED/RESTRICTED duplicate-member guard lemma',
  inputs:{checker:path.relative(root,checker),checker_git_blob:gitBlob(checkerBytes),checker_sha256:sha256(checkerBytes),seed:path.relative(root,seed),seed_sha256:sha256(Buffer.from(base))},
  baseline:{bytes:Buffer.byteLength(base),sha256:sha256(Buffer.from(base)),duplicates:baseDup,checker:baselineRun},
  hostile:{bytes:Buffer.byteLength(shadow),sha256:sha256(Buffer.from(shadow)),duplicates:shadowDup,checker:shadowRun},
  reversed_last_localconvert:{bytes:Buffer.byteLength(reversed),sha256:sha256(Buffer.from(reversed)),duplicates:reversedDup,checker:reversedRun},
  lexical_controls:lexicalControls,malformed_rejected:malformedRejected,
  guard_disposition:{baseline:'PASS then checker ACCEPT',hostile:'REJECT before JSON.parse',reversed:'REJECT before JSON.parse'},
  theorem:'For any valid JSON text, the recursive lexical pass rejects iff some object contains two member names equal after JSON string decoding; otherwise JSON.parse preserves one value for every reported member and the pass changes no proof value or logical cost.',
  interpretation:{
    validation:'LSPV-3/567 is independently reproduced with actual OS Node v'+process.versions.node+'; the first displayed LOCAL-CONVERT is shadow metadata, while the final RES is dispatched.',
    abstraction:'A parsed-object abstraction loses duplicate-member provenance. A sound raw-byte front end can refine concrete states by unique decoded keys before parsed-object alpha.',
    cost:'The guard is a streaming lexical validation cost, not historical logical proof work; W remains 50 on accepted baseline and hostile packets.',
    scope:'This repairs duplicate decoded names for JSON inputs only. It neither authenticates missing R_mix341 operations nor proves P2-C3/P2-B1/B2/B3.'
  }
};
fs.mkdirSync(path.dirname(outPath),{recursive:true});fs.writeFileSync(outPath,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));

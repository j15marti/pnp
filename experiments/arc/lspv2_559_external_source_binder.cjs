#!/usr/bin/env node
'use strict';
// LSPV-2/559. Independent source-binding wrapper for the archived /386 verifier.
// NOT an authoritative historical R_mix341 checker.
// Usage: node experiments/arc/lspv2_559_external_source_binder.cjs
// or: node experiments/arc/lspv2_559_external_source_binder.cjs --packet FILE --source FILE [--sha256 HASH]
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const packetDefault=path.join(root,'results/raw/arc/2026-11-11_0407_LSPV2_555_ACCEPTED_LIVE_DEF_RES_K1.json');
const sourceDefault=path.join(root,'results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf');
const sourceMinus=path.join(root,'results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_MINUS_ONE_SAT.cnf');
const PINS={checker:'338305c0ce101704205e57543756b8127074a986',
 packet:'aeeb555c4dcf7f510a9a501c8afc609b629a9298'};
const must=(p,m)=>{if(!p)throw new Error(m)};
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const blob=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
function assertPin(file,want){must(blob(fs.readFileSync(file))===want,'pinned original artifact changed: '+file)}
function parseDIMACS(raw){
  const t=new TextDecoder('utf-8',{fatal:true}).decode(raw);
  let head=null,rows=[],cur=[];
  for(let line of t.split(/\r?\n/)){
    line=line.trim();if(!line||/^c(?:\s|$)/.test(line))continue;
    if(/^p(?:\s|$)/.test(line)){
      must(!head&&!rows.length&&!cur.length,'duplicate/late DIMACS header');
      const m=line.match(/^p\s+cnf\s+([0-9]+)\s+([0-9]+)$/);
      must(m,'bad DIMACS header');
      head={n:Number(m[1]),m:Number(m[2])};
      must(Number.isSafeInteger(head.n)&&head.n>0&&Number.isSafeInteger(head.m),'DIMACS dimensions not safe integers');
      continue;
    }
    must(head,'clauses before header');
    for(const word of line.split(/\s+/)){
      must(/^-?[0-9]+$/.test(word),'bad literal token');
      const x=Number(word);
      must(Number.isSafeInteger(x)&&Math.abs(x)<=head.n,'out of range DIMACS literal');
      if(x===0){rows.push(cur);cur=[]}else cur.push(x);
    }
  }
  must(head&&cur.length===0&&rows.length===head.m,'unterminated DIMACS or bad clause count');
  return {n:head.n,m:head.m,rows};
}
function clauseKey(c){
  must(Array.isArray(c)&&c.every(x=>Number.isSafeInteger(x)&&x!==0),'noninteger clause literal');
  return JSON.stringify(c.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b));
}
function bindOccurrences(packet,source){
  const native=packet.records.map((r,i)=>({r,i})).filter(x=>x.r.kind==='SOURCE');
  const pool=new Map();
  for(const [i,c] of source.rows.entries()){
    const k=clauseKey(c),v=pool.get(k)||[];
    v.push(i);pool.set(k,v);
  }
  const mapping=[];
  for(const {r,i} of native){
    const k=clauseKey(r.c),v=pool.get(k);
    must(v&&v.length>0,'external signed clause occurrence missing for native SOURCE record '+i);
    mapping.push({record:i,original_vertex:r.source,external_occurrence:v.shift()});
  }
  must(native.length===source.m&&[...pool.values()].every(v=>v.length===0),'external signed source multiset differs');
  return mapping;
}
function originalCLI(packetPath){
  assertPin(checker,PINS.checker);
  const p=cp.spawnSync(process.execPath,[checker,packetPath],
    {encoding:'utf8',timeout:30000,maxBuffer:2<<20});
  must(!p.error&&p.status===0,'unchanged original /386 CLI rejection: '+String(p.stderr||p.error).slice(0,240));
  return JSON.parse(p.stdout.trim());
}
function bind(packetPath,sourcePath,sourceSha){
  const pkt=fs.readFileSync(packetPath),src=fs.readFileSync(sourcePath);
  const verdict=originalCLI(packetPath); // actual archived /386 authority only
  if(sourceSha)must(sha(src)===sourceSha,'external raw source SHA-256 mismatch');
  const parsed=JSON.parse(pkt); // native Node Buffer decoder and last decoded key
  const external=parseDIMACS(src);
  const phi=bindOccurrences(parsed,external);
  return {status:'REFERENCE_BOUND_ARCHIVED_386_ONLY',source_sha256:sha(src),
    packet_sha256:sha(pkt),original_paid_work:verdict.paid,original_native_checks:verdict.assertions,
    external_signed_occurrences:phi.length,mapping:phi,
    certificate_bytes:pkt.length,source_bytes:src.length,
    caveat:'External binding is NOT performed by the original /386 CLI; no R_mix341 mixed rules authenticated'};
}
function findModel(rows,n){
  must(n<=15,'model search restricted to deterministic small controls');
  for(let m=0;m<2**n;m++)if(rows.every(c=>c.some(l=>(m>>(Math.abs(l)-1)&1)===(l>0?1:0))))
    return Array.from({length:n},(_,i)=>String(m>>i&1)).join('');
  return null;
}
function selftest(){
  assertPin(packetDefault,PINS.packet);
  const orig=originalCLI(packetDefault),F=parseDIMACS(fs.readFileSync(sourceDefault));
  must(orig.paid===33&&orig.sources===17&&orig.negativeTests===11,'original result differs');
  must(F.m===17&&findModel(F.rows,7)===null,'authentic external signed source is not UNSAT');
  const bound=bind(packetDefault,sourceDefault);
  let rejectNames=[];
  function rejects(label,fn){
    let failure=null;
    try{fn()}catch(e){failure=e}
    must(failure!==null,'false acceptance: '+label);
    rejectNames.push(label);
  }
  rejects('SAT external F minus clause zero',()=>bind(packetDefault,sourceMinus));
  const wrong=parseDIMACS(Buffer.from(fs.readFileSync(sourceDefault,'utf8').replace('1 2 3 -7 0','-1 2 3 -7 0')));
  rejects('signed clause mutation',()=>bindOccurrences(JSON.parse(fs.readFileSync(packetDefault)),wrong));
  rejects('source byte-digest mutation',()=>bind(packetDefault,sourceDefault,'0'.repeat(64)));
  rejects('invalid external UTF8',()=>parseDIMACS(Buffer.from([0x80])));
  rejects('invalid DIMACS clause token',()=>parseDIMACS(Buffer.from('p cnf 7 1\n1 x 0\n')));
  rejects('duplicate signed source',()=>bindOccurrences(JSON.parse(fs.readFileSync(packetDefault)),
    {n:7,m:17,rows:[...F.rows.slice(1),F.rows[1]]}));
  let witnesses=[];
  for(let i=0;i<F.rows.length;i++){
    const assignment=findModel(F.rows.filter((_,j)=>i!==j),7);
    must(assignment!==null,'source not deletion-minimal at occurrence '+i);
    witnesses.push({removed:i,witness:assignment});
  }
  const p=JSON.parse(fs.readFileSync(packetDefault));
  p.records[4].c=[12345];
  const tmp=path.join(require('node:os').tmpdir(),'lspv2_559_bad_'+process.pid+'.json');
  try{
    fs.writeFileSync(tmp,JSON.stringify(p)+'\n');
    rejects('original native invalid signed SOURCE',()=>originalCLI(tmp));
  }finally{try{fs.unlinkSync(tmp)}catch(e){}}
  return {status:'PASS',native_verdict:orig,source_sha256:bound.source_sha256,
    external_occurrences:bound.external_signed_occurrences,
    deletion_witnesses:witnesses,rejection_controls:rejectNames,
    caveat:'This checks the original /386 CLI plus a separately labeled external source binder, not complete R_mix341'};
}
const argv=process.argv.slice(2);
if(argv.length===0)console.log(JSON.stringify(selftest(),null,2));
else {
  let pkt=null,src=null,expected=null;
  for(let i=0;i<argv.length;i++){
    if(argv[i]==='--packet')pkt=argv[++i];
    else if(argv[i]==='--source')src=argv[++i];
    else if(argv[i]==='--sha256')expected=argv[++i];
    else throw Error('unsupported argument '+argv[i]);
  }
  must(pkt&&src,'require --packet and --source');
  console.log(JSON.stringify(bind(pkt,src,expected),null,2));
}

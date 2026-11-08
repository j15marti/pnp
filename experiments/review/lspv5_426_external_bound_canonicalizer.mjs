// LSPV-5/426: compose exact external-source binding with the recovered
// SOURCE/AND3/XOR canonicalizer.  This is a distinct two-input adapter around
// the preserved checker, not the historical full R_mix341 byte grammar.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../..');
const PACKET = path.join(ROOT, 'replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
const CHECKER = path.join(ROOT, 'replay/413/lspv2_341_independent_verify.js');
const raw = fs.readFileSync(PACKET, 'utf8');
const packet = JSON.parse(raw);
let checks = 0, rejections = 0;
function need(x, msg) { checks++; if (!x) throw new Error(msg); }
function reject(fn, msg) { let yes=false; try { fn(); } catch { yes=true; } need(yes,msg); rejections++; }
function sha(x) { return crypto.createHash('sha256').update(x).digest('hex'); }

function runChecker(text) {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-426-'));
  const file=path.join(dir,'packet.json'); fs.writeFileSync(file,text);
  const cp=spawnSync(process.execPath,[CHECKER,file],{encoding:'utf8'});
  fs.rmSync(dir,{recursive:true,force:true});
  return cp.status===0;
}

function canonicalize(parsed) {
  if (!parsed || !Array.isArray(parsed.fixtures)) throw Error('fixtures missing');
  return {fixtures:parsed.fixtures.map(f=>{
    const E=f.graph.edges.length, keep=(1n<<BigInt(E))-1n, ids=new Map();
    const put=(old,fresh)=>{if(ids.has(old))throw Error('duplicate parsed identity');ids.set(old,fresh);return fresh;};
    const get=old=>{if(!ids.has(old))throw Error('missing parsed identity');return ids.get(old);};
    const clauses=f.clauses.map((c,i)=>({id:put(c.id,`s${i}`),vertex:c.vertex,literals:[...c.literals]}));
    const row=r=>({mask:'0x'+(BigInt(r.mask)&keep).toString(16),rhs:r.rhs});
    const proof=f.proof.map((p,i)=>{
      const q={id:`d${i}`,kind:p.kind,rule:p.rule,parents:p.parents.map(get)}; put(p.id,q.id);
      if(p.rule==='AND3'){q.support=[...p.support];q.table=p.table;if(p.row)q.row=row(p.row);}
      else if(p.rule==='XOR')q.row=row(p.row); else throw Error('unknown rule');
      return q;
    });
    return {graph:{name:f.graph.name==='BRIDGE_K4x2'?'BRIDGE_K4x2':'G',n:f.graph.n,edges:f.graph.edges.map(e=>[...e])},charges:[...f.charges],clauses,proof,deleted:f.deleted.map(d=>({sourceId:get(d.sourceId),assignment:d.assignment})),evenWitness:f.evenWitness,properties:{essential:f.properties.essential}};
  }),summary:parsed.fixtures.map(()=>null)};
}
function canonicalRaw(text){return JSON.stringify(canonicalize(JSON.parse(text)))+'\n';}

function parseDIMACS(src){
  if(typeof src!=='string')throw Error('source not text');
  const a=src.trim().split(/\s+/); if(a.length<4||a[0]!=='p'||a[1]!=='cnf')throw Error('bad header');
  if(!/^(0|[1-9]\d*)$/.test(a[2])||!/^(0|[1-9]\d*)$/.test(a[3]))throw Error('bad counts');
  const nv=Number(a[2]),m=Number(a[3]); if(!Number.isSafeInteger(nv)||!Number.isSafeInteger(m))throw Error('unsafe counts');
  const clauses=[]; let now=[];
  for(let i=4;i<a.length;i++){
    if(!/^-?(0|[1-9]\d*)$/.test(a[i]))throw Error('bad token');
    const x=Number(a[i]); if(!Number.isSafeInteger(x))throw Error('unsafe literal');
    if(x===0){clauses.push(now);now=[];} else {if(Math.abs(x)>nv)throw Error('literal outside header');now.push(x);}
  }
  if(now.length||clauses.length!==m)throw Error('wrong termination/count');
  return {nv,clauses};
}
function clauseKey(c){return c.slice().sort((a,b)=>a-b).join(',');}
function multiset(cs){const m=new Map();for(const c of cs){const k=clauseKey(c);m.set(k,(m.get(k)||0)+1);}return JSON.stringify([...m].sort((a,b)=>a[0].localeCompare(b[0])));}
function bind(f,src){
  const ext=parseDIMACS(src), inside=f.clauses.map(c=>c.literals);
  if(ext.nv!==f.graph.edges.length)throw Error('variable bound differs');
  if(ext.clauses.length!==inside.length||multiset(ext.clauses)!==multiset(inside))throw Error('clause multiset differs');
  return true;
}
function serialize(f,at=-1,repl=null){
  const rows=[`p cnf ${f.graph.edges.length} ${f.clauses.length}`];
  f.clauses.forEach((c,i)=>{const xs=i===at?repl:c.literals;rows.push(xs.map(x=>String(x).padStart(10,' ')).join('')+' 0');});
  return rows.join('\n')+'\n';
}
function sat(cs,bits){return cs.every(c=>c.some(l=>l>0?bits[Math.abs(l)-1]==='1':bits[Math.abs(l)-1]==='0'));}

need(runChecker(raw),'published packet rejected');
const canonRaw=canonicalRaw(raw), canon=JSON.parse(canonRaw);
need(runChecker(canonRaw),'canonical packet rejected');
need(sha(canonRaw)==='1637821fc706fd80abcaf70cbd458d1ad648bcf1576e1eed564b519bb62aba25','run425 canonical SHA drift');

let acceptedBindings=0, essentialMutants=0, equalLengthMutants=0;
for(let i=0;i<packet.fixtures.length;i++){
  const orig=packet.fixtures[i], cf=canon.fixtures[i], src=serialize(orig);
  need(bind(orig,src),'original packet/source bind failed'); acceptedBindings++;
  need(bind(cf,src),'canonical packet/source bind failed'); acceptedBindings++;
  const perm=orig.clauses.slice().reverse().map(c=>[...c.literals].reverse());
  const permSrc=`p cnf ${orig.graph.edges.length} ${perm.length}\n`+perm.map(c=>c.join(' ')+' 0').join('\n')+'\n';
  need(bind(cf,permSrc),'semantic multiset permutation rejected'); acceptedBindings++;
  if(orig.clauses.length>1){
    const dup=orig.clauses.map(c=>[...c.literals]);dup[1]=[...dup[0]];
    const dupSrc=`p cnf ${orig.graph.edges.length} ${dup.length}\n`+dup.map(c=>c.join(' ')+' 0').join('\n')+'\n';
    reject(()=>bind(cf,dupSrc),'duplicate multiplicity substitution accepted');
  }
  for(let j=0;j<orig.clauses.length;j++){
    const d=orig.deleted[j]; if(d.assignment===null)continue;
    const lits=orig.clauses[j].literals, taut=[Math.abs(lits[0]),-Math.abs(lits[0]),Math.abs(lits[1])];
    const mutant=serialize(orig,j,taut);
    need(mutant.length===src.length,'mutation length changed'); equalLengthMutants++;
    need(sat(orig.clauses.filter((_,k)=>k!==j).map(c=>c.literals),d.assignment),'deletion witness invalid');
    need(sat([taut],d.assignment),'replacement clause not satisfied');
    reject(()=>bind(cf,mutant),'same-length SAT source mutant accepted'); essentialMutants++;
  }
  reject(()=>bind(cf,src.replace(/^p cnf \d+/,'p cnf 999')),'wrong variable bound accepted');
  reject(()=>bind(cf,src.replace(/ 0\n/,' \n')),'unterminated source accepted');
  reject(()=>bind(cf,src.replace(/^p cnf/,'x cnf')),'bad header accepted');
}

// Parser-semantic packet aliases from runs 414--419 still normalize to the
// same externally bound representative.
const aliases=[];
aliases.push(['baseline',raw]);
const meta=structuredClone(packet);meta.version='X'.repeat(1<<20);meta.unknown='Y'.repeat(1<<20);aliases.push(['ignored_metadata',JSON.stringify(meta)]);
const ghost=structuredClone(packet);const gr=ghost.fixtures[0].proof.filter(p=>p.rule==='AND3'&&p.row);for(const p of gr.slice(0,2))p.row.mask='0x'+(BigInt(p.row.mask)^(1n<<8192n)).toString(16);aliases.push(['paired_ghost',JSON.stringify(ghost)]);
const compact=JSON.stringify(packet);
aliases.push(['numeric_id',compact.replace('"id":"s0"','"id":9007199254740992').replace('"parents":["s0","s1"]','"parents":[9007199254740993,"s1"]').replace('"sourceId":"s0"','"sourceId":9007199254740993')]);
aliases.push(['lexical_id',compact.replace('"id":"s0"','"id":1').replace('"parents":["s0","s1"]','"parents":[1e0,"s1"]').replace('"sourceId":"s0"','"sourceId":1.0')]);
aliases.push(['duplicate_member',compact.replace('"id":"s0"','"id":"ignored","id":"s0"')]);
const aliasRows=[];
for(const [name,text] of aliases){
  need(runChecker(text),`${name} rejected before canonicalization`);
  const cr=canonicalRaw(text);need(cr===canonRaw,`${name} canonical bytes differ`);need(runChecker(cr),`${name} canonical rejected`);
  for(let i=0;i<packet.fixtures.length;i++){need(bind(JSON.parse(cr).fixtures[i],serialize(packet.fixtures[i])),`${name} source bind failed`);acceptedBindings++;}
  aliasRows.push({name,input_bytes:Buffer.byteLength(text),canonical_bytes:Buffer.byteLength(cr),canonical_sha256:sha(cr)});
}

const totalExternalBytes=packet.fixtures.reduce((n,f)=>n+Buffer.byteLength(serialize(f)),0);
console.log(JSON.stringify({
  run:'LSPV-5/426',
  status:'PROVED-RESTRICTED composition theorem; COMPUTATIONAL exact-checker and source-binding replay',
  published_packet_sha256:sha(raw),checker_sha256:sha(fs.readFileSync(CHECKER)),
  canonical_bytes:Buffer.byteLength(canonRaw),canonical_sha256:sha(canonRaw),
  checks,rejections,fixtures:packet.fixtures.length,accepted_bindings:acceptedBindings,
  essential_sat_mutants:essentialMutants,equal_length_mutants:equalLengthMutants,
  external_source_bytes_total:totalExternalBytes,aliases:aliasRows,
  theorem:'If the recovered checker accepts P and an exact external binder accepts (F,P), then canonicalization C preserves acceptance and the external clause multiset/variable-bound binding; pair length is |F|+O(sum V(E+W+1)).',
  scope:['distinct two-input adapter, not historical full parser','post-JSON-parse packet canonicalization','no RES/LOCAL-CONVERT/DEF/branch-discharge','no proof construction, B3, or all-algorithm lower bound']
},null,2));

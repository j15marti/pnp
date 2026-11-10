#!/usr/bin/env node
'use strict';
/* LSPV-2/539: SEPARATE STRICT REFERENCE AUDITOR, NOT HISTORICAL R_mix341 CHECKER.
 * Inputs: separately authenticated canonical signed 3-CNF DIMACS bytes and
 * legacy /341 fixture packet bytes. Only SOURCE + AND3 + XOR admitted.
 * Unknown native opcodes are NOT declared illegal; their semantics remain OPEN.
 * node lspv2_539_strict_fragment_reference.cjs INPUT.cnf PACKET.json
 */
const fs=require('fs'), crypto=require('crypto');
const fail=(why)=>{throw Error('REFERENCE-539: '+why)};
function chk(b,why){if(!b)fail(why)}
function plain(x){return x!==null&&typeof x==='object'&&!Array.isArray(x)}
function isInt(x){return typeof x==='number'&&Number.isSafeInteger(x)}
function parseDimacs(s){
  chk(typeof s==='string'&& /^[\x09\x0a\x0d\x20-\x7e]*$/.test(s),'non-ASCII or nontext DIMACS');
  const lines=s.replace(/\r\n/g,'\n').split('\n');
  let toks=[],hasP=false;
  for(const l of lines){const x=l.trim();if(!x)continue;
    if(/^c(?:\s|$)/.test(x))continue;
    const t=x.split(/\s+/);if(!hasP){chk(t.length===4&&t[0]==='p'&&t[1]==='cnf','bad header');
      chk(/^\d+$/.test(t[2])&&/^\d+$/.test(t[3]),'header integer');
      const nv=Number(t[2]), nc=Number(t[3]);chk(isInt(nv)&&nv>=1&&isInt(nc)&&nc>=1,'dimensions');
      hasP={nv,nc};continue;
    }
    chk(t[0]!=='p','duplicate header');toks.push(...t);
  }
  chk(hasP,'missing header');let clauses=[],row=[];
  for(const t of toks){chk(/^(?:0|-?[1-9]\d*)$/.test(t),'noncanonical signed literal');
    let v=Number(t);chk(isInt(v),'unsafe literal');
    if(v===0){chk(row.length===3,'source requires strict width three');
      chk(new Set(row.map(Math.abs)).size===3,'source repeated/complementary var');
      clauses.push(row);row=[];
    } else {chk(Math.abs(v)<=hasP.nv,'out-of-range literal');row.push(v);chk(row.length<=3,'source width');}
  }
  chk(row.length===0&&clauses.length===hasP.nc,'terminators/count');
  return {nv:hasP.nv,nc:hasP.nc,clauses};
}
function strictIntList(v,n,why){
  chk(Array.isArray(v)&&v.length<=n,why+' array');
  const seen=new Set();for(const x of v){chk(isInt(x)&&x>=0&&x<n&&!seen.has(x),why+' items');seen.add(x);}
  return v;
}
function normalizedMask(mask,nv){
  chk(typeof mask==='string'&&/^0x(?:0|[1-9a-f][0-9a-f]*)$/.test(mask),'canonical nonnegative hex mask');
  const x=BigInt(mask);chk(x<(1n<<BigInt(nv)),'mask references outside source');return x;
}
function factorEval(f,bits){
  let idx=0;f.support.forEach((e,j)=>{idx|=(bits[e]<<j)});
  return (f.table>>idx)&1;
}
function affineEval(row,bits){
  let k=row.mask,out=row.rhs,i=0;while(k){if(k&1n)out^=bits[i]||0;k>>=1n;i++;}return out===0?1:0;
}
function auditCertificate(sourceText,packetText){
  const F=parseDimacs(sourceText), pkt=JSON.parse(packetText);
  chk(plain(pkt)&&Array.isArray(pkt.fixtures)&&pkt.fixtures.length===1,'single legacy fixture');
  const f=pkt.fixtures[0];chk(plain(f)&&Array.isArray(f.clauses)&&Array.isArray(f.proof),'fixture shape');
  chk(f.clauses.length===F.nc,'source clause total');
  const nodes=new Map(),paid=new Set(),original=new Set();
  for(let i=0;i<F.nc;i++){
    const c=f.clauses[i],src=F.clauses[i];
    chk(plain(c)&&typeof c.id==='string'&&c.id.length>0,'source ID');
    chk(Array.isArray(c.literals)&&c.literals.length===3,'source field array');
    chk(c.literals.every((v,j)=>isInt(v)&&v===src[j]),'SOURCE != external signed DIMACS');
    chk(!nodes.has(c.id),'duplicate SOURCE ID');
    const support=[...new Set(src.map(l=>Math.abs(l)-1))];
    let table=0;
    for(let bits=0;bits<(1<<support.length);bits++){
      const sat=src.some(l=>{const j=support.indexOf(Math.abs(l)-1);const val=(bits>>j)&1;return val===(l>0?1:0)});
      if(sat)table|=(1<<bits);
    }
    nodes.set(c.id,{kind:'factor',support,table,parents:[],span:0,depth:0});original.add(c.id);
  }
  let references=0, maxSpan=0;
  for(const p of f.proof){
    chk(plain(p)&&typeof p.id==='string'&&p.id.length>0&&!nodes.has(p.id),'fresh paid ID');
    chk(Array.isArray(p.parents)&&p.parents.length===2&&p.parents[0]!==p.parents[1],'two distinct parents');
    chk(p.parents.every(x=>typeof x==='string'&&nodes.has(x)),'prior parents');
    const a=nodes.get(p.parents[0]),b=nodes.get(p.parents[1]);references+=2;
    let v=null;
    if(p.rule==='AND3'){
      chk(p.kind==='factor'&&a.kind==='factor'&&b.kind==='factor','factor types');
      const u=[...new Set([...a.support,...b.support])];
      chk(u.length<=3,'AND3 local support');
      const sup=strictIntList(p.support,F.nv,'AND3 support');
      chk(sup.length===u.length&&u.every(k=>sup.includes(k)),'AND3 exact support');
      chk(isInt(p.table)&&p.table>=0&&p.table<(1<<(1<<sup.length)),'AND3 table width');
      for(let i=0;i<(1<<sup.length);i++){
        const bits=Array(F.nv).fill(0);sup.forEach((e,j)=>bits[e]=(i>>j)&1);
        chk(((p.table>>i)&1)===(factorEval(a,bits)&factorEval(b,bits)),'AND3 semantic mismatch');
      }
      v={kind:'factor',support:sup,table:p.table};
      if(Object.prototype.hasOwnProperty.call(p,'row')){
        chk(plain(p.row),'affine alias shape');
        const mask=normalizedMask(p.row.mask,F.nv),rhs=p.row.rhs;
        chk(isInt(rhs)&&(rhs===0||rhs===1),'affine alias RHS');
        for(let e=0;e<F.nv;e++)if((mask>>BigInt(e))&1n)chk(sup.includes(e),'affine alias external variable');
        for(let i=0;i<(1<<sup.length);i++){
          const bits=Array(F.nv).fill(0);sup.forEach((e,j)=>bits[e]=(i>>j)&1);
          chk(((p.table>>i)&1)===affineEval({mask,rhs},bits),'affine alias not equivalent');
        }
        v.row={mask,rhs};
      }
    }else if(p.rule==='XOR'){
      chk(p.kind==='affine'&&a.row&&b.row&&plain(p.row),'XOR operands');
      const mask=normalizedMask(p.row.mask,F.nv),rhs=p.row.rhs;
      chk(isInt(rhs)&&(rhs===0||rhs===1),'XOR rhs');
      chk(mask===(a.row.mask^b.row.mask)&&rhs===(a.row.rhs^b.row.rhs),'XOR incorrect algebra');
      v={kind:'affine',row:{mask,rhs}};
    }else{
      fail('UNAUTHENTICATED NATIVE OPCODE '+String(p.rule)+'; neither accepted nor excluded');
    }
    const span=Math.max(a.span,b.span)+1;v.span=span;v.parents=p.parents.slice();
    nodes.set(p.id,v);paid.add(p.id);maxSpan=Math.max(maxSpan,span);
  }
  chk(f.proof.length>0,'no sink');let sink=f.proof[f.proof.length-1],last=nodes.get(sink.id);
  chk(last.row&&last.row.mask===0n&&last.row.rhs===1,'missing 0=1');
  const ancestry=new Set();function anc(id){if(ancestry.has(id))return;ancestry.add(id);for(const q of nodes.get(id).parents)anc(q)}anc(sink.id);
  const hash=crypto.createHash('sha256').update(sourceText,'utf8').digest('hex');
  return {status:'STRICT_REFERENCE_FRAGMENT_VALID',sourceSHA256:hash,sourceBytes:Buffer.byteLength(sourceText),packetBytes:Buffer.byteLength(packetText),variables:F.nv,clauses:F.nc,paidDistinct:paid.size,paidAncestorCount:[...paid].filter(x=>ancestry.has(x)).length,sourceAncestorCount:[...original].filter(x=>ancestry.has(x)).length,referenceCount:references,logicalWeight:paid.size,maxDependencySpan:maxSpan,goal:sink.id,scope:'SOURCE+AND3+XOR ONLY; separate reference semantics, NOT authentic historical rule dispatcher; no physical RAM/time inference'};
}
function tryAudit(s,p){try{return {accepted:true,result:auditCertificate(s,p)}}catch(e){return {accepted:false,diagnostic:String(e.message)}}}
module.exports={parseDimacs,auditCertificate,tryAudit};
if(require.main===module){
  if(process.argv.length!==4){console.error('usage: node '+process.argv[1]+' source.cnf certificate.json');process.exit(2)}
  const s=fs.readFileSync(process.argv[2],'utf8'),p=fs.readFileSync(process.argv[3],'utf8'),r=tryAudit(s,p);
  console.log(JSON.stringify(r,null,2));if(!r.accepted)process.exitCode=1;
}

'use strict';
// LSPV-2/544: independent, NON-AUTHORITATIVE lossless UTF-8 JSON scanner/replayer.
// It authenticates no missing historical R_mix341 operation.
// Run: node experiments/arc/lspv2_544_utf8_lossless_replayer.cjs
function enc(s){
  const q=encodeURIComponent(s),out=[];
  for(let i=0;i<q.length;i++)if(q[i]==='%'){out.push(parseInt(q.slice(i+1,i+3),16));i+=2;}
  else out.push(q.charCodeAt(i));
  return Uint8Array.from(out);
}
function dec(b){return decodeURIComponent(Array.from(b,x=>'%'+x.toString(16).padStart(2,'0')).join(''));}
function sameBytes(a,b){return a.length===b.length&&a.every((x,i)=>x===b[i]);}
function scan(bytes){
  if(!(bytes instanceof Uint8Array))throw Error('Uint8Array required');
  JSON.parse(dec(bytes)); // JS parser validates syntax, not historical R_mix341 proof validity
  let i=0,count=0,maxDepth=0;
  function ws(){while([32,10,13,9].includes(bytes[i]))i++;}
  function string(){
    let start=i++;
    while(i<bytes.length){
      const c=bytes[i++];
      if(c===34)return {kind:'string',start,end:i,value:JSON.parse(dec(bytes.subarray(start,i)))};
      if(c===92){if(i===bytes.length)throw Error('unterminated escape');i++;}
    }
    throw Error('unterminated string');
  }
  function value(depth){
    if(depth>512)throw Error('scanner depth cap');maxDepth=Math.max(maxDepth,depth);
    ws();const start=i;count++;let node;
    if(bytes[i]===123){
      i++;ws();const props=new Map(),children=[];
      if(bytes[i]!==125)while(true){
        ws();const key=string();ws();if(bytes[i++]!==58)throw Error('colon');
        const val=value(depth+1);props.set(key.value,val);children.push(val);
        ws();if(bytes[i]===44){i++;continue;}break;
      }
      if(bytes[i++]!==125)throw Error('object');
      node={kind:'object',props,children};
    }else if(bytes[i]===91){
      i++;ws();const children=[];
      if(bytes[i]!==93)while(true){
        children.push(value(depth+1));ws();if(bytes[i]===44){i++;continue;}break;
      }
      if(bytes[i++]!==93)throw Error('array');
      node={kind:'array',children};
    }else if(bytes[i]===34)node=string();
    else {
      const c=bytes[i];
      if(c===116)i+=4;
      else if(c===102)i+=5;
      else if(c===110)i+=4;
      else while(i<bytes.length&&[45,43,46,101,69,48,49,50,51,52,53,54,55,56,57].includes(bytes[i]))i++;
      if(i===start)throw Error('unrecognized scalar');
      node={kind:'scalar'};
    }
    node.start=start;node.end=i;return node;
  }
  const root=value(0);ws();if(i!==bytes.length)throw Error('trailing bytes');
  function at(path){
    let n=root;
    for(const key of path){
      n=typeof key==='number'&&n.kind==='array'?n.children[key]:
        typeof key==='string'&&n.kind==='object'?n.props.get(key):undefined;
      if(!n)throw Error('missing active path');
    }
    return n;
  }
  function strings(){
    const out=[];function visit(n){
      if(n.kind==='string')out.push(n);
      else if(n.kind==='array'||n.kind==='object')for(const child of n.children)visit(child);
    }
    visit(root);return out;
  }
  return {root,at,strings,nodes:count,maxDepth,bytes:bytes.length};
}
function splice(bytes,edits){
  let end=0,len=0;
  for(const x of edits){
    if(x.start<end||x.end<x.start||x.end>bytes.length)throw Error('overlap');
    len+=x.start-end+x.token.length;end=x.end;
  }
  len+=bytes.length-end;
  const out=new Uint8Array(len);let p=0;end=0;
  for(const x of edits){
    out.set(bytes.subarray(end,x.start),p);p+=x.start-end;
    out.set(x.token,p);p+=x.token.length;end=x.end;
  }
  out.set(bytes.subarray(end),p);return out;
}
function reencodeSameString(bytes,s,tokenText){
  const token=enc(tokenText);
  if(typeof JSON.parse(tokenText)!=='string'||JSON.parse(tokenText)!==s)
    throw Error('new token has different decoded value');
  const edits=scan(bytes).strings().filter(x=>x.value===s)
    .map(x=>({start:x.start,end:x.end,token})).sort((a,b)=>a.start-b.start);
  if(!edits.length)throw Error('no matching values');
  const output=splice(bytes,edits);
  if(JSON.stringify(JSON.parse(dec(bytes)))!==JSON.stringify(JSON.parse(dec(output))))
    throw Error('not JSON.parse invariant');
  return {bytes:output,edits:edits.length,oldBytes:bytes.length,newBytes:output.length};
}
function repairSignedLiteral(bytes,path,tokenText){
  const old=scan(bytes).at(path),before=JSON.parse(dec(bytes.subarray(old.start,old.end)));
  const after=JSON.parse(tokenText),v=Number(before);
  if(!Number.isSafeInteger(v)||v===0||Number(after)!==v||!Number.isSafeInteger(Number(after)))
    throw Error('invalid signed-literal replacement');
  const output=splice(bytes,[{start:old.start,end:old.end,token:enc(tokenText)}]);
  scan(output).at(path);
  return {bytes:output,span:[old.start,old.end],oldBytes:bytes.length,newBytes:output.length};
}
function baseline(d){return {version:d.version,fixtures:[d.fixtures[0]],summary:[d.summary[0]]};}
function unicodePacket(d){
  const clone=JSON.parse(JSON.stringify(baseline(d))),f=clone.fixtures[0];
  const old=f.clauses[0].id,newId='源🤖';
  f.clauses[0].id=newId;
  for(const p of f.proof)p.parents=p.parents.map(x=>x===old?newId:x);
  for(const del of f.deleted)if(del.sourceId===old)del.sourceId=newId;
  f.graph.name='K4-éÅ😀';clone['😀']='v';clone['α']='β';
  return JSON.stringify(clone);
}
function countModels(f){
  const E=f.graph.edges.length;let sat=0;
  for(let m=0;m<2**E;m++)
    if(f.clauses.every(c=>c.literals.some(l=>Boolean(m&(1<<(Math.abs(l)-1)))===(l>0))))sat++;
  return sat;
}
function packets(data){
  const base=enc(JSON.stringify(baseline(data)));
  const unicode=enc(unicodePacket(data));
  const esc=reencodeSameString(unicode,'源🤖','"\\u6e90\\ud83e\\udd16"');
  const path=['fixtures',0,'clauses',0,'literals',0];
  const padded=repairSignedLiteral(unicode,path,'" 0001 "');
  const repaired=repairSignedLiteral(padded.bytes,path,'1');
  const shadow=enc('{"\\ud83d\\ude00":"old","😀":"new","\\u0066ixtures":[],'+unicodePacket(data).slice(1));
  const a=scan(shadow);
  if(a.at(['😀']).value!=='v'||a.at(['fixtures']).kind!=='array')
    throw Error('unicode duplicate-key last-wins regression');
  if(!sameBytes(unicode,repaired.bytes))throw Error('byte identity repair failed');
  const wrong=enc(dec(unicode).replace('"literals":[1,','"literals":["2",'));
  const missing=enc(dec(unicode).replace('"parents":["d0",','"parents":["missing",'));
  const cases=[
    {name:'baseline',bytes:base,accept:true},
    {name:'live_utf8_source_id',bytes:unicode,accept:true},
    {name:'equivalent_escaped_utf8_id',bytes:esc.bytes,accept:true},
    {name:'utf8_shadowed_decoded_keys',bytes:shadow,accept:true},
    {name:'untyped_numeric_literal',bytes:padded.bytes,accept:true},
    {name:'surgical_typed_repair',bytes:repaired.bytes,accept:true},
    {name:'wrong_signed_source',bytes:wrong,accept:false},
    {name:'broken_parent',bytes:missing,accept:false}
  ];
  return {cases,escapedReplacements:esc.edits,tokenRepairSpan:padded.span,
    sourcePath:path,unicodeBytes:unicode.length,escapedBytes:esc.bytes.length};
}
function audit(data,native){
  if(countModels(data.fixtures[0])!==0||data.fixtures[0].clauses.length!==16||
      data.fixtures[0].proof.length!==15)throw Error('K4 original control');
  const {cases,escapedReplacements,tokenRepairSpan,sourcePath,unicodeBytes,escapedBytes}=packets(data);
  const obs=cases.map(c=>{
    const res=native(dec(c.bytes));
    if(res.accepted!==c.accept)throw Error(c.name+': '+JSON.stringify(res));
    return {name:c.name,accepted:res.accepted,bytes:c.bytes.length,
      nativeChecks:res.checks??null,error:res.error??null};
  });
  if(escapedReplacements<2)throw Error('shared references not exercised');
  for(const invalid of [[34,192,175,34],[34,237,160,128,34]]){
    let rejected=false;try{scan(Uint8Array.from(invalid));}catch(e){rejected=true;}
    if(!rejected)throw Error('invalid UTF-8 admitted');
  }
  return {run:'LSPV2-544',scope:'valid UTF-8 JSON, recovered restricted /341 fixture checker only',
    producerGitBlob:'4081022e8a3841d79f751a3d3a7a10decbb026da',
    verifierGitBlob:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
    K4:{variables:6,sourceClauses:16,paidNodes:15,models:0},
    referenceLexer:{unicodeBytes,escapedBytes,escapedReplacements,tokenRepairSpan,
      nodes:scan(cases[1].bytes).nodes,maxDepth:scan(cases[1].bytes).maxDepth},
    cases:obs,invalidUtf8Controls:2,
    conclusion:'lossless UTF-8 token spans and equivalent multi-occurrence ID lexemes; no full historical parser'};
}
module.exports={enc,dec,scan,splice,reencodeSameString,repairSignedLiteral,baseline,unicodePacket,packets,audit};
if(typeof require!=='undefined'&&require.main===module){
  const fs=require('fs'),cp=require('child_process'),os=require('os'),path=require('path');
  const root=path.resolve(__dirname,'../..');
  const prod=path.join(root,'experiments/arc/lspv2_341_mixed_tseitin_min_dag.js');
  const check=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
  const data=JSON.parse(cp.execFileSync(process.execPath,[prod],{encoding:'utf8',maxBuffer:12e6}));
  const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp544-'));
  try{
    const native=raw=>{
      const file=path.join(tmp,'fixture.json');fs.writeFileSync(file,raw,'utf8');
      try{return {accepted:true,checks:JSON.parse(cp.execFileSync(process.execPath,
        [check,file],{encoding:'utf8',maxBuffer:2e6})).checks};}
      catch(e){return {accepted:false,error:(e.stderr?.toString()||e.message).slice(0,160)};}
    };
    console.log(JSON.stringify(audit(data,native),null,2));
  }finally{fs.rmSync(tmp,{recursive:true,force:true});}
}
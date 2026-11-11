'use strict';
// LSPV-2/543: independent, non-authoritative ASCII JSON span parser and source-token editor.
// Run: node experiments/arc/lspv2_543_lossless_json_span_replayer.cjs
function scan(raw) {
  if(typeof raw!=='string'||/[^\x00-\x7f]/.test(raw))throw Error('ASCII JSON only');
  let i=0,nodes=0,depth=0,maxDepth=0;
  function ws(){while(i<raw.length&&/[ \t\r\n]/.test(raw[i]))i++;}
  function string(){
    const start=i++;
    while(i<raw.length){
      const c=raw[i++];
      if(c==='"')return {kind:'string',start,end:i,key:JSON.parse(raw.slice(start,i))};
      if(c==='\\')i++;
    }
    throw Error('unterminated string');
  }
  function val(){
    ws();const start=i;nodes++;depth++;maxDepth=Math.max(maxDepth,depth);
    if(depth>512)throw Error('scanner depth cap');
    let n;
    if(raw[i]==='{'){
      i++;ws();const props=new Map();
      if(raw[i]!=='}')while(true){
        ws();if(raw[i]!=='"')throw Error('expected object key');
        const k=string();ws();if(raw[i++]!==':')throw Error('expected colon');
        props.set(k.key,val()); // decoded duplicate properties: last occurrence wins
        ws();if(raw[i]===','){i++;continue;}break;
      }
      if(raw[i++]!=='}')throw Error('expected object end');
      n={kind:'object',props};
    }else if(raw[i]==='['){
      i++;ws();const items=[];
      if(raw[i]!==']')while(true){
        items.push(val());ws();if(raw[i]===','){i++;continue;}break;
      }
      if(raw[i++]!==']')throw Error('expected array end');
      n={kind:'array',items};
    }else if(raw[i]==='"')n=string();
    else {
      const m=/^(?:-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null)/.exec(raw.slice(i));
      if(!m)throw Error('invalid scalar at '+i);
      i+=m[0].length;
      n={kind:/^(true|false)$/.test(m[0])?'boolean':m[0]==='null'?'null':'number'};
    }
    n.start=start;n.end=i;depth--;return n;
  }
  const root=val();ws();if(i!==raw.length)throw Error('trailing content');
  JSON.parse(raw); // final syntax authority: original JavaScript JSON parser
  function at(path){
    let n=root;
    for(const k of path){
      n=typeof k==='number'?(n.kind==='array'?n.items[k]:undefined):
        (n.kind==='object'?n.props.get(k):undefined);
      if(!n)throw Error('missing or shadowed JSON path');
    }
    return n;
  }
  return {at,bytes:raw.length,nodes,maxDepth};
}
const SOURCE_PATH=['fixtures',0,'clauses',0,'literals',0];
function patch(raw,token){
  const tree=scan(raw),leaf=tree.at(SOURCE_PATH);
  const a=Number(JSON.parse(raw.slice(leaf.start,leaf.end)));
  const b=Number(JSON.parse(token));
  if(!Number.isSafeInteger(a)||a===0||a!==b)throw Error('non-equivalent signed literal');
  const result=raw.slice(0,leaf.start)+token+raw.slice(leaf.end);
  const r=scan(result);r.at(SOURCE_PATH);
  return {text:result,originalBytes:raw.length,modifiedBytes:result.length,
    priorKind:leaf.kind,afterKind:r.at(SOURCE_PATH).kind,
    samePrefix:raw.slice(0,leaf.start)===result.slice(0,leaf.start),
    sameSuffix:raw.slice(leaf.end)===result.slice(leaf.start+token.length),
    scannerNodes:tree.nodes,scannerDepth:tree.maxDepth};
}
const baseline=d=>({version:d.version,fixtures:[d.fixtures[0]],summary:[d.summary[0]]});
function difficultPacket(data){
  const d=JSON.parse(JSON.stringify(baseline(data))),f=d.fixtures[0];
  const ids={s0:'__LSPV543_POS__',s1:'__LSPV543_NEG__'};
  for(const c of f.clauses)if(ids[c.id])c.id=ids[c.id];
  for(const p of f.proof)p.parents=p.parents.map(x=>ids[x]||x);
  for(const x of f.deleted)if(ids[x.sourceId])x.sourceId=ids[x.sourceId];
  let raw=JSON.stringify(d).replace(/"__LSPV543_POS__"/g,'1e400')
      .replace(/"__LSPV543_NEG__"/g,'-1e400');
  return '{"\\u0066ixtures":[],'+raw.slice(1);
}
function strictSource(raw){
  const f=JSON.parse(raw).fixtures[0];
  return f.clauses.every(c=>Array.isArray(c.literals)&&c.literals.length===3&&
    c.literals.every(x=>typeof x==='number'&&Number.isSafeInteger(x)&&x!==0));
}
function audit(data,native){
  const base=JSON.stringify(baseline(data)),alien=difficultPacket(data);
  const padded=patch(alien,'" 0001 "'),repaired=patch(padded.text,'1');
  const nested=patch(alien,'[[1]]'),hex=patch(alien,'"0x1"');
  const wrong=alien.replace('"literals":[1,','"literals":["2",');
  const badParent=alien.replace('"parents":["d0",','"parents":["missing",');
  const normalize=JSON.stringify(JSON.parse(padded.text));
  const test=[
    ['base',base,true],['escaped_shadow_infinite_ids',alien,true],
    ['padded_source',padded.text,true],['span_repaired',repaired.text,true],
    ['nested_source',nested.text,true],['hex_source',hex.text,true],
    ['wrong_source_value',wrong,false],['dangling_parent',badParent,false],
    ['global_reserialization',normalize,false]];
  const cases=test.map(([name,raw,expected])=>{
    const r=native(raw);if(r.accepted!==expected)throw Error(name+': '+JSON.stringify(r));
    return {name,accepted:r.accepted,bytes:raw.length,strictSource:strictSource(raw),
      checks:r.checks??null,error:r.error??null};
  });
  if(!padded.samePrefix||!padded.sameSuffix||!repaired.samePrefix||!repaired.sameSuffix)
    throw Error('nonlocal byte mutation');
  if(strictSource(padded.text)||!strictSource(repaired.text))throw Error('type firewall');
  if(scan(alien).at(['fixtures']).kind!=='array'||JSON.parse(alien).fixtures.length!==1)
    throw Error('last-key-wins');
  const f=data.fixtures[0],E=f.graph.edges.length;
  let sats=0;
  for(let a=0;a<(1<<E);a++)
    if(f.clauses.every(c=>c.literals.some(x=>((a>>(Math.abs(x)-1))&1)===(x>0?1:0))))
      sats++;
  if(sats!==0||f.clauses.length!==16||f.proof.length!==15)throw Error('K4 control');
  return {run:'LSPV2-543',scope:'recovered 341 fixture checker only',
    producerBlob:'4081022e8a3841d79f751a3d3a7a10decbb026da',
    checkerBlob:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
    graph:'K4',signedSourceClauses:16,paidDistinctNodes:15,originalSATModels:sats,
    sourcePath:SOURCE_PATH,spanPatch:{before:padded.originalBytes,after:padded.modifiedBytes,
      prefixUnchanged:padded.samePrefix,suffixUnchanged:padded.sameSuffix,
      scannerNodes:padded.scannerNodes,scannerDepth:padded.scannerDepth},
    cases,note:'Not a full R_mix341 parser, source-bound UNSAT checker, or SAT lower bound.'};
}
module.exports={scan,patch,baseline,difficultPacket,strictSource,audit};
if(require.main===module){
  const fs=require('fs'),cp=require('child_process'),os=require('os'),path=require('path');
  const root=path.resolve(__dirname,'../..');
  const producer=path.join(root,'experiments/arc/lspv2_341_mixed_tseitin_min_dag.js');
  const checker=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
  const data=JSON.parse(cp.execFileSync(process.execPath,[producer],{encoding:'utf8',maxBuffer:16e6}));
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-543-'));
  try{
    function native(raw){
      const file=path.join(dir,'packet.json');fs.writeFileSync(file,raw);
      try{return {accepted:true,checks:JSON.parse(cp.execFileSync(process.execPath,
        [checker,file],{encoding:'utf8',maxBuffer:2e6})).checks};}
      catch(e){return {accepted:false,error:(e.stderr?.toString()||e.message).slice(0,180)};}
    }
    console.log(JSON.stringify(audit(data,native),null,2));
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
}
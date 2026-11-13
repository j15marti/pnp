"use strict";
/* LSPV-1/612. Reproduce native /341 balanced malformed String-support paths.
   Exact inputs: original archived checker and published LSPV-1/609 SAT packet.
   No claim concerning the missing full historical mixed calculus.
   OS: node experiments/arc/lspv1_612_native341_support_namespace.cjs [raw.json]
*/
function gitBlobSha(text) {
  // For local OS pinning, the caller hashes bytes. Core hosted replay pins files externally.
  return null;
}
function deepCopy(x){return JSON.parse(JSON.stringify(x));}
function truthClause(c,bits){return c.literals.some(l=>l>0?bits[l-1]===1:bits[-l-1]===0);}
function sourceMap(f) {
  const E=f.graph.edges.length, inc=Array.from({length:f.graph.n},()=>[]);
  f.graph.edges.forEach(([u,v],i)=>{inc[u].push(i);inc[v].push(i);});
  const map=new Map();
  for(const c of f.clauses){
    const support=inc[c.vertex],tableBits=[];
    for(let m=0;m<8;m++){
      const bits=Array(E).fill(0);
      support.forEach((e,j)=>{bits[e]=(m>>j)&1;});
      tableBits.push(truthClause(c,bits)?1:0);
    }
    const table=tableBits.reduce((v,bit,i)=>v|(bit<<i),0);
    map.set(c.id,{support,table});
  }
  return map;
}
function keyOf(x){return String(x);}
function keyedBit(childSupport,m,parentKey) {
  let j=-1;
  for(let k=0;k<childSupport.length;k++)
    if(keyOf(childSupport[k])===keyOf(parentKey))j=k;
  return j<0?0:(m>>j)&1;
}
function specTable(a,b,childSupport) {
  const sup=[...new Set([...a.support,...b.support])];
  if(sup.length>3||sup.length!==childSupport.length||new Set(childSupport).size!==sup.length)
    throw Error("invalid local support cardinality");
  if(!sup.every(x=>childSupport.includes(x)))throw Error("invalid local membership");
  const lookup=(p,m)=>{
    let key=0;
    for(let i=0;i<p.support.length;i++)
      key|=keyedBit(childSupport,m,p.support[i])<<i;
    return (p.table>>key)&1;
  };
  let tab=0;
  for(let m=0;m<(1<<sup.length);m++)if(lookup(a,m)&&lookup(b,m))tab|=1<<m;
  return tab;
}
function originalLocalTable(a,b,childSupport,E) {
  const sup=[...new Set([...a.support,...b.support])];
  if(sup.length>3||childSupport.length!==sup.length||new Set(childSupport).size!==sup.length||
     !sup.every(x=>childSupport.includes(x)))throw Error("invalid support");
  const lookup=(p,bits)=>{
    let key=0;
    for(let i=0;i<p.support.length;i++)
      key|=Number(bits[p.support[i]])<<i;
    return (p.table>>key)&1;
  };
  let tab=0;
  for(let m=0;m<(1<<sup.length);m++){
    const bits=Array(E).fill(0);
    for(let j=0;j<childSupport.length;j++)bits[childSupport[j]]=(m>>j)&1;
    if(lookup(a,bits)&&lookup(b,bits))tab|=1<<m;
  }
  return tab;
}
function balanced(base,carrier) {
  const packet=deepCopy(base),f=packet.fixtures[0],E=f.graph.edges.length;
  if(f.proof.length!==47||f.graph.n!==12||E!==18)
    throw Error("unexpected base structure");
  const by=sourceMap(f),three=[];
  for(let i=0;i<f.proof.length;i++){
    const p=f.proof[i];
    if(i===15)p.support=carrier;
    if(i===16){p.parents=["s22","s23"];p.support=carrier;}
    if(i===17){p.parents=["d15","d16"];p.support=carrier;}
    if(p.rule==="AND3"){
      const [a,b]=p.parents.map(x=>by.get(x));
      if(!a||!b)throw Error("unavailable parent");
      const native=originalLocalTable(a,b,p.support,E),
            predicted=specTable(a,b,p.support);
      if(native!==predicted)throw Error("keyed transformer mismatch");
      p.table=native;
      if(i>=15&&i<=17)three.push({id:p.id,parents:p.parents.slice(),
        parentSupports:[a.support,b.support],support:p.support,table:native});
    }
    by.set(p.id,p);
  }
  const unchanged=["graph","charges","clauses","deleted","evenWitness","properties"]
    .every(k=>JSON.stringify(f[k])===JSON.stringify(base.fixtures[0][k]));
  if(!unchanged)throw Error("source data changed");
  return {packet,three};
}
function originalCheck(checkerSource,packet) {
  const outputs=[];
  try {
    const shimRequire=name=>{
      if(name==="fs")return {readFileSync:()=>JSON.stringify(packet)};
      throw Error("Unexpected Node require "+name);
    };
    (new Function("require","process","console",checkerSource))(
      shimRequire,{argv:["node","archived-checker.js","candidate.json"]},
      {log:x=>outputs.push(x)});
    if(outputs.length!==1)throw Error("unexpected checker stdout");
    return {accepted:true,body:JSON.parse(outputs[0])};
  }catch(e){return {accepted:false,error:String(e)};}
}
function testLocalArrayOfChars() {
  const a={support:"10A",table:0xf0},b={support:"10A",table:0xff};
  const s=["1","0","A"];
  return {parentSupports:[a.support,b.support],support:s,
    localGate:true,table:originalLocalTable(a,b,s,18),
    keyedTable:specTable(a,b,s)};
}
function run(checkerSource,base){
  const f=base.fixtures[0],E=f.graph.edges.length,modelBits=[];
  const models=[];
  for(let x=0;x<(1<<E);x++){
    for(let e=0;e<E;e++)modelBits[e]=(x>>e)&1;
    if(f.clauses.every(c=>truthClause(c,modelBits)))models.push(x);
  }
  if(models.length!==64)throw Error("source model count changed");
  const accepted=[],rejected=[],variants=[];
  for(const carrier of ["10A","A10","102","10\uD800"]){
    const made=balanced(base,carrier),o=originalCheck(checkerSource,made.packet);
    if(!o.accepted)throw Error("unexpected reject "+carrier+": "+o.error);
    accepted.push({carrier_json:JSON.stringify(carrier),checks:o.body.checks,
      tables:made.three.map(z=>z.table),
      d17_parent_supports:made.three[2].parentSupports,
      paid_nodes:made.packet.fixtures[0].proof.length});
    variants.push(made);
  }
  const broken=[];
  const b0=deepCopy(variants[0].packet);
  b0.fixtures[0].proof[17].table^=1;
  broken.push(["wrong_table",b0]);
  const b1=deepCopy(variants[0].packet);
  b1.fixtures[0].proof[17].row.rhs=1;
  broken.push(["wrong_alias_rhs",b1]);
  const b2=deepCopy(variants[0].packet);
  b2.fixtures[0].proof[17].parents=["d15","s23"];
  broken.push(["mixed_string_numeric_parent",b2]);
  const b3=deepCopy(variants[0].packet);
  b3.fixtures[0].proof[17].support=["1","0","A"];
  broken.push(["string_to_character_array_invalid_terminal_row",b3]);
  const b4=deepCopy(variants[0].packet);
  b4.fixtures[0].proof[17].parents=["missing","d16"];
  broken.push(["unknown_parent",b4]);
  const b5=deepCopy(variants[0].packet);
  b5.fixtures[0].clauses[0].literals[0]=999;
  broken.push(["changed_signed_source",b5]);
  for(const [name,pkt] of broken){
    const o=originalCheck(checkerSource,pkt);
    if(o.accepted)throw Error("hostile mutation accepted: "+name);
    rejected.push({name,error:o.error});
  }
  const local=testLocalArrayOfChars();
  if(local.table!==local.keyedTable||local.table!==0xf0)
    throw Error("String-to-Array local transformer regression");
  if(accepted.some(a=>a.checks!==5155)||accepted[0].tables.join(",")!=="153,255,153"||
    accepted[1].tables.join(",")!=="195,255,195")
    throw Error("pinned native checks/tables mismatch");
  return {
    result:"PASS",scope:"Pinned archived /341 fixture ONLY; missing full historical R_mix341",
    originalCheckerBlob:"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0",
    baselinePacketBlob:"8d6d9bc7f2940a77edf2a07fcb72af111ba5b928",
    sourceModels:models.length,firstModelBits:Array.from({length:E},(_,i)=>(models[0]>>i)&1).join(""),
    accepted,hostileRejected:rejected,localCharArrayShape:local,
    proofStatus:"PROVED/RESTRICTED exact source-code key transformer + COMPUTATIONAL checker replay",
    note:"Full accepted /609 source SAT despite checker acceptance. No legal full mixed-calculus proof."
  };
}
if(typeof module!=="undefined")module.exports={run,balanced,originalCheck,specTable,originalLocalTable};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
  const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
  const root=path.resolve(__dirname,"../..");
  const ck=path.join(root,"experiments/arc/lspv2_341_independent_verify.js");
  const bp=path.join(root,"results/raw/arc/2026-11-12_2100_LSPV1_609_BRIDGE_SLICE_SAT_ACCEPTED.json");
  const blob=bytes=>crypto.createHash("sha1").update(Buffer.from("blob "+bytes.length+"\0")).update(bytes).digest("hex");
  const c=fs.readFileSync(ck),b=fs.readFileSync(bp);
  if(blob(c)!=="fcb7d4ced8f922de14c0bda16263a8cc7853e8e0"||
     blob(b)!=="8d6d9bc7f2940a77edf2a07fcb72af111ba5b928")
     throw Error("original checker or baseline packet SHA mismatch");
  const result=run(c.toString("utf8"),JSON.parse(b.toString("utf8")));
  const out=JSON.stringify(result,null,2)+"\n";
  if(process.argv[2])fs.writeFileSync(process.argv[2],out);
  process.stdout.write(out);
}

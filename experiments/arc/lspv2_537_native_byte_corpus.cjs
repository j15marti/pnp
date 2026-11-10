#!/usr/bin/env node
"use strict";
/* LSPV-2/537. Execute exact PINNED historical source files via a V8 I/O shim.
 NOT a new authoritative checker or an authenticated full R_mix341 grammar.
 node experiments/arc/lspv2_537_native_byte_corpus.cjs [output.json]
*/
const fs=require("fs"),crypto=require("crypto");
const paths={producer:"experiments/arc/lspv2_341_mixed_tseitin_min_dag.js",checker:"experiments/arc/lspv2_341_independent_verify.js"};
const pin={producer:"4081022e8a3841d79f751a3d3a7a10decbb026da",checker:"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0"};
function shaGit(s){const b=Buffer.from(s,"utf8");return crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+b.length+" "),Buffer.from([0]),b])).digest("hex");}
function audit(producerText,checkerText){
  let pOut=[];
  new Function("console",producerText)({log:x=>pOut.push(x)});
  const data=JSON.parse(pOut[0]), z=data.fixtures[0], copy=x=>JSON.parse(JSON.stringify(x));
  const f={
    graph:{n:z.graph.n,edges:z.graph.edges},charges:z.charges,
    clauses:z.clauses.map(c=>({id:c.id,vertex:c.vertex,literals:c.literals})),
    proof:z.proof.map(p=>({id:p.id,rule:p.rule,kind:p.kind,parents:p.parents,...(p.support?{support:p.support,table:p.table}:{}),...(p.row?{row:p.row}:{})})),
    deleted:z.deleted,evenWitness:z.evenWitness,properties:{essential:z.properties.essential}
  };
  const minimal={fixtures:[f],summary:[null]};
  function nativeCheck(bytes){
    let stdout=[];
    try{
      new Function("require","process","console",checkerText)(
        ()=>({readFileSync:()=>bytes}),{argv:["node","historical341","candidate.json"]},{log:s=>stdout.push(s)});
      let x=JSON.parse(stdout[0]);return {accepted:true,checks:x.checks,fixtures:x.cases.length};
    }catch(e){return {accepted:false,diagnostic:String(e).slice(0,160)};}
  }
  const sourceDimacs= "p cnf "+f.graph.edges.length+" "+f.clauses.length+"\n"+f.clauses.map(c=>c.literals.join(" ")+" 0").join("\n")+"\n";
  const cases=[];
  function add(id,change,want,meaning){
    let o=copy(minimal);change(o);let bytes=JSON.stringify(o);
    let result=nativeCheck(bytes);
    if(result.accepted!==want)throw Error(id+" expected "+want+" but "+JSON.stringify(result));
    cases.push({id,expected:want,meaning,byteLength:bytes.length,checker:result,packetBytes:bytes});
  }
  add("K4_MINIMAL_SOURCE_AND3_XOR",()=>{},true,"one-fixture valid source, 15 unique paid nodes, native checker");
  add("SOURCE_METADATA_MATCHES",o=>o.fixtures[0].externalOriginalInput=sourceDimacs,true,"external source metadata ignored even if matching");
  add("SOURCE_METADATA_SAT_SPOOF",o=>o.fixtures[0].externalOriginalInput="p cnf 1 1\n1 0\n",true,"native checker ignores external original input; source binding must be separate");
  add("FORGED_CONTEXT_WEIGHT",o=>o.fixtures[0].proof.forEach(p=>{p.context=["x=0"];p.weight=0;p.exportedWire="UNVALIDATED";}),true,"native checker ignores branch and weight metadata");
  add("FORGED_VERSION",o=>{o.version="MALICIOUS-CLAIM";o.definition="DEF and DISCHARGE are free";},true,"version and description ignored");
  add("FAKE_SUMMARY",o=>o.summary[0]={name:"SAT",nodes:0},true,"summary content ignored");
  for(const tag of ["RES","LOCAL-CONVERT","DEF","SOURCE","SPLIT","ASSUME","DISCHARGE","JOIN","DELETE","WEAKEN","GF(2)","RAT"]){
    add("UNSUPPORTED_"+tag,o=>o.fixtures[0].proof[0].rule=tag,false,"only historical checker sublanguage, NOT a full-calculus invalidity result");
  }
  add("AND3_FALSE_TABLE",o=>o.fixtures[0].proof[0].table^=1,false,"semantic conjunction forgery");
  add("XOR_FALSE_ROW",o=>o.fixtures[0].proof.find(p=>p.rule==="XOR").row.mask="0x555",false,"semantic affine computation forgery");
  add("SOURCE_OUT_OF_RANGE",o=>o.fixtures[0].clauses[0].literals[0]=999,false,"original source signed incidence forgery");
  add("SOURCE_WRONG_SIGN",o=>o.fixtures[0].clauses[0].literals[0]*=-1,false,"wrong original signed source");
  add("PARENT_NOT_PRESENT",o=>o.fixtures[0].proof[0].parents[0]="missing",false,"dependency does not exist");
  add("DUPLICATE_PAID_ID",o=>o.fixtures[0].proof[1].id=o.fixtures[0].proof[0].id,false,"paid identity collision");
  add("WRONG_CONTRADICTION",o=>o.fixtures[0].proof.at(-1).row.rhs=0,false,"sink not 0=1");
  add("BAD_DELETION_WITNESS",o=>o.fixtures[0].deleted[0].assignment="000001",false,"source deletion model invalid");
  add("WRONG_SUMMARY_COUNT",o=>o.summary=[],false,"summary length");
  add("VALID_REDUNDANT_PAID_PADDING",o=>{let p=copy(o.fixtures[0].proof[0]);p.id="extra";o.fixtures[0].proof.splice(1,0,p);},false,"valid isolated AND3 inference is forbidden solely by 4V-1 length guard");
  const baseline=nativeCheck(JSON.stringify(data));
  if(!baseline.accepted||baseline.checks!==30714||baseline.fixtures!==7)throw Error("pinned history drift");
  function referenceReplay(f){
    const E=f.graph.edges.length, all=new Map(), paid=new Set(), originals=new Set();
    for(let c of f.clauses){
      if(originals.has(c.id))throw Error("duplicate source");originals.add(c.id);
      let support=[...new Set(c.literals.map(v=>Math.abs(v)-1))],table=0;
      for(let i=0;i<1<<support.length;i++){
        if(c.literals.some(l=>((i>>support.indexOf(Math.abs(l)-1))&1)===(l>0?1:0)))table|=1<<i;
      }
      all.set(c.id,{kind:"factor",support,table,parents:[]});
    }
    const val=(a,bits)=>(a.table>>a.support.reduce((k,e,j)=>k|((bits[e]||0)<<j),0))&1;
    for(const p of f.proof){
      if(all.has(p.id)||p.parents.length!==2||p.parents[0]===p.parents[1])throw Error("paid identity/arity");
      const a=all.get(p.parents[0]),b=all.get(p.parents[1]);if(!a||!b)throw Error("dangling parents");
      if(p.rule==="AND3"){
        if(a.kind!=="factor"||b.kind!=="factor"||p.kind!=="factor")throw Error("AND3 type");
        let support=[...new Set([...a.support,...b.support])];
        if(support.length>3||p.support.length!==support.length||support.some(e=>!p.support.includes(e)))throw Error("AND3 support");
        let table=0;for(let i=0;i<(1<<p.support.length);i++){
          let bits=Array(E).fill(0);p.support.forEach((e,j)=>bits[e]=(i>>j)&1);
          if(val(a,bits)&&val(b,bits))table|=1<<i;
        }
        if(table!==p.table)throw Error("AND3 table");
        if(p.row){
          for(let i=0;i<1<<p.support.length;i++){
            let bits=Array(E).fill(0);p.support.forEach((e,j)=>bits[e]=(i>>j)&1);
            let parity=0,mask=BigInt(p.row.mask);
            for(let e=0;e<E;e++)if((mask>>BigInt(e))&1n)parity^=bits[e];
            if(((p.table>>i)&1)!==Number(parity===p.row.rhs))throw Error("affine alias");
          }
        }
      } else if(p.rule==="XOR"){
        if(!a.row||!b.row||p.kind!=="affine"||!p.row)throw Error("XOR typing");
        if((BigInt(a.row.mask)^BigInt(b.row.mask))!==BigInt(p.row.mask)||p.row.rhs!==(a.row.rhs^b.row.rhs))throw Error("XOR");
      }else throw Error("non-native rule left UNKNOWN");
      paid.add(p.id);all.set(p.id,p);
    }
    const last=f.proof.at(-1);
    if(last.kind!=="affine"||BigInt(last.row.mask)!==0n||last.row.rhs!==1)throw Error("invalid goal");
    let visited=new Set();function visit(id){if(visited.has(id))return;visited.add(id);for(const q of all.get(id).parents)visit(q);}
    visit(last.id);
    if([...originals].some(id=>!visited.has(id)))throw Error("missing source dependency");
    return {sourceNodes:originals.size,paidOnce:paid.size,ancestors:visited.size,contexts:"empty",definitions:"none",logicalWork:paid.size,certificateBits:"separate",peakSpace:"not inferred"};
  }
  const ref=referenceReplay(f);
  if(ref.sourceNodes!==16||ref.paidOnce!==15)throw Error("reference replay failed");
  let nGood=cases.filter(x=>x.checker.accepted).length,nBad=cases.length-nGood;
  return {id:"LSPV2-537-NATIVE341-MINIMAL-BYTE-CORPUS",status:"COMPUTATIONAL; recovered historical SOURCE/AND3/XOR checker ONLY",sourceBlobs:{producer:"4081022e8a3841d79f751a3d3a7a10decbb026da",checker:"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0"},original:{...baseline},minimal:{packetBytes:cases[0].packetBytes,byteLength:cases[0].byteLength,sourceDimacs,reference:ref},totals:{cases:cases.length,accepted:nGood,rejected:nBad},cases,model:{alpha:"project to exact source-labelled typed factor/affine DAG, empty contexts, unique paid IDs; ignore untrusted metadata",gamma:"all accepted byte variants with same checked projection",costPolarity:"projected distinct paid count <= concrete paid count; unknown rules/historical weight semantics overapproximate",cegar:"forged XOR is allowed in kind-only abstraction but concrete checker rejects; adding exact affine row semantics rejects; true 15-paid K4 path retained",unknown:"RES LOCAL-CONVERT DEF context/branch/discharge exported/private wires remain OPEN; absence from checker is not absence from declared R_mix341"},open:["P2-D1","P2-C3","P2-B1","P2-B2"]};
}
const source={};
for(const k of Object.keys(paths)){source[k]=fs.readFileSync(paths[k],"utf8");if(shaGit(source[k])!==pin[k])throw Error("historical Git blob mismatch: "+k);}
const raw=audit(source.producer,source.checker);
raw.packetSHA256=Object.fromEntries(raw.cases.map(x=>[x.id,crypto.createHash("sha256").update(x.packetBytes,"utf8").digest("hex")]));
raw.originalSourceSHA256=crypto.createHash("sha256").update(raw.minimal.sourceDimacs,"utf8").digest("hex");
const rendered=JSON.stringify(raw,null,2)+"\n";
if(process.argv[2])fs.writeFileSync(process.argv[2],rendered,"utf8");else process.stdout.write(rendered);

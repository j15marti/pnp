'use strict';
// LSPV-1/555. Independent strict audit kernel, SOURCE/AND3/XOR only.
// NOT historical R_mix341 byte grammar, NOT authoritative checker.
const okay=(b,msg)=>{if(!b)throw Error("STRICT: "+msg)};
const num=x=>typeof x==="number"&&Number.isSafeInteger(x)&&x>=0;
const key=(x,p)=>typeof x==="string"&&new RegExp("^"+p+"[0-9]+$").test(x);
const enc=f=>"p cnf "+f.graph.edges.length+" "+f.clauses.length+"\n"+
  f.clauses.map(c=>c.literals.join(" ")+" 0").join("\n")+"\n";
function parse(src){
 okay(typeof src==="string","source not byte string");
 const lines=src.trimEnd().split("\n"),h=/^p cnf ([0-9]+) ([0-9]+)$/.exec(lines[0]);
 okay(h!==null,"source header");
 const n=Number(h[1]),m=Number(h[2]);
 okay(num(n)&&num(m)&&n>=3&&lines.length===m+1,"source dimensions");
 const clauses=lines.slice(1).map(l=>{
  const v=l.trim().split(/\s+/);
  okay(v.length===4&&v[3]==="0"&&v.slice(0,3).every(t=>/^-?[0-9]+$/.test(t)),"literal tokens");
  const c=v.slice(0,3).map(Number);
  okay(c.every(x=>Number.isSafeInteger(x)&&x!==0&&Math.abs(x)<=n),"signed literals");
  okay(new Set(c.map(Math.abs)).size===3,"proper 3-CNF");
  return c;
 });
 return {n,clauses};
}
function row(r,n){
 okay(r&&typeof r.mask==="string"&&/^0x(?:0|[1-9a-f][0-9a-f]*)$/i.test(r.mask)&&
   (r.rhs===0||r.rhs===1),"row type");
 const mask=BigInt(r.mask);okay((mask>>BigInt(n))===0n,"row variables");
 return {mask,rhs:r.rhs};
}
function evalFactor(v,b){
 let idx=0;v.support.forEach((x,i)=>{if(b.get(x))idx|=1<<i});return (v.table>>idx)&1;
}
function kernel(f,src){
 const {n,clauses}=parse(src);
 okay(f&&Array.isArray(f.clauses)&&Array.isArray(f.proof)&&f.clauses.length===clauses.length,"packet");
 const env=new Map();
 for(let j=0;j<clauses.length;j++){
  const c=f.clauses[j],l=clauses[j];
  okay(c&&key(c.id,"s")&&!env.has(c.id),"source ID");
  okay(Array.isArray(c.literals)&&c.literals.length===3&&l.every((x,i)=>
    typeof c.literals[i]==="number"&&c.literals[i]===x),"original DIMACS binding");
  let t=0;for(let v=0;v<8;v++)if(l.some((x,i)=>((v>>i)&1)===(x>0?1:0)))t|=1<<v;
  env.set(c.id,{kind:"factor",support:l.map(x=>Math.abs(x)-1),table:t});
 }
 if(f.charges!==undefined)okay(Array.isArray(f.charges)&&f.charges.every(x=>x===0||x===1),"charge metadata type");
 for(const p of f.proof){
  okay(p&&key(p.id,"d")&&!env.has(p.id),"paid identity freshness");
  okay(Array.isArray(p.parents)&&p.parents.length===2&&p.parents.every(x=>typeof x==="string")&&p.parents[0]!==p.parents[1],"parent IDs");
  const [a,b]=p.parents.map(x=>env.get(x));okay(a&&b,"prior premises");
  let child;
  if(p.rule==="AND3"){
   okay(p.kind==="factor"&&a.kind==="factor"&&b.kind==="factor","AND3 type");
   const u=[...new Set([...a.support,...b.support])],s=p.support;
   okay(Array.isArray(s)&&s.every(x=>num(x)&&x<n)&&new Set(s).size===s.length&&
     s.length===u.length&&u.every(x=>s.includes(x))&&s.length<=3,"exact support");
   okay(num(p.table)&&p.table<(1<<(1<<s.length)),"factor bits");
   let t=0;for(let v=0;v<(1<<s.length);v++){
    const bits=new Map(s.map((x,i)=>[x,(v>>i)&1]));
    if(evalFactor(a,bits)&&evalFactor(b,bits))t|=1<<v;
   }
   okay(t===p.table,"actual conjunction");
   child={kind:"factor",support:s.slice(),table:t};
   if(p.row!==undefined){
    const z=row(p.row,n);
    okay([...Array(n).keys()].every(x=>((z.mask>>BigInt(x))&1n)===0n||s.includes(x)),"affine scoped");
    for(let v=0;v<(1<<s.length);v++){
     let parity=0;for(let i=0;i<s.length;i++)if(((z.mask>>BigInt(s[i]))&1n)!==0n)parity^=(v>>i)&1;
     okay(((t>>v)&1)===(parity===z.rhs?1:0),"affine alias");
    }
    child.row=z;
   }
  }else if(p.rule==="XOR"){
   okay(p.kind==="affine"&&a.row&&b.row,"GF2 type");
   const z=row(p.row,n);
   okay(z.mask===(a.row.mask^b.row.mask)&&z.rhs===(a.row.rhs^b.row.rhs),"GF2 step");
   child={kind:"affine",row:z};
  }else throw Error("STRICT: unsupported rule outside audited fragment");
  env.set(p.id,child);
 }
 okay(f.proof.length>0,"empty proof");
 const sink=env.get(f.proof.at(-1).id);
 okay(sink.kind==="affine"&&sink.row&&sink.row.mask===0n&&sink.row.rhs===1,"terminal contradiction");
 return {sourceVariables:n,clauses:clauses.length,paid:f.proof.length};
}
module.exports={kernel,enc,parse};
if(require.main===module){
 const fs=require("node:fs"),cp=require("node:child_process"),crypto=require("node:crypto");
 const p="experiments/arc/lspv2_341_mixed_tseitin_min_dag.js";
 const v="experiments/arc/lspv2_341_independent_verify.js";
 const h="results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json";
 const sha=s=>{let b=Buffer.from(s);return crypto.createHash("sha1").update("blob "+b.length+"\0").update(b).digest("hex")};
 okay(sha(fs.readFileSync(p,"utf8"))==="4081022e8a3841d79f751a3d3a7a10decbb026da","producer pin");
 okay(sha(fs.readFileSync(v,"utf8"))==="fcb7d4ced8f922de14c0bda16263a8cc7853e8e0","checker pin");
 okay(sha(fs.readFileSync(h,"utf8"))==="706947c767361e7c979b8208677eb983d33838f4","SAT packet pin");
 const baseline=JSON.parse(cp.execFileSync(process.execPath,[p],{encoding:"utf8",maxBuffer:1e7}));
 const forgery=JSON.parse(fs.readFileSync(h,"utf8"));
 const positive=baseline.fixtures.map(x=>({fixture:x.graph.name,...kernel(x,enc(x))}));
 const clone=x=>JSON.parse(JSON.stringify(x)), negative=[];
 function reject(name,input,fn){
  let f=clone(input);if(fn)fn(f);
  try{kernel(f,enc(input))}catch(e){negative.push({name,rejected:true,error:e.message});return}
  throw Error("hostile passed: "+name);
 }
 reject("SAT-source forged proof",forgery.fixtures[1]);
 const k=baseline.fixtures[0];
 reject("literal string",k,f=>{f.clauses[0].literals[0]="1"});
 reject("support string",k,f=>{f.proof[2].support="012"});
 reject("unsafe paid ID",k,f=>{f.proof[0].id=9007199254740993});
 reject("false GF2 sink",k,f=>{f.proof.at(-1).row.rhs=0});
 reject("false AND3",k,f=>{f.proof[2].table^=1});
 reject("future reference",k,f=>{f.proof[0].parents[0]="d999"});
 reject("outside fragment RES",k,f=>{f.proof[0].rule="RES"});
 let changed=enc(k).replace("1 2 3 0","-1 2 3 0");
 try{kernel(k,changed);throw Error("external mutation accepted")}catch(e){
  okay(e.message==="STRICT: original DIMACS binding","mismatch control");
  negative.push({name:"external source substitution",rejected:true,error:e.message});
 }
 let padded=clone(k),extra=clone(k.proof[0]);extra.id="d9999";padded.proof.splice(-1,0,extra);
 const pad=kernel(padded,enc(k));okay(pad.paid===k.proof.length+1,"padding");
 console.log(JSON.stringify({positive,negative,pad,scope:"new strict audit checker only; NOT native R_mix341 parser"},null,2));
}
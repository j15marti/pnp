#!/usr/bin/env node
import fs from "node:fs";
import crypto from "node:crypto";

const started=process.hrtime.bigint(), path=process.argv[2];
if(!path)throw Error("usage: verifier record.json");
const original=JSON.parse(fs.readFileSync(path,"utf8"));
let checks=0;const ok=(p,m)=>{if(!p)throw Error(m);checks++};
const N=15,A=1<<N,BYTES=A/8;
const truth=(lit,a)=>((a>>(Math.abs(lit)-1))&1)===(lit>0?1:0);
const sat=(cl,a)=>cl.some(l=>truth(l,a));
function maskFor(pred){const b=Buffer.alloc(BYTES);for(let a=0;a<A;a++)if(pred(a))b[a>>3]|=1<<(a&7);return b}
const andMask=(x,y)=>{const b=Buffer.alloc(BYTES);for(let i=0;i<BYTES;i++)b[i]=x[i]&y[i];return b};
const subset=(x,y)=>{for(let i=0;i<BYTES;i++)if((x[i]&~y[i])!==0)return false;return true};
const hash=b=>crypto.createHash("sha256").update(b).digest("hex");
const clauseMask=c=>maskFor(a=>sat(c,a));
const affineMask=(vs,rhs)=>maskFor(a=>vs.reduce((z,v)=>z^((a>>(v-1))&1),0)===rhs);
const union=(a,b)=>[...new Set([...a,...b])].sort((x,y)=>x-y);
const xorSet=(a,b)=>[...new Set([...a,...b].filter(x=>!(a.includes(x)&&b.includes(x))))].sort((x,y)=>x-y);

function independentSource(){
 const edges=[];for(const off of [0,5])for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)
   (u===0&&v===1)?edges.push([off,off+4],[off+4,off+1]):edges.push([off+u,off+v]);
 edges.push([4,9]);const inc=Array.from({length:10},()=>[]);edges.forEach(([u,v],i)=>{inc[u].push(i+1);inc[v].push(i+1)});
 const chi=[1,0,0,0,0,0,0,0,0,0],F=[];
 for(let v=0;v<10;v++)for(let t=0;t<8;t++){
  const bits=[(t>>2)&1,(t>>1)&1,t&1];if((bits[0]^bits[1]^bits[2])===chi[v])continue;
  F.push(inc[v].map((e,j)=>bits[j]?-e:e));
 }
 const dimacs=`p cnf 15 40\n${F.map(c=>`${c.join(" ")} 0\n`).join("")}`;
 return {edges,inc,chi,F,sha:crypto.createHash("sha256").update(dimacs).digest("hex")};
}

function replay(rec){try{
 const src=independentSource(),F=src.F,D=[];
 if(JSON.stringify(F)!==JSON.stringify(rec.source.clauses)||src.sha!==rec.source.dimacs_sha256)return false;
 const get=([k,v])=>k==="s"?{mask:clauseMask(F[v]),support:F[v].map(Math.abs).sort((a,b)=>a-b),clause:F[v],affine:null}:D[v];
 for(const n of rec.trace){
  if(n.id!==D.length)return false;const ps=n.parents.map(get);if(ps.some(x=>!x))return false;let out;
  if(n.rule==="AND3"){
   if(ps.length!==2)return false;const support=union(ps[0].support,ps[1].support);if(support.length>3)return false;
   const mask=andMask(ps[0].mask,ps[1].mask);let affine=null;
   if(n.affine){affine={vars:[...n.affine.vars],rhs:n.affine.rhs};if(!affineMask(affine.vars,affine.rhs).equals(mask))return false}
   out={mask,support,clause:null,affine};
  }else if(n.rule==="XOR"){
   if(ps.length!==2||!ps[0].affine||!ps[1].affine)return false;
   const vars=xorSet(ps[0].affine.vars,ps[1].affine.vars),rhs=ps[0].affine.rhs^ps[1].affine.rhs;
   out={mask:affineMask(vars,rhs),support:vars,clause:null,affine:{vars,rhs}};
  }else if(n.rule==="LOCAL"){
   if(ps.length!==1||!Array.isArray(n.clause))return false;const mask=clauseMask(n.clause);if(!subset(ps[0].mask,mask))return false;
   out={mask,support:n.clause.map(Math.abs).sort((a,b)=>a-b),clause:n.clause,affine:null};
  }else if(n.rule==="RES"){
   if(ps.length!==2||!ps[0].clause||!ps[1].clause)return false;const p=n.pivot;
   if(!ps[0].clause.includes(p)||!ps[1].clause.includes(-p))return false;const clause=[];
   for(const l of [...ps[0].clause,...ps[1].clause])if(l!==p&&l!==-p&&!clause.includes(l))clause.push(l);
   if(clause.some(l=>clause.includes(-l)))return false;out={mask:clauseMask(clause),support:clause.map(Math.abs).sort((a,b)=>a-b),clause,affine:null};
  }else return false;
  if(JSON.stringify(out.support)!==JSON.stringify(n.support)||hash(out.mask)!==n.mask_sha256)return false;
  if((n.clause||out.clause)&&JSON.stringify(n.clause)!==JSON.stringify(out.clause))return false;
  if(n.affine||out.affine){
   if(!n.affine||!out.affine||n.affine.rhs!==out.affine.rhs||JSON.stringify(n.affine.vars)!==JSON.stringify(out.affine.vars))return false;
  }
  D.push(out);
 }
 const root=get(rec.root);return !!root&&root.clause?.length===0&&root.mask.every(x=>x===0);
}catch{return false}}

const src=independentSource();ok(src.sha==="4f8a7e613ace4f67cd0b62204cdda2a4d8072047bd55a70da23da282e3537b18","source hash");
ok(src.F.length===40&&src.edges.length===15,"source sizes");
let models=0;const oneBad=new Map();for(let a=0;a<A;a++){
 const bad=src.F.map((c,i)=>sat(c,a)?-1:i).filter(i=>i>=0);if(!bad.length)models++;if(bad.length===1&&!oneBad.has(bad[0]))oneBad.set(bad[0],a);
}
ok(models===0&&oneBad.size===36,"complete UNSAT and essential set");
ok(JSON.stringify([...oneBad.keys()].sort((a,b)=>a-b))===JSON.stringify(original.core),"core ids");
for(const [sid,a] of oneBad){ok(!sat(src.F[sid],a),"deleted false");ok(src.F.every((c,i)=>i===sid||sat(c,a)),"complete deletion witness")}
ok(replay(original),"complete typed replay");
ok(original.work===37&&original.span===7,"work span");
ok(JSON.stringify(original.rule_counts)===JSON.stringify({AND3:28,LOCAL:2,RES:1,XOR:6}),"rule counts");
ok(JSON.stringify(original.ancestry)===JSON.stringify({cycle_rank:0,dependency_edges:72,nullary_paid:0,paid_nodes:37,unary_paid:2,used_sources:36}),"Euler ledger");

const mutants=[];
let m=structuredClone(original);m.trace[0].parents[0]=["s",39];mutants.push(m);
m=structuredClone(original);const xi=m.trace.find(n=>n.rule==="XOR");xi.affine.rhs^=1;mutants.push(m);
m=structuredClone(original);const lo=m.trace.find(n=>n.rule==="LOCAL");lo.clause=[-lo.clause[0]];mutants.push(m);
m=structuredClone(original);const rr=m.trace.find(n=>n.rule==="RES");rr.parents.reverse();mutants.push(m);
m=structuredClone(original);m.trace.pop();mutants.push(m);
m=structuredClone(original);m.trace[0].mask_sha256="00".repeat(32);mutants.push(m);
m=structuredClone(original);m.source.clauses[0][0]*=-1;mutants.push(m);
m=structuredClone(original);m.trace.find(n=>n.rule==="AND3").support=[1,2,3,4];mutants.push(m);
for(const x of mutants)ok(!replay(x),"hostile mutation rejected");

console.log(JSON.stringify({pass:true,checks,mutations_rejected:mutants.length,source_models:models,essential:oneBad.size,
 work:original.work,span:original.span,elapsed_seconds:Number(process.hrtime.bigint()-started)/1e9,
 max_rss_kib:process.resourceUsage().maxRSS,scope:"rule-level independent replay; no authoritative historical byte checker"}));

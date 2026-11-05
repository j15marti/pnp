#!/usr/bin/env node
"use strict";
/* LSPV-2/414. Deterministic exhaustive producer. Run:
   node experiments/arc/lspv2_414_paid_def_support.js
   Writes results/raw/arc/2026-11-05_0312_LSPV2_414_PAID_DEF_SUPPORT3_raw.json
   This tests legal conservative paid-DEF prefixes, NOT native AND3 consumption. */
const fs=require("fs"), path=require("path");
const clauses=[[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]];
const selector=[3,4,5,6],u=7,src=[[u],...[1,2,3,4,5,6].map(x=>[u,x])];
function gate(g,op,a,b) {
 const id=8+g.length;
 if(!["NOT","AND","OR"].includes(op)||[a,b].some(x=>x<1||x>=id))
    throw Error("illegal paid 2-input gate");
 g.push({id,op,a,b});return id;
}
function compile(cs){
 const g=[],inv=gate(g,"NOT",1,1),one=gate(g,"OR",1,inv);
 let c=one;
 for(const cl of cs){
    let d=null;
    for(const l of cl){const w=l>0?l:gate(g,"NOT",-l,-l);d=d===null?w:gate(g,"OR",d,w);}
    c=gate(g,"AND",c,d);
 }
 for(const s of selector)c=gate(g,"AND",c,s);
 return {g,out:gate(g,"OR",u,c)};
}
function evaluate(g,out,a){
 const v=Array(8+g.length).fill(false);
 for(let j=1;j<=7;j++)v[j]=!!(a&(1<<(j-1)));
 for(const t of g){const x=v[t.a],y=v[t.b];v[t.id]=t.op==="NOT"?!x:t.op==="AND"?(x&&y):(x||y);}
 return v[out];
}
function clauseTrue(c,a){return c.some(l=>l>0?!!(a&(1<<(l-1))):!(a&(1<<(-l-1))));}
function sourceTrue(a){return src.every(c=>clauseTrue(c,a));}
function cnfSat(cs){return [0,1,2,3].some(a=>cs.every(c=>clauseTrue(c,a)));}
function main(){
 let checks=0;const rows=[];
 for(let mask=0;mask<256;mask++){
   const cs=clauses.filter((_,i)=>!!(mask&(1<<i))),sat=cnfSat(cs),{g,out}=compile(cs);
   const truth=Array.from({length:128},(_,a)=>evaluate(g,out,a)),support=[];
   for(let v=1;v<=7;v++){
     if(truth.some((b,a)=>b!==truth[a^(1<<(v-1))]))support.push(v);
     checks+=128;
   }
   if((support.length<=3)!==(!sat))throw Error("reduction fails");
   checks++;
   for(let a=0;a<128;a++){
     const source=sourceTrue(a),direct=!!(a&64)||(selector.every(s=>!!(a&(1<<(s-1))))&&cs.every(c=>clauseTrue(c,a)));
     if(truth[a]!==direct||(source&&!truth[a]))throw Error("invalid gate extension or entailment");
     checks+=source?2:1;
   }
   if(g.some((t,j)=>t.id!==j+8||t.a>=t.id||t.b>=t.id))throw Error("bad gate record");
   checks++;
   rows.push({mask,sat,support,gates:g.length,out});
 }
 const total={
 cases:256,SAT:rows.filter(r=>r.sat).length,UNSAT:rows.filter(r=>!r.sat).length,
 small_support:rows.filter(r=>r.support.length<=3).length,
 gate_min:Math.min(...rows.map(r=>r.gates)),gate_max:Math.max(...rows.map(r=>r.gates)),
 checks,all_source_models:64,source_clauses:src.length,original_vars:7,
 source_ascii_bytes:("p cnf 7 7\n"+src.map(c=>c.join(" ")+" 0\n").join("")).length
 };
 const output={metadata:{description:"Exhaustive 256 two-variable CNF predicates; each compiled to individually paid conservative two-input DEF gates; syntactic source F=(u) AND ∏(u OR v); entire extension is unique. Named output h=u OR (C(X) AND s1 AND ... AND s4).",clauses,source:src,selector,unit:u,restriction:"The output's global essential support is tested; this does not grant native AND3 or GF2 export of that output.",no_randomness:true},total,rows};
 const dest=path.join("results","raw","arc","2026-11-05_0312_LSPV2_414_PAID_DEF_SUPPORT3_raw.json");
 fs.mkdirSync(path.dirname(dest),{recursive:true});
 fs.writeFileSync(dest,JSON.stringify(output,null,2)+"\n");
 console.log(JSON.stringify(total,null,2));
}
if(require.main===module)main();

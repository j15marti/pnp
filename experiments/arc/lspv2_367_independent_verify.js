"use strict";
const fs=require("fs");
function need(x,m){if(!x)throw Error(m);}
function literals(v,n){
 need(Array.isArray(v),"clause type");let s=new Set();
 for(let x of v){need(Number.isInteger(x)&&x!==0&&Math.abs(x)<=n,"literal range");
 need(!s.has(x)&&!s.has(-x),"duplicate/tautology");s.add(x);}return s;
}
function equal(a,b){return a.size===b.size&&[...a].every(x=>b.has(x));}
function resolve(a,b,p){
 need(Number.isInteger(p)&&p>0&&a.has(p)&&b.has(-p),"pivot");
 let c=new Set([...a].filter(x=>x!==p).concat([...b].filter(x=>x!==-p)));
 need(![...c].some(x=>c.has(-x)),"tautological resolvent");return c;
}
function models(C,n){
 let total=0;for(let a=0;a<2**n;a++){
  if(C.every(c=>[...c].some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0))))total++;
 }return total;
}
function replay(T){
 let n=T.n;need(Number.isInteger(n)&&n>=1&&n<=10,"n");
 need(T.source.length===T.m,"source count");let C=T.source.map(c=>literals(c,n));
 need(models(C,n)===0,"SAT source");
 let lines=[],paid=0;
 for(let i=0;i<T.strict.length;i++){
  let z=T.strict[i],actual=literals(z.C,n);
  if(z.op==="src"){need(Number.isInteger(z.source)&&z.source>=0&&z.source<C.length,"source reference");
   need(equal(actual,C[z.source]),"forged source");}
  else{need(z.op==="res"&&z.P.length===2&&z.P.every(j=>Number.isInteger(j)&&j>=0&&j<i),"bad proof ancestry");
   need(equal(actual,resolve(lines[z.P[0]],lines[z.P[1]],z.pivot)),"bad resolvent");paid++;}
  lines.push(actual);
 }
 need(lines.length>0&&lines[lines.length-1].size===0,"not contradiction");
 need(paid===T.strict_resolution_nodes&&paid<=T.scope_cost_bound,"cost mismatch");
 let deleted=0,flipped=0;
 for(let j=0;j<C.length;j++){
  need(models(C.filter((_,i)=>i!==j),n)>0,"deleted formula UNSAT");deleted++;
  for(let x of C[j]){let D=C.map((c,i)=>i!==j?c:new Set([...c].map(v=>v===x?-v:v)));
   need(models(D,n)>0,"flip did not restore SAT");flipped++;}
 }
 return {name:T.name,source:C.length,strict_lines:lines.length,paid,deleted,flipped};
}
function verify(DATA){
 need(DATA&&Array.isArray(DATA.full)&&DATA.full.length===4,"missing fixtures");
 let records=DATA.full.map(replay),xor=DATA.full.find(z=>z.name==="opposite_XOR3");
 need(models(xor.source.slice(0,4).map(c=>literals(c,3)),3)===4,"even parity SAT");
 need(models(xor.source.slice(4).map(c=>literals(c,3)),3)===4,"odd parity SAT");
 let k4=DATA.full.find(z=>z.name==="odd_K4");
 let vars=[...new Set(k4.source[0].map(Math.abs))].sort((a,b)=>a-b);
 need(vars.length===3,"K4 first vertex");
 let oppositeClauses=[];
 for(let a=0;a<8;a++)if(((a&1)^((a>>1)&1)^((a>>2)&1))===1)
  oppositeClauses.push(vars.map((x,i)=>((a>>i)&1)?-x:x));
 let evenCNF=oppositeClauses.concat(k4.source.slice(4)).map(c=>literals(c,6));
 need(models(evenCNF,6)===8,"even K4 SAT");
 let mutations=[
  D=>{D.full[0].strict[D.full[0].strict.length-1].C=[1];},
  D=>{D.full[0].strict[D.full[0].strict.length-1].pivot=999;},
  D=>{D.full[1].strict[0].C=[99];},
  D=>{D.full[1].strict[1].source=99;},
  D=>{let a=D.full[2].strict; a[a.length-1].P=[a.length-1,a.length-1];},
  D=>{D.full[3].source[0].push(D.full[3].source[0][0]);},
  D=>{D.full[0].source[0]=[0];},
  D=>{D.full[0].n=-1;}
 ];
 let rejected=0;
 for(let f of mutations){let D=JSON.parse(JSON.stringify(DATA));try{f(D);D.full.forEach(replay);}catch(e){rejected++;}}
 need(rejected===mutations.length,"failed negative controls "+rejected+"/"+mutations.length);
 return {status:"PASS",records,total_sources:records.reduce((s,v)=>s+v.source,0),
  total_paid:records.reduce((s,v)=>s+v.paid,0),total_deletions:records.reduce((s,v)=>s+v.deleted,0),
  total_sign_flips:records.reduce((s,v)=>s+v.flipped,0),XOR3_each_parity_models:4,
  even_K4_models:8,mutations_rejected:rejected,
  scope:"independent strict Resolution and source-controls, not native mixed-rule verifier"};
}
if(require.main===module){
 let path=process.argv[2];if(!path)throw Error("Usage: node lspv2_367_independent_verify.js DATA.json");
 console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(path,"utf8"))),null,2));
}
module.exports={verify};

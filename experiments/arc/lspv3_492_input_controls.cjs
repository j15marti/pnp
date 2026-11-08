"use strict";
/* LSPV-3/492 original one-hot external DIMACS malformed controls.
   Depends on published 490 parser and 492 proof producer. */
const {build,check}=require("./lspv3_492_onehot_declared_mixed_shortcut.cjs");
const {parse,multiset}=require("./lspv3_490_external_source_bind.cjs");
function need(b,m){if(!b)throw Error(m)}
function source(P){return "p cnf "+(2*P.edges.length)+" "+P.src.length+"\n"+
 P.src.map(x=>x.c.join(" ")+" 0").join("\n")+"\n"}
function bound(P,dimacs){
 const r=parse(dimacs);
 need(r.nv===2*P.edges.length,"external variable count");
 need(multiset(r.cls)===multiset(P.src.map(x=>x.c)),"original signed source multiset");
 return r;
}
function run(){
 let graphs=[["K4",[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],4],
 ["K3,3",Array.from({length:9},(_,i)=>[Math.floor(i/3),3+i%3]),6]];
 let results=[],rejected=0;
 for(let [name,edges,h] of graphs){
  const P=build(name,edges,[1,...Array(h-1).fill(0)]);check(P);
  const original=source(P),r=bound(P,original);
  let malformed=[
   original.replace("p cnf","p bad"),
   original.trimEnd().slice(0,-1),
   original.replace(/p cnf (\d+) (\d+)/,(_,a,b)=>"p cnf "+a+" "+(+b+1)),
   original.replace(/p cnf (\d+) (\d+)/,(_,a,b)=>"p cnf "+(+a-1)+" "+b),
   original.replace(/(^|\s)(-?\d+)(?=\s0)/m,"$1xx"),
   original.replace(/\b0\s*$/,"999 0"),
   original+"\n0\n",
   original.replace(/(^|\s)(-?\d+)(?=\s0)/m,(_,sp,x)=>sp+(-Number(x)))
  ];
  let n=0;
  for(let altered of malformed){let fails=false;try{bound(P,altered)}catch(e){fails=true}
   need(fails,"malformed/mismatched source accepted");rejected++;n++}
  results.push({name,originalExternalBytes:original.length,clauses:r.cls.length,negativesRejected:n});
 }
 return {status:"PASS",results,rejected,scope:"strict external source binder, not historical full mixed grammar"};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={source,bound,run};
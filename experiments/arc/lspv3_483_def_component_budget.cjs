"use strict";
// LSPV-3/483: charged binary-DEF incidence identity, not a native R_mix341 checker.
function run(){
 let count=0,seed=48320261107>>>0;
 const check=(v,msg)=>{count++;if(!v)throw Error("ASSERT: "+msg)};
 const rnd=n=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n};
 function inspect(g){
  const p=new Map(),seen=new Set(),sources=new Set(),edges=new Set();
  function find(x){if(!p.has(x))p.set(x,x);let a=x;while(p.get(a)!==a)a=p.get(a);while(p.get(x)!==x){let y=p.get(x);p.set(x,a);x=y;}return a;}
  for(const [z,op,a,b] of g){
   check(/^z[0-9]+$/.test(z)&&!seen.has(z),"fresh gate output");
   check(["AND","OR","XOR"].includes(op),"gate kind");
   for(const x of [a,b]){
    check(/^[xz][0-9]+$/.test(x),"typed input");
    if(x[0]==="z")check(seen.has(x),"prior output");
    else sources.add(x);
    const edge=[z,x].sort().join(":");
    edges.add(edge);p.set(find(z),find(x));
   }seen.add(z);
  }
  const d=g.length,s=sources.size,c=new Set([...p.keys()].map(find)).size;
  const e=edges.size,delta=2*d-e,r=e-(d+s)+c;
  check(r>=0&&delta>=0&&s===d+c-r-delta,"exact graphic rank");
  return {d,s,c,r,delta};
 }
 function tight(d,c){
  let sizes=Array(c).fill(1),z=0,x=0,g=[];
  for(let i=0;i<d-c;i++)sizes[i%c]++;
  for(const t of sizes){
   let out="z"+(++z);g.push([out,"AND","x"+(++x),"x"+(++x)]);
   for(let j=1;j<t;j++){let prev=out;out="z"+(++z);g.push([out,"OR",prev,"x"+(++x)]);}
  }return g;
 }
 const o={status:"COMPUTATIONAL: independent declared-gate incidence tests",tight:0,random:0,cycles_observed:0,operand_duplicate_cases:0,invalid_rejected:0,k4_branch_checks:0,odd_models:0,even_models:0,assertions:0};
 for(let d=1;d<=12;d++)for(let c=1;c<=d;c++){
  const t=inspect(tight(d,c));check(t.s===d+c&&t.r===0&&t.delta===0&&t.c===c,"tight forest");o.tight++;
 }
 for(let d=1;d<=14;d++)for(let j=0;j<170;j++){
  let g=[],xs=Array.from({length:d+3},(_,i)=>"x"+(i+1));
  for(let k=0;k<d;k++){let opts=xs.concat(g.map(v=>v[0])),a=opts[rnd(opts.length)],b=opts[rnd(opts.length)];
   g.push(["z"+(k+1),["AND","OR","XOR"][rnd(3)],a,b]);}
  let v=inspect(g);if(v.r)o.cycles_observed++;if(v.delta)o.operand_duplicate_cases++;o.random++;
 }
 const neg=[
  [["z1","AND","z2","x1"]],
  [["z1","AND","x1","x2"],["z1","OR","x2","x3"]],
  [["z1","XOR","oops","x1"]],
  [["z1","UNPAID","x1","x2"]]
 ];
 for(const g of neg){let rejected=false;try{inspect(g);}catch(e){rejected=true;}check(rejected,"reject malformed DAG");o.invalid_rejected++;}
 const edges=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)edges.push([i,j]);
 const encode=charge=>{
  let clauses=[];for(let v=0;v<4;v++){let ix=edges.map((e,k)=>e.includes(v)?k:-1).filter(x=>x>=0);
   for(let mask=0;mask<8;mask++){let b=[0,1,2].map(i=>(mask>>i)&1);
    if((b[0]^b[1]^b[2])!==charge[v])clauses.push(ix.map((k,i)=>(b[i]?-1:1)*(k+1)));}}
  return clauses;
 };
 const satisfied=(clauses,bits)=>clauses.every(c=>c.some(l=>{let b=(bits>>(Math.abs(l)-1))&1;return l>0?b===1:b===0;}));
 const gates=[["z1","AND","x1","x2"],["z2","XOR","z1","x3"],["z3","OR","z2","z1"],["z4","AND","x6","z3"]];
 let diag=inspect(gates);check(diag.s===4&&diag.c===1&&diag.r===1,"reconvergent K4 auxiliary graph");
 const evalg=(g,a)=>g[1]==="AND"?(a[g[2]]&a[g[3]]):g[1]==="OR"?(a[g[2]]|a[g[3]]):(a[g[2]]^a[g[3]]);
 for(const [tag,charge] of [["odd",[1,0,0,0]],["even",[0,0,0,0]]]){
  let cs=encode(charge),models=0;check(cs.length===16,"proper 3CNF source");
  for(let bits=0;bits<64;bits++){
   if(satisfied(cs,bits))models++;
   let a={};for(let j=0;j<6;j++)a["x"+(j+1)]=(bits>>j)&1;
   for(const g of gates)a[g[0]]=evalg(g,a);
   for(let other=0;other<64;other++){
    let b={};for(let j=0;j<6;j++)b["x"+(j+1)]=(other>>j)&1;
    if(["x1","x2","x3","x6"].some(x=>a[x]!==b[x]))continue;
    for(const g of gates)b[g[0]]=evalg(g,b);
    check(gates.every(g=>a[g[0]]===b[g[0]]),"all gates constant after branch pin");o.k4_branch_checks++;
   }
  }o[tag+"_models"]=models;
 }
 check(o.odd_models===0&&o.even_models===8,"K4 both-label models");
 o.assertions=count;return o;
}
if(typeof module!=="undefined")module.exports={run};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));

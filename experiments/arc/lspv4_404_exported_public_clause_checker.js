// LSPV-4/404: complete explicit paid-output LOCAL fragment, two independent semantic checks
"use strict";
function run() {
let seed=4042026; const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed};
const ops=["AND","OR","XOR","XNOR","NAND","NOR","IMP"];
const fn=(op,a,b)=>({AND:a&&b,OR:a||b,XOR:a!==b,XNOR:a===b,NAND:!(a&&b),NOR:!(a||b),IMP:(!a)||b})[op]?1:0;
const lit=(l,v)=>l>0?v:1-v;
function wellformed(gs,C,F) {
 if(!Array.isArray(gs)||!Array.isArray(C)||!Array.isArray(F)||F.length!==2)return false;
 let pool=new Set([1,2,3]),all=new Set([1,2,3,4]);
 for(let i=0;i<gs.length;i++){let g=gs[i];if(!g||g.id!==5+i||!ops.includes(g.op)||!Number.isInteger(g.a)||!Number.isInteger(g.b)||!pool.has(Math.abs(g.a))||!pool.has(Math.abs(g.b)))return false;pool.add(g.id);all.add(g.id)}
 return C.every(l=>Number.isInteger(l)&&l!==0&&all.has(Math.abs(l)))&&F.every(cl=>Array.isArray(cl)&&cl.length>0&&cl.every(l=>Number.isInteger(l)&&l!==0&&Math.abs(l)<=3));
}
function brute(F,gs,C) {
 let calls=0,models=0;
 for(let a=0;a<16;a++){let v={};for(let k=1;k<=4;k++)v[k]=(a>>(k-1))&1;
  for(const g of gs){v[g.id]=fn(g.op,lit(g.a,v[Math.abs(g.a)]),lit(g.b,v[Math.abs(g.b)]));calls++}
  if(F.every(cl=>cl.some(l=>lit(l,v[Math.abs(l)])))){models++;if(!C.some(l=>lit(l,v[Math.abs(l)])))return {ok:false,witness:a,calls,models}}
 }
 return {ok:true,calls,models};
}
function project(F,gs,C){
 const V={};let opsCount=0;
 for(let j=1;j<=3;j++){let m=0;for(let a=0;a<8;a++)if((a>>(j-1))&1)m|=1<<a;V[j]=m}
 const row=l=>l>0?V[l]:255^V[-l];
 for(const g of gs){let a=row(g.a),b=row(g.b);V[g.id]=({AND:a&b,OR:a|b,XOR:a^b,XNOR:255^(a^b),NAND:255^(a&b),NOR:255^(a|b),IMP:((255^a)|b)})[g.op];opsCount+=8}
 const cm=cl=>cl.reduce((m,l)=>m|row(l),0);
 if(C.includes(4)&&C.includes(-4))return {ok:true,opsCount};
 let keep=C.filter(l=>Math.abs(l)!==4);
 return {ok:(cm(F[0])&cm(F[1])&(255^cm(keep)))===0,opsCount};
}
let samples=0,accepted=0,rejected=0,bc=0,pc=0;let labels={SAT:0,UNSAT:0};
const clauses=[[1],[-1],[2],[-2],[3],[-3],[1,2],[1,-2],[-1,2],[-1,-2],[2,3],[-2,3]];
for(let k=1;k<=7;k++)for(let n=0;n<110;n++){
 const F=[clauses[rnd()%clauses.length],clauses[rnd()%clauses.length]],gs=[];
 for(let i=0;i<k;i++){let pool=[1,2,3,...gs.map(g=>g.id)],choose=()=>{let x=pool[rnd()%pool.length];return rnd()%2?-x:x};gs.push({id:5+i,op:ops[rnd()%ops.length],a:choose(),b:choose()})}
 if(!wellformed(gs,[1],F))throw Error("invalid source generator");
 let sat=false;for(let a=0;a<8;a++)if(F.every(cl=>cl.some(l=>l>0?((a>>(l-1))&1):!((a>>(-l-1))&1))))sat=true;
 labels[sat?"SAT":"UNSAT"]++;
 for(let t=0;t<35;t++){
  let C=[];for(let p=0,z=1+(rnd()%5);p<z;p++){let v=1+(rnd()%(k+4));C.push(rnd()%2?v:-v)}
  let b=brute(F,gs,C),c=project(F,gs,C);
  if(b.ok!==c.ok)throw Error("disagreement "+JSON.stringify({F,gs,C,b,c}));
  samples++;accepted+=b.ok?1:0;rejected+=b.ok?0:1;bc+=b.calls;pc+=c.opsCount;
 }
}
const positive={F:[[1],[1,2]],gs:[{id:5,op:"XOR",a:1,b:2}],C:[5,2]};
const negative={F:[[1],[1,2]],gs:[{id:5,op:"AND",a:1,b:2}],C:[5,2]};
if(!brute(positive.F,positive.gs,positive.C).ok||!project(positive.F,positive.gs,positive.C).ok)throw Error("positive");
if(brute(negative.F,negative.gs,negative.C).ok||project(negative.F,negative.gs,negative.C).ok)throw Error("negative");
if(!project([[1],[-1]],negative.gs,[5,2]).ok||!brute([[1],[-1]],negative.gs,[5,2]).ok)throw Error("UNSAT control");
if(!project(positive.F,positive.gs,[4,-4]).ok||!brute(positive.F,positive.gs,[4,-4]).ok)throw Error("tautology control");
const bad=[[{id:5,op:"XOR",a:1,b:5}],[{id:5,op:"XOR",a:1,b:6}],[{id:5,op:"XOR",a:1,b:2},{id:5,op:"AND",a:5,b:3}],[{id:5,op:"INVALID",a:1,b:2}],[{id:5,op:"XOR",a:0,b:2}],[{id:5,op:"AND",a:1,b:4}]];
if(!bad.every(gs=>!wellformed(gs,[5],positive.F)))throw Error("malformed DEF accepted");
if(wellformed(positive.gs,[999],positive.F)||wellformed(positive.gs,[0],positive.F))throw Error("malformed conclusion");
return {status:"PASS",seed:4042026,network_cases:770,source_labels:labels,clauses_checked:samples,valid:accepted,invalid:rejected,brute_gate_evals:bc,projected_bit_gate_evals:pc,malformed_rejections:8,positive_export:true,negative_gate_mutation:true,UNSAT_parent:true,tautological_outside_pair:true};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));

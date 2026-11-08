"use strict";
function insist(ok,msg){if(!ok)throw Error(msg)}
function negatedWrong(bits,incident){return incident.map((e,i)=>-(2*e+bits[i]+1))}
function resolve(a,b,p){
  insist((a.includes(-p)&&b.includes(p))||(a.includes(p)&&b.includes(-p)),"pivot polarity");
  const c=[...new Set([...a,...b].filter(x=>Math.abs(x)!==p))];
  insist(!c.some(x=>c.includes(-x)),"tautology");
  return c.sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y)
}
function build(h,edges,charge){
  insist(charge.length===h&&charge.reduce((a,b)=>a+b,0)%2===1,"odd total charge required");
  const T=[],B=[],steps=[];let checked=0;
  for(let e=0;e<edges.length;e++) T.push([2*e+1,2*e+2],[-(2*e+1),-(2*e+2)]);
  for(let v=0;v<h;v++){
    const inc=edges.map(([a,b],e)=>(a===v||b===v)?e:-1).filter(x=>x>=0);
    insist(inc.length===3,"not cubic");
    for(let b=0;b<8;b++){
      const bits=[(b>>2)&1,(b>>1)&1,b&1];
      if(bits.reduce((a,c)=>a+c,0)%2===charge[v])continue;
      let clause=negatedWrong(bits,inc);
      T.push(clause);let p=T.length-1;
      for(let j=0;j<3;j++)if(bits[j]===0){
        const ax=2*inc[j],pivot=2*inc[j]+1;
        const out=resolve(clause,T[ax],pivot);
        steps.push({vertex:v,source:p,edge:inc[j],pivot,other:ax,before:clause,after:out});
        clause=out;p=T.length+steps.length-1;checked++;
      }
      const expected=inc.map((e,j)=>bits[j]===0?2*e+2:-(2*e+2));
      insist(clause.length===3&&expected.every(x=>clause.includes(x)),"incorrect local translation");
      B.push(expected);checked++;
    }
  }
  insist(T.length===7*h && B.length===4*h && steps.length===6*h,"size identities");
  return {T,B,steps,checked};
}
function countModel(clauses,m){
  let s=0;
  for(let y=0;y<2**m;y++){
    const bit=(x)=>{const e=Math.floor((Math.abs(x)-1)/2);const isOne=(!(Math.abs(x)%2));const z=(y>>e)&1;const val=isOne?z:1-z;return x>0?val:1-val};
    if(clauses.every(c=>c.some(l=>bit(l)===1)))s++;
  }
  return s;
}
function run(){
  const cases=[{name:"K4",h:4,edges:[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]},
  {name:"K3,3",h:6,edges:Array.from({length:9},(_,i)=>[Math.floor(i/3),3+i%3])}];
  let assertions=0;const results=[];
  for(const {name,h,edges} of cases){
    const odd=[1,...Array(h-1).fill(0)], even=Array(h).fill(0);
    const {T,B,steps,checked}=build(h,edges,odd);assertions+=checked;
    insist(countModel(T,edges.length)===0&&countModel(B,edges.length)===0,"wrong UNSAT");assertions+=2;
    const modify=T.map(x=>x.slice());modify.pop();insist(countModel(modify,edges.length)>0,"bad deletion");assertions++;
    const corrupted=steps[0];let fails=false;
    try{resolve(corrupted.before,T[corrupted.other],-999)}catch(_){fails=true}
    insist(fails,"corruption undetected");assertions++;
    fails=false;try{build(h,edges,even)}catch(_){fails=true}
    insist(fails,"even-charge input should be rejected by odd constructor");assertions++;
    const eT=[],eB=[];
    for(let e=0;e<edges.length;e++) eT.push([2*e+1,2*e+2],[-(2*e+1),-(2*e+2)]);
    for(let v=0;v<h;v++){
      const inc=edges.map(([a,b],e)=>(a===v||b===v)?e:-1).filter(x=>x>=0);
      for(let b=0;b<8;b++){const bits=[b>>2&1,b>>1&1,b&1];if(bits[0]^bits[1]^bits[2])continue;
      eT.push(negatedWrong(bits,inc));eB.push(inc.map((e,j)=>bits[j]===0?2*e+2:-(2*e+2)))}
    }
    const expected=2**(edges.length-h+1);
    insist(countModel(eT,edges.length)===expected&&countModel(eB,edges.length)===expected,"wrong SAT model count");assertions+=2;
    results.push({family:name,vertices:h,edge_variables:edges.length,bit_3cnf_clauses:B.length,onehot_variables:2*edges.length,onehot_cnf_clauses:T.length,derived_bit_clauses:B.length,ordinary_res_steps:steps.length,ResPC_nodes_added_upper:2*steps.length,odd_models:0,even_models:expected});
  }
  return {status:"FINITE_CONTROLS_PASS",assertions,results,qualification:"Exact finite source-clause derivations. Res(PC_r/F3) primitive simulation: each Boolean RES step is linear-combination-to-false-constant plus deletion. Not historical R_mix341 checker."};
}
const result=run();
if(typeof console!=="undefined" && typeof process!=="undefined")console.log(JSON.stringify(result,null,2));
result;
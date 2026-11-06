#!/usr/bin/env node
// LSPV-4/448: standalone hostile bridge witness. Pure Node, no dependencies.
"use strict";
function check(c,m){if(!c)throw Error(m);}
let es=[];
for(const [off,z] of [[0,8],[4,9]]){
  for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)
    if(!(i===0&&j===1))es.push([off+i,off+j]);
  es.push([off,z],[off+1,z]);
}
es.push([8,9]);es=es.map(e=>e.sort((a,b)=>a-b)).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
check(es.length===15,"cubic edges");
for(let v=0;v<10;v++)check(es.filter(e=>e.includes(v)).length===3,"cubic degree");
const bridge=es.findIndex(e=>e[0]===8&&e[1]===9);
check(bridge>=0,"missing bridge");
function source(charges){
  let incidence=Array.from({length:10},()=>[]);
  es.forEach(([a,b],i)=>{incidence[a].push(i);incidence[b].push(i);});
  let clauses=[];
  for(let v=0;v<10;v++){
    const inds=incidence[v];
    for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++){
      if((a^b^c)===charges[v])continue;
      clauses.push(inds.map((id,j)=>[a,b,c][j]===0?id+1:-id-1));
    }
  }
  return clauses;
}
function up(clauses,alpha){
  let val=new Map([[bridge,alpha]]);
  while(true){
    const units=[];
    for(const clause of clauses){
      let satisfied=false,unknown=[];
      for(let l of clause){
        let v=val.get(Math.abs(l)-1);
        if(v===undefined)unknown.push(l);
        else if(v===(l>0?1:0)){satisfied=true;break;}
      }
      if(satisfied)continue;
      if(!unknown.length)return false;
      if(unknown.length===1)units.push(unknown[0]);
    }
    if(!units.length)return true;
    let changed=false;
    for(const lit of units){
      let id=Math.abs(lit)-1,bit=lit>0?1:0;
      if(val.has(id)){if(val.get(id)!==bit)return false;}
      else{val.set(id,bit);changed=true;}
    }
    if(!changed)return true;
  }
}
function bruteSAT(clauses,alpha){
  for(let bits=0;bits<1<<15;bits++){
    if(((bits>>bridge)&1)!==alpha)continue;
    if(clauses.every(c=>c.some(l=>((bits>>(Math.abs(l)-1))&1)===(l>0?1:0))))
      return true;
  }
  return false;
}
let results=[];
for(const odd of [false,true]){
  const charges=Array(10).fill(0);if(odd)charges[0]=1;
  const cnf=source(charges);
  check(cnf.length===40,"source clauses");
  for(const alpha of [0,1]){
    let opened=up(cnf,alpha),satisfiable=bruteSAT(cnf,alpha);
    check(opened,"both bridge branches must remain UP open");
    check(satisfiable===(!odd && alpha===0),"parity consistency");
    results.push({odd,bridge_assignment:alpha,UPopen:opened,SAT:satisfiable});
  }
}
console.log(JSON.stringify({status:"PASS",model:"original 3-CNF bridge graph",results},null,2));

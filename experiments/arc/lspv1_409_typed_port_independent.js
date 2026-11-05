#!/usr/bin/env node
// LSPV1/409: independent compact record and source-semantic checker, Node >=18.
// Source is every subset of eight proper signed two-variable clauses.
// Splus exports two paid fresh XOR-gate DEF rows. Sminus keeps them private.
const cs=[[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]], count={SAT:0,UNSAT:0};
let checks=0,models=0;
function sat(mask,x,y){return cs.every((cl,i)=>!(mask&(1<<i))||cl.some(l=>(l>0?[x,y][Math.abs(l)-1]:1-[x,y][Math.abs(l)-1])===1))}
function row(variables,rhs,z){let v=rhs;for(const id of variables)v^=z[id];return v===0}
for(let mask=0;mask<256;mask++){let k=0;
 for(let x=0;x<2;x++)for(let y=0;y<2;y++)if(sat(mask,x,y)){
  k++;models++;const a=x^y,b=x^y,z={1:x,2:y,3:a,4:b};
  if(!row([1,2,3],0,z)||!row([1,2,4],0,z)||!row([3,4],0,z))throw Error("unsound Splus");
  checks+=3;
 }
 count[k?"SAT":"UNSAT"]++;checks+=2;
}
if(count.SAT!==95||count.UNSAT!==161)throw Error("wrong labels");
for(let x=0;x<2;x++)for(let y=0;y<2;y++){
 let z={3:x^y,4:1^(x^y)};
 if(row([3,4],0,z)||!row([3,4],1,z))throw Error("forged XNOR conclusion");
 checks+=2;
}
const proof=[{id:1,op:"DEF",out:3,gate:"XOR",inputs:[1,2]},
 {id:2,op:"DEF",out:4,gate:"XOR",inputs:[1,2]},
 {id:3,op:"XOR",parents:[1,2],mask:[3,4],rhs:0}];
console.log(JSON.stringify({cases:256,labels:count,source_models_extended:models,checks,
 proof, Splus:"accepts",Sminus:"rejects node 3 private GF2 antecedents",
 note:"hypothetical grammar comparison, full native Rmix341 and B3 OPEN"}));

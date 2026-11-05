#!/usr/bin/env node
// LSPV4/423 compact independent cube-cut parity verifier (no dependencies).
// Full Python producer and independent exhaustive Node verifier are in the run ZIP.
let E=[];for(let v=0;v<8;v++)for(let k=0;k<3;k++){let w=v^(1<<k);if(v<w)E.push([v,w]);}
E.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
const S=E.map(([u,v],i)=>((u&1)!=(v&1))?i:-1).filter(x=>x>=0);
if(S.length!==4)throw Error("cut width");
function residual(charge,bits){let adjacency=Array.from({length:8},()=>[]),rhs=Array(8).fill(0);if(charge)rhs[0]=1;
E.forEach(([u,v],i)=>{let j=S.indexOf(i);if(j<0){adjacency[u].push(v);adjacency[v].push(u);}else{rhs[u]^=bits[j];rhs[v]^=bits[j];}});
let seen=new Set(),componentParities=[];for(let v=0;v<8;v++)if(!seen.has(v)){let todo=[v],p=0;seen.add(v);while(todo.length){let a=todo.pop();p^=rhs[a];for(let b of adjacency[a])if(!seen.has(b)){seen.add(b);todo.push(b)}}componentParities.push(p)}
return {sat:componentParities.every(x=>x===0),componentParities};
}
let evenSat=0,oddSat=0,checks=0;
for(let z=0;z<16;z++){let bits=[0,1,2,3].map(k=>(z>>k)&1),a=residual(0,bits),b=residual(1,bits);if(a.sat)evenSat++;if(b.sat)oddSat++;if(a.componentParities.length!==2||b.componentParities.length!==2)throw Error('components');checks+=2;}
if(evenSat!==8||oddSat!==0)throw Error('bad branch joins');
console.log(JSON.stringify({result:'PASS',evenSat,oddSat,checks}));

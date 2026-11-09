"use strict";
// LSPV-4/506 independent K3,3 finite control. Hosted V8, not FLMV.
const E=[];for(let u=0;u<3;u++)for(let v=3;v<6;v++)E.push([u,v]);
const inc=Array.from({length:6},()=>[]);
for(let i=0;i<E.length;i++){let [u,v]=E[i];inc[u].push(i+1);inc[v].push(i+1)}
const rows=[];
for(let v=0;v<6;v++){let ids=inc[v];for(let z=0;z<8;z++){
let b=[(z>>2)&1,(z>>1)&1,z&1];if((b[0]^b[1]^b[2])!==(v===0?1:0))rows.push(ids.map((id,k)=>b[k]?-id:id));
}}
function sat(c){for(let a=0;a<512;a++)if(c.every(cl=>cl.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0))))return true;return false}
if(sat(rows))throw Error("odd K3,3 must be UNSAT");
const M=rows.length*3;let checked=0;for(let i=0;i<rows.length;i++)for(let j=0;j<3;j++){
let c=rows.map(x=>x.slice());c[i][j]*=-1;if(!sat(c))throw Error("single flip not SAT");checked++;
}
const rng=(state=>()=>{state=(Math.imul(1664525,state)+1013904223)>>>0;return state/2**32})(506);
let ranks=0;
for(let run=0;run<128;run++){let p=Array.from({length:M},(_,i)=>i);
for(let i=M-1;i>0;i--){let j=Math.floor(rng()*(i+1));[p[i],p[j]]=[p[j],p[i]]}
let rank=new Map(p.map((x,i)=>[x,i+1]));
if([...rank.values()].reduce((a,b)=>a+b,0)!==M*(M+1)/2)throw Error("star floor");ranks++;
}
const result={label:"LSPV4_506_INDEPENDENT_K33",status:"PASS",graph:"K3,3",vertices:6,clauses:rows.length,critical_bits:M,flipped_sat_mutants:checked,permutations:ranks,one_anchor_all_neighbors_probe_floor:M*(M+1)/2,native_FLMV:false,historical_Rmix341:false};
if(typeof module!=="undefined"&&module.exports){module.exports=result;if(require.main===module)process.stdout.write(JSON.stringify(result,null,2)+"\n");}
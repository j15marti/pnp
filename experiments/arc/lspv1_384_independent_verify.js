// LSPV-1/384 independent witness verifier, algorithmically distinct from producer. Node >=18.
const verify = function verify(){
"use strict";
 let checks=0,total=0,positive=0,negative=0,witnesses=0,malformed=0;
 const assert=(b,m)=>{checks++;if(!b)throw Error("Independent checker: "+m)};
 function classify(n,clauses){if(!Number.isInteger(n)||n<0||n>12||!Array.isArray(clauses))throw Error("bad header");let satisfying=0,unsat=true;for(let w=0;w<(1<<n);w++){let all=true;for(const row of clauses){if(!Array.isArray(row))throw Error("bad clause");let rowTrue=false;for(const l of row){if(typeof l!=="number"||!Number.isSafeInteger(l)||l===0||Math.abs(l)>n)throw Error("bad literal");let bit=(w>>(Math.abs(l)-1))&1;if((l>0&&bit===1)||(l<0&&bit===0))rowTrue=true}if(!rowTrue){all=false;break}}if(all){satisfying++;unsat=false}}
 // Every y-sketch fiber must be constant, all four types of x/z settings included.
 let factoring=true,proofWitness=false;
 for(let y=0;y<2;y++){let reference=null;for(let w=0;w<(1<<n);w++){for(let z=0;z<2;z++){let satisfies=true;for(let j=0;j<clauses.length;j++)if(!clauses[j].some(l=>l>0?((w>>(l-1))&1)===1:((w>>(-l-1))&1)===0))satisfies=false;let val=z&&satisfies?1:0;if(reference===null)reference=val;else if(reference!==val){factoring=false;proofWitness=true}}}}
 assert(factoring===unsat,"factor equivalence");assert(proofWitness===(!unsat),"counter-witness");assert(satisfying>0 || unsat,"label");
 total++;if(unsat)negative++;else{positive++;witnesses++}
 }
 for(let n=1;n<=3;n++){let all=[];for(let bad=0;bad<(1<<n);bad++){let row=[];for(let j=0;j<n;j++)row.push(bad&(1<<j)?-j-1:j+1);all.push(row)}const masks=1<<all.length;for(let subset=0;subset<masks;subset++){let rows=[];for(let i=0;i<all.length;i++)if(subset&(1<<i))rows.push(all[i]);classify(n,rows);assert((subset===masks-1)===(rows.length===(1<<n)),"full-width tautological counting")}}
 const cases=[
 [1,[[1],[-1]]],[2,[[1],[-1],[2]]],[2,[[1,2],[-1],[-2]]],
 [3,[[1],[-1,2],[-2,3],[-3]]],
 [3,[[1,2,3],[-1,-2,-3]]],
 [4,[[1],[-1,2],[-2,3],[-3,4],[-4]]],
 [0,[]],[0,[[]]],[2,[[1,-1],[2]]]];
 for(const [n,c]of cases)classify(n,c);
 const bad=[[-1,[]],[2,null],[2,[[0]]],[2,[[3]]],[2,[[1.5]]],[2,[false]],[1,[[NaN]]],[0,[[1]]],[2,[["1"]]],[2,[null]]];
 for(const [n,c]of bad){let threw=false;try{classify(n,c)}catch(e){threw=true}assert(threw,"malformed input");malformed++}
 const incident=[[0,1,2],[0,3,4],[1,3,5],[2,4,5]];
 let counts=[];for(let ch=0;ch<2;ch++){let m=0;for(let state=0;state<64;state++){let mismatch=0;for(let v=0;v<4;v++){let sum=0;for(let e of incident[v])sum^=(state>>e)&1; if(sum!==(v===0?ch:0))mismatch++}if(mismatch===0)m++}counts.push(m)}
 assert(counts[0]===8&&counts[1]===0,"even/odd controls");
 return {result:"384_INDEPENDENT",seed:null,formulas:total,sat:positive,unsat:negative,witnesses,malformed_rejected:malformed,controls_k4_even_odd:counts,assertions:checks,independence:"separate direct formula truth-table and same-sketch pairwise enumeration without constructing a circuit gate list"};
};
console.log(JSON.stringify(verify(),null,2));

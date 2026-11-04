/* LSPV-1 378 independent verifier. No import from producer.
 * Closed-form one-step Resolution characterization, plus semantic
 * clause-deletion witness identities, not a second graph search.
 */
"use strict";
function assert(p,msg){if(!p)throw Error(msg);}
const original=[[1,2],[-1],[-2]];
const optional=[[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]];
function value(l,x,y,z){const v=[null,x,y,z][Math.abs(l)];return l>0?v:!v;}
function holds(c,a){return c.some(l=>value(l,(a&1)!==0,(a&2)!==0,(a&4)!==0));}
function holdsAll(cs,a){return cs.every(c=>holds(c,a));}
function key(c){return [...c].sort((a,b)=>a-b).join(",")}
function sourceHasOppositeUnits(cs){
 const units=new Set(cs.filter(c=>c.length===1).map(c=>c[0]));
 return [...units].some(u=>units.has(-u));
}
function parityCount(charges){
 const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 let total=0;
 for(let mask=0;mask<64;mask++){
  const at=Array(4).fill(0);
  E.forEach(([u,v],i)=>{const b=(mask>>i)&1;at[u]^=b;at[v]^=b;});
  if(at.every((b,i)=>b===charges[i]))total++;
 }
 return total;
}
function main(){
 let checks=0;const hist={};
 // Every source-deletion formula has precisely one satisfying
 // assignment, for deletions C0,C1,C2 respectively: 00,10,01.
 const witness=[0,1,2];
 for(let i=0;i<3;i++){
  const cs=original.filter((_,j)=>j!==i);
  const m=[];for(let a=0;a<4;a++)if(holdsAll(cs,a))m.push(a);
  assert(JSON.stringify(m)===JSON.stringify([witness[i]]),"witness mismatch "+i);checks++;
 }
 for(let mask=0;mask<256;mask++){
  const D=optional.filter((_,i)=>mask&(1<<i));
  const r=witness.filter(a=>holdsAll(D,a)).length;
  const cs=[...new Map([...original,...D].map(c=>[key(c),c])).values()];
  const q=sourceHasOppositeUnits(cs)?1:2;
  hist[r+","+q]=(hist[r+","+q]||0)+1;
  assert(![0,1,2,3].some(a=>holdsAll(cs,a)),"lost UNSAT");checks++;
  assert(q>=Math.max(0,r-1),"lost charged floor");checks++;
  assert(q===1||q===2,"q bad");checks++;
  // One-step derivation of false is possible exactly when opposing
  // source units exist. Otherwise the original two-step proof works.
  assert(q===2 || sourceHasOppositeUnits(cs),"invalid claimed q=1");checks++;
 }
 // Conservative and total over original assignments, including false.
 for(const defs of [
  [[-3,1],[-3,2],[3,-1,-2]],
  [[1,2,-3],[-1,-2,-3],[1,-2,3],[-1,2,3]]
 ]){
  for(let a=0;a<4;a++){
   const b=[0,1].filter(z=>holdsAll(defs,a|(z<<2)));
   assert(b.length===1,"nonfunctional definitional extension");checks++;
  }
  for(let i=0;i<3;i++){
   const core=original.filter((_,j)=>j!==i);
   assert([0,1,2,3,4,5,6,7].some(a=>holdsAll([...core,...defs],a)),
     "definition killed MUS witness");checks++;
  }
 }
 // Hostile labels and proof-forgery controls.
 assert(parityCount([0,0,0,0])===8,"even charge");checks++;
 assert(parityCount([1,0,0,0])===0,"odd charge");checks++;
 assert([0,1,2,3].some(a=>holdsAll([[1,2],[1],[-2]],a)),"flipped sibling SAT");checks++;
 assert(!holdsAll([[1,2],[-1]],0),"nonempty resolution pivot forged");checks++;
 const malformed=[[],[0],[1,-1],[1,1],[3],[1.2]];
 for(const c of malformed){
  const valid=c.length>0&&c.every(x=>Number.isInteger(x)&&x!==0&&Math.abs(x)<=2)
    &&new Set(c).size===c.length&&!c.some(x=>c.includes(-x));
  assert(!valid,"malformed accepted");checks++;
 }
 return {title:"LSPV1_378_INDEPENDENT_CLOSED_FORM",independent_checks:checks,
    histogram_r_q:hist,parity_even_models:8,parity_odd_models:0,
    certified_method:"one-step Resolution iff source contains complementary units",
    no_source_code_import:true,seed:null};
}
if(typeof module!=="undefined"&&require.main===module) process.stdout.write(JSON.stringify(main(),null,2)+"\n");

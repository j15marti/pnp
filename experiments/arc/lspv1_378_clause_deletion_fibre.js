/* LSPV-1 / 378: deletion witness preservation and exact two-variable Resolution minima.
 * Deterministic, zero dependencies. No random seeds. Node.js: node <filename>.
 */
"use strict";
const BASE=[[1,2],[-1],[-2]];
const CHOICES=[[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]];
function ck(c){return [...c].sort((a,b)=>a-b).join(",")}
function sat(clauses,a){
  return clauses.every(c=>c.some(l=>Boolean(a[Math.abs(l)])===(l>0)));
}
function mod(clauses,k){
  const r=[];for(let x=0;x<(1<<k);x++){
    const a={};for(let v=1;v<=k;v++)a[v]=(x>>(v-1))&1;
    if(sat(clauses,a))r.push(x);
  }return r;
}
function res(a,b){
  const out=new Set();
  for(let p=1;p<=2;p++){
    if((a.includes(p)&&b.includes(-p))||(a.includes(-p)&&b.includes(p))){
      const c=[...new Set([...a,...b].filter(x=>Math.abs(x)!==p))];
      if(c.some(x=>c.includes(-x)))continue;
      out.add(ck(c));
    }
  }return [...out];
}
const ALL=[[],...CHOICES];
const IDS=Object.fromEntries(ALL.map((a,i)=>[ck(a),i]));
function minRes(clauses){
  let start=0;for(const c of clauses)start|=1<<IDS[ck(c)];
  const q=[[start,0]], seen=new Set([start]);
  for(let idx=0;idx<q.length;idx++){
    const [mask,d]=q[idx];if(mask&1)return d;
    const available=[];for(let i=1;i<ALL.length;i++)if(mask&(1<<i))available.push(i);
    for(let i=0;i<available.length;i++)for(let j=i+1;j<available.length;j++){
      for(const k of res(ALL[available[i]],ALL[available[j]])){
        const next=mask|(1<<IDS[k]);if(next===mask||seen.has(next))continue;
        seen.add(next);q.push([next,d+1]);
      }
    }
  }
  throw new Error("resolution closure failed");
}
function guards(clauses,vars){
 if(!Array.isArray(clauses))return false;
 return clauses.every(c=>Array.isArray(c)&&c.length>0&&c.every(l=>Number.isInteger(l)&&l!==0&&Math.abs(l)<=vars)&&new Set(c).size===c.length&&!c.some(l=>c.includes(-l)));
}
function assert(ok,reason){if(!ok)throw new Error(reason);}
function main(){
 let tests=0, hist={},totalD=0, full=0, partial=0, none=0, tight=0;
 const stats=[];
 assert(guards(BASE,2),"BASE malformed"); tests++;
 assert(mod(BASE,2).length===0,"base not UNSAT");tests++;
 for(let mask=0;mask<256;mask++){
   const D=CHOICES.filter((_,i)=>(mask>>i)&1);
   const union=[...new Map([...BASE,...D].map(c=>[ck(c),c])).values()];
   const r=BASE.reduce((s,c,i)=>s+(mod([...BASE.filter((_,j)=>i!==j),...D],2).length>0?1:0),0);
   const q=minRes(union);
   assert(q===1||q===2,"invalid q");tests++;
   assert(q>=Math.max(0,r-1),"arity lower bound failed");tests++;
   assert(mod(union,2).length===0,"lost UNSAT");tests++;
   hist[r+","+q]=(hist[r+","+q]||0)+1;
   if(r===3)full++;else if(r===0)none++;else partial++;
   if(q===Math.max(1,r-1))tight++;
   if(mask===0 || mask===1 || mask===2 || mask===4 || mask===128)stats.push({mask,r,q});
   totalD++;
 }
 const totalityExtras=[
   {type:"AND2_def",D:[[-3,1],[-3,2],[3,-1,-2]]},
   {type:"XOR_def",D:[[1,2,-3],[-1,-2,-3],[1,-2,3],[-1,2,3]]}
 ];
 for(const {type,D} of totalityExtras){
   assert(guards(D,3),type+" malformed");tests++;
   for(let a=0;a<4;a++){
     let witnessCount=0;for(let z=0;z<2;z++)if(sat(D,{1:a&1,2:(a>>1)&1,3:z}))witnessCount++;
     assert(witnessCount===1,type+" not functional");tests++;
   }
   for(let i=0;i<3;i++){
     assert(mod([...BASE.filter((_,j)=>i!==j),...D],3).length>=1,type+" killed source witness");tests++;
   }
 }
 const malformed=[[[0]],[[1,-1]],[[3]],[[1,1]],[[1.5]],"bad",null,[0],[[]]];
 for(const v of malformed){assert(!guards(v,2),"accepted malformed");tests++;}
 assert(mod([...BASE,[1]],2).length===0,"control D label");tests++;
 assert(mod([...BASE.filter((_,i)=>i!==0),[1]],2).length===0,"control forbidden witness");tests++;
 return {title:"LSPV1_378_CLAUSE_DELETION_FIBRE",status:"COMPUTATIONAL exact finite 2-variable Resolution search; mathematical theorem separately",seed:null,deterministic:true,candidate_D:8,subsets:totalD,assertions:tests,histogram_r_q:hist,source_witness_full:full,partial,none,tight_count:tight,selected_cases:stats,total_extension_controls:totalityExtras.map(o=>o.type),malformed_rejections:malformed.length};
}
if(typeof module!=="undefined" && require.main===module) process.stdout.write(JSON.stringify(main(),null,2)+"\n");

"use strict";
const run=()=>{
 let seed=2010320; const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>9)%n}; const assert=(x,m)=>{if(!x)throw Error(m)};
 function basis(xs){let B=[];for(let x of xs){for(const b of B)x=Math.min(x,x^b);if(x){B.push(x);B.sort((a,b)=>b-a)}}return B}
 const has=(B,x)=>{for(const b of B)x=Math.min(x,x^b);return x===0};
 const xor=(a,b)=>new Set([...a].flatMap(x=>[...b].map(y=>x^y)));
 const hull=S=>{if(!S.size)return null;let a=[...S][0];return {a,B:basis([...S].map(x=>x^a))}};
 let out={seed,dag:{graphs:0,empty:0,paths:0,rank_checks:0},closure:{systems:0,targets:0,sat:0,unsat:0,affine_unsat_detected:0,removed_points:0},stagnation:{formulas:0,unchanged_factors:0}};
 for(let k=0;k<240;k++){
   let n=4+rnd(7),A=Array.from({length:n},()=>[]);for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(rnd(100)<40)A[u].push([v,rnd(64)]);
   let P=Array(n).fill(null);P[0]=0;for(let u=0;u<n;u++)if(P[u]!==null)for(let [v,g]of A[u])if(P[v]===null)P[v]=P[u]^g;
   let Q=Array(n).fill(false);Q[n-1]=true;for(let u=n-2;u>=0;u--)Q[u]=A[u].some(([v])=>Q[v]);
   let S=new Set();function dfs(u,s){if(u===n-1){S.add(s);out.dag.paths++;return}for(let [v,g]of A[u])dfs(v,s^g)}dfs(0,0);
   out.dag.graphs++;if(!S.size){assert(P[n-1]===null,"empty");out.dag.empty++;continue}
   let D=[];for(let u=0;u<n;u++)if(P[u]!==null)for(let[v,g]of A[u])if(Q[v])D.push(P[u]^g^P[v]);
   let B=basis(D),H=hull(S);assert(B.length===H.B.length&&has(B,H.a^P[n-1])&&H.B.every(x=>has(B,x)),"path hull");out.dag.rank_checks++;
 }
 function closure(S,t){let F=S.map(x=>new Set(x)),removed=0;while(true){if(F.some(x=>!x.size))return {F,removed,empty:true};let changed=false;
   for(let i=0;i<F.length;i++){let a=0,V=[];for(let j=0;j<F.length;j++)if(j!==i){let h=hull(F[j]);if(!h)return {F,removed,empty:true};a^=h.a;V.push(...h.B)}let B=basis(V);
     for(let x of [...F[i]])if(!has(B,t^a^x)){F[i].delete(x);removed++;changed=true}
     if(!F[i].size)return {F,removed,empty:true};
   }if(!changed)return {F,removed,empty:false};}}
 for(let k=0;k<120;k++){
   let S=Array.from({length:2+rnd(4)},()=>new Set(Array.from({length:1+rnd(6)},()=>rnd(16))));
   let full=S.reduce(xor,new Set([0]));out.closure.systems++;
   for(let t=0;t<16;t++){let R=closure(S,t);out.closure.targets++;out.closure[full.has(t)?"sat":"unsat"]++;out.closure.removed_points+=R.removed;
     if(R.empty){assert(!full.has(t),"false UNSAT");out.closure.affine_unsat_detected++;continue}
     assert(R.F.reduce(xor,new Set([0])).has(t)===full.has(t),"closure decision");
     // every locally chosen point with an actual global extension must remain
     for(let i=0;i<S.length;i++){let O=S.filter((_,j)=>j!==i).reduce(xor,new Set([0]));for(let x of S[i])if(O.has(t^x))assert(R.F[i].has(x),"lost witness")}
   }
 }
 // Small 3-CNF factor instances, full occurrence coordinates; distinct variables per clause.
 for(let k=0;k<60;k++){let n=3+rnd(3),m=2+rnd(5),V=Array(n).fill(0),F=[];
   for(let j=0;j<m;j++){let vars=[];while(vars.length<3){let v=rnd(n);if(!vars.includes(v))vars.push(v)}let bad=rnd(8);for(let l=0;l<3;l++)V[vars[l]]^=1<<(3*j+l);
     F.push(new Set(Array.from({length:8},(_,x)=>x).filter(x=>x!==bad).map(x=>x<<(3*j))));
   }F.push(...V.filter(x=>x!==0).map(x=>new Set([0,x])));let R=closure(F,0);assert(!R.empty&&R.removed===0,"stagnation");out.stagnation.formulas++;out.stagnation.unchanged_factors+=F.length;
 }
 return out;
};
console.log(JSON.stringify(run(),null,2));

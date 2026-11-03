/* LSPV-2 DEF-SUPPORT-COVERAGE346: OUTPUT-support-strengthened independently rerunnable exact 5-node tree exclusion.
   node lspv2_342_compact.js; no third-party dependencies. */
'use strict';
const G=[[-3,1,4],[-1,2],[1,3],[-4,-3],[-2,-1,3],[-2,4]];
const H=[[-3,-1],[1,2,4],[-3,-2,4],[3,4],[-4,1],[-4,-1,3]];
const pop=x=>{let n=0;for(;x;x&=x-1)n++;return n};
function tt(C,n=4){let t=0;for(let x=0;x<(1<<n);x++)if(C.some(a=>((x>>(Math.abs(a)-1))&1)==(a>0?1:0)))t|=1<<x;return t}
function support(t,n=4){let r=0;for(let i=0;i<n;i++)for(let x=0;x<(1<<n);x++)if(((t>>x)&1)!=((t>>(x^(1<<i)))&1)){r|=1<<i;break}return r}
function affine(mask,rhs,n=4){let t=0;for(let x=0;x<(1<<n);x++)if((pop(x&mask)&1)==rhs)t|=1<<x;return t}
function models(C,n=4){let cnt=0;for(let x=0;x<(1<<n);x++)if(C.every(cl=>cl.some(a=>((x>>(Math.abs(a)-1))&1)==(a>0?1:0))))cnt++;return cnt}
const clauseAliases=new Map(),rowAliases=new Map();
for(let code=0;code<81;code++){let z=code,C=[];for(let i=1;i<=4;i++){let d=z%3;z=Math.floor(z/3);if(d)C.push(d==1?i:-i)}clauseAliases.set(tt(C),C)}
for(let m=0;m<16;m++)for(let r=0;r<2;r++)rowAliases.set(affine(m,r),[m,r]);
function combine(a,b,mixed){let o=new Set();
 if(mixed){if(pop(support(a&b))<=3)o.add(a&b);
  if(rowAliases.has(a)&&rowAliases.has(b)){let [u,r]=rowAliases.get(a),[v,s]=rowAliases.get(b);o.add(affine(u^v,r^s))}}
 if(clauseAliases.has(a)&&clauseAliases.has(b)){
  let C=clauseAliases.get(a),D=clauseAliases.get(b);
  for(let p of C)if(D.includes(-p)){
   let R=new Set([...C,...D]);R.delete(p);R.delete(-p);
   if(![...R].some(v=>R.has(-v)))o.add(tt([...R]));
  }
 }return o}
function allTrees(C,mixed=true){let n=C.length,T=new Array(1<<n).fill(null).map(()=>new Set());
 for(let i=0;i<n;i++)T[1<<i].add(tt(C[i]));
 let pairTests=0,generated=0,counts=[];
 for(let size=2;size<=n;size++){let seen=0;
  for(let S=1;S<(1<<n);S++){if(pop(S)!=size)continue;
   for(let A=(S-1)&S;A;A=(A-1)&S){let B=S^A;
    if(A>B)continue;
    for(let a of T[A])for(let b of T[B]){
     pairTests++;for(let f of combine(a,b,mixed)){T[S].add(f);generated++}
    }
   }seen+=T[S].size;
  }counts.push(seen)
 }return {falseReachable:T[(1<<n)-1].has(0),finalStates:T[(1<<n)-1].size,
  pairTests,generated,counts:[n,...counts],subsets:(1<<n)-1}}
const dagG=[
 [0,3,4,[-3,1]],[2,6,3,[1]],[3,5,4,[-3,-2]],
 [4,8,3,[-2,-1]],[1,9,2,[-1]],[7,10,1,[]]];
function proofCheck(C,rows){let all=C.map(x=>x.slice());for(let [a,b,p,r] of rows){
 if(a>=all.length||b>=all.length)throw Error('forward reference');
 let A=all[a].slice(),B=all[b].slice();
 if(A.includes(-p)&&B.includes(p)){A.splice(A.indexOf(-p),1);B.splice(B.indexOf(p),1)}
 else if(A.includes(p)&&B.includes(-p)){A.splice(A.indexOf(p),1);B.splice(B.indexOf(-p),1)}
 else throw Error('invalid pivot');
 const R=new Set([...A,...B]);if([...R].some(x=>R.has(-x))||R.size!==r.length||!r.every(x=>R.has(x)))throw Error('invalid resolvent');
 all.push(r.slice());
 }if(all.at(-1).length)throw Error('not false');return rows.length}
const stats={version:'LSPV2-DEF-SUPPORT-COVERAGE346/v1',R:'Rmix341; paid unit binary RES/AND3/XOR; charged conversions and auxiliary definitions',
 G:{clauses:G,models:models(G),deletionModels:G.map((_,i)=>models(G.filter((_,j)=>j!=i))),
  mixedTree5:allTrees(G,true),resolutionTree5:allTrees(G,false),
  witnessResolution6:proofCheck(G,dagG),certifiedMixedMin_iff_source_independent_VARDEF:6},
 H:{clauses:H,models:models(H),deletionModels:H.map((_,i)=>models(H.filter((_,j)=>j!=i))),
  mixedTree5:allTrees(H,true),resolutionTree5:allTrees(H,false),
  certifiedMixedMin:5,certifiedResolutionMin:6},
 note:'Audit: free equivalent aliases, output-support AND3, charged unary rules excluded at m-1 floor; source-bearing factor-DEF remains unverified. H five-node mixed proof: d0=AND3(s0,s5), d1=AND3(d0,s4), d2=AND3(d1,s3), d3=RES_x2(s1,s2), d4=AND3(d2,d3)=false'};
if(stats.G.mixedTree5.falseReachable||!stats.H.mixedTree5.falseReachable||stats.G.models||stats.H.models)throw Error('invalid results');
console.log(JSON.stringify(stats,null,2));
"use strict";
console.log(JSON.stringify((function affineExperiment(){
 const S={calls:0,rankCalls:0,exchangeTests:0,augmentations:0,closureScans:0,deductions:0,tautologies:0,lifts:0,referenceAssignments:0,coreAssignments:0};
 const ok=(a,m)=>{if(!a)throw Error(m)},R=n=>Array.from({length:n},(_,i)=>i);
 const dot=(a,x)=>{let v=a&x,p=0;while(v){v&=v-1;p^=1}return p};
 function basis(E){const B=new Map();for(let [a,b] of E){while(a){const k=31-Math.clz32(a);if(B.has(k)){const [u,v]=B.get(k);a^=u;b^=v}else{B.set(k,[a,b]);break}}if(!a&&b)return null}return B}
 function reduce(B,a,b){for(const k of [...B.keys()].sort((a,b)=>b-a))if(a&(1<<k)){const [u,v]=B.get(k);a^=u;b^=v}return [a,b]}
 function rank(A){S.rankCalls++;return basis(A.map(a=>[a,0])).size}
 const sat=(C,x)=>C.every(c=>c.some(([a,b])=>dot(a,x)===b)),gsat=(G,x)=>G.every(([a,b])=>dot(a,x)===b);
 function close(C,G){G=G.map(e=>e.slice());C=C.map(c=>c.map(e=>e.slice()));for(;;){const B=basis(G);if(!B)return null;let changed=false;const next=[];for(let i=0;i<C.length;i++){const c=C[i];S.closureScans++;const q=c.map(([a,b])=>reduce(B,a,b));
   if(q.some(([a,b])=>!a&&!b)||!basis(q.map(([a,b])=>[a,b^1]))){S.tautologies++;continue}
   const r=q.filter(([a])=>a);if(!r.length)return null;
   if(rank(r.map(e=>e[0]))===1){G.push(r[0]);S.deductions++;C=next.concat(C.slice(i+1));changed=true;break}next.push(c)
  }if(!changed)return {C:next,G}}
 }
 function mi(C,ids,A){S.calls++;const E=ids.flatMap(j=>C[j].map(([a,b])=>({j,a,b})));const d=rank(A);let I=[];
  const indep=I=>rank(A.concat(I.map(i=>E[i].a)))===d+I.length;
  for(;;){const sel=new Set(I),owners=new Map(I.map(i=>[E[i].j,i])),prev=new Map(),q=[];for(let x=0;x<E.length;x++)if(!sel.has(x)&&!owners.has(E[x].j)){prev.set(x,-1);q.push(x)}
   let end=-1;for(let h=0;h<q.length;h++){const x=q[h];if(!sel.has(x)){if(indep(I.concat(x))){end=x;break}for(const y of I)if(!prev.has(y)){S.exchangeTests++;if(indep(I.filter(i=>i!==y).concat(x))){prev.set(y,x);q.push(y)}}}
   else for(let y=0;y<E.length;y++)if(!sel.has(y)&&!prev.has(y)){S.exchangeTests++;const o=owners.get(E[y].j);if(o===undefined||o===x){prev.set(y,x);q.push(y)}}}
   if(end<0)return I.map(i=>E[i]);for(let x=end;x!==-1;x=prev.get(x)){if(sel.has(x))sel.delete(x);else sel.add(x)}I=[...sel];S.augmentations++;ok(indep(I)&&new Set(I.map(i=>E[i].j)).size===I.length,"augmentation")
  }
 }
 function solve(n,orig,guard){
  const z=close(orig,guard);if(!z)return {x:null,core:null,delta:null};const {C,G}=z,A=G.map(e=>e[0]),ids=R(C.length),d=ids.length-mi(C,ids,A).length;
  const X=d?ids.filter(i=>{const J=ids.filter(j=>j!==i);return J.length-mi(C,J,A).length<d}):[];
  const keep=new Set(X),O=ids.filter(j=>!keep.has(j)),D=X.map(j=>C[j]),A2=A.concat(D.flatMap(c=>c.map(e=>e[0]))),W=mi(C,O,A2);ok(W.length===O.length,"outside");
  let x=null;if(!X.length)x=0;else for(let i=0;i<2**n;i++){S.coreAssignments++;if(gsat(G,i)&&sat(D,i)){x=i;break}}
  if(x===null)return {x:null,core:X.length,delta:d};
  const B=basis(G.concat(D.flatMap(c=>c.map(([a])=>[a,dot(a,x)])),W.map(({a,b})=>[a,b])));ok(B,"lift equations");
  let y=0;for(const k of [...B.keys()].sort((a,b)=>a-b)){const [a,b]=B.get(k);if(dot(a,y)!==b)y|=1<<k}
  ok(sat(orig,y)&&gsat(guard,y),"source lift");S.lifts++;return {x:y,core:X.length,delta:d}
 }
 let seed=771124;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 const out={cases:0,sat:0,unsat:0,emptyCore:0,properNonempty:0};
 for(let t=0;t<180;t++){const n=3+rnd(5),m=1+rnd(10),C=R(m).map(()=>R(1+rnd(4)).map(()=>[1+rnd((1<<n)-1),rnd(2)])),G=R(rnd(4)).map(()=>[1+rnd((1<<n)-1),rnd(2)]),r=solve(n,C,G);let count=0;for(let i=0;i<1<<n;i++){S.referenceAssignments++;if(sat(C,i)&&gsat(G,i))count++}ok((r.x!==null)===!!count,"random mismatch");out.cases++;out[count?"sat":"unsat"]++;if(r.core===0)out.emptyCore++;if(r.core>0&&r.core<m)out.properNonempty++}
 const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const nae=([a,b,c])=>[[(1<<a)^(1<<b),1],[(1<<a)^(1<<c),1]];
 const full=F.map(nae),f=solve(7,full,[]);ok(f.x===null&&f.delta===1,"Fano");
 const neighbors=[];for(let j=0;j<7;j++)for(const b of [0,1]){const C=full.map((c,i)=>i===j?F[i].map(v=>[1<<v,b]):c),r=solve(7,C,[]);ok(r.x!==null&&r.delta===0&&r.core===0,"one-owner forest");let count=0;for(let x=0;x<128;x++){S.referenceAssignments++;if(sat(C,x))count++}ok(count===5,"count");neighbors.push({edge:j,literal:b,delta:r.delta,core:r.core,models:count})}
 return {seed:771124,random:out,Fano:{root:f,neighbors},stats:S}
})(),null,2));

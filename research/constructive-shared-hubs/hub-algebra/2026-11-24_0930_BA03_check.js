"use strict";
function main(){
 const C={rankCalls:0,vectorVisits:0,xors:0,miCalls:0,exchangeTests:0,augmentations:0,closurePasses:0,closureRowChecks:0,closureDeletes:0,quotients:0,absorbedRank:0,projectedRows:0,lifts:0,dpEdges:0,dpPeak:0,subsetChecks:0,referenceTuples:0,sourceAssignments:0};
 function xor(a,b){C.xors++;return a^b}
 function sum(a){return a.reduce(xor,0n)}
 function basis(vs){C.rankCalls++;let p=new Map();for(let x of vs){C.vectorVisits++;while(x){let k=x.toString(2).length-1;if(p.has(k))x=xor(x,p.get(k));else {p.set(k,x);break}}}return [...p].sort((a,b)=>b[0]-a[0]);}
 function rem(x,B){for(const [k,v] of B)if((x>>BigInt(k))&1n)x=xor(x,v);return x}
 const rank=vs=>basis(vs).length;
 const unique=vs=>[...new Set(vs)];
 const dirs=R=>unique(R.slice(1).map(x=>xor(x,R[0]))).filter(Boolean);
 function mi(D){
  C.miCalls++;let E=[];D.forEach((a,g)=>unique(a).filter(Boolean).forEach(v=>E.push({g,v})));let I=[];
  for(;;){
   const S=new Set(I), used=new Set(I.map(j=>E[j].g)), V=I.map(j=>E[j].v);
   const p=new Map(), q=[];for(let i=0;i<E.length;i++)if(!S.has(i)&&!used.has(E[i].g)){p.set(i,-1);q.push(i)}
   let end=-1;
   for(let h=0;h<q.length&&end<0;h++){let u=q[h];
    if(!S.has(u)){C.exchangeTests++;if(rank([...V,E[u].v])>I.length){end=u;break}
     for(let j=0;j<I.length;j++){const v=I[j];if(p.has(v))continue;C.exchangeTests++;if(rank([...V.filter((_,k)=>k!==j),E[u].v])===I.length){p.set(v,u);q.push(v)}}
    }else for(let v=0;v<E.length;v++)if(!S.has(v)&&!p.has(v)&&(!used.has(E[v].g)||E[v].g===E[u].g)){p.set(v,u);q.push(v)}
   }
   if(end<0)return I.map(j=>E[j]);
   for(let v=end;v!==-1;v=p.get(v)){if(S.has(v))S.delete(v);else S.add(v)}
   I=[...S].sort((a,b)=>a-b);C.augmentations++;
   if(new Set(I.map(j=>E[j].g)).size!==I.length||rank(I.map(j=>E[j].v))!==I.length)throw Error("bad augment")
  }
 }
 function discover(D){
  const m=D.length, all=mi(D), h=rank(D.flat());if(all.length===h)return {J:D.map((_,i)=>i),sel:all};
  const opt=all.length-m,J=[];
  for(let i=0;i<m;i++){const B=basis(D[i]);const Q=D.filter((_,j)=>j!==i).map(a=>a.map(v=>rem(v,B)));const forced=B.length-1+mi(Q).length-(m-1);if(forced===opt)J.push(i)}
  const s=mi(J.map(i=>D[i])).map(x=>({g:J[x.g],v:x.v}));
  if(s.length!==rank(J.flatMap(i=>D[i])))throw Error("bad maximal subset");
  return {J,sel:s};
 }
 function close(R,t){
  R=R.map(a=>[...a]);
  for(;;){C.closurePasses++;if(R.some(a=>!a.length))return null;
   let base=sum(R.map(a=>a[0])), D=R.map(dirs), changed=false;
   if(rem(xor(t,base),basis(D.flat())))return null;
   outer:for(let i=0;i<R.length;i++){let B=basis(D.filter((_,j)=>j!==i).flat());for(let k=0;k<R[i].length;k++){C.closureRowChecks++;if(rem(xor(xor(xor(t,base),R[i][0]),R[i][k]),B)){R[i].splice(k,1);C.closureDeletes++;changed=true;break outer}}}
   if(!changed)return R
  }
 }
 function solve(R,t,allowDP=true){
  let orig=R;R=close(R,t);if(!R)return null;if(!R.length)return t===0n?[]:null;
  const {J,sel}=discover(R.map(dirs));
  if(J.length){
   let H=basis(sel.map(x=>x.v)), s=new Set(J), out=R.map((_,i)=>i).filter(i=>!s.has(i));
   let anchor=sum(J.map(i=>R[i][0]));let qt=rem(xor(t,anchor),H);
   let maps=out.map(i=>{let a=new Map();for(let v of R[i]){C.projectedRows++;let q=rem(v,H);if(!a.has(q))a.set(q,v)}return a});
   C.quotients++;C.absorbedRank+=H.length;
   let z=solve(maps.map(a=>[...a.keys()]),qt,allowDP);if(!z)return null;
   let w=R.map(a=>a[0]);out.forEach((i,k)=>w[i]=maps[k].get(z[k]));let d=xor(t,sum(w));
   // Gaussian elimination retaining selector coefficients.
   let p=new Map();sel.forEach((e,j)=>{let v=e.v,b=1n<<BigInt(j);while(v){let k=v.toString(2).length-1;if(!p.has(k)){p.set(k,[v,b]);return}let a=p.get(k);v=xor(v,a[0]);b=xor(b,a[1])}throw Error("nonindependent")});
   let mask=0n;while(d){let k=d.toString(2).length-1,a=p.get(k);if(!a)throw Error("no repair");d=xor(d,a[0]);mask=xor(mask,a[1])}
   sel.forEach((e,j)=>{if((mask>>BigInt(j))&1n)w[e.g]=xor(w[e.g],e.v)});
   if(sum(w)!==t||w.some((v,i)=>!orig[i].includes(v)))throw Error("invalid lift");C.lifts++;return w;
  }
  if(!allowDP)throw Error("nonterminal on scale");
  let map=new Map([[0n,[]]]);
  for(let a of R){let next=new Map();for(let [x,p] of map)for(let v of a){C.dpEdges++;let y=xor(x,v);if(!next.has(y))next.set(y,[...p,v])}map=next;C.dpPeak=Math.max(C.dpPeak,map.size)}
  return map.get(t)??null;
 }
 function ref(R){let S=new Set();function go(i,x){if(i===R.length){C.referenceTuples++;S.add(x);return}for(let v of R[i])go(i+1,x^v)}go(0,0n);return S}
 function check(R,t,expected,allowDP=true){let w=solve(R,t,allowDP);if((w!==null)!==expected||w&&(sum(w)!==t||w.some((v,i)=>!R[i].includes(v))))throw Error("decision/lift discrepancy");return w}
 let seed=3172026;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 let random={systems:0,sat:0,unsat:0,discoveries:0};
 for(let a=0;a<180;a++){let d=2+rnd(5),m=1+rnd(6);let R=Array.from({length:m},()=>unique(Array.from({length:1+rnd(4)},()=>BigInt(rnd(1<<d)))));let D=R.map(dirs),found=discover(D).J;let best=Infinity, union=0;
  for(let s=0;s<(1<<m);s++){C.subsetChecks++;let J=D.filter((_,i)=>(s>>i)&1),f=rank(J.flat())-J.length;if(f<best){best=f;union=s}else if(f===best)union|=s}
  // discover may return all if all spans; all is then necessarily maximal minimizer.
  if(found.reduce((s,i)=>s|(1<<i),0)!==union)throw Error("maximal subset discrepancy");
  const S=ref(R);for(let k=0;k<4;k++){let t=k===0?[...S][0]:BigInt(rnd(1<<d));let expected=S.has(t);check(R,t,expected);random[expected?"sat":"unsat"]++}random.systems++;if(found.length)random.discoveries++;
 }
 // Fano: exact occurrence-equality syndrome compiler with one fused relation per triple.
 const lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 function fano(relax=-1){
  let tags=lines.map(()=>[0n,0n,0n]),p=0;
  for(let v=0;v<7;v++){let occ=[];lines.forEach((l,i)=>l.forEach((x,j)=>{if(x===v)occ.push([i,j])}));for(let k=1;k<occ.length;k++){let bit=1n<<BigInt(p++);for(let [i,j] of [occ[0],occ[k]])tags[i][j]^=bit}}
  let R=lines.map((_,i)=>Array.from({length:8},(_,x)=>x).filter(x=>x!==0&&x!==7||relax===2*i&&x===0||relax===2*i+1&&x===7).map(x=>sum(tags[i].filter((_,j)=>(x>>j)&1))));
  let count=0;for(let x=0;x<128;x++){C.sourceAssignments++;if(lines.every((l,i)=>{let k=l.reduce((s,v)=>s+((x>>v)&1),0);return k===1||k===2||k===0&&relax===2*i||k===3&&relax===2*i+1}))count++}
  let before=C.quotients;check(R,0n,count>0);return {relax,count,quotients:C.quotients-before};
 }
 let fanoCases=Array.from({length:15},(_,i)=>fano(i-1));
 function graph(n,edges){
  let tree=[],parent=Array.from({length:n},(_,i)=>i);function root(i){while(parent[i]!==i)i=parent[i];return i}
  let chords=[];edges.forEach(([u,v],i)=>{if(root(u)===root(v))chords.push(i);else {parent[root(u)]=root(v);tree.push(i)}});
  let adj=Array.from({length:n},()=>[]);tree.forEach(i=>{let [u,v]=edges[i];adj[u].push([v,i]);adj[v].push([u,i])});
  let cols=edges.map(()=>0n);chords.forEach((i,j)=>{let bit=1n<<BigInt(j),[u,v]=edges[i];cols[i]^=bit;let q=[[u,-1,[]]];for(let k=0;k<q.length;k++){let [x,pr,path]=q[k];if(x===v){for(let e of path)cols[e]^=bit;break}for(let [y,e] of adj[x])if(y!==pr)q.push([y,x,[...path,e]])}});
  let b=BigInt(chords.length),R=cols.map(c=>unique([c,c<<b,c^(c<<b)])),count=0;for(let x=0;x<4**n;x++){C.sourceAssignments++;if(edges.every(([u,v])=>((x>>(2*u))&3)!==((x>>(2*v))&3)))count++}
  let before=C.quotients;check(R,0n,count>0);return {n,m:edges.length,rank:2*chords.length,count,quotients:C.quotients-before};
 }
 const complete=n=>Array.from({length:n},(_,i)=>Array.from({length:n-i-1},(_,j)=>[i,i+j+1])).flat();
 let K=complete(5), graphs=[graph(4,complete(4)),graph(5,K),...K.map((_,i)=>graph(5,K.filter((_,j)=>i!==j)))];
 let scales=[];for(let r of [3,4,8,16,24]){
  let bits=Array.from({length:r},(_,i)=>1n<<BigInt(i)),cols=[...bits,...bits.slice(0,-1).map((v,i)=>v^bits[i+1]),bits[0]^bits[1]^bits[r-1]];
  let R=cols.map(v=>[v,v<<BigInt(r),v^(v<<BigInt(r))]);
  if(new Set(cols).size!==cols.length)throw Error("duplicate columns");
  let old={...C},t=(1n<<BigInt(2*r))-1n;check(R,t,true,false);scales.push({factors:R.length,initialRank:2*r,absorbedRank:C.absorbedRank-old.absorbedRank,quotients:C.quotients-old.quotients,rankCalls:C.rankCalls-old.rankCalls,exchangeTests:C.exchangeTests-old.exchangeTests,closureRowChecks:C.closureRowChecks-old.closureRowChecks,dpEdges:C.dpEdges-old.dpEdges});
 }
 const counter=[[0n,1n,2n,4n,7n],[0n,1n,2n,4n,7n]];let cr=ref(counter).size, j=discover(counter.map(dirs)).J.length;if(cr!==8||j!==0)throw Error("counterexample");
 return {seed:3172026,random,fanoCases,graphs,scales,counterexample:{sumsetSize:cr,selectedFactors:j},counters:C,discrepancies:0};
}
console.log(JSON.stringify(main(),null,2));

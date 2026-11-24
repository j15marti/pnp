"use strict";
function runBA04(){
 const C={rankAdds:0,xor:0,closureScans:0,rowDeletes:0,periodCandidates:0,membershipChecks:0,quotients:0,removedRank:0,dpEdges:0,peakDP:0,lifts:0,sourceChecks:0,referenceLeaves:0};
 const assert=(x,m)=>{if(!x)throw Error(m)};
 const bit=i=>1n<<BigInt(i), key=r=>r.c.join(",")+"|"+r.k, rk=r=>key(r)+"|"+r.t;
 class Basis{
 constructor(){this.b=[];this.g=[]}
 reduce(v){let z=0n;for(const a of this.b)if(v&a.p){v^=a.v;z^=a.z;C.xor++}return [v,z]}
 add(v,i=0){C.rankAdds++;let [w,z]=this.reduce(v);if(!w)return;let p=bit(w.toString(2).length-1);z^=bit(this.g.length);this.g.push({v,i});this.b.push({p,v:w,z});this.b.sort((a,b)=>a.p>b.p?-1:1)}
 }
 const xor=a=>a.reduce((s,x)=>s^x,0n);
 function closure(A,t,K){A=A.map(a=>a.slice());for(;;){C.closureScans++;if(A.some(a=>!a.length))return null;let changed=false;
  outer:for(let i=0;i<A.length;i++){let B=new Basis(), offset=0n;const mins=K.map(()=>0);
   for(let j=0;j<A.length;j++)if(i!==j){let a=A[j][0];offset^=a.t;for(const r of A[j])B.add(r.t^a.t);K.forEach((_,k)=>mins[k]+=Math.min(...A[j].map(r=>r.c[k])))}
   for(let j=0;j<A[i].length;j++){let r=A[i][j];if(B.reduce(t^offset^r.t)[0]||K.some((k,l)=>r.c[l]+mins[l]>k)){A[i].splice(j,1);C.rowDeletes++;changed=true;break outer}}
  }if(!changed)return A;
 }}
 function periods(a){const M=new Map();for(const r of a){const k=key(r);if(!M.has(k))M.set(k,new Set());M.get(k).add(r.t)}
  const F=[...M.values()].sort((a,b)=>a.size-b.size), x=[...F[0]][0],out=[];
  for(const y of F[0]){const h=x^y;if(!h)continue;C.periodCandidates++;let ok=true;
   check:for(const S of F)for(const v of S){C.membershipChecks++;if(!S.has(v^h)){ok=false;break check}}
   if(ok)out.push(h)
  }return out;
 }
 function normalize(A,t,K,reverse=false){let stack=[],history=[];for(;;){A=closure(A,t,K);if(!A)return {A:null,t,stack,history};const B=new Basis();const ids=A.map((_,i)=>i);if(reverse)ids.reverse();for(const i of ids)for(const h of periods(A[i]))B.add(h,i);
   if(!B.g.length)return {A,t,stack,history};C.quotients++;C.removedRank+=B.g.length;history.push(B.g.length);stack.push({A,t,B});
   A=A.map(a=>{const m=new Map();for(const r of a){const q={...r,t:B.reduce(r.t)[0],prev:r};if(!m.has(rk(q)))m.set(rk(q),q)}return [...m.values()]});t=B.reduce(t)[0]
 }}
 function lift(Z,picks){for(let j=Z.stack.length-1;j>=0;j--){let {A,t,B}=Z.stack[j];picks=picks.map(r=>r.prev);let [rem,z]=B.reduce(t^xor(picks.map(r=>r.t)));assert(!rem,"lift discrepancy");let shifts=A.map(()=>0n);B.g.forEach((g,i)=>{if(z&bit(i))shifts[g.i]^=g.v});picks=picks.map((r,i)=>{const p=A[i].find(q=>key(q)===key(r)&&q.t===(r.t^shifts[i]));assert(p,"missing period witness");return p});C.lifts++}return picks}
 function verify(A,t,K,p){C.sourceChecks++;assert(p.length===A.length&&p.every((r,i)=>A[i].includes(r))&&xor(p.map(r=>r.t))===t&&K.every((k,j)=>p.reduce((s,r)=>s+r.c[j],0)<=k),"source witness")}
 function dp(A,t,K){let M=new Map([["0|"+K.map(()=>0).join(","),{t:0n,c:K.map(()=>0),p:[]}]]);for(const a of A){let D=new Map();for(const s of M.values())for(const r of a){C.dpEdges++;let c=s.c.map((x,j)=>x+r.c[j]);if(c.some((x,j)=>x>K[j]))continue;let v=s.t^r.t,k=v+"|"+c.join(",");if(!D.has(k))D.set(k,{t:v,c,p:[...s.p,r]})}M=D;C.peakDP=Math.max(C.peakDP,M.size)}return [...M.values()].find(s=>s.t===t)?.p??null}
 function solve(A,t,K,reverse=false){let Z=normalize(A,t,K,reverse);let p=Z.A&&dp(Z.A,Z.t,K);if(p){p=lift(Z,p);verify(A,t,K,p)}return {sat:!!p,history:Z.history,rows:Z.A?.reduce((s,a)=>s+a.length,0)??0}}
 function brute(A,t,K){function rec(i,v,c){if(i===A.length){C.referenceLeaves++;return v===t}return A[i].some(r=>{let d=c.map((x,j)=>x+r.c[j]);return d.every((x,j)=>x<=K[j])&&rec(i+1,v^r.t,d)})}return rec(0,0n,K.map(()=>0))}
 const row=(t,c=[],k="")=>({t:BigInt(t),c,k});
 function pad(A,d){const m=A.length;return A.map((a,i)=>{const e=bit(d+i),prev=bit(d+(i+m-1)%m),S=i===0?[0n,e,prev,e^prev]:[0n,e,e^prev];return a.flatMap(r=>S.map(h=>row(r.t^h,r.c,r.k)))})}
 function graph(n,E){let tree=[],adj=Array.from({length:n},()=>[]),seen=new Set([0]);for(let again=true;again;){again=false;for(let i=0;i<E.length;i++){let [u,v]=E[i];if(seen.has(u)!==seen.has(v)){seen.add(u);seen.add(v);tree.push(i);adj[u].push([v,i]);adj[v].push([u,i]);again=true}}}assert(seen.size===n,"connected");let col=E.map(()=>0n),q=0;
 for(let i=0;i<E.length;i++)if(!tree.includes(i)){let [u,v]=E[i];function path(x,p){if(x===v)return [];for(let [y,j] of adj[x])if(y!==p){let a=path(y,x);if(a)return [j,...a]}return null}for(let j of [i,...path(u,-1)])col[j]|=bit(q);q++}
 return {A:col.map(c=>[1,2,3].map(x=>row((x&1?c:0n)^(x&2?c<<BigInt(q):0n)))),d:2*q}}
 let seed=20261124;const rnd=n=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n};
 let random={sat:0,unsat:0},orderChecks=0;
 for(let i=0;i<180;i++){let A=Array.from({length:2+rnd(4)},()=>Array.from({length:2+rnd(7)},()=>row(rnd(16),[rnd(3)],String(rnd(2))))),t=BigInt(rnd(16)),K=[rnd(8)];let ref=brute(A,t,K),got=solve(A,t,K),rev=solve(A,t,K,true);assert(got.sat===ref&&rev.sat===ref,"random decision");assert(got.history.reduce((a,b)=>a+b,0)===rev.history.reduce((a,b)=>a+b,0),"basis order");orderChecks++;random[ref?"sat":"unsat"]++}
 const graphs=[];let E=[];for(let u=0;u<5;u++)for(let v=u+1;v<5;v++)E.push([u,v]);for(let del=-1;del<E.length;del++){let edges=E.filter((_,i)=>i!==del),{A,d}=graph(5,edges),P=pad(A,d),t=bit(d+edges.length)-bit(d);let got=solve(P,t,[]),base=solve(A,0n,[]);let models=0;for(let w=0;w<1024;w++)if(edges.every(([u,v])=>((w>>(2*u))&3)!==((w>>(2*v))&3)))models++;assert(got.sat===(models>0)&&base.sat===got.sat,"graph");graphs.push({del,models,rank:d,paddedRank:d+edges.length,history:got.history,remainingRows:got.rows})}
 const triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 function fano(rel){let cols=triples.map(()=>[0n,0n,0n]),d=0;for(let v=0;v<7;v++){let occ=[];triples.forEach((a,i)=>a.forEach((x,j)=>{if(x===v)occ.push([i,j])}));for(let j=1;j<occ.length;j++){let [i0,k0]=occ[0],[i1,k1]=occ[j];cols[i0][k0]^=bit(d);cols[i1][k1]^=bit(d++)}}
 let A=cols.map((a,i)=>Array.from({length:8},(_,w)=>w).filter(w=>(w!==0||rel===2*i)&&(w!==7||rel===2*i+1)).map(w=>row(xor(a.filter((_,j)=>w&(1<<j))))));return {A,d}}
 const fanos=[];for(let rel=-1;rel<14;rel++){let {A,d}=fano(rel),P=pad(A,d),t=bit(d+7)-bit(d),got=solve(P,t,[]);let models=0;for(let w=0;w<128;w++)if(triples.every((a,i)=>{let s=a.reduce((q,v)=>q+((w>>v)&1),0);return (s!==0||rel===2*i)&&(s!==3||rel===2*i+1)}))models++;assert(got.sat===(models>0),"fano");fanos.push({rel,models,history:got.history,remainingRows:got.rows})}
 let hostile=solve([[row(0,[],"a"),row(1,[],"b")]],1n,[]);assert(hostile.sat,"key");assert(!solve([[row(0,[0]),row(1,[1])]],1n,[0]).sat,"key budget");let ap=normalize([[row(0),row(1),row(2)],[row(0),row(1),row(2)]],3n,[]);assert(ap.history.length===0&&!!dp(ap.A,ap.t,[]),"emergent period");
 const scale=[];for(let m of [8,16,32,64,128]){let A=Array.from({length:m},()=>[row(1),row(2),row(3)]),P=pad(A,2),t=bit(2+m)-4n,got=solve(P,t,[]);assert(got.sat&&got.history.reduce((a,b)=>a+b,0)===m,"scale");scale.push({m,removed:m,rounds:got.history.length,remainingRows:got.rows})}
 return {seed:20261124,random,orderChecks,graphs,fanos,scale,hostile:"key budget rejects, aperiodic pair has full sumset but no local periods",counters:C}
}
console.log(JSON.stringify(runBA04(),null,2));

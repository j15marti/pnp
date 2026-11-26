'use strict';
// Independent direct path-traversal table construction and partial matching context audit.
// Run with Node.js.
function audit(){
 const comb=(a,k)=>k===0?[[]]:a.length<k?[]:a.flatMap((x,i)=>comb(a.slice(i+1),k-1).map(t=>[x,...t]));
 const perms=a=>a.length===0?[[]]:a.flatMap((x,i)=>perms(a.filter((_,j)=>j!==i)).map(t=>[x,...t]));
 const partial=a=>!a.length?[[]]:[...partial(a.slice(1)),...a.slice(1).flatMap((x,i)=>partial(a.slice(1).filter((_,j)=>j!==i)).map(p=>[[a[0],x],...p]))];
 const edge=(a,b)=>[Math.min(a,b),Math.max(a,b)]; const norm=p=>p.map(e=>edge(...e)).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
 const reach=(i,j,es)=>{let q=[i],s=new Set(q);for(let k=0;k<q.length;k++)for(const [a,b] of es){const v=a===q[k]?b:b===q[k]?a:-1;if(v>=0&&!s.has(v)){s.add(v);q.push(v)}}return s.has(j)};
 const ports=[0,1,2,3,4,5];const all=partial(ports);
 function check(R){const U=new Set(R.flatMap(p=>p.map(e=>e.join(','))));const P=all.filter(p=>p.every(e=>U.has(e.join(','))));for(const [i,j] of comb(ports,2))for(const W of partial(ports.filter(x=>x!==i&&x!==j)))if(P.some(p=>reach(i,j,p.concat(W)))&&!R.some(p=>reach(i,j,p.concat(W))))return false;return true;}
 const cache=new Map(),counts={};
 for(const A of comb(ports,3))for(const B of comb(ports.map(x=>x+6),3))for(const C of perms(B)){
 const W=new Map();A.forEach((a,i)=>{W.set(a,C[i]);W.set(C[i],a)});const exposed=Array.from({length:12},(_,i)=>i).filter(i=>!W.has(i));const R=new Map();
 for(let x=0;x<2;x++)for(let y=0;y<2;y++){
 const T=new Map();for(const [v,b] of [[0,x],[6,y]])for(let i=b;i<6;i+=2){const a=v+i,c=v+(i+1)%6;T.set(a,c);T.set(c,a)}
 let p=[];for(const s of exposed){let u=T.get(s),guard=0;while(W.has(u)){u=T.get(W.get(u));if(++guard>12)throw Error("loop")};if(s<u)p.push(edge(exposed.indexOf(s),exposed.indexOf(u)))}
 p=norm(p);R.set(JSON.stringify(p),p)}
 const rel=[...R.entries()].sort((a,b)=>a[0].localeCompare(b[0])).map(e=>e[1]);const key=JSON.stringify(rel);if(!cache.has(key))cache.set(key,check(rel));const tag=rel.length+":"+cache.get(key);counts[tag]=(counts[tag]||0)+1;
 }
 const hex=[[[0,1],[2,3],[4,5]],[[0,5],[1,2],[3,4]]];if(check(hex))throw Error("hex unexpectedly safe");
 const expected={"4:false":1224,"3:false":864,"4:true":144,"2:false":144,"3:true":24};for(const k in expected)if(counts[k]!==expected[k])throw Error("count mismatch");
 return {counts,distinct:cache.size,hexSafe:false};
}
console.log(JSON.stringify(audit(),null,2));

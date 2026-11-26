// Node.js independent exact source rotation/phase/finite-mask verification.
const run=()=>{
let checks=0;const ok=x=>{checks++;if(!x)throw Error("assertion "+checks)};
const B="000 012 010 110 111 221 333 332 002 100 103 223".split(" ").map(s=>[...s].map(Number));
const V=[[0,4,7,11],[1,5,6,9],[2,5,7,10],[3,5,6,8]];
const R0=[[12,14,13,20],[15,21,22,16],[17,23],[18,19],[12,20,22,21],[13,14,15,16],[23,17],[19,18],[14,12,21,15],[16,17],[20,13,19],[23,22,18],[0,4,8],[10,0,5],[5,0,8],[8,1,5],[1,9,5],[9,2,6],[11,3,7],[3,10,7],[4,0,10],[1,8,4],[11,1,4],[2,11,6]];
function instance(k){
 const T=Array.from({length:k},(_,i)=>B.map(t=>t.map(v=>v+4*i))).flat(),R=Array.from({length:k},(_,i)=>R0.map(r=>r.map(v=>v+24*i))).flat();
 const replace=(u,v,w)=>{let j=R[u].indexOf(v);ok(j>=0);R[u][j]=w;};
 for(let i=0;i<k-1;i++)for(const [e,ax] of [[i%2?4:11,1],[i%2?7:6,2]]){
  let a=12*i+e,b=a+12;[T[a][ax],T[b][ax]]=[T[b][ax],T[a][ax]];
  let t=24*i+12+e,u=24*i+4*ax+B[e][ax],s=t+24,v=u+24;
  replace(t,u,v);replace(u,t,s);replace(s,v,u);replace(v,s,t);
 }
 return {T,R};
}
function cover(T,n,W){return W.length===n&&[0,1,2].every(a=>new Set(W.map(e=>T[e][a])).size===n)}
function brute(T,n){const by=Array.from({length:n},(_,i)=>T.flatMap((t,j)=>t[0]===i?[j]:[]));let count=0;const dfs=(i,Y,Z)=>{if(i===n){count++;return}for(const j of by[i]){const [x,y,z]=T[j];if(!Y.has(y)&&!Z.has(z)){Y.add(y);Z.add(z);dfs(i+1,Y,Z);Y.delete(y);Z.delete(z)}}};dfs(0,new Set(),new Set());return count}
const results=[];
for(const k of [1,2,4,8,16,32,64,128]){
 const {T,R}=instance(k),n=4*k;
 ok(new Set(T.map(t=>t.join(","))).size===T.length);
 for(let i=0;i<R.length;i++){ok(new Set(R[i]).size===R[i].length);for(const v of R[i])ok(R[v].includes(i));}
 for(let e=0;e<T.length;e++){let u=24*Math.floor(e/12)+12+e%12;let v=T[e].map((x,a)=>24*Math.floor(x/4)+4*a+x%4);ok(v.every(j=>R[u].includes(j)));}
 let D=new Set(),F=0;for(let i=0;i<R.length;i++)for(let j of R[i])if(!D.has(i+","+j)){F++;let a=i,b=j;while(!D.has(a+","+b)){D.add(a+","+b);let c=R[b][(R[b].indexOf(a)+1)%R[b].length];a=b;b=c;}ok(a===i&&b===j);}
 ok(D.size===72*k);ok(F===12*k+2);ok(R.length-D.size/2+F===2);
 let seen=new Set([0]),Q=[0];while(Q.length)for(let v of R[Q.pop()])if(!seen.has(v)){seen.add(v);Q.push(v)}ok(seen.size===R.length);
 const words=[Array(k).fill(0),Array(k).fill(2),Array(k).fill(1),Array(k).fill(3)];for(let i=0;i<k;i++)words.push(Array.from({length:k},(_,j)=>i===j?3:1));
 const W=words.map(w=>w.flatMap((v,i)=>V[v].map(e=>12*i+e)));for(const w of W)ok(cover(T,n,w));
 // Derive signed classes from the separating genuine witnesses (diagnostic, not acquisition).
 let rep=new Map(),C=[];
 for(let e=0;e<T.length;e++){let a=W.map(w=>+w.includes(e)).join(""),b=[...a].map(x=>1-Number(x)).join("");ok(a.includes("0")&&a.includes("1"));let t=a<b?a:b;if(!rep.has(t))rep.set(t,rep.size);C[e]=[rep.get(t),a===t?1:0];}
 let rows=new Map();
 for(let a=0;a<3;a++)for(let v=0;v<n;v++){
  const r=T.flatMap((t,e)=>t[a]===v?[C[e]]:[]).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
  ok(new Set(r.map(x=>x.join(","))).size===r.length);
  if(r.some(([c,s])=>r.some(([d,t])=>c===d&&s!==t))){ok(r.length===2);continue;}
  rows.set(JSON.stringify(r),r);
 }
 const Rw=[...rows.values()],occ=Array.from({length:rep.size},(_,c)=>Rw.flatMap((r,i)=>r.some(x=>x[0]===c)?[i]:[])),H=occ.flatMap((s,c)=>s.length>2?[c]:[]);
 let parent=Rw.map((_,i)=>i);function root(i){while(parent[i]!==i)i=parent[i];return i}for(let s of occ)if(s.length===2)parent[root(s[1])]=root(s[0]);let cc=new Set(Rw.map((_,i)=>root(i)));let E=H.reduce((a,h)=>a+new Set(occ[h].map(root)).size,0);
 if(k>1){ok(Rw.length===2*k+1);ok(H.length===3);ok(cc.size===k+1);ok(E===3*(k+1));}
 if(k<=4)ok(brute(T,n)===2**k+2);
 // Direct rational redundancy identity on symbolic rows: g=A+C+F=1, s_i=B_i+D_i-F=0, r_i=A+C+B_i+D_i=1.
 for(let i=0;i<k;i++)for(let bits=0;bits<32;bits++){let a=bits&1,c=(bits>>1)&1,f=(bits>>2)&1,b=(bits>>3)&1,d=(bits>>4)&1;ok((a+c+b+d-1)===(a+c+f-1)+(b+d-f))}
 results.push({k,triples:T.length,faces:F,rows:Rw.length,hubs:H.length,torsos:cc.size,edges:E,witnesses:W.length});
}
// Independently enumerate all small mandatory/optional matching gadgets for all 16 masks.
let maskChecks=0;for(let mask=0;mask<16;mask++){
 let edges=[],req=new Set(),add=(u,v)=>edges.push([u,v]);const zero=mask&1,one=[0,1].filter(i=>mask&(1<<(1<<i))),two=mask&8;
 if(zero){for(let u of one)add(u,2);if(two)add(0,1)}
 else if(two&&!one.length){req.add(2);req.add(3);add(0,2);add(1,3)}
 else{req.add(2);for(let u of one)add(u,2);if(two){add(0,3);add(1,3)}}
 let realized=0;for(let s=0;s<(1<<edges.length);s++){let used=new Set(),valid=true;for(let i=0;i<edges.length;i++)if(s>>i&1){for(let u of edges[i]){if(used.has(u))valid=false;used.add(u)}}if(valid&&[...req].every(u=>used.has(u)))realized|=1<<((used.has(0)?1:0)|(used.has(1)?2:0));}ok(realized===mask);maskChecks++;
}
return {checks,maskChecks,results};
};
console.log(JSON.stringify(run(),null,2));

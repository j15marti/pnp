// Run with node adaptive_audit.js in directory containing results.json
function adaptive(records){
 const bits=x=>{let a=[];while(x){let b=x&-x;x^=b;a.push(31-Math.clz32(b))}return a},f=s=>"1".repeat(s.length)+"0"+s;let checks=0;const ck=x=>{checks++;if(!x)throw Error("assert "+checks)};
 function reconstruct(G){let n=G.length-1,E=G.flatMap((a,i)=>i?bits(a).filter(j=>j>0).map(j=>[i-1,j-1]):[]),id=2,ready=Array.from({length:n},()=>id++),seek=Array.from({length:n},(_,v)=>Array.from({length:v+1},()=>id++)),ret=Array.from({length:n},()=>id++),verify=id++,R=[];
 const add=(u,a,v,c,d)=>R.push([u,a,0,v,c,0,d,2]),stay=(u,v)=>{for(let a of [1,2])add(u,a,v,a,2)};
 for(let v=0;v<n;v++)stay(0,seek[v][v]);for(let [u,v] of E)stay(ready[u],seek[v][v]);for(let u of [0,...ready])stay(u,verify);
 for(let v=0;v<n;v++){for(let r=v;r>0;r--)for(let a of [1,2])add(seek[v][r],a,seek[v][r-1],a,1);add(seek[v][0],1,ret[v],2,0);for(let a of [1,2])add(ret[v],a,ret[v],a,0);add(ret[v],0,ready[v],0,1)}add(verify,2,verify,2,1);add(verify,0,1,0,2);
 let w=f(R.map(r=>r.map(x=>f(x.toString(2))).join("")).join(""))+f("0".repeat(n))+f((n*n+3*n+2).toString(2));let hash=2166136261;for(let c of w)hash=Math.imul(hash^c.charCodeAt(0),16777619)>>>0;return{w,hash:hash.toString(16)}}
 function calc(G,C,S=0){let n=G.length,V=((1<<n)-1)^S,A=G.map((a,i)=>(V>>i&1)?(a&V)|(1<<i):0);for(let k=0;k<n;k++)if(V>>k&1)for(let i=0;i<n;i++){C.tick();if(A[i]>>k&1)A[i]|=A[k]}return[A,V]}
 function match(G,C){let n=G.length,M=Array(n).fill(-1),seen=0,count=0;function aug(i){for(let j of bits(G[i])){C.tick();if(seen>>j&1)continue;seen|=1<<j;if(M[j]<0||aug(M[j])){M[j]=i;return true}}return false}for(let i=0;i<n;i++){seen=0;if(aug(i))count++}return {M,count}}
 function support(G,C){let {M,count}=match(G,C);if(count!==G.length)return null;let H=G.map(a=>bits(a).reduce((x,j)=>x|(1<<M[j]),0)),[A]=calc(H,C);return G.map((a,i)=>bits(a).reduce((x,j)=>{C.tick();return A[M[j]]>>i&1?x|(1<<j):x},0))}
 function prefix(G,C){let n=G.length,[A,V]=calc(G,C);if(A.some(a=>a!==V))return{S:[],type:"not strongly connected"};
 let degree=G.map((a,i)=>bits(a).length+G.reduce((t,b)=>t+(b>>i&1),0)),order=Array.from({length:n},(_,i)=>i).sort((i,j)=>degree[j]-degree[i]||i-j),S=0;
 for(let i=0;i<n-1;i++){S|=1<<order[i];let [A,V]=calc(G,C,S),rep=[];let un=V;while(un){let u=bits(un)[0],block=0;for(let v of bits(un)){C.tick();if((A[u]>>v&1)&&(A[v]>>u&1))block|=1<<v}rep.push(u);un&=~block}
 if(rep.length<=i+1)continue;let H=rep.map(u=>rep.reduce((a,v,j)=>{C.tick();return u!==v&&(A[u]>>v&1)?a|(1<<j):a},0)),{count}=match(H,C),width=rep.length-count;if(width>i+1)return{S:bits(S),rep,width,matchingSize:count};}
 return null}
 function lane(r,hybrid){let C={ops:0,cap:r.N**2,tick(){if(++this.ops>this.cap)throw Error("cap")}};try{let G=r.rows.slice();if(hybrid){G=support(G,C);if(!G)return{status:"NO",cert:"Hall",ops:C.ops}}let cert=prefix(G,C);return{status:cert?"NO":"UNKNOWN",cert,ops:C.ops}}catch(e){if(e.message!=="cap")throw e;return{status:"UNKNOWN",cap:true,ops:C.cap}}}
 let results=[];for(let r of records){let a=reconstruct(r.rows);ck(a.w.length===r.N&&a.hash===r.fnv32);let b=reconstruct(r.rows);ck(a.w===b.w);let B=lane(r,false),I=lane(r,true);results.push({kind:r.kind,n:r.n,N:r.N,fnv32:r.fnv32,B,I})}return{checks,results,scope:"same exact deterministic reconstruction of native inputs from authenticated records, equality across copies, FNV diagnostic; numerical probe cap N^2; prefix degree scan only, no claims of complete separator discovery"}}
const fs=require('fs');console.log(JSON.stringify(adaptive(JSON.parse(fs.readFileSync('results.json','utf8')).records),null,2));

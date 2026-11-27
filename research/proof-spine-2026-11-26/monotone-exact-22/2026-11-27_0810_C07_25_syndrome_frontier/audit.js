function audit(){
const CAP=2000000, sizes=[2,4,8,16,32], results=[];
function meter(){let n=0;return {tick(k=1){n+=k;if(n>CAP)throw Error("cap")},get n(){return n}}}
function source(k){
 let rows=[], next=k+1;
 for(let i=0;i<k;i++){let v=[i,i+1,next++,next++,next++,next++,next++];for(let t of [[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]])rows.push(t.map(j=>v[j]));}
 rows.push([0,Math.floor(k/2),k]);let n=next;return {rows:rows.map(t=>[...t,n++]),n,guards:{}}}
function rank(vs,M){let b=new Map();for(let x of vs){while(x){M.tick();let i=x.toString(2).length-1;if(b.has(i))x^=b.get(i);else{b.set(i,x);break}}}return b}
function inspan(x,b,M){while(x){M.tick();let i=x.toString(2).length-1;if(!b.has(i))return false;x^=b.get(i)}return true}
function chart(F,M){
 let freq=Array(F.n).fill(0);for(let row of F.rows)for(let x of row){M.tick();freq[x]++}
 let edges=[],pairs=[], seen=new Set();
 for(let row of F.rows){let priv=row.filter(x=>freq[x]===1);if(priv.length!==1)throw Error("private");let t=row.filter(x=>x!==priv[0]);let j=edges.length;for(let x of t.slice(1)){let u=t[0],key=[u,x].sort((a,b)=>a-b).join(",");if(seen.has(key))throw Error("duplicate");seen.add(key);edges.push([u,x]);M.tick()}pairs.push([j,j+1]);}
 // Fundamental cycles from a spanning forest, via tree paths.
 let adj=Array.from({length:F.n},()=>[]),parent=Array.from({length:F.n},(_,i)=>i),cycles=[];
 function find(i){while(parent[i]!==i){M.tick();i=parent[i]}return i}
 edges.forEach(([u,v],j)=>{let a=find(u),b=find(v);if(a!==b){parent[a]=b;adj[u].push([v,j]);adj[v].push([u,j]);return}
 let stack=[[u,-1,0n]],found=false;
 while(stack.length){M.tick();let [w,p,mask]=stack.pop();if(w===v){cycles.push(mask|(1n<<BigInt(j)));found=true;break}for(let [z,e] of adj[w])if(z!==p)stack.push([z,w,mask|(1n<<BigInt(e))])}if(!found)throw Error("path")});
 let cols=edges.map((_,i)=>{let c=0n;cycles.forEach((v,j)=>{M.tick();if((v>>BigInt(i))&1n)c|=1n<<BigInt(j)});return c});
 return {edges,pairs,cols,r:cycles.length};
}
function native(F,M){let last=Array(F.n).fill(-1);F.rows.forEach((row,i)=>row.forEach(x=>{M.tick();last[x]=i}));let seen=new Set(),states=new Set([0n]),peak=1,tries=0;
 for(let i=0;i<F.rows.length;i++){let row=F.rows[i],fresh=row.filter(x=>!seen.has(x)),out=new Set(),retire=row.filter(x=>last[x]===i).reduce((v,x)=>v|(1n<<BigInt(x)),0n);
 for(let s of states)for(let a=0;a<2**fresh.length;a++){M.tick();tries++;let v=s;fresh.forEach((x,j)=>{if((a>>j)&1)v|=1n<<BigInt(x)});let sum=row.reduce((z,x)=>z+Number((v>>BigInt(x))&1n),0);if(sum===2)out.add(v&~retire)}
 row.forEach(x=>seen.add(x));states=out;peak=Math.max(peak,states.size);}
 return {no:states.size===0,peak,tries,work:M.n};}
function algebra(F,M){let C=chart(F,M);let r=rank(C.cols,M).size;if(r!==C.r)throw Error("rank");return {r,edges:C.edges.length,clauses:C.pairs.length,work:M.n,lowWeight:0,reason:"simple graph cycle space has no weight 1 or 2; H is disjoint positive pairs; both independently feasible"}}
function independent(F,k,M){let checks=0;for(let i=0;i<k;i++){let rows=F.rows.slice(6*i,6*i+6),ids=[...new Set(rows.flatMap(r=>r.slice(0,3)))].sort((a,b)=>a-b),bound=[i,i+1,...ids.filter(x=>x>k).slice(0,1)];let support=new Set();
 for(let a=0;a<2**ids.length;a++){M.tick();let bit=x=>(a>>ids.indexOf(x))&1,ok=true;for(let row of rows){M.tick();checks++;let t=row.slice(0,3).reduce((s,x)=>s+bit(x),0);if(t!==1&&t!==2){ok=false;break}}if(ok)support.add(bound.map(bit).join(""))}
 if([...support].sort().join(",")!=="000,111")throw Error("bad support");}
 let final=F.rows[F.rows.length-1];if(final.slice(0,3).some(x=>x>k)||new Set(final.slice(0,3)).size!==3)throw Error("bad end");return {no:true,checks,blocks:k,work:M.n}}
function hybrid(F,M){let C=chart(F,M),m=C.cols.length,suffix=[],width=0,p=0,states=new Set([0n]),peak=1,tries=0,pre=[];for(let j=0;j<=m;j+=2){let l=rank(C.cols.slice(0,j),M),r=rank(C.cols.slice(j),M);width=Math.max(width,l.size+r.size-C.r);suffix.push(r)}
 for(let j=0;j<m;j+=2){let b=suffix[j/2+1],u=C.cols[j],v=C.cols[j+1],out=new Set();for(let s of states)for(let t of [u,v,u^v]){M.tick();tries++;let z=s^t;if(inspan(z,b,M))out.add(z)}states=out;peak=Math.max(peak,states.size);pre.push(states.size)}
 return {no:!states.has(0n),width,peak,tries,work:M.n,frontier:pre};}
for(let k of sizes){let F=source(k),encoded=JSON.stringify(F),N=8*encoded.length;let A=native(F,meter()),B=algebra(F,meter()),C=independent(F,k,meter()),D=hybrid(F,meter());if(!A.no||!C.no||!D.no)throw Error("mismatch");results.push({k,N,n:F.n,rows:F.rows.length,A,B,C,D,source:F})}
return results;
}
if(typeof module!=='undefined' && require.main===module)console.log(JSON.stringify(audit(),null,2));

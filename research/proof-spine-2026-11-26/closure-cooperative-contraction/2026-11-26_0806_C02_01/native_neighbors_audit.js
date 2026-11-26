// Node.js. Independent cubic source neighbors and tariff checks.
const audit=()=>{
let checks=0;const ok=p=>{checks++;if(!p)throw Error("audit "+checks)};
function graph(n,edges){let I=Array.from({length:n},()=>[]);edges.forEach(([u,v],e)=>{ok(u!==v&&u>=0&&v>=0&&u<n&&v<n);I[u].push(e);I[v].push(e)});ok(I.every(a=>a.length===3));ok(new Set(edges.map(e=>e.slice().sort((a,b)=>a-b).join(","))).size===edges.length);return {n,E:edges,I}}
function ring(h,d){let n=2*h*d+2,s=n-2,t=n-1,E=[],b=[],v=(i,j)=>2*d*i+j;function edge(u,w,z){E.push([u,w]);b.push(z)}
for(let i=0;i<h;i++)for(let j=0;j<2*d;j++)edge(v(i,j),v(i,(j+1)%(2*d)),+(j%2===0)^(+(i<2)));
for(let i=0;i<h;i++)for(let j=0;j<d;j++){let u=v(i,d+j),w=v((i+1)%h,j);if(i===h-1&&j<2){edge(u,u%2?t:s,1);edge(w,w%2?t:s,1)}else edge(u,w,1)}edge(s,t,0);
let G=graph(n,E),c=b.map(v=>v?0:2);for(let e=0;e<E.length;e++)if(!c[e]){let start=E[e][0],u=start,k=e,col=1;do{ok(!c[k]);c[k]=col;u=E[k][0]^E[k][1]^u;k=G.I[u].find(j=>j!==k&&b[j]);col=4-col}while(u!==start);ok(k===e&&col===1)}verify(G,c);return {G,c}}
function verify(G,c){ok(c.length===G.E.length&&c.every(v=>v>=1&&v<=3));for(let a of G.I)ok(new Set(a.map(i=>c[i])).size===3)}
function small(step){let E=[];for(let i=0;i<5;i++){E.push([i,(i+1)%5],[i+5,5+(i+step)%5],[i,i+5])}return graph(10,E)}
function all(G){let c=Array(G.E.length).fill(0),used=Array(G.n).fill(0),count=0,witness=null;function rec(){let best=-1,opts=0;for(let e=0;e<c.length;e++)if(!c[e]){let [u,v]=G.E[e],m=14&~(used[u]|used[v]);if(!m)return;let pc=[1,2,3].filter(k=>m>>k&1).length;if(best<0||pc<[1,2,3].filter(k=>opts>>k&1).length){best=e;opts=m}}if(best<0){count++;witness??=c.slice();return}let [u,v]=G.E[best];for(let k=1;k<=3;k++)if(opts>>k&1){c[best]=k;used[u]|=1<<k;used[v]|=1<<k;rec();c[best]=0;used[u]^=1<<k;used[v]^=1<<k}}rec();return {count,witness}}
let P=small(2),Q=small(1),p=all(P),q=all(Q);ok(p.count===0&&q.count>0);verify(Q,q.witness);
function join(G,H){let a=G.E.length-1,b=0,[u,v]=G.E[a],[x,y]=H.E[b],E=G.E.slice(0,a).concat(H.E.slice(1).map(e=>e.map(w=>w+G.n)),[[u,G.n+x],[v,G.n+y]]);return graph(G.n+H.n,E)}
let pairs=[];for(let [h,d] of [[4,3],[8,9],[16,15],[32,31],[64,3]]){let {G,c}=ring(h,d),Y=join(G,Q),N=join(G,P);let color=q.witness[0],perm=z=>z===color?2:z===2?color:z,cy=c.slice(0,-1).concat(q.witness.slice(1).map(perm),[2,2]);verify(Y,cy);for(let H of [Y,N]){let cut=H.E.filter(([u,v])=>(u<G.n)!==(v<G.n));ok(cut.length===2);let seen=new Set([0]),todo=[0];for(let u of todo)for(let e of H.I[u]){let v=H.E[e][0]^H.E[e][1]^u;if(!seen.has(v)){seen.add(v);todo.push(v)}}ok(seen.size===H.n)}pairs.push({h,d,vertices:Y.n,YES:"verified",NO:"Petersen two-cut cap; all 15-edge colorings excluded by backtracking"})}
let recurrences=0;for(let m=2;m<=40;m++)for(let a=1;a<m;a++)for(let c=2;c<=6;c++){let M=BigInt(m),A=BigInt(a),B=BigInt(m-a),C=BigInt(c),p=M**(C-2n),q1=p/A**(C-2n),q2=p/B**(C-2n);ok(q1*A**C+q2*B**C<=M**C-1n);recurrences++}
return {checks,recurrences,petersenColorings:p.count,pentagonalPrismColorings:q.count,pairs}
};
console.log(JSON.stringify(audit(),null,2));

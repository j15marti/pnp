function audit(){
let seed=20261126, checks=0, flowCalls=0;
function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
function check(ok,msg){checks++;if(!ok)throw Error(msg)}
function rankcut(edges,S){return new Set(edges.filter(([a,b])=>S.has(a)!==S.has(b)).map(e=>e[2]).filter(x=>x>=0)).size}
function flow(n,edges,A,B,alpha,beta){
 flowCalls++; const labels=new Map();for(const [a,b,l] of edges){if(l<0)continue;if(!labels.has(l))labels.set(l,new Set());labels.get(l).add(a);labels.get(l).add(b)}
 const L=labels.size,src=n+2*L,snk=src+1,V=snk+1,g=Array.from({length:V},()=>[]);
 const inf=alpha*L+beta*n+1;
 function arc(a,b,c){g[a].push({b,c,rev:g[b].length});g[b].push({b:a,c:0,rev:g[a].length-1})}
 let j=0;for(const s of labels.values()){let i=n+2*j++,o=i+1;arc(i,o,alpha);for(const v of s){arc(v,i,inf);arc(o,v,inf)}}
 for(let i=0;i<n;i++)if(beta)arc(i,snk,beta);
 for(const a of A)arc(src,a,inf);for(const b of B)arc(b,snk,inf);
 let value=0,seen;
 while(true){let p=Array(V).fill(null),q=[src];p[src]=[-1,-1];for(let z=0;z<q.length&&!p[snk];z++){let a=q[z];for(let i=0;i<g[a].length;i++){let e=g[a][i];if(e.c>0&&!p[e.b]){p[e.b]=[a,i];q.push(e.b)}}}
 if(!p[snk]){seen=new Set(q.filter(v=>v<n));break}
 let d=inf;for(let v=snk;v!==src;){let [a,i]=p[v];d=Math.min(d,g[a][i].c);v=a}
 for(let v=snk;v!==src;){let [a,i]=p[v],e=g[a][i];e.c-=d;g[v][e.rev].c+=d;v=a}value+=d
 }
 check(A.every(x=>seen.has(x))&&B.every(x=>!seen.has(x)),"anchors");check(value===alpha*rankcut(edges,seen)+beta*seen.size,"flow objective");return {S:seen,value,r:rankcut(edges,seen)}
}
function allcuts(n,fn){for(let m=1;m<2**n-1;m++){let S=new Set();for(let i=0;i<n;i++)if(m&(1<<i))S.add(i);if(S.size>=2&&S.size<=n-2)fn(S)}}
function good(n,S,r,K){let u=Math.min(S.size,n-S.size)-1,mu=n-2;return (2n**BigInt(r))*(BigInt(u)**BigInt(K))<=BigInt(mu)**BigInt(K)}
function discover(n,edges,K){let mu=n-2;
 for(let u=1;u<=Math.floor(mu/2);u++)for(let r=0;r<=Math.floor(K*Math.log2(mu));r++){
 if((2n**BigInt(r))*BigInt(u)**BigInt(K)>BigInt(mu)**BigInt(K))continue;
 for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)for(let c=0;c<n;c++)if(c!==a&&c!==b)for(let d=c+1;d<n;d++)if(d!==a&&d!==b){
 let f=flow(n,edges,[a,b],[c,d],u,r);
 if(good(n,f.S,f.r,4*K))return f;
 }}
 return null
}
let synthetic={weighted:0,discovery:0,admitted:0,returned:0};
for(let t=0;t<120;t++){
 let n=4+rand(5),edges=[];for(let i=1;i<n;i++)edges.push([i,rand(i),i-1]);
 // each extra edge either new phase or attached to endpoint of one existing phase
 for(let j=0;j<6;j++){let e=edges[rand(edges.length)],a=e[rand(2)],b=rand(n);if(a!==b)edges.push([a,b,e[2]])}
 let order=Array.from({length:n},(_,i)=>i);for(let i=n-1;i>0;i--){let j=rand(i+1);[order[i],order[j]]=[order[j],order[i]]}
 let A=order.slice(0,2),B=order.slice(2,4),alpha=1+rand(6),beta=rand(6);
 let f=flow(n,edges,A,B,alpha,beta),best=Infinity;
 allcuts(n,S=>{if(A.every(x=>S.has(x))&&B.every(x=>!S.has(x)))best=Math.min(best,alpha*rankcut(edges,S)+beta*S.size)});
 check(f.value===best,"exhaustive objective");synthetic.weighted++;
 if(t<30){let admitted=false;allcuts(n,S=>{if(good(n,S,rankcut(edges,S),1))admitted=true});let out=discover(n,edges,1);check(!admitted||!!out,"missed admissible cut");if(out)check(good(n,out.S,out.r,4),"invalid expanded cut");synthetic.discovery++;synthetic.admitted+=+admitted;synthetic.returned+=+!!out}
}
let rec=0;
for(let mu=2;mu<=150;mu++)for(let u=1;u<=Math.floor(mu/2);u++)for(let K=1;K<=3;K++){
 let c=BigInt(4*K+2), U=BigInt(u), M=BigInt(mu),V=M-U;
 let r=0;while((2n**BigInt(r+1))*U**BigInt(4*K)<=M**BigInt(4*K))r++;
 check((2n**BigInt(r))*U**c+V**c<=M**c-1n,"recurrence");rec++;
}
function make(k,yes){
 let F=Array.from({length:4},()=>[]),n=18*k,w=Array(n);
 for(let q=0;q<2*k;q++){
 let off=9*q,phase=q%2;
 for(let y=0;y<3;y++)for(let x=0;x<3;x++)w[off+3*y+x]=y===0?phase:y===1?1-phase:(x===2?1:0);
 for(let y=0;y<3;y++)F[0].push([0,1,2].map(x=>off+3*y+x));
 for(let s=0;s<3;s++)for(let j=0;j<3;j++)F[s+1].push([0,1,2].map(y=>off+3*y+(j+s*y)%3));
 }
 function swap(i,j,p=0){let a=F[0][i],b=F[0][j];[a[p],b[p]]=[b[p],a[p]]}
 for(let i=0;i<k;i++){swap(6*i,6*i+3);if(yes||i!==0)swap(6*i+1,6*i+4)}
 for(let i=0;i<k-1;i++)swap(6*i+5,6*(i+1)+5);
 let pair=new Set();for(let P of F){let ids=P.flat();check(ids.length===n&&new Set(ids).size===n,"partition");for(let c of P){for(let a=0;a<3;a++)for(let b=a+1;b<3;b++){let key=[c[a],c[b]].sort((x,y)=>x-y).join(",");check(!pair.has(key),"linearity");pair.add(key)}}}
 let C=F.flat(),edges=[];C.forEach((c,i)=>c.forEach(x=>edges.push([x,n+i,x])));
 let adj=Array.from({length:n+C.length},()=>[]);for(let [a,b] of edges){adj[a].push(b);adj[b].push(a)}let q=[0],seen=new Set(q);for(let a of q)for(let b of adj[a])if(!seen.has(b)){seen.add(b);q.push(b)}check(seen.size===adj.length,"connected");
 if(yes)check(C.every(c=>!c.every(x=>w[x]===w[c[0]])),"source SAT witness");else{
 let core=C.filter(c=>c.every(x=>x<9));check(core.length===11,"NO core");for(let mask=0;mask<512;mask++)check(core.some(c=>c.every(x=>((mask>>x)&1)===((mask>>c[0])&1))),"NO exhaustive core")
 }
 // Anchor the first two and last two vertices, not a supplied decomposition.
 let f=flow(adj.length,edges,[0,1],[adj.length-2,adj.length-1],1,0);
 return {k,yes,n,m:C.length,anchoredMinRank:f.r,shore:f.S.size}
}
let sources=[];for(let k of [1,2,4,8,16])for(let yes of [true,false])sources.push(make(k,yes));
let wide=[];for(let n of [32,128,512,2048]){
 let edges=[],r=Math.floor(Math.log2(n-2));for(let i=0;i<r;i++)edges.push([0,2,i]);edges.push([0,1,r]);for(let i=3;i<n;i++)edges.push([2,i,r+1]);let f=flow(n,edges,[0,1],[2,3],1,r);
 check(f.r===r&&f.S.size===2,"wide");check(good(n,f.S,f.r,1),"wide recurrence");wide.push({vertices:n,rank:f.r,smallShore:f.S.size})
}
return {seed:20261126,checks,flowCalls,synthetic,recurrenceChecks:rec,sources,wide};
}
console.log(JSON.stringify(audit(), null, 2));

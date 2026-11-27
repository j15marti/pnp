function audit(){
const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
const mod=x=>(x%3+3)%3,pop=x=>{let n=0;for(;x;x&=x-1)n++;return n},sign=(a,z)=>pop(a&z)%2?2:1;
const row=F.map((_,e)=>F.reduce((r,t,j)=>r|(t.includes(e)?1<<j:0),0));
const words=[];for(let x=0;x<128;x++)if(row.every(r=>pop(x&r)%2===1))words.push(x);
const word=z=>words.find(x=>(x&1)===(z&1)&&(x>>3&1)===(z>>1&1)&&(x>>1&1)===(z>>2&1));
if(new Set(Array.from({length:8},(_,z)=>word(z))).size!==8)throw Error("chart");
function fourier(a){let n=a.length,inv=n%3===1?1:2;return a.map((_,u)=>mod(inv*a.reduce((s,v,z)=>s+v*sign(u,z),0)))}
function evalrow(a,z){return mod(a.reduce((s,v,u)=>s+v*sign(u,z),0))}
function basis(rows){let B=[];for(let a of rows){a=a.slice();for(let [i,b] of B){let v=a[i];a=a.map((x,j)=>mod(x-v*b[j]))}let i=a.findIndex(x=>x);if(i>=0){let q=a[i];B.push([i,a.map(x=>mod(q*x))])}}return B.map(x=>x[1])}
function project(coeff,b){let k=1<<b,rows=[];for(let i=0;i<coeff.length;i+=k)rows.push(coeff.slice(i,i+k));return basis(rows)}
function joint(A,B){let products=[],ops=0;for(let a of A)for(let b of B){let c=new Array(a.length).fill(0);for(let i=0;i<a.length;i++)if(a[i])for(let j=0;j<b.length;j++)if(b[j]){ops++;c[i^j]=mod(c[i^j]+a[i]*b[j])}products.push(c)}return {ops,basis:basis(products)}}
const support=(B,k)=>Array.from({length:k},(_,z)=>z).filter(z=>B.some(a=>evalrow(a,z)));
function hull(S){if(!S.length)return [];let a=S[0],H=new Set([0]);for(let z of S)for(let v of [...H])H.add(v^z^a);return [...H].map(x=>x^a).sort((a,b)=>a-b)}
const Arows=[3,5],Brows=[0,1,2,4,6],fn=J=>Array.from({length:8},(_,z)=>Number(J.every(e=>pop(word(z)&row[e])===1)));
const a=fn(Arows),b=fn(Brows),ac=fourier(a),bc=fourier(b),ap=project(ac,2),bp=project(bc,2),J=joint(ap,bp);
if(J.basis.length)throw Error("not refuted");
let seed=2527;function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
let checks=0,joinChecks=0,scalarLost=0;
for(let k=0;k<400;k++){let seam=1+(rand()%3),priv=1+(rand()%3),n=1<<(seam+priv),m=1<<seam;let f=Array.from({length:n},()=>Number((rand()>>>24)%4!==0)),g=Array.from({length:n},()=>Number((rand()>>>24)%3===0));let F=fourier(f),G=fourier(g),P=project(F,seam),Q=project(G,seam),C=joint(P,Q).basis;for(let z=0;z<m;z++){let s=f.some((v,i)=>v&&(i&(m-1))===z),t=g.some((v,i)=>v&&(i&(m-1))===z);if(Boolean(P.some(a=>evalrow(a,z)))!==s||Boolean(Q.some(a=>evalrow(a,z)))!==t)throw Error("projection");if(s&&!evalrow(F.slice(0,m),z))scalarLost++;if(Boolean(C.some(a=>evalrow(a,z)))!==(s&&t))throw Error("join");checks+=2;joinChecks++}}
const cancellation=[1,1,1,0],c=fourier(cancellation),cp=project(c,0);if(c[0]!==0||cp.length!==1)throw Error("modular control");
function graph(blocks){
let T=[];for(let i=0;i<blocks;i++)for(let j=0;j<7;j++)T.push(F[j].map(e=>7*((j===0&&e===0)?(i+1)%blocks:(j===3&&e===1)?(i+blocks-1)%blocks:i)+e));
let inc=Array.from({length:7*blocks},()=>[]);T.forEach((a,j)=>a.forEach(e=>inc[e].push(j)));
let center=[],groups=T.map(()=>[]),k=[],p=[],g=[],region=[],s=0;
for(let e=0;e<inc.length;e++){let c=s++,L=inc[e].map(()=>s++),d=s++,R=inc[e].map(()=>s++).reverse();center.push([c,d]);inc[e].forEach((j,i)=>groups[j].push(L[i],R[i]));L.forEach((a,i)=>{k[a]=R[i];k[R[i]]=a})}
for(let i=0;i<s;i++){p[i]=(i+1)%s;g[i]=i;if(k[i]===undefined)k[i]=i}
for(let [a,d] of center)[p[a],p[d]]=[p[d],p[a]];
groups.forEach((G,j)=>G.forEach((i,h)=>{g[i]=G[(h+1)%6];region[i]=j}));
const n=3*s,u=i=>s+i,v=i=>2*s+i,arcs=new Set(),seen=new Set(),adj=Array.from({length:n},()=>[]),rev=Array.from({length:n},()=>[]);
function add(i,j){let q=i*n+j;if(!arcs.has(q)){arcs.add(q);adj[i].push(j);rev[j].push(i)}}
for(let i=0;i<s;i++){add(i,u(i));add(u(i),v(i));add(v(i),p[i]);if(region[i]!==undefined){add(g[i],v(i));add(v(i),u(i));add(u(i),p[k[g[i]]])}}
function reach(a){let st=[0],v=new Set(st);for(let i=0;i<st.length;i++)for(let j of a[st[i]])if(!v.has(j)){v.add(j);st.push(j)}return v.size}
if(reach(adj)!==n||reach(rev)!==n)throw Error("not strong");
function lift(x){let P=new Int32Array(n).fill(-1);function put(i,j){if(P[i]!==-1||!arcs.has(i*n+j))throw Error("bad arc");P[i]=j;seen.add(i*n+j)}
for(let i=0;i<s;i++)if(region[i]!==undefined&&x[region[i]]){put(g[i],v(i));put(v(i),u(i));put(u(i),p[k[g[i]]])}else{put(i,u(i));put(u(i),v(i));put(v(i),p[i])}
let mark=new Uint8Array(n);for(let j of P){if(j<0||mark[j])throw Error("not permutation");mark[j]=1}mark.fill(0);let count=0;for(let i=0;i<n;i++)if(!mark[i]){count++;let j=i;while(!mark[j]){mark[j]=1;j=P[j]}}
let want=1+inc.reduce((a,I)=>a+Math.abs(I.reduce((c,j)=>c+x[j],0)-1),0);if(count!==want||count%2!==1)throw Error("cycle");return count}
let base=new Array(T.length).fill(1);lift(base);for(let j=1;j<T.length;j++){let x=base.slice();x[0]=x[j]=0;lift(x)}if(seen.size!==arcs.size)throw Error("arc support");
let exhaustive=0,projectionChecks=0;
if(blocks<=6)for(let z=0;z<2**(blocks+2);z++){let x=[];for(let i=0;i<blocks;i++){let y=word((z&3)|((z>>(i+2)&1)<<2));for(let j=0;j<7;j++)x.push(y>>j&1)}if(!inc.every(I=>I.reduce((c,j)=>c+x[j],0)%2===1))throw Error("odd");let test=(block,J)=>J.every(e=>inc[7*block+e].reduce((c,j)=>c+x[j],0)===1);if(test(0,Arows)!==Boolean(a[(z&3)|((z>>2&1)<<2)])||test(1,Brows)!==Boolean(b[(z&3)|((z>>3&1)<<2)]))throw Error("source region map");if(test(0,Arows)&&test(1,Brows))throw Error("joint");projectionChecks+=2;if(lift(x)===1)throw Error("HC");exhaustive++}
return {blocks,n,arcs:arcs.size,signLifts:T.length,exhaustive,projectionChecks,affineDimension:blocks+2,nominalWords:(2n**BigInt(blocks+2)).toString()}
}
return {words,local:{Arows,Brows,a,b,ac,bc,ap,bp,keysA:support(ap,4),keysB:support(bp,4),hullA:hull(support(ap,4)),hullB:hull(support(bp,4)),joint:J},random:{checks,joinChecks,scalarLost},cancellation:{word:cancellation,coefficients:c,projectedBasis:cp},scales:[3,6,12,24,48].map(graph)}
}
console.log(JSON.stringify(audit(),null,2));

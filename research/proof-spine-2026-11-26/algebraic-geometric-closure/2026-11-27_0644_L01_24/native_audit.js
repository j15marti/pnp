function nativeAudit(){
const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
const A=[];let pop=x=>{let n=0;while(x){n++;x&=x-1}return n};
const row=F.map((_,e)=>F.reduce((r,t,j)=>r|(t.includes(e)?1<<j:0),0));
for(let x=0;x<128;x++)if([2,3,4,5,6].every(e=>pop(x&row[e])%2))A.push(x);
if(!A.every(x=>row.every(r=>pop(x&r)%2)))throw Error("parity implication");
function h(S){if(!S.length)return[];let a=S[0],H=new Set([0]);for(let x of S)if(!H.has(x^a))for(let y of [...H])H.add(y^x^a);return [...H].map(x=>x^a).sort((a,b)=>a-b)}
let cur=A, trace=[];for(let J of [[0,1,2],[0,3,4],[5],[6]]){let S=cur.filter(x=>J.every(e=>pop(x&row[e])===1));let H=h(S);trace.push({J,prior:cur,attained:S,hull:H});cur=H}
if(cur.length)throw Error("not contradiction");
let pairChecks=0;for(let i=0;i<7;i++)for(let j=i+1;j<7;j++){if(h(A.filter(x=>[i,j].every(e=>pop(x&row[e])===1))).length!==8)throw Error("pair hull");pairChecks++}
function graph(b){
let T=[];for(let i=0;i<b;i++)for(let j=0;j<7;j++)T.push(F[j].map(e=>7*((j===0&&e===0)?(i+1)%b:(j===3&&e===1)?(i+b-1)%b:i)+e));
let m=7*b,t=T.length,inc=Array.from({length:m},()=>[]);T.forEach((a,j)=>a.forEach(e=>inc[e].push(j)));
let center=[], groups=Array.from({length:t},()=>[]),k=[],p=[],g=[],region=[],s=0;
function newPair(j){let a=s++,d=s++;return[a,d]}
// assign endpoints in circular order, then partner indices
s=0;for(let e=0;e<m;e++){let c=s++,L=inc[e].map(()=>s++),d=s++,R=inc[e].map(()=>s++).reverse();center.push([c,d]);inc[e].forEach((j,i)=>groups[j].push(L[i],R[i]));L.forEach((a,i)=>{k[a]=R[i];k[R[i]]=a})}
for(let i=0;i<s;i++){p[i]=(i+1)%s;g[i]=i;if(k[i]===undefined)k[i]=i}
for(let [a,d] of center){[p[a],p[d]]=[p[d],p[a]]}
for(let G of groups){if(G.length!==6)throw Error("group");G.forEach((i,j)=>{g[i]=G[(j+1)%6];region[i]=groups.indexOf(G)})}
const n=3*s, u=i=>s+i,v=i=>2*s+i;let arcs=new Set(),seen=new Set(),adj=Array.from({length:n},()=>[]),rev=Array.from({length:n},()=>[]);
function add(a,d){let key=a*n+d;if(arcs.has(key))return;arcs.add(key);adj[a].push(d);rev[d].push(a)}
for(let i=0;i<s;i++){add(i,u(i));add(u(i),v(i));add(v(i),p[i]);if(region[i]!==undefined){add(g[i],v(i));add(v(i),u(i));add(u(i),p[k[g[i]]])}}
function reach(a){let st=[0],v=new Set(st);for(let i=0;i<st.length;i++)for(let j of a[st[i]])if(!v.has(j)){v.add(j);st.push(j)}return v.size}
if(reach(adj)!==n||reach(rev)!==n)throw Error("not strong");
function lift(x,requireSign){let P=new Int32Array(n).fill(-1);function put(a,d){if(P[a]!==-1||!arcs.has(a*n+d))throw Error("bad lift");P[a]=d;seen.add(a*n+d)}
for(let i=0;i<s;i++){if(region[i]!==undefined&&x[region[i]]){put(g[i],v(i));put(v(i),u(i));put(u(i),p[k[g[i]]])}else{put(i,u(i));put(u(i),v(i));put(v(i),p[i])}}
let mark=new Uint8Array(n);for(let a of P){if(a<0||mark[a])throw Error("not permutation");mark[a]=1}mark.fill(0);let cycles=0;for(let i=0;i<n;i++)if(!mark[i]){cycles++;let j=i;while(!mark[j]){mark[j]=1;j=P[j]}}let want=1+inc.reduce((a,I)=>a+Math.abs(I.reduce((c,j)=>c+x[j],0)-1),0);if(cycles!==want||(requireSign&&cycles%2!==1))throw Error("cycle identity");return cycles}
let base=new Array(t).fill(1);lift(base,true);for(let j=1;j<t;j++){let x=base.slice();x[0]=x[j]=0;lift(x,true)}
let support=seen.size;if(support!==arcs.size)throw Error("unsupported");
let chartChecks=0;if(b<=6){for(let z=0;z<2**(b+2);z++){let x=[];for(let i=0;i<b;i++){let u=z&1,v=z>>1&1,w=z>>(i+2)&1;let y=A.find(x=>(x&1)===u&&(x>>3&1)===v&&(x>>1&1)===w);for(let j=0;j<7;j++)x.push(y>>j&1)}if(!inc.every(I=>I.reduce((c,j)=>c+x[j],0)%2===1))throw Error("not chart");if(lift(x,true)===1)throw Error("HC");chartChecks++}}
return {b,n,arcs:arcs.size,support,lifts:t,chartChecks}
}
return {localParityWords:A,pairChecks,trace,scales:[3,6,12,24,48].map(graph)}
}
console.log(JSON.stringify(nativeAudit(),null,2));

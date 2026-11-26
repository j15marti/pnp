function audit(){
const M=x=>((x%3)+3)%3, A=(x,m)=>{if(!x)throw Error(m)}, range=n=>Array.from({length:n},(_,i)=>i), stats={tables:0,subsets:0,recurrence:0,embeddings:0,nodes:0,cuts:{},cutScans:0,closure:0,matching:0,probes:0,terminals:0,terminalBranches:0,lifts:0}, results=[];
function masks(k){return range(1<<k).map(m=>range(k).map(i=>(m>>i)&1))}
for(let k=1;k<=3;k++)for(const sig of masks(k).map(a=>a.map(x=>x?1:-1)))for(let q=0;q<3;q++){
 const t=masks(k).filter(a=>M(a.reduce((s,x,i)=>s+x*sig[i],0))===q);stats.tables++;
 for(let b=1;b<(1<<t.length);b++){
 const s=t.filter((_,i)=>(b>>i)&1), pins=range(k).map(i=>s.every(a=>a[i]===s[0][i])?s[0][i]:-1);
 A(t.filter(a=>a.every((x,i)=>pins[i]<0||pins[i]===x)).length===s.length,"pin closure");stats.subsets++;
 }}
for(let a=2;a<=100;a++)for(let b=a;b<=200;b++){A(3n*BigInt(a+1)**5n+BigInt(b+1)**5n<BigInt(a+b)**5n,"recurrence");stats.recurrence++}
const sq=masks(4).filter(([a,p,b,q])=>p===q&&a+b+p===1);
A(sq.length===3,"square");for(const pair of [[0,1],[1,2]])A(new Set(sq.map(x=>M(x[pair[0]]*(pair[0]%2?-1:1)+x[pair[1]]*(pair[1]%2?-1:1)))).size===3,"three syndrome states");
function prism(n){let R={},K={};for(let l=0;l<2;l++)for(let i=0;i<n;i++){let v=l*n+i,pr=l*n+(i+n-1)%n,ne=l*n+(i+1)%n,ru=(1-l)*n+i;R[v]=l?[ne,pr,ru]:[pr,ne,ru];K[v]=(i+l)%2?"C":"V"}return{R,K}}
function fromR(r,n){let R={},K={};r.forEach((a,i)=>{R[i]=a.slice();K[i]=i<n?"V":"C"});return{R,K}}
const neg=fromR([[22,19,18],[13,16,21],[14,13,21],[18,13,14],[19,22,17],[16,19,23],[12,17,20],[12,20,15],[15,23,12],[16,14,21],[17,22,20],[23,15,18],[6,7,8],[3,1,2],[9,3,2],[7,11,8],[1,5,9],[4,10,6],[11,0,3],[5,0,4],[10,7,6],[2,1,9],[10,4,0],[8,11,5]],12);
const prior=fromR([[10,2,3],[4,1,16],[2,6,5],[3,9,0],[1,4,13],[5,3,2],[7,8,1],[9,5,6],[6,10,9],[8,7,12],[10,15,8],[14,17,11],[12,13,4],[13,12,7],[15,0,14],[11,15,14],[11,17,16],[16,17,0]].map(a=>a.map(x=>x+18)).concat([[32,21,35],[19,22,24],[18,20,23],[23,21,18],[30,22,19],[20,25,23],[25,20,26],[31,27,24],[24,27,28],[21,25,26],[26,18,28],[29,34,33],[27,31,30],[22,30,31],[32,29,33],[28,32,33],[34,35,19],[35,34,29]].map(a=>a.map(x=>x-18))),18);
// Historical rotation was indexed clauses first, variables second; above exchanges the halves.
function splice(src,c){let R=JSON.parse(JSON.stringify(src.R)),K={...src.K},off=Math.max(...Object.keys(R).map(Number))+1,B=prism(4);for(const [v,rs] of Object.entries(B.R)){R[off+Number(v)]=rs.map(x=>off+x);K[off+Number(v)]=B.K[v]}
let u=R[c].slice(),v=R[off].slice().reverse();for(let i=0;i<3;i++){R[u[i]]=R[u[i]].map(x=>x===c?v[i]:x);R[v[i]]=R[v[i]].map(x=>x===off?u[i]:x)}delete R[c];delete K[c];delete R[off];delete K[off];return{R,K}}
function make(src){const V=Object.keys(src.R).map(Number),E=[],R={},Q={},K={...src.K};let ids={};for(let u of V){A(src.R[u].length===3&&new Set(src.R[u]).size===3,"native degree");Q[u]=K[u]==="V"?0:2;for(let v of src.R[u]){A(src.R[v].includes(u)&&K[u]!==K[v],"native incidence");if(K[u]==="V"){let id=E.length;E.push({id,u,v});ids[u+","+v]=id;ids[v+","+u]=id}}}for(let u of V)R[u]=src.R[u].map(v=>ids[u+","+v]);return{V,E,R,Q,K,P:{}}}
const other=(e,u)=>e.u===u?e.v:e.u, sign=(e,u)=>e.u===u?1:-1;
function indexed(g){return Object.fromEntries(g.E.map(e=>[e.id,e]))}
function verify(g){const I=indexed(g),seen=new Set();let faces=0;for(let u of g.V){A(g.R[u].length<=3&&new Set(g.R[u]).size===g.R[u].length,"rotation degree");for(let id of g.R[u]){let e=I[id];A(e&&(e.u===u||e.v===u)&&e.u!==e.v&&g.R[other(e,u)].includes(id),"rotation reciprocal");let key=u+","+id;if(seen.has(key))continue;faces++;let v=u,j=id;do{let s=v+","+j;A(!seen.has(s),"face walk");seen.add(s);v=other(I[j],v);let r=g.R[v];j=r[(r.indexOf(j)+1)%r.length]}while(v!==u||j!==id)}}A(seen.size===2*g.E.length,"half edges");A(g.V.length-g.E.length+faces===2,"Euler");stats.embeddings++}
function check(g,p){return g.E.every(e=>p[e.id]===0||p[e.id]===1)&&Object.entries(g.P).every(([i,x])=>p[i]===x)&&g.V.every(u=>M(g.E.reduce((s,e)=>s+(e.u===u?p[e.id]:e.v===u?-p[e.id]:0),0))===g.Q[u])}
function put(p,id,x){if(p[id]!==undefined)return p[id]===x;p[id]=x;return true}
function closure(g,p0){stats.closure++;let p={...p0},I=indexed(g);
while(true){let before=Object.keys(p).length;
 for(let u of g.V){let r=g.R[u],t=masks(r.length).filter(a=>M(a.reduce((s,x,i)=>s+x*sign(I[r[i]],u),0))===g.Q[u]&&a.every((x,i)=>p[r[i]]===undefined||p[r[i]]===x));if(!t.length)return null;for(let i=0;i<r.length;i++)if(t.every(a=>a[i]===t[0][i]))p[r[i]]=t[0][i]}
 // Exact GF(3) residual feasibility: incidence columns span zero-sum vectors per unknown-edge component.
 let rem=Object.fromEntries(g.V.map(u=>[u,g.Q[u]]));for(let e of g.E)if(p[e.id]!==undefined){rem[e.u]=M(rem[e.u]-p[e.id]);rem[e.v]=M(rem[e.v]+p[e.id])}
 let vis=new Set();for(let u of g.V)if(!vis.has(u)){let stack=[u],sum=0;vis.add(u);while(stack.length){let v=stack.pop();sum+=rem[v];for(let id of g.R[v])if(p[id]===undefined){let w=other(I[id],v);if(!vis.has(w)){vis.add(w);stack.push(w)}}}if(M(sum)!==0)return null}
 // Clause-slot matching relaxation on surviving native clause vertices, private slots for cap endpoints.
 stats.matching++;let owner={},rows=g.V.filter(u=>g.K[u]==="C"&&!g.R[u].some(id=>p[id]===1));
 function augment(u,seen){for(let id of g.R[u])if(p[id]!==0){let v=other(I[id],u),slots=g.K[v]==="V"?[v+":0",v+":1",v+":2"]:["e:"+id];for(let s of slots)if(!seen.has(s)){seen.add(s);if(owner[s]===undefined||augment(owner[s],seen)){owner[s]=u;return true}}}return false}
 if(rows.some(u=>!augment(u,new Set())))return null;
 if(Object.keys(p).length===before)return p;
 }}
function close(g,p){let q=closure(g,p);if(!q)return null; // all opposite-value probes on small residuals; large residuals use base closure.
 if(g.V.length<=26){let change=true;while(change){change=false;for(let e of g.E)if(q[e.id]===undefined){stats.probes+=2;let a=closure(g,{...q,[e.id]:0}),b=closure(g,{...q,[e.id]:1});if(!a&&!b)return null;if(!a||!b){q=a||b;change=true;break}}}}
 return q}
function cut(g){let I=indexed(g),best=null;function scan(skip){stats.cutScans++;let time=0,dis={},low={},par={},order=[],ends={},bridges=[];function dfs(u,pe){dis[u]=low[u]=time++;order.push(u);for(let id of g.R[u])if(id!==pe&&!skip.has(id)){let v=other(I[id],u);if(dis[v]===undefined){par[v]=id;dfs(v,id);low[u]=Math.min(low[u],low[v]);if(low[v]>dis[u])bridges.push(v)}else low[u]=Math.min(low[u],dis[v])}ends[u]=time}
 dfs(g.V[0],-1);if(order.length!==g.V.length)return null;
 for(let v of bridges){let s=order.slice(dis[v],ends[v]);if(s.length<2||g.V.length-s.length<2)continue;let S=new Set(s),boundary=g.E.filter(e=>S.has(e.u)!==S.has(e.v)).map(e=>e.id);if(boundary.length<=3){if(s.length>g.V.length-s.length)S=new Set(g.V.filter(x=>!S.has(x)));return{S,boundary}}}return null}
 if((best=scan(new Set())))return best;
 for(let e of g.E)if((best=scan(new Set([e.id]))))return best;
 for(let i=0;i<g.E.length;i++)for(let j=0;j<i;j++)if((best=scan(new Set([g.E[i].id,g.E[j].id]))))return best;
 return null}
function cap(g,S,p){let I=indexed(g),O=g.V.filter(u=>!S.has(u)),capid=Math.max(...g.V)+1,member=Object.fromEntries(O.map(u=>[u,u])),rr=Object.fromEntries(O.map(u=>[u,g.R[u].slice()]));
 for(let e of g.E)if(!S.has(e.u)&&!S.has(e.v)){let a=member[e.u],b=member[e.v];if(a===b)continue;let x=rr[a],y=rr[b],ix=x.indexOf(e.id),iy=y.indexOf(e.id);A(ix>=0&&iy>=0,"contract");rr[a]=x.slice(ix+1).concat(x.slice(0,ix),y.slice(iy+1),y.slice(0,iy));for(let u of O)if(member[u]===b)member[u]=a;delete rr[b]}
 A(Object.keys(rr).length===1,"connected complement");let E=g.E.filter(e=>S.has(e.u)||S.has(e.v)).map(e=>({...e,u:S.has(e.u)?e.u:capid,v:S.has(e.v)?e.v:capid})),ids=new Set(E.map(e=>e.id)),R=Object.fromEntries([...S].map(u=>[u,g.R[u].slice()]));R[capid]=Object.values(rr)[0].filter(id=>ids.has(id));let Q=Object.fromEntries([...S].map(u=>[u,g.Q[u]]));Q[capid]=M(O.reduce((s,u)=>s+g.Q[u],0));let K=Object.fromEntries([...S].map(u=>[u,g.K[u]]));K[capid]="A";return{V:[...S,capid],E,R,Q,K,P:Object.fromEntries(Object.entries(p).filter(([id])=>ids.has(Number(id))))}}
function terminal(g,p){stats.terminals++;if(g.V.length>30)return undefined;function rec(x){stats.terminalBranches++;let q=closure(g,x);if(!q)return null;let e=g.E.find(e=>q[e.id]===undefined);if(!e){A(check(g,q),"terminal lift");return q}return rec({...q,[e.id]:0})||rec({...q,[e.id]:1})}return rec(p)}
function solve(g){stats.nodes++;verify(g);let p=close(g,g.P);if(!p)return null;if(g.E.every(e=>p[e.id]!==undefined)){A(check(g,p),"closure lift");return p}
 let c=cut(g);if(!c)return terminal(g,p);let {S,boundary:B}=c, O=new Set(g.V.filter(u=>!S.has(u)));stats.cuts[B.length]=(stats.cuts[B.length]||0)+1;
 A(3n*BigInt(S.size+1)**5n+BigInt(O.size+1)**5n<BigInt(g.V.length)**5n,"charged split");
 let small=cap(g,S,p),large=cap(g,O,p),I=indexed(small),u=small.V[small.V.length-1],t=masks(B.length).filter(a=>M(a.reduce((s,x,i)=>s+x*sign(I[B[i]],u),0))===small.Q[u]&&a.every((x,i)=>p[B[i]]===undefined||p[B[i]]===x));A(t.length<=3,"mask budget");let yes=[];
 for(let a of t){let P={...small.P};B.forEach((id,i)=>P[id]=a[i]);let x=solve({...small,P});if(x===undefined)return undefined;if(x)yes.push({a,x})}
 if(!yes.length)return null;let P={...large.P};for(let i=0;i<B.length;i++)if(yes.every(y=>y.a[i]===yes[0].a[i]))P[B[i]]=yes[0].a[i];A(t.filter(a=>a.every((x,i)=>P[B[i]]===undefined||P[B[i]]===x)).length===yes.length,"exact acquired cap");
 let z=solve({...large,P});if(z===undefined||z===null)return z;let y=yes.find(y=>B.every((id,i)=>z[id]===y.a[i]));A(y,"joint mask");let x={...y.x,...z};A(check(g,x),"original lift");stats.lifts++;return x}
function reference(g){let vs=g.V.filter(u=>g.K[u]==="V");A(vs.length<=18,"ref size");for(let a of masks(vs.length)){let p={};vs.forEach((u,i)=>g.R[u].forEach(id=>p[id]=a[i]));if(check(g,p))return true}return false}
for(const [name,seed,label] of [["SAT",prism(12),true],["UNSAT",neg,false]]){
 let src=seed;for(let k of range(9)){if([0,1,2,4,8].includes(k)){let g=make(src);let n=g.V.length/2;let b={...stats.cuts},z=solve(g);A(z!==undefined&&!!z===label,"family label");if(n<=18)A(reference(g)===label,"reference");results.push({name,k,n,answer:!!z,cuts:Object.fromEntries(Object.entries(stats.cuts).map(([j,v])=>[j,v-(b[j]||0)]))})}if(k<8){let c=Math.max(...Object.keys(src.K).filter(u=>src.K[u]==="C").map(Number));src=splice(src,c)}}
}
let gp=make(prior),z=solve(gp);A(z&&reference(gp),"historical SAT");results.push({name:"P1AB06 same source",n:18,answer:!!z});
let prime=make(prism(18));verify(prime);A(cut(prime)===null,"prime control");results.push({name:"prism prime",n:18,answer:"OPEN by cap terminal",nontrivialBond:false});
return{stats,results,square:sq}}
console.log(JSON.stringify(audit(),null,2));

// C08-13 independent interleaved replicas. node audit.js
function audit(){
let seed=20261126,checks=0;
function ok(t,msg){checks++;if(!t)throw Error(msg||"check "+checks)}
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
function shuffle(a){for(let i=a.length-1;i>0;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
const AG=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]];
const FANO=[[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
const bit=(w,i)=>(w>>>i)&1;
function nae(c,x){let a=x[c[0][0]]^c[0][1];return c.some(([v,s])=>(x[v]^s)!==a)}
const valid=(C,x)=>C.every(c=>nae(c,x));
const pos=C=>C.map(c=>c.map(v=>[v,0]));
function auth(F,n){ok(F.length===4);let seen=new Set;for(const p of F){let d=Array(n).fill(0);for(const c of p){ok(c.length===3&&new Set(c).size===3);for(const v of c){ok(v>=0&&v<n);d[v]++}for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let q=Math.min(c[i],c[j])*n+Math.max(c[i],c[j]);ok(!seen.has(q));seen.add(q)}}ok(d.every(v=>v===1))}}
function ring(k,no){let F=[[],[],[],[]];for(let b=0;b<k;b++)for(let j=0;j<4;j++)for(let i=0;i<3;i++){let c=AG[j][i].map(v=>9*b+v);if(j===0&&(i===0||(!no&&i===1)))c[2]=9*((b+1)%k)+AG[j][i][2];F[j].push(c)}return F}
function connected(C,n){let a=Array.from({length:n},()=>[]);for(let c of C)for(let i=1;i<c.length;i++){let u=c[0][0],v=c[i][0];a[u].push(v);a[v].push(u)}let q=[0],s=new Set(q);for(let i=0;i<q.length;i++)for(let v of a[q[i]])if(!s.has(v)){s.add(v);q.push(v)}return s.size===n}
function localTable(C,V,B){let id=new Map(V.map((v,i)=>[v,i])),D=C.map(c=>c.map(([v,s])=>[id.get(v),s])),M=new Map(),models=0;for(let w=0;w<2**V.length;w++){let x=V.map((_,i)=>bit(w,i));if(!valid(D,x))continue;models++;let y=B.reduce((a,v,i)=>a+2**i*x[id.get(v)],0);if(!M.has(y))M.set(y,x)}return{models,M}}
function compile(F,n){let C=[];for(let v=0;v<n;v++){for(let s of [0,7])for(let c of FANO)C.push(c.map(u=>[14*v+s+u,0]));C.push([[14*v+2,0],[14*v+9,1]])}let ports=[0,1,7,8];for(let j=0;j<4;j++)for(let c of F[j])C.push(c.map(v=>[14*v+ports[j],0]));let perm=shuffle(Array.from({length:14*n},(_,i)=>i));C=shuffle(C.map(c=>shuffle(c.map(([v,s])=>[perm[v],s]))));return{C,perm}}
function matchRoots(C,n,P){
let allowed=new Uint8Array(n).fill(1);for(let v of P)allowed[v]=0;
let adj=C.map(c=>[...new Set(c.map(p=>p[0]))]),mv=new Int32Array(n).fill(-1),mc=new Int32Array(C.length).fill(-1),visC=new Int32Array(C.length),visV=new Int32Array(n),pred=new Int32Array(n),stamp=0,scans=0;
function augment(root){stamp++;let q=[root];visC[root]=stamp;for(let i=0;i<q.length;i++){let c=q[i];for(let v of adj[c]){scans++;if(!allowed[v]||visV[v]===stamp)continue;visV[v]=stamp;pred[v]=c;if(mv[v]<0){let u=v;while(u>=0){let a=pred[u],old=mc[a];mc[a]=u;mv[u]=a;u=old}return true}let a=mv[v];if(visC[a]!==stamp){visC[a]=stamp;q.push(a)}}}return false}
let r=0;for(let c=0;c<C.length;c++)if(augment(c))r++;allowed.fill(1);let total=r;for(let c=0;c<C.length;c++)if(mc[c]<0&&augment(c))total++;
ok(total===C.length,"Hall full");let roots=[];for(let v=0;v<n;v++)if(mv[v]<0)roots.push(v);let kept=P.filter(v=>mv[v]<0),deg=Array(n).fill(0);for(let c of C)for(let [v] of c)deg[v]++;let positions=P.reduce((a,v)=>a+deg[v],0);ok(P.length-kept.length===C.length-r);ok(kept.length>=P.length-Math.floor(positions/3));
let rev=Array.from({length:n},()=>[]);for(let c=0;c<C.length;c++){let u=mc[c],su=C[c].find(p=>p[0]===u)[1];for(let [v,s] of C[c])if(v!==u)rev[v].push([u,1^su^s])}
let dist=new Int32Array(n).fill(-1),par=new Int32Array(n).fill(-1),sg=new Uint8Array(n),q=roots.slice();for(let v of q)dist[v]=0;for(let i=0;i<q.length;i++){let v=q[i];for(let [u,s] of rev[v])if(dist[u]<0){dist[u]=dist[v]+1;par[u]=v;sg[u]=s;q.push(u)}}ok(q.length===n,"unreached: regular closed component");
function extend(f){let x=Array(n).fill(0);for(let v of roots)x[v]=f(v);for(let u of q)if(par[u]>=0)x[u]=x[par[u]]^sg[u];ok(valid(C,x));for(let v of roots)ok(x[v]===f(v));return x}
return{kept,roots,r,positions,scans,extend}
}
function extract(C,n){let T=Array.from({length:n},()=>[]),binary=[];C.forEach((c,i)=>{if(c.length===2)binary.push(i);else for(let [v] of c)T[v].push(i)});let blocks=[],phase=Array(n).fill(-1),used=new Set,links=[];
for(let i of binary){let lr=[];for(let [p,s] of C[i]){ok(T[p].length===2);let I=[...new Set(T[p].flatMap(j=>C[j].map(a=>a[0])).filter(v=>v!==p))];ok(I.length===4);let owners=[...new Set(I.flatMap(v=>T[v]))];ok(owners.length===6&&owners.every(j=>!used.has(j)));let V=[...new Set(owners.flatMap(j=>C[j].map(a=>a[0])))].sort((a,b)=>a-b),B=V.filter(v=>owners.filter(j=>C[j].some(a=>a[0]===v)).length===2);ok(V.length===7&&B.length===3&&B.includes(p));ok(V.every(v=>phase[v]<0));let tab=localTable(owners.map(j=>C[j]),V,B);ok(tab.M.size===2&&tab.M.has(0)&&tab.M.has(7)&&tab.models===10);let k=blocks.length;blocks.push({V,B,tab});V.forEach(v=>phase[v]=k);owners.forEach(j=>used.add(j));lr.push([k,s])}links.push(lr)}
ok(phase.every(k=>k>=0));let clauses=C.filter((c,i)=>c.length===3&&!used.has(i)).map(c=>c.map(([v,s])=>[phase[v],s]));let partner=Array(blocks.length).fill(-1),pol=Array(blocks.length),root=Array(blocks.length).fill(-1),nr=0;for(let [[a,s],[b,t]] of links){ok(partner[a]<0&&partner[b]<0);partner[a]=b;partner[b]=a;root[a]=root[b]=nr++;pol[a]=0;pol[b]=1^s^t}ok(root.every(v=>v>=0));let Q=clauses.map(c=>c.map(([v,s])=>[root[v],s^pol[v]]));
function lift(z){let x=Array(n);for(let b=0;b<blocks.length;b++){let B=blocks[b],w=B.tab.M.get((z[root[b]]^pol[b])?7:0);B.V.forEach((v,i)=>x[v]=w[i])}ok(valid(C,x));return x}
return{Q,nr,blocks:blocks.length,lift}
}
function eliminate(C,n,cap=14){let F=C.map(c=>({v:c.map(p=>p[0]),t:Array.from({length:8},(_,w)=>w).filter(w=>{let x=c.map((p,i)=>bit(w,i)^p[1]);return x.includes(0)&&x.includes(1)})})),active=new Set(Array.from({length:n},(_,i)=>i)),hist=[],width=0;
function at(f,id,w){let a=0;for(let i=0;i<f.v.length;i++)a+=2**i*bit(w,id.get(f.v[i]));return f.t.includes(a)}
while(active.size){let best=null;for(let v of active){let L=F.filter(f=>f.v.includes(v)),S=[...new Set(L.flatMap(f=>f.v))].filter(u=>u!==v);if(!best||S.length<best.S.length)best={v,L,S};if(!S.length)break}let{v,L,S}=best;width=Math.max(width,S.length);if(width>cap)return{status:"UNKNOWN",width};let id=new Map(S.map((u,i)=>[u,i]));id.set(v,S.length);let tab=[],wit=new Map;for(let w=0;w<2**S.length;w++)for(let b of [0,1]){if(L.every(f=>at(f,id,w+b*2**S.length))){tab.push(w);wit.set(w,b);break}}if(!tab.length)return{status:"UNSAT",width};F=F.filter(f=>!L.includes(f));if(S.length&&tab.length!==2**S.length)F.push({v:S,t:tab});hist.push({v,S,wit});active.delete(v)}
let x=Array(n);for(let {v,S,wit} of hist.reverse()){let w=S.reduce((a,u,i)=>a+2**i*x[u],0);x[v]=wit.get(w);ok(x[v]!==undefined)}ok(valid(C,x));return{status:"SAT",width,x}
}
let capTable=localTable(pos(FANO),Array.from({length:7},(_,i)=>i),[0,1,2]);ok(capTable.models===10&&capTable.M.size===2&&capTable.M.has(0)&&capTable.M.has(7));
let L=pos(FANO.concat(FANO.map(c=>c.map(v=>v+7)))),B=[0,1,7,8],V=Array.from({length:14},(_,i)=>i);
let open=localTable(L,V,B),closed=localTable(L.concat([[[2,0],[9,1]]]),V,B);ok(open.models===100&&open.M.size===4&&closed.models===50&&closed.M.size===2&&closed.M.has(0)&&closed.M.has(15));let root=matchRoots(L,14,B);ok(root.kept.length===2);for(let w=0;w<4;w++){let a=new Map(root.kept.map((v,i)=>[v,bit(w,i)]));let x=root.extend(v=>a.get(v)||0);ok(root.kept.every(v=>x[v]===a.get(v)))}
let random={gadgets:0,profiles:0,maxFree:0};for(let z=0;z<240;z++){let n=5+rnd(6),C=[],d=Array(n).fill(0);for(let j=0;j<n*5;j++){let V=shuffle(Array.from({length:n},(_,i)=>i).filter(v=>d[v]<3));if(V.length<3)break;let c=V.slice(0,3);if(rnd(5)===0)continue;c.forEach(v=>d[v]++);C.push(c.map(v=>[v,rnd(2)]));if(C.length>=n-1)break}if(!connected(C,n))continue;let P=Array.from({length:n},(_,i)=>i).filter(v=>d[v]<=2);if(!P.length)continue;let A=matchRoots(C,n,P),tab=localTable(C,Array.from({length:n},(_,i)=>i),A.kept);ok(tab.M.size===2**A.kept.length);for(let w=0;w<2**A.kept.length;w++){let M=new Map(A.kept.map((v,i)=>[v,bit(w,i)]));let x=A.extend(v=>M.get(v)||0);ok(A.kept.every(v=>x[v]===M.get(v)));random.profiles++}random.gadgets++;random.maxFree=Math.max(random.maxFree,A.kept.length)}
let tests=[];for(let k of [2,4,8,16,32])for(let no of [false,true]){let n=9*k,F=ring(k,no);auth(F,n);ok(connected(pos(F.flat()),n));let {C,perm}=compile(F,n),N=14*n;ok(C.length===43*n/3);ok(connected(C,N));let deg=Array(N).fill(0),binary=C.filter(c=>c.length===2),T=C.filter(c=>c.length===3);for(let c of C)for(let [v] of c)deg[v]++;ok(deg.every(d=>d===3)&&binary.length===n&&T.length===40*n/3);
// Replica A: exact geometric cap extraction; no compiler labels or target.
let q=extract(C,N);ok(q.nr===n&&q.blocks===2*n&&q.Q.length===4*n/3);
// Replica B: delete short links only as a relaxation, acquire matching and independent root assignments.
let P=binary.flatMap(c=>c.map(p=>p[0]));let r=matchRoots(T,N,P);ok(r.kept.length>=Math.ceil(2*n/3));for(let j=0;j<3;j++){let x=r.extend(v=>j===0?0:j===1?1:v%2);ok(valid(T,x))}
let v=r.extend(()=>0);let violations=binary.filter(c=>!nae(c,v)).length;
// Replica C: independent source classification certificate, not a large brute-force solver.
if(no){let core=F.flat().filter(c=>c.every(v=>v<9));ok(core.length===11);let a=localTable(pos(core),Array.from({length:9},(_,i)=>i),[]);ok(a.models===0)}else{let x=Array.from({length:n},(_,v)=>{let b=Math.floor(v/9),s=v%9;return s<3?b%2:s<6?1^(b%2):s===8?1:0});ok(valid(pos(F.flat()),x))}
// Integrated: import exact cap identities, retain the binary equations, contract them, solve the resulting actual quotient and lift.
let a=eliminate(q.Q,q.nr);ok(a.status===(no?"UNSAT":"SAT"));if(a.x)q.lift(a.x);tests.push({sourceVars:n,compiledVars:N,ternary:T.length,binary:binary.length,deficiency:C.length-N,unmatchedPorts:r.kept.length,matchingScans:r.scans,relaxationBinaryViolations:violations,width:a.width,status:a.status})}
return{seed:20261126,checks,capModels:capTable.models,unlinkedModels:open.models,unlinkedPortWords:[...open.M.keys()].sort((a,b)=>a-b),linkedModels:closed.models,linkedPortWords:[...closed.M.keys()].sort((a,b)=>a-b),random,tests};
}
console.log(JSON.stringify(audit(),null,2));

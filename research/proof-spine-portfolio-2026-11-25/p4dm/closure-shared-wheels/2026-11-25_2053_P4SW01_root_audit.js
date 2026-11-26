// P4SW01 exact reproducible reference audit. Node.js, no dependencies.
function audit(){
const Q=[];for(let i=0;i<16;i++){const t=[0,1,2,3].map(c=>(i>>c)&1);if(t.reduce((a,b)=>a+b,0)===2)Q.push(t)}
const U=[[3,5,0,0],[2,0,4,2],[1,1,2,2],[0,5,1,3],[1,4,2,4],[5,0,4,5],[3,2,5,0],[0,4,2,2],[5,3,4,1],[4,2,0,0],[4,2,5,1],[0,4,1,4],[5,3,3,5],[2,1,3,3],[3,3,5,3],[2,0,3,5],[4,5,0,1],[1,1,1,4]];
const V=[[0,0,5,1],[0,1,0,1],[0,1,1,0],[1,0,0,1],[1,0,1,0],[1,1,0,0],[2,2,3,3],[2,3,2,3],[2,4,3,2],[3,2,2,3],[3,2,3,2],[3,3,2,2],[4,3,5,5],[4,5,4,5],[4,5,5,4],[5,4,4,5],[5,4,1,4],[5,5,4,4]];
const W=U.map(t=>t.slice());[W[1][3],W[14][3]]=[W[14][3],W[1][3]];
let assertions=0, matchingCalls=0, searchNodes=0, pinUpdates=0;
function ok(x,msg){assertions++;if(!x)throw Error(msg||"assert")}
const tn=i=>"t"+i,en=(c,a)=>"e"+c+":"+a;
function graph(T){const adj=new Map, E=[];function add(a,b){if(!adj.has(a))adj.set(a,[]);adj.get(a).push(b)}
for(let t=0;t<T.length;t++)for(let c=0;c<4;c++){const a=tn(t),b=en(c,T[t][c]);E.push({t,c,a,b});add(a,b);add(b,a)}
return {adj,E,vs:[...adj.keys()]}}
function groups(T){const g=new Map;for(let j=0;j<T.length;j++)for(let c=0;c<4;c++){const e=en(c,T[j][c]);if(!g.has(e))g.set(e,[]);g.get(e).push(j)}return g}
function valid(T,distinct=true){const g=groups(T);ok(T.every(t=>t.length===4&&t.every(v=>v!==null&&v!==undefined)),"tuple");ok(!distinct||new Set(T.map(t=>JSON.stringify(t))).size===T.length,"distinct");ok([...g.values()].every(a=>a.length===3),"E3");for(let c=0;c<4;c++)ok(new Set(T.map(t=>t[c])).size*3===T.length,"balance")}
function witness(T,p,pins={}){return p!==null&&[...groups(T).values()].every(a=>a.reduce((s,j)=>s+p[j],0)===1)&&Object.entries(pins).every(([j,v])=>p[j]===v)}
function addPin(p,j,v){if(p[j]!==-1&&p[j]!==v)return false;if(p[j]===-1){p[j]=v;pinUpdates++}return true}
function exactOne(g,p){let change=true;while(change){change=false;for(const a of g.values()){const yes=a.filter(j=>p[j]===1),free=a.filter(j=>p[j]===-1);if(yes.length>1||(!yes.length&&!free.length))return false;if(yes.length===1){for(const j of free){p[j]=0;pinUpdates++;change=true}}else if(free.length===1){p[free[0]]=1;pinUpdates++;change=true}}}return true}
function pairMatch(T,p,a,b,force=-1){matchingCalls++;const chosen=[];for(let j=0;j<T.length;j++)if(p[j]===1||j===force)chosen.push(j);
const L=new Set(T.map(t=>t[a])),R=new Set(T.map(t=>t[b]));for(const j of chosen){if(!L.delete(T[j][a])||!R.delete(T[j][b]))return false}
const A=new Map([...L].map(v=>[v,[]]));for(let j=0;j<T.length;j++)if(p[j]===-1&&j!==force&&L.has(T[j][a])&&R.has(T[j][b]))A.get(T[j][a]).push(T[j][b]);
const M=new Map;function aug(u,seen){for(const v of A.get(u)||[]){if(seen.has(v))continue;seen.add(v);if(!M.has(v)||aug(M.get(v),seen)){M.set(v,u);return true}}return false}
for(const u of L)if(!aug(u,new Set))return false;return M.size===R.size}
function close(T,g,p){while(true){if(!exactOne(g,p))return false;let changed=false;outer:for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){if(!pairMatch(T,p,a,b))return false;for(let j=0;j<T.length;j++)if(p[j]===-1&&!pairMatch(T,p,a,b,j)){p[j]=0;pinUpdates++;changed=true;break outer}}if(!changed)return true}}
function solve(T,pins={},full=true){const g=groups(T),p=Array(T.length).fill(-1);for(const [j,v] of Object.entries(pins))if(!addPin(p,+j,v))return null;
function rec(p){searchNodes++;if(!(full?close(T,g,p):exactOne(g,p)))return null;let best=null;for(const a of g.values())if(!a.some(j=>p[j]===1)){const free=a.filter(j=>p[j]===-1);if(best===null||free.length<best.length)best=free}
if(best===null){const out=p.map(v=>v===1?1:0);ok(witness(T,out,pins),"leaf witness");return out}for(const j of best){const q=p.slice();q[j]=1;const w=rec(q);if(w!==null)return w}return null}return rec(p)}
function connected(G,S){if(!S.size)return false;const seen=new Set,stack=[[...S][0]];while(stack.length){const v=stack.pop();if(seen.has(v))continue;seen.add(v);for(const w of G.adj.get(v))if(S.has(w)&&!seen.has(w))stack.push(w)}return seen.size===S.size}
function cut(G,S){return G.E.filter(e=>S.has(e.a)!==S.has(e.b))}
function type(C,S){const d=[0,0,0,0],count=[0,0,0,0];for(const e of C){d[e.c]+=S.has(e.a)?1:-1;count[e.c]++}const signs=C.map(e=>S.has(e.a)?1:-1);
if(C.length===2&&count.includes(2)&&d.every(v=>v===0))return "2-pair";
if(C.length===3&&count.includes(3)&&signs.every(v=>v===signs[0]))return "3-mono";
if(C.length===4&&count.every(v=>v===1)&&signs.every(v=>v===signs[0]))return "4-rainbow";
if(C.length===4&&d.every(v=>v===0)&&count.filter(v=>v===2).length===2)return "4-two-pairs";
if(C.length===4&&d.every(v=>v===0)&&count.includes(4))return "4-one-color";
return "invalid"}
function envelope(C,S,mask,typ){const b=C.map((_,i)=>(mask>>i)&1);if(typ==="2-pair"||typ==="4-rainbow")return b.every(v=>v===b[0]);
if(typ==="3-mono")return b.reduce((a,v)=>a+v,0)===1;
const z=[0,0,0,0];C.forEach((e,i)=>z[e.c]+=(S.has(e.a)?1:-1)*b[i]);return z.every(v=>v===0)}
function localMasks(T,G,S,C,pins={}){const I=T.map((_,j)=>j).filter(j=>S.has(tn(j)));ok(I.length<=20,"local enumeration cap");const out=new Set;for(let bm=0;bm<(1<<C.length);bm++)for(let w=0;w<(1<<I.length);w++){const p=new Map(I.map((j,i)=>[j,(w>>i)&1]));if(I.some(j=>j in pins&&p.get(j)!==pins[j]))continue;if(C.some((e,i)=>S.has(e.a)&&p.get(e.t)!==((bm>>i)&1)))continue;
let good=true;for(const e of S)if(e.startsWith("e")){let s=0;for(const t of G.adj.get(e))if(S.has(t))s+=p.get(+t.slice(1));else{const i=C.findIndex(q=>q.b===e&&q.a===t);s+=(bm>>i)&1}if(s!==1){good=false;break}}if(good){out.add(bm);break}}return out}
function cap(T,G,S,C,typ,pins={}){const idx=new Map, R=[],p={},port=Array(C.length).fill(-1);for(let j=0;j<T.length;j++)if(S.has(tn(j))){idx.set(j,R.length);R.push(T[j].map((v,c)=>S.has(en(c,v))?v:null));if(j in pins)p[R.length-1]=pins[j]}
const used=new Set(T.flat().map(String));let seq=0;function fresh(){while(used.has("@cap"+seq))seq++;const x="@cap"+seq++;used.add(x);return x}
const out=C.map(e=>S.has(e.a));function put(i,v){const e=C[i],k=idx.get(e.t);ok(k!==undefined,"out tuple");R[k][e.c]=v;port[i]=k}
if(typ==="2-pair"){const a=out.indexOf(true),b=1-a;put(a,T[C[b].t][C[b].c]);port[b]=port[a]}
else if(typ==="3-mono"&&out[0]){const v=fresh();C.forEach((e,i)=>put(i,v))}
else if(typ==="3-mono"){const c=C[0].c, labels=Array.from({length:4},()=>[fresh(),fresh()]);let k=0;for(const q of Q){const r=q.map((v,i)=>labels[i][v]);if(q[c]===0){const e=C[k];r[c]=T[e.t][c];port[k++]=R.length}R.push(r)}ok(k===3,"mono cap")}
else if(typ==="4-rainbow"&&out[0]){const labels=Array.from({length:4},()=>[fresh(),fresh()]),q0=Q[0];for(const q of Q.slice(1))R.push(q.map((v,i)=>labels[i][v]));C.forEach((e,i)=>put(i,labels[e.c][q0[e.c]]))}
else if(typ==="4-rainbow"){const r=Array(4);C.forEach((e,i)=>{r[e.c]=T[e.t][e.c];port[i]=R.length});R.push(r)}
else throw Error("unsupported cap "+typ);
ok(port.every(j=>j>=0),"ports");valid(R,false);return {R,p,port,idx}}
function impose(cap,mask){const p={...cap.p};for(let i=0;i<cap.port.length;i++){const j=cap.port[i],v=(mask>>i)&1;if(j in p&&p[j]!==v)return null;p[j]=v}return p}
function cappedMasks(cap,C,S,typ,full=false){const out=new Map;for(let m=0;m<(1<<C.length);m++)if(envelope(C,S,m,typ)){const p=impose(cap,m);if(p===null)continue;const w=solve(cap.R,p,full);if(w!==null){ok(witness(cap.R,w,p));out.set(m,w)}}return out}
function same(A,B){return A.size===B.size&&[...A].every(x=>B.has(x))}
function split(T,S,pins={},full=true){const G=graph(T),O=new Set(G.vs.filter(v=>!S.has(v))),C=cut(G,S),typ=type(C,S);ok(connected(G,S)&&connected(G,O),"bond");ok(["2-pair","3-mono","4-rainbow"].includes(typ),"cap type");
let A=cap(T,G,S,C,typ,pins),B=cap(T,G,O,C,typ,pins);const small=S.size<=O.size?A:B,large=small===A?B:A,shore=small===A?S:O;
const rows=cappedMasks(small,C,shore,typ,full);if(!rows.size)return {typ,cut:C.length,smaller:Math.min(S.size,O.size),sizes:[A.R.length,B.R.length],rows:[],sat:false};
const guard={...large.p};let clash=false;function set(j,v){if(j in guard&&guard[j]!==v)clash=true;guard[j]=v}
if(typ==="3-mono"){for(let i=0;i<C.length;i++)if(!rows.has(1<<i))set(large.port[i],0)}else if(rows.size===1){const m=[...rows.keys()][0];set(large.port[0],m&1)}
const w=clash?null:solve(large.R,guard,full);if(w===null)return {typ,cut:C.length,smaller:Math.min(S.size,O.size),sizes:[A.R.length,B.R.length],rows:[...rows.keys()],sat:false};
let m=0;for(let i=0;i<C.length;i++)m|=w[large.port[i]]<<i;ok(rows.has(m),"allowed mask");const p=Array(T.length).fill(-1);for(const [j,k] of large.idx)p[j]=w[k];for(const [j,k] of small.idx)p[j]=rows.get(m)[k];ok(witness(T,p,pins),"lift");
return {typ,cut:C.length,smaller:Math.min(S.size,O.size),sizes:[A.R.length,B.R.length],rows:[...rows.keys()],sat:true,selected:p.flatMap((v,j)=>v?[j]:[])}}
const qg=graph(Q), tally={};let localComparisons=0, cappedComparisons=0, guardComparisons=0;
for(let m=1;m<(1<<qg.vs.length)-1;m++){if(!(m&1))continue;const S=new Set(qg.vs.filter((_,i)=>(m>>i)&1)),C=cut(qg,S);if(C.length>4)continue;const O=new Set(qg.vs.filter(v=>!S.has(v)));if(!connected(qg,S)||!connected(qg,O))continue;const typ=type(C,S);ok(typ!=="invalid","classification");tally[typ]=(tally[typ]||0)+1;for(const X of [S,O]){const L=localMasks(Q,qg,X,C);localComparisons++;for(const b of L)ok(envelope(C,X,b,typ),"envelope");if(["2-pair","3-mono","4-rainbow"].includes(typ)){const A=cap(Q,qg,X,C,typ);ok(same(L,new Set(cappedMasks(A,C,X,typ).keys())),"exact cap");cappedComparisons++;for(let j=0;j<Q.length;j++)if(X.has(tn(j)))for(let v=0;v<2;v++){const p={[j]:v},LL=localMasks(Q,qg,X,C,p),B=cap(Q,qg,X,C,typ,p);ok(same(LL,new Set(cappedMasks(B,C,X,typ).keys())),"guard cap");guardComparisons++}}}}
function chain(blocks){let T=[],block=[],off=0;for(const B of blocks){block.push({start:T.length,end:T.length+B.length,off,n:B.length/3});for(const t of B)T.push(t.map(v=>v+off));off+=B.length/3}for(let i=0;i+1<block.length;i++){const a=block[i].start,b=block[i+1].start,c=i%2;[T[a][c],T[b][c]]=[T[b][c],T[a][c]]}return {T,block}}
function blockSet(T,bs,from){const S=new Set;for(let i=from;i<bs.length;i++){const B=bs[i];for(let j=B.start;j<B.end;j++)S.add(tn(j));for(let c=0;c<4;c++)for(let a=B.off;a<B.off+B.n;a++)S.add(en(c,a))}return S}
const jobs=[];for(const [name,T,label] of [["Q",Q,true],["U",U,false],["V",V,true],["W",W,true]]){valid(T);const w=solve(T);ok((w!==null)===label,name);jobs.push({name,tuples:T.length,sat:w!==null})}
for(const [name,blocks,mid,label] of [["VV",[V,V],1,true],["VU",[V,U],1,false],["VW",[V,W],1,true],["Q12",Array(12).fill(Q),6,true],["Q24",Array(24).fill(Q),12,true],["Q-U-Q",[...Array(5).fill(Q),U,...Array(5).fill(Q)],5,false],["Q-W-Q",[...Array(5).fill(Q),W,...Array(5).fill(Q)],5,true]]){
const {T,block}=chain(blocks);valid(T);const root=Array(T.length).fill(-1);const rootOK=close(T,groups(T),root);ok(rootOK||!label,"root closure sound");jobs.push({name:name+"-root",tuples:T.length,rootOK,pins:root.filter(v=>v!==-1).length});const S2=blockSet(T,block,mid);const r2=split(T,S2,rootOK?Object.fromEntries(root.flatMap((v,j)=>v===-1?[]:[[j,v]])):{},true);ok(r2.sat===label,name+" 2");jobs.push({name:name+"-pair",tuples:T.length,...r2});
const S4=blockSet(T,block,mid+1);S4.add(tn(block[mid].start));const r4=split(T,S4,rootOK?Object.fromEntries(root.flatMap((v,j)=>v===-1?[]:[[j,v]])):{},true);ok(r4.sat===label,name+" 4");jobs.push({name:name+"-rainbow",tuples:T.length,...r4})}
let seed=2053;function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}function spin(mask,i){return (mask>>i)&1?1:-1}
let psTables=0,psNonzero=0;
for(let trial=0;trial<160;trial++){const term=[0,2,8,6],priv=[1,3,4,5,7],edges=[];for(let v=0;v<9;v++){if(v%3!==2)edges.push([v,v+1,rand()%15-7]);if(v<6)edges.push([v,v+3,rand()%15-7])}const f=[];for(let b=0;b<16;b++){let best=Infinity;for(let p=0;p<32;p++){const s=Array(9);term.forEach((v,i)=>s[v]=spin(b,i));priv.forEach((v,i)=>s[v]=spin(p,i));best=Math.min(best,edges.reduce((e,[u,v,J])=>e+J*s[u]*s[v],0))}f.push(best)}
function coef(mask,F){return F.reduce((z,v,b)=>{let s=1;for(let i=0;i<4;i++)if((mask>>i)&1)s*=spin(b,i);return z+v*s},0)/16}
const A=coef(5,f),B=coef(10,f),q=coef(15,f);ok(2*q===Math.abs(A+B)-Math.abs(A-B),"PS05 switching");if(q!==0)psNonzero++;
const h=Math.min(Math.abs(A),Math.abs(B)),a=Math.abs(A)+h,b=Math.abs(B)+h,weights=[a,b,A>0?-a:a,B>0?-b:b];const g=Array.from({length:16},(_,m)=>-Math.abs(weights.reduce((z,J,i)=>z+J*spin(m,i),0)));const rim=[3,6,12,9];for(let m=0;m<16;m++){let y=g[m]+coef(0,f)-coef(0,g);for(const r of rim){let z=1;for(let i=0;i<4;i++)if((r>>i)&1)z*=spin(m,i);y+=(coef(r,f)-coef(r,g))*z}ok(y===f[m],"star rim")}psTables++}
let recurrenceChecks=0;for(let a=52;a<=100;a++)for(let b=a;b<=300;b++){ok(3*(a+13)**3+(b+13)**3<=(a+b)**3-1,"recurrence");recurrenceChecks++}
return {seed:2053,assertions,matchingCalls,searchNodes,pinUpdates,qBondCounts:tally,localComparisons,cappedComparisons,guardComparisons,psTables,psNonzero,recurrenceChecks,jobs,limitations:"Exact reference DFS, not polynomial prime solver. Q all connected cuts <=4, chain cuts supplied and validated; embedding via separate planarity checks and disk gluing proof. No general cut enumeration run."}
}
console.log(JSON.stringify(audit(),null,2));

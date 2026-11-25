// S27 source arrays: 4b9667f07bd3f1007a11d8a0106869f7b7225db2; fixed finite controls only.
const inputs=[{"n":7,"root":[{"t":[0,1,2],"bad":[0,7]},{"t":[0,3,4],"bad":[0,7]},{"t":[0,5,6],"bad":[0,7]},{"t":[1,3,5],"bad":[0,7]},{"t":[1,4,6],"bad":[0,7]},{"t":[2,3,6],"bad":[0,7]},{"t":[2,4,5],"bad":[0,7]}],"sat":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[0,7]},{"t":[0,5,6],"bad":[0,7]},{"t":[1,3,5],"bad":[0,7]},{"t":[1,4,6],"bad":[0,7]},{"t":[2,3,6],"bad":[0,7]},{"t":[2,4,5],"bad":[0,7]}],"guards":[]},{"n":15,"root":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[1,6]},{"t":[0,5,6],"bad":[3,4]},{"t":[0,7,8],"bad":[2,5]},{"t":[0,9,10],"bad":[3,4]},{"t":[0,11,12],"bad":[3,4]},{"t":[0,13,14],"bad":[1,6]},{"t":[1,3,5],"bad":[2,5]},{"t":[1,4,6],"bad":[3,4]},{"t":[1,7,9],"bad":[1,6]},{"t":[1,8,10],"bad":[3,4]},{"t":[1,11,13],"bad":[1,6]},{"t":[1,12,14],"bad":[2,5]},{"t":[2,3,6],"bad":[1,6]},{"t":[2,4,5],"bad":[2,5]},{"t":[2,7,10],"bad":[3,4]},{"t":[2,8,9],"bad":[2,5]},{"t":[2,11,14],"bad":[1,6]},{"t":[2,12,13],"bad":[1,6]},{"t":[3,7,11],"bad":[3,4]},{"t":[3,8,12],"bad":[3,4]},{"t":[3,9,13],"bad":[3,4]},{"t":[3,10,14],"bad":[3,4]},{"t":[4,7,12],"bad":[1,6]},{"t":[4,8,11],"bad":[2,5]},{"t":[4,9,14],"bad":[2,5]},{"t":[4,10,13],"bad":[1,6]},{"t":[5,7,13],"bad":[1,6]},{"t":[5,8,14],"bad":[3,4]},{"t":[5,9,11],"bad":[2,5]},{"t":[5,10,12],"bad":[2,5]},{"t":[6,7,14],"bad":[3,4]},{"t":[6,8,13],"bad":[2,5]},{"t":[6,9,12],"bad":[2,5]},{"t":[6,10,11],"bad":[0,7]}],"sat":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[1,6]},{"t":[0,5,6],"bad":[3,4]},{"t":[0,7,8],"bad":[2,5]},{"t":[0,9,10],"bad":[3,4]},{"t":[0,11,12],"bad":[3,4]},{"t":[0,13,14],"bad":[1,6]},{"t":[1,3,5],"bad":[2,5]},{"t":[1,4,6],"bad":[3,4]},{"t":[1,7,9],"bad":[1,6]},{"t":[1,8,10],"bad":[3,4]},{"t":[1,11,13],"bad":[1,6]},{"t":[1,12,14],"bad":[2,5]},{"t":[2,3,6],"bad":[1,6]},{"t":[2,4,5],"bad":[2,5]},{"t":[2,7,10],"bad":[3,4]},{"t":[2,8,9],"bad":[2,5]},{"t":[2,11,14],"bad":[1,6]},{"t":[2,12,13],"bad":[1,6]},{"t":[3,7,11],"bad":[3,4]},{"t":[3,8,12],"bad":[3,4]},{"t":[3,9,13],"bad":[3,4]},{"t":[3,10,14],"bad":[3,4]},{"t":[4,7,12],"bad":[1,6]},{"t":[4,8,11],"bad":[2,5]},{"t":[4,9,14],"bad":[2,5]},{"t":[4,10,13],"bad":[1,6]},{"t":[5,7,13],"bad":[1,6]},{"t":[5,8,14],"bad":[3,4]},{"t":[5,9,11],"bad":[2,5]},{"t":[5,10,12],"bad":[2,5]},{"t":[6,7,14],"bad":[3,4]},{"t":[6,8,13],"bad":[2,5]},{"t":[6,9,12],"bad":[2,5]},{"t":[6,10,11],"bad":[2,5]}],"guards":[[4,6,0],[6,8,0],[0,3,0],[1,2,0],[2,3,0],[3,5,1],[5,7,1]]}];

const stats={closureScans:0,ownerVisits:0,words:0,boundaryVisits:0,inequalities:0,liftChecks:0};
let seed=20261125;function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
function check(b,m){if(!b)throw Error(m)}
function parity(x){let p=0;while(x){x&=x-1;p^=1}return p}
function reduce(a,b,B){for(const [p,q] of B){if(a&(p&-p)){a^=p;b^=q}}return [a,b]}
function add(a,b,B){[a,b]=reduce(a,b,B);if(!a)return b?-1:0;B.push([a,b]);B.sort((u,v)=>(u[0]&-u[0])-(v[0]&-v[0]));return 1}
function rows(o){let [a,b,c]=o.t,w=o.bad[0];return [[(1<<a)^(1<<b),(w&1)^((w>>1)&1)],[(1<<a)^(1<<c),(w&1)^((w>>2)&1)]]}
function close(owners,guards){let B=[];for(const [a,b,c] of guards)if(add((1<<a)^(1<<b),c,B)<0)return null;
while(true){stats.closureScans++;let change=false;for(const o of owners){let L=[];let empty=false;for(let [a,b] of rows(o)){[a,b]=reduce(a,b,B);if(add(a,b,L)<0){empty=true;break}}
if(empty)continue;if(!L.length)return null;if(L.length===1){if(add(L[0][0],L[0][1]^1,B)<0)return null;change=true;break}}
if(!change)return B}}
function inGuard(x,G){return G.every(([a,b,c])=>(((x>>a)^(x>>b))&1)===c)}
function energy(x,O){let e=0;for(const o of O){stats.ownerVisits++;let w=0;for(let j=0;j<o.t.length;j++)w|=((x>>o.t[j])&1)<<j;if(o.bad.includes(w))e++}return e}
function pool(n,O,G){let P=[],models=0;for(let x=0;x<1<<n;x++){stats.words++;if(!inGuard(x,G))continue;let e=energy(x,O);P.push([x,e,2**(O.length-e)]);if(!e)models++}return {P,models}}
function tab(P,S){let M=Array(16).fill(Infinity),C=Array(16).fill(0),Z=Array(16).fill(0),W=Array(16).fill(-1);
for(const [x,e,z] of P){stats.boundaryVisits++;let a=((x>>S[0])&1)|(((x>>S[1])&1)<<1)|(((x>>S[2])&1)<<2)|(((x>>S[3])&1)<<3);if(e<M[a]){M[a]=e;W[a]=x}if(!e)C[a]++;Z[a]+=z}
check(Z.every(Number.isSafeInteger),"integer weight precision");return {M,C,Z,W}}
function inequalities(T,S,record){let out=[0,0,0],example=null;
for(let a=0;a<16;a++){let b=a^10,p=a^2,q=a^8,u=a^1,v=a^4;
let [M,C,Z]=[T.M,T.C,T.Z];let e=M[a]+M[b]<Math.min(M[p]+M[q],M[u]+M[v]);let test=(A)=>BigInt(A[a])*BigInt(A[b])>BigInt(A[p])*BigInt(A[q])+BigInt(A[u])*BigInt(A[v]);let c=test(C),z=test(Z);stats.inequalities+=3;
if(e)out[0]++;if(c)out[1]++;if(z)out[2]++;if(!example&&(e||c||z))example={scope:S,a,b,p,q,u,v,M:M.map(x=>isFinite(x)?x:null),C,Z,minimumWitnesses:T.W,violates:[e,c,z]}}
return {out,example}}
function test(n,O,G,id){let B=close(O,G);if(B===null)return {id,closure:"UNSAT",skipped:true};
let {P,models}=pool(n,O,G);for(const [x,e] of P)if(!e){check(B.every(([a,b])=>parity(x&a)===b),"closure unsound");stats.liftChecks++}
let totals=[0,0,0],orders=[0,0,0],first=null,scopeCount=0;
for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)for(let c=b+1;c<n;c++)for(let d=c+1;d<n;d++)for(const S of [[a,b,c,d],[a,b,d,c],[a,c,b,d]]){let t=tab(P,S),v=inequalities(t,S);scopeCount++;for(let i=0;i<3;i++){totals[i]+=v.out[i];if(v.out[i])orders[i]++}if(!first&&v.example)first=v.example}
return {id,n,closureRank:B.length,models,orderedScopes:scopeCount,violatingOrders:orders,violations:totals,first}}
function planarControls(){let results=[];for(let i=0;i<96;i++){
let O=[];for(let j=0;j<4;j++){let a=j,b=(j+1)%4,w=(rnd()>>>16)&7;O.push({t:[a,b,4],bad:[w,w^7]});if(i%2){let z=(rnd()>>>20)&1;O.push({t:[a,b],bad:[z,z^3]})}}
let {P}=pool(5,O,[]),T=tab(P,[0,1,2,3]),v=inequalities(T,[0,1,2,3]);check(v.out.every(x=>x===0),"planar wheel inequality failed");results.push(v.out)}
let crossing=[{t:[0,2],bad:[1,2]},{t:[1,3],bad:[1,2]}],adjacent=[{t:[0,1],bad:[1,2]},{t:[2,3],bad:[1,2]}];
let x=inequalities(tab(pool(4,crossing,[]).P,[0,1,2,3]),[0,1,2,3]);check(x.out.every(v=>v>0),"crossing negative control missed");
let a=inequalities(tab(pool(4,adjacent,[]).P,[0,1,2,3]),[0,1,2,3]);check(a.out.every(v=>v===0),"adjacent control failed");return {wheels:results.length,crossing:x,adjacent:a}}
const controls=planarControls(),shared=[];
for(const u of inputs){for(const label of ["root","sat"])shared.push(test(u.n,u[label],[], "S27-"+u.n+"-"+label+"-raw"));if(u.guards.length)for(const p of [1,u.guards.length])shared.push(test(u.n,u.root,u.guards.slice(0,p),"S27-"+u.n+"-root-"+p+"-cuts"))}
console.log(JSON.stringify({controls,shared,stats},null,2));

"use strict";
function main(){
const L={gauss:0,xor:0,closure:0,pins:0,energy:0,pairBuild:0,energyTerms:0,directEdges:0,cosets:0,coalesced:0,queries:0,queryTerms:0,checks:0,referenceWords:0};const b=i=>1n<<BigInt(i),piv=x=>x.toString(2).length-1,par=x=>{let p=0;while(x){x&=x-1n;p^=1}return p},dot=(x,y)=>par(x&y),sg=x=>x?-1n:1n,ck=(x,m)=>{L.checks++;if(!x)throw Error(m)};
function rr(rows){L.gauss++;let A=[];for(let [v,t] of rows){for(const [w,s,p] of A)if(v&p){v^=w;t^=s;L.xor++}if(!v){if(t)return null;continue}let p=b(piv(v));for(let i=0;i<A.length;i++)if(A[i][0]&p){A[i]=[A[i][0]^v,A[i][1]^t,A[i][2]];L.xor++}A.push([v,t,p]);A.sort((x,y)=>x[2]<y[2]?-1:1)}return A.map(([v,t])=>[v,t])}
const zr=vs=>vs.map(v=>[v,0]),basis=vs=>rr(zr(vs)).map(x=>x[0]);
function mem(v,B){for(const w of B)if(v&b(piv(w)))v^=w;return v===0n}
const point=R=>R.reduce((x,[v,t])=>t?x|b(piv(v)):x,0n),holds=(R,x)=>R.every(([v,t])=>dot(v,x)===t),key=R=>R.map(([v,t])=>v.toString(16)+":"+t).join(",");
function ker(R,d){let P=new Set(R.map(([v])=>piv(v))),K=[];for(let i=0;i<d;i++)if(!P.has(i)){let x=b(i);for(const [v] of R)if(dot(v,x))x^=b(piv(v));K.push(x)}return K}
function close(G,es){G=rr(G);if(!G)return null;while(true){L.closure++;let M=new Map(),pin=false;for(const E of es){let J=rr(G.concat(E));if(!J)continue;let r=J.length-G.length;if(!r)return null;if(r===1){let q=E.find(([v])=>!mem(v,G.map(x=>x[0])));G=rr(G.concat([[q[0],q[1]^1]]));L.pins++;pin=true;break}let k=key(J);if(!M.has(k))M.set(k,E)}if(!pin)return {G,es:[...M.values()]}}}
function chart(n,G,es){let C=close(G,es);if(!C)return null;let a=point(C.G),K=ker(C.G,n);return {a,K,es:C.es.map(E=>rr(E.map(([v,t])=>[K.reduce((w,k,j)=>dot(v,k)?w|b(j):w,0n),t^dot(v,a)])))}}
function add(M,w,c){let s=(M.get(w)||0n)+c;if(s)M.set(w,s);else M.delete(w)}
function words(B){let W=[0n];for(let v of B)W=W.concat(W.map(w=>w^v));return W}
function transition(F,E,U,d,force=false){let r=E.length,V=E.map(x=>x[0]),a=point(E),den=b(r),O=new Map();
if(r<=3&&!force){for(const [u,c] of F){if(mem(u,U))add(O,u,den*c);for(const v of words(V)){L.directEdges++;let w=u^v;if(mem(w,U))add(O,w,-c*sg(dot(v,a)))}}for(const [w,c] of O){ck(c%den===0n,"direct integral");O.set(w,c/den)}return O}
let OU=ker(zr(U),d),OV=ker(zr(V),d),M=new Map();
function term(R,p,c){if(!R||!c)return;L.cosets++;let id=key(R)+";"+p.toString(16),old=M.get(id);if(old){L.coalesced++;c+=old.c}if(c)M.set(id,{R,p,c});else M.delete(id)}
for(const [u,c] of F){if(mem(u,U))term(Array.from({length:d},(_,i)=>[b(i),dot(u,b(i))]),0n,den*c);term(rr(zr(OU).concat(OV.map(v=>[v,dot(v,u)]))),a,-c*sg(dot(a,u)))}
let T=[...M.values()],P=[];for(let i=0;i<T.length;i++)for(let j=0;j<=i;j++){L.pairBuild++;let R=rr(T[i].R.concat(T[j].R));if(R)P.push({R,p:T[i].p^T[j].p,c:T[i].c*T[j].c*(i===j?1n:2n)})}
function energy(Q){L.energy++;let s=0n;for(const t of P){L.energyTerms++;let R=rr(t.R.concat(Q));if(R&&mem(t.p,R.map(x=>x[0])))s+=t.c*sg(dot(t.p,point(R)))*b(d-R.length)}ck(s>=0n,"square");return s}
let coords=U.map(piv);function visit(Q,j){if(!energy(Q))return;if(j===coords.length){let R=rr(zr(OU).concat(Q));ck(R&&R.length===d,"leaf");let w=point(R),s=0n;for(const t of T)if(holds(t.R,w))s+=t.c*sg(dot(t.p,w));ck(s!==0n&&s%den===0n,"integral");O.set(w,s/den);return}let v=b(coords[j]);visit(Q.concat([[v,0]]),j+1);visit(Q.concat([[v,1]]),j+1)}
visit([],0);return O}
function query(F,P){L.queries++;let R=rr(P);if(!R)return 0n;let a=point(R),B=R.map(x=>x[0]),s=0n;for(const [w,c] of F){L.queryTerms++;if(mem(w,B))s+=c*sg(dot(w,a))}ck(s%b(R.length)===0n,"query integral");return s/b(R.length)}
function solve(n,G,events,force=false,lift=true){let C=chart(n,G,events);if(!C)return {count:0n,peak:0,states:0};let {a,K,es}=C,d=K.length,m=es.length,U=Array(m+1);U[m]=[];for(let i=m-1;i>=0;i--)U[i]=basis(U[i+1].concat(es[i].map(x=>x[0])));let F=[new Map([[0n,b(d)]])],peak=1,states=1,widths=[1];for(let i=0;i<m;i++){let v=transition(F[i],es[i],U[i+1],d,force);F.push(v);peak=Math.max(peak,v.size);states+=v.size;widths.push(v.size);if(!v.size)return {count:0n,peak,states,widths}}
let count=F[m].get(0n)||0n;ck(count>=0n,"count");if(!count||!lift)return {count,peak,states,widths};let P=[],audit=[];for(let i=m-1;i>=0;i--){let q=Q=>query(F[i],Q)-query(F[i],Q.concat(es[i]));ck(q(P)>0n,"reverse start");for(let v of U[i])if(!mem(v,P.map(x=>x[0]))){let Q=rr(P.concat([[v,0]]));P=q(Q)>0n?Q:rr(P.concat([[v,1]]));ck(q(P)>0n,"reverse positive");let c=close(audit.concat(P),es);ck(c!==null,"closure lift");audit=c.G}}
let z=point(P),x=a;for(let j=0;j<d;j++)if(z&b(j))x^=K[j];ck(holds(G,x)&&events.every(e=>!holds(e,x)),"source lift");return {count,peak,states,widths,witness:x}}
function ref(n,G,es){let c=0n;for(let x=0n;x<b(n);x++){L.referenceWords++;if(holds(G,x)&&es.every(e=>!holds(e,x)))c++}return c}
const bad=(vs,j)=>vs.map((v,i)=>[b(v),(j>>i)&1]);let R={suite:{},scale:[],wide:[],ledger:L};
function compare(name,n,G,es,force=false){let a=solve(n,G,es,force),c=ref(n,G,es);ck(a.count===c,name);let s=R.suite[name]||(R.suite[name]={sat:0,unsat:0,maxPeak:0,lifts:0});s[c?"sat":"unsat"]++;s.maxPeak=Math.max(s.maxPeak,a.peak);if(a.witness!==undefined)s.lifts++}
let cube=Array.from({length:8},(_,j)=>bad([0,1,2],j));for(let mask=0;mask<256;mask++)compare("cube",3,[],cube.filter((_,i)=>mask&(1<<i)),mask%8===0);
let lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],fano=lines.flatMap(v=>[bad(v,0),bad(v,7)]);compare("fano",7,[],fano);for(let i=0;i<14;i++)compare("fano",7,[],fano.filter((_,j)=>j!==i));
let seed=24082026;function rnd(k){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%k}
for(let j=0;j<32;j++){let es=[];for(let i=0;i<4+j%4;i++){let E=rr(Array.from({length:2+j%3},()=>[BigInt(1+rnd(31)),rnd(2)]));if(E)es.push(E)}compare("random_affine",5,j%3===0?[[3n,j%2]]:[],es,true)}
for(let k of [2,4,8,16,32]){let es=[],tail=[];for(let i=0;i<k;i++){let j=k+8*i;es.push(bad([i,j,j+1],0),bad([i,j+2,j+3],1));tail.push(bad([i,j+4,j+5],0),bad([i,j+6,j+7],1))}let a=solve(9*k,[],es.concat(tail),false,k===2);ck(a.count===b(5*k)*3n**BigInt(2*k),"pair scale");R.scale.push({k,n:9*k,peak:a.peak,states:a.states,cutWidth:a.widths[2*k],affineKeysAtCut:(3n**BigInt(k)).toString(),count:a.count.toString(),lift:a.witness!==undefined})}
for(let k of [2,8,16,32]){let es=[bad([0,1],0),bad([0,2],1)],E=Array.from({length:k+2},(_,j)=>[b(j+1),0]),tail=[];for(let i=1;i<=k+2;i++){let j=k+3+2*(i-1);tail.push(bad([i,j],0),bad([i,j+1],1))}let n=k+3+2*(k+2),a=solve(n,[],es.concat([E],tail),false,k===2);ck(a.count===b(2*k+4),"wide count");R.wide.push({k,n,rank:k+2,peak:a.peak,before:a.widths[2],after:a.widths[3],naiveEdgesLowerBound:b(k+2).toString(),count:a.count.toString(),lift:a.witness!==undefined})}
return R}
console.log(JSON.stringify(main(),null,2));

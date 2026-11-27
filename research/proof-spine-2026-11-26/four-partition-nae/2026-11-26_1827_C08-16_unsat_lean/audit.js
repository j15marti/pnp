// node audit.js -- C08-16 UNSAT and lean-kernel audit
function audit(){
let seed=20261126,checks=0,capProfiles=0,partialProfiles=0,clauseChecks=0;
function ok(x,m){checks++;if(!x)throw Error(m||"check "+checks)}
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
function shuffle(a){for(let i=a.length-1;i>0;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
const bit=(w,i)=>(w>>>i)&1, nae=(c,x)=>x[c[0]]!==x[c[1]]||x[c[0]]!==x[c[2]], sat=(C,x)=>{for(let c of C){clauseChecks++;if(!nae(c,x))return false}return true};
const AG=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]];
const L=AG.flat().filter(c=>c.join(",")!=="0,1,2"&&c.join(",")!=="0,3,6");
const Q=[390,54,77,294,166,404,205,278,180,93];
function dsu(n){let a=Array.from({length:n},(_,i)=>i);function f(v){while(a[v]!==v){a[v]=a[a[v]];v=a[v]}return v}return{f,add(u,v){u=f(u);v=f(v);if(u!==v)a[u]=v}}}
function ring(k,no){let F=[[],[],[],[]];for(let b=0;b<k;b++)for(let s=0;s<4;s++)for(let j=0;j<3;j++){let c=AG[s][j].map(v=>9*b+v);if(s<2&&j===0)c[2]=9*((b+1)%k)+AG[s][j][2];F[s].push(c)}
if(!no)for(let s of [0,1]){let a=F[s][0],b=F[s][3];[a[1],b[1]]=[b[1],a[1]]}
return F}
function auth(F,n){ok(F.length===4);let D=dsu(n),P=new Set;for(let p of F){let d=Array(n).fill(0);for(let c of p){ok(c.length===3&&new Set(c).size===3);for(let v of c){ok(v>=0&&v<n);d[v]++}for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let u=c[i],v=c[j],key=Math.min(u,v)*n+Math.max(u,v);ok(!P.has(key));P.add(key);D.add(u,v)}}ok(d.every(x=>x===1))}ok(Array.from({length:n},(_,i)=>D.f(i)).every(v=>v===D.f(0)))}
function labels(F){return F.flatMap((p,s)=>p.map((c,j)=>({id:s*p.length+j,p:s,c})))}
function permute(F,n){let perm=shuffle(Array.from({length:n},(_,i)=>i));return {F:F.map(p=>shuffle(p.map(c=>shuffle(c.map(v=>perm[v]))))),perm}}
// Two independent local acquisition lanes, geometry certificate or full local truth table.
function acquire(F,n,method){let C=labels(F);for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){let D=dsu(n);for(let s of [a,b])for(let c of F[s]){D.add(c[0],c[1]);D.add(c[0],c[2])}let M=new Map;for(let v=0;v<n;v++){let r=D.f(v);if(!M.has(r))M.set(r,[]);M.get(r).push(v)}let blocks=[...M.values()];if(!blocks.every(v=>v.length===9))continue;
let cl=Array(n),offset=Array(n),local=blocks.map(()=>[]),external=[];blocks.forEach((V,i)=>V.forEach(v=>cl[v]=i));for(let c of C){if(c.c.every(v=>cl[v]===cl[c.c[0]]))local[cl[c.c[0]]].push(c);else external.push(c)}
let good=true;
for(let i=0;i<blocks.length;i++){let V=blocks[i],I=local[i];if(I.length!==10){good=false;break}let id=new Map(V.map((v,j)=>[v,j])),T=I.map(c=>c.c.map(v=>id.get(v))),x=null;
if(method==="pair"){let pair=new Set;for(let c of T)for(let j=0;j<3;j++)for(let l=j+1;l<3;l++)pair.add(Math.min(c[j],c[l])*9+Math.max(c[j],c[l]));if(pair.size!==30){good=false;break}
let missing=[],touch=new Set,D2=dsu(9);for(let u=0;u<9;u++)for(let v=u+1;v<9;v++)if(!pair.has(9*u+v)){missing.push([u,v]);touch.add(u);touch.add(v);D2.add(u,v)}
if(missing.length!==6||touch.size!==5||new Set([...touch].map(v=>D2.f(v))).size!==1){good=false;break}
x=V.map((_,j)=>touch.has(j)?0:1);if(!sat(T,x)){good=false;break}
}else{let W=[];for(let w=0;w<512;w++){capProfiles++;let z=V.map((_,j)=>bit(w,j));if(sat(T,z))W.push(z)}if(W.length!==2||!W[0].every((z,j)=>z!==W[1][j])){good=false;break}x=W[0]}
if(x[0])x=x.map(v=>v^1);V.forEach((v,j)=>offset[v]=x[j]);}
if(good)return{blocks,cl,offset,local,external,C,cut:[a,b]};}
return null}
function factors(R){return R.external.map(c=>({id:c.id,p:c.p,lit:c.c.map(v=>[R.cl[v],R.offset[v]])}))}
function satL(c,z){let a=c.lit[0];return c.lit.some(([v,s])=>(z[v]^s)!==(z[a[0]]^a[1]))}
function reduce(F){let edges=[],bad=[],dep=[],nonlinear=[];for(let c of F){let g=new Map;for(let [v,s] of c.lit){if(!g.has(v))g.set(v,[]);g.get(v).push(s)}let P=[...g];if(P.length===1){if(new Set(P[0][1]).size===1)bad.push({v:P[0][0],id:c.id});continue}
if(P.length===2){let [a,b]=P;if(a[1].length===1)[a,b]=[b,a];if(a[1][0]!==a[1][1])dep.push({a:b[0],b:a[0],id:c.id});else edges.push({a:a[0],b:b[0],t:1^a[1][0]^b[1][0],id:c.id});continue}
nonlinear.push(c)}return{edges,bad,dep,nonlinear}}
function parity(n,E,unit=[]){let adj=Array.from({length:n},()=>[]),z=Array(n).fill(-1),comp=Array(n),parent=Array(n).fill(-1),pe=Array(n).fill(null),groups=[],bad=new Set,cert=null;for(let e of E){adj[e.a].push([e.b,e]);adj[e.b].push([e.a,e])}
function cycle(u,v,e){let A=new Map,pu=[],pv=[],a=u,b=v;while(a>=0){A.set(a,pu.length);if(pe[a])pu.push(pe[a]);a=parent[a]}while(!A.has(b)){pv.push(pe[b]);b=parent[b]}let C=pu.slice(0,A.get(b)).concat(pv,[e]);ok(C.reduce((s,e)=>s^e.t,0)===1);let d=new Set;for(let e of C)for(let v of [e.a,e.b]){if(d.has(v))d.delete(v);else d.add(v)}ok(!d.size);return C}
for(let v=0;v<n;v++)if(z[v]<0){let j=groups.length,q=[v];groups.push(q);z[v]=0;comp[v]=j;for(let i=0;i<q.length;i++){let u=q[i];for(let [w,e] of adj[u])if(z[w]<0){z[w]=z[u]^e.t;comp[w]=j;parent[w]=u;pe[w]=e;q.push(w)}else if((z[u]^z[w])!==e.t){bad.add(j);if(!cert)cert=cycle(u,w,e)}}}
for(let u of unit)bad.add(comp[u.v]);return{z,comp,groups,bad,cert}}
function gaussian(n,E,bad=[]){let piv=Array(n).fill(0n),rhs=new Uint8Array(n),rank=0;for(let e of E){let a=(1n<<BigInt(e.a))^(1n<<BigInt(e.b)),b=e.t;for(let i=n-1;i>=0;i--)if(a&(1n<<BigInt(i))){if(piv[i]){a^=piv[i];b^=rhs[i]}else{piv[i]=a;rhs[i]=b;rank++;a=0n;b=0;break}}if(!a&&b)return{ok:false,rank}}return{ok:!bad.length,rank}}
function autarky(n,F){let r=reduce(F);ok(!r.nonlinear.length);let P=parity(n,r.edges,r.bad),rev=Array.from({length:P.groups.length},()=>[]);for(let e of r.dep)rev[P.comp[e.b]].push(P.comp[e.a]);let blocked=new Set(P.bad),q=[...blocked];for(let i=0;i<q.length;i++)for(let a of rev[q[i]])if(!blocked.has(a)){blocked.add(a);q.push(a)}let x=P.z.map((b,v)=>blocked.has(P.comp[v])?-1:b);
return{x,blocked:[...blocked],SAT:P.bad.size===0}}
function checkPartial(F,x){return F.every(c=>{let V=c.lit.filter(([v])=>x[v]>=0).map(([v,s])=>x[v]^s);return !V.length||(V.includes(0)&&V.includes(1))})}
// Local exact rigidity and independently enumerated all 3^9 partial assignments.
let cap=[],autLocal=0;
for(let w=0;w<512;w++){let x=Array.from({length:9},(_,i)=>bit(w,i));if(sat(L,x))cap.push(w)}
ok(cap.length===2&&((cap[0]^cap[1])===511));let FL=L.map((c,id)=>({id,lit:c.map(v=>[v,0])}));
for(let w=0;w<3**9;w++){let a=w,x=[];for(let i=0;i<9;i++){x.push(a%3-1);a=Math.floor(a/3)}partialProfiles++;if(checkPartial(FL,x)){autLocal++;ok(x.every(v=>v<0)||x.every(v=>v>=0))}}ok(autLocal===3);
for(let i=0;i<10;i++){let w=Q[i],x=Array.from({length:9},(_,j)=>bit(w,j));ok(x[2]===1&&!(x[0]&&x[1])&&!nae(L[i],x)&&L.every((c,j)=>j===i||nae(c,x)))}
// Track C: independent generated MUS deletion witnesses with original owner mapping.
function phaseWord(k,z){return Array.from({length:9*k},(_,v)=>{let b=Math.floor(v/9),i=v%9;return z[b]^([0,1,2,3,6].includes(i)?0:1)})}
function pathPhases(k,start,first,howMany){let z=Array(k).fill(0);for(let t=0;t<howMany;t++)z[(start+t)%k]=first^(t%2);return z}
function verifyMUS(k,F){let raw=labels(F),M=raw.filter(c=>c.c.every(v=>Math.floor(v/9)===Math.floor(c.c[0]/9))||(c.p===0));ok(M.length===11*k);
let deleted=0;for(let i=0;i<k;i++){let x=phaseWord(k,pathPhases(k,(i+1)%k,0,k));let seam=F[0][3*i];ok(M.every(c=>c.c===seam||nae(c.c,x))&&!nae(seam,x));deleted++;
// Stronger full source test: remove both connectors of seam i.
ok(raw.every(c=>c.c===F[0][3*i]||c.c===F[1][3*i]||nae(c.c,x)));
for(let j=0;j<10;j++){let y=phaseWord(k,pathPhases(k,(i+1)%k,1,k-1));for(let a=0;a<9;a++)y[9*i+a]=bit(Q[j],a);let target=L[j].map(v=>v+9*i),bad=M.filter(c=>!nae(c.c,y));ok(bad.length===1&&bad[0].c.every(v=>target.includes(v)));deleted++}
// Drop ALL internal clauses of module i: original FULL formula becomes SAT.
let z=phaseWord(k,pathPhases(k,(i+1)%k,1,k-1));for(let j=0;j<9;j++)z[9*i+j]=0;z[9*i+2]=z[9*i+6]=1;ok(raw.every(c=>c.c.every(v=>Math.floor(v/9)===i)||nae(c.c,z)));
}
return{MUS:M.length,verifiedDeletions:deleted}}
let cases=[],smallCert=null,totalDeletion=0;
for(let k of [3,5,9,17,33,65,129,257])for(let no of [true,false]){let raw=ring(k,no),n=9*k;auth(raw,n);let {F}=permute(raw,n);auth(F,n);
let A=acquire(F,n,"pair"),B=acquire(F,n,"table");ok(A&&B&&A.blocks.length===k&&B.blocks.length===k);for(let v=0;v<n;v++)for(let u of A.blocks[A.cl[v]])ok(B.cl[v]===B.cl[u]&&((A.offset[v]^A.offset[u])===(B.offset[v]^B.offset[u])));
let a=factors(A),b=factors(B),aR=reduce(a),bR=reduce(b),P=parity(k,aR.edges,aR.bad),G=gaussian(k,bR.edges,bR.bad);ok(P.bad.size>0===no&&G.ok===!no);ok(P.groups.length===1);let lift=P.z;let exactStatus;
if(P.bad.size){exactStatus="UNSAT";ok(P.cert&&P.cert.length===k&&aR.nonlinear.length===0);let auto=autarky(k,a);ok(auto.x.every(x=>x<0)&&!auto.SAT);if(k===3)smallCert={source:F,localOwnerIds:A.local.map(L=>L.map(c=>c.id)),blocks:A.blocks,offset:A.offset,cycle:P.cert};}
else{ok(a.every(c=>satL(c,lift)));let x=A.cl.map((v,j)=>lift[v]^A.offset[j]);ok(sat(F.flat(),x));exactStatus="SAT"}
let minimal=no?verifyMUS(k,raw):null;if(minimal)totalDeletion+=minimal.verifiedDeletions;cases.push({k,n,clauses:12*k,label:no?"UNSAT":"SAT",exactStatus,localCaps:k,parityEdges:aR.edges.length,nonlinear:aR.nonlinear.length,cycle:P.cert?.length??0,lean:no,cut:A.cut,...(minimal??{})});
}
// Generic synthetic two-phase signed quotient audit; actual 3-state partial assignments, not marginal supports.
let syn={cases:0,unsat:0,nonemptyLean:0,tautImplications:0,partialProfiles:0};
for(let t=0;t<600;t++){let n=2+rnd(5),m=1+rnd(12),F=[];for(let j=0;j<m;j++){let a=rnd(n),b=rnd(n);F.push({id:j,lit:[[a,rnd(2)],[a,rnd(2)],[b,rnd(2)]]})}
let A=autarky(n,F),U=new Set,full=false;for(let w=0;w<3**n;w++){let a=w,x=[];for(let v=0;v<n;v++){x.push(a%3-1);a=Math.floor(a/3)}syn.partialProfiles++;if(!checkPartial(F,x))continue;for(let v=0;v<n;v++)if(x[v]>=0)U.add(v);if(x.every(v=>v>=0))full=true}
ok(A.SAT===full&&checkPartial(F,A.x)&&A.x.every((b,v)=>(b>=0)===U.has(v)));
let remaining=F.filter(c=>c.lit.every(([v])=>A.x[v]<0)),B=autarky(n,remaining);for(let c of remaining)for(let [v] of c.lit)ok(B.x[v]<0);
syn.cases++;syn.unsat+=!full;syn.nonemptyLean+=remaining.length>0;syn.tautImplications+=reduce(F).dep.length;
}
const special=[{id:0,lit:[[0,0],[0,0],[0,0]]},{id:1,lit:[[0,0],[0,1],[1,0]]}],t=autarky(3,special);ok(t.x[0]<0&&t.x[1]<0&&t.x[2]>=0&&!t.SAT);
return{seed:20261126,checks,clauseChecks,capProfiles,partialProfiles,cap,localAutarkies:autLocal,patchWords:Q,cases,totalDeletion,synthetic:syn,smallCert};
}
console.log(JSON.stringify(audit(),null,2));

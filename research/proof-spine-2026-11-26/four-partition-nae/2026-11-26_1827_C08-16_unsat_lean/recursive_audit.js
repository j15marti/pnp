// node recursive_audit.js -- C08-16 exact source compiler and iterative UNSAT certificate
function recursiveAudit(){
let checks=0,seed=20261127,matchingScans=0,matchingAug=0,localScans=0;
function ok(v,m){checks++;if(!v)throw Error(m||"check "+checks)}
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
function shuffle(a){for(let i=a.length-1;i>0;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
const AG=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]];
const nae=(c,x)=>c.some(v=>x[v]!==x[c[0]]);
function dsu(n){let p=Array.from({length:n},(_,i)=>i);function f(v){while(p[v]!==v){p[v]=p[p[v]];v=p[v]}return v}return{f,add(a,b){a=f(a);b=f(b);if(a!==b)p[a]=b}}}
function auth(F,n){let D=dsu(n),P=new Set;ok(F.length===4);for(let part of F){let d=new Uint8Array(n);for(let c of part){ok(c.length===3&&new Set(c).size===3);for(let v of c){ok(v>=0&&v<n);d[v]++}for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let u=c[i],v=c[j],key=Math.min(u,v)*n+Math.max(u,v);ok(!P.has(key));P.add(key);D.add(u,v)}}ok(d.every(x=>x===1))}ok(Array.from({length:n},(_,i)=>D.f(i)).every(v=>v===D.f(0)))}
function ring(k,no){let F=[[],[],[],[]];for(let b=0;b<k;b++)for(let s=0;s<4;s++)for(let j=0;j<3;j++){let c=AG[s][j].map(v=>9*b+v);if(s<2&&j===0)c[2]=9*((b+1)%k)+AG[s][j][2];F[s].push(c)}if(!no)for(let s of [0,1]){let a=F[s][0],b=F[s][3];[a[1],b[1]]=[b[1],a[1]]}return F}
function cyclic(p){return Array.from({length:4},(_,s)=>Array.from({length:p},(_,i)=>[i,p+(i+s)%p,2*p+(i+3*s)%p]))}
function centers(C,n){let owner=new Int32Array(n).fill(-1),variable=new Int32Array(n).fill(-1),seenO=new Int32Array(n),seenV=new Int32Array(n),parent=new Int32Array(n);
for(let root=0;root<n;root++){let stamp=root+1,q=[root],end=-1;seenO[root]=stamp;for(let j=0;j<q.length&&end<0;j++){let c=q[j];for(let v of C[c]){matchingScans++;if(seenV[v]===stamp)continue;seenV[v]=stamp;parent[v]=c;if(owner[v]<0){end=v;break}let u=owner[v];if(seenO[u]!==stamp){seenO[u]=stamp;q.push(u)}}}ok(end>=0);matchingAug++;for(let v=end;v>=0;){let c=parent[v],old=variable[c];variable[c]=v;owner[v]=c;v=old}}
ok(new Set(variable).size===n);return variable}
function compile(F,n){let G=[[],[],[],[]], provenance=[];for(let v=0;v<n;v++)for(let s=0;s<4;s++)for(let i=0;i<3;i++)if(!(s<2&&i===0))G[s].push(AG[s][i].map(u=>9*v+u));
for(let s=0;s<2;s++){let C=(s===0?[0,1,2]:[3,0,1]).flatMap(j=>F[j]),match=centers(C,n),used=new Uint8Array(n);let free=s===0?[1,2]:[3,6];C.forEach((c,i)=>{let row=c.map(v=>9*v+(v===match[i]?0:free[used[v]++]));ok(row.filter(v=>v%9===0).length===1);G[s].push(row);provenance.push({s,clause:c.slice(),physical:row.slice()})});ok(used.every(x=>x===2))}
auth(G,9*n);return {F:G,map:provenance}}
function renamed(F,n){let p=shuffle(Array.from({length:n},(_,i)=>i));return F.map(part=>shuffle(part.map(c=>shuffle(c.map(v=>p[v])))))}
function factorKey(c){let L=c.lit.map(([v,s])=>[v,s]).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);let a=L.map(([v,s])=>2*v+s).join(","),b=L.map(([v,s])=>2*v+(s^1)).sort((a,b)=>a-b).join(",");return a<b?a:b}
function graphParity(n,E){let A=Array.from({length:n},()=>[]),x=new Int8Array(n).fill(-1),root=new Int32Array(n),par=new Int32Array(n).fill(-1),via=Array(n).fill(null),groups=0;for(let e of E){A[e.a].push([e.b,e]);A[e.b].push([e.a,e])}
function contradiction(u,v,e){let a=u,b=v,L=[],R=[],pos=new Map;while(a>=0){pos.set(a,L.length);if(via[a])L.push(via[a]);a=par[a]}while(!pos.has(b)){R.push(via[b]);b=par[b]}let C=L.slice(0,pos.get(b)).concat(R,[e]);ok(C.reduce((s,e)=>s^e.t,0)===1);let d=new Set;for(let e of C)for(let u of [e.a,e.b]){if(d.has(u))d.delete(u);else d.add(u)}ok(!d.size);return C}
for(let i=0;i<n;i++)if(x[i]<0){let q=[i],g=groups++;x[i]=0;root[i]=g;for(let j=0;j<q.length;j++){let u=q[j];for(let [v,e] of A[u]){if(x[v]<0){x[v]=x[u]^e.t;root[v]=g;par[v]=u;via[v]=e;q.push(v)}else if((x[u]^x[v])!==e.t)return{bad:contradiction(u,v,e)}}}}
return{root:[...root],offset:[...x],groups}}
function terminal(F,n,trace=false){let C=F.flat().map((c,id)=>({id,lit:c.map(v=>[v,0])})),N=n,history=[],rounds=[],traces=[];
function done(status,why,cert=null){let result={status,why,rounds,finalVars:n,finalClauses:C.length};if(trace)result.trace={rounds:traces,cert};if(status==="SAT"){let x=Array(n).fill(0);for(let H of history.reverse())x=H.root.map((v,i)=>x[v]^H.offset[i]);ok(x.length===N&&F.flat().every(c=>nae(c,x)));result.x=x}return result}
for(let round=0;round<=N;round++){let E=[],live=[],seen=new Set;
for(let c of C){let g=new Map;for(let [v,s] of c.lit){if(!g.has(v))g.set(v,[]);g.get(v).push(s)}if([...g.values()].some(a=>new Set(a).size>1))continue;
if(g.size===1)return done("UNSAT","unary monochromatic",{id:c.id,lit:c.lit});
let key=factorKey(c);if(seen.has(key))continue;seen.add(key);live.push(c);
if(g.size===2){let P=[...g];E.push({a:P[0][0],b:P[1][0],t:1^P[0][1][0]^P[1][1][0],origin:{type:"binary",id:c.id,lit:c.lit}})}}
C=live;if(!C.length)return done("SAT","all constraints discharged");
let adj=Array.from({length:n},()=>new Set),inc=Array.from({length:n},()=>[]);for(let j=0;j<C.length;j++){let V=[...new Set(C[j].lit.map(p=>p[0]))];for(let u of V){inc[u].push(j);for(let v of V)if(u!==v)adj[u].add(v)}}
let candidate=new Set,capCount=0,binaryCount=E.length;
for(let v=0;v<n;v++)if(adj[v].size===8){let V=[v,...adj[v]].sort((a,b)=>a-b),key=V.join(",");if(candidate.has(key))continue;candidate.add(key);localScans++;let S=new Set(V),I=[...new Set(V.flatMap(u=>inc[u]))].filter(j=>C[j].lit.every(([u])=>S.has(u)));if(I.length<10||I.length>12)continue;
let signs=new Map,ids=new Map(V.map((u,i)=>[u,i])),P=new Set,legal=true;for(let j of I){let c=C[j].lit;if(new Set(c.map(p=>p[0])).size!==3){legal=false;break}for(let [u,s] of c){if(signs.has(u)&&signs.get(u)!==s)legal=false;signs.set(u,s)}for(let a=0;a<3;a++)for(let b=a+1;b<3;b++){let u=ids.get(c[a][0]),w=ids.get(c[b][0]),p=Math.min(u,w)*9+Math.max(u,w);if(P.has(p))legal=false;P.add(p)}}if(!legal)continue;
let origin={type:"pairCount",V,clauses:I.map(j=>({id:C[j].id,lit:C[j].lit})),signs:V.map(u=>signs.get(u))};
if(I.length>=11){rounds.push({vars:n,clauses:C.length,localCaps:capCount,binary:binaryCount,candidates:candidate.size,contradiction:"pair count"});return done("UNSAT","9-point pair count",origin)}
let missing=[],U=new Set,D=dsu(9);for(let a=0;a<9;a++)for(let b=a+1;b<9;b++)if(!P.has(a*9+b)){missing.push([a,b]);U.add(a);U.add(b);D.add(a,b)}if(U.size!==5||missing.length!==6||new Set([...U].map(u=>D.f(u))).size!==1)continue;
let y=V.map((u,i)=>(U.has(i)?0:1)^signs.get(u));if(!I.every(j=>{let c=C[j].lit;return c.some(([u,s])=>(y[ids.get(u)]^s)!==(y[ids.get(c[0][0])]^c[0][1]))}))continue;
capCount++;for(let i=1;i<9;i++)E.push({a:V[0],b:V[i],t:y[0]^y[i],origin});}
let R=graphParity(n,E);rounds.push({vars:n,clauses:C.length,localCaps:capCount,binary:binaryCount,candidates:candidate.size,nextVars:R.groups??null});
if(R.bad)return done("UNSAT","parity cycle",R.bad);
if(R.groups===n)return done("UNKNOWN","no further certified parity contraction");
if(trace)traces.push({equations:E,root:R.root,offset:R.offset});
history.push(R);C=C.map(c=>({id:c.id,lit:c.lit.map(([v,s])=>[R.root[v],s^R.offset[v]])}));n=R.groups;
}throw Error("round bound")}
let cases=[],example=null;
for(let k of [3,5,9,17,33])for(let no of [true,false])for(let depth of (k===3?[1,2,3]:k<=9?[1,2]:[1])){let F=ring(k,no),n=9*k;auth(F,n);let rawN=n,sourceM=F.flat().length;for(let d=0;d<depth;d++){let R=compile(F,n);F=R.F;n*=9}
let X=renamed(F,n);auth(X,n);let z=terminal(X,n,k===3&&depth===1&&no);ok(z.status===(no?"UNSAT":"SAT"));if(z.trace)example={source:X,trace:z.trace,rounds:z.rounds};cases.push({kind:"ring",k,depth,sourceVars:rawN,n,sourceM,status:z.status,why:z.why,rounds:z.rounds})}
for(let depth of [1,2,3]){let F=AG,n=9;for(let d=0;d<depth;d++){F=compile(F,n).F;n*=9}let z=terminal(renamed(F,n),n);ok(z.status==="UNSAT"&&z.why==="9-point pair count");cases.push({kind:"AG9",depth,n,status:z.status,why:z.why,rounds:z.rounds})}
for(let p of [5,7,13,31]){let F=cyclic(p),n=3*p;auth(F,n);let R=compile(F,n),z=terminal(renamed(R.F,9*n),9*n);ok(z.status==="UNKNOWN"&&z.finalVars===n&&z.finalClauses===4*n/3);ok(F.flat().every(c=>nae(c,Array.from({length:n},(_,i)=>i>=2*p?1:0))));cases.push({kind:"cyclic",p,depth:1,n:9*n,status:z.status,knownSourceSAT:true,nonlinearBlockerLowerBound:n/3,rounds:z.rounds})}
return{seed:20261127,checks,matchingScans,matchingAug,localScans,cases,example};
}
console.log(JSON.stringify(recursiveAudit(),null,2));

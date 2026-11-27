function audit(){
const CAP=65536,assert=(x,s)=>{if(!x)throw Error(s)},C=(a,b,c)=>new Set([a,b,c]).size===3&&[0,1,2,3,4].some(i=>[a,b,c].every(x=>[i,(i+1)%5,(i+2)%5].includes(x))),R=(a,b,c)=>new Set([a,b,c]).size===3&&([1,3].includes((b-a+5)%5)!==[1,3].includes((c-a+5)%5));
let gates=0;for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++){assert(C(a,b,c)===(R(a,b,c)&&R(b,a,c)),"C/R");gates++}
let dom=[0,1,2,3,4].filter(p=>[2,3,4].every(a=>[0,1,2,3,4].some(z=>C(a,p,z))));assert(dom.join()==="0,1","domain");
for(let p of dom)for(let q of dom){assert(C(2,p,q)===(p!==q),"not");for(let z of dom){let good=false;for(let u=0;u<5;u++)for(let v=0;v<5;v++)good||=C(1,2,u)&&C(0,1,v)&&C(4,p,u)&&C(3,q,v)&&C(z,u,v);assert(good===(z===(p|q)),"or");gates++}}
function native(F){let n=5,m=0,hash=2166136261;const a=[0,1,2,3,4],newid=()=>n++,row=(x,y,z)=>{assert(x!==y&&x!==z&&y!==z,"distinct");m++;for(let v of [x,y,z])hash=Math.imul(hash^(v+1),16777619)>>>0},wire=()=>{let p=newid();for(let j of [2,3,4])row(a[j],p,newid());return p},not=p=>{let z=wire();row(a[2],p,z);return z},or=(p,q)=>{let z=wire(),u=newid(),v=newid();row(a[1],a[2],u);row(a[0],a[1],v);row(a[4],p,u);row(a[3],q,v);row(z,u,v);return z},pin=p=>row(a[0],a[2],p);
for(let i=0;i<5;i++)row(a[i],a[(i+1)%5],a[(i+2)%5]);let w=F.triples.map(()=>wire());for(let o of F.owners){let p=w[o[0]];for(let id of o.slice(1)){let x=w[id];pin(or(not(p),not(x)));p=or(p,x)}pin(p)}
let E=F.triples.length,O=F.owners.length;assert(n===64*E-20*O+5&&m===78*E-24*O+5,"size");return{n,m,N:n+1+2*Math.floor(Math.log2(m+1))+1+3*m*Math.ceil(Math.log2(n+1)),hash:hash.toString(16),E,O}}
function rawSearch(F){let covered=new Uint8Array(F.owners.length),visits=0,stopped=false,selected=[],H=F.t+F.k;let oids=F.triples.map(e=>e.map((v,i)=>i*H+v));function go(depth){if(depth===H)return true;let best=null;for(let u=0;u<covered.length;u++)if(!covered[u]){let a=[];for(let e of F.owners[u]){if(visits>=CAP){stopped=true;return false}visits++;if(oids[e].every(v=>!covered[v]))a.push(e);if(best&&a.length>=best.length)break}if(!a.length)return false;if(!best||a.length<best.length)best=a}
for(let e of best){selected.push(e);oids[e].forEach(v=>covered[v]=1);if(go(depth+1))return true;oids[e].forEach(v=>covered[v]=0);selected.pop();if(stopped)return false}return false}let ok=go(0);return{status:ok?"YES":stopped?"UNKNOWN":"NO",visits}}
function match(F,a,b){let H=F.t+F.k,G=Array.from({length:H},()=>new Set());for(let e of F.triples)G[e[a]].add(e[b]);let M=Array(H).fill(-1),scans=0;function go(i,seen){for(let j of G[i]){scans++;if(seen.has(j))continue;seen.add(j);if(M[j]<0||go(M[j],seen)){M[j]=i;return true}}return false}for(let i=0;i<H;i++)if(!go(i,new Set()))return{ok:false,scans};assert(new Set(M).size===H,"matching");return{ok:true,scans}}
function brute(F){let {paths,q,b,t}=F,I=Array(q).fill(0),O=Array(q).fill(0),support=new Set(),visits=0,stop=false;function go(i,s){if(i===paths.length){if(I.every((x,j)=>x===O[j]))support.add(s);return}let p=paths[i];for(let f=0;f<=p.cap;f++){if(visits===CAP){stop=true;return}visits++;if(O[p.u]+f>b||I[p.v]+f>b)continue;O[p.u]+=f;I[p.v]+=f;go(i+1,s+f*p.L);O[p.u]-=f;I[p.v]-=f;if(stop)return}}go(0,0);return{complete:!stop,visits,support:[...support].sort((a,b)=>a-b)}}

function source(q,b,hostile=false){
let paths=[],classes=q;const path=(u,v,L)=>{let chain=[u];for(let i=1;i<L;i++)chain.push(classes++);chain.push(v);paths.push({u,v,L,chain,cap:b})};
for(let i=0;i<q;i++){path(i,i,3);path(i,i,5)}
for(let i=0;i+2<q;i+=2)for(let [u,v] of [[i,i+1],[i+1,i+2],[i+2,i]]){path(u,v,1);path(v,u,2)}
if(hostile)path(0,0,4);
let t=classes*b,k=5*b*q-1,arcs=[];
for(let p=0;p<paths.length;p++)for(let j=0;j<paths[p].L;j++)for(let x=0;x<b;x++)for(let y=0;y<b;y++)arcs.push([paths[p].chain[j]*b+x,paths[p].chain[j+1]*b+y,p]);
let triples=[],type=[],owners=Array.from({length:3*(t+k)},()=>[]),ids=new Map(),add=(a,c,d,tag)=>{let id=triples.length;assert(!ids.has([a,c,d].join()),"duplicate");ids.set([a,c,d].join(),id);triples.push([a,c,d]);type.push(tag);[a,c,d].forEach((x,g)=>owners[g*(t+k)+x].push(id))};
for(let i=0;i<t;i++){add(i,i,i,["l",i]);for(let x=0;x<k;x++)for(let y=0;y<k;y++)add(i,t+x,t+y,["u",i])}
for(let [i,j,p] of arcs)for(let x=0;x<k;x++)add(t+x,i,j,["v",p]);
return{q,b,k,t,paths,arcs,triples,type,owners,ids}
}
function certificates(F){
let {q,b,k,t,paths,triples,type,owners,ids}=F;let S=5*b*q,W=paths.reduce((s,p)=>s+p.L,0),D=20*q*S-W;
let f=paths.map(p=>1+(p.u===p.v&&p.L===5?b*(D-20*q):0)),d=Array(t/b).fill(0);for(let p=0;p<paths.length;p++)for(let i=0;i<paths[p].L;i++)d[paths[p].chain[i]]+=f[p];
let denom=BigInt(D*b*b*k*k),num=type.map(([tag,i])=>BigInt(tag==="l"?(D*b-d[Math.floor(i/b)])*b*k*k:tag==="u"?d[Math.floor(i/b)]*b:f[i]*k));
assert(num.every(x=>x>0n),"positive");for(let o of owners)assert(o.reduce((s,i)=>s+num[i],0n)===denom,"fractional owner");
let signed=new Int32Array(triples.length),flow=new Map();const addcycle=(p,weight)=>{for(let i=0;i<p.L;i++){let x=p.chain[i]*b,y=p.chain[i+1]*b,key=x+","+y;flow.set(key,(flow.get(key)||0)+weight)}};addcycle(paths.find(p=>p.u===p.v&&p.L===3),-2);addcycle(paths.find(p=>p.u===p.v&&p.L===5),b*q+1);
let od=Array(t).fill(0),id=Array(t).fill(0);for(let [key,v] of flow){let [x,y]=key.split(",").map(Number);od[x]+=v;id[y]+=v;signed[ids.get([t,x,y].join())]+=v}
for(let i=0;i<t;i++){assert(od[i]===id[i],"signed flow");signed[ids.get([i,i,i].join())]=1-od[i];signed[ids.get([i,t,t].join())]=od[i]}
for(let g=0;g<3;g++){let base=owners[g*(t+k)+t][0];for(let j=1;j<k;j++){let e=triples[base].slice();e[g]=t+j;let variant=ids.get(e.join());assert(variant!==undefined,"variant");signed[base]--;signed[variant]++}}
for(let o of owners)assert(o.reduce((s,i)=>s+signed[i],0)===1,"signed owner");return{fractionalDenominator:String(denom),ownersChecked:2*owners.length}
}
// Factor elimination: exact partial in/out loads and cardinality, source path factors.
function eliminate(F,cap=65536){
let {paths,q,b,t}=F,visits=0,peak=0,width=0,order=[],factors=paths.map(p=>{let scope=[...new Set([p.u,p.v])].sort((a,b)=>a-b),rows=[];for(let r=0;r<=p.cap;r++){let v=Array(2*scope.length+1).fill(0);v[2*scope.indexOf(p.u)]+=r;v[2*scope.indexOf(p.v)+1]+=r;v[v.length-1]=p.L*r;rows.push(v)}return{scope,rows}});
let remaining=new Set(Array.from({length:q},(_,i)=>i));
function join(A,B){let scope=[...new Set([...A.scope,...B.scope])].sort((a,b)=>a-b),a=A.scope.map(v=>scope.indexOf(v)),bb=B.scope.map(v=>scope.indexOf(v)),rows=new Map();width=Math.max(width,scope.length);for(let x of A.rows)for(let y of B.rows){if(visits===cap)throw Error("CAP");visits++;let r=Array(2*scope.length+1).fill(0);a.forEach((j,i)=>{r[2*j]+=x[2*i];r[2*j+1]+=x[2*i+1]});bb.forEach((j,i)=>{r[2*j]+=y[2*i];r[2*j+1]+=y[2*i+1]});r[r.length-1]=x.at(-1)+y.at(-1);if(r.at(-1)>t||r.slice(0,-1).some(v=>v>b))continue;rows.set(r.join(),r)}peak=Math.max(peak,rows.size);return{scope,rows:[...rows.values()]}}
try{while(remaining.size){let v=[...remaining].sort((a,b)=>new Set(factors.filter(f=>f.scope.includes(a)).flatMap(f=>f.scope)).size-new Set(factors.filter(f=>f.scope.includes(b)).flatMap(f=>f.scope)).size||a-b)[0];order.push(v);remaining.delete(v);let fs=factors.filter(f=>f.scope.includes(v));factors=factors.filter(f=>!f.scope.includes(v));if(!fs.length)continue;let X=fs.reduce(join),j=X.scope.indexOf(v);width=Math.max(width,X.scope.length);let scope=X.scope.filter(x=>x!==v),rows=new Map();for(let r of X.rows){if(r[2*j]!==r[2*j+1])continue;let z=r.slice();z.splice(2*j,2);rows.set(z.join(),z)}factors.push({scope,rows:[...rows.values()]})}let X=factors.reduce(join,{scope:[],rows:[[0]]});return{complete:true,visits,peak,width,order,support:X.rows.map(x=>x[0]).sort((a,b)=>a-b)}}catch(e){if(String(e).includes("CAP"))return{complete:false,visits,peak,width,order};throw e}
}
// Independent block enumeration with signed offset; chain of triangles.
function blockDP(F,cap=65536){
let {q,b,paths,t}=F,visits=0,peak=0;const tick=()=>{if(visits===cap)throw Error("CAP");visits++};
try{let L=Array.from({length:q},()=>[]);for(let v=0;v<q;v++){let X=[[0,0]];for(let p of paths.filter(p=>p.u===v&&p.v===v)){let Y=new Map();for(let [c,w] of X)for(let r=0;r<=p.cap;r++){tick();if(c+r<=b)Y.set([c+r,w+r*p.L].join(),[c+r,w+r*p.L])}X=[...Y.values()]}L[v]=X}
let M=L[q-1];for(let i=q-3;i>=0;i-=2){let V=[i,i+1,i+2],edges=[[V[0],V[1]],[V[1],V[2]],[V[2],V[0]]],E=edges.map(([u,v])=>{let P=paths.filter(p=>p.u===u&&p.v===v),Q=paths.filter(p=>p.u===v&&p.v===u);assert(P.length===1&&Q.length===1,"one path each");let X=[];for(let a=0;a<=P[0].cap;a++)for(let c=0;c<=Q[0].cap;c++){tick();X.push([a,c,a*P[0].L+c*Q[0].L])}return X});let out=new Map();for(let x of E[0])for(let y of E[1])for(let z of E[2]){tick();if(x[0]-x[1]!==y[0]-y[1]||x[0]-x[1]!==z[0]-z[1])continue;let c0=x[0]+z[1],c1=y[0]+x[1],c2=z[0]+y[1];for(let [a,aw] of L[i])for(let [c,cw] of L[i+1])for(let [d,dw] of M){tick();if(a+c0>b||c+c1>b||d+c2>b)continue;let r=[a+c0,aw+cw+dw+x[2]+y[2]+z[2]];if(r[1]<=t)out.set(r.join(),r)}}M=[...out.values()];peak=Math.max(peak,M.length)}return{complete:true,visits,peak,support:[...new Set(M.map(x=>x[1]))].sort((a,b)=>a-b)}}catch(e){if(String(e).includes("CAP"))return{complete:false,visits,peak};throw e}
}
let jobs=[];
for(let [q,b] of [[3,1],[5,1],[7,1],[3,2]]){
let F=source(q,b),nativeInfo=native(F),min=Math.min(...F.owners.map(o=>o.length));assert(min>=2,"local closure");
let A=rawSearch(F),B=certificates(F),M=[[0,1],[0,2],[1,2]].map(([a,c])=>match(F,a,c)),C0=brute(F),E=eliminate(F),I=blockDP(F);
assert(A.status!=="YES"&&M.every(x=>x.ok)&&I.complete&&!I.support.includes(F.k)&&I.support.at(-1)===F.k+1,"family");
if(C0.complete)assert(C0.support.join()===I.support.join(),"brute");else assert(C0.support.every(x=>I.support.includes(x)),"partial");
if(E.complete)assert(E.support.join()===I.support.join(),"elimination");
jobs.push({q,b,t:F.t,k:F.k,...nativeInfo,min,A,B,M,C:C0,E,I})
}
let H=source(3,1,true),HD=blockDP(H),HE=eliminate(H);assert(HD.support.includes(H.k)&&HE.complete&&HE.support.includes(H.k),"hostile support");
let chosen=[H.paths.find(p=>p.u===0&&p.v===0&&p.L===4),H.paths.find(p=>p.u===1&&p.v===1&&p.L===5),H.paths.find(p=>p.u===2&&p.v===2&&p.L===5)],active=new Set(),arcs=[];for(let p of chosen)for(let i=0;i<p.L;i++){active.add(p.chain[i]);arcs.push([p.chain[i],p.chain[i+1]])}
let selected=[];for(let i=0;i<H.t;i++)if(!active.has(i))selected.push(H.ids.get([i,i,i].join()));[...active].forEach((i,j)=>selected.push(H.ids.get([i,H.t+j,H.t+j].join())));arcs.forEach(([i,j],g)=>selected.push(H.ids.get([H.t+g,i,j].join())));let SS=new Set(selected);assert(H.owners.every(o=>o.filter(x=>SS.has(x)).length===1),"hostile lift");
let triangle={q:3,b:1,t:3,paths:[{u:0,v:1,L:1,cap:1},{u:1,v:2,L:1,cap:1},{u:2,v:0,L:1,cap:1}]},tri=eliminate(triangle);assert(tri.complete&&tri.support.join()==="0,3","directed triangle");
return{CAP,gates,jobs,hostile:{k:H.k,witnessSize:selected.length,block:HD.visits,elimination:HE.visits},triangle:tri};

}
console.log(JSON.stringify(audit(),null,2));

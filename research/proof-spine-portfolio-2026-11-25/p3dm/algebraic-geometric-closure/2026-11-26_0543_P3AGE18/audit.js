// P3AGE18; run node audit.js. Deterministic native Hall-mode + modular Pfaffian audit.
function audit(){
const ck=(x,m)=>{if(!x)throw Error(m)},R=n=>Array.from({length:n},(_,i)=>i),key=(a,b)=>`${a},${b}`,eq=(a,b)=>String(a)===String(b);
function source(l){
 let V=l*l,E=[],H=[],T=[],del=[],extra=[];for(let y=0;y<l;y++)for(let x=0;x<l;x++){let u=y*l+x;if(x+1<l)E.push([u,u+1,1,x>0&&x+1<l-1&&y>0&&y<l-1&&(x-1)%3===0&&(y-1)%3===0]);if(y+1<l)E.push([u,u+l,0,false]);}
 E.forEach(([u,v,b],j)=>H.push([u,V+j,b,1],[v,V+j,b,1]));
 let n=V+E.length,inc=R(n).map(()=>[]);H.forEach(([u,v,b,c],i)=>{inc[u].push([i,b,0]);inc[v].push([i,c,1]);});
 let base=0;
 for(let v=0;v<n;v++){let d=2*inc[v].length;for(let k=0;k<inc[v].length;k++){let[e,bad,side]=inc[v][k],a=4*e,b=a+1,p=a+2+side;
 for(let j=0;j<2;j++)for(let s=0;s<2;s++){let i=2*k+j,dom=s===bad?(j?[p]:[a]):(j?[b,p]:[a,p]);for(let x of dom){let id=T.length;T.push([id,x,base+i,base+(i+s)%d]);if(e%2===0&&side===0&&E[e>>1][3]&&s!==bad){if(j===0&&x===a)del.push(id);if(j===1&&x===p)extra.push(id);}}}}
 base+=d;}return {T,E,del,extra};
}
function components(A){let seen=new Set,out=[];for(let i=0;i<A.length;i++)if(!seen.has(i)){let q=[i];seen.add(i);for(let j=0;j<q.length;j++)for(let u of A[q[j]])if(!seen.has(u)){seen.add(u);q.push(u)}out.push(q)}return out;}
function acquire(T,deleted=new Set){
 let P=[],pm=new Map,X=new Map,Y=new Map,Z=new Map;
 for(let t of T){let[id,x,y,z]=t,k=key(y,z);if(!pm.has(k)){pm.set(k,P.length);P.push({y,z,ts:[]});}let i=pm.get(k);P[i].ts.push(t);for(let [map,k]of [[X,x],[Y,y],[Z,z]]){if(!map.has(k))map.set(k,new Set);map.get(k).add(i)}}
 function adj(maps){let a=R(P.length).map(()=>[]);for(let map of maps)for(let vs of map.values()){let v=[...vs];for(let i=1;i<v.length;i++){a[v[0]].push(v[i]);a[v[i]].push(v[0])}}return a}
 let regions=components(adj([Y,Z])),mode=Array(P.length),which=Array(P.length);
 regions.forEach((C,r)=>{ck(C.every(i=>Y.get(P[i].y).size===2&&Z.get(P[i].z).size===2),"degree");let a=C.slice().sort((i,j)=>P[i].y-P[j].y||P[i].z-P[j].z)[0],q=[a];mode[a]=0;for(let j=0;j<q.length;j++){let i=q[j];which[i]=r;for(let u of [...Y.get(P[i].y),...Z.get(P[i].z)])if(u!==i){if(mode[u]===undefined){mode[u]=1-mode[i];q.push(u)}else ck(mode[u]!==mode[i],"cycle parity")}}ck(q.length===C.length,"cycle coverage")});
 let factors=[];for(let C of components(adj([X]))){let scope=[...new Set(C.map(i=>which[i]))].sort((a,b)=>a-b),owners=new Set(C.flatMap(i=>P[i].ts.map(t=>t[1]))),table=[],lifts=[];ck(scope.length===2,"scope");for(let a=0;a<2;a++)for(let b=0;b<2;b++){let w=[a,b],L=C.filter(i=>mode[i]===w[scope.indexOf(which[i])]),out=[];function rec(k,U,S){if(k===L.length){if(U.size===owners.size)out.push(S);return}for(let t of P[L[k]].ts)if(!deleted.has(t[0])&&!U.has(t[1]))rec(k+1,new Set([...U,t[1]]),[...S,t[0]])}if(L.length===owners.size)rec(0,new Set,[]);lifts.push(out);table.push(out.length)}factors.push({scope,table,lifts,ids:C.flatMap(i=>P[i].ts.map(t=>t[0]))})}
 return {P,regions,mode,which,n:regions.length,factors};
}
function solve(A,pins=[]){
 let n=A.n,g=R(2*n).map(()=>[]),rev=R(2*n).map(()=>[]);function arc(i,j){g[i].push(j);rev[j].push(i)}function clause(i,a,j,b){arc(2*i+1-a,2*j+b);arc(2*j+1-b,2*i+a)}
 for(let f of A.factors)for(let k=0;k<4;k++)if(!f.table[k])clause(f.scope[0],1-(k>>1),f.scope[1],1-(k&1));for(let[i,a]of pins)clause(i,a,i,a);
 let seen=new Set,ord=[];function dfs(i){if(seen.has(i))return;seen.add(i);for(let j of g[i])dfs(j);ord.push(i)}for(let i=0;i<2*n;i++)dfs(i);let C=Array(2*n).fill(-1),c=0;function mark(i){if(C[i]>=0)return;C[i]=c;for(let j of rev[i])mark(j)}for(let i of ord.reverse())if(C[i]<0){mark(i);c++}
 if(R(n).some(i=>C[2*i]===C[2*i+1]))return null;let w=R(n).map(i=>Number(C[2*i+1]>C[2*i]));ck(pins.every(([i,a])=>w[i]===a)&&A.factors.every(f=>f.table[2*w[f.scope[0]]+w[f.scope[1]]]),"SCC word");return w
}
function lift(A,w,f0=null,L=null){return new Set(A.factors.flatMap(f=>f===f0?L:f.lifts[2*w[f.scope[0]]+w[f.scope[1]]][0]))}
function valid(T,S){let r=new Map;for(let t of T)for(let c=1;c<=3;c++){let k=key(c,t[c]);r.set(k,(r.get(k)||0)+Number(S.has(t[0])))}return [...r.values()].every(x=>x===1)}
function closure(T,deleted){let r=new Map,P=new Map([...deleted].map(i=>[i,0]));for(let t of T)for(let c=1;c<=3;c++){let k=key(c,t[c]);if(!r.has(k))r.set(k,[]);r.get(k).push(t[0])}for(let change=true;change;){change=false;for(let row of r.values()){let o=row.filter(i=>P.get(i)===1),u=row.filter(i=>!P.has(i));if(o.length>1||!o.length&&!u.length)return null;if(o.length)for(let i of u){P.set(i,0);change=true}else if(u.length===1){P.set(u[0],1);change=true}}}return P}
function eliminate(A,l){
 let adj=R(A.n).map(()=>[]);for(let f of A.factors){let[u,v]=f.scope;adj[u].push([v,f]);adj[v].push([u,f])}let c=Array(A.n).fill(-1),q=[0];c[0]=0;for(let j=0;j<q.length;j++)for(let[v]of adj[q[j]])if(c[v]<0){c[v]=1-c[q[j]];q.push(v)}else ck(c[v]!==c[q[j]],"bipartite");
 for(let side=0;side<2;side++){let K=R(A.n).filter(i=>c[i]===side),D=R(A.n).filter(i=>c[i]!==side);if(K.length!==l*l||D.some(i=>adj[i].length!==2))continue;
 let E=[],G=new Map(K.map(i=>[i,[]]));for(let i of D){let[[u,f],[v,g]]=adj[i],at=(h,j,a,b)=>h.table[h.scope[0]===j?2*a+b:2*b+a],T=[];for(let a=0;a<2;a++)for(let b=0;b<2;b++)T.push(at(f,u,a,0)*at(g,v,b,0)+at(f,u,a,1)*at(g,v,b,1));E.push({u,v,T});G.get(u).push(v);G.get(v).push(u)}
 let C=K.filter(i=>G.get(i).length===2),a=C[0];function dist(s){let q=[s],d=new Map([[s,0]]);for(let j=0;j<q.length;j++)for(let v of G.get(q[j]))if(!d.has(v)){d.set(v,d.get(q[j])+1);q.push(v)}return d}let da=dist(a),b=C.find(v=>da.get(v)===l-1);if(b===undefined)continue;let db=dist(b),coords=new Map(K.map(v=>{let x=(da.get(v)-db.get(v)+l-1)/2,y=da.get(v)-x;return [v,[x,y]]}));if([...coords.values()].some(([x,y])=>!Number.isInteger(x)||!Number.isInteger(y)||x<0||x>=l||y<0||y>=l)||new Set([...coords.values()].map(String)).size!==K.length)continue;
 let F=E.map(({u,v,T})=>{let[x,y]=coords.get(u),[xx,yy]=coords.get(v);return {u:y*l+x,v:yy*l+xx,T,h:y===yy,ok:Math.abs(x-xx)+Math.abs(y-yy)===1}});if(F.some(e=>!e.ok)||F.length!==2*l*(l-1))continue;return F;
 }throw Error("not grid");
}
function normalize(E){let h=E.find(e=>e.h).T[0];ck(E.every(e=>eq(e.T,e.h?(h===5?[5,2,2,1]:[1,2,2,5]):(h===5?[1,2,2,5]:[5,2,2,1]))),"unperturbed grid matrices");return h===5?E:E.map(e=>({...e,T:e.T.slice().reverse()}))}
function transfer(l){let L=1<<l,H=[],V=[];for(let s=0;s<L;s++){let p=1n;for(let x=0;x<l-1;x++)p*=BigInt([5,2,2,1][2*((s>>x)&1)+((s>>(x+1))&1)]);H.push(p);let row=[];for(let t=0;t<L;t++){let z=1n;for(let x=0;x<l;x++)z*=BigInt([1,2,2,5][2*((s>>x)&1)+((t>>x)&1)]);row.push(z)}V.push(row)}let D=H.slice();for(let y=1;y<l;y++)D=H.map((h,t)=>h*D.reduce((a,v,s)=>a+v*V[s][t],0n));return D.reduce((a,b)=>a+b,0n)}
function pfGrid(l,p,E){
 const mod=x=>((x%p)+p)%p,pow=(x,n)=>{let z=1;for(x=mod(x);n;n=Math.floor(n/2),x=x*x%p)if(n%2)z=z*x%p;return z},inv=x=>pow(x,p-2);
 let q=pow(5,(p+1)/4);ck(q*q%p===5,"sqrt5");let n=l*l,rot=R(n).map(()=>[]),sp=new Map,exp=Array(n).fill(0);
 for(let {u,v,h}of E){exp[u]+=h?1:-1;exp[v]+=h?1:-1;sp.set(key(Math.min(u,v),Math.max(u,v)),[1,2*inv(q)%p]);rot[u].push(v);rot[v].push(u)}
 let bd=R(n).filter(i=>exp[i]),apex=bd.length?n:-1;
 if(apex>=0){let rim=[];for(let x=0;x<l;x++)rim.push(x);for(let y=1;y<l;y++)rim.push(y*l+l-1);for(let x=l-2;x>=0;x--)rim.push((l-1)*l+x);for(let y=l-2;y>0;y--)rim.push(y*l);rot.push(rim.filter(i=>exp[i]).reverse());for(let u of bd){rot[u].push(apex);sp.set(key(u,apex),[exp[u]>0?pow(q,exp[u]):pow(inv(q),-exp[u]),1])}}
 for(let u=0;u<n;u++){let x=u%l,y=Math.floor(u/l);function angle(v){if(v===apex)return y===0?3:x===l-1?0:y===l-1?1:2;return v===u+1?0:v===u+l?1:v===u-1?2:3}rot[u].sort((a,b)=>angle(a)-angle(b))}
 let A=[],W=new Map,ref=[],port=new Map;function node(){A.push([]);return A.length-1}function edge(a,b,w){let k=key(Math.min(a,b),Math.max(a,b));ck(!W.has(k),"duplicate");W.set(k,mod(w))}function pair(a,b){ref.push([Math.min(a,b),Math.max(a,b)])}
 for(let u=0;u<rot.length;u++){let d=rot[u].length+(rot[u].length%2),C=R(d).map(()=>[node(),node(),node()]);ck(d>=2,"city");for(let i=0;i<d;i++){let[a,t,b]=C[i],prev=C[(i+d-1)%d][2],next=C[(i+1)%d][0];edge(a,t,1);edge(t,b,1);edge(a,b,1);edge(b,next,1);A[a]=[prev,t,b];A[b]=[a,t,next];A[t]=[a,b];if(i<rot[u].length)port.set(key(u,rot[u][i]),t);if(i%2===0){pair(a,t);pair(b,next)}else pair(t,b)}}
 for(let[k,[s,d]]of sp){let[u,v]=k.split(",").map(Number),t=port.get(key(u,v)),z=port.get(key(v,u)),a=node(),b=node();edge(t,a,mod(s-d));edge(a,b,mod(s+d));edge(b,z,1);A[t].splice(1,0,a);A[z].splice(1,0,b);A[a]=[t,b];A[b]=[a,z];pair(a,b)}
 let N=A.length;ck(N%2===0&&new Set(ref.flat()).size===N,"reference");
 let face=[],of=new Map;for(let u=0;u<N;u++)for(let v of A[u])if(!of.has(key(u,v))){let f=[],a=u,b=v;do{ck(!of.has(key(a,b)),"dart");of.set(key(a,b),face.length);f.push([a,b]);let c=A[b][(A[b].indexOf(a)+1)%A[b].length];a=b;b=c}while(a!==u||b!==v);face.push(f)}ck(N-W.size+face.length===2,"Euler");
 let D=face.map(()=>[]),sign=new Map;for(let k of W.keys()){let[a,b]=k.split(",").map(Number),i=of.get(key(a,b)),j=of.get(key(b,a));sign.set(k,1);if(i!==j){D[i].push([j,k]);D[j].push([i,k])}}let ord=[0],par=new Map([[0,null]]);for(let i=0;i<ord.length;i++)for(let[j,k]of D[ord[i]])if(!par.has(j)){par.set(j,k);ord.push(j)}ck(ord.length===face.length,"dual");
 function odd(f){return f.reduce((s,[a,b])=>s^Number(sign.get(key(Math.min(a,b),Math.max(a,b)))===(a<b?1:-1)),0)}for(let i=ord.length-1;i>0;i--){let f=ord[i],k=par.get(f);if(!odd(face[f]))sign.set(k,-sign.get(k))}ck(ord.slice(1).every(f=>odd(face[f])),"orientation");
 ref.sort((a,b)=>a[0]-b[0]);let seq=ref.flat(),sg=1;for(let i=0;i<N;i++)for(let j=i+1;j<N;j++)if(seq[i]>seq[j])sg=-sg;for(let[a,b]of ref)sg*=sign.get(key(a,b));
 let M=R(N).map(()=>new Float64Array(N));for(let[k,w]of W){let[a,b]=k.split(",").map(Number);M[a][b]=mod(sign.get(k)*w);M[b][a]=mod(-M[a][b])}
 let pf=1;for(let i=0;i<N;i+=2){let j=i+1;while(j<N&&!M[i][j])j++;if(j===N){pf=0;break}if(j!==i+1){[M[j],M[i+1]]=[M[i+1],M[j]];for(let r=0;r<N;r++) [M[r][j],M[r][i+1]]=[M[r][i+1],M[r][j]];pf=mod(-pf)}let v=M[i][i+1],iv=inv(v);pf=pf*v%p;for(let a=i+2;a<N;a++){let x=M[i][a]*iv%p,y=M[i+1][a]*iv%p;for(let b=a+1;b<N;b++){let z=mod(M[a][b]-x*M[i+1][b]+y*M[i][b]);M[a][b]=z;M[b][a]=z?p-z:0}}}
 let value=mod(sg*pf)*pow(inv(2),sp.size)%p;if(apex>=0)value=value*inv(2)%p;value=value*pow(5,l*(l-1))%p;return {value,N,faces:face.length,anchor:apex>=0?1:0};
}
function primes(){let out=[];for(let p=100003;out.length<25;p+=4){if(p%5!==1&&p%5!==4)continue;let ok=true;for(let d=3;d*d<=p;d+=2)if(p%d===0){ok=false;break}if(ok)out.push(p)}return out}
function invBig(a,p){let r=1n;for(let n=p-2n;n;n>>=1n,a=a*a%p)if(n&1n)r=r*a%p;return r}
function nativeCount(T){let rows=new Map;for(let t of T)for(let c=1;c<=3;c++){let k=key(c,t[c]);if(!rows.has(k))rows.set(k,[]);rows.get(k).push(t[0])}let K=[...rows.keys()],I=new Map(K.map((k,i)=>[k,i])),M=T.map(t=>t.slice(1).reduce((s,v,c)=>s|1n<<BigInt(I.get(key(c+1,v))),0n)),memo=new Map;function f(m){if(!m)return 1n;if(memo.has(m))return memo.get(m);let best=null;for(let j=0;j<K.length;j++)if(m>>BigInt(j)&1n){let a=rows.get(K[j]).filter(i=>(m&M[i])===M[i]);if(best===null||a.length<best.length)best=a;if(!a.length)break}let v=best.reduce((s,i)=>s+f(m^M[i]),0n);memo.set(m,v);return v}return f((1n<<BigInt(K.length))-1n)}
let results=[],neighbors=[],hostile=[],P=primes();
for(let l of [2,3,4,5]){
 let {T}=source(l),A=acquire(T),E=normalize(eliminate(A,l)),sizes=[1,2,3].map(c=>new Set(T.map(t=>t[c])).size);ck(sizes.every(x=>x===sizes[0])&&new Set(T.map(t=>String(t.slice(1)))).size===T.length,"native source");ck(closure(T,new Set).size===0,"initial closure");let yes=new Set,no=new Set,witnessTests=0;
 for(let f of A.factors)for(let k=0;k<4;k++)if(f.table[k]){let w=solve(A,[[f.scope[0],k>>1],[f.scope[1],k&1]]);ck(w,"extendible");for(let L of f.lifts[k]){let S=lift(A,w,f,L);ck(valid(T,S),"source lift");for(let id of f.ids)(S.has(id)?yes:no).add(id);witnessTests++}}ck(yes.size===T.length&&no.size===T.length,"semantic unary support");
 let z=transfer(l),bound=1n<<BigInt(A.n+A.factors.length),r=0n,M=1n,checks=[],fullCRT=l<=4;for(let p of P){let a=pfGrid(l,p,E),bp=BigInt(p);ck(BigInt(a.value)===z%bp,"Pfaffian mismatch");checks.push({p,...a});let t=((BigInt(a.value)-r%bp+bp)%bp)*invBig(M%bp,bp)%bp;r+=M*t;M*=bp;if(!fullCRT||M>bound)break}if(fullCRT)ck(M>bound&&r===z,"CRT");
 if(l===2)ck(nativeCount(T)===z,"independent native owner-mask count");
 let f=A.factors[0],bad=f.table.indexOf(0),d=[];for(let[i,b]of [[f.scope[0],bad>>1],[f.scope[1],bad&1]]){let j=A.regions[i].find(j=>A.mode[j]!==b&&A.P[j].ts.length===2);d.push(...A.P[j].ts.map(t=>t[0]))}let good=new Set(d.slice(0,-1)),badset=new Set(d),G=acquire(T,good),B=acquire(T,badset),w=solve(G);ck(w&&valid(T,lift(G,w))&&[...good].every(i=>!lift(G,w).has(i))&&!solve(B),"deletion neighbor");for(let c=1;c<=3;c++)ck(new Set(T.filter(t=>!badset.has(t[0])).map(t=>t[c])).size===sizes[c-1],"no isolated owner");let cl=closure(T,badset);neighbors.push({l,positiveDeleted:[...good],negativeAdditional:d.at(-1),negativeUnitClosure:cl===null,YES:true,NO:true});
 results.push({l,triples:T.length,modes:A.n,binaryFactors:A.factors.length,witnessTests,count:z.toString(),crtExact:fullCRT,modulusBits:M.toString(2).length,checks,independentNativeCount:l===2});
}
for(let l of [4,6,9,12]){
 let {T,del,extra}=source(l),A=acquire(T),B=acquire(T,new Set(del)),S=acquire(T,new Set([...del,...extra])),by=new Set(B.factors.flatMap(f=>f.lifts.flat(2)));
 ck(extra.every(i=>!by.has(i))&&T.every(t=>del.includes(t[0])||extra.includes(t[0])||by.has(t[0])),"exact support pruning");
 ck(B.factors.every((f,i)=>eq(f.table.map(Boolean),A.factors[i].table.map(Boolean))&&eq(f.table,S.factors[i].table)),"same binary support");
 let w=solve(S),s=lift(S,w);ck(valid(T,s)&&[...del,...extra].every(i=>!s.has(i)),"hostile lift");
 let E=eliminate(S,l),num=R(l*l).map(()=>1n),den=num.slice();for(let {u,v,T:[a,b,c,d]}of E){ck(a*b*c*d>0,"positive table");num[u]*=BigInt(a*b);den[u]*=BigInt(c*d);num[v]*=BigInt(a*c);den[v]*=BigInt(b*d)}
 let interior=R(l*l).filter(i=>i%l>0&&i%l<l-1&&Math.floor(i/l)>0&&Math.floor(i/l)<l-1&&num[i]!==den[i]).length;ck(interior===2*del.length,"field count");
 let p=closure(T,new Set([...del,...extra]));ck(p!==null,"hostile initial closure");
 hostile.push({l,originalTriples:T.length,explicitDeletions:del.length,certifiedAdditionalUnsupported:extra.length,remainingTriples:T.length-del.length-extra.length,interiorFields:interior,fixedEmbeddingFaceCoverLowerBound:Math.ceil(interior/4),unitPins:p.size,sourceWitness:true});
}
return {results,neighbors,hostile};
}
console.log(JSON.stringify(audit(),null,2));

// Run: node 2026-11-25_1740_T5S07_audit.js
const audit = function(){
let checks=0, scans=0, nodes=0;
const ok=(p)=>{checks++;if(!p)throw Error("assertion "+checks)};
const mod=x=>(x%5+5)%5, R=(a,b)=>[1,3].includes(mod(b-a)), C=(a,b,c)=>R(a,b)&&R(b,c)&&R(c,a)||R(b,a)&&R(c,b)&&R(a,c);
const A=(a,b)=>[1,4].includes(mod(b-a)), range=n=>Array.from({length:n},(_,i)=>i), words=(n,fn,a=[])=>{if(a.length===n){fn(a);return}for(let i=0;i<5;i++)words(n,fn,[...a,i])};
let ct=[0,0,0,0,0,0], frames=0;
words(3,([a,b,c])=>{let h=(x,y,z)=>new Set([x,y,z]).size===3&&R(x,y)!==R(x,z);let q=R(a,b)!==R(a,c);let p=R(a,b)&&R(a,c);let s=R(a,c)&&R(b,c);ct[0]+=+C(a,b,c);ct[1]+=+h(a,b,c);ct[2]+=+q;ct[3]+=+p;ct[4]+=+s;ct[5]+=+(s&&new Set([a,b,c]).size===3);ok(C(a,b,c)===(h(a,b,c)&&h(b,a,c)))});
ok(JSON.stringify(ct)===JSON.stringify([30,40,60,20,20,10]));
words(5,a=>{let yes=range(5).every(i=>C(a[i],a[(i+1)%5],a[(i+2)%5]));let frame=[1,4].some(d=>a.every((x,i)=>x===mod(a[0]+d*i)));ok(yes===frame);frames+=+yes});
for(let b=0;b<5;b++)ok([2,3,4].every(j=>range(5).some(h=>C(j,b,h)))===(b<2));
for(let p=0;p<2;p++)for(let q=0;q<2;q++){
let o=[];words(3,([x,y,z])=>{if(x<2&&C(1,2,y)&&C(0,1,z)&&C(4,p,y)&&C(3,q,z)&&C(x,y,z))o.push(x)});
ok(o.length===1&&o[0]===(p|q));ok(range(2).filter(x=>C(2,p,x)).join("")===String(1-p));}
ok(range(2).filter(o=>C(0,2,o)).join("")==="1");
let gp=new Set,chart=new Set;words(5,([a,u,v,b,h])=>{if(C(a,u,v)&&C(u,v,b)&&C(a,h,b)){gp.add(u+":"+v);if(mod(a+v-2*u)===0&&mod(u+b-2*v)===0&&mod(a+b-2*h)===0&&A(u,a)&&A(v,b)&&A(h,a))chart.add(u+":"+v)}});
for(let u=0;u<5;u++)for(let v=0;v<5;v++){ok(gp.has(u+":"+v)===A(u,v));ok(chart.has(u+":"+v)===A(u,v))}
let residues=new Set;for(let a of [1,4])for(let b of [1,4])for(let c of [1,4])residues.add(mod(a+b+c));ok(residues.size===4&&!residues.has(0));
const complete=n=>range(n).flatMap(u=>range(n).filter(v=>v>u).map(v=>[u,v]));
const bip=(a,b)=>range(a).flatMap(u=>range(b).map(v=>[u,a+v]));
const cycle=n=>range(n).map(i=>[i,(i+1)%n]);
const blow=(E,k)=>E.flatMap(([u,v])=>range(k).flatMap(i=>range(k).map(j=>[u*k+i,v*k+j])));
function comps(n,E){let p=range(n);const f=x=>{while(p[x]!==x)x=p[x];return x};for(let [u,v] of E)p[f(u)]=f(v);return new Set(p.map(f)).size}
function matrix(n,E){let T=[],ch=[];for(let e of E){if(comps(n,[...T,e])<comps(n,T))T.push(e);else ch.push(e)}let ordered=[...T,...ch];let rows=ch.map(([u,v],i)=>{let a=Array(ordered.length).fill(0),seen=new Set([v]),Q=[[v,[]]];while(Q.length){let [x,path]=Q.shift();if(x===u){for(let [j,s] of path)a[j]=s;break}T.forEach(([s,t],j)=>{let y=x===s?t:x===t?s:-1;if(y>=0&&!seen.has(y)){seen.add(y);Q.push([y,[...path,[j,x===s?1:4]]])}})}a[T.length+i]=1;return a});return {ordered,rows}}
function rank(M){if(!M.length)return 0;let a=M.map(r=>r.map(mod)),r=0;for(let j=0;j<a[0].length&&r<a.length;j++){let i=a.findIndex((x,k)=>k>=r&&x[j]);if(i<0)continue;[a[i],a[r]]=[a[r],a[i]];let z=[0,1,3,2,4][a[r][j]];a[r]=a[r].map(x=>mod(x*z));for(let k=r+1;k<a.length;k++){let t=a[k][j];if(t)a[k]=a[k].map((x,l)=>mod(x-t*a[r][l]))}r++}return r}
let subsetChecks=0, syndromeChecks=0;
for(let [n,E] of [[5,complete(5)],[8,bip(4,4)]]){
let {ordered,rows}=matrix(n,E);
for(let mask=1;mask<2**E.length;mask++){
let J=range(E.length).filter(j=>mask&(1<<j)),rest=ordered.filter((_,j)=>!(mask&(1<<j))),r=J.length-comps(n,rest)+1;
ok(J.length<=2*r&&2n**BigInt(J.length)<5n**BigInt(r));subsetChecks++;
if(n===5||mask%257===0){ok(rank(rows.map(row=>J.map(j=>row[j])))===r)}
if(n===5){let S=new Set;for(let k=0;k<2**J.length;k++){S.add(rows.map(row=>mod(J.reduce((s,j,i)=>s+row[j]*((k>>i&1)?1:-1),0))).join(""))}ok(S.size<5**r);syndromeChecks++;}
}}
function close(D,E){let change=true;while(change){change=false;for(let [u,v] of E)for(let [a,b] of [[u,v],[v,u]]){scans++;let q=D[a].filter(x=>D[b].some(y=>A(x,y)));if(!q.length)return false;if(q.length!==D[a].length){D[a]=q;change=true}}}return true}
function solve(n,E,D=range(n).map(()=>range(5))){nodes++;D=D.map(a=>a.slice());if(!close(D,E))return null;let u=D.findIndex(a=>a.length>1);if(u<0)return D.map(a=>a[0]);for(let a of D[u]){let Q=D.map(x=>x.slice());Q[u]=[a];let w=solve(n,E,Q);if(w)return w}return null}
function lift(E,x){for(let [u,v] of E){let t=mod(x[v]-x[u]),a=mod(x[u]-t),b=mod(x[v]+t),h=mod(x[u]+3*t);ok(A(x[u],x[v])&&C(a,x[u],x[v])&&C(x[u],x[v],b)&&C(a,h,b));ok(A(x[u],a)&&A(x[v],b)&&A(h,a)&&mod(a+x[v]-2*x[u])===0&&mod(x[u]+b-2*x[v])===0&&mod(a+b-2*h)===0)}}
let controls=[];
for(let [n,E,expect] of [[3,complete(3),false],[5,cycle(5),true],[2,[[0,1]],true],[5,complete(5),false]]){
let w=solve(n,E),F=blow(E,4),z=solve(4*n,F);ok(!!w===expect&&!!z===expect);
if(z)lift(F,z);controls.push({n,edges:E.length,blown_n:n*4,blown_edges:F.length,sat:!!z});
}
let affine=[];
for(let k of [6,8,10]){
let n=k*k,E=[];for(let i=0;i<k;i++)for(let j=0;j<k;j++)E.push([i*k+j,i*k+(j+1)%k],[i*k+j,((i+1)%k)*k+j]);
let {ordered,rows}=matrix(n,E);let side=v=>((Math.floor(v/k)+v%k)%2);let x=range(n).map(side),diff=x=>ordered.map(([u,v])=>mod(x[v]-x[u]));let W=[diff(x)];for(let v=0;v<n;v++){let p=range(n).map(u=>side(u)===side(v)?1:0);let a=diff(p);p[v]=4;let b=diff(p);W.push(a.map((z,j)=>mod(b[j]-z)));ok(b.every(t=>t===1||t===4));}ok(rank(W.slice(1))===n-1);ok(close(range(n).map(()=>range(5)),E));lift(E,x);affine.push({k,n,m:E.length,r:rows.length,affine_rank:n-1});
}
return {checks,relationCounts:ct,frames,subsetChecks,syndromeChecks,scans,nodes,controls,affine};
};
console.log(JSON.stringify(audit(),null,2));

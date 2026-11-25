// T5S03: node 18+; exact neighborhood reference and guarded support/sign solver.
const D=[-1,0,1], Z=[0,1,2,3,4];
function* product(A,n,p=[]){if(!n){yield p;return;}for(const x of A)yield* product(A,n-1,[...p,x]);}
const mod=x=>(x+10)%5, R=(a,b)=>[1,3].includes(mod(b-a));
const C=(a,b,c)=>new Set([a,b,c]).size===3 && Z.some(i=>[a,b,c].every(x=>[i,mod(i+1),mod(i+2)].includes(x)));
const T=[[-1,-1,-1],[-1,-1,1],[-1,1,1],[0,0,0],[0,1,-1],[1,-1,0],[1,1,1]];
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
let checks=0, scans=0, nodes=0, conflicts=0, signEdges=0, zeroForces=0;
function assert(x){checks++;if(!x)throw Error('assert '+checks);}
function good(a,t,x){return C(...t.map(i=>mod(a[i]+x[i])));}
function roles(a,t){for(const l of t)for(const m of t)for(const r of t)if(new Set([l,m,r]).size===3&&mod(a[m]-a[l])===1&&mod(a[r]-a[m])===1)return [l,m,r];throw Error('bad owner');}
const copy=d=>d.map(q=>q.slice());
function gac(dom,rs){let changed=true;while(changed){changed=false;for(const [t,tab] of rs){scans++;let p=tab.filter(v=>t.every((i,k)=>dom[i].includes(v[k])));if(!p.length)return false;for(let j=0;j<3;j++){let i=t[j],d=dom[i].filter(v=>p.some(q=>q[j]===v));if(d.length!==dom[i].length){dom[i]=d;changed=true;}}}}return true;}
function maxSupport(dom,rs){let s=dom.map(d=>d.some(v=>v!==0)),ch=true;while(ch){ch=false;for(const [l,m,r] of rs){let off=!s[m]?[l,r]:!s[l]&&!s[r]?[m]:[];for(const i of off)if(s[i]){s[i]=false;ch=true;}}}return s.some((v,i)=>!v&&!dom[i].includes(0))?null:s;}
function signs(dom,rs,s){let pos=new Map(),neg=new Map(),edges=dom.map(()=>[]);
const put=(m,i,h)=>{if(!m.has(i))m.set(i,h);};
for(let i=0;i<s.length;i++)if(s[i]){if(!dom[i].includes(-1))put(pos,i,[i]);if(!dom[i].includes(1))put(neg,i,[i]);}
for(const t of rs){let [l,m,r]=t;if(s[l]&&s[r]){edges[l].push([m,t]);edges[m].push([r,t]);signEdges+=2;}else if(s[l]){put(pos,l,[l,m]);put(neg,m,[l,m]);}else if(s[r]){put(pos,m,[m,r]);put(neg,r,[m,r]);}}
let q=[...pos.keys()];for(let k=0;k<q.length;k++){let u=q[k];if(neg.has(u)){let hit=[...new Set([...pos.get(u),...neg.get(u)])];return {hit};}for(const [v,t] of edges[u])if(!pos.has(v)){pos.set(v,[...new Set([...pos.get(u),...t])]);q.push(v);}}
return {word:s.map((v,i)=>!v?0:pos.has(i)?1:-1)};
}
function solve(a,goodOwners,d,cap=Infinity,hcap=Infinity){
let n=a.length,rs=goodOwners.map(t=>roles(a,t)),dt=[...product(D,3)].filter(x=>C(...d.map((i,k)=>mod(a[i]+x[k])))),all=[...rs.map(t=>[t,T]),[d,dt]],root=Array.from({length:n},()=>D.slice());
assert(goodOwners.every(t=>good(a,t,Array(n).fill(0)))&&!good(a,d,Array(n).fill(0)));
if(!gac(root,all))return {status:'NO'};let unknown=false;
function branch(dom,depth){nodes++;let s;
while(true){if(!gac(dom,all))return {status:'NO'};s=maxSupport(dom,rs);if(!s)return {status:'NO'};let ch=false;for(let i=0;i<n;i++)if(!s[i]&&dom[i].length!==1){dom[i]=[0];zeroForces++;ch=true;}if(!ch)break;}
let z=signs(dom,rs,s);if(z.word){assert([...goodOwners,d].every(t=>good(a,t,z.word)));return {status:'YES',word:z.word};}
conflicts++;assert(z.hit.every(i=>s[i]));if(depth===cap||z.hit.length>hcap)return {status:'UNKNOWN',hit:z.hit};let u=false;
for(const i of z.hit){if(!dom[i].includes(0))continue;let f=copy(dom);f[i]=[0];let r=branch(f,depth+1);if(r.status==='YES')return r;if(r.status==='UNKNOWN')u=true;}return {status:u?'UNKNOWN':'NO'};
}
for(const p of dt){if(!d.every((i,k)=>root[i].includes(p[k])))continue;let f=copy(root);d.forEach((i,k)=>f[i]=[p[k]]);let r=branch(f,0);if(r.status==='YES')return r;if(r.status==='UNKNOWN')unknown=true;}return {status:unknown?'UNKNOWN':'NO'};
}
function reference(a,gs,d,local=true){for(const x of product(local?D:Z,a.length)){if(local?[...gs,d].every(t=>good(a,t,x)):[...gs,d].every(t=>C(...t.map(i=>x[i]))))return x;}return null;}
function audit(){
// Exact definition firewall and anchored circuit truth tables.
let counts=[0,0,0,0];
for(const [x,y,z] of product(Z,3)){let cyc=(R(x,y)&&R(y,z)&&R(z,x))||(R(x,z)&&R(z,y)&&R(y,x));assert(C(x,y,z)===cyc);counts[0]+=+cyc;counts[1]+=+(new Set([x,y,z]).size===3&&R(x,y)!==R(x,z));counts[2]+=+(R(x,y)!==R(x,z));counts[3]+=+(R(x,y)&&R(x,z));}
assert(eq(counts,[30,40,60,20]));
for(let k=0;k<5;k++)for(const p of product(D,3))assert(C(...p.map((v,i)=>mod(k+i+v)))===T.some(t=>eq(t,p)));
for(const x of Z)for(const y of Z)assert(Z.some(h=>C(x,y,h))===(x!==y));
for(const x of Z)assert([2,3,4].every(j=>Z.some(h=>C(j,x,h)))===[0,1].includes(x));
for(const p of [0,1])for(const x of [0,1])assert(C(2,p,x)===(x===1-p));
for(const p of [0,1])for(const q of [0,1])for(const x of [0,1])assert([...product(Z,2)].some(([y,z])=>C(1,2,y)&&C(0,1,z)&&C(4,p,y)&&C(3,q,z)&&C(x,y,z))===(x===(p||q)));
for(const x of [0,1])assert(C(0,2,x)===(x===1));
// The 9-vertex counterexample defeats ALL maximal-support defect-tuple tracks even after GAC.
let a=[2,0,2,1,2,3,1,3,4], gs=[[4,5,8],[1,4,6],[2,7,8],[4,7,8],[1,3,8],[0,3,5]], d=[0,1,7];
let w=[1,-1,-1,0,-1,-1,-1,-1,1];assert([...gs,d].every(t=>good(a,t,w)));let r0=solve(a,gs,d,0),r1=solve(a,gs,d,1);assert(r0.status==='UNKNOWN');assert(r1.status==='YES');
let explicit={a,gs,d,w,cap0:r0,cap1:r1};
let b=[0,1,2,3],bg=[[0,1,2],[1,2,3]],bd=[0,1,3];assert(reference(b,bg,bd,false)===null);assert(solve(b,bg,bd).status==='NO');
let seed=20261125;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;}
let stat={localYes:0,localNo:0,maxYes:0,maxUnknown:0,cap1Yes:0,cap1Unknown:0,fullYes:0,fullNo:0,fullYesLocalNo:0};
for(let j=0;j<120;j++){let n=5+j%4,a=Array.from({length:n},()=>rnd(5)),g=[],bad=[];for(let l=0;l<n;l++)for(let m=l+1;m<n;m++)for(let r=m+1;r<n;r++)(C(a[l],a[m],a[r])?g:bad).push([l,m,r]);if(!g.length||!bad.length){j--;continue;}let d=bad[rnd(bad.length)];g=g.filter(()=>rnd(5)!==0);if(!g.length){j--;continue;}
let ref=reference(a,g,d),r=solve(a,g,d),q=solve(a,g,d,0),q1=solve(a,g,d,1);assert((r.status==='YES')===!!ref&&r.status!=='UNKNOWN');assert(q.status==='UNKNOWN'||q.status===r.status);assert(q1.status==='UNKNOWN'||q1.status===r.status);
stat[ref?'localYes':'localNo']++;if(q.status==='YES')stat.maxYes++;if(q.status==='UNKNOWN')stat.maxUnknown++;if(q1.status==='YES')stat.cap1Yes++;if(q1.status==='UNKNOWN')stat.cap1Unknown++;
if(j<32){let full=reference(a,g,d,false);stat[full?'fullYes':'fullNo']++;if(full&&!ref)stat.fullYesLocalNo++;assert(!ref||!!full);}
}
return {seed:20261125,counts,checks,scans,nodes,conflicts,signEdges,zeroForces,stat,explicit};
}
const results=audit();
console.log(JSON.stringify(results,null,2));

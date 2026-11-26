function audit(){
const pairs=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)pairs.push([i,j]);const bit=(a,b)=>1<<pairs.findIndex(([i,j])=>i===Math.min(a,b)&&j===Math.max(a,b));
const perms=(a)=>a.length===0?[[]]:a.flatMap((x,i)=>perms(a.filter((_,j)=>j!==i)).map(p=>[x,...p]));const P=perms([0,1,2,3,4]);const cycles=[...new Set(P.flatMap(p=>[3,4,5].map(k=>p.slice(0,k).reduce((s,a,i)=>s|bit(a,p[(i+1)%k]),0))))].sort((a,b)=>a-b);
const signature=m=>cycles.filter(c=>!(c&m)).join(",");const count=m=>m.toString(2).replace(/0/g,"").length;const check=(b,msg)=>{if(!b)throw Error(msg);checks++};let checks=0,queries=0,visits=0,switches=0,lifts=0;
const base=[
{e:[[0,1],[0,2],[0,3],[1,3],[2,3]],p:[1,2,4,4,4],m:896},
{e:[[0,1],[0,2]],p:[0,1,1,2,2],m:480},
{e:[[0,1],[0,3],[1,2],[2,4],[3,4]],p:[0,1,2,3,4],m:789},
{e:[[0,1],[0,4],[1,5],[2,4],[2,5],[3,5],[3,6],[4,6]],p:[0,1,2,3,6],m:470},
{e:[[0,1],[0,4],[1,2],[1,5],[2,6],[3,4],[4,5],[5,6]],p:[0,2,3,3,6],m:182},
{e:[[0,1],[0,4],[1,5],[2,3],[2,6],[3,4],[4,5],[5,6]],p:[0,1,2,3,6],m:937},
{e:[[0,3],[0,4],[0,6],[1,5],[2,3],[2,4],[2,6],[3,4]],p:[1,1,5,5,6],m:0}
];
const size=a=>1+Math.max(...a.p,...a.e.flat());
function authenticate(a){const n=size(a),d=Array(n).fill(0),s=new Set();for(const [u,v] of a.e){check(u!==v&&!s.has([Math.min(u,v),Math.max(u,v)].join(",")),"simple");s.add([Math.min(u,v),Math.max(u,v)].join(","));d[u]++;d[v]++}for(const v of a.p)d[v]++;check(d.every(x=>x===3)&&a.p.length===5,"cubic pole");}
function solve(E,n,fixed={}){let used=Array(n).fill(0),w=Array(E.length).fill(0);for(const [k,c] of Object.entries(fixed)){let [u,v]=E[k];if((used[u]|used[v])&c)return null;used[u]|=c;used[v]|=c;w[k]=c}
function dfs(){visits++;let k=-1,b=0,best=4;for(let i=0;i<E.length;i++)if(!w[i]){let [u,v]=E[i],a=7&~(used[u]|used[v]),t=count(a);if(!t)return false;if(t<best){best=t;k=i;b=a;if(t===1)break}}if(k<0)return true;let [u,v]=E[k];while(b){let c=b&-b;b-=c;used[u]|=c;used[v]|=c;w[k]=c;if(dfs())return true;used[u]^=c;used[v]^=c;w[k]=0}return false}return dfs()?w:null}
function poleEdges(a){const n=size(a);return [...a.e,...a.p.map((v,i)=>[v,n+i])]}
function poleMask(a){const E=poleEdges(a),n=size(a)+5;let m=0;for(const [i,[u,v]] of pairs.entries()){const f={};for(let j=0;j<5;j++)f[a.e.length+j]=j===u?1:j===v?2:4;if(solve(E,n,f))m|=1<<i}return m}
function type(a,w){let b=w.slice(a.e.length),c=b.find(x=>b.filter(y=>y===x).length===3);return bit(...b.map((x,i)=>x===c?-1:i).filter(i=>i>=0))}
function valid(E,w,n,ports=false){const d=Array(n).fill(0);for(let i=0;i<E.length;i++){const [u,v]=E[i],c=w[i];check([1,2,4].includes(c)&&!(d[u]&c)&&!(d[v]&c),"color");d[u]|=c;d[v]|=c}check(d.every(x=>x===7||(ports&&[1,2,4].includes(x))),"complete");}
function join(a,b){let n=size(a)+size(b),E=[...a.e,...b.e.map(([u,v])=>[u+size(a),v+size(a)])],seams=[];for(let i=0;i<5;i++){let u=a.p[i],v=b.p[i]+size(a);if(E.some(([x,y])=>x===u&&y===v)){let [x,y,z,t]=[n,n+1,n+2,n+3];n+=4;seams.push(E.length);E.push([u,x],[y,v],[x,z],[x,t],[y,z],[y,t],[z,t]);}else{seams.push(E.length);E.push([u,v])}}return {n,E,seams}}
function query(a,b){queries++;const J=join(a,b),w=solve(J.E,J.n);if(!w)return null;valid(J.E,w,J.n);const c=J.seams.map(i=>w[i]);const A=[...w.slice(0,a.e.length),...c],B=[...w.slice(a.e.length,a.e.length+b.e.length),...c];valid(poleEdges(a),A,size(a)+5,true);valid(poleEdges(b),B,size(b)+5,true);return [A,B]}
function relabel(m,p){let r=0;for(let i=0;i<10;i++)if(m>>i&1)r|=bit(pairs[i].map(j=>p.indexOf(j))[0],pairs[i].map(j=>p.indexOf(j))[1]);return r}
const lib=new Map(),cycap=new Map();for(const a of base){authenticate(a);check(poleMask(a)===a.m,"cap mask");for(const p of P){let m=relabel(a.m,p),b={e:a.e,p:p.map(i=>a.p[i]),m};lib.set(signature(m),b);if(cycles.includes(m))cycap.set(m,b)}}
const masks=[];for(let m=0;m<1024;m++){if([0,1,2,3,4].some(v=>pairs.filter((e,i)=>e.includes(v)&&(m>>i&1)).length===1))continue;masks.push(m);check(lib.has(signature(m)),"class missing")}
check(lib.size===64&&cycap.size===37&&masks.length===314,"class counts");
let cross=0;for(const a of masks)for(const b of masks){const x=lib.get(signature(a)).m;check(Boolean(a&b)===Boolean(x&b),"context");cross++}
function extend(a,W){const E=poleEdges(a),n=size(a);let m=0;for(const e of W.keys())m|=e;for(let v=0;v<5;v++){const inc=pairs.map((p,i)=>[p,1<<i]).filter(([p,b])=>p.includes(v)&&(m&b));if(inc.length!==1)continue;const [p,b]=inc[0],u=p.find(x=>x!==v),w=W.get(b),port=w.slice(a.e.length),c=port[u],d=port.find(x=>port.filter(y=>y===x).length===3),start=n+u,seen=new Set([start]),todo=[start],flip=[];while(todo.length){let x=todo.pop();for(let i=0;i<E.length;i++)if([c,d].includes(w[i])&&E[i].includes(x)&&!flip.includes(i)){flip.push(i);let y=E[i][0]===x?E[i][1]:E[i][0];if(!seen.has(y)){seen.add(y);todo.push(y)}}}const t=w.slice();for(const i of flip)t[i]=t[i]===c?d:c;valid(E,t,n+5,true);let e=type(a,t);check(!(m&e),"new edge");W.set(e,t);switches++;return true}return false}
function contract(a,b){let W=new Map(),miss=[];for(const c of cycles){const z=query(a,cycap.get(c));if(z)W.set(type(a,z[0]),z[0]);else miss.push(c)}const cap=lib.get(miss.join(","));check(!!cap,"actual class");if(!W.size)return false;const z=query(b,cap);if(!z)return false;const V=new Map([[type(b,z[0]),z[0]]]);while(extend(b,V)){}let t=[...V.keys()].find(e=>W.has(e));check(!!t,"witness intersection");if(t!==type(b,z[0]))lifts++;const wa=W.get(t),wb=V.get(t),pa=wa.slice(a.e.length),pb=wb.slice(b.e.length),map=new Map(pb.map((x,i)=>[x,pa[i]]));check(map.size===3,"color permutation");const J=join(a,b);let w=[...wa.slice(0,a.e.length),...wb.slice(0,b.e.length).map(x=>map.get(x))];for(let i=0;i<5;i++){const c=pa[i];w.push(c);if(J.seams[i]+1<(J.seams[i+1]??J.E.length)){const [d,e]=[1,2,4].filter(x=>x!==c);w.push(c,d,e,e,d,c)}}valid(J.E,w,J.n);return true}
let sat=0,unsat=0,tests=0;for(let i=0;i<base.length;i++)for(let j=0;j<base.length;j++)for(const p of P.filter((_,k)=>k%17===0)){const a=base[i],b={e:base[j].e,p:p.map(i=>base[j].p[i])};const truth=Boolean(poleMask(a)&poleMask(b));const direct=Boolean(query(a,b));const got=contract(a,b);check(truth===direct&&got===truth,"actual join");tests++;if(got)sat++;else unsat++}
return {checks,queries,visits,switches,lifts,classes:lib.size,cycles:cycles.length,abstractMasks:masks.length,abstractCompatibilityChecks:cross,tests,sat,unsat,base};
}
console.log(JSON.stringify(audit(),null,2));

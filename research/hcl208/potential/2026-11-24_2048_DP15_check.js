function main(){
const stats={oracle:0,closureScans:0,pins:0,projectionQueries:0,projectionRows:0,joinTests:0,maxPrefix:0,consumerReads:0,localLifts:0,assertions:0,cacheHits:0};const check=(x)=>{stats.assertions++;if(!x)throw Error("assertion")};
function oracle(r,p){stats.oracle++;let lo=0,free=[];const w={};for(let j=0;j<r.v.length;j++){const x=r.v[j],s=r.s?.[j]||0;if(x in p){w[x]=p[x];lo+=p[x]^s}else free.push([x,s])}let target=Math.max(lo,r.lo);if(target>Math.min(lo+free.length,r.hi))return null;for(const [x,s] of free){w[x]=s^(lo<target?1:0);if(lo<target)lo++}return w}
const proj=(w,v)=>v.map(x=>w[x]).join("");
function solve(n,R,E,C,cap){
const adj=R.map(()=>[]);for(const [i,j] of E){adj[i].push(j);adj[j].push(i)}const par=R.map(()=>-2),ord=[0];par[0]=-1;for(let h=0;h<ord.length;h++)for(const j of adj[ord[h]])if(par[j]===-2){par[j]=ord[h];ord.push(j)}check(ord.length===R.length&&E.length===R.length-1);
for(let x=0;x<n;x++){const ids=R.map((r,i)=>r.v.includes(x)?i:-1).filter(i=>i>=0);if(ids.length){const set=new Set(ids),seen=new Set([ids[0]]),q=[ids[0]];for(let h=0;h<q.length;h++)for(const j of adj[q[h]])if(set.has(j)&&!seen.has(j)){seen.add(j);q.push(j)}check(seen.size===ids.length)}}
const p={};let change=true;while(change){change=false;stats.closureScans++;outer:for(const r of R){if(!oracle(r,p))return {label:"UNSAT",peak:0};for(const x of r.v)if(!(x in p)){let a=oracle(r,{...p,[x]:0}),b=oracle(r,{...p,[x]:1});if(!a&&!b)return {label:"UNSAT",peak:0};if(!a||!b){p[x]=a?0:1;stats.pins++;change=true;break outer}}}}
const sep=(i,j)=>R[i].v.filter(x=>R[j].v.includes(x)).sort((a,b)=>a-b);
const S=R.map((r,i)=>[...new Set(adj[i].flatMap(j=>sep(i,j)))].sort((a,b)=>a-b));
const cache=new Map(),msg=R.map(()=>new Map());let peak=0;
function projection(i,v){const key=i+":"+v.join(",");if(cache.has(key)){stats.cacheHits++;return cache.get(key)}let rows=[];function dfs(k,w){stats.projectionQueries++;if(!oracle(R[i],{...p,...w}))return;if(k===v.length){rows.push(proj(w,v));stats.projectionRows++;if(rows.length>cap)throw "CAP";return}const x=v[k];for(let b=0;b<2;b++)if(!(x in p)||p[x]===b)dfs(k+1,{...w,[x]:b})}dfs(0,{});cache.set(key,rows);return rows}
try{for(const i of ord.slice().reverse()){
const v=S[i],covers=C[i].map(j=>{const u=v.filter(x=>R[j].v.includes(x));return {u,rows:projection(j,u)}});check(v.every(x=>covers.some(c=>c.u.includes(x))));
let prefixes=[""];for(let k=0;k<v.length;k++){let next=[];for(const pre of prefixes)for(const b of ["0","1"]){const t=pre+b;if(v[k] in p&&Number(b)!==p[v[k]])continue;stats.joinTests++;if(covers.every(c=>c.rows.some(row=>c.u.every((x,j)=>{const pos=v.indexOf(x);return pos>k||t[pos]===row[j]})))){next.push(t);if(next.length>cap)throw "CAP"}}prefixes=next;peak=Math.max(peak,prefixes.length);stats.maxPrefix=Math.max(stats.maxPrefix,prefixes.length)}
for(const t of prefixes){const guard={...p};v.forEach((x,j)=>guard[x]=Number(t[j]));const w=oracle(R[i],guard);if(!w)continue;let ok=true;const kids=[];for(const j of adj[i])if(par[j]===i){stats.consumerReads++;const key=proj(guard,sep(i,j));if(!msg[j].has(key)){ok=false;break}kids.push([j,key])}if(!ok)continue;const key=par[i]<0?"":proj(guard,sep(i,par[i]));if(!msg[i].has(key)){msg[i].set(key,{w,kids});stats.localLifts++}}
}if(!msg[0].has(""))return {label:"UNSAT",peak};let w={...p};function lift(i,key){const q=msg[i].get(key);for(const x in q.w){check(!(x in w)||w[x]===q.w[x]);w[x]=q.w[x]}for(const [j,k] of q.kids){stats.consumerReads++;lift(j,k)}}lift(0,"");for(const r of R){let c=r.v.reduce((s,x,j)=>s+(w[x]^(r.s?.[j]||0)),0);check(c>=r.lo&&c<=r.hi)}return {label:"SAT",peak,witness:w}
}catch(e){if(e==="CAP")return {label:"UNKNOWN",peak};throw e}}
const range=n=>Array.from({length:n},(_,i)=>i),make=(v,lo,hi,s)=>({v,lo,hi,s});
let controls=[];const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
function fano(flip,relax){let R=[make(range(7),0,7),...F.map((v,i)=>make(v,relax?.[0]===i&&relax[1]===0?0:1,relax?.[0]===i&&relax[1]===1?3:2,range(3).map(j=>+(flip?.[0]===i&&flip[1]===j))))];let E=F.map((_,i)=>[0,i+1]);let C=[F.map((_,i)=>i+1),...F.map((_,i)=>[i+1])];let count=0;for(let mask=0;mask<128;mask++)if(R.every(r=>{let s=r.v.reduce((s,x,j)=>s+(((mask>>x)&1)^(r.s?.[j]||0)),0);return s>=r.lo&&s<=r.hi}))count++;let z=solve(7,R,E,C,512);check(z.label===(count?"SAT":"UNSAT"));controls.push({family:"Fano",flip,relax,count,label:z.label,peak:z.peak})}
fano(null,null);for(let i=0;i<7;i++){for(let j=0;j<3;j++)fano([i,j],null);for(let j=0;j<2;j++)fano(null,[i,j])}
for(const n of [8,32,128])for(const lo of [1,2]){let v=range(n);let z=solve(n,[make(v,0,1),make(v,lo,n)],[[0,1]],[[0],[0]],n+1);check(z.label===(lo===1?"SAT":"UNSAT"));check(z.peak===n+1);controls.push({family:"wideSparse",n,lo,label:z.label,peak:z.peak})}
for(const k of [4,16])for(const bad of [false,true]){let n=k*8,R=[make([],0,0)],E=[],C=[[]];for(let i=0;i<k;i++){let v=range(8).map(x=>i*8+x),j=R.length;R.push(make(v,0,1),make(v,bad&&i===k-1?2:1,8));E.push([0,j],[j,j+1]);C.push([j],[j])}const z=solve(n,R,E,C,9);check(z.label===(bad?"UNSAT":"SAT"));controls.push({family:"product",k,bad,label:z.label,peak:z.peak})}
let v=range(16);let z=solve(16,[make(v,1,15),make(v,1,15)],[[0,1]],[[0],[0]],32);check(z.label==="UNKNOWN");controls.push({family:"cap",label:z.label,peak:z.peak});
let forced=solve(3,[make([0,1],2,2),make([1,2],0,1)],[[0,1]],[[0],[0]],8);check(forced.label==="SAT"&&forced.witness[2]===0);let contra=solve(2,[make([0,1],2,2),make([0,1],0,1)],[[0,1]],[[0],[0]],8);check(contra.label==="UNSAT");controls.push({family:"closure",label:forced.label},{family:"closure",label:contra.label});
return {stats,controls,totals:controls.reduce((o,r)=>(o[r.label]=(o[r.label]||0)+1,o),{})}
}
console.log(JSON.stringify(main(),null,2));

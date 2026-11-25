
// M28: signed edge-coset, exact local closure, F7 minor and one-exception min-cut adapter.
// node checker.js RT26_results.json S27_results.json DA22_results.json
function run(jobs){
let count={closure:0,checks:0,reference:0,k4:0,flowBFS:0,cutTests:0};
function check(b){count.checks++;if(!b)throw Error("assertion")}
function state(n,reg,rows){
 let p=Array.from({length:n},(_,i)=>i),q=Array(n).fill(0);
 function find(a){if(p[a]===a)return [a,0];let [b,s]=find(p[a]);return [b,s^q[a]]}
 function join(a,b,v){let [i,s]=find(a),[j,t]=find(b);if(i===j)return (s^t)===v?0:-1;p[i]=j;q[i]=s^t^v;return 1}
 for(const [a,b,v] of rows)if(join(a,b,v)<0)return null;
 for(;;){let changed=false;for(const o of reg){count.closure++;let vs=[];for(let w=0;w<8;w++){if(o.bad.includes(w))continue;let ok=true;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let [a,s]=find(o.t[i]),[b,t]=find(o.t[j]);if(a===b&&((w>>i^w>>j)&1)!==(s^t))ok=false}if(ok)vs.push(w)}if(!vs.length)return null;for(let i=0;i<3&&!changed;i++)for(let j=i+1;j<3&&!changed;j++){let v=(vs[0]>>i^vs[0]>>j)&1;if(vs.every(w=>((w>>i^w>>j)&1)===v)){let k=join(o.t[i],o.t[j],v);if(k<0)return null;if(k>0)changed=true}}if(changed)break}if(!changed)break}
 const roots=[...new Set(p.map((_,i)=>find(i)[0]))].sort((a,b)=>a-b),map=p.map((_,i)=>{let [a,b]=find(i);return [roots.indexOf(a),b]});
 let d=roots.length,base=0,E=new Map();
 for(const o of reg)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let [a,s]=map[o.t[i]],[b,t]=map[o.t[j]],v=1^((o.bad[0]>>i^o.bad[0]>>j^s^t)&1);if(a===b)base+=v;else{let u=Math.min(a,b),z=Math.max(a,b),k=u*d+z;if(!E.has(k))E.set(k,[0,0]);E.get(k)[v]++}}
 let edges=[];for(const [k,[a,b]] of E){base+=Math.min(a,b);if(a!==b)edges.push([Math.floor(k/d),k%d,b>a?1:0,Math.abs(a-b)])}return {d,map,base,edges}
}
function evalW(reg,x){let e=0;for(const o of reg){let w=o.t.reduce((s,t,i)=>s|(((x>>t)&1)<<i),0);if(o.bad.includes(w))e++}return e}
function cost(st,x){return st.base+st.edges.reduce((s,[a,b,v,w])=>s+((((x>>a^x>>b)&1)^v)?w:0),0)}
function lift(st,x){return st.map.reduce((s,[a,v],i)=>s|((((x>>a)&1)^v)<<i),0)}
function k4(st){let d=st.d,P=Array.from({length:d},()=>Array(d).fill(-1));for(const [a,b,v] of st.edges)P[a][b]=P[b][a]=v;let hits=0,first=null;for(let a=0;a<d;a++)for(let b=a+1;b<d;b++)for(let c=b+1;c<d;c++)for(let e=c+1;e<d;e++){count.k4++;let t=[a,b,c,e],l=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)l.push(P[t[i]][t[j]]);if(l.includes(-1))continue;let [ab,ac,ae,bc,be,ce]=l;if((ab^ac^bc)&&(ab^ae^be)&&(ac^ae^ce)){hits++;if(!first)first={vertices:t,signs:l,minorColumns:[1,2,4,3,5,6,7]}}}return {hits,first}}
function treeGauge(st){let d=st.d,adj=Array.from({length:d},()=>[]);for(const [a,b,v] of st.edges){adj[a].push([b,v]);adj[b].push([a,v])}let g=Array(d).fill(-1);for(let a=0;a<d;a++)if(g[a]<0){g[a]=0;let q=[a];for(let h=0;h<q.length;h++)for(const [b,v] of adj[q[h]])if(g[b]<0){g[b]=g[q[h]]^v;q.push(b)}}return g}
function mincut(d,edges,s,t){let A=Array.from({length:d},()=>Array(d).fill(0));for(const [a,b,v,w] of edges){A[a][b]+=w;A[b][a]+=w}let value=0;for(;;){count.flowBFS++;let p=Array(d).fill(-1),q=[s];p[s]=s;for(let h=0;h<q.length&&p[t]<0;h++)for(let j=0;j<d;j++)if(p[j]<0&&A[q[h]][j]>0){p[j]=q[h];q.push(j)}if(p[t]<0){let x=p.reduce((w,a,i)=>w|(a>=0?1<<i:0),0);return {value,x}}let w=Infinity;for(let j=t;j!==s;j=p[j])w=Math.min(w,A[p[j]][j]);for(let j=t;j!==s;j=p[j]){A[p[j]][j]-=w;A[j][p[j]]+=w}value+=w}}
function adapter(st){let g=treeGauge(st),gw=g.reduce((s,b,i)=>s|(b<<i),0),bad=st.edges.filter(([a,b,v])=>g[a]^g[b]^v);if(!bad.length)return {min:st.base,witness:gw,kind:"balanced"}; // H target equals a single column iff toggling that edge makes preferences consistent.
 for(let k=0;k<st.edges.length;k++){count.cutTests++;let E=st.edges.map((e,i)=>[e[0],e[1],e[2]^(i===k?1:0),e[3]]),h=treeGauge({...st,edges:E});if(E.some(([a,b,v])=>h[a]^h[b]^v))continue;let [a,b,v,w]=st.edges[k],q=mincut(st.d,st.edges.filter((_,i)=>i!==k),a,b),hw=h.reduce((s,b,i)=>s|(b<<i),0);let min=st.base+Math.min(w,q.value),witness=w<=q.value?hw:hw^q.x;check(cost(st,witness)===min);return {min,witness,kind:"one-column",edge:k}}
 return {kind:"OPEN",treeExceptions:bad.length}
}
let out=[];for(const j of jobs){let models=[],min=Infinity;for(let x=0;x<2**j.n;x++){count.reference++;let e=evalW(j.reg,x);min=Math.min(min,e);if(!e)models.push(x)}
 let runs=[];for(const [mode,rows] of [["raw",[]],["DA21",j.imported],["DA22",j.cuts]]){if(mode!=="raw"&&!rows.length)continue;for(const [a,b,v] of rows)check(models.every(x=>((x>>a^x>>b)&1)===v));let st=state(j.n,j.reg,rows);if(!st){check(!models.length);runs.push({mode,kind:"closure"});continue}let ref=Infinity;for(let x=0;x<2**st.d;x++){count.reference++;let e=evalW(j.reg,lift(st,x));check(cost(st,x)===j.reg.length+2*e);ref=Math.min(ref,cost(st,x))}let cert=adapter(st),minor=k4(st);if(cert.min!==undefined){check(cert.min===ref);check(cost(st,cert.witness)===ref);check(evalW(j.reg,lift(st,cert.witness))===(ref-j.reg.length)/2)}if(minor.hits)check(cert.kind==="OPEN");runs.push({mode,d:st.d,edges:st.edges.length,base:st.base,minimum:ref,minor,cert})}out.push({id:j.id,n:j.n,m:j.reg.length,models:models.length,min,runs})}
 // General signed-graph controls: balanced, one-exception, and odd K4.
 let controls=[];for(let mask=0;mask<64;mask++){let E=[],k=0;for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)E.push([i,j,(mask>>k++)&1,1+(k%3)]);let st={d:4,base:0,edges:E},a=adapter(st),b=k4(st),ref=Math.min(...Array.from({length:16},(_,x)=>cost(st,x)));if(a.min!==undefined)check(a.min===ref);if(b.hits)check(a.kind==="OPEN");controls.push({mask,ref,kind:a.kind,F7:!!b.hits})}
 return {count,out,controls};
}
function assemble(rt,sy,da){let jobs=[];for(let c of rt.controls)for(let neighbor of [false,true]){let reg=JSON.parse(JSON.stringify(c.registry));if(neighbor)reg[0].bad=reg[0].bad.map(x=>x^1);jobs.push({id:"RT26-"+c.n+"-"+(neighbor?"SAT":"UNSAT"),n:c.n,reg})}for(let c of sy.controls.filter(c=>c.neighbor))jobs.push({id:"S27-"+c.n+"-UNSAT",n:c.n,reg:c.neighbor.root},{id:"S27-"+c.n+"-SAT",n:c.n,reg:c.neighbor.satRegistry});for(let j of jobs){let a=da.results.find(x=>x.id===j.id);j.imported=a.imported;j.cuts=a.runs.find(x=>x.mode===2&&!x.use).cuts.map(x=>x.cut)}return jobs}
if(typeof require!=="undefined"&&typeof process!=="undefined"){let fs=require("fs");console.log(JSON.stringify(run(assemble(...process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,"utf8"))))),null,2))}

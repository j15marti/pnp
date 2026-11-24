/* Reproduce: node 2026-11-24_1340_BH07_check.js */
function run(){
 const stats={scans:0,unitPins:0,tautologies:0,leafDeletes:0,graphBuilds:0,incidences:0,treeProjects:0,cycleProjects:0,liftTrials:0,liftRows:0,branches:0,nodes:0,checks:0,referenceWords:0};
 const assert=(v,m)=>{stats.checks++;if(!v)throw Error(m)};
 const id=Math.abs, sg=l=>+(l<0), val=(l,a)=>a[id(l)]^sg(l);
 function ok(f,a){if(!f.b)return true;if(!f.a.length)return false;let b=val(f.a[0],a);return !(f.b>>b&1)||f.a.some(l=>val(l,a)!==b)}
 function normal(f,a){let b=f.b, s=new Set;for(let l of f.a){if(a[id(l)]!==undefined)b&=1<<val(l,a);else{if(s.has(-l))return {a:[],b:0};s.add(l)}}return {a:[...s],b}}
 function graph(F){stats.graphBuilds++;let occ=new Map;F.forEach((f,i)=>f.a.forEach(l=>{stats.incidences++;let v=id(l);if(!occ.has(v))occ.set(v,[]);occ.get(v).push([i,l])}));let adj=F.map(()=>[]),edges=[];for(let [v,o] of occ)if(o.length===2&&o[0][0]!==o[1][0]){let [i,l]=o[0],[j,k]=o[1],e={v,i,j,l,k};edges.push(e);adj[i].push(e);adj[j].push(e)}return {occ,adj,edges}}
 const other=(e,i)=>e.i===i?e.j:e.i;
 const lit=(e,i)=>e.i===i?e.l:e.k;
 function component(F,g,start){let vs=[start],seen=new Set(vs),es=new Set,par=new Map,order=[];for(let i of vs){order.push(i);for(let e of g.adj[i]){es.add(e);let j=other(e,i);if(!seen.has(j)){seen.add(j);vs.push(j);par.set(j,e)}}}return {F,vs,seen,es:[...es],par,order,root:start}}
 function project(C){let {F,vs,es,par,root,order}=C;
  if(es.length>=vs.length){stats.cycleProjects++;let pure=es.length===vs.length&&vs.every(i=>F[i].a.length===2&&F[i].b===3);if(pure){let r=0;for(let e of es)r^=1^sg(e.l)^sg(e.k);return {a:[],b:r?3:0}}return {a:[],b:0}}
  stats.treeProjects++;let p=new Map([[root,0]]), priv=new Set(es.map(e=>e.v)),a=[],b=3;
  for(let i of order){if(i!==root){let e=par.get(i),j=other(e,i);p.set(i,p.get(j)^1^sg(e.l)^sg(e.k))}let t=p.get(i),mask=F[i].b;if(t)mask=((mask&1)<<1)|((mask&2)>>1);b&=mask;for(let l of F[i].a)if(!priv.has(id(l)))a.push(t?-l:l)}
  return normal({a,b},{})
 }
 // Local exact tree DP. If cyclic, fix all chords except one to zero and try that chord both ways.
 function lift(C,external){let {F,es,par,order,root}=C,tree=new Set(par.values()),chords=es.filter(e=>!tree.has(e)),kids=new Map(order.map(i=>[i,[]]));for(let [i,e] of par)kids.get(other(e,i)).push([i,e]);let priv=new Set(es.map(e=>e.v));
  for(let bit=0;bit<(chords.length?2:1);bit++){stats.liftTrials++;let a={...external};chords.forEach((e,j)=>a[e.v]=j===0?bit:0);let tab=new Map;
   for(let i of [...order].reverse()){let pe=par.get(i),rows=[];for(let p=0;p<(pe?2:1);p++){stats.liftRows++;let z={...a},choices=[];if(pe)z[pe.v]=p;let fail=false;for(let [j,e] of kids.get(i)){let r=tab.get(j),opts=[0,1].filter(b=>r[b]!==null);if(!opts.length){fail=true;break}z[e.v]=opts[0];if(opts.length===2)choices.push(e)}if(fail){rows.push(null);continue}if(!ok(F[i],z)&&choices.length)z[choices[0].v]^=1;rows.push(ok(F[i],z)?kids.get(i).map(([j,e])=>[j,e,z[e.v]]):null)}tab.set(i,rows)}
   if(tab.get(root)[0]===null)continue;let todo=[[root,0]];for(let [i,p] of todo){for(let [j,e,b] of tab.get(i)[p]){a[e.v]=b;todo.push([j,b])}}assert(order.every(i=>ok(F[i],a)),"lift source");return a
  }return null
 }
 function solve(F,n,initial={}){function rec(F,a){stats.nodes++;a={...a};F=F.map(f=>({a:[...f.a],b:f.b}));let archive=[];
   function finish(w){if(!w)return null;for(let i=archive.length-1;i>=0;i--){let r=archive[i];if(r.one){let {v,f}=r.one;w[v]=0;if(!ok(f,w))w[v]=1;assert(ok(f,w),"leaf lift")}else{let w2=lift(r.C,w);assert(w2!==null,"region lift");w=w2}}return w}
   while(true){stats.scans++;let changed=false;
    for(let i=0;i<F.length;i++){let f=normal(F[i],a);if(!f.b){F.splice(i,1);stats.tautologies++;changed=true;break}if(!f.a.length)return null;if(f.a.length===1){if(f.b===3)return null;let l=f.a[0];a[id(l)]=(f.b===1?1:0)^sg(l);F.splice(i,1);stats.unitPins++;changed=true;break}F[i]=f}
    if(changed)continue;
    if(!F.length){let w={};for(let v=1;v<=n;v++)w[v]=a[v]??0;return finish(w)}
    let g=graph(F),leaf=[...g.occ].find(([v,o])=>o.length===1);
    if(leaf){let [v,o]=leaf,i=o[0][0];archive.push({one:{v,f:F[i]}});F.splice(i,1);stats.leafDeletes++;continue}
    let start=g.adj.findIndex(q=>q.length);
    if(start>=0){let C=component(F,g,start),f=project(C);if(!f.a.length&&f.b)return null;archive.push({C});F=F.filter((_,i)=>!C.seen.has(i));if(f.b)F.push(f);continue}
    // Closure has stagnated: guarded exact fallback, no polynomial claim.
    let v=[...g.occ].sort((a,b)=>b[1].length-a[1].length||a[0]-b[0])[0][0];stats.branches++;let w=rec(F,{...a,[v]:0});if(!w)w=rec(F,{...a,[v]:1});return finish(w)
   }
  }let w=rec(F,initial);if(w)assert(F.every(f=>ok(f,w))&&Object.entries(initial).every(([v,b])=>w[v]===b),"original source");return w}
 function reference(F,n,pins={}){let count=0;for(let k=0;k<2**n;k++){stats.referenceWords++;let a={};for(let v=1;v<=n;v++)a[v]=k>>(v-1)&1;if(Object.entries(pins).every(([v,b])=>a[v]===b)&&F.every(f=>ok(f,a)))count++}return count}
 let seed=20261124;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 const result={seed:20261124,fano:[],cube:{SAT:0,UNSAT:0},random:{SAT:0,UNSAT:0},regional:{SAT:0,UNSAT:0},scaling:[],binary:[]};
 // Regional chain/cycle, private edges numbered first; distinct external ports.
 function region(L,cyclic,random=false,binary=false){let F=Array.from({length:L},()=>({a:[],b:3})),e=0;for(let i=0;i<L-(cyclic?0:1);i++){let j=(i+1)%L,v=++e;F[i].a.push(random&&rnd(2)?-v:v);F[j].a.push(random&&rnd(2)?-v:v)}
  let k=e;for(let f of F){while(f.a.length<(binary?2:3)){let v=++k;f.a.push(random&&rnd(2)?-v:v)}if(random)f.b=1+rnd(3)}return {F,e,k,C:component(F,graph(F),0)}}
 function regionalTest(R,a,brute){let f=project(R.C),pred=ok(f,a),w=lift(R.C,a);assert(pred===!!w,"projection/lift");if(brute){let exists=false;for(let k=0;k<2**R.e;k++){stats.referenceWords++;let q={...a};for(let j=1;j<=R.e;j++)q[j]=k>>(j-1)&1;if(R.F.every(f=>ok(f,q)))exists=true}assert(pred===exists,"region brute")}result.regional[pred?"SAT":"UNSAT"]++;return pred}
 for(let j=0;j<200;j++){let R=region(2+rnd(5),false,true);let a={};for(let k=R.e+1;k<=R.k;k++)a[k]=rnd(2);regionalTest(R,a,true)}
 for(let j=0;j<200;j++){let R=region(3+rnd(5),true,true);let a={};for(let k=R.e+1;k<=R.k;k++)a[k]=rnd(2);regionalTest(R,a,true)}
 for(let L of [3,4,5,6]){let R=region(L,true,false,true);let v=regionalTest(R,{},true);assert(v===(L%2===0),"binary parity");result.binary.push({L,SAT:v})}
 for(let L of [5,9,33,129,513]){let R=region(L,false),f=project(R.C),a={};for(let l of f.a)a[id(l)]=sg(l);let u=regionalTest(R,a,false);assert(!u,"chain hostile");a[id(f.a[0])]^=1;let s=regionalTest(R,a,false);assert(s,"chain neighbor");let C=region(L,true),b={};for(let i=C.e+1;i<=C.k;i++)b[i]=0;assert(regionalTest(C,b,false),"loose cycle");result.scaling.push({L,ports:f.a.length,treeUNSAT:!u,treeNeighborSAT:s,looseCycleSAT:true})}
 const lines=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
 for(let i=-1;i<7;i++)for(let b of (i<0?[3]:[1,2])){let F=lines.map((a,j)=>({a,b:j===i?b:3})),before={...stats};let w=solve(F,7),count=reference(F,7);assert(!!w===!!count,"Fano");result.fano.push({i,b,count,SAT:!!w,nodes:stats.nodes-before.nodes,branches:stats.branches-before.branches,treeProjects:stats.treeProjects-before.treeProjects,cycleProjects:stats.cycleProjects-before.cycleProjects})}
 for(let k=0;k<256;k++){let F=[];for(let j=0;j<8;j++)if(k>>j&1)F.push({a:[1,2,3].map((v,i)=>j>>i&1?-v:v),b:1});let w=solve(F,3),count=reference(F,3);assert(!!w===!!count,"cube");result.cube[w?"SAT":"UNSAT"]++}
 for(let j=0;j<150;j++){let F=[],n=6;for(let i=0;i<2+rnd(13);i++){let v=[];while(v.length<2+(i%2)){let k=1+rnd(n);if(!v.some(l=>id(l)===k))v.push(rnd(3)===0?-k:k)}F.push({a:v,b:1+rnd(3)})}let pins=j%3===0?{1:j%2}:{};let w=solve(F,n,pins),count=reference(F,n,pins);assert(!!w===!!count,"random");result.random[w?"SAT":"UNSAT"]++}
 return {...result,stats}
}
console.log(JSON.stringify(run(),null,2));

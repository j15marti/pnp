// BW02: deterministic bounded-region projection and exact guard closure.
// Node.js, no dependencies. Run: node 2026-11-24_0810_BW02_check.js
function main(){
 const assert=(p,s)=>{if(!p)throw Error(s)};
 const uniq=a=>[...new Set(a)].sort((a,b)=>a-b);
 const bit=(a,i)=>(a>>i)&1;
 const val=(v,a,x)=>bit(a,v.indexOf(x));
 function factor(v,p){v=uniq(v);let rows=[];for(let a=0;a<2**v.length;a++)if(p(x=>val(v,a,x)))rows.push(a);return {v,rows}}
 function evalF(f,x){let a=0;for(let i=0;i<f.v.length;i++)a|=x[f.v[i]]<<i;return f.rows.includes(a)}
 function nae(e,rel=-1){return factor(e,x=>{let s=e.reduce((a,v)=>a+x(v),0);return (s>0||rel===0)&&(s<3||rel===1)})}
 function pin(v,b){return factor([v],x=>x(v)===b)}
 function brute(n,fs){let count=0;for(let a=0;a<2**n;a++){let x=Array.from({length:n},(_,i)=>bit(a,i));if(fs.every(f=>evalF(f,x)))count++}return count}
 function solve(n,original,cap=5,endCap=10){
  let fs=original.slice(),live=new Set(Array.from({length:n},(_,i)=>i)),stack=[];
  let stats={closureRounds:0,closureRowChecks:0,scopeMerges:0,forced:0,componentTrials:0,adjacencyVisits:0,factorScans:0,regionAssignments:0,regions:0,eqRegions:0,peakLive:n,peakFactors:fs.length,storedRows:0,finalAssignments:0,verifiedFactors:0};
  function substitute(v,u,b){
   assert(live.has(v)&&(u===-1||live.has(u)&&u!==v),"substitute live");
   stack.push({v,u,b});live.delete(v);stats.forced++;
   fs=fs.map(f=>{stats.factorScans++;if(!f.v.includes(v))return f;
    let nv=f.v.filter(x=>x!==v);if(u!==-1)nv.push(u);
    return factor(nv,x=>{let a=0;for(let i=0;i<f.v.length;i++){let w=f.v[i];a|=(w===v?(u===-1?b:x(u)^b):x(w))<<i}stats.closureRowChecks++;return f.rows.includes(a)})
   })
  }
  function closure(){
   while(true){stats.closureRounds++;let m=new Map();
    for(let f of fs){stats.factorScans++;if(!f.rows.length)return false;if(f.rows.length===2**f.v.length)continue;
     let k=f.v.join(","),old=m.get(k);if(old){stats.scopeMerges++;let rows=old.rows.filter(a=>{stats.closureRowChecks++;return f.rows.includes(a)});m.set(k,{v:f.v,rows})}else m.set(k,f)
    }
    fs=[...m.values()];let move=null;
    for(let f of fs){stats.factorScans++;if(!f.rows.length)return false;
     for(let i=0;i<f.v.length&&!move;i++){let b=bit(f.rows[0],i);if(f.rows.every(a=>{stats.closureRowChecks++;return bit(a,i)===b}))move=[f.v[i],-1,b]}
     for(let i=0;i<f.v.length&&!move;i++)for(let j=i+1;j<f.v.length&&!move;j++){let b=bit(f.rows[0],i)^bit(f.rows[0],j);if(f.rows.every(a=>{stats.closureRowChecks++;return (bit(a,i)^bit(a,j))===b}))move=[f.v[j],f.v[i],b]}
     if(move)break
    }
    if(!move)return true;substitute(...move)
   }
  }
  function find(){
   let adj=Array.from({length:n},()=>new Set());
   for(let f of fs){stats.factorScans++;for(let a of f.v)for(let b of f.v)if(a!==b)adj[a].add(b)}
   function trial(s,B,seen=null){
    stats.componentTrials++;let cut=new Set(B),C=[s],have=new Set(C);
    for(let i=0;i<C.length;i++)for(let v of adj[C[i]]){stats.adjacencyVisits++;if(!cut.has(v)&&!have.has(v)){have.add(v);C.push(v);if(C.length>cap)return null}}
    if(seen)for(let v of C)seen.add(v);
    let actual=uniq(C.flatMap(v=>[...adj[v]].filter(w=>!have.has(w))));
    assert(actual.every(v=>cut.has(v)),"not closed");return {C:uniq(C),B:actual}
   }
   let vs=[...live].sort((a,b)=>adj[a].size-adj[b].size||a-b);
   // Local fast path; no source gadget labels.
   for(let s of vs){let q=[...adj[s]].sort((a,b)=>a-b),hit=trial(s,[]);if(hit)return hit;
    for(let i=0;i<q.length;i++){hit=trial(s,[q[i]]);if(hit)return hit;for(let j=i+1;j<q.length;j++){hit=trial(s,[q[i],q[j]]);if(hit)return hit}}
   }
   // Complete enumeration for boundary <=2. Failed trials charged.
   for(let i=0;i<vs.length;i++)for(let j=i;j<vs.length;j++){let B=i===j?[vs[i]]:[vs[i],vs[j]],seen=new Set(B);for(let s of vs)if(!seen.has(s)){let hit=trial(s,B,seen);if(hit)return hit;seen.add(s)}}
   return null
  }
  function peel({C,B}){
   let set=new Set(C),inF=[],out=[];
   for(let f of fs){stats.factorScans++;(f.v.some(v=>set.has(v))?inF:out).push(f)}
   assert(inF.every(f=>f.v.every(v=>set.has(v)||B.includes(v))),"hidden port");
   let rows=[],witness={};
   for(let a=0;a<2**B.length;a++)for(let z=0;z<2**C.length;z++){
    stats.regionAssignments++;let x={};B.forEach((v,i)=>x[v]=bit(a,i));C.forEach((v,i)=>x[v]=bit(z,i));
    let ok=inF.every(f=>{stats.factorScans++;return evalF(f,x)});
    if(ok){rows.push(a);witness[a]=z;break}
   }
   stats.regions++;if(B.length===2&&rows.length===2&&(rows.join(",")==="0,3"||rows.join(",")==="1,2"))stats.eqRegions++;
   stats.storedRows+=rows.length;stack.push({C,B,witness});C.forEach(v=>live.delete(v));
   if(rows.length!==2**B.length)out.push({v:B,rows});fs=out;
  }
  function finish(label,x=null){
   if(label==="SAT"){
    for(let j=stack.length-1;j>=0;j--){let s=stack[j];if(s.C){let a=0;s.B.forEach((v,i)=>a|=x[v]<<i);assert(Object.hasOwn(s.witness,a),"bad lift guard");s.C.forEach((v,i)=>x[v]=bit(s.witness[a],i))}
     else x[s.v]=s.u===-1?s.b:x[s.u]^s.b}
    for(let f of original){stats.verifiedFactors++;assert(evalF(f,x),"bad source lift")}
   }
   return {label,residual:live.size,stats}
  }
  while(true){
   if(!closure())return finish("UNSAT");
   if(!fs.length){let x=Array(n).fill(0);return finish("SAT",x)}
   let hit=find();if(hit){peel(hit);continue}
   // Stagnation closure before bounded terminal; no unrestricted branch.
   if(!closure())return finish("UNSAT");
   if(live.size>endCap)return finish("UNKNOWN");
   let vs=[...live];for(let a=0;a<2**vs.length;a++){stats.finalAssignments++;let x=Array(n).fill(0);vs.forEach((v,i)=>x[v]=bit(a,i));if(fs.every(f=>{stats.factorScans++;return evalF(f,x)}))return finish("SAT",x)}
   return finish("UNSAT")
  }
 }
 const F=[[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]], full=F.concat([[0,1,2]]);
 function gadget(G,a,b){let ids=[a,b];for(let i=0;i<5;i++)ids.push(G.n++);for(let e of F)G.e.push(e.map(i=>ids[i]))}
 function path(G,a,k){for(let i=0;i<k;i++){let b=G.n++;gadget(G,a,b);a=b}return a}
 function base(){let G={n:1,e:[]},b=path(G,0,4),c=path(G,0,4);G.e.push([0,b,c]);return G}
 function stretch(G){let H={n:G.n,e:[]};for(let e of G.e){let q=[];for(let a of e){let b=H.n++;gadget(H,a,b);q.push(b)}H.e.push(q)}return H}
 function instance(G,owner=-1){return G.e.map((e,i)=>nae(e,Math.floor(owner/2)===i?owner%2:-1))}
 // Permute source IDs deterministically, discard all generator manifests.
 let seed=20261124;function rnd(k){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%k}
 function shuffled(G){let p=Array.from({length:G.n},(_,i)=>i);for(let i=p.length-1;i>0;i--){let j=rnd(i+1);[p[i],p[j]]=[p[j],p[i]]}return {n:G.n,e:G.e.map(e=>e.map(v=>p[v]))}}
 let G=shuffled(base()),H=shuffled(stretch(base())),B={n:7,e:full},out={seed:20261124,cap:5,endCap:10};
 function check(G,owner,expected){let r=solve(G.n,instance(G,owner));assert(r.label===expected,"control "+G.n+"/"+owner+" "+r.label);return {owner,...r}}
 out.fano=[check(B,-1,"UNSAT")];for(let i=0;i<14;i++){assert(brute(7,instance(B,i))===5,"neighbor count");out.fano.push(check(B,i,"SAT"))}
 out.base=[check(G,-1,"UNSAT")];for(let i=0;i<2*G.e.length;i++)out.base.push(check(G,i,"SAT"));
 out.stretch=[check(H,-1,"UNSAT")];for(let i of [0,1,12,13,2*H.e.length-2,2*H.e.length-1])out.stretch.push(check(H,i,"SAT"));
 let random={cases:0,sat:0,unsat:0,referenceAssignments:0,regions:0,forced:0};
 for(let t=0;t<160;t++){let n=5+rnd(4),fs=[];for(let j=0;j<3+rnd(10);j++){
  let v=[];let k=2+rnd(3);while(v.length<k){let a=rnd(n);if(!v.includes(a))v.push(a)}
  let signs=v.map(()=>rnd(2)),type=rnd(4);
  fs.push(factor(v,x=>{let a=v.map((w,i)=>x(w)^signs[i]),s=a.reduce((a,b)=>a+b,0);return type===0?s===0||s===k:type===1?s===Math.floor(k/2):type===2?s>0:s%2===0}))
 }if(t%2===0)fs.push(pin(rnd(n),rnd(2)));
 let count=brute(n,fs),r=solve(n,fs);assert(r.label===(count?"SAT":"UNSAT"),"random");random.cases++;random[count?"sat":"unsat"]++;random.referenceAssignments+=2**n;random.regions+=r.stats.regions;random.forced+=r.stats.forced}
 out.random=random;
 // Four-color palette lists: every two-bit support, and every relative ternary support.
 let maskChecks=0,relChecks=0;
 for(let m=0;m<16;m++)for(let a=0;a<4;a++){let forbidden=[0,1,2,3].filter(c=>!(m>>c&1));assert(!forbidden.includes(a)===Boolean(m>>a&1),"hub list");maskChecks++}
 for(let m=0;m<16;m++)for(let a=0;a<8;a++){let h=2*(bit(a,0)^bit(a,1))+(bit(a,0)^bit(a,2)),f=7^a;let h2=2*(bit(f,0)^bit(f,1))+(bit(f,0)^bit(f,2));assert(h===h2&&Boolean(m>>h&1)===Boolean(m>>h2&1),"relative");relChecks++}
 out.hub={maskChecks,relChecks};
 let dense={n:12,e:[]};for(let i=0;i<12;i++)for(let j=i+1;j<12;j++)for(let k=j+1;k<12;k++)dense.e.push([i,j,k]);
 let d=solve(12,instance(dense));assert(d.label==="UNKNOWN","hostile decline");let planted=dense.e.filter(e=>e.some(v=>v<6)&&e.some(v=>v>=6)),p=solve(12,planted.map(e=>nae(e)));assert(p.label==="UNKNOWN","hostile sat decline");out.hostile={unsat:d,sat:p};
 out.discrepancies=0;return out
}
console.log(JSON.stringify(main(),null,2));

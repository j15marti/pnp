"use strict";
function audit(){
 let checks=0;const ck=(v,msg="")=>{checks++;if(!v)throw Error("assertion "+checks+" "+msg)};
 const nae=(t,w)=>w[t[0]]!==w[t[1]]||w[t[1]]!==w[t[2]], good=(O,w)=>O.every(t=>nae(t,w));
 const bits=(n,v)=>Array.from({length:n},(_,i)=>(v>>i)&1);
 function sourceModels(n,O){return Array.from({length:2**n},(_,i)=>bits(n,i)).filter(w=>good(O,w))}
 const S=Array.from({length:6},(_,i)=>bits(3,i+1));
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const plane=[];for(let p=0;p<3;p++)for(let b=0;b<3;b++)plane.push([0,1,2].map(i=>3*i+(p*i+b)%3));for(let i=0;i<3;i++)plane.push([3*i,3*i+1,3*i+2]);
 const G=plane.map((t,i)=>({p:Math.floor(i/3),t})).filter((o,i)=>i!==0&&i!==1);
 const gw=[0,1,0,0,1,0,0,1,1];
 const modelsG=sourceModels(9,G.map(o=>o.t));for(let w of modelsG){ck(w[0]===w[3]&&w[3]===w[6]);ck(w[1]===w[4]&&w[4]===w[7]);ck(w[0]!==w[1])}ck(good(G.map(o=>o.t),gw));
 function compile(n,O){
  let R=[[[2*n,0],[2*n+1,0],[2*n+2,0]]];for(let i=0;i<n;i++)for(let j=0;j<3;j++)R.push([[2*n+j,1],[2*i,0],[2*i+1,0]]);
  for(let [a,b,c] of O)R.push([[2*a+1,1],[2*b,0],[2*c,0]]);
  let C=[],D=[],occ=Array.from({length:2*n+3},()=>[]);
  const vertex=(v,s)=>{D.push([v,s]);return D.length-1},owner=(p,t)=>C.push({p,t});
  for(let t of R){let ids=t.map(([v,s])=>{let i=vertex(v,s);occ[v].push({i,s});return i});owner(0,ids)}
  function opposite(a){let [v,s]=D[a];return vertex(v,s^1)}
  function wire(a,b,p){ck(D[a][0]===D[b][0]&&D[a][1]!==D[b][1]);let ids=gw.map(g=>vertex(D[a][0],g^D[a][1]^1));for(let o of G)owner((o.p+p)%4,o.t.map(i=>ids[i]));owner(p,[a,ids[0],ids[3]]);owner(p,[b,ids[1],ids[4]])}
  for(let list of occ){let p=1;for(let j=1;j<list.length;j++){let a=list[j-1],b=list[j];if(a.s===b.s){let z=opposite(a.i);wire(a.i,z,p);p=3-p;wire(z,b.i,p);p=3-p}else{wire(a.i,b.i,p);p=3-p}}}
  while(D.length%3)vertex(-1,0);
  let partial=D.length,seen=Array.from({length:4},()=>new Uint8Array(partial));for(let {p,t} of C)for(let i of t){ck(!seen[p][i]);seen[p][i]=1}
  for(let p=0;p<4;p++){let missing=[];for(let i=0;i<partial;i++)if(!seen[p][i])missing.push(i);ck(missing.length%3===0);
    for(let j=0;j<missing.length;j+=3){let terminal=[];for(let cp=0;cp<2;cp++){let a=Array.from({length:21},(_,i)=>vertex(-1,Number(Math.floor(i/7)===1)^cp));for(let q=0;q<4;q++)for(let k=0;k<7;k++)if(q!==p||k!==0)owner(q,[a[k],a[7+(k+q)%7],a[14+(k+2*q)%7]]);terminal.push([a[0],a[7+p],a[14+2*p]])}for(let k=0;k<3;k++)owner(p,[missing[j+k],terminal[0][k],terminal[1][k]])}
  }
  let N=D.length,parts=Array.from({length:4},()=>new Uint8Array(N)),pairs=new Set();
  for(let {p,t} of C){ck(new Set(t).size===3);for(let i of t){ck(!parts[p][i]);parts[p][i]=1}for(let a=0;a<3;a++)for(let b=a+1;b<3;b++){let z=[t[a],t[b]].sort((a,b)=>a-b).join(",");ck(!pairs.has(z));pairs.add(z)}}
  for(let p of parts)ck(p.every(x=>x===1));let y=D.map(([v,s])=>s),x=y.slice();x[0]^=1;
  ck(C.filter(o=>!nae(o.t,y)).length===1&&!nae(C[0].t,y));
  for(let side of [0,1]){let w=side?y:x,colors=side?[1,2]:[0,3],count=0,quota=[0,0];for(let {p,t} of C)if(colors.includes(p)){ck(nae(t,w));quota[colors.indexOf(p)]+=t.reduce((a,i)=>a+w[i],0);if(t.includes(0)&&t.filter(i=>i!==0).every(i=>w[i]!==w[0]))count++}ck(quota[0]===quota[1]);ck(count===1)}
  function lift(w,s){let b=w.flatMap(z=>[z,z^1]).concat(s);return D.map(([v,z])=>(v<0?0:b[v])^z)}
  return{C,x,y,N,partial,lift}
 }
 function minIndex(t,w){let a=w[t[0]],b=w[t[1]],c=w[t[2]];return a===b?2:a===c?1:0}
 let lifted=0,bridgeChecks=0,macroChecks=0,controls=[];
 function verifyLift(F,n,w,s){
  let W=F.lift(w,s);ck(F.C.every(o=>nae(o.t,W)));let change=0,dist=0,choices=[];
  for(let i=0;i<F.C.length;i++){let {p,t}=F.C[i],side=p===0||p===3?0:1,ref=side?F.y:F.x,m=minIndex(t,ref),others=[0,1,2].filter(j=>j!==m);
   let candidates=others.filter(j=>W[t[j]]!==W[t[m]]);ck(candidates.length>0);choices.push([side,t[m],t[candidates[0]]]);if(i>0&&i<=3*n){ck(m===0);ck(minIndex(t,W)!==m);ck(candidates.length===1);let q=Number(candidates[0]===2),i0=Math.floor((i-1)/3),j=(i-1)%3;ck(q===(w[i0]^s[j]));change++;dist+=q}
  }ck(change===3*n&&dist>=n);lifted++;
  // Lifted pairing graph: contract all chosen equality pairs and all nondisagreeing copy links.
  let parent=Int32Array.from({length:2*F.N},(_,i)=>i);function root(a){while(parent[a]!==a){parent[a]=parent[parent[a]];a=parent[a]}return a}function join(a,b){parent[root(a)]=root(b)}
  for(let [side,a,b] of choices)join(side*F.N+a,side*F.N+b);for(let i=1;i<F.N;i++)join(i,F.N+i);ck(root(0)!==root(F.N));bridgeChecks++;
 }
 let seed=20261125;function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
 // Macro selector acquisition: allowed mask bits 1,2,3 correspond q=0,1,both.
 // For every pinned s0=0, test three remaining nonconstant selector words.
 function macro(n,A){let ans=[];for(let [u,v] of [[0,1],[1,0],[1,1]]){let s=[0,u,v],r=[];for(let i=0;i<n;i++){let mask=0;for(let b=0;b<2;b++)if(s.every((z,j)=>(A[i][j]>>(b^z))&1))mask|=1<<b;r.push(mask)}if(r.every(x=>x))ans.push({s,r})}return ans}
 for(let n=1;n<=6;n++){for(let k=0;k<300;k++){let A=Array.from({length:n},()=>Array.from({length:3},()=>1+rnd()%3)),ans=macro(n,A),actual=new Set(),pred=new Set();for(let x=0;x<2**n;x++){let w=bits(n,x);for(let s of [[0,0,1],[0,1,0],[0,1,1]]){let z=w.every((b,i)=>s.every((t,j)=>(A[i][j]>>(b^t))&1));if(z)actual.add(w.join("")+":"+s.join(""))}for(let {s,r} of ans)if(w.every((b,i)=>(r[i]>>b)&1))pred.add(w.join("")+":"+s.join(""))}ck(actual.size===pred.size&&[...actual].every(x=>pred.has(x)));macroChecks++}}
 for(let k of [1,2,3,4,8,16]){
  let n=3*k,O=Array.from({length:k},(_,j)=>[3*j,3*j+1,3*j+2]),F=compile(n,O),masks=new Set(),total=0;
  if(k<=4){for(let w of sourceModels(n,O))for(let s of S){let pattern=w.map(b=>b^s[0]).join("");masks.add(pattern);total++}ck(masks.size===6**k);ck(total===6**(k+1))}
  let sample=Array.from({length:k},()=>[0,0,1]).flat();verifyLift(F,n,sample,[0,1,0]);verifyLift(F,n,sample.map(b=>b^1),[1,0,1]);
  controls.push({family:"disjoint",k,n,compiledVariables:F.N,owners:F.C.length,sourceModels:6**k,mandatoryMinorityLower:3*n,allXdistanceLower:n,minimumChartsForCompleteCoverage:6**k/2,enumeratedSelectorColumnPatterns:k<=4?masks.size:null})
 }
 // Unique up to complement family, all mixed triples for balanced target.
 for(let n of [6,8,10]){let words=sourceModels(n,[]).filter(w=>w.reduce((a,b)=>a+b,0)===n/2&&w[0]===0),count=0;for(let w of words){let O=[];for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)for(let c=b+1;c<n;c++)if(nae([a,b,c],w))O.push([a,b,c]);let M=sourceModels(n,O);ck(M.length===2&&M.some(z=>z.join("")===w.join("")));count++}controls.push({family:"balanced unique source",n,complementClasses:count})}
 for(let [name,n,O] of [["Fano",7,fano],["Fano deletion",7,fano.slice(1)],["plane",9,plane],["plane deletion two",9,G.map(o=>o.t)]]){let M=sourceModels(n,O),F=compile(n,O);if(M.length)verifyLift(F,n,M[0],[0,1,0]);controls.push({family:name,n,sourceModels:M.length,compiledVariables:F.N,owners:F.C.length,expandedUnsatNotEnumerated:!M.length})}
 return{checks,lifted,bridgeChecks,macroChecks,modelsG:modelsG.length,controls,scope:"Independent reconstruction of DS17 compiler. Negative expanded labels by projection theorem and source brute force; no expanded UNSAT enumeration or universal solver. No source SAT oracle in compiler. Seed 20261125."}
}
console.log(JSON.stringify(audit(),null,2));

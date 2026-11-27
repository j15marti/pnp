function audit(){
  const ok=(x,msg)=>{if(!x)throw Error(msg)}, bits=(v,n)=>Array.from({length:n},(_,i)=>(v>>i)&1);
  let seed=20261126;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
  const fp=s=>{let h=2166136261;for(let i=0;i<s.length;i++)h=Math.imul(h^s.charCodeAt(i),16777619)>>>0;return h.toString(16).padStart(8,"0")};
  const valid=(F,x)=>F.every(r=>r.reduce((s,i)=>s+x[i],0)===2);
  const clone=x=>JSON.parse(JSON.stringify(x));
  function source(n,F){
    let rows=[],maps=[],next=2*n+2,c0=2*n,c1=c0+1,ext=[];
    for(let x=0;x<n;x++){rows.push([x,n+x,c0,c1]);let h=next++,k=next++;rows.push([c0,x,h,k]);ext.push([x,h,k])}
    for(let [a,b,c,d] of F){let p=next++,q=next++;let start=rows.length;rows.push([a,b,p,q],[n+c,n+d,p,q]);maps.push({a,b,c,d,p,q,start})}
    return {n,nativeN:next,F,rows,maps,ext,pins:[[c0,0],[c1,1]]};
  }
  function liftBase(S,z){let x=Array(S.nativeN).fill(0);for(let i=0;i<S.n;i++){x[i]=z[i];x[S.n+i]=1-z[i]}x[S.pins[1][0]]=1;for(let [i,h,k] of S.ext){x[h]=1;x[k]=1-z[i]}return x}
  function laneA(S,z){let x=liftBase(S,z),trials=0,good=true,local=[];for(let M of S.maps){let hit=false;for(let p=0;p<2;p++)for(let q=0;q<2;q++){trials++;x[M.p]=p;x[M.q]=q;if(valid(S.rows.slice(M.start,M.start+2),x))hit=true}local.push(hit);good&&=hit}return {good,trials,local}}
  function laneB(S,z){let local=[],w=[],checks=0;for(let {a,b,c,d} of S.maps){let s=z[a]^z[b],other=z[c]^z[d];checks++;if(s!==other){local.push(false);w.push(null);continue}let forb=new Set();if(s===0){forb.add(z[a]);forb.add(1-z[c])}let p=[0,1].find(t=>!forb.has(t));local.push(p!==undefined);w.push(p===undefined?null:[p,p^s]);}return {good:local.every(Boolean),local,w,checks}}
  function laneC(S,z){let local=S.maps.map(({a,b,c,d})=>2-z[a]-z[b]===z[c]+z[d]);return {good:local.every(Boolean),local}}
  function integrated(S,z,A,B,C){ok(A.local.every((v,i)=>v===B.local[i]&&v===C.local[i]),"local projection disagreement");ok(C.good===valid(S.F,z),"source adapter");if(!B.good)return false;let x=liftBase(S,z);for(let i=0;i<S.maps.length;i++){let M=S.maps[i];[x[M.p],x[M.q]]=B.w[i]}ok(valid(S.rows,x)&&S.pins.every(([i,v])=>x[i]===v),"native lift");return true}
  const split=[];
  function splitTest(n,F,name){let S=source(n,F),A=clone(S),B=clone(S),C=clone(S),I=clone(S),raw=JSON.stringify(S),sat=0,trials=0,checks=0,local=0;for(let v=0;v<2**n;v++){let z=bits(v,n),a=laneA(A,z),b=laneB(B,z),c=laneC(C,z);trials+=a.trials;checks+=b.checks;local+=F.length; if(integrated(I,z,a,b,c))sat++}split.push({name,originalBoundary:n,nativeVariables:S.nativeN,nativeRows:S.rows.length,originalRows:F.length,encodingBits:8*raw.length,fingerprint:fp(raw),boundaryWords:2**n,accepted:sat,localComparisons:local,occupancyTrials:trials,algebraicChecks:checks})}
  splitTest(4,[[0,1,2,3]],"single");
  const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
  splitTest(14,fano.map((r,i)=>[...r,7+i]),"Fano NO");
  splitTest(13,fano.slice(0,6).map((r,i)=>[...r,7+i]),"Fano deletion YES");
  for(let j=0;j<40;j++){let n=4+rand(5),all=[];for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)for(let c=b+1;c<n;c++)for(let d=c+1;d<n;d++)all.push([a,b,c,d]);let F=[];let m=1+rand(Math.min(8,all.length));for(let i=0;i<m;i++)F.push(all.splice(rand(all.length),1)[0]);splitTest(n,F,"random-"+j)}
  // Coupled private coordinates: actual native row (boundary anchor, private i, private j, fresh completion).
  // B constructs conditional implications, evaluates reachability circuit, reconstructs by paid pin tests.
  function graphSat(p,edges,pins=[]){let n=2*p,R=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j));for(let [i,j] of edges)R[i][j]=true;for(let [i,v] of pins)R[2*i+1-v][2*i+v]=true;for(let k=0;k<n;k++)for(let i=0;i<n;i++)for(let j=0;j<n;j++)R[i][j]||=R[i][k]&&R[k][j];return !Array.from({length:p},(_,i)=>R[2*i][2*i+1]&&R[2*i+1][2*i]).some(Boolean)}
  function coupledSource(b,p,E){let c0=b+p+E.length,next=c0+1,rows=E.map(([a,i,j],k)=>[a,b+i,b+j,b+p+k]),ex=[];for(let a=0;a<b;a++){let h=next++,k=next++;rows.push([c0,a,h,k]);ex.push([a,h,k])}return {b,p,E,rows,c0,ex,n:next}}
  function coupledLift(S,z,t,w){let x=Array(S.n).fill(0);for(let i=0;i<S.b;i++)x[i]=z[i];for(let i=0;i<S.p;i++)x[S.b+i]=t[i];for(let i=0;i<w.length;i++)x[S.b+S.p+i]=w[i];for(let [a,h,k] of S.ex){x[h]=1;x[k]=1-z[a]}return x}
  function directA(S,z){let trials=0;for(let v=0;v<2**S.p;v++){trials++;let t=bits(v,S.p),w=S.E.map(([a,i,j])=>2-z[a]-t[i]-t[j]);if(w.every(v=>v===0||v===1)){let x=coupledLift(S,z,t,w);ok(valid(S.rows,x),"A lift");return {yes:true,trials}}}return {yes:false,trials}}
  function graphB(S,z){let edges=[];for(let [a,i,j] of S.E){let v=z[a];edges.push([2*i+v,2*j+1-v],[2*j+v,2*i+1-v])}let calls=1;if(!graphSat(S.p,edges))return {yes:false,calls};let pins=[];for(let i=0;i<S.p;i++){calls++;pins.push([i,0]);if(!graphSat(S.p,edges,pins))pins[pins.length-1][1]=1}let t=pins.map(x=>x[1]),w=S.E.map(([a,i,j])=>2-z[a]-t[i]-t[j]);ok(w.every(v=>v===0||v===1),"B completion");return {yes:true,calls,witness:coupledLift(S,z,t,w)}}
  function bruteC(S,z){let trials=0;for(let v=0;v<2**(S.p+S.E.length);v++){trials++;let x=bits(v,S.p+S.E.length),w=coupledLift(S,z,x.slice(0,S.p),x.slice(S.p));if(valid(S.rows,w))return {yes:true,trials}}return {yes:false,trials}}
  let coupled=[];
  function coupledTest(b,p,E,name){let S=coupledSource(b,p,E),A=clone(S),B=clone(S),C=clone(S),I=clone(S),raw=JSON.stringify(S),n=0,yes=0,ta=0,tb=0,tc=0;for(let v=0;v<2**b;v++){let z=bits(v,b),a=directA(A,z),c=bruteC(C,z),g=graphB(B,z);ok(a.yes===c.yes&&c.yes===g.yes,"coupled agreement");ta+=a.trials;tb+=g.calls;tc+=c.trials;n++;if(g.yes){yes++;ok(valid(I.rows,g.witness)&&g.witness[I.c0]===0,"integrated witness")}}coupled.push({name,b,p,m:E.length,encodingBits:8*raw.length,fingerprint:fp(raw),words:n,accepted:yes,privateTrials:ta,reachabilityCalls:tb,fullNativeTrials:tc})}
  // Two disjoint forced opposite-edge triangles on same three private variables when both boundary anchors differ.
  // Each edge with both anchor values enforces disequality; odd triangle impossible.
  coupledTest(2,3,[[0,0,1],[1,0,1],[0,1,2],[1,1,2],[0,0,2],[1,0,2]],"coupled odd cycle");
  for(let i=0;i<40;i++){let b=2+rand(2),p=3+rand(3),E=[];let m=3+rand(4);for(let j=0;j<m;j++){let a=rand(b),u=rand(p),v=rand(p-1);if(v>=u)v++;E.push([a,Math.min(u,v),Math.max(u,v)])}coupledTest(b,p,E,"random-"+i)}
  return {seed:20261126,execution:"sequential same-source copies, finite exhaustive boundary words",split,coupled};
}
console.log(JSON.stringify(audit(),null,2));

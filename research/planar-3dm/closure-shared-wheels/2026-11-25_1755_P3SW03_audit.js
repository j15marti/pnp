function runAudit(){
 let seed=20261125,stats={seed:20261125,checks:0,cases:0,sat:0,unsat:0,oneSided:0,mixed:0,closureNO:0,branchNodes:0,relaxScans:0,forcedDeletions:0,smallFamilies:{},large:[],examples:{}};
 const check=(q,m)=>{stats.checks++;if(!q)throw Error(m)};
 const rnd=n=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed%n};
 // E entries [x,y,z,left,right,hostFace]. All original projection edges retained for height equations.
 function matching(E,n,A,a,b,required=[]){
   const mx=Array(n).fill(-1),my=Array(n).fill(-1),adj=Array.from({length:n},()=>[]),locked=new Set();
   for(const i of required){if(!A[i])return null;const e=E[i],u=e[a],v=e[b];if(mx[u]>=0||my[v]>=0)return null;mx[u]=i;my[v]=i;locked.add(u)}
   for(let i=0;i<E.length;i++)if(A[i])adj[E[i][a]].push(i);
   function visit(u,seen){if(locked.has(u))return false;for(const i of adj[u]){const v=E[i][b];if(seen[v])continue;seen[v]=true;const old=my[v];if(old<0||visit(E[old][a],seen)){mx[u]=i;my[v]=i;return true}}return false}
   for(let u=0;u<n;u++)if(mx[u]<0&&!visit(u,Array(n).fill(false)))return null;
   return {mx,my};
 }
 function closure(E,n,A){A=A.slice();for(;;){
   let changed=false;for(let c=0;c<3;c++){const adj=Array.from({length:n},()=>[]);E.forEach((e,i)=>{if(A[i])adj[e[c]].push(i)});if(adj.some(v=>!v.length))return null;
   for(const a of adj)if(a.length===1){let i=a[0];if(!A[i])return null;for(let j=0;j<E.length;j++)if(A[j]&&j!==i&&E[j].slice(0,3).some((v,c)=>v===E[i][c])){A[j]=false;changed=true;stats.forcedDeletions++}}}
   for(const [a,b] of [[0,1],[0,2],[1,2]]){let M=matching(E,n,A,a,b);if(!M)return null;
    const adj=Array.from({length:n},()=>[]);E.forEach((e,i)=>{if(A[i])adj[e[a]].push(E[M.my[e[b]]][a])});
    const reach=adj.map((_,s)=>{let seen=new Set([s]),q=[s];for(let k=0;k<q.length;k++)for(const t of adj[q[k]])if(!seen.has(t)){seen.add(t);q.push(t)}return seen});
    E.forEach((e,i)=>{if(A[i]&&!reach[E[M.my[e[b]]][a]].has(e[a])){A[i]=false;changed=true;stats.forcedDeletions++}});
   }if(!changed)return A;
 }}
 function verify(E,n,ids){return ids.length===n&&[0,1,2].every(c=>new Set(ids.map(i=>E[i][c])).size===n)}
 function brute(E,n){let adj=Array.from({length:n},()=>[]);E.forEach((e,i)=>adj[e[0]].push(i));const Y=new Set(),Z=new Set(),w=[];
  function rec(x){if(x===n)return w.slice();for(const i of adj[x]){let e=E[i];if(Y.has(e[1])||Z.has(e[2]))continue;Y.add(e[1]);Z.add(e[2]);w.push(i);let a=rec(x+1);if(a)return a;w.pop();Y.delete(e[1]);Z.delete(e[2])}return null}return rec(0)}
 function compile(E,n,F,A){
  const M=matching(E,n,A,0,1);if(!M)return null;const sel=new Set(M.mx),s=E.map((_,i)=>Number(sel.has(i))),D=[],P=[],Q=[],groups=Array.from({length:n},()=>[]);
  // h[v] <= max(h[a]+c,h[b]+d); use repeated a for a single difference.
  const diff=(v,a,c)=>D.push([v,a,c,a,c]);
  E.forEach((e,i)=>{const [x,y,z,l,r,f]=e;check(f===l||f===r,"host face incidence");diff(l,r,(A[i]?1:0)-s[i]);diff(r,l,s[i]);if(A[i])groups[z].push(i)});
  const badP=new Set(),badQ=new Set();
  for(let z=0;z<n;z++){let ids=groups[z];check(ids.every(i=>E[i][5]===E[ids[0]][5]),"one host face per label in these connected fixtures");
   for(let u=0;u<ids.length;u++)for(let v=u+1;v<ids.length;v++){
    let i=ids[u],j=ids[v],e=E[i],g=E[j];if(e[0]===g[0]||e[1]===g[1])continue;
    // omit constant bridges only if zero; for selected constant bridges the other edge must be zero
    if(e[3]===e[4]||g[3]===g[4]){if(g[3]===g[4]){[i,j]=[j,i];[e,g]=[g,e]}if(s[i]===1){diff(g[3],g[4],-s[j]);}continue}
    const f=e[5],ep=e[3]===f,gp=g[3]===f, a=ep?e[4]:e[3],b=gp?g[4]:g[3];
    if(ep!==gp){if(ep)diff(b,a,1-s[i]-s[j]);else diff(a,b,1-s[i]-s[j]);}
    else if(a===b){ // two indicators with the same difference; sum <=1, integer floor
      if(ep)diff(f,a,Math.floor((1-s[i]-s[j])/2));else diff(a,f,Math.floor((1-s[i]-s[j])/2));
    }else if(ep){P.push([f,a,-s[i],b,-s[j],z]);badP.add(z)}
    else{Q.push([f,a,s[i],b,s[j],z]);badQ.add(z)}
   }
  }
  return {s,D,P,Q,groups,badP,badQ,F};
 }
 function greatest(F,m,atoms){
  let h=Array(F).fill(m);h[0]=0;
  for(;;){let changed=false;for(const [v,a,c,b,d] of atoms){stats.relaxScans++;let t=Math.max(h[a]+c,h[b]+d);if(h[v]>t){h[v]=t;changed=true;if(h[v]<-m||v===0)return null}}if(!changed)return h}
 }
 function candidate(E,n,C,flip){const {D,P,Q,F,s}=C;let atoms=flip?D.map(([v,a,c])=>[a,v,c,v,c]).concat(Q.map(([v,a,c,b,d])=>[v,a,-c,b,-d])):D.concat(P);
  let h=greatest(F,E.length,atoms);if(!h)return {no:true};if(flip)h=h.map(x=>-x);
  const w=[];for(let i=0;i<E.length;i++){let q=s[i]+h[E[i][3]]-h[E[i][4]];check(q===0||q===1,"binary lift");if(q)w.push(i)}
  check(w.length===n&&new Set(w.map(i=>E[i][0])).size===n&&new Set(w.map(i=>E[i][1])).size===n,"XY lift");
  return {w:verify(E,n,w)?w:null,h};
 }
 // Minority-label enumeration. All choices tried; cap only limits number of labels, not logical completeness.
 function solve(E,n,F,A,cap=5,root=true){stats.branchNodes++;A=closure(E,n,A);if(!A){if(root)stats.closureNO++;return {status:"NO",kind:"closure"}}
  let C=compile(E,n,F,A);check(!!C,"closure projection");let flip=C.badP.size<C.badQ.size;
  if(root){if(C.badP.size&&C.badQ.size)stats.mixed++;else stats.oneSided++;}
  let r=candidate(E,n,C,flip);if(r.no)return {status:"NO",kind:"relaxation"};if(r.w){check(r.w.every(i=>A[i]),"pins preserved");return {status:"YES",kind:C.badP.size&&C.badQ.size?"mixed-relaxation":"one-sided",w:r.w}}
  let bad=flip?C.badP:C.badQ;if(!bad.size)throw Error("one-sided invalid lift");
  if(bad.size>cap||cap<=0)return {status:"UNKNOWN",kind:"cap"};
  let z=[...bad][0],unknown=false;
  for(let i of C.groups[z]){let B=A.slice();E.forEach((e,j)=>{if(j!==i&&e.slice(0,3).some((v,c)=>v===E[i][c]))B[j]=false});let a=solve(E,n,F,B,cap-1,false);if(a.status==="YES")return a;if(a.status==="UNKNOWN")unknown=true}
  return {status:unknown?"UNKNOWN":"NO",kind:"branch"};
 }
 // Geometrically explicit plane ladder/ring projection; label spokes in each host face are contiguous intervals.
 function fixture(n,ring=false){
  let E=[],faces=Array.from({length:ring?n+2:n},()=>[]),rungs=[],bottom=[],top=[];
  function add(j,r,k,t,L,R){let x,y;if((j+r)%2===0){x=j;y=k;}else{x=k;y=j;[L,R]=[R,L]} // each column has exactly one X and one Y
   let i=E.length;E.push([x,y,-1,L,R,-1]);return i}
  for(let j=0;j<n;j++)rungs.push(add(j,0,j,1,ring?j+1:(j===0?0:j),ring?((j+n-1)%n)+1:(j===n-1?0:j+1)));
  for(let j=0;j<(ring?n:n-1);j++){let k=(j+1)%n;bottom.push(add(j,0,k,0,ring?n+1:j+1,ring?j+1:0));top.push(add(j,1,k,1,ring?j+1:0,ring?0:j+1))}
  if(ring){for(let j=0;j<n;j++){for(const i of [rungs[j],bottom[j],top[j]]){E[i][2]=j;E[i][5]=j+1}}return {E,F:n+2,n}}
  for(let j=0;j<n-1;j++)faces[j+1]=[bottom[j],rungs[j+1],top[j],rungs[j]];
  faces[0]=bottom.concat([rungs[n-1]],top.slice().reverse(),[rungs[0]]);
  E.forEach(e=>e[5]=rnd(2)?e[3]:e[4]);
  let groups=faces.map((ls,f)=>ls.filter(i=>E[i][5]===f)).filter(a=>a.length);
  while(groups.length<n){let opts=groups.map((a,i)=>a.length>1?i:-1).filter(i=>i>=0),i=opts[rnd(opts.length)],a=groups[i],j=1+rnd(a.length-1);groups.splice(i,1,a.slice(0,j),a.slice(j))}
  groups.forEach((a,z)=>a.forEach(i=>E[i][2]=z));check(E.every(e=>e[2]>=0),"all labels assigned");return {E,F:n,n}
 }
 function small(f,name){const {E,n,F}=f,A=E.map(()=>true),b=brute(E,n),r=solve(E,n,F,A,9);stats.cases++;if(b)stats.sat++;else stats.unsat++;
  check(r.status===(b?"YES":"NO"),"exact comparison "+name);if(r.w)check(verify(E,n,r.w),"source witness");
  const s=stats.smallFamilies[name]??={cases:0,sat:0,unsat:0};s.cases++;s[b?"sat":"unsat"]++;
 }
 // square all-two labels, same-sign collision for both labels, opposite host faces => common polarity
 const square={n:2,F:2,E:[[0,0,0,0,1,0],[1,1,0,0,1,0],[0,1,1,1,0,1],[1,0,1,1,0,1]]};
 // In this square both label faces are the left face of their two opposite edges.
 small(square,"one-sided-square-NO");
 const squareSat={n:2,F:2,E:square.E.map(e=>e.slice())};squareSat.E[1][2]=1;squareSat.E[1][5]=1;squareSat.E[2][2]=0;squareSat.E[2][5]=0;small(squareSat,"square-SAT");
 for(let n=2;n<=9;n++)for(let k=0;k<45;k++)small(fixture(n),"ladder");
 for(let n of [4,6,8,10])small(fixture(n,true),"ring");
 // P3AGE03 genuine planar controls, rotation-derived face data verified separately by NetworkX.
 const T0=[[0,0,0,0,1,1],[0,0,2,2,0,2],[0,1,0,1,6,1],[0,1,1,6,4,4],[0,2,1,4,7,4],[0,2,2,7,2,2],[1,0,0,1,5,1],[1,0,1,5,4,4],[1,1,1,4,1,4],[2,0,1,4,3,4],[2,0,2,3,2,2],[2,2,1,2,4,4]];
 const T1=T0.map(e=>e.slice());T1[8][4]=8;T1.push([1,1,0,8,1,1]);
 small({E:T0,n:3,F:8},"AGE03-NO");small({E:T1,n:3,F:9},"AGE03-YES");
 for(let n of [16,32,64,128,256]){let {E,F}=fixture(n,true),A=closure(E,n,E.map(()=>true));check(A&&A.every(Boolean),"ring all support");let C=compile(E,n,F,A);check(C.badP.size===n/2&&C.badQ.size===n/2,"ring mixed linear");
  let r=solve(E,n,F,A,0);check(verify(E,n,Array.from({length:n},(_,i)=>i)),"ring explicit witness");check(r.status!=="NO","ring no false reject");stats.large.push({n,triples:E.length,faces:F,positiveLabels:C.badP.size,negativeLabels:C.badQ.size,status:r.status,allProjectionsSupported:true})}
 return stats;
}
console.log(JSON.stringify(runAudit(),null,2));

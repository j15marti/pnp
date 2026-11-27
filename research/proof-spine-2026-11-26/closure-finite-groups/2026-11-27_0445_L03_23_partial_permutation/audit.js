const result=(function audit(){
 const out=[], seed=2611270445;let rng=seed>>>0;
 const rand=n=>{rng=(Math.imul(rng,1664525)+1013904223)>>>0;return rng%n;};
 const range=n=>Array.from({length:n},(_,i)=>i), mod=(x,n)=>((x%n)+n)%n;
 const perm=n=>{let p=range(n);for(let i=n-1;i>0;i--){let j=rand(i+1);[p[i],p[j]]=[p[j],p[i]];}return p;};
 const assert=(v,s)=>{if(!v)throw Error(s);};
 const cap=20000000;
 function meter(){let n=0;return {tick(k=1){n+=k;if(n>cap)throw Error("CAP");},get n(){return n;}}}
 function mk(n,r,c){
  let P=perm(n),Q=perm(n),Z=perm(n),R=perm(n).slice(0,r),C=perm(n).slice(0,c),rr=new Set(R),cc=new Set(C),e=[],extra=[];
  for(let i=0;i<n;i++)for(let j=0;j<n;j++){
   e.push([P[i],Q[j],Z[(i+j)%n],i*n+j]);
   if(rr.has(i)||cc.has(j))extra.push([P[i],Q[j],Z[(i+j+1)%n],n*n+extra.length]);
  }
  return {n,e,extra,P,Q,Z,R,C};
 }
 function cells(n,E,m){let A=range(n).map(()=>range(n).map(()=>[]));for(let [i,j,z] of E){m.tick();A[i][j].push(z);}return A;}
 function cover(A,m){
  let n=A.length, mt=Array(n).fill(-1), adj=A.map(row=>row.map((x,j)=>x.length>1?j:-1).filter(j=>j>=0));
  function aug(i,seen){for(let j of adj[i]){m.tick();if(seen[j])continue;seen[j]=true;if(mt[j]<0||aug(mt[j],seen)){mt[j]=i;return true;}}return false;}
  for(let i=0;i<n;i++)aug(i,Array(n).fill(false));
  let rt=Array(n).fill(-1);for(let j=0;j<n;j++)if(mt[j]>=0)rt[mt[j]]=j;
  let rs=new Set(range(n).filter(i=>rt[i]<0)),cs=new Set(),q=[...rs];
  for(let h=0;h<q.length;h++){let i=q[h];for(let j of adj[i]){m.tick();if(rt[i]===j||cs.has(j))continue;cs.add(j);if(mt[j]>=0&&!rs.has(mt[j])){rs.add(mt[j]);q.push(mt[j]);}}}
  let R=range(n).filter(i=>!rs.has(i)),C=[...cs];assert(R.length+C.length===mt.filter(x=>x>=0).length,"cover count");
  for(let i=0;i<n;i++)for(let j of adj[i]){m.tick();assert(R.includes(i)||cs.has(j),"cover invalid");}
  return {R,C};
 }
 function cyclic(p,m){let n=p.length,l=Array(n).fill(-1),z=0;for(let k=0;k<n;k++){m.tick();if(z<0||l[z]>=0)return null;l[z]=k;z=p[z];}return z===0?l:null;}
 function pick(S,n){if(S.size===1)return [...S][0];if(S.size!==2)return null;let [x,y]=[...S];return mod(y-x,n)===1?x:mod(x-y,n)===1?y:null;}
 function check(E,n,l,u,v,R,C,m){
  let d=mod(l.reduce((a,b)=>a+b,0)-u.reduce((a,b)=>a+b,0)-v.reduce((a,b)=>a+b,0),n);
  let r=new Set(R),c=new Set(C),positive=0;
  for(let [i,j,z] of E){m.tick();let w=mod(l[z]-u[i]-v[j],n);if(w>1||w===1&&!r.has(i)&&!c.has(j))return null;positive+=w;}
  return R.length+C.length<d?{l,u,v,R,C,delta:d,positive}:null;
 }
 function reconstruct(A,E,l,I,J,R,C,m){
  let n=A.length,a=I[0],u=Array(n),v=Array(n);
  for(let j of J)v[j]=l[A[a][j][0]];
  for(let i=0;i<n;i++){let s=new Set();for(let j of J)for(let z of A[i][j]){m.tick();s.add(mod(l[z]-v[j],n));}u[i]=pick(s,n);if(u[i]===null)return null;}
  for(let j=0;j<n;j++){let s=new Set();for(let i=0;i<n;i++)for(let z of A[i][j]){m.tick();s.add(mod(l[z]-u[i],n));}v[j]=pick(s,n);if(v[j]===null)return null;}
  return check(E,n,l,u,v,R,C,m);
 }
 // A: old dictionary structural admission, full candidate search with capacity cover
 function old(n,E,m){
  for(let trans=0;trans<2;trans++){
   let F=trans?E.map(([i,j,z,id])=>[j,i,z,id]):E,A=cells(n,F,m),{R,C}=cover(A,m);
   for(let omit=-1;omit<n;omit++){
    let rows=[];for(let i=0;i<n;i++){let p=Array(n).fill(-1),s=new Set(),ok=true;
     for(let j=0;j<n;j++)if(j!==omit){m.tick();if(A[i][j].length!==1||s.has(A[i][j][0])){ok=false;break;}p[j]=A[i][j][0];s.add(p[j]);}
     if(ok&&omit>=0){let z=range(n).find(x=>!s.has(x));if(!A[i][omit].includes(z))ok=false;else p[omit]=z;}
     if(ok)rows.push(p);
    }
    for(let a of rows)for(let b of rows){if(a===b)continue;let p=Array(n);for(let j=0;j<n;j++){m.tick();p[a[j]]=b[j];}
     let l=cyclic(p,m);if(!l)continue;let v=a.map(z=>l[z]),u=[];
     for(let i=0;i<n;i++){let s=new Set();for(let j=0;j<n;j++)for(let z of A[i][j]){m.tick();s.add(mod(l[z]-v[j],n));}u.push(pick(s,n));}
     if(u.some(x=>x===null))continue;let cert=check(F,n,l,u,v,R,C,m);
     if(cert)return trans?{...cert,u:cert.v,v:cert.u,R:cert.C,C:cert.R}:cert;
    }
   }
  }return null;
 }
 // B: build partial maps independently of the modular verifier.
 function glue(A,I,J,m){
  let n=A.length,G=[],maps=0;
  for(let a of I)for(let b of I){if(a===b)continue;
   let p=Array(n).fill(-1);
   for(let j of J){m.tick();assert(A[a][j].length===1&&A[b][j].length===1,"bad clean rectangle");p[A[a][j][0]]=A[b][j][0];}
   maps++;let g=null;
   for(let q of G){let ok=true;for(let z=0;z<n;z++){m.tick();if(p[z]>=0&&q[z]>=0&&p[z]!==q[z]){ok=false;break;}}if(ok){g=q;break;}}
   if(!g){G.push(p);continue;}
   for(let z=0;z<n;z++)if(p[z]>=0){m.tick();g[z]=p[z];}
  }
  return {G,maps};
 }
 function hybrid(n,E,m){
  let A=cells(n,E,m),{R,C}=cover(A,m);if(2*(R.length+C.length)>=n)return {cert:null};
  let I=range(n).filter(i=>!R.includes(i)),J=range(n).filter(j=>!C.includes(j));
  let {G,maps}=glue(A,I,J,m);
  let complete=G.filter(g=>g.every(x=>x>=0)&&new Set(g).size===n),cycles=0;
  for(let p of complete){let l=cyclic(p,m);if(!l)continue;cycles++;let cert=reconstruct(A,E,l,I,J,R,C,m);if(cert)return {cert,maps,groups:G.length,complete:complete.length,cycles,cover:R.length+C.length};}
  return {cert:null,maps,groups:G.length,complete:complete.length,cycles,cover:R.length+C.length};
 }
 // C: independent enumeration of exact owner covers, capped; separate planted certificate replay.
 function brute(n,E,m){
  if(n>10)return "NOT_RUN";
  let rows=range(n).map(()=>[]);for(let [i,j,z] of E)rows[i].push([j,z]);
  rows.sort((a,b)=>a.length-b.length);
  function f(i,cols,colors){m.tick();if(i===n)return true;for(let [j,z] of rows[i]){m.tick();if(!(cols&(1<<j))&&!(colors&(1<<z))&&f(i+1,cols|(1<<j),colors|(1<<z)))return true;}return false;}
  return f(0,0,0)?"YES":"NO";
 }
 function replay(E,n,c){let R=new Set(c.R),C=new Set(c.C),d=mod(c.l.reduce((a,b)=>a+b,0)-c.u.reduce((a,b)=>a+b,0)-c.v.reduce((a,b)=>a+b,0),n);
  assert(d===c.delta&&R.size+C.size<d,"bad residue");
  for(let [i,j,z] of E){let w=mod(c.l[z]-c.u[i]-c.v[j],n);assert(w===0||w===1&&(R.has(i)||C.has(j)),"bad original edge");}
 }
 function run(fn){let m=meter();try{return {v:fn(m),ops:m.n};}catch(e){if(String(e).includes("CAP"))return {v:null,ops:m.n,capped:true};throw e;}}
 for(let n of [8,10,12,16,24,32,48,64]){
  let r=Math.floor((n/2-1)/2),c=n/2-1-r,P=mk(n,r,c);
  for(let t of [0,Math.floor(P.extra.length/2),P.extra.length]){
   let E=P.e.concat(P.extra.slice(0,t)).map(x=>x.slice()); // shuffle presentation independent of hidden labels
   for(let i=E.length-1;i>0;i--){let j=rand(i+1);[E[i],E[j]]=[E[j],E[i]];}
   let id=new Set(E.map(x=>x[3]));assert(id.size===E.length,"ID");
   let h=2166136261;for(let x of E)for(let v of x){h=Math.imul(h^v,16777619)>>>0;}
   let inv=p=>{let a=[];p.forEach((z,i)=>a[z]=i);return a;};
   let planted={l:inv(P.Z),u:inv(P.P),v:inv(P.Q),R:P.R.map(i=>P.P[i]),C:P.C.map(i=>P.Q[i]),delta:n/2};
   replay(E,n,planted);
   let A=run(m=>old(n,E,m)), B=run(m=>hybrid(n,E,m)), C=run(m=>brute(n,E,m));
   assert(B.v?.cert,"hybrid failed");replay(E,n,B.v.cert);if(A.v)replay(E,n,A.v);
   assert(C.v!=="YES","unexpected cover");
   let {cert,...metrics}=B.v;
   out.push({n,r,c,t,parent_extras:P.extra.length,active:E.length,hash:h.toString(16),old:!!A.v,old_ops:A.ops,old_capped:!!A.capped,hybrid:metrics,hybrid_ops:B.ops,certificate:{...cert},reference:C.v??"CAP",reference_ops:C.ops});
  }
 }
 // minimal YES falsifier: shifted diagonal edges in first half, base diagonal in second half
 let n=8,E=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)E.push([i,j,(i+j)%n,i*n+j]);for(let i=0;i<n/2;i++)E.push([i,i,(2*i+1)%n,n*n+i]);
 let W=range(n).map(i=>[i,i,(2*i+(i<n/2?1:0))%n]);assert(new Set(W.map(x=>x[2])).size===n,"YES witness");
 let Y=run(m=>hybrid(n,E,m));assert(!Y.v?.cert,"false reject");
 return {seed,cap,instances:out,yes_control:{n,hybrid:!!Y.v?.cert,witness:W,ops:Y.ops}};
})();
console.log(JSON.stringify(result,null,2));

function experiment(){
  let state=0x5f062026; const rand=n=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state%n;};
  const assert=(x,msg)=>{if(!x)throw Error(msg);};
  const counts={random:0,sat:0,unsat:0,assignments:0,hullChecks:0,tagChecks:0,verifiedLifts:0,cutChecks:0,closureDeletions:0,augmentations:0,cycles:0};
  function basis(){const piv=new Map();return {piv,add(x){while(x){const k=x.toString(2).length-1;if(piv.has(k))x^=piv.get(k);else{piv.set(k,x);return true;}}return false;},has(x){while(x){const k=x.toString(2).length-1;if(!piv.has(k))return false;x^=piv.get(k);}return true;}};}
  function prepare(rows,K){let n=0;return rows.map(rs=>rs.map(c=>({c:c.map(BigInt),id:n++}))); }
  function valid(rows,K,m){const cost=K.map(()=>0n);for(const rs of rows){let selected=0;for(const r of rs)if(m>>BigInt(r.id)&1n){selected++;r.c.forEach((x,i)=>cost[i]+=x);}if(selected!==1)return false;}return cost.every((x,i)=>x<=K[i]);}
  function solve(rows,K,features=true){
    let active=rows.map(rs=>rs.slice()),base,rem;
    // All deductions are unconditional relative to the supplied fixed guard.
    while(true){
      if(active.some(rs=>!rs.length))return {sat:false,kind:"empty"};
      base=active.map(rs=>K.map((_,j)=>rs.reduce((m,r)=>r.c[j]<m?r.c[j]:m,rs[0].c[j])));
      rem=K.map((k,j)=>k-base.reduce((s,b)=>s+b[j],0n));
      if(rem.some(x=>x<0n))return {sat:false,kind:"minima"};
      let changed=false;
      active=active.map((rs,i)=>rs.filter(r=>{const keep=r.c.every((v,j)=>v-base[i][j]<=rem[j]);if(!keep){changed=true;counts.closureDeletions++;}return keep;}));
      if(!changed)break;
    }
    const B=active.length,O=K.length,d=K.map(()=>0n);
    for(let i=0;i<B;i++)for(const r of active[i]){
      const nz=[];r.c.forEach((x,j)=>{const a=x-base[i][j];if(a){nz.push(j);if(d[j]===0n)d[j]=a;assert(d[j]===a,"unsupported differing unit");}});
      assert(nz.length<=1,"unsupported multi-owner increment");r.owner=nz.length?nz[0]:O;
    }
    const s=0,ob=1+B,t=ob+O+1,V=t+1;
    const adj=Array.from({length:V},()=>[]),orig=[];
    function add(u,v,cap,tag=0n){const a={u,v,cap,tag},b={u:v,v:u,cap:0,tag};a.rev=b;b.rev=a;adj[u].push(a);adj[v].push(b);orig.push({a,cap});return a;}
    const ar=[];
    for(let i=0;i<B;i++){add(s,i+1,1);for(const r of active[i])ar.push({r,a:add(i+1,ob+r.owner,1,1n<<BigInt(r.id))});}
    for(let j=0;j<O;j++){const cap=d[j]===0n?0n:rem[j]/d[j];add(ob+j,t,Number(cap>BigInt(B)?BigInt(B):cap));}add(ob+O,t,B);
    function bfs(u,allowed=null){const pred=Array(V).fill(null),q=[u];pred[u]=false;for(let p=0;p<q.length;p++)for(const a of adj[q[p]])if(a.cap>0&&pred[a.v]===null&&(!allowed||allowed.has(a.v))){pred[a.v]=a;q.push(a.v);}return {pred,q};}
    function path(pred,v){const p=[];while(pred[v]){p.push(pred[v]);v=pred[v].u;}return p.reverse();}
    let flow=0;
    while(flow<B){const {pred,q}=bfs(s);if(pred[t]===null){const set=new Set(q);const cap=orig.reduce((n,{a,cap})=>n+(set.has(a.u)&&!set.has(a.v)?cap:0),0);assert(cap===flow,"cut invalid");counts.cutChecks++;return {sat:false,kind:"cut",flow,cut:cap};}for(const a of path(pred,t)){a.cap--;a.rev.cap++;}flow++;counts.augmentations++;}
    let anchor=0n;for(const {r,a} of ar)if(a.cap===0)anchor|=1n<<BigInt(r.id);
    assert(valid(rows,K,anchor),"anchor invalid");counts.verifiedLifts++;
    if(!features)return {sat:true,anchor,flow};
    const span=basis(),witnesses=[anchor];
    // Small-test SCC discovery via reachability (polynomial); production can use Tarjan.
    const reach=Array.from({length:V},(_,u)=>new Set(bfs(u).q));const seen=new Set();
    function cycleCheck(c){counts.cycles++;let delta=0n;for(const a of c)delta^=a.tag;const w=anchor^delta;assert(valid(rows,K,w),"cycle witness invalid");counts.verifiedLifts++;if(span.add(delta))witnesses.push(w);}
    function walkCycles(w,start){let vs=[start],es=[];for(const a of w){assert(vs[vs.length-1]===a.u,"walk mismatch");const k=vs.indexOf(a.v);if(k>=0){cycleCheck(es.slice(k).concat(a));vs=vs.slice(0,k+1);es=es.slice(0,k);}else{es.push(a);vs.push(a.v);}}assert(es.length===0,"not closed");}
    for(let root=0;root<V;root++)if(!seen.has(root)){
      const comp=new Set([...reach[root]].filter(v=>reach[v].has(root)));for(const v of comp)seen.add(v);
      if(comp.size===1)continue;
      const pref=bfs(root,comp).pred,back=new Map([...comp].map(v=>[v,path(bfs(v,comp).pred,root)]));
      for(const v of comp){walkCycles(path(pref,v).concat(back.get(v)),root);for(const a of adj[v])if(a.cap>0&&comp.has(a.v))walkCycles(path(pref,v).concat(a,back.get(a.v)),root);}
    }
    return {sat:true,anchor,span,witnesses,flow};
  }
  function exhaustive(rows,K){let sols=[];function rec(i,m){if(i===rows.length){counts.assignments++;if(valid(rows,K,m))sols.push(m);return;}for(const r of rows[i])rec(i+1,m|(1n<<BigInt(r.id)));}rec(0,0n);return sols;}
  const parity=x=>{let p=0;while(x){x&=x-1n;p^=1;}return p;};
  const cases=[];
  function compare(raw,k,name){const K=k.map(BigInt),rows=prepare(raw,K),ans=solve(rows,K),ref=exhaustive(rows,K);assert(ans.sat===(ref.length>0),"decision "+name);if(ans.sat){counts.sat++;const b=basis();for(const x of ref)b.add(x^ans.anchor);assert(b.piv.size===ans.span.piv.size,"rank "+name);for(const x of ref)assert(ans.span.has(x^ans.anchor),"span missing");for(const x of ans.witnesses)assert(b.has(x^ans.anchor),"span excess");counts.hullChecks++;
      for(let j=0;j<8;j++){const n=rows.flat().length;let mask=0n;for(let z=0;z<n;z++)if(rand(7)<3)mask|=1n<<BigInt(z);for(let bit=0;bit<2;bit++){const w=ans.witnesses.find(x=>parity(x&mask)===bit);assert((w!==undefined)===ref.some(x=>parity(x&mask)===bit),"tag");counts.tagChecks++;}}
    }else counts.unsat++;cases.push({name,sat:ans.sat,feasible:ref.length,rank:ans.sat?ans.span.piv.size:null,kind:ans.kind??"flow"});}
  for(let z=0;z<240;z++){const O=2+rand(4),B=2+rand(5),d=Array.from({length:O},()=>BigInt(1+rand(5))*(z%7===0?1n<<70n:1n));const raw=Array.from({length:B},()=>{const base=Array.from({length:O},()=>BigInt(rand(3)));return Array.from({length:2+rand(3)},()=>{const c=base.slice(),j=rand(O+1);if(j<O)c[j]+=d[j];return c;});});const chosen=raw.map(rs=>rs[rand(rs.length)]);const K=Array.from({length:O},(_,j)=>chosen.reduce((s,r)=>s+r[j],0n)+(z%3===0?d[j]:z%3===1?0n:-d[j]));compare(raw,K,"random-"+z);counts.random++;}
  compare([[[1,0,0],[0,1,0]],[[1,0,0],[0,1,0]],[[1,0,0],[0,1,0]],[[0,0,1],[0,0,1]]],[1,1,2],"Hall hostile");
  compare([[[0,0],[0,0]],[[1,0],[0,1]]],[1,1],"equal-cost distinct rows");
  const scaling=[];
  for(const h of [5,9,17,25,41]){
    const raw=[];for(let i=0;i<h;i++)for(let j=i+1;j<h;j++){const a=Array(h).fill(0),b=a.slice();a[i]=1;b[j]=1;raw.push([a,b]);}
    for(const sat of [true,false]){const K=Array(h).fill(BigInt((h-1)/2));if(!sat)K[0]--;const rows=prepare(raw,K);const ans=solve(rows,K,false);assert(ans.sat===sat,"scale");scaling.push({owners:h,blocks:raw.length,incidenceFeedback:raw.length-h+1,sat,flow:ans.flow??null,cut:ans.cut??null});}
  }
  return {seed:"0x5f062026",counts,cases,scaling};
}
console.log(JSON.stringify(experiment(), null, 2));

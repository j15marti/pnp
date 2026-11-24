function BS04(input){
  "use strict";
  input=input??null;
  const A=(v,m)=>{if(!v)throw Error(m||"assertion");};
  const C={closureScans:0,rowTests:0,deletions:0,basisReductions:0,basisXors:0,components:0,localEdges:0,globalEdges:0,localStates:0,globalStates:0,peakLayer:0,flowCalls:0,flowEdgeVisits:0,flowMatchingCalls:0,countGroups:0,countAlternatives:0,affineCalls:0,wheelChecks:0,verifiedRows:0,referenceLeaves:0};
  let seed=204110; const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n);};
  const xor=xs=>xs.reduce((a,b)=>a^b,0n), zero=n=>Array(n).fill(0n), add=(a,b)=>a.map((x,i)=>x+b[i]), sub=(a,b)=>a.map((x,i)=>x-b[i]), fits=(a,b)=>a.every((x,i)=>x<=b[i]), same=(a,b)=>a.every((x,i)=>x===b[i]), min=(a,b)=>a<b?a:b;
  const high=x=>x.toString(2).length-1;
  function basis(){
    const piv=new Map(),orig=[];
    function red(v){C.basisReductions++;let mask=0n;while(v){const p=high(v),z=piv.get(p);if(!z)break;v^=z.v;mask^=z.mask;C.basisXors++;}return {v,mask};}
    function put(v,owner){const z=red(v);if(!z.v)return;const i=orig.length;orig.push({v,owner});piv.set(high(z.v),{v:z.v,mask:z.mask^(1n<<BigInt(i))});}
    return {orig,red,put};
  }
  function eachBit(m,fn){while(m){const b=m&-m;fn(high(b));m^=b;}}
  const row=(t,g,c,id)=>({t:BigInt(t),g:BigInt(g),c:c.map(BigInt),id});
  function verified(F,K,b,h,w){if(w===null)return false;A(w.length===F.length,"witness length");let c=zero(K.length),t=0n,g=0n;for(let i=0;i<F.length;i++){const r=F[i].find(r=>r.id===w[i]);A(r,"row missing");c=add(c,r.c);t^=r.t;g^=r.g;C.verifiedRows++;}A(fits(c,K)&&t===b&&g===h,"invalid witness");return true;}
  function closure(F,K,b,h,q){
    F=F.map(f=>f.slice());if(K.some(x=>x<0n))return null;
    const packed=r=>h===null?r.t:(r.t<<BigInt(q))|r.g, target=h===null?b:(b<<BigInt(q))|h;
    while(true){
      C.closureScans++;if(F.some(f=>!f.length))return null;
      const minima=F.map(f=>K.map((_,j)=>f.reduce((v,r)=>min(v,r.c[j]),f[0].c[j])));
      const total=minima.reduce(add,zero(K.length));if(!fits(total,K))return null;
      let changed=false;
      outer:for(let i=0;i<F.length;i++){
        const B=basis();let anchor=0n;
        for(let j=0;j<F.length;j++)if(j!==i){const a=packed(F[j][0]);anchor^=a;for(const r of F[j])B.put(packed(r)^a,j);}
        for(let k=0;k<F[i].length;k++){
          C.rowTests++;const r=F[i][k];
          if(!fits(add(sub(total,minima[i]),r.c),K)||B.red(target^anchor^packed(r)).v){F[i].splice(k,1);C.deletions++;changed=true;break outer;}
        }
      }
      if(!changed)return F;
    }
  }
  function normalize(F,K,b,h){
    let cap=K.slice(),bt=b,gh=h??0n;
    const G=F.map(f=>{const a=f[0],m=K.map((_,j)=>f.reduce((v,r)=>min(v,r.c[j]),a.c[j]));cap=sub(cap,m);bt^=a.t;gh^=a.g;return f.map(r=>({...r,t:r.t^a.t,g:r.g^a.g,c:sub(r.c,m)}));});
    return {G,cap,bt,gh};
  }
  function partition(G,cap,bt,pub){
    const p=G.map((_,i)=>i);const root=i=>p[i]===i?i:(p[i]=root(p[i]));const join=(i,j)=>{i=root(i);j=root(j);if(i!==j)p[j]=i;};
    const B=basis();G.forEach((f,i)=>f.forEach(r=>B.put(r.t,i)));
    G.forEach((f,i)=>f.forEach(r=>{const z=B.red(r.t);A(!z.v);eachBit(z.mask,j=>join(i,B.orig[j].owner));}));
    for(let o=0;o<cap.length;o++)if(!pub.has(o)){let first=-1;G.forEach((f,i)=>{if(f.some(r=>r.c[o]!==0n)){if(first<0)first=i;else join(first,i);}});}
    const z=B.red(bt);if(z.v)return null;
    const groups=new Map();G.forEach((_,i)=>{const k=root(i);if(!groups.has(k))groups.set(k,{ids:[],t:0n});groups.get(k).ids.push(i);});
    eachBit(z.mask,j=>{const a=B.orig[j];groups.get(root(a.owner)).t^=a.v;});
    C.components+=groups.size;
    return [...groups.values()].sort((a,b)=>a.ids[0]-b.ids[0]);
  }
  function flow(F,cap){
    // Exact capacitated bipartite matching via slots. Only constant tag/feature rows,
    // and zero or one normalized owner load, with one positive scale per owner.
    if(F.some(f=>f.some(r=>r.t||r.g)))return undefined;
    const d=zero(cap.length), choices=[];
    for(const f of F){const z=[];for(const r of f){const nz=r.c.map((x,i)=>x?i:-1).filter(i=>i>=0);if(nz.length>1)return undefined;let o=nz[0]??cap.length;if(o<cap.length){if(d[o]&&d[o]!==r.c[o])return undefined;d[o]=r.c[o];}z.push({o,id:r.id});}choices.push(z);}
    C.flowCalls++;const slots=[],byOwner=Array.from({length:cap.length+1},()=>[]);
    for(let o=0;o<=cap.length;o++){const u=o===cap.length?F.length:d[o]?Number(min(BigInt(F.length),cap[o]/d[o])):0;for(let j=0;j<u;j++){byOwner[o].push(slots.length);slots.push(-1);}}
    if(byOwner.every((s,o)=>o===cap.length||s.length<=1))C.flowMatchingCalls++;
    const selected=Array(F.length);
    function aug(i,seen){for(const ch of choices[i])for(const s of byOwner[ch.o]){C.flowEdgeVisits++;if(seen.has(s))continue;seen.add(s);if(slots[s]===-1||aug(slots[s],seen)){slots[s]=i;selected[i]=ch.id;return true;}}return false;}
    for(let i=0;i<F.length;i++)if(!aug(i,new Set()))return null;
    return selected;
  }
  function affine(F,target,cap){
    if(F.some(f=>f.some(r=>r.g||r.c.some(x=>x))))return undefined;
    const B=basis();const local=[];
    for(let i=0;i<F.length;i++){const f=F[i],S=new Map(f.map(r=>[r.t.toString(),r.id]));const Q=basis();f.forEach(r=>Q.put(r.t,i));if(BigInt(S.size)!==(1n<<BigInt(Q.orig.length)))return undefined;local.push(S);for(const z of Q.orig)B.put(z.v,i);}
    C.affineCalls++;const z=B.red(target);if(z.v)return null;const tags=F.map(()=>0n);eachBit(z.mask,j=>{const a=B.orig[j];tags[a.owner]^=a.v;});return tags.map((t,i)=>{const id=local[i].get(t.toString());A(id!==undefined,"affine lift");return id;});
  }
  const key=(t,g,c)=>`${t}/${g}/${c.join(",")}`;
  function alternatives(F,ids){
    const G=new Map(), singles=[];
    for(let j=0;j<F.length;j++){const f=F[j];if(f.length!==2){singles.push(f.map(r=>({...r,w:[[ids[j],r.id]]})));continue;}
      const [a,b]=f,k=key(a.t^b.t,a.g^b.g,sub(b.c,a.c));if(!G.has(k))G.set(k,[]);G.get(k).push({a,b,i:ids[j]});
    }
    for(const gs of G.values()){
      C.countGroups++;const al=[];
      for(let k=0;k<=gs.length;k++){let t=0n,g=0n,c=zero(gs[0].a.c.length),w=[];gs.forEach((z,j)=>{const r=j<k?z.b:z.a;t^=r.t;g^=r.g;c=add(c,r.c);w.push([z.i,r.id]);});al.push({t,g,c,w});C.countAlternatives++;}
      singles.push(al);
    }return singles;
  }
  function profiles(G,group,cap,pub){
    const F=group.ids.map(i=>G[i]), target=group.t, onlyPrivate=F.every(f=>f.every(r=>[...pub].every(j=>r.c[j]===0n)));
    let w;
    if(onlyPrivate){w=affine(F,target,cap);if(w===undefined&&target===0n)w=flow(F,cap);}
    if(w!==undefined)return w===null?[]:[{g:0n,c:zero(cap.length),w:w.map((id,i)=>[group.ids[i],id])}];
    const al=alternatives(F,group.ids);
    // Suffix affine feasibility, using actual count alternatives as generators.
    const suffix=al.map((_,i)=>{const B=basis();let a=0n;for(let j=i+1;j<al.length;j++){a^=al[j][0].t;for(const r of al[j])B.put(r.t^al[j][0].t,j);}return {B,a};});
    let D=new Map([["0",{t:0n,g:0n,c:zero(cap.length),w:[]}]]);
    for(let i=0;i<al.length;i++){const E=new Map(),{B,a}=suffix[i];for(const p of D.values())for(const r of al[i]){C.localEdges++;const t=p.t^r.t,g=p.g^r.g,c=add(p.c,r.c);if(!fits(c,cap)||B.red(target^t^a).v)continue;const k=key(t,g,c);if(!E.has(k)){E.set(k,{t,g,c,w:p.w.concat(r.w)});C.localStates++;}}D=E;C.peakLayer=Math.max(C.peakLayer,D.size);}
    const out=new Map();for(const p of D.values())if(p.t===target){const c=p.c.map((x,j)=>pub.has(j)?x:0n),k=key(0n,p.g,c);if(!out.has(k))out.set(k,{g:p.g,c,w:p.w});}
    return [...out.values()];
  }
  function solve(F,K,b=0n,h=0n,q=0,publicOwners=[]){
    const P=closure(F,K,b,h,q);if(P===null)return h===null?{}:null;
    const {G,cap,bt,gh}=normalize(P,K,b,h),pub=new Set(publicOwners);
    const groups=partition(G,cap,bt,pub);if(groups===null)return h===null?{}:null;
    let D=new Map([["0",{g:0n,c:zero(cap.length),w:[]}]]);
    for(const group of groups){const ps=profiles(G,group,cap,pub),E=new Map();for(const x of D.values())for(const y of ps){C.globalEdges++;const g=x.g^y.g,c=add(x.c,y.c);if(!fits(c,cap))continue;const k=key(0n,g,c);if(!E.has(k)){E.set(k,{g,c,w:x.w.concat(y.w)});C.globalStates++;}}D=E;C.peakLayer=Math.max(C.peakLayer,D.size);if(!D.size)return h===null?{}:null;}
    if(h===null){const out={};for(const z of D.values()){const actual=z.g^gh,k=actual.toString();if(Object.hasOwn(out,k))continue;const w=Array(F.length);for(const [i,id] of z.w)w[i]=id;verified(F,K,b,actual,w);out[k]=w;}return out;}const hit=[...D.values()].find(z=>z.g===gh);if(!hit)return null;const w=Array(F.length);for(const [i,id] of hit.w)w[i]=id;verified(F,K,b,h,w);return w;
  }
  function brute(F,K,b,h){let w=[];function rec(i,c,t,g){if(!fits(c,K))return null;if(i===F.length){C.referenceLeaves++;return t===b&&g===h?w.slice():null;}for(const r of F[i]){w.push(r.id);const z=rec(i+1,add(c,r.c),t^r.t,g^r.g);w.pop();if(z!==null)return z;}return null;}return rec(0,zero(K.length),0n,0n);}
  function cnf(n,clauses,cap){const K=clauses.map((c,i)=>BigInt(cap?cap[i]:c.length-1));const F=Array.from({length:n},(_,i)=>[0,1].map(x=>row(0,0,clauses.map(c=>c.filter(l=>Math.abs(l)===i+1&&((l>0?x:1-x)===0)).length),x)));return {F,K};}
  function graphRows(n,edges){const K=edges.flatMap(()=>[1n,1n,1n,1n]);const F=Array.from({length:n},(_,i)=>[0,1,2,3].map(x=>row(0,0,edges.flatMap(([u,v,s])=>[0,1,2,3].map(a=>Number(i===u&&x===a)+Number(i===v&&x===(a^s)))),x)));return {F,K};}
  const edgeKey=([u,v,s])=>`${Math.min(u,v)},${Math.max(u,v)},${s}`;
  function shard(n,edges){
    let next=n;const es=[],gadgets=[];
    for(const [u,v,s] of edges){const ends=[];for(const h of [u,v]){const b=next++,rim=[next++,next++,next++],a=(h+b)%4;gadgets.push({h,b,rim,a});ends.push(b);for(let i=0;i<3;i++){es.push([h,rim[i],0],[b,rim[i],a],[rim[i],rim[(i+1)%3],0]);}}es.push([ends[0],ends[1],s^gadgets[gadgets.length-2].a^gadgets[gadgets.length-1].a]);}return {n:next,es,gadgets};
  }
  function project(n,es,gs){
    const keys=new Map();for(const e of es){const k=edgeKey(e);keys.set(k,(keys.get(k)||0)+1);}
    const privateR=new Set(gs.flatMap(g=>g.rim)),ports=new Map(gs.map(g=>[g.b,g]));A(privateR.size===3*gs.length&&ports.size===gs.length,"manifest overlap");
    const remove=new Set();
    for(const g of gs){const {h,b,rim,a}=g;A(h!==b&&!privateR.has(h)&&!privateR.has(b)&&!ports.has(h),"nonprivate hub");for(let i=0;i<3;i++)for(const e of [[h,rim[i],0],[b,rim[i],a],[rim[i],rim[(i+1)%3],0]]){C.wheelChecks++;const k=edgeKey(e);A(keys.get(k)===1&&!remove.has(k),"manifest edge");remove.add(k);}}
    const kept=[];for(const e of es){const [u,v,s]=e;if(remove.has(edgeKey(e)))continue;A(!privateR.has(u)&&!privateR.has(v),"private rim external incidence");const a=ports.get(u),b=ports.get(v),x=a?a.h:u,y=b?b.h:v,z=s^(a?a.a:0)^(b?b.a:0);A(x!==y,"unsupported self-edge");kept.push([x,y,z]);}
    const roots=Array.from({length:n},(_,i)=>i).filter(i=>!privateR.has(i)&&!ports.has(i));const ix=new Map(roots.map((x,i)=>[x,i]));const out=kept.map(([u,v,s])=>[ix.get(u),ix.get(v),s]);
    return {roots,edges:out,lift(w){const x=Array(n);roots.forEach((r,i)=>x[r]=w[i]);for(const {h,b,rim,a} of gs){x[b]=x[h]^a;const colors=[0,1,2,3].filter(c=>c!==x[h]);rim.forEach((r,i)=>x[r]=colors[i]);}for(const [u,v,s] of es){C.wheelChecks++;A((x[u]^x[v])!==s,"wheel lift");}return x;}};
  }
  // User-facing JSON input. All numeric costs/tags may be decimal strings.
  if(input!==null){
    const q=input.q??0; A(Number.isSafeInteger(q)&&q>=0,"q");
    let F,K; if(input.cnf!==undefined){
      const {n,clauses}=input.cnf; A(Number.isSafeInteger(n)&&n>=0&&Array.isArray(clauses),"CNF");
      A(clauses.every(c=>Array.isArray(c)&&c.length<=3&&c.every(l=>Number.isSafeInteger(l)&&l!==0&&Math.abs(l)<=n)),"CNF literals");
      ({F,K}=cnf(n,clauses));
    }else{
      K=input.K.map(BigInt);
      F=input.factors.map(f=>f.map((r,i)=>row(r.t??0,r.g??0,r.c??zero(K.length),i)));
    }
    A(F.every(f=>f.every(r=>r.t>=0n&&r.g>=0n&&r.g<(1n<<BigInt(q))&&r.c.length===K.length&&r.c.every(c=>c>=0n))),"row schema");
    const b=BigInt(input.b??0),h=input.allGuards?null:BigInt(input.h??0),pub=input.publicOwners??[];
    A(b>=0n&&(h===null||(h>=0n&&h<(1n<<BigInt(q))))&&pub.every(o=>Number.isSafeInteger(o)&&o>=0&&o<K.length),"target schema");
    const result=solve(F,K,b,h,q,pub);return {result,counters:C};
  }
  let random={sat:0,unsat:0,allGuardComparisons:0};for(let z=0;z<240;z++){const n=1+rnd(6),m=rnd(4),q=2,K=Array.from({length:m},()=>BigInt(rnd(8))),F=Array.from({length:n},()=>Array.from({length:1+rnd(4)},(_,i)=>row(rnd(8),rnd(4),Array.from({length:m},()=>rnd(3)),i))),b0=BigInt(rnd(8)),h0=BigInt(rnd(4)),pub=Array.from({length:m},(_,i)=>i).filter(()=>rnd(2));let b=b0,h=h0;if(z%2===0){let c=zero(m);b=0n;h=0n;for(const f of F){const r=f[rnd(f.length)];b^=r.t;h^=r.g;c=add(c,r.c);}for(let j=0;j<m;j++)K[j]=c[j]+BigInt(rnd(3));}const a=solve(F,K,b,h,q,pub),r=brute(F,K,b,h);A((a!==null)===(r!==null),"random mismatch "+z);random[a===null?"unsat":"sat"]++;if(z<80){const all=solve(F,K,b,null,q,pub);for(let g=0;g<4;g++){const truth=brute(F,K,b,BigInt(g));A(Object.hasOwn(all,String(g))===(truth!==null),"all guards mismatch");random.allGuardComparisons++;}}}
  // Every subformula of the complete 3-cube.
  const cube=Array.from({length:8},(_,w)=>[1,2,3].map((i,j)=>w>>j&1?i:-i));let cubeCounts={sat:0,unsat:0};
  for(let mask=0;mask<256;mask++){const cls=cube.filter((_,i)=>mask>>i&1),{F,K}=cnf(3,cls),w=solve(F,K),r=brute(F,K,0n,0n);A((w!==null)===(r!==null),"cube");const direct=Array.from({length:8},(_,x)=>x).some(x=>cls.every(c=>c.some(l=>Boolean(x>>(Math.abs(l)-1)&1)===(l>0))));A((w!==null)===direct,"direct source cube");cubeCounts[w===null?"unsat":"sat"]++;}
  const lines=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]],fano=lines.flatMap(c=>[c,c.map(x=>-x)]),fanoResults=[];
  for(let r=-1;r<14;r++){const cap=fano.map((_,i)=>i===r?3:2),{F,K}=cnf(7,fano,cap),w=solve(F,K),ref=brute(F,K,0n,0n);A((w!==null)===(r>=0)&&(w!==null)===(ref!==null),"fano");let models=0;for(let s=0;s<128;s++)if(fano.every((c,i)=>c.filter(l=>((s>>(Math.abs(l)-1))&1)!==Number(l<0)).length>=3-cap[i]))models++;A(models===(r<0?0:5),"fano count");fanoResults.push({relaxed:r,models,sat:w!==null});}
  // Exact shifted-wheel projection for every offset and ordered boundary pair.
  for(let a=0;a<4;a++)for(let h=0;h<4;h++)for(let b=0;b<4;b++){let count=0;for(let s=0;s<64;s++){const v=[s&3,s>>2&3,s>>4&3];if(new Set(v).size===3&&v.every(x=>x!==h&&x!==(b^a)))count++;}A(count===((h^b)===a?6:0),"wheel truth");C.wheelChecks++;}
  const k5=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)k5.push([i,j,0]);const graph=[];
  for(let r=-1;r<10;r++){const es=k5.filter((_,i)=>i!==r),s=shard(5,es),p=project(s.n,s.es,s.gadgets),{F,K}=graphRows(p.roots.length,p.edges),w=solve(F,K),ref=brute(F,K,0n,0n);A((w!==null)===(r>=0)&&(w!==null)===(ref!==null),"K5");if(w)p.lift(w);graph.push({deleted:r,expandedVertices:s.n,expandedEdges:s.es.length,sat:w!==null});}
  // Dense change of basis defeats coordinate-only decomposition; q-bit guard
  // is an arbitrary row observation, not included in component discovery.
  const scales=[];
  for(const k of [2,4,8,16,32,64]){
    const v=j=>((1n<<BigInt(j+1))-1n); // invertible triangular dense basis
    const F=[];let target=0n;
    for(let copy=0;copy<2;copy++)for(let j=0;j<k;j++){const a=v(2*j),b=v(2*j+1);F.push([0,1,2,3].map(x=>row((x&1?a:0n)^(x&2?b:0n),x===0?1:0,[],x)));if(copy===0)target^=a;}
    const before={...C};const all=solve(F,[],target,null,1);A(Object.hasOwn(all,"0")&&Object.hasOwn(all,"1"),"guard reset SAT");const hostile=solve(F,[],0n,null,1);A(Object.hasOwn(hostile,"0")&&!Object.hasOwn(hostile,"1"),"guard reset UNSAT target zero");
    scales.push({pairs:k,ambientBaseRank:2*k,oldGuardedCutAffineCapacity:(1n<<BigInt(2*k+1)).toString(),componentCountTwoAllGuardRuns:C.components-before.components,localEdges:C.localEdges-before.localEdges,globalEdges:C.globalEdges-before.globalEdges});
  }
  // Flow / matching / affine / shared owner guard and count controls.
  const terminal=[];
  for(const n of [8,24,48]){const F=Array.from({length:n},(_,i)=>[0,1].map((j)=>row(0,0,[Number(j===0),Number(j===1)],j)));for(const K of [[BigInt(n/2),BigInt(n/2)],[BigInt(n/2-1),BigInt(n/2)]]){const w=solve(F,K);A((w!==null)===(K[0]+K[1]>=BigInt(n)),"flow");terminal.push({kind:"capacitated flow",n,sat:w!==null});}}
  const match=Array.from({length:5},(_,i)=>[i,(i+1)%5].map((o,j)=>row(0,0,Array.from({length:5},(_,k)=>Number(k===o)),j)));A(solve(match,Array(5).fill(1n))!==null,"matching");A(solve(match,[0n,1n,1n,1n,1n])===null,"matching unsat");
  const affineF=Array.from({length:20},(_,i)=>[0,1].map(j=>row(j?1n<<BigInt(i):0n,0,[],j)));A(solve(affineF,[],(1n<<20n)-1n)!==null,"affine");
  // No private owner: exact public count and parity convolution; count grouping
  // in one private owner component retains both budgets and nonlinear feature.
  const countF=Array.from({length:24},()=>[row(0,0,[0,2],0),row(0,1,[2,0],1)]);
  A(solve(countF,[24n,24n],0n,0n,1)!==null,"count SAT");
  A(solve(countF,[24n,24n],0n,1n,1)===null,"count UNSAT");
  for(const h of [0n,1n])A((solve(countF,[24n,24n],0n,h,1,[0,1])!==null)===(h===0n),"public count guard");
  return {seed:204110,random,cubeCounts,fanoResults,graph,scales,terminal,counters:C,assertionFailures:0,limitations:"Finite controls, not general BS03 blossom, no strict E4/B4 source compiler, no full integrated closure; peakLayer is maximum individual map size, not peak memory."};
}
if(typeof module!=="undefined")module.exports=BS04;
if(typeof require!=="undefined"&&require.main===module){const fs=require("fs");const arg=process.argv[2];console.log(JSON.stringify(BS04(arg?JSON.parse(fs.readFileSync(arg,"utf8")):null),null,2));}

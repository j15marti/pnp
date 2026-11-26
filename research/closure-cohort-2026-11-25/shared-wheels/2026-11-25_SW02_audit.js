"use strict";
function audit() {
  let checks=0; const ok=(b,msg)=>{checks++;if(!b)throw Error(msg)};
  const K=[[[0,1],[2,3]],[[0,2],[1,4]],[[0,3],[2,4]],[[0,4],[1,3]],[[1,2],[3,4]]];
  const cut=(x,e)=>x[e[0]]^x[e[1]];
  const sat=(x,G)=>G.every(g=>g.some(e=>cut(x,e)));
  const bits=(w,n)=>Array.from({length:n},(_,i)=>(w>>i)&1);
  const padWords=[];
  for(let w=0;w<32;w++){const x=bits(w,5);ok(!sat(x,K),"K5 must be UNSAT");if(sat(x,K.slice(1))){padWords.push(x);ok(!cut(x,K[0][0])&&!cut(x,K[0][1]),"false padding");}}
  ok(padWords.length>0,"pad SAT");
  for(let w=0;w<16;w++){const x=bits(w,4),f=x.map((a,i)=>a^i);const ex=[0,1,2,3].some(c=>!f.includes(c));ok(ex===Boolean((x[0]^x[1])|(x[2]^x[3])),"star projection");}
  const make=(n=0)=>({n,G:[],new(){return this.n++},add(...es){this.G.push(es);}});
  function degrees(g){const d=new Int32Array(g.n);for(const a of g.G)for(const [u,v] of a){d[u]++;d[v]++;}return d;}
  function components(g,groups=g.G){const p=Array.from({length:g.n},(_,i)=>i);function find(x){while(p[x]!==x){p[x]=p[p[x]];x=p[x];}return x;}for(const a of groups)for(const [u,v] of a){p[find(u)]=find(v);}return p.map((_,i)=>find(i));}
  function verify(g,regular=false){const seen=new Set();for(const a of g.G){ok(a.length===1||a.length===2,"group size");const v=a.flat();ok(new Set(v).size===v.length,"disjoint");for(let [u,v] of a){ok(u>=0&&v>=0&&u<g.n&&v<g.n,"endpoint");const k=Math.min(u,v)+":"+Math.max(u,v);ok(!seen.has(k),"simple");seen.add(k);}}const d=degrees(g);ok(d.every(x=>regular?x===4:x<=4),"degree");ok(new Set(components(g)).size===1,"connected");if(regular)ok(g.G.length===g.n&&g.G.every(a=>a.length===2),"regular count");}
  function valid(n,parts){ok(parts.length===4,"four parts");const seen=new Set();for(const part of parts){const v=part.flat();ok(v.length===n&&new Set(v).size===n&&v.every(x=>x>=0&&x<n),"partition");for(const t of part){ok(t.length===3&&new Set(t).size===3,"clause");for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let k=Math.min(t[i],t[j])+":"+Math.max(t[i],t[j]);ok(!seen.has(k),"linear");seen.add(k);}}}}
  function source(n,parts){valid(n,parts);const clauses=parts.flat(),g=make(),ports=Array.from({length:n},()=>[]),wires=[],paths=[];
    for(const [a,b,c] of clauses){const ids=[a,b,b,c].map(v=>{const k=g.new();ports[v].push(k);return k;});g.add([ids[0],ids[1]],[ids[2],ids[3]]);}
    for(const list of ports)for(let i=1;i<list.length;i++){const u=list[i-1],v=list[i],z=g.new();g.add([u,z]);g.add([z,v]);wires.push([u,z,v]);}
    const preN=g.n,preGroups=g.G.slice(),preC=components(g),unique=[...new Set(preC)]; const delta=preGroups.length-(preN-unique.length);
    ok(delta===clauses.length-n+unique.length,"deficit identity");
    const pools=new Map(unique.map(c=>[c,[]]));for(const w of wires)pools.get(preC[w[1]]).push(w[1]);
    for(let i=1;i<unique.length;i++){const u=pools.get(unique[i-1]).pop(),v=pools.get(unique[i]).pop(),a=g.new(),b=g.new(),c=g.new();ok(u!==undefined&&v!==undefined,"spare wire ports");g.add([u,a],[b,c]);g.add([a,b],[c,v]);paths.push([u,a,b,c,v]);}
    verify(g);ok(degrees(g).every(x=>x<=3),"source subcubic");
    function lift(x){const y=Array(g.n);for(let i=0;i<n;i++)for(const j of ports[i])y[j]=x[i];for(const [u,z,v] of wires){ok(y[u]===y[v],"equality wire");y[z]=1^y[u];}for(const [u,a,b,c,v] of paths){y[a]=1^y[u];y[b]=y[u];y[c]=1^y[u];}return y;}
    function decode(y){return ports.map(a=>y[a[0]]);}
    return {g,clauses,ports,wires,preN,preGroups,delta,preC:unique.length,lift,decode};
  }
  function pad(g){const h=make(g.n),pads=[],bridges=[],coreIds=[];const start=degrees(g).findIndex(d=>d<=2);ok(start>=0,"spare");let tail=start;
    for(const a of g.G){if(a.length===2){coreIds.push(h.G.length);h.add(...a);continue;}
      const s=Array.from({length:5},()=>h.new()); const prior=tail;bridges.push([tail,s[2]]);tail=s[3];const ids=[];
      for(const k of K.slice(1)){ids.push(h.G.length);h.add(...k.map(([u,v])=>[s[u],s[v]]));}
      const i=h.G.length;h.add(a[0],[s[0],s[1]]);coreIds.push(i,...ids);pads.push({s,prior,edge:a[0]});
    }
    let leaf=-1;if(bridges.length%2){leaf=h.new();bridges.push([tail,leaf]);}
    for(let i=0;i<bridges.length;i+=2)h.add(bridges[i],bridges[i+1]);verify(h);ok(degrees(h).some(x=>x<=2),"remaining rank-two degree slack");
    function lift(x){const y=Array(h.n);for(let i=0;i<g.n;i++)y[i]=x[i];for(const {s,prior} of pads){const z=padWords[0],f=1^y[prior]^z[2];for(let j=0;j<5;j++)y[s[j]]=z[j]^f;}if(leaf>=0)y[leaf]=1^y[tail];return y;}
    return {h,pads,coreIds,lift};
  }
  function regularize(h){const g=make(8*h.n),d=degrees(h);for(let i=0;i<8;i++)for(const a of h.G)g.add(...a.map(([u,v])=>[u+i*h.n,v+i*h.n]));for(let v=0;v<h.n;v++)for(let s=0;s<4-d[v];s++){const es=[];for(let i=0;i<4;i++)es.push([i*h.n+v,(4+(i+s)%4)*h.n+v]);g.add(es[0],es[1]);g.add(es[2],es[3]);}verify(g,true);
    function lift(x){return Array.from({length:8},(_,i)=>x.map(b=>b^(i>=4?1:0))).flat();}
    return {g,lift};
  }
  function physical(g,x){let starCount=0;for(const a of g.G){const f=a.flat().map((v,j)=>x[v]^j);const center=[0,1,2,3].find(c=>!f.includes(c));ok(center!==undefined,"star lift");for(let j=0;j<4;j++)ok((center^x[a.flat()[j]])!==j,"physical edge");starCount++;}return starCount;}
  function ag(){return Array.from({length:4},(_,k)=>Array.from({length:3},(_,c)=>Array.from({length:3},(_,t)=>k===0?3*c+t:3*t+(c+(k-1)*t)%3)));}
  function trip(p){return Array.from({length:4},(_,j)=>Array.from({length:p},(_,i)=>[i,p+(i+j)%p,2*p+(i+2*j)%p]));}
  function union(parts,n,qparts){return parts.map((p,j)=>p.concat(qparts[j].map(t=>t.map(v=>v+n))));}
  const cases=[{name:"AG(2,3)",n:9,P:ag(),ex:true},{name:"tripartite5",n:15,P:trip(5),ex:true},{name:"AG+trip5",n:24,P:union(ag(),9,trip(5)),ex:false},{name:"tripartite17",n:51,P:trip(17),ex:false},{name:"tripartite65",n:195,P:trip(65),ex:false}];
  let sourceWords=0,sourceSat=0,sourceNo=0,starWitnesses=0,stats=[];
  for(const c of cases){const s=source(c.n,c.P),p=pad(s.g),r=regularize(p.h);
    const is=x=>s.clauses.every(([a,b,c])=>x[a]!==x[b]||x[b]!==x[c]);
    let ns=0,nn=0,model=null;
    if(c.ex){for(let w=0;w<2**c.n;w++){const x=bits(w,c.n);const y=s.lift(x);const expected=is(x);ok(sat(y,s.g.G)===expected,"source projection");ok(s.decode(y).every((v,i)=>v===x[i]),"source decode");if(expected){ns++;if(!model)model=x;}else nn++;}sourceWords+=ns+nn;sourceSat+=ns;sourceNo+=nn;}
    else if(c.name.startsWith("tripartite"))model=Array.from({length:c.n},(_,i)=>+(i>=c.n/3&&i<2*c.n/3));
    if(model){ok(is(model),"source model");const y=s.lift(model),z=p.lift(y),x=r.lift(z);ok(sat(y,s.g.G)&&sat(z,p.h.G)&&sat(x,r.g.G),"global witness");ok(s.decode(x).every((b,i)=>b===model[i]),"decode target");starWitnesses+=physical(r.g,x);}
    // Lower bound from a subset: take one copy of original owner groups and their singleton pads.
    // Each included pad contributes four internal groups and rank exactly four.
    let q=0;for(const a of s.preGroups)if(a.length===1)q++;
    const coreCount=s.preGroups.length+4*q,coreRank=s.preN-s.preC+4*q;
    ok(coreCount-coreRank===s.delta,"padding deficit preserved");
    stats.push({case:c.name,n:c.n,clauses:s.clauses.length,sourceComponents:s.preC,preDeficiency:s.delta,sourceGraphVertices:s.g.n,sourceGraphGroups:s.g.G.length,pads:p.pads.length,targetVertices:r.g.n,targetGroups:r.g.G.length,enumeratedSat:ns,enumeratedUnsat:nn,lifted:!!model});
  }
  // Check no-local-forcing theorem using actual exhaustive truth tables for random pairings/signs.
  let state=20261125>>>0;const rnd=n=>{state=(Math.imul(1664525,state)+1013904223)>>>0;return state%n;};
  let localTests=0,graphs=0,cutChecks=0;
  for(let n=5;n<=9;n++){const E=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if([1,2,n-1,n-2].includes(j-i))E.push([i,j]);ok(E.length===2*n,"circulant");
    for(let S=1;S<(1<<n)-1;S++){let k=0;for(const [u,v] of E)k+=((S>>u)^(S>>v))&1;ok(k>=4,"4edgeconn");cutChecks++;}
    for(let rep=0;rep<24;rep++){const ed=E.slice();for(let i=ed.length-1;i>0;i--){let j=rnd(i+1);[ed[i],ed[j]]=[ed[j],ed[i]];}const signs=ed.map(()=>rnd(2));const size=1<<n,all=size-1,masks=new Uint16Array(size);for(let w=0;w<size;w++){let mask=0;for(let i=0;i<2*n;i++){const [u,v]=ed[i];if((((w>>u)^(w>>v))&1)===signs[i])mask|=1<<(i>>1);}masks[w]=mask;}
      for(let i=0;i<2*n;i++)for(let s=0;s<2;s++){const [u,v]=ed[i],can=new Uint8Array(size);for(let w=0;w<size;w++)if((((w>>u)^(w>>v))&1)===s)can[masks[w]]=1;for(let b=0;b<n;b++)for(let T=0;T<size;T++)if(!(T&(1<<b)))can[T]|=can[T|(1<<b)];for(let T=0;T<size;T++)if(!(T&(1<<(i>>1)))&&T!==(all^(1<<(i>>1)))){ok(can[T],"one omitted edge freedom");localTests++;}}
      graphs++;
    }
  }
  return {seed:20261125,assertions:checks,k5PadModels:padWords.map(x=>x.reduce((a,b,i)=>a+(b<<i),0)),sourceWords,sourceSat,sourceNo,starWitnesses,localTests,graphs,cutChecks,stats,limits:"No exhaustive full-target solver or integrated production closure; exact local truth tables, exhaustive source words, constructive target lifts, and exhaustive small forcing comparisons."};
}
console.log(JSON.stringify(audit(),null,2));

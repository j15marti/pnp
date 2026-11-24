"use strict";
const run = () => {
  let seed=20261124; const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n};
  const eq=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
  const assert=(x,m)=>{if(!x)throw Error(m)};
  const xor=(a,b)=>new Set([...a].flatMap(x=>[...b].map(y=>x^y)));
  const span=ws=>ws.reduce((s,w)=>xor(s,new Set([0,w])),new Set([0]));
  // Certificate discovery by exhaustive translation testing (small controls ONLY).
  function compress(S){
    if(!S.size)return null;
    const a=[...S][0],W=[...S].map(x=>x^a).filter(w=>[...S].every(x=>S.has(x^w)));
    let b=[],H=new Set([0]);for(const w of W)if(!H.has(w)){b.push(w);H=xor(H,new Set([0,w]))}
    const todo=new Set(S),R=[];while(todo.size){const r=[...todo][0];R.push(r);for(const w of H)todo.delete(r^w)}
    return {R,b};
  }
  // DAG with distinct vertices for all alternatives; split into bipartite PM.
  function graph(fs){
    let n=2, arcs=[];const add=()=>n++, edge=(u,v,g)=>arcs.push([u,v,g]);
    for(const f of fs){if(!f||!f.R.length)continue;let u=add();for(const r of f.R){let a=add();edge(0,a,r);edge(a,u,0)}
      for(const w of f.b){let v=add(),a=add();edge(u,v,0);edge(u,a,w);edge(a,v,0);u=v}edge(u,1,0)}
    const E=[...arcs,[1,0,0]];for(let i=2;i<n;i++)E.push([i,i,0]);
    return {n,E,arcs};
  }
  function supportPM(G){
    let S=new Set(),count=0;const L=Array.from({length:G.n},()=>[]);
    for(const [u,v,g] of G.E)L[u].push([v,g]);
    // forced minimum remaining choices; backtracking enumerates actual matchings.
    function rec(U,V,s){if(!U.length){S.add(s);count++;return}
      let best=-1,A=null;for(const u of U){let a=L[u].filter(([v])=>!V.has(v));if(A===null||a.length<A.length){best=u;A=a}if(!a.length)return}
      const rest=U.filter(u=>u!==best);for(const [v,g] of A){V.add(v);rec(rest,V,s^g);V.delete(v)}}
    rec(Array.from({length:G.n},(_,i)=>i),new Set(),0);return {S,count};
  }
  function local(n,edges){
    const S=Array.from({length:4},()=>new Set()),L=Array.from({length:n},()=>[]);
    for(const [u,v,g] of edges){L[u].push([v,g]);L[v].push([u,g])}
    let count=0;
    function rec(mask,o,s){if(!mask){S[o&3].add(o|(s<<4));count++;return}
      let u=0;while(!(mask&(1<<u)))u++;const rem=mask^(1<<u);
      if(u<4)rec(rem,o,s);
      for(const [v,g] of L[u])if(rem&(1<<v))rec(rem^(1<<v),o|(u<4?1<<u:0)|(v<4?1<<v:0),s^g)}
    rec((1<<n)-1,0,0);return {S,count};
  }
  const out={seed:20261124,physical:{graphs:0,local_matchings:0,fibers:0,empty_fibers:0,replacement_matchings:0,targets:0,sat:0,unsat:0,strict_compressions:0},sat_compiler:{instances:0,assignments:0,sat:0,unsat:0,local_clause_graphs:0},scaling:[]};
  for(let i=0;i<120;i++){
    const n=6+2*rnd(2),E=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(rnd(100)<45)E.push([u,v,rnd(16)]);
    const {S,count}=local(n,E),fs=S.map(compress),G=graph(fs),a=supportPM(G),full=new Set(S.flatMap(s=>[...s]));
    assert(eq(a.S,full),"physical support");
    out.physical.graphs++;out.physical.local_matchings+=count;out.physical.replacement_matchings+=a.count;
    for(let h=0;h<4;h++){out.physical.fibers++;if(!fs[h])out.physical.empty_fibers++;else if(fs[h].R.length<S[h].size)out.physical.strict_compressions++}
    // Independent second region sharing occupancy labels; target all four shared vertices occupied.
    const E2=[];for(let u=0;u<6;u++)for(let v=u+1;v<6;v++)if(rnd(100)<45)E2.push([u,v,rnd(16)]);
    const ext=new Set(local(6,E2).S.flatMap(s=>[...s]));
    const direct=xor(full,ext),compressed=xor(a.S,ext);
    for(let t=0;t<16;t++){let z=15|(t<<4),v=direct.has(z);assert(v===compressed.has(z),"global target");out.physical.targets++;out.physical[v?"sat":"unsat"]++}
  }
  // 3-CNF clause module: guard j chooses a true literal, free other two bits.
  function clause(c){
    const fs=c.map((lit,j)=>({R:[lit.sign?1<<j:0],b:[0,1,2].filter(k=>k!==j).map(k=>1<<k)}));
    const p=supportPM(graph(fs)).S;out.sat_compiler.local_clause_graphs++;
    for(let x=0;x<8;x++)assert(p.has(x)===c.some((lit,j)=>Boolean(x&(1<<j))===lit.sign),"clause graph");
    return p;
  }
  function test(n,cs){
    const supports=cs.map(clause);let sat=false;
    for(let x=0;x<(1<<n);x++){
      let truth=cs.every(c=>c.some(l=>Boolean(x&(1<<l.v))===l.sign));
      let z=cs.every((c,i)=>supports[i].has(c.reduce((a,l,j)=>a|(((x>>l.v)&1)<<j),0)));
      assert(z===truth,"pointwise compiler");sat||=z;out.sat_compiler.assignments++;
    }
    out.sat_compiler.instances++;out.sat_compiler[sat?"sat":"unsat"]++;return sat;
  }
  for(let i=0;i<100;i++){
    let cs=[],n=4+rnd(3);for(let j=0,m=4+rnd(13);j<m;j++){let c=[],used=new Set();while(c.length<3){let v=rnd(n);if(!used.has(v)){used.add(v);c.push({v,sign:!!rnd(2)})}}cs.push(c)}test(n,cs)
  }
  const cube=Array.from({length:8},(_,i)=>[0,1,2].map(v=>({v,sign:!!(i&(1<<v))})));
  assert(!test(3,cube),"cube UNSAT");for(let j=0;j<8;j++)assert(test(3,cube.filter((_,i)=>i!==j)),"deletion SAT");
  // Bounded explicit rank for numeric tags; graph size counts analytic high-rank family.
  // Four branches, one representative each, r independent basis choices each.
  for(let r of [4,8,16,32,64,128]){const G=graph(Array.from({length:4},(_,h)=>({R:[h],b:Array(r).fill(0)})));
    out.scaling.push({rank:r,vertices:2*G.n,edges:G.E.length,analytic_support_per_guard:"2^"+r,structural_count_only:true})}
  return out;
};
console.log(JSON.stringify(run(),null,2));

"use strict";
function experiment(){
  const stats={queries:0,sourceWords:0,closureSweeps:0,closureSupportTests:0,closureDeletions:0,transitionAttempts:0,peakStates:0,assertions:0};
  const assert=(b,m)=>{stats.assertions++;if(!b)throw Error(m)};
  const parity=x=>{let z=0;while(x){z^=1;x&=x-1}return z};
  const enabled=(e,x)=>e.g.every(([a,b])=>parity(a&x)===b);
  const edge=(u,v,g=[])=>({u,v,g});
  function compile(n,E){
    const R=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j));
    for(const {u,v} of E)R[u][v]=true;
    for(let k=0;k<n;k++)for(let i=0;i<n;i++)for(let j=0;j<n;j++)R[i][j] ||= R[i][k]&&R[k][j];
    const C=R.map((r,i)=>r.findIndex((v,j)=>v&&R[j][i]));
    // DFS heads of back edges form a feedback vertex set, even for loops.
    const color=Array(n).fill(0),F=new Set(),adj=Array.from({length:n},()=>[]);
    for(const {u,v} of E)if(C[u]===C[v])adj[u].push(v);
    function dfs(u){color[u]=1;for(const v of adj[u]){if(!color[v])dfs(v);else if(color[v]===1)F.add(v)}color[u]=2}
    for(let u=0;u<n;u++)if(!color[u])dfs(u);
    const k=C.map(c=>[...F].filter(v=>C[v]===c).length);
    // Verify zero-weight subgraph acyclic (Kahn, including parallel edges).
    const Z=Array(n).fill(0),A=Array.from({length:n},()=>[]);
    for(const {u,v} of E)if(C[u]===C[v]&&!F.has(v)){A[u].push(v);Z[v]++}
    const q=Z.map((z,i)=>z===0?i:-1).filter(i=>i>=0);
    for(let i=0;i<q.length;i++)for(const v of A[q[i]])if(--Z[v]===0)q.push(v);
    assert(q.length===n,"bad feedback set");
    return {n,E,C,F,k};
  }
  function reference(P,x){
    const seen=new Set([0]),Q=[0];
    for(let i=0;i<Q.length;i++)for(const e of P.E)if(e.u===Q[i]&&enabled(e,x)&&!seen.has(e.v)){seen.add(e.v);Q.push(e.v)}
    return !seen.has(P.n-1);
  }
  function evaluate(P,x,old=false){
    stats.queries++;const {n,E,C,F,k}=P, inf=-1;
    const D=Array.from({length:n},(_,v)=>v===0?[[0,0]]:v===n-1?[[inf,0]]:[[inf,0],...Array.from({length:(old?0:k[v])+1},(_,d)=>[[d,0],[d,1]]).flat()]);
    const edges=E.filter(e=>enabled(e,x));
    function ok(e,a,b){
      if(a[0]===inf)return true;
      if(b[0]===inf)return false;
      const cap=old?a[0]:C[e.u]!==C[e.v]?0:a[0]+Number(F.has(e.v));
      if(b[0]>cap)return false;
      return !(b[1]&&b[0]===cap);
    }
    // Certified structural support closure, restart after every strict deletion.
    // Conditional on exact source word x; no signed cancellation used for deletion.
    for(;;){stats.closureSweeps++;let changed=false;
      outer:for(const e of edges)for(const u of new Set([e.u,e.v])){
        const v=u===e.u?e.v:e.u;
        for(let i=0;i<D[u].length;i++){
          const a=D[u][i];let support=false;
          for(const b of u===v?[a]:D[v]){stats.closureSupportTests++;if(u===e.u?ok(e,a,b):ok(e,b,a)){support=true;break}}
          if(!support){D[u].splice(i,1);stats.closureDeletions++;changed=true;if(!D[u].length)return 0n;break outer}
        }
      }
      if(!changed)break;
    }
    // Ordered frontier contraction, exact signed sum; scopes use the static graph.
    let frontier=[],states=new Map([["",1n]]);
    for(let v=0;v<n;v++){
      const next=Array.from({length:v+1},(_,i)=>i).filter(i=>E.some(e=>(e.u===i&&e.v>v)||(e.v===i&&e.u>v)));
      const check=edges.filter(e=>Math.max(e.u,e.v)===v), out=new Map();
      for(const [key,w] of states){
        const a=key===""?[]:key.split(",").map(Number);
        for(let j=0;j<D[v].length;j++){
          stats.transitionAttempts++;
          const lookup=u=>u===v?D[v][j]:D[u][a[frontier.indexOf(u)]];
          if(!check.every(e=>ok(e,lookup(e.u),lookup(e.v))))continue;
          const nk=next.map(u=>u===v?j:a[frontier.indexOf(u)]).join(",");
          out.set(nk,(out.get(nk)??0n)+(D[v][j][1]?-w:w));
        }
      }
      for(const [key,w] of out)if(w===0n)out.delete(key);
      frontier=next;states=out;stats.peakStates=Math.max(stats.peakStates,states.size);
    }
    return states.get("")??0n;
  }
  const E0=[edge(1,2),edge(2,1)],P0=compile(4,E0);
  assert(evaluate(P0,0,true)===2n,"old failure");
  assert(evaluate(P0,0)===1n,"new isolated cycle");
  let exhaustive={graphs:0,sat:0,unsat:0};
  const pairs=[];for(let u=0;u<4;u++)for(let v=0;v<4;v++)if(u!==v)pairs.push(edge(u,v));
  for(let mask=0;mask<4096;mask++){const P=compile(4,pairs.filter((_,i)=>(mask>>i)&1));const b=reference(P,0);assert(evaluate(P,0)===BigInt(b),"exhaustive");exhaustive.graphs++;exhaustive[b?"sat":"unsat"]++}
  let seed=0x201012;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed};
  let random={graphs:0,sat:0,unsat:0,guardedCounts:0};
  for(let j=0;j<120;j++){
    const n=4+(rand()%3),E=[];for(let i=0;i<12;i++){const u=(rand()>>>8)%n,v=(rand()>>>8)%n;const a=1+((rand()>>>8)%7),b=(rand()>>>10)&1;E.push(edge(u,v,i%4?[[a,b]]:[]))}
    const P=compile(n,E);let sum=0n,ref=0;
    // Explicit affine source guard: parity x0 xor x1 = j mod 2.
    for(let x=0;x<8;x++)if(parity(x&3)===(j&1)){stats.sourceWords++;const b=reference(P,x),z=evaluate(P,x);assert(z===BigInt(b),"random");sum+=z;ref+=Number(b);random[b?"sat":"unsat"]++}
    assert(sum===BigInt(ref),"guarded count");random.graphs++;random.guardedCounts++;
  }
  // Common Fano owner controls: one rejection edge per monochromatic event.
  // All rejection edges go s->a; a->t always; a,b have a cycle.
  const lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
  const events=lines.flatMap(L=>[0,1].map(b=>edge(0,1,L.map(v=>[1<<v,b]))));
  const fano=[];
  for(let drop=-1;drop<events.length;drop++){
    const P=compile(4,[...events.filter((_,i)=>i!==drop),edge(1,2),edge(2,1),edge(1,3)]);
    let count=0,first=null;
    for(let x=0;x<128;x++){stats.sourceWords++;const b=reference(P,x),z=evaluate(P,x);assert(z===BigInt(b),"Fano");count+=Number(z);if(z&&first===null)first=x}
    assert(count===(drop<0?0:5),"Fano known count");if(first!==null)assert(reference(P,first),"Fano witness");fano.push({drop,count,first});
  }
  // 2-cycles in a chain: SCC-local reset keeps every k_C=1.
  const scaling=[];
  for(const k of [4,16,64,128]){
    const n=2*k+2,E=[];
    for(let i=0;i<k;i++){let a=1+2*i,b=a+1;E.push(edge(a,b),edge(b,a));if(i)E.push(edge(a-1,a))}
    E.push(edge(0,1),edge(n-2,n-1,[[1,1]]));
    const P=compile(n,E),before=stats.transitionAttempts;
    const sat=evaluate(P,0),unsat=evaluate(P,1);assert(sat===1n&&unsat===0n,"scale");
    scaling.push({cycles:k,feedback:P.F.size,maxLocalFeedback:Math.max(...P.k),attempts:stats.transitionAttempts-before,sat:Number(sat),unsat:Number(unsat)});
  }
  return {seed:"0x201012",exhaustive,random,fano,scaling,stats,oldIsolatedCycle:2,newIsolatedCycle:1};
}
console.log(JSON.stringify(experiment(),null,2));

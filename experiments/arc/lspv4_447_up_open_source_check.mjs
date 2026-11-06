#!/usr/bin/env node
// LSPV-4/447 standalone independent original-source UP-open branch referee.
// Node 18+, no packages, no external oracle, no pre-generated input required.
// Enumerates every branch (k<=2 or 3) for four charges and five cubic graphs.
const requireTest=(b,msg)=>{checks++;if(!b)throw Error(msg)};
let checks=0;
function graph(name){
  let n=0,edges=[];
  if(name==="K4"){n=4;for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edges.push([a,b]);}
  if(name==="Cube"){n=8;for(let a=0;a<8;a++)for(let b=a+1;b<8;b++)if([1,2,4].includes(a^b))edges.push([a,b]);}
  if(name==="Petersen"){n=10;for(let a=0;a<5;a++)edges.push([a,(a+1)%5],[5+a,5+(a+2)%5],[a,5+a]);}
  if(name==="Heawood"){n=14;for(let a=0;a<7;a++)for(let delta of [0,1,3])edges.push([a,7+(a+delta)%7]);}
  if(name==="BridgeCubic"){n=10;for(let b of [0,5])for(let a=0;a<4;a++)for(let c=a+1;c<4;c++){
    if(a===0&&c===1)edges.push([b,b+4],[b+4,b+1]);else edges.push([b+a,b+c]);}
    edges.push([4,9]);}
  if(n===0)throw Error("unknown graph");
  edges=edges.map(([a,b])=>a<b?[a,b]:[b,a]).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
  const inc=Array.from({length:n},()=>[]);
  edges.forEach(([a,b],j)=>{inc[a].push(j);inc[b].push(j)});
  requireTest(inc.every(x=>x.length===3),"not cubic");
  return {n,edges,inc};
}
function formula(G,charges){
  const clauses=[];
  for(let v=0;v<G.n;v++){
    const inc=G.inc[v].slice().sort((a,b)=>a-b);
    for(let pattern=0;pattern<8;pattern++){
      const b=[(pattern>>2)&1,(pattern>>1)&1,pattern&1];
      if((b[0]^b[1]^b[2])!==charges[v])
        clauses.push(inc.map((e,j)=>b[j]===0?e+1:-(e+1)));
    }
  }
  return clauses;
}
function up(clauses,selected){
  let env=new Map(selected),forced=0;
  for(;;){
    let changed=false;
    for(const clause of clauses){
      let unknown=[],hit=false;
      for(const lit of clause){
        const id=Math.abs(lit)-1;
        if(!env.has(id))unknown.push(lit);
        else if(env.get(id)===(lit>0?1:0)){hit=true;break;}
      }
      if(hit)continue;
      if(unknown.length===0)return {open:false,forced};
      if(unknown.length===1){
        const lit=unknown[0],id=Math.abs(lit)-1,val=lit>0?1:0;
        if(!env.has(id)){env.set(id,val);forced++;changed=true;}
        else requireTest(env.get(id)===val,"inconsistent implication");
      }
    }
    if(!changed)return {open:true,forced};
  }
}
function components(G,selected){
  const omit=new Set(selected),adj=Array.from({length:G.n},()=>[]);
  G.edges.forEach(([a,b],j)=>{if(!omit.has(j)){adj[a].push(b);adj[b].push(a)}});
  const seen=new Set(),res=[];
  for(let v=0;v<G.n;v++)if(!seen.has(v)){
    let nodes=[v];seen.add(v);
    for(let i=0;i<nodes.length;i++)for(let w of adj[nodes[i]])if(!seen.has(w)){seen.add(w);nodes.push(w);}
    let remain=nodes.reduce((acc,x)=>acc+adj[x].length,0)/2;
    res.push({nodes,tree:remain===nodes.length-1});
  }
  return res;
}
function gf2Rank(rows,n){
  let a=rows.slice(),rank=0;
  for(let j=0;j<n;j++){
    let pivot=rank;
    while(pivot<a.length&&!((a[pivot]>>BigInt(j))&1n))pivot++;
    if(pivot===a.length)continue;
    [a[rank],a[pivot]]=[a[pivot],a[rank]];
    for(let i=0;i<a.length;i++)if(i!==rank&&((a[i]>>BigInt(j))&1n))a[i]^=a[rank];
    rank++;
  }
  return rank;
}
function choose(n,k,emit,p=[],start=0){
  if(p.length===k){emit(p);return;}
  for(let j=start;j<=n-(k-p.length);j++)choose(n,k,emit,[...p,j],j+1);
}
let grand={cases:0,open:0,closed:0,forced:0,semantic:0},perGraph=[];
for(const [name,maxk] of [["K4",2],["Cube",3],["Petersen",3],["Heawood",2],["BridgeCubic",3]]){
  const G=graph(name);
  let stats={graph:name,cases:0,open:0,closed:0,forced:0,semantic:0};
  for(let phase=0;phase<4;phase++){
    const charge=Array(G.n).fill(0);
    for(let v=0;v<phase;v++)charge[v]=1;
    const F=formula(G,charge);
    requireTest(F.length===4*G.n,"original source clause count");
    // Exact semantic check of each original 3-clause bundle.
    for(let v=0;v<G.n;v++)for(let q=0;q<8;q++){
      const ids=G.inc[v].slice().sort((a,b)=>a-b);
      const bit=ids.map((_,j)=>(q>>(2-j))&1);
      let truth=F.slice(4*v,4*v+4).every(cl=>cl.some(l=>{
        let i=ids.indexOf(Math.abs(l)-1);return bit[i]===(l>0?1:0);
      }));
      requireTest(truth===((bit[0]^bit[1]^bit[2])===charge[v]),"source sign");
      stats.semantic++;
    }
    // A corrupted original source clause must not authenticate.
    let bad=F.map(x=>x.slice());bad[0][0]=-bad[0][0];
    let poisonDetected=false;
    for(let q=0;q<8;q++){
      const ids=G.inc[0].slice().sort((a,b)=>a-b);
      const bits=ids.map((_,i)=>(q>>(2-i))&1);
      let truth=bad.slice(0,4).every(cl=>cl.some(l=>bits[ids.indexOf(Math.abs(l)-1)]===(l>0?1:0)));
      if(truth!==((bits[0]^bits[1]^bits[2])===charge[0]))poisonDetected=true;
    }
    requireTest(poisonDetected,"corrupt source accepted");
    for(let k=0;k<=maxk;k++)choose(G.edges.length,k,S=>{
      const cs=components(G,S),trees=cs.filter(x=>x.tree);
      requireTest(cs.some(x=>!x.tree),"no cyclic component");
      requireTest(3*trees.length<=2*k,"incidence bound");
      const rows=trees.map(C=>{
        const V=new Set(C.nodes);let word=0n;
        for(let j=0;j<S.length;j++){
          let [a,b]=G.edges[S[j]];
          if(V.has(a)!==V.has(b))word|=1n<<BigInt(j);
        }
        return word;
      });
      requireTest(gf2Rank(rows,k)===trees.length,"tree constraints rank");
      let openForSubset=0;
      for(let m=0;m<(1<<k);m++){
        const selected=S.map((edge,j)=>[edge,(m>>j)&1]);
        const result=up(F,selected);
        let predicted=trees.every(C=>{
          const vertices=new Set(C.nodes);
          let rhs=C.nodes.reduce((a,v)=>a^charge[v],0);
          for(const [eid,bit] of selected){
            let [a,b]=G.edges[eid];
            if(vertices.has(a)!==vertices.has(b))rhs^=bit;
          }
          return rhs===0;
        });
        requireTest(result.open===predicted,"UP vs tree equations");
        requireTest(result.forced<=2*k,"forced edges > 2k");
        stats.cases++;stats.forced+=result.forced;
        if(result.open){stats.open++;openForSubset++;}else stats.closed++;
      }
      requireTest(openForSubset===2**(k-trees.length),"wrong exact rank count");
      requireTest(openForSubset>=2**Math.ceil(k/3),"wrong open floor");
    });
  }
  perGraph.push(stats);
  for(let prop of Object.keys(grand))grand[prop]+=stats[prop];
}
requireTest(grand.cases===44748&&grand.open===44300&&grand.closed===448,"producer mismatch");
console.log(JSON.stringify({status:"PASS",assertions:checks,totals:grand,perGraph},null,2));

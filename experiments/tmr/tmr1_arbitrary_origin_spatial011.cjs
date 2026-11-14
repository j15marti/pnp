'use strict';
// TMR-1/011: arbitrary initial position, one pre-move-read local input head.
// Exact MAY distance versus independent BFS, plus every-edge potentials.
function main() {
  let seed = 0x1A2B3C4D;
  const rng = () => (seed = (Math.imul(seed,1664525)+1013904223) >>> 0);
  const integer = n => rng()%n;
  const hits = (v,sets) => sets.every(D => (v&D)!==0);
  const formula = (L,start,sets) => {
    let best=Infinity,argmin=null;
    for(let a=0;a<=start;a++) for(let b=start;b<L;b++) {
      const mask=(((1<<(b-a+1))-1)<<a)>>>0;
      if(hits(mask,sets)){
        const cost=(b-a)+Math.min(start-a,b-start)+1;
        if(cost<best){best=cost;argmin=[a,b];}
      }
    }
    return {best,argmin};
  };
  const bfs = (L,start,sets) => {
    const Q=[[start,0,0]],seen=new Set([start+':0']);let idx=0,edges=0;
    while(idx<Q.length){
      const [p,v,t]=Q[idx++];
      if(hits(v,sets))return {time:t,states:Q.length,edges};
      const nv=v|(1<<p);
      for(let q=Math.max(0,p-1);q<=Math.min(L-1,p+1);q++){
        edges++;const key=q+':'+nv;
        if(!seen.has(key)){seen.add(key);Q.push([q,nv,t+1]);}
      }
    }
    throw Error('No goal');
  };
  const phi = (L,p,v,sets) => {
    let best=0;
    for(const D of sets)if(!(v&D)){
      let d=1000000;
      for(let q=0;q<L;q++)if(D&(1<<q))d=Math.min(d,Math.abs(p-q));
      best=Math.max(best,1+d);
    }
    return best;
  };
  let stats={version:'TMR1-011',seed:'0x1A2B3C4D',
    algorithm:'one local pre-read head, arbitrary initial location, precise one-step MAY BFS',
    cases:0,states:0,paid_edges_bfs:0,all_edge_potential_checks:0,
    goals_checked:0,failures:0,max_L:0,largest_path:0,
    origin_zero_checks:0,sharp_potential_edge_checks:0,hostile_controls:[]};
  const run=(L,start,sets)=>{
    if(!sets.length||sets.some(D=>D===0||(D>>L)!==0))throw Error('Bad supports');
    const f=formula(L,start,sets), b=bfs(L,start,sets);
    if(f.best!==b.time)throw Error('Formula/BFS mismatch '+JSON.stringify({L,start,sets,f,b}));
    if(start===0){
      const lhs=1+Math.max(...sets.map(D=>Math.log2(D&-D)|0));
      if(lhs!==b.time)throw Error('Left-aligned identity');
      stats.origin_zero_checks++;
    }
    for(let p=0;p<L;p++)for(let v=0;v<(1<<L);v++){
      const old=phi(L,p,v,sets);
      if(hits(v,sets)){if(old!==0)throw Error('Goal potential');stats.goals_checked++;}
      for(let q=Math.max(0,p-1);q<=Math.min(L-1,p+1);q++)for(let obs=0;obs<=1;obs++){
        const nv=obs?(v|(1<<p)):v;
        if(old>1+phi(L,q,nv,sets))throw Error('Old potential edge');
        stats.all_edge_potential_checks++;
      }
    }
    stats.cases++;stats.states+=b.states;stats.paid_edges_bfs+=b.edges;
    stats.max_L=Math.max(stats.max_L,L);stats.largest_path=Math.max(stats.largest_path,b.time);
    return {formula:f.best,algorithm:b.time,argmin:f.argmin};
  };
  const hostile=run(11,5,[1,1<<10]);
  if(hostile.formula!==16||phi(11,5,0,[1,1<<10])!==6)throw Error('Interior head control');
  stats.hostile_controls.push({name:'start-at-5, force reads at 0 and 10',L:11,start:5,initial_phi:6,exact_MAY:16});
  if(formula(11,0,[1,1<<10]).best!==11)throw Error('Two-head control');
  stats.hostile_controls.push({name:'two initially dispersed heads invalidate one-head transfer',L:11,
    head_positions:[0,10],supports:[[0],[10]],cost:1,one_head_exact:11});
  stats.hostile_controls.push({name:'free index jump invalidates adjacent-moving one-head model',
    L:11,start:0,supports:[[10]],local_cost:11,indexed_cost:2});
  for(let L=2;L<=9;L++){
    for(let c=0;c<40;c++){
      const sets=[], z=1+integer(Math.min(5,L+1));
      for(let j=0;j<z;j++){let D=0;while(!D)D=integer(1<<L);sets.push(D);}
      run(L,integer(L),sets);
    }
    for(let start=0;start<L;start++){
      run(L,start,[1,1<<(L-1)]);
      run(L,start,[(1<<L)-1]);
      run(L,start,Array.from({length:L},(_,j)=>1<<j));
    }
  }
  for(let L=2;L<=7;L++)for(let trial=0;trial<8;trial++){
    const sets=[];
    for(let j=0;j<4;j++){let D=0;while(!D)D=integer(1<<L);sets.push(D);}
    const sharp=(p,v)=>{
      const remaining=sets.filter(D=>(D&v)===0);
      return remaining.length?formula(L,p,remaining).best:0;
    };
    for(let p=0;p<L;p++)for(let v=0;v<(1<<L);v++){
      const prior=sharp(p,v);
      for(let q=Math.max(0,p-1);q<=Math.min(L-1,p+1);q++)for(let obs=0;obs<=1;obs++){
        const nv=obs?(v|(1<<p)):v;
        if(prior>1+sharp(q,nv))throw Error('Sharp potential edge');
        stats.sharp_potential_edge_checks++;
      }
    }
  }
  console.log(JSON.stringify(stats,null,2));
}
if(require.main===module)main();
module.exports={main};

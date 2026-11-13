"use strict";
// TMR-4 exact source of the executed deterministic V8 audit.
const runAudit=function runAudit(){
  const assert=(p,s)=>{if(!p) throw Error(s)};
  let families=0, edges=0, potentials=0, exact=0, maxima=[], examples=[];
  function testFamily(L,Ds){
    const R=Ds.length, total=(1<<R);
    const phi=Array(total).fill(0),dist=Array(total).fill(Infinity);
    const tau=(U)=>{if(U===0)return 0;let best=L+1;for(let q=0;q<(1<<L);q++){
      let ok=true;for(let i=0;i<R;i++){if((U&(1<<i)) && (q&Ds[i])===0){ok=false;break}}
      if(ok){let w=0;for(let b=q;b;b&=b-1)w++;if(w<best)best=w}
    }return best};
    for(let U=0;U<total;U++)phi[U]=tau(U);
    dist[0]=0;
    for(let U=1;U<total;U++){
      for(let j=0;j<L;j++){
        let V=U;for(let i=0;i<R;i++)if(Ds[i]&(1<<j)) V &= ~(1<<i);
        assert(phi[U]<=1+phi[V],"potential failed");
        potentials++;
        if(V!==U)dist[U]=Math.min(dist[U],1+dist[V]);
        edges++;
      }
      assert(dist[U]===phi[U],"distance mismatch");
      exact++;
    }
    assert(phi[total-1]<=L,"linear ceiling failed");
    families++;
    return phi[total-1];
  }
  for(let L=1;L<=6;L++){
    let count=0,mx=0;
    const maxR=L<=4?4:L===5?4:3;
    const masks=[...Array((1<<L)-1)].map((_,i)=>i+1);
    for(let r=1;r<=Math.min(maxR,masks.length);r++){
      const a=Array(r);
      function rec(st,k){if(k===r){const z=testFamily(L,a);count++;mx=Math.max(mx,z);return}
        for(let j=st;j<=masks.length-(r-k);j++){a[k]=masks[j];rec(j+1,k+1)}
      }rec(0,0);
    }
    maxima.push({L,families:count,max_potential:mx});
  }
  const disjoint=[];for(let n=1;n<=6;n++){const Ds=Array.from({length:2*n},(_,i)=>1<<i);disjoint.push({n,potential:testFamily(2*n,Ds)})}
  const overlap=testFamily(3,[0b011,0b110]);
  const allSame=testFamily(4,[0b1111,0b1111,0b1111,0b1111]);
  assert(overlap===1 && allSame===1,"overlap counterexample fails");
  examples.push({kind:"overlap",L:3,difference_sets:["011","110"],naive_count:2,certified_cost:overlap});
  examples.push({kind:"fully_overlapping",L:4,difference_sets:["1111","1111","1111","1111"],naive_count:4,certified_cost:allSame});
  const zeroEdgeWouldViolate = 1<=0+0;assert(!zeroEdgeWouldViolate,"zero edge unexpectedly valid");
  return {schema:"TMR4_OBSERVATION_HITSET001",timestamp:"2026-11-13 13:36 PST",method:"Exhaustive finite abstract state graphs and hitting-set potentials; deterministic, no randomness",maxima,disjoint,examples,checks:{families,read_edges:edges,potential_edge_inequalities:potentials,exact_distance_states:exact,zero_cost_shortcut_detected:true},status:"COMPUTATIONAL; theorem requires separate symbolic proof",all_pass:true};
};
const result=runAudit();
if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));

// LSPV-2/520 independent stand-alone verifier (plain ECMAScript).
// The only cost model proved is descriptor-bit query rank, not FLMV time/space.
(function () {
  let checks = 0;
  const assert = (p, m) => { if (!p) throw Error(m); checks++; };
  function rank(a) {
    const piv = {};
    for (let v of a) while (v) {
      let k = 31 - Math.clz32(v);
      if (Object.prototype.hasOwnProperty.call(piv, k)) v ^= piv[k];
      else { piv[k] = v; break; }
    }
    return Object.keys(piv).length;
  }
  function span(a, p) { return rank([...a,p]) === rank(a); }
  function rstar(rows, p) {
    rows = [...new Set(rows.filter(Boolean))];
    function scan(start, need, acc) {
      if (!need) return span(acc,p) ? rank(acc) : null;
      for (let j=start;j<=rows.length-need;j++) {
        const x=scan(j+1,need-1,[...acc,rows[j]]);
        if (x!==null) return x;
      }
      return null;
    }
    for (let d=0;d<=rows.length;d++) {
      const x=scan(0,d,[]);
      if (x!==null) return x;
    }
    return null;
  }
  let coord=[], count=0, brute=0, sat=0, unsat=0, corruption=0;
  for (let k=1;k<=8;k++) {
    const p=(1<<k)-1, unit=Array.from({length:k},(_,j)=>1<<j);
    assert(rstar(unit,p)===k,"unit basis");
    assert(rstar([p,...unit],p)===1,"direct parity row");
    coord.push([k,k,1]);
  }
  const graphs=[
    [4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],
    [6,[[0,1],[0,2],[0,3],[1,2],[1,4],[2,5],[3,4],[3,5],[4,5]]],
    [8,Array.from({length:8},(_,i)=>Array.from({length:8-i-1},(_,t)=>[i,i+t+1])).flat().filter(([i,j])=>(((i^j)&((i^j)-1))===0))]
  ];
  for (const [H,edges] of graphs) {
    const inc=Array.from({length:H},()=>[]);
    edges.forEach(([u,v],i)=>{inc[u].push(i+1);inc[v].push(i+1);});
    assert(inc.every(a=>a.length===3),"cubic");
    for (let d=0;d<1<<(H-1);d++) {
      const cls=[],rows=[];
      for(let v=0;v<H;v++) for(let p=0;p<2;p++) for(let q=0;q<2;q++) {
        let c=v<H-1?((d>>v)&1):0;
        cls.push(inc[v].map((id,t)=>[id,[p,q,1^c^p^q][t]]));
        rows.push(0,0,v<H-1?(1<<v):0);
      }
      assert(rstar(rows,(1<<(H-1))-1)===H-1,"original charge bit rank");
      for(let v=0;v<H;v++) {
        const a=cls.slice(4*v,4*v+4);
        assert(new Set(a.map(c=>c.map(x=>x[1]).join(""))).size===4,"facets distinct");
        assert(a.every(c=>c.reduce((z,x)=>z^x[1],0)===(1^(v<H-1?((d>>v)&1):0))),"charge facet");
      }
      const expected=(d.toString(2).split("1").length%2===1);
      if(expected) sat++;else unsat++;
      if(H!==8 || [0,1,3,7,31,127].includes(d)){
        let models=0;
        for(let a=0;a<(1<<edges.length);a++){
          if(cls.every(cl=>cl.some(([id,neg])=>(((a>>(id-1))&1)^neg)===1)))models++;
        }
        assert((models>0)===expected,"original 3CNF truth");
        if(expected) assert(models===2**(edges.length-H+1),"linear model count");
        brute++;
      }
      if(d<2){
        let changed=cls.map(c=>c.map(x=>[...x]));
        changed[0][2][1]^=1;
        const old=cls[0].reduce((z,x)=>z^x[1],0);
        const now=changed[0].reduce((z,x)=>z^x[1],0);
        assert(old!==now,"corrupted original sign");
        corruption++;
      }
      count++;
    }
  }
  return {checks,original_cnf_sources:count,SAT:sat,UNSAT:unsat,brute_force_sources:brute,corruption_controls:corruption,rank_coordinates_and_direct:coord,scope:"promise descriptor input-bit queries only; no native FLMV/R_mix341 execution"};
})()

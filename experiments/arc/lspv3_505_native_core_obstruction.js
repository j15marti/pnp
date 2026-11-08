// LSPV-3/505: finite SOURCE/AND3/XOR exact-support factor closure.
// DISTINCT R_core505 only; not a historical R_mix341 checker.
// Run: node lspv3_505_native_core_obstruction.js > raw.json
console.log(JSON.stringify((function experiment505(){
  const graphDefs=[
    ["K4",4,Array.from({length:4},(_,i)=>Array.from({length:4-i-1},(_,j)=>[i,i+j+1])).flat()],
    ["K33",6,Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>[i,j+3])).flat()],
    ["cube",8,Array.from({length:8},(_,i)=>[1,2,4].filter(b=>i<(i^b)).map(b=>[i,i^b])).flat()]
  ];
  let checks=0;
  function check(v,msg){checks++;if(!v)throw Error(msg);}
  function base(V,edges,odd){
    const inc=Array.from({length:V},()=>[]);
    edges.forEach(([u,v],idx)=>{inc[u].push(idx+1);inc[v].push(idx+1);});
    check(inc.every(a=>a.length===3),"cubic");
    const cs=[];
    for(let v=0;v<V;v++){const s=inc[v].slice().sort((a,b)=>a-b),charge=(odd&&v===0)?1:0;
      for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++)
        if((a^b^c)!==charge)cs.push(s.map((x,j)=>[a,b,c][j]?-x:x));
    }
    return cs;
  }
  function expand(cs,S){
    let n=Math.max(...cs.flat().map(Math.abs)),out=[];
    cs.forEach((C,j)=>{
      if(!S.has(j)){out.push(C.slice());return;}
      const [a,b,c]=C,u=++n,v=++n;
      out.push([a,b,u],[-u,c,v],[-u,c,-v]);
    });
    return {cs:out,n};
  }
  function factor(C){
    const s=[...new Set(C.map(Math.abs))].sort((a,b)=>a-b),map=new Map(s.map((x,i)=>[x,i]));
    let table=0;
    for(let a=0;a<(1<<s.length);a++){
      const ok=C.some(l=>(((a>>map.get(Math.abs(l)))&1)===(l>0?1:0)));
      if(ok)table|=1<<a;
    }
    return {s,table};
  }
  function key(f){return f.s.join(",")+"|"+f.table;}
  function at(f,assign){
    let z=0; f.s.forEach((x,i)=>{z|=assign.get(x)<<i;});
    return (f.table>>z)&1;
  }
  function merge(a,b){
    const s=[...new Set([...a.s,...b.s])].sort((x,y)=>x-y);
    if(s.length>3)return null;
    let table=0;
    for(let bits=0;bits<(1<<s.length);bits++){
      const assign=new Map(s.map((x,i)=>[x,(bits>>i)&1]));
      if(at(a,assign)&&at(b,assign))table|=1<<bits;
    }
    return {s,table};
  }
  function equations(f){
    const eq=[];
    for(let local=1;local<(1<<f.s.length);local++){
      let mask=0n;f.s.forEach((v,i)=>{if((local>>i)&1)mask|=(1n<<BigInt(v-1));});
      for(const rhs of [0,1]){
        let table=0;
        for(let x=0;x<(1<<f.s.length);x++){
          let p=0;for(let k=0;k<f.s.length;k++)if((local>>k)&1)p^=(x>>k)&1;
          if(p===rhs)table|=(1<<x);
        }
        if(table===f.table)eq.push({mask,rhs});
      }
    }
    return eq;
  }
  function inconsistent(eq){
    const basis=new Map();
    for(const e of eq){
      let m=e.mask,r=e.rhs;
      while(m!==0n){
        const high=m.toString(2).length-1;
        if(!basis.has(high)){basis.set(high,[m,r]);break;}
        const [bm,br]=basis.get(high);m^=bm;r^=br;
      }
      if(m===0n&&r)return true;
    }
    return false;
  }
  function closure(cs){
    const facts=new Map(cs.map(C=>{const f=factor(C);return [key(f),f];}));
    let rounds=0;
    for(;;){
      rounds++; const vals=[...facts.values()],adds=[];
      for(let i=0;i<vals.length;i++)for(let j=i;j<vals.length;j++){
        const f=merge(vals[i],vals[j]);if(f&&!facts.has(key(f)))adds.push(f);
      }
      if(!adds.length)break;
      for(const f of adds)facts.set(key(f),f);
      check(rounds<20,"closure termination");
    }
    const eq=new Map();
    for(const f of facts.values())for(const e of equations(f))eq.set(e.mask.toString()+"/"+e.rhs,e);
    return {factors:facts.size,affine_seeds:eq.size,false_factor:[...facts.values()].some(f=>f.table===0),
            xor_contradiction:inconsistent([...eq.values()]),rounds};
  }
  function satCount(cs,n){
    if(n>12)return null;
    let count=0;
    for(let a=0;a<(1<<n);a++){
      if(cs.every(C=>C.some(l=>(((a>>(Math.abs(l)-1))&1)===(l>0?1:0)))))count++;
    }
    return count;
  }
  const out=[];
  for(const [name,V,edges] of graphDefs){
    for(const odd of [true,false]){
      const original=base(V,edges,odd);
      check(original.length===4*V,"base m");
      const schemes=[["none",[]],["single_first",[0]],["single_last",[4*V-1]],["two",[0,1]],
                     ["every_other",Array.from({length:2*V},(_,j)=>2*j)],["all",Array.from({length:4*V},(_,j)=>j)]];
      for(const [label,indices] of schemes){
        const {cs,n}=expand(original,new Set(indices)), cl=closure(cs), count=satCount(cs,n);
        check(cs.length===4*V+2*indices.length,"source count");
        check(cs.every(C=>C.length===3 &&new Set(C.map(Math.abs)).size===3),"strict3");
        check(cl.xor_contradiction===(odd&&indices.length===0),"XOR closure claim "+name+" "+label+" "+odd);
        check(!cl.false_factor,"false factor");
        if(count!==null)check((count===0)===odd,"actual SAT label");
        out.push({graph:name,h:V,odd,scenario:label,k:indices.length,variables:n,source_clauses:cs.length,
                  model_count_if_n_le_12:count,...cl});
      }
    }
  }
  check(closure([[1],[-1]]).false_factor,"incompatible units positive detection");
  const specific=expand([[1,2,3]],new Set([0]));
  check(closure(specific.cs).affine_seeds===0,"one gadget has no affine seed");
  // Each source in the one-gadget odd K4 is indispensable, independently checked.
  const K4=base(4,graphDefs[0][2],true),g=expand(K4,new Set([0]));
  check(satCount(g.cs,g.n)===0,"gadget UNSAT");
  for(let j=0;j<g.cs.length;j++)check(satCount(g.cs.filter((_,i)=>i!==j),g.n)>0,"source essential "+j);
  return {claim:"Any nonempty /503 replacement blocks SOURCE/AND3/XOR-only refutation in exact-support R_core505, not full R_mix341",
          family:"strict3 odd Tseitin with /503 replacement",assertion_groups:checks,scenarios:out.length,
          negative_controls:["even-charge SAT","source-deletion SAT witnesses","gadget alone nonaffine","contradictory units positive"],results:out};
})(),null,2));

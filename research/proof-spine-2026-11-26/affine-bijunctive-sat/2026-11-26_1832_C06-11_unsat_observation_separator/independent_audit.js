function run(){
  let checks=0;
  const assert=b=>{checks++;if(!b)throw Error("check "+checks)};
  const atom=Array.from({length:6},(_,i)=>[(i+5)%6,i,(i+1)%6]);
  const parity=[],exact=[];
  for(let w=0;w<64;w++){
    const sums=atom.map(c=>c.reduce((s,i)=>s+((w>>i)&1),0));
    if(sums.every(x=>x%2===1))parity.push(w);
    if(sums.every(x=>x===1))exact.push(w);
  }
  assert(parity.length===4&&exact.length===3);
  for(let w of parity){for(let i=0;i<3;i++)assert(((w>>i)&1)===((w>>(i+3))&1));}
  let out=[];
  for(let s of [4,16,64]){
    let atoms=4, guards=[],edges=[];
    for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)for(let c=0;c<3;c++){
      guards.push([[6*atoms,6*i+c],0],[[6*atoms+1,6*j+c],0]);
      edges.push([i,j,c,atoms++]);
    }
    for(let i=0;i<s;i++)guards.push([[0,6*(atoms+i)],0]);
    const clauses=Array.from({length:atoms+s},(_,k)=>atom.map(c=>c.map(i=>i+6*k))).flat();
    let branch=[0,0], totals=[0,0];
    for(let w=0;w<256;w++){
      const core=Array.from({length:4},(_,i)=>parity.find(p=>(p&3)===((w>>(2*i))&3)));
      const slots=core.slice();
      for(let [i,j,c,k] of edges){
        const a=(core[i]>>c)&1,b=(core[j]>>c)&1;
        slots[k]=parity.find(p=>(p&3)===(a|b<<1));assert(slots[k]!==undefined);
      }
      const bits=slots.flatMap(p=>Array.from({length:6},(_,i)=>(p>>i)&1));
      for(let c of clauses.slice(0,6*atoms))assert(c.reduce((v,i)=>v+bits[i],0)%2===1);
      for(let [g,b] of guards.slice(0,36))assert(g.reduce((v,i)=>v^bits[i],0)===b);
      const shared=bits[0];totals[shared]++;
      const ok=clauses.slice(0,6*atoms).every(c=>c.reduce((v,i)=>v+bits[i],0)===1);
      if(ok)branch[shared]++;
    }
    assert(totals[0]===128&&totals[1]===128&&branch[0]===0&&branch[1]===0);
    for(let b=0;b<2;b++)assert(exact.filter(p=>(p&1)===b).length===(b===0?2:1));
    out.push({spectators:s,variables:clauses.length,dimension:8+s,branch_core_words:totals,branch_core_solutions:branch,clauses,guards});
  }
  return {checks,parity,exact,controls:out};
}
console.log(JSON.stringify(run(),null,2));

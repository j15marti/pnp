// Independent finite audit of signed two-factor phase supports. No solver dependencies.
const assert=require('node:assert/strict');
const L=[0,13,14],U=[1,2,15];
const subs=a=>Array.from({length:(1<<a.length)-1},(_,i)=>a.filter((_,j)=>((i+1)>>j)&1));
const phase=m=>(m>>2)&1, pop=m=>m.toString(2).replaceAll('0','').length;
let nonempty=0,empty=0,both=0,one=0;
for(const R of [...subs(L),...subs(U)])for(const S of [...subs(L),...subs(U)]){
  const W=new Set();for(const a of R)for(const b of S)if(phase(a)!==phase(b))W.add((a&3)|((b&3)<<2));
  if(!W.size){empty++;continue;}nonempty++;const rank=pop([...W][0]);assert([...W].every(x=>pop(x)===rank));
  const live=[...W].reduce((a,b)=>a|b,0),H=[...W].map(m=>m&3?1:0); // incidence-level ground set
  let ok=false;
  // Enumerate bucket labels and capacities; only four incidences, fixed finite search.
  for(let code=0;code<256&&!ok;code++){
    const bucket=[0,1,2,3].map(i=>(code>>(2*i))&3);
    for(let c=0;c<256&&!ok;c++){
      const cap=[0,1,2,3].map(i=>(c>>(2*i))&3);const V=new Set();
      for(let m=0;m<16;m++)if((m&~live)===0&&pop(m)===rank){const n=[0,0,0,0];for(let i=0;i<4;i++)if(m&(1<<i))n[bucket[i]]++;if(n.every((v,i)=>v<=cap[i]))V.add(m);}
      if(V.size===W.size&&[...V].every(m=>W.has(m)))ok=true;
    }
  }
  assert(ok);const tset=new Set();for(const a of R)for(const b of S)if(phase(a)!==phase(b))tset.add(phase(a));if(tset.size===2)both++;else one++;
}
assert.equal(nonempty,164);assert.equal(empty,32);console.log(JSON.stringify({nonempty,empty,both,one}));

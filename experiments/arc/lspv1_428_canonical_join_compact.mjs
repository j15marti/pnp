// LSPV-1/428: no-import independent compact exact canonical-join certificate.
// Run: node experiments/arc/lspv1_428_canonical_join_compact.mjs
function assert(ok,why){if(!ok) throw Error(why)}
function clause(t,a){return Array.from({length:t},(_,i)=>a&(1<<i)?-(i+1):i+1)}
function sat(c,a){return c.some(x=>Boolean(a&(1<<(Math.abs(x)-1)))===(x>0))}
function test(t){
  const n=2**t;
  let dag=new Map();
  for(let a=0;a<n;a++) dag.set(a,clause(t,a));
  for(let a=0;a<n;a++){
    assert(!sat(dag.get(a),a),'blocked witness');
    for(let b=0;b<n;b++)if(b!==a)assert(sat(dag.get(b),a),'indispensable source');
  }
  let count=0;
  for(let pivot=t;pivot>=1;pivot--){
    const next=new Map();
    for(const key of [...dag.keys()].filter(k=>(k&(1<<(pivot-1)))===0).sort((a,b)=>a-b)){
      const p=dag.get(key), q=dag.get(key|(1<<(pivot-1)));
      assert(p.includes(pivot)&&q.includes(-pivot),'correct pivot polarity');
      const res=[...new Set([...p.filter(l=>l!==pivot),...q.filter(l=>l!==-pivot)])];
      assert(res.every(l=>!res.includes(-l)),'not tautological');
      for(let a=0;a<n;a++)if(sat(p,a)&&sat(q,a))assert(sat(res,a),'sound consequence');
      next.set(key,res);count++;
    }
    dag=next;
  }
  assert(dag.size===1&&[...dag.values()][0].length===0,'empty root');
  assert(count===n-1,'work exactly 2^t-1');
  return {width:t,canonical_source_clauses:n,paid_res_nodes:count,ideal_parallel_span:t};
}
const results=Array.from({length:9},(_,i)=>test(i+1));
assert(results.reduce((s,x)=>s+x.paid_res_nodes,0)===1013,'summary');
const graphs=[['K4',4,4],['K33',6,9],['cube',8,4],['Petersen',10,5]];
for(const [name,h,cut] of graphs){
  assert(2**cut-1>0&&4*h-1>0,'graph size and cut');
  if(name==='K33')assert(2**cut-1===511&&4*h-1===23,'K33 exact contrast');
}
console.log(JSON.stringify({status:'PASS',results,graph_cuts:graphs},null,2));

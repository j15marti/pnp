/* LSPV-2/492: standalone finite verification, no third-party dependencies.
 * Math theorem is symbolic and NOT inferred from these tests.
 * Execute: node experiments/arc/lspv2_492_sensitivity_projection.cjs
 */
function audit492(){
  function claim(ok,msg){if(!ok)throw new Error(msg||"failed"); checks++}
  function make(m){
    const F=[];
    for(let i=1;i<=m;i++)
      for(const y of [1,-1])for(const z of [1,-1])
        F.push([i,y*(m+i),z*(2*m+i)]);
    return F;
  }
  function sat(F,mask){
    return F.every(C=>C.some(l=>((mask>>>(Math.abs(l)-1))&1)===(l>0?1:0)));
  }
  let checks=0, assignments=0, pivots=0, negatives=0, rows=[];
  for(let m=1;m<=4;m++){
    const F=make(m), U=Array.from({length:m},(_,i)=>[i+1]);
    claim(F.length===4*m && F.every(c=>new Set(c.map(Math.abs)).size===3),"strict");
    let yes=0;
    for(let mask=0;mask<(1<<(3*m));mask++){
      assignments++;
      let want=U.every(c=>sat([c],mask));
      claim(sat(F,mask)===want,"projection");
      if(!want)continue;
      yes++;
      let used=new Set();
      for(let i=0;i<m;i++){
        const flip=mask^(1<<i);
        claim(!sat(F,flip),"sensitivity");
        const unique=[];
        for(let j=0;j<F.length;j++)if(!sat([F[j]],flip))unique.push(j);
        claim(unique.length===1,"unique flip clause");
        claim(!used.has(unique[0]),"duplicate pivotal clause");
        used.add(unique[0]);pivots++;
      }
      claim(used.size===m,"pivotal");
    }
    const missing=U.slice(0,m-1);
    const a=(1<<(m-1))-1;
    claim(sat(missing,a)&&!sat(F,a),"missing x child must fail pointwise equivalence");
    rows.push({m,source_clauses:F.length,satisfying_assignments:yes,pointwise_pivots:m});
  }
  const malformed=[[1,1,2],[1,-1,2],[1,2],[0,1,2],[]];
  for(const c of malformed){
    const ok=(c.length===3&&c.every(v=>v!==0)&&new Set(c.map(Math.abs)).size===3);
    claim(!ok,"malformed accepted"); negatives++;
  }
  function encodedSize(m,n){
    const b=Math.ceil(Math.log2(128*(n+m+3)));
    return 3*b+1+3*m*(b+2);
  }
  const large=[];
  for(const m of [16,64,512,8192,65536,1000000]){
    const src=encodedSize(4*m,3*m);
    const minChild=encodedSize(m,m);
    claim(minChild>Math.sqrt(src),"large m threshold");
    large.push({m,source_bits:src,lower_child_bits:minChild,source_sqrt:Math.sqrt(src)});
  }
  return {status:"PASS",checks,assignments,pivots,negative_controls:negatives,rows,large,
    scope:"Finite strict-3CNF positive/negative sensitivities. No all-machine time lower bound. No R_mix341/FLMV native execution."};
}
if(typeof module!=="undefined"&&module.exports){module.exports={audit492}; if(require.main===module)console.log(JSON.stringify(audit492(),null,2));}
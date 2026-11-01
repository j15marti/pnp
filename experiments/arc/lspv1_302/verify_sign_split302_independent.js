/* Standalone independent verifier, no import of producer. */
function independent(){
  const plus=[
    [[1,2,3],[1,4,5],[2,4,6],[3,5,6]],
    [[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9]],
    [[1,2,7],[1,3,8],[4,5,9],[4,6,10],[2,3,5],[6,11,12],[7,11,13],[8,12,14],[9,13,15],[10,14,15]]
  ];
  const minus=[
    [[1,2,4],[1,3,6],[2,3,5],[4,5,6]],
    [[4,6,8],[1,6,7],[2,3,4],[3,5,8],[1,2,9],[5,7,9]],
    [[1,2,11],[2,3,11],[1,3,12],[4,5,13],[5,6,14],[4,6,15],[7,8,12],[8,9,13],[9,10,14],[10,7,15]]
  ];
  let checked=0;
  function assert(p,s){checked++;if(!p)throw Error(s)}
  function c(i,j){const rows=plus[i].map(x=>x.map(v=>v)),nn=minus[i].map(x=>x.map(v=>-v));return rows.concat(nn)[j]}
  function tt(clause,mask){return clause.some(l=>((mask>>(Math.abs(l)-1))&1)==Number(l>0))}
  const targets=[20,70,1032],observations=[];
  for(let fi=0;fi<3;fi++){
    const n=3*(plus[fi].length/2),m=plus[fi].length*2,clauses=Array.from({length:m},(_,j)=>c(fi,j));let models=0,weights={};
    const degree={};
    for(const clause of clauses)for(const l of clause)degree[l]=(degree[l]||0)+1;
    for(let i=1;i<=n;i++)assert(degree[i]===2&&degree[-i]===2,"grammar");
    for(let bits=0;bits<2**n;bits++){
      for(const cl of clauses){
        const nt=cl.filter(l=>((bits>>(Math.abs(l)-1))&1)==Number(l>0)).length;
        const ct=cl.filter(l=>(((2**n-1-bits)>>(Math.abs(l)-1))&1)==Number(l>0)).length;
        assert(nt+ct===3,"complement");
      }
      if(clauses.every(cl=>tt(cl,bits))){
        const w=bits.toString(2).split("1").length-1;
        assert(w>=n/3&&w<=2*n/3,"weight");
        models++;weights[w]=(weights[w]||0)+1;
        const ep=clauses.filter(cl=>cl[0]>0).reduce((s,cl)=>s+cl.filter(l=>((bits>>(l-1))&1)).length-1,0);
        const em=clauses.filter(cl=>cl[0]<0).reduce((s,cl)=>s+cl.filter(l=>!((bits>>(Math.abs(l)-1))&1)).length-1,0);
        assert(ep===2*(w-n/3)&&em===2*(2*n/3-w),"polarities");
      }
    }
    assert(models===targets[fi],"models");
    observations.push({n,m,models,weights});
  }
  const ticket=(m)=>{let p=[1n];for(let j=0;j<m;j++){let q=Array(p.length+2).fill(0n);for(let i=0;i<p.length;i++){q[i]+=p[i];q[i+1]+=3n*p[i];q[i+2]+=p[i]}p=q;}let all=0n,split=0n;for(let j=0;j<=m;j++){let v=p[j]*p[m-j];all+=v;if(!(j%2))split+=v;}return [all.toString(),split.toString()]};
  assert(JSON.stringify(ticket(4))===JSON.stringify(["7210","3754"]),"ticket n6");
  assert(JSON.stringify(ticket(6))===JSON.stringify(["1021306","507118"]),"ticket n9");
  assert(JSON.stringify(ticket(10))===JSON.stringify(["23623844028","11809659012"]),"ticket n15");
  return {status:"PASS",independent_generation:true,checks:checked,sources:observations,coefficients_validated:true,warning:"Offline exhaustive small controls; no native-machine FLMV or universal ARC transfer."};
}
console.log(JSON.stringify(independent(),null,2));

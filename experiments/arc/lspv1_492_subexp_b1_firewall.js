// LSPV-1/492 JS independent finite controls. Does NOT execute the ETH algorithms or Pang theorem.
function test492(){
  let tests=0, sat=0, unsat=0, bad=0;
  const sampleRows=[];
  function count(n,cs){
    let z=0;
    for(let b=0;b<(1<<n);b++){
      if(cs.every(c=>c.some(l=>Boolean(b&(1<<(Math.abs(l)-1)))===(l>0))))z++;
    }
    return z;
  }
  function norm(n,cs){
    let used=[...new Set(cs.flat().map(Math.abs))].sort((a,b)=>a-b);
    let remap=new Map(used.map((x,i)=>[x,i+1]));
    let normcs=[...new Set(cs.map(c=>c.map(x=>(x<0?-1:1)*remap.get(Math.abs(x))).sort((a,b)=>a-b).join(",")))].map(s=>s.split(",").map(Number));
    return [used.length,normcs,n-used.length];
  }
  function valid(n,cs){
    return Number.isInteger(n)&&n>=0 && Array.isArray(cs)&&cs.every(c=>Array.isArray(c)&&c.length===3&&c.every(x=>Number.isInteger(x)&&x!==0&&Math.abs(x)<=n)&&new Set(c.map(Math.abs)).size===3);
  }
  let state=74291;
  function rand(k){state=(Math.imul(state,1664525)+1013904223)>>>0;return state%k;}
  for(let n=3;n<=9;n++){
    for(let trial=0;trial<20;trial++){
      const cs=[];
      for(let t=0;t<8*n;t++){
        const avail=Array.from({length:n},(_,i)=>i+1),c=[];
        for(let j=0;j<3;j++){let k=rand(avail.length), v=avail.splice(k,1)[0];c.push(rand(2)?v:-v);}
        cs.push(c);
      }
      if(!valid(n,cs))throw Error("strict3 error");
      tests++;
      const a=count(n,cs),[nn,short,free]=norm(n,cs),b=count(nn,short)*(2**free);
      if(a!==b)throw Error("source projection mismatch");
      tests++;
      a===0?unsat++:sat++;
      if(trial===0)sampleRows.push({n,clauses:cs.length,model_count:a,free_vars:free});
    }
  }
  const cubes=[];
  for(let j=0;j<8;j++)cubes.push([1,2,3].map((v,i)=>(j&(1<<i))?v:-v));
  if(count(3,cubes)!==0||count(3,cubes.slice(0,7))!==1||count(3,[])!==8)throw Error("SAT controls");
  tests+=3;
  for(const b of [[[1,1,2]],[[1,2,0]],[[1,2,4]],[[1,2]],[[1,2,3,4]],[[true,2,3]]]){
    if(valid(3,b))throw Error("malformed accepted");tests++;bad++;
  }
  const rates=[];
  for(const z of [8,12,16,20,24,32,40]){
    const ratio=z*z/Math.sqrt(2**z);
    rates.push({log2_log2_n:z,ratio});
    if(!(ratio>=0))throw Error("rate arithmetic");
    tests++;
  }
  if(!(rates[6].ratio<rates[0].ratio))throw Error("illustration");
  tests++;
  return {status:"FINITE CONTROLS ONLY; no Lean replay",checks:tests,sampled_strict3:140,sat_samples:sat,unsat_samples:unsat,malformed_rejections:bad,sampleRows,rates};
}
const out=test492();
if (typeof console !== 'undefined') console.log(JSON.stringify(out,null,2));

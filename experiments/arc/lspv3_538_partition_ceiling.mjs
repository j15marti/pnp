// LSPV-3/538: source-partition abstract ceiling, independent finite test.
// Restricted may abstraction only; NOT historical R_mix341 checker.
let checks=0;
function ok(c,m){ checks++; if(!c) throw new Error(m); }
function php(n){
 const v=(i,j)=>1+i*n+j, a=[];
 for(let i=0;i<=n;i++)a.push(Array.from({length:n},(_,j)=>v(i,j)));
 for(let j=0;j<n;j++)for(let i=0;i<=n;i++)for(let k=i+1;k<=n;k++)a.push([-v(i,j),-v(k,j)]);
 return a;
}
const holds=(F,a)=>F.every(C=>C.some(l=>a[Math.abs(l)-1]===(l>0)));
function run(){
 const rows=[];
 for(const n of [2,3]){
  const F=php(n),m=F.length,p=n+1,bitN=n*p;
  let total=0;
  for(let mask=0;mask<(1<<bitN);mask++){
   const a=Array.from({length:bitN},(_,j)=>Boolean((mask>>j)&1));
   if(holds(F,a))total++;
  }
  ok(total===0,'PHP UNSAT');
  let witnessCount=0;
  for(let d=0;d<m;d++){
   const a=Array(bitN).fill(false);
   if(d<p){
    let j=0;for(let i=0;i<p;i++)if(i!==d)a[i*n+j++]=true;
   }else{
    const pairs=[];
    for(let i=0;i<p;i++)for(let k=i+1;k<p;k++)pairs.push([i,k]);
    const idx=d-p,j=Math.floor(idx/pairs.length),pair=pairs[idx%pairs.length];
    for(const i of pair)a[i*n+j]=true;
    let q=0;
    for(let i=0;i<p;i++)if(!pair.includes(i)){
     while(q===j)q++;
     a[i*n+q++]=true;
    }
   }
   ok(!holds(F,a) && holds(F.filter((_,i)=>i!==d),a),'indispensable original clause');
   witnessCount++;
  }
  let blocks=F.map((_,i)=>[i]), merges=0;
  while(blocks.length>1){
   blocks=[[...blocks[0],...blocks[1]],...blocks.slice(2)];
   merges++; 
  }
  ok(merges===m-1 && blocks[0].length===m,'m-1 spanning-merge abstract goal');
  ok(!F[0].some(l=>F[1].includes(-l)),'first pair has no RES pivot');
  ok(new Set([...F[0],...F[1]].map(Math.abs)).size>3,'AND3 support too large');
  // One-step typed CEGAR rejects this RES-labeled spurious transition;
  // it does not exclude other rule types or certify a full proof minimum.
  rows.push({holes:n,pigeons:p,variables:bitN,original_clauses:m,essentiality_witnesses:witnessCount,
    satisfying_assignments:total,abstract_paid_merges:merges,
    initial_merge_resolution_legal:false,initial_merge_and3_legal:false});
 }
 return {status:'PASS',model:'restricted unrestricted-pair-merge partition may abstraction',checks,
         historical_native_checker_executed:false,instances:rows};
}
const result=run();
if(typeof process!=='undefined')console.log(JSON.stringify(result,null,2));

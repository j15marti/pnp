const run = function(){
 const parity=x=>{let p=0;while(x){p^=1;x&=x-1}return p};
 const rank=(vs,n)=>{const b=Array(n).fill(0);let r=0;for(let v of vs)while(v){let i=31-Math.clz32(v);if(b[i])v^=b[i];else{b[i]=v;r++;break}}return r};
 const assert=(x,m)=>{if(!x)throw Error(m)};
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(([a,b,c])=>({rows:[(1<<a)^(1<<b),(1<<a)^(1<<c)],rhs:[0,0]}));
 const toy=Array.from({length:4},(_,i)=>({rows:[1,2],rhs:[i&1,i>>1]}));
 function test(base,n,r){
  let owners=[{rows:[],rhs:[]}];for(let j=0;j<r;j++)owners=owners.flatMap(p=>base.map(q=>({rows:p.rows.concat(q.rows.map(a=>a<<(j*n))),rhs:p.rhs.concat(q.rhs)})));
  let d=n*r,lim=1<<d, violates=(p,x)=>p.rows.every((a,j)=>parity(a&x)===p.rhs[j]);
  let unique=Array(owners.length).fill(0),root=0,baseNeighbor=base.slice(1),satWords=[];
  let min=Infinity,kernel=0,checks=0;
  for(let x=0;x<lim;x++){
   let bad=[];for(let i=0;i<owners.length;i++)if(violates(owners[i],x))bad.push(i);
   if(!bad.length)root++;if(bad.length===1)unique[bad[0]]++;
   if(Array.from({length:r},(_,j)=>baseNeighbor.every(p=>!violates(p,x>>(j*n)))).some(Boolean))satWords.push(x);
   let hits=owners.filter(p=>p.rows.some(a=>parity(a&x))).length;
   if(hits)min=Math.min(min,hits);else kernel++;
  }
  assert(root===0,'root');assert(unique.every(x=>x>0),'criticality');assert(min>=base.length**(r-1),'direction');checks+=3;
  const hull=rank(satWords.map(x=>x^satWords[0]),d);assert(hull===d,'full hull');checks++;
  let probes=0;
  for(let a=1;a<lim;a++){let seen=0;for(let x of satWords){seen|=1<<parity(a&x);if(seen===3)break}assert(seen===3,'rank1');probes++}
  if(r===3)for(let a=1;a<lim;a++)for(let b=a+1;b<lim;b++){let seen=0;for(let x of satWords){seen|=1<<(parity(a&x)+2*parity(b&x));if(seen===15)break}assert(seen===15,'rank2');probes++}
  let batchChecks=0;
  for(let k=0;k<20;k++){let ids=Array.from({length:base.length-1},(_,i)=>(k*13+i*7)%owners.length),w=[];for(let x=0;x<lim;x++)if(ids.every(i=>!violates(owners[i],x)))w.push(x);
   assert(rank(w.map(x=>x^w[0]),d)===d,'small batch hull');batchChecks++;}
  assert(owners.every(p=>rank(p.rows,d)>=2),'no rank-one unit');checks++;
  return {n,r,coordinates:d,owners:owners.length,enumerated_words:lim,root_models:root,single_deletion_model_min:Math.min(...unique),single_deletion_model_max:Math.max(...unique),all_factor_relaxation_models:satWords.length,hull_rank:hull,minimum_nonzero_direction_hits:min,invisible_directions:kernel,independent_affine_probes:probes,small_batch_hull_checks:batchChecks,assertions:checks+probes+batchChecks};
 }
 return {fano:test(fano,7,2),toy:test(toy,2,3)};
};
console.log(JSON.stringify(run(),null,2));

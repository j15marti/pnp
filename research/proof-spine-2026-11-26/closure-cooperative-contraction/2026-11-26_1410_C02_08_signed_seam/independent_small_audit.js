// Independent finite audit; brute-force affine forms, not production algorithm.
const audit=()=>{
 let seed=26112608, checks=0,contradictions=0,merges=0,pins=0,positive=0,negative=0;
 const rand=n=>(seed=(Math.imul(seed,1664525)+1013904223)>>>0)%n;
 const parity=x=>{let s=0;while(x){s^=1;x&=x-1;}return s;};
 const assert=x=>{checks++;if(!x)throw Error("audit assertion "+checks);};
 for(let j=0;j<1600;j++){
  let n=3+rand(5),F=[];
  for(let i=0;i<1+rand(9);i++){
   let scope=0;while(!scope)scope=rand(1<<n);while(parity(scope)>1)break;
   let rhs=rand(2),rows=[];for(let x=0;x<(1<<n);x++)if((x&~scope)===0&&parity(x)===rhs&&rand(4)!==0)rows.push(x);
   if(!rows.length){let x=0;while((x&~scope)!==0||parity(x)!==rhs)x=rand(1<<n);rows=[x];}
   F.push({scope,rhs,rows});
  }
  let exact=[],aff=[];
  for(let x=0;x<1<<n;x++){if(F.every(f=>parity(x&f.scope)===f.rhs))aff.push(x);if(F.every(f=>f.rows.includes(x&f.scope)))exact.push(x);}
  if(!aff.length){contradictions++;assert(!exact.length);negative++;continue;}
  let rep=[],map=[];
  for(let v=0;v<n;v++){
   let col=aff.map(x=>(x>>v)&1);if(col.every(b=>b===col[0])){map.push([-1,col[0]]);pins++;continue;}
   let r=rep.findIndex(u=>aff.every((x,i)=>((x>>u)&1)=== (col[i]^col[0]^((aff[0]>>u)&1))));
   if(r<0){r=rep.length;rep.push(v);map.push([r,0]);}else{map.push([r,col[0]^((aff[0]>>rep[r])&1)]);merges++;}
  }
  let lift=[];
  for(let q=0;q<1<<rep.length;q++){let x=0;map.forEach(([r,s],v)=>{x|=((r<0?0:(q>>r)&1)^s)<<v;});if(F.every(f=>f.rows.includes(x&f.scope)))lift.push(x);}
  assert(lift.length===exact.length);assert(lift.every(x=>exact.includes(x)));assert(exact.every(x=>lift.includes(x)));if(exact.length)positive++;else negative++;
 }
 // Counterexample: exact two on three bits. Its affine hull admits zero and its majority is 111.
 const R=[3,5,6];assert(R.every(x=>parity(x)===0));assert(!R.includes(0));assert(!R.includes((3&5)|(3&6)|(5&6)));
 return {seed:26112608,trials:1600,checks,contradictions,merges,pins,positive,negative};
};
console.log(JSON.stringify(audit(),null,2));

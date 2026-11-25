/* Node.js: node checker.js path/to/S23_inputs.json */
const fs=require('fs');
function run(inputs){
 let checks=0;const assert=x=>{checks++;if(!x)throw Error("assert "+checks)};
 const bit=(x,i)=>(x>>i)&1;
 const pop=x=>{let s=0;while(x){s++;x&=x-1}return s};
 const rank=(a)=>{let b=[];for(let x of a){while(x){let i=31-Math.clz32(x);if(b[i])x^=b[i];else{b[i]=x;break}}}return b.filter(Boolean).length};
 const hull=a=>a.length?rank(a.map(x=>x^a[0])):-1;
 const family=[];
 for(let k=1;k<=6;k++){
  const n=2*k, total=1<<n, R=[],S=[];let sourceTests=0;
  for(let y=0;y<total;y++){
   let good=false;for(let j=0;j<k;j++)if(((y>>(2*j))&3)===3)good=true;
   (good?S:R).push(y);
   let exists=false;for(let s=1;s<(1<<k);s++){sourceTests++;let ok=true;for(let j=0;j<k;j++)if(bit(s,j)&&((y>>(2*j))&3)!==3){ok=false;break}if(ok){exists=true;break}}
   assert(exists===good);
  }
  assert(R.length===3**k&&S.length===4**k-3**k);
  if(k>=2)assert(hull(S)===n);
  let maxAffine=-1,affineSets=0;
  if(k<=3){
   const bad=new Set(R), seen=new Set();
   for(const a of R){
    const todo=[[a]];
    while(todo.length){
     const A=todo.pop().sort((a,b)=>a-b), key=A.join(",");
     if(seen.has(key))continue;seen.add(key);affineSets++;
     const dim=Math.log2(A.length);assert(Number.isInteger(dim)&&dim<=k);maxAffine=Math.max(maxAffine,dim);
     for(const b of R){if(A.includes(b))continue;const d=a^b, B=A.map(x=>x^d);if(B.every(x=>bad.has(x))&&!B.some(x=>A.includes(x)))todo.push(A.concat(B))}
    }
   }
   assert(maxAffine===k);
  }
  // guard all odd-indexed coordinates to zero: no witness; unguard last pair's first coordinate: SAT.
  const pin=y=>Array.from({length:k},(_,j)=>bit(y,2*j)).every(x=>x===0);
  const relax=y=>Array.from({length:k-1},(_,j)=>bit(y,2*j)).every(x=>x===0);
  assert(!S.some(pin));assert(S.some(relax));
  family.push({k,n,rejected:R.length,accepted:S.length,hull:hull(S),minPacketCount:Math.ceil((1.5)**k),sourceTests,affineSets,maxAffine});
 }
 const jobs=[];
 for(const src of inputs)for(let j=0;j<src.pins.length;j++){
  const pin=src.pins[j];
  const choose=Array.from({length:src.n},(_,i)=>i).find(v=>{
   const own=src.O.filter(o=>o.t.includes(v));const nb=own.flatMap(o=>o.t.filter(x=>x!==v));
   return own.length===4&&new Set(nb).size===8&&(pin===-1||(v!==0&&!nb.includes(0)));
  });
  assert(choose!==undefined);
  const own=src.O.map((o,i)=>({...o,i})).filter(o=>o.t.includes(choose));
  const pairs=own.map(o=>o.t.filter(x=>x!==choose));const nb=pairs.flat();let accepted=[],directTests=0,pairTests=0;
  for(let w=0;w<256;w++){
   let ex=false;for(let v=0;v<2;v++){let ok=true;for(let p=0;p<4;p++){directTests++;const a=bit(w,2*p),b=bit(w,2*p+1);if(a===v&&b===v){ok=false;break}}if(ok)ex=true}
   let fact=true;for(let p=0;p<4;p++)for(let q=p+1;q<4;q++){pairTests++;const a=(w>>(2*p))&3,b=(w>>(2*q))&3;if((a===0&&b===3)||(a===3&&b===0))fact=false}
   assert(ex===fact);if(ex)accepted.push(w);
  }
  assert(accepted.length===146&&hull(accepted)===8);
  for(let p=0;p<4;p++)for(let q=p+1;q<4;q++){const a=[];for(let w=0;w<16;w++)if(w!==3&&w!==12)a.push(w);assert(hull(a)===4)}
  // Independent local projection onto every three boundary coordinates is full.
  for(let a=0;a<8;a++)for(let b=a+1;b<8;b++)for(let c=b+1;c<8;c++)assert(new Set(accepted.map(w=>bit(w,a)+2*bit(w,b)+4*bit(w,c))).size===8);
  // Each rejected word violates a factor; a center value is reconstructed for every accepted word.
  for(const w of accepted){const v=[0,1].find(v=>pairs.every((_,p)=>!(bit(w,2*p)===v&&bit(w,2*p+1)===v)));assert(v!==undefined)}
  jobs.push({id:src.id,job:j,pin,center:choose,sourceOwners:own.map(o=>o.i),pairs,accepted:accepted.length,relativeAccepted:accepted.length/2,explicitPackets:6,scope:nb,directTests,pairTests,postLocalAffineForces:0});
 }
 return {checks,family,jobs,limitations:"Local projection and lift only; no full cooperative solver, guard transported unchanged outside selected star, no physical CM."};
}
console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2],'utf8')))),null,2));

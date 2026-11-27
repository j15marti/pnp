function patternAudit(){
 const assert=x=>{if(!x)throw Error("pattern check failed")};
 const rows=[];let total=0,subsetChecks=0,constructed=0;
 function make(r){
  let C=[];for(let i=0;i<r;i++)C.push([-(i+1),r+i+1],[-(i+1),-(r+i+1)]);
  for(let i=0;i<r;i++)C.push([...(i?[-(2*r+i)]:[]),i+1,...(i<r-1?[2*r+i+1]:[])]);
  return C;
 }
 function violated(C,a){return C.reduce((mask,c,j)=>c.some(l=>a[Math.abs(l)]===Number(l>0))?mask:mask|(1<<j),0)}
 for(let r=2;r<=5;r++){
  const C=make(r),actual=new Set();
  for(let w=0;w<2**(3*r-1);w++){let a=Array.from({length:3*r},(_,j)=>j?((w>>(j-1))&1):0);actual.add(violated(C,a));total++}
  const theoretical=new Set();
  for(let w=1;w<4**r;w++){
   let digits=Array.from({length:r},(_,i)=>(w>>(2*i))&3);
   if(digits.some((d,i)=>d===3&&digits[i-1]===3))continue;
   let mask=0;for(let i=0;i<r;i++){let d=digits[i];if(d)mask|=1<<(d===3?2*r+i:2*i+d-1)}
   theoretical.add(mask);
   // Construct witness: if no C choose an A or B stage for a hidden descent.
   let desc=digits.map((d,i)=>d===3?i:-1).filter(i=>i>=0);
   if(!desc.length)desc=[digits.findIndex(d=>d===1||d===2)];
   let a=Array(3*r).fill(0),s=1;
   for(let i=0;i<r;i++){let d=digits[i];a[i+1]=Number(d===1||d===2);a[r+i+1]=Number(d===2);
    if(desc.includes(i))s=0;else if(desc.includes(i+1))s=1;
    if(i<r-1)a[2*r+i+1]=s;
   }
   assert(s===0&&violated(C,a)===mask);constructed++;
  }
  assert(actual.size===theoretical.size&&[...actual].every(x=>theoretical.has(x)));
  // Exact coefficients: every nonempty subset of an attained pattern is attained.
  for(let p of actual){let parity=0;for(let q=p;q;q=(q-1)&p){assert(actual.has(q));parity^=1;subsetChecks++}assert(parity===1)}
  rows.push({r,actualPatterns:actual.size,exactMinimumProducts:actual.size})
 }
 let f0=1n,f1=4n;const counts={1:"3"};
 for(let r=2;r<=256;r++){let f=3n*f1+3n*f0;f0=f1;f1=f;if([2,3,4,5,8,16,32,64,128,256].includes(r))counts[r]=(f-1n).toString()}
 for(let z of rows)assert(counts[z.r]===String(z.actualPatterns));
 return {rows,counts,exhaustiveAssignments:total,constructedPatterns:constructed,subsetChecks}
}
console.log(JSON.stringify(patternAudit(),null,2));

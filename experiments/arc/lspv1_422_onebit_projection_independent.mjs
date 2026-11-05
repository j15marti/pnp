#!/usr/bin/env node
// LSPV-1/422 independent exact-one and ternary-factor oracle. No dependencies.
// Inputs: all subsets of triples for n=4,5, no randomness.
const assert=(b,msg)=>{if(!b)throw Error(msg)};
const triples=n=>{let z=[];for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)for(let c=b+1;c<n;c++)z.push([a,b,c]);return z};
let checks=0, totals={};
for(const n of [4,5]) {
  const edges=triples(n); const count={only0:0,with1:0};
  for(let mask=0;mask<2**edges.length;mask++) {
    let witness=false;
    for(let a=0;a<2**n;a++) {
      let valid=true;
      for(let j=0;j<edges.length;j++)if((mask>>j)&1){
        const s=edges[j].reduce((v,k)=>v+((a>>k)&1),0);
        if(s!==1){valid=false;break}
      }
      if(valid){witness=true;break}
    }
    if(mask===0) for(let a=0;a<8;a++) {
      const [x,y,z]=[a&1,(a>>1)&1,(a>>2)&1];
      for(const t of [0,1]){
        let gates=false;
        for(let s=0;s<=1;s++){
          if(x+y===s&&s+z===t)gates=true;
        }
        assert(gates===(x+y+z===t),'local factor mismatch');checks++;
      }
    }
    count[witness?'with1':'only0']++;
    checks++;
  }
  totals[n]=count;
}
assert(totals[4].only0===1&&totals[4].with1===15,'n4');checks++;
assert(totals[5].only0===548&&totals[5].with1===476,'n5');checks++;
console.log(JSON.stringify({format:'LSPV1-422-independent',totals,checks}));

// Independent finite promise control for LSPV-4/445. Node.js >=18.
import assert from 'node:assert/strict';
let cases=0,clauseVisits=0;
for(const h of [4,8,10])for(let c=1;c<=4;c++)for(let a=0;a<(1<<c);a++)for(let b=0;b<(1<<c);b++){
  // A, fixed-zero, B is the source ordering; each vertex has four clauses.
  const blocks=[];
  for(let j=0;j<c;j++)for(let v=0;v<h;v++){
    const chi=v===0?(a>>j)&1:v===1?(b>>j)&1:0;
    blocks.push({j,v,signs:[1^chi,0^chi,0^chi,1^chi]});
  }
  const stream=[...blocks.filter(x=>x.v===0),...blocks.filter(x=>x.v>=2),...blocks.filter(x=>x.v===1)];
  assert.equal(stream.length,c*h);
  for(let p=1;p<=c;p++){
    const k=Math.ceil(c/p);let mismatch=false;let reads=0;
    for(let pass=0;pass<p;pass++){
      const bank=[];const low=pass*k, high=Math.min(c,low+k);
      for(const {j,v,signs} of stream){
        reads+=4;
        if(j<low||j>=high)continue;
        const charge=signs[0]^1;
        if(v===0)bank.push(charge);
        if(v===1)mismatch||=(bank[j-low]!==charge);
      }
    }
    assert.equal(!mismatch,a===b);
    assert.equal(reads,p*4*h*c);
    cases++;clauseVisits+=reads;
  }
}
console.log(JSON.stringify({status:'PASS',cases,clauseVisits}));

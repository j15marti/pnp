#!/usr/bin/env node
// Public compact independent single-bit sensitivity control, K4 odd/even Tseitin.
// Full 336 witnesses, parser and independent referee in the reproducibility ZIP.
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const h=4,n=6;
function tseitin(charge){
  const clauses=[];
  for(let v=0;v<h;v++){
    let incident=edges.map(([a,b],i)=>[a,b].includes(v)?i:-1).filter(i=>i>=0);
    for(let p=0;p<8;p++){
      let signs=[p&1,(p>>1)&1,(p>>2)&1];
      if(signs.reduce((a,b)=>a^b,0)!==charge[v])
        clauses.push(incident.map((i,j)=>[i,signs[j]]));
    }
  }
  return clauses;
}
function sat(f,a){return f.every(c=>c.some(([i,s])=>((a>>i)&1)!==s))}
const odd=tseitin([1,0,0,0]),even=tseitin([0,0,0,0]);
let oddModels=0,evenModels=0,sensitive=0;
for(let a=0;a<64;a++){
  oddModels+=sat(odd,a)?1:0;
  evenModels+=sat(even,a)?1:0;
}
if(oddModels!==0||evenModels!==8)throw new Error('bad parity controls');
for(let j=0;j<odd.length;j++)for(let k=0;k<3;k++){
  const F=odd.map((c,i)=>c.map(([v,s],t)=>[v,s^((j===i&&k===t)?1:0)]));
  if(!Array.from({length:64},(_,a)=>a).some(a=>sat(F,a)))throw new Error('non-SAT sign neighbor');
  sensitive++;
}
if(sensitive!==48)throw new Error('wrong count');
console.log(JSON.stringify({graph:'K4',odd_models:oddModels,even_models:evenModels,single_polarity_SAT_neighbors:sensitive,status:'PASS'}));

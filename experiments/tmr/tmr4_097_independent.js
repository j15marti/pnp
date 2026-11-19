'use strict';
// TMR-4/097 independent full-original-source verification, Node 18+.
const crypto = require('crypto');
const beat = (a,b) => ((b-a+5)%5 === 1 || (b-a+5)%5 === 3);
const examples = [
  ['unsat',[[0,1],[0,2],[1,0],[1,3]]],
  ['sat',[[0,1],[0,2],[1,3]]]
];
const output=[];
for(const [label,edges] of examples) {
  const src='T5-ROWS-v1 n=4 edges='+edges.length+'\n'+
    edges.slice().sort((a,b)=>a[0]-b[0]||a[1]-b[1]).map(p=>p.join(' ')+'\n').join('');
  let total=0, acceptedOriginal=0, profiles={};
  for(let u=0;u<5;u++)for(let v=0;v<5;v++) {
    let row0=0,row1=0;
    for(let a=0;a<5;a++) if(beat(u,v)&&beat(u,a)) row0++;
    for(let b=0;b<5;b++) if(beat(v,b)&&(label==='sat'||beat(v,u))) row1++;
    total+=row0*row1;
    const key=row0+','+row1;profiles[key]=(profiles[key]||0)+1;
    for(let a=0;a<5;a++)for(let b=0;b<5;b++) {
      const x=[u,v,a,b];
      if(edges.every(([i,j])=>beat(x[i],x[j]))) acceptedOriginal++;
    }
  }
  if(total!==acceptedOriginal || (label==='sat'?total!==40:total!==0))throw new Error('mismatch');
  output.push({label,source_sha256:crypto.createHash('sha256').update(src).digest('hex'),count:total,profiles});
}
console.log(JSON.stringify(output,null,2));

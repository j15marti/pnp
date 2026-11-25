// DA20 independent BS19 replay. Node: node checker.js frozen.json BS19_results.json
const fs=require('fs');
const checker=function checker(src,bs){
 const assert=(v,m)=>{if(!v)throw Error(m)};
 const sort=a=>[...new Set(a)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
 const neg=a=>a.map(x=>-x);
 const taut=a=>a.some(x=>a.includes(-x));
 const canon=a=>{a=sort(a);if(taut(a))return null;return a[0]<0?neg(a):a};
 const key=a=>a.join(",");
 const registry=a=>[...new Map(a.map(canon).filter(x=>x!==null).map(x=>[key(x),x])).values()];
 const eq=(a,b)=>JSON.stringify(a.map(key).sort())===JSON.stringify(b.map(key).sort());
 const ok=(C,word)=>C.every(a=>{let bits=a.map(x=>((word>>>(Math.abs(x)-1))&1)^(x<0?1:0));return bits.includes(0)&&bits.includes(1)});
 function step(C,v,stats){
  const buckets=C.filter(a=>a.some(x=>Math.abs(x)===v)).map(a=>{let b=a.includes(v)?a:neg(a);return b.filter(x=>x!==v)});
  const keep=C.filter(a=>a.every(x=>Math.abs(x)!==v));
  const fill=[];
  for(let i=0;i<buckets.length;i++)for(let j=i+1;j<buckets.length;j++){
   let a=buckets[i],b=buckets[j],p=sort([...a,...neg(b)]),q=sort([...neg(a),...b]);
   stats.pairs++;assert(eq([sort([...neg(a),...b])],[sort(neg(p))]),"opposite clauses");
   if(!taut(p)){fill.push(p);stats.resolutionLines+=2;assert(!taut(q),"mirror");}
  }
  const vars=[...new Set(buckets.flat().map(Math.abs))];assert(vars.length<20,"test boundary cap");
  const local=buckets.map(a=>[v,...a]);
  for(let w=0;w<2**vars.length;w++){
   let x=vars.reduce((z,u,i)=>z|(((w>>>i)&1)<<(u-1)),0);
   assert((ok(local,x)||ok(local,x|(1<<(v-1))))===ok(fill,x),"local exact projection");stats.localWords++;
  }
  return {C:registry([...keep,...fill]),buckets};
 }
 const stats={pairs:0,resolutionLines:0,localWords:0};
 const original=registry(src.O.map(o=>{assert(o.bad[0]===0&&o.bad[1]===7,"positive owners");return o.t.map(x=>x+1)}));
 assert(eq(original,registry(bs.source.O.map(o=>o.t.map(x=>x+1)))),"source identity");
 let C=original;const k=bs.common.find(o=>o.K===16);
 for(const s of k.residual.log){assert(!C.some(a=>a.length<3),"unexpected closure");let z=step(C,s.v,stats);assert(eq(z.buckets.map(sort),s.bucket.map(sort)),"bucket readback");C=z.C}
 assert(eq(C,registry(k.residual.C)),"final registry");
 const witnesses=[13310626,13308834,5193219];for(const x of witnesses)assert(ok(original,x)&&ok(C,x),"source and residual witness");
 const common={...stats,remaining:C.length,steps:k.residual.log.length,witnesses};
 const controls=[]; const F=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
 for(let t=-1;t<21;t++){
  let A=F.map(a=>a.slice());if(t>=0)A[Math.floor(t/3)][t%3]*=-1;
  const models=Array.from({length:128},(_,i)=>i).filter(x=>ok(A,x)).length;
  let B=registry(A),s={pairs:0,resolutionLines:0,localWords:0},steps=0;
  while(B.length&&!B.some(a=>a.length<2)){
   let vars=[...new Set(B.flat().map(Math.abs))];
   let binary=B.find(a=>a.length===2);let v=binary?Math.abs(binary[0]):vars[0];B=step(B,v,s).C;steps++;
  }
  let reject=B.some(a=>a.length<2);assert(reject===(models===0),"opposite label");
  controls.push({signFlip:t,models,reject,steps,...s});
 }
 return {common,controls};
};
console.log(JSON.stringify(checker(JSON.parse(fs.readFileSync(process.argv[2])),JSON.parse(fs.readFileSync(process.argv[3]))),null,2));

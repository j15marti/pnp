// Run with Node.js
const run=()=>{
let checks=0;const ok=x=>{checks++;if(!x)throw Error("check "+checks)};
const pop=x=>x.toString(2).replaceAll("0","").length;
const P=[3,5,6,9,10,12];
let counts={matroid:0,nonmatroid:0,matroid_but_grouped_planar_defect:0,grouped_planar_admitted:0};
for(let s=1;s<64;s++){
 let B=P.filter((p,i)=>s>>i&1),A=new Set(B);
 let ex=B.every(a=>B.every(b=>[0,1,2,3].every(i=>!(a&~b&(1<<i))||[0,1,2,3].some(j=>(b&~a&(1<<j))&&A.has(a^(1<<i)^(1<<j))))));
 let V=[0,1,2,3].filter(i=>B.some(b=>b>>i&1));
 let eq=(i,j)=>i===j||!A.has((1<<i)|(1<<j));
 let trans=V.every(i=>V.every(j=>V.every(k=>!eq(i,j)||!eq(j,k)||eq(i,k))));
 ok(ex===trans);
 if(ex)counts.matroid++;else counts.nonmatroid++;
 let R=new Set(B.map(b=>b^12)),p=(a,b)=>R.has(a)&&R.has(b),mg=(p(0,15)||p(5,10))===(p(3,12)||p(9,6));
 if(mg)counts.grouped_planar_admitted++;
 if(ex&&!mg)counts.matroid_but_grouped_planar_defect++;
}
let T=Array.from({length:8},(_,i)=>[(i>>2)&1,(i>>1)&1,i&1]);let feasible=0,queries=0;
for(let g=0;g<3**8;g++){
 let guard=[],z=g;for(let i=0;i<8;i++){guard.push(z%3);z=Math.floor(z/3)}
 let cost=Array.from({length:8},(_,i)=>((g*17+i*43)%101)-50),f=Array(16).fill(Infinity);
 for(let w=0;w<16;w++)for(let s=0;s<256;s++){
  if(pop(s)!==2||(s&3)!==(w&3)||guard.some((v,i)=>v!==0&&((s>>i&1)!==v-1)))continue;
  let r=[pop(w>>2),0,0,0,0,0],c=0;
  for(let i=0;i<8;i++)if(s>>i&1){let [x,y,z]=T[i];if(i>=2)r[x]++;r[2+y]++;r[4+z]++;c+=cost[i]}
  if(r.every(x=>x===1))f[w]=Math.min(f[w],c);
 }
 let mode=[f[0],f[5],f[6]];
 for(let w=0;w<16;w++){
  let e=w===0?mode[0]:[5,9].includes(w)?mode[1]:[6,10].includes(w)?mode[2]:Infinity;
  ok(f[w]===e);queries++;
 }
 if(mode.some(Number.isFinite))feasible++;
}
// Independently enumerate lexicographic occupancy scalarization for arbitrary signed rows.
let seed=261126;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};let scalarCases=0;
for(let k=0;k<2000;k++){
 let n=1+rnd(7),r=1+rnd(5),rows=Array.from({length:r},()=>Array.from({length:n},()=>rnd(3)-1)),target=Array.from({length:r},()=>rnd(2)),w=Array.from({length:n},()=>rnd(101)-50),M=1+w.reduce((a,b)=>a+Math.abs(b),0),best=Infinity,cost=Infinity,chosen=null;
 for(let a=0;a<1<<n;a++){
  let d=rows.map(R=>R.reduce((s,v,i)=>s+(v===0?0:v===1?(a>>i&1):1-(a>>i&1)),0)),c=w.reduce((s,v,i)=>s+v*(a>>i&1),0);
  if(d.every((x,i)=>x===target[i]))cost=Math.min(cost,c);
  if(d.every((x,i)=>(x&1)===target[i])){let obj=M*d.reduce((s,v)=>s+v,0)+c;if(obj<best){best=obj;chosen={d,c}}}
 }
 let c=chosen&&chosen.d.every((x,i)=>x===target[i])?chosen.c:Infinity;ok(c===cost);scalarCases++;
}
let local=[0,2,5,7],R=[];
for(let w=0;w<16;w++)for(let a of local)for(let b of local)if(a<b){
 if((+([a,b].includes(0))+2*+([a,b].includes(7)))!==(w&3))continue;
 let r=[w>>2&1,w>>3&1,0,0,0,0];
 for(let i of [a,b]){let [x,y,z]=T[i];if(i!==0&&i!==7)r[x]++;r[2+y]++;r[4+z]++}
 if(r.every(x=>x===1))R.push(w);
}
ok(R.join(",")==="0,15");
return {checks,guard_patterns:3**8,guard_word_checks:queries,nonempty_guard_patterns:feasible,rank2_supports:counts,scalarization_cases:scalarCases,nonmatroid_local_words:R};
};
console.log(JSON.stringify(run(),null,2));

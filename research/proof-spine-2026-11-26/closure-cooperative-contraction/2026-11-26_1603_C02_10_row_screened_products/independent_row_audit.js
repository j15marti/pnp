// Exact finite row-first vs explicit join audit (abstract, no native adapter claimed).
const audit = ()=>{
 let seed=2611261003;function rng(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 let checks=0, cases=0;const ok=b=>{checks++;if(!b)throw Error("check "+checks)};
 function prod(sets){let S=[0];for(const T of sets)S=S.flatMap(x=>T.map(y=>x|y));return S}
 for(let trial=0;trial<400;trial++){
  let k=1+rng(3), blocks=[],all=0,shift=0;
  for(let j=0;j<k;j++){let d=1+rng(3),mask=((1<<d)-1)<<shift;all|=mask;let S=[];for(let a=0;a<(1<<d);a++)if(rng(3))S.push(a<<shift);if(!S.length)S=[0];blocks.push({mask,S});shift+=d;}
  let M=rng(1<<shift), Y=rng(1<<shift), R=[];
  for(let r=0;r<(1<<shift);r++)if((r&~M)===0&&rng(3)===0)R.push(r);
  const direct=new Set(prod(blocks.map(b=>b.S)).filter(x=>R.includes(x&M)).map(x=>x&Y));
  let screened=new Set();
  for(const r of R){
   const sets=blocks.map(b=>[...new Set(b.S.filter(x=>((x^r)&M&b.mask)===0).map(x=>x&Y))]);
   for(const z of prod(sets))screened.add(z);
  }
  ok(direct.size===screened.size&&[...direct].every(z=>screened.has(z)));
  for(const z of screened){let witness=null;for(const r of R){const w=blocks.map(b=>b.S.find(x=>((x^r)&M&b.mask)===0&&((x^z)&Y&b.mask)===0));if(w.every(x=>x!==undefined)){witness=w.reduce((a,b)=>a|b,0);break}}
   ok(witness!==null&&R.includes(witness&M)&&(witness&Y)===z&&blocks.every(b=>b.S.includes(witness&b.mask)));
  }cases++;
 }
 for(let k=1;k<=9;k++){let S=new Set();for(let x=0;x<1<<k;x++)for(let i=0;i<k;i++)if((x&(1<<i))===0)S.add(x);ok(S.size===(1<<k)-1);ok(!S.has((1<<k)-1));}
 // Mixing independent functional coordinates by x+y=0 cannot preserve product.
 const diagonal=[0,3];ok(diagonal.length===2&&new Set(diagonal.map(x=>x&1)).size*new Set(diagonal.map(x=>x>>1)).size===4);
 return {checks,cases,seed:2611261003}
};
console.log(JSON.stringify(audit(),null,2));

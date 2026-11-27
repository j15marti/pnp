// Independent small replay of strict Rado and native rank-three obstruction.
// Run: node replay19.js
function main() {
 const ok=(b,m)=>{if(!b)throw Error(m)};
 const add=(a,b)=>new Set([...a].flatMap(x=>[...b].map(y=>x^y)));
 const sum=f=>f.reduce(add,new Set([0]));
 const span=v=>[...v].reduce((a,x)=>add(a,new Set([0,x])),new Set([0]));
 const eq=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
 const subs=k=>Array.from({length:(1<<k)-1},(_,i)=>Array.from({length:k},(_,j)=>j).filter(j=>(i+1)>>j&1));
 let seed=2611270032>>>0;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 const stat={tight:0,saturated:0,aperiodic:0,paths:0,coreSelections:0,lifts:0,seams:0};
 for(let n=2;n<=5;n++)for(let q=0;q<500;q++){
  const f=Array.from({length:1+rnd(5)},()=>new Set([0,...Array.from({length:1+rnd(5)},()=>rnd(1<<n))])).filter(a=>a.size>1);
  const I=subs(f.length).filter(I=>span(I.flatMap(i=>[...f[i]])).size<=2**I.length).sort((a,b)=>a.length-b.length);
  const S=sum(f);stat.tight++;
  if(I.length){let J=I[0],W=span(J.flatMap(i=>[...f[i]]));ok(W.size===2**J.length&&eq(W,sum(J.map(i=>f[i]))),'saturation');ok([...W].every(w=>eq(S,add(S,new Set([w])))),'period');stat.saturated++}
  const period=[...Array(1<<n).keys()].filter(w=>eq(S,add(S,new Set([w]))));
  if(period.length===1){ok(!I.length,'aperiodic');ok(f.length<=n-1,'active count');stat.aperiodic++}
 }
 for(let r=2;r<=14;r++){let S=sum(Array.from({length:r-1},(_,i)=>new Set([0,1<<i,1<<(i+1)])));ok(S.size===(1<<r)-1&&!S.has((1<<r)-1),'sharp path');stat.paths++}
 const C=new Map([[1,[0,0,1]],[2,[0,0,2]],[5,[0,1,2]],[8,[1,0,2]],[9,[1,1,0]],[13,[2,2,1]],[14,[2,2,3]],[17,[2,3,3]],[20,[3,2,3]],[21,[3,3,0]]]);
 const keys=[...C.keys()],combs=subs(keys.length).filter(a=>a.length===4).map(a=>a.map(i=>keys[i]));
 const pm=(I,T,p,n)=>p.every(c=>new Set(I.map(i=>T.get(i)[c])).size===n);
 ok(!combs.some(I=>pm(I,C,[0,1,2],4)),'core native NO');
 const P=[[0,1],[0,2],[1,2]];
 for(let p of P){let m=combs.filter(I=>pm(I,C,p,4));ok(new Set(m.flat()).size===C.size&&m.some(I=>I.includes(1))&&m.some(I=>!I.includes(1)),'core supports');stat.coreSelections+=combs.length}
 const M=combs.filter(I=>pm(I,C,[0,1],4));
 const response=(I,T)=>I.reduce((v,i)=>v^(1n<<BigInt(T.get(i)[2])),0n);
 for(let k of [0,1,2,4,8,16,32,64]){
  let T=new Map([...C].map(([i,t])=>[i,t.slice()]));let n=4+2*k;
  for(let a=0;a<k;a++)for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let z=0;z<2;z++)T.set(100+8*a+4*x+2*y+z,[4+2*a+x,4+2*a+y,4+2*a+z]);
  for(let a=0;a<k;a++){let b=a%2?7:0,u=a?100+8*(a-1)+b:1,v=100+8*a+b;[T.get(u)[2],T.get(v)[2]]=[T.get(v)[2],T.get(u)[2]]}
  let seen=new Set();
  for(let I of M){let J=I.slice();for(let a=0;a<k;a++)for(let b of I.includes(1)?[0,7]:[1,6])J.push(100+8*a+b);ok(pm(J,T,[0,1],n),'lift');let d=response(J,T)^((1n<<BigInt(n))-1n);seen.add(Number(d));stat.lifts++}
  ok(eq(seen,new Set([3,5,6,9,10,12,15])),'all seven target-relative defects');
  for(let q=0;q<k;q++){let end=4+2*q,inside=i=>C.has(i)||(i>=100&&i<100+8*q);ok([...T].filter(([i,t])=>inside(i)&&t[2]>=end).length===1&&[...T].filter(([i,t])=>!inside(i)&&t[2]<end).length===1,'balanced seam');stat.seams++}
  // Exact image check: original core response retained, each cube response collapses to zero.
  const H=z=>z<4?1<<z:2;
  for(let I of M){let v=I.reduce((x,i)=>x^H(T.get(i)[2]),0);ok(BigInt(v)===response(I,C),'core observation')}
  for(let a=0;a<k;a++)ok(Array.from({length:8},(_,b)=>H(T.get(100+8*a+b)[2])).every(x=>x===2),'cube quotient')
 }
 return stat;
}
if(typeof console!=='undefined')console.log(JSON.stringify(main()));

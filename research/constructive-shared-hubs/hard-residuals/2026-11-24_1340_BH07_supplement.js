function supplement(){
 let seed=0xb07cafe,checks=0,words=0,tests={tree:0,cyclic:0,binary:0},labels={SAT:0,UNSAT:0},maxInternal=0,maxBoundary=0;
 function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
 const assert=(v,m)=>{checks++;if(!v)throw Error(m)},sg=l=>+(l<0),id=Math.abs, val=(l,w)=>((w>>(id(l)-1))&1)^sg(l);
 function ok(f,w){let b=val(f.a[0],w);return !(f.b>>b&1)||f.a.some(l=>val(l,w)!==b)}
 for(let trial=0;trial<96;trial++){
  let t=3+rnd(4),kind=trial%3===0?"tree":"cyclic",deg=Array(t).fill(0),edges=[],adj=Array.from({length:t},()=>[]);
  const add=(i,j)=>{let v=edges.length+1,l=rnd(2)?v:-v,k=rnd(2)?v:-v;let e={i,j,l,k,v};edges.push(e);adj[i].push(e);adj[j].push(e);deg[i]++;deg[j]++};
  // bounded-degree random tree, optionally add multiple chords (parallel allowed).
  for(let i=1;i<t;i++){let opts=Array.from({length:i},(_,j)=>j).filter(j=>deg[j]<3);add(i,opts[rnd(opts.length)])}
  if(kind==="cyclic"){let target=1+rnd(3);for(let j=0;j<target;j++){let opts=deg.map((d,i)=>d<3?i:-1).filter(i=>i>=0);if(opts.length<2)break;let i=opts.splice(rnd(opts.length),1)[0];add(i,opts[rnd(opts.length)])}}
  if(edges.length<t)kind="tree";
  let e=edges.length,F=adj.map((a,i)=>({a:a.map(q=>q.i===i?q.l:q.k),b:1+rnd(3)})),ports=3*t-2*e,bn=Math.max(1,Math.min(ports,1+rnd(5)));
  for(let f of F)while(f.a.length<3){let v=e+1+rnd(bn);f.a.push(rnd(2)?v:-v)}
  maxInternal=Math.max(maxInternal,e);maxBoundary=Math.max(maxBoundary,bn);
  let p=[0],order=[0],seen=new Set(order);for(let i of order)for(let q of adj[i]){let j=q.i===i?q.j:q.i;if(!seen.has(j)){seen.add(j);order.push(j);p[j]=p[i]^1^sg(q.l)^sg(q.k)}}
  for(let b=0;b<2**bn;b++){
   let bad=false;if(kind==="tree")for(let root=0;root<2;root++){let hit=true;for(let i=0;i<t;i++){let c=root^p[i];if(!(F[i].b>>c&1)||F[i].a.some(l=>id(l)>e&&val(l,b<<e)!==c))hit=false}bad||=hit}
   let sat=false;for(let x=0;x<2**e;x++){words++;if(F.every(f=>ok(f,(b<<e)|x)))sat=true}
   assert(sat===!bad,kind+" projection with repeated boundary");tests[kind]++;labels[sat?"SAT":"UNSAT"]++
  }
 }
 for(let t=3;t<=7;t++)for(let trial=0;trial<24;trial++){let F=[];for(let i=0;i<t;i++){let v=i+1,w=(i+1)%t+1;F.push({a:[rnd(2)?v:-v,rnd(2)?w:-w],b:trial%2===0?3:1+rnd(3)})}
  let p=t%2;for(let f of F)for(let l of f.a)p^=sg(l);let pred=F.some(f=>f.b!==3)||p===0,sat=false;for(let x=0;x<2**t;x++){words++;if(F.every(f=>ok(f,x)))sat=true}assert(sat===pred,"binary signed parity");tests.binary++;labels[sat?"SAT":"UNSAT"]++}
 return {seed:"0xb07cafe",tests,labels,checks,referenceWords:words,maxInternal,maxBoundary}
}
console.log(JSON.stringify(supplement(),null,2));

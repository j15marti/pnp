function audit(){
const E0=[[0,7],[0,9],[0,19],[1,3],[1,14],[1,18],[2,11],[2,13],[2,16],[3,5],[3,19],[4,7],[4,13],[4,15],[5,6],[5,9],[6,8],[6,16],[7,11],[8,10],[8,12],[9,18],[10,11],[10,15],[12,14],[12,15],[13,17],[14,16],[17,18],[17,19]];
const check=(v,m)=>{if(!v)throw Error(m)},pc=x=>{let k=0;while(x){x&=x-1;k++}return k};
function solve(E,n,old){
 const inc=Array.from({length:n},()=>[]);E.forEach(([a,b],i)=>{inc[a].push([b,i]);inc[b].push([a,i])});check(inc.every(a=>a.length===3),"degree");
 function pm(V,allowed=-1){if(!V)return [0];let u=0;while(!(V>>u&1))u++;let out=[];for(const [v,i] of inc[u])if((V>>v&1)&&(allowed>>i&1))for(const p of pm(V^(1<<u)^(1<<v),allowed))out.push(p|(1<<i));return out}
 const P=pm((1<<n)-1);
 function cycles(M){let seen=new Set(),C=[];for(let s=0;s<n;s++)if(!seen.has(s)){let a=[],u=s,v=-1;while(!seen.has(u)){a.push(u);seen.add(u);let w=inc[u].find(([w,i])=>w!==v&&!(M>>i&1))[0];v=u;u=w}C.push(a)}return C}
 const O=P.map(p=>cycles(p).filter(c=>c.length%2).length),even=P.filter((_,i)=>!O[i]);if(old===null)old=P[O.indexOf(2)];check(old!==undefined,"old");
 const Cs=cycles(old);check(Cs.filter(c=>c.length%2).length===2,"odd2");let cuts=[0];for(const C of Cs){let masks=[];for(let t=0;t<(C.length%2?C.length:1);t++){let b=0,all=0;C.forEach((v,i)=>{all|=1<<v;if(i%2)b|=1<<C[(i+t)%C.length]});masks.push(b,b^all)}cuts=cuts.flatMap(x=>masks.map(y=>x|y))}cuts=cuts.filter(x=>!(x&1));
 let yes=0,no=0,strict=0,guardChecks=0,feasibleGuards=0,sccEdgeChecks=0,neutralGuards=0,matchingSupportChecks=0,neutralPairs=0,neutralRouteMax=0;
 for(let i=0;i<E.length;i++){check(P.some(p=>p>>i&1)&&P.some(p=>!(p>>i&1)),"ordinary closure");matchingSupportChecks++}
 for(const x of cuts){
  let D=0;E.forEach(([u,v],i)=>{if(!(((x>>u)^(x>>v))&1))D|=1<<i});let k=Math.min(...P.map(p=>pc(D&~p)));if(k<2)strict++;
  const ref=even.some(p=>pc(D&~p)===k);if(ref)yes++;else no++;
  if(k!==2)continue;let got=false;
  for(let i=0;i<E.length;i++)if(D>>i&1)for(let j=i+1;j<E.length;j++)if(D>>j&1){
   guardChecks++;const T=(1<<i)|(1<<j),F=D^T;let V=(1<<n)-1,valid=true;
   for(let z=0;z<E.length;z++)if(F>>z&1){let [a,b]=E[z],v=(1<<a)|(1<<b);if((V&v)!==v){valid=false;break}V^=v}
   let R=valid?pm(V,~T):[];const refP=P.filter(p=>(p&F)===F&&!(p&T));check(R.length===refP.length&&R.every(p=>refP.includes(p|F)),"guard equivalence");if(!R.length)continue;feasibleGuards++;
   const b=R[0],reach=Array.from({length:n},(_,q)=>1<<q);E.forEach(([a,c],z)=>{if((V>>a&1)&&(V>>c&1)&&!(T>>z&1)){check(((x>>a)^(x>>c))&1,"bipartite");if(x>>a&1)[a,c]=[c,a];if(b>>z&1)[a,c]=[c,a];reach[a]|=1<<c}});for(let z=0;z<n;z++)for(let a=0;a<n;a++)if(reach[a]>>z&1)reach[a]|=reach[z];
   let allowed=0;E.forEach(([a,c],z)=>{if((V>>a&1)&&(V>>c&1)&&!(T>>z&1)){const have=!!((b>>z&1)||((reach[a]>>c&1)&&(reach[c]>>a&1)));check(have===R.some(p=>p>>z&1),"allowed-edge SCC");sccEdgeChecks++;if(have)allowed|=1<<z}});
   check(pm(V,allowed).length===R.length,"allowed graph exact");
   for(const p of refP){const C=cycles(p);let parity=C.map(c=>{const S=new Set(c);return E.reduce((a,[u,v],z)=>a+((T>>z&1)&&S.has(u)&&S.has(v)?1:0),0)%2});check(parity.reduce((a,b)=>a+b,0)===C.filter(c=>c.length%2).length,"two terminal parity");if(!parity.some(Boolean)){got=true;neutralGuards++;break}}
  }
  check(got===ref,"neutral guard coverage");
  const opt=P.filter(p=>pc(D&~p)===k);
  // Independent test: each connected component of the symmetric difference
  // of two optimal PMs has zero change in objective; any subset is optimal.
  for(let a=0;a<opt.length;a++)for(let b=a+1;b<opt.length;b++){
   let A=opt[a],B=opt[b],d=A^B,rem=d,groups=[];while(rem){let z=0;while(!(rem>>z&1))z++;let stack=[...E[z]],seen=new Set(),g=0;while(stack.length){let u=stack.pop();if(seen.has(u))continue;seen.add(u);for(const [v,i] of inc[u])if(d>>i&1){g|=1<<i;stack.push(v)}}rem^=g;groups.push(g);check(pc(D&A&g)===pc(D&B&g),"zero-weight alternating cycle")}
   let H=A;for(const g of groups){H^=g;check(opt.includes(H),"neutral walk")};check(H===B,"route lift");neutralPairs++;neutralRouteMax=Math.max(neutralRouteMax,groups.length)
  }
 }
 return {n,matchings:P.length,even:even.length,oldCycles:Cs.map(c=>c.length),cuts:cuts.length,yes,no,strict,guardChecks,feasibleGuards,sccEdgeChecks,neutralGuards,matchingSupportChecks,neutralPairs,neutralRouteMax}
}
const petersen=[];for(let i=0;i<5;i++)petersen.push([i,(i+1)%5],[i,5+i],[5+i,5+(i+2)%5]);const prism=[];for(let i=0;i<5;i++)prism.push([i,(i+1)%5],[i,5+i],[5+i,5+(i+1)%5]);
const r={trap:solve(E0,20,74474769),petersen:solve(petersen,10,null),prism:solve(prism,10,null)};
check(r.trap.yes===39&&r.trap.no===101&&r.trap.strict===0,"trap counts");return r;
}
console.log(JSON.stringify(audit(),null,2));

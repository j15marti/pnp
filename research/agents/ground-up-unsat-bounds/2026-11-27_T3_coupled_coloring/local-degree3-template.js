const fs=require('node:fs'),crypto=require('node:crypto');
const verifyTemplate=function verifyTemplate(data){
 const A=(b,m)=>{if(!b)throw Error(m)},K=c=>c.slice().sort((a,b)=>a-b).join(","),P=ts=>{let s=new Set();for(let t of ts){let k=[...new Set(t)].sort((a,b)=>a-b).join(":");if(s.has(k))s.delete(k);else s.add(k)}return s},terms=p=>[...p].map(k=>k?k.split(":").map(Number):[]),plus=(...ps)=>P(ps.flatMap(terms)),mul=(p,q)=>P(terms(p).flatMap(t=>terms(q).map(s=>[...t,...s]))),one=P([[]]),v=i=>P([[i]]),colors=u=>[v(2*u+1),v(2*u+2),plus(one,v(2*u+1),v(2*u+2))];
 // Five local vertices: u,v,u-shadow,v-shadow,apex. Multipliers list 0 for constant, positive coordinate ID otherwise.
 const template=[
 [0,1,0,[0,6,8]],[0,1,1,[0,5,7]],[0,1,2,[0,5,7]],
 [0,3,0,[0,4,10]],[0,3,1,[0,3,9]],[0,3,2,[0,3,9]],
 [1,2,0,[0,2,10]],[1,2,1,[0,1,9]],[1,2,2,[0,1,9]],
 [4,2,0,[0,2,4]],[4,2,1,[0,1,2,3]],[4,2,2,[0,1,3]],
 [4,3,0,[0,2,4]],[4,3,1,[0,1,3,4]],[4,3,2,[0,1,3]]
 ];
 const localColors=Array.from({length:5},(_,i)=>colors(i));
 function T(u,s,a){let U=colors(u),S=colors(s),C=colors(a);return plus(...[0,1,2].map(c=>mul(C[c],plus(U[(c+1)%3],mul(U[c],S[(c+1)%3])))))}
 function row(u,v,c){return mul(colors(u)[c],colors(v)[c])}
 let left=plus(...template.flatMap(([i,j,c,m])=>m.map(vv=>mul(row(i,j,c),vv?v(vv):one))));
 let right=plus(one,T(0,2,4),T(1,3,4));A(plus(left,right).size===0,"symbolic local identity");
 let truthTests=0;for(let w=0;w<1024;w++){function evalP(p){let a=0;for(let t of terms(p))if(t.every(v=>w>>(v-1)&1))a^=1;return a}A(evalP(left)===evalP(right),"truth replay");truthTests++}
 let results=[];
 for(let x of data.families.filter(x=>x.label==="NO")){
  let F=x.raw.trimEnd().split("\n").slice(1).map(c=>c.split(" ").map(Number).slice(0,-1)),db=new Set(F.map(K)),{apex,pair,cycle}=x.recognizer,M=new Map(pair),sum=new Set(),used=new Set(),proof=[],counts={sourceChecks:0,monomialToggles:0,sourceOneHotChecks:0};
  A(cycle.length%2===1&&new Set(cycle).size===cycle.length,"cycle");
  function toggle(p){for(let t of p){counts.monomialToggles++;if(sum.has(t))sum.delete(t);else sum.add(t)}}
  for(let i=0;i<cycle.length;i++){
   let u=cycle[i],w=cycle[(i+1)%cycle.length],L=[u,w,M.get(u),M.get(w),apex];A(L.every(z=>Number.isInteger(z)&&z>=0&&z<x.vertices)&&new Set(L).size===5,"map");
   for(let z of L)used.add(z);
   for(let [p,q,c,m] of template){let a=L[p],b=L[q];counts.sourceChecks++;A(db.has(K([-(3*a+c+1),-(3*b+c+1)])),"source edge");
    for(let h of m){let mv=h?2*L[Math.floor((h-1)/2)]+(h-1)%2+1:0;toggle(mul(row(a,b,c),mv?v(mv):one));proof.push([a,b,c,mv])}
   }
  }
  for(let z of used){counts.sourceOneHotChecks++;A(db.has(K([3*z+1,3*z+2,3*z+3])),"positive one-hot"); // Exact one-hot gives affine row, verify the three binary exclusions too.
    for(let i=1;i<=3;i++)for(let j=i+1;j<=3;j++){counts.sourceOneHotChecks++;A(db.has(K([-(3*z+i),-(3*z+j)])),"one-hot binary")}
  }
  A(sum.size===1&&sum.has(""),"global constant");
  results.push({k:x.k,sha:x.sha,N:x.N,variables:x.variables,rows:x.rows,apex,pair,cycle,sourceGroupCount:used.size,templateTerms:template.reduce((n,x)=>n+x[3].length,0),proofTerms:proof.length,proof,counts,constant:true});
 }
 return {template,localIdentityMonomials:[...right],truthTests,results}
};
const d=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));for(let x of d.families){if(crypto.createHash('sha256').update(x.raw).digest('hex')!==x.sha||Buffer.byteLength(x.raw)*8!==x.N)throw Error('source hash');}
console.log(JSON.stringify(verifyTemplate(d),null,2));

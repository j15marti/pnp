
'use strict';
function audit(){
 let checks=0; const ck=(v,s)=>{checks++;if(!v)throw Error('FAIL '+s)};
 const bit=(x,i)=>(x>>>i)&1;
 const edge=(i,k,j)=>(k===i+1||(i===0&&k===j-1));
 function mix(x,j){
  let Q=0;
  for(let i=0;i<j;i++)for(let k=i+1;k<j;k++)if(!edge(i,k,j))Q^=bit(x,i)&bit(x,k);
  let g=0;for(let i=0;i<j;i++)g|=(Q^(bit(x,i)&bit(x,(i+1)%j)))<<i;
  return g;
 }
 function forward(x,z,j){let u=x^mix(z,j),v=z^mix(u,j);return [u,v]}
 function inverse(u,v,j){let z=v^mix(u,j),x=u^mix(z,j);return [x,z]}
 function build(m){
  let next=2*m, X=Array.from({length:m},(_,i)=>i+1),Z=Array.from({length:m},(_,i)=>m+i+1);
  const gates=[],clauses=[],memo=new Map(),scales=[];
  function gate(op,a,b){
   if(a===b)throw Error('identical operands');
   let key=op+':'+Math.min(a,b)+':'+Math.max(a,b);
   if(memo.has(key))return memo.get(key);
   const out=++next; let p=0,r=0;
   if(op==='AND'){
    p=++next;r=++next;
    clauses.push([-a,-b,out],[a,-out,p],[a,-out,-p],[b,-out,r],[b,-out,-r]);
   } else {
    clauses.push([-a,b,out],[a,-b,out],[a,b,-out],[-a,-b,-out]);
   }
   gates.push({op,a,b,out,p,r});memo.set(key,out);return out;
  }
  function g(w,j){
   const terms=[];
   for(let i=0;i<j;i++)for(let k=i+1;k<j;k++)if(!edge(i,k,j))terms.push(gate('AND',w[i],w[k]));
   let Q=terms[0];for(let i=1;i<terms.length;i++)Q=gate('XOR',Q,terms[i]);
   return Array.from({length:j},(_,i)=>gate('XOR',Q,gate('AND',w[i],w[(i+1)%j])));
  }
  for(let j=5;j<=m;j++){
   const U=g(Z,j).map((t,i)=>gate('XOR',X[i],t));
   const V=g(U,j).map((t,i)=>gate('XOR',Z[i],t));
   scales.push({j,U,V});
  }
  let source=clauses.map(c=>c.map(l=>(Math.abs(l)<=m&&Math.abs(l)%2===1)?-l:l));
  return {m,X,Z,gates,clauses:source,variables:next,scales,
   naiveG:scales.reduce((s,v)=>s+2*v.j*v.j-2,0)};
 }
 function assign(F,x,z){
  const a=new Uint8Array(F.variables+1);
  for(let i=0;i<F.m;i++){a[F.X[i]]=bit(x,i);a[F.Z[i]]=bit(z,i)}
  for(const g of F.gates){
   a[g.out]=g.op==='AND'?(a[g.a]&a[g.b]):(a[g.a]^a[g.b]);
   if(g.op==='AND'){a[g.p]=0;a[g.r]=0}
  }
  for(let i=0;i<F.m;i+=2)a[F.X[i]]^=1;
  return a;
 }
 const holds=(c,a)=>c.some(l=>(a[Math.abs(l)]===1)===(l>0));
 const sat=(F,a)=>F.clauses.every(c=>holds(c,a));
 const serialize=(F)=>'p cnf '+F.variables+' '+F.clauses.length+'\n'+F.clauses.map(c=>c.join(' ')+' 0').join('\n')+'\n';
 function recognize(str,limit){for(let j=5;j<=limit;j++)if(serialize(build(j))===str)return j;return null}
 const rows=[],tariffs=[];
 for(let m=5;m<=9;m++){
  const F=build(m), G=F.gates.length,V=F.variables,src=serialize(F);
  const S=(4n**BigInt(m+1)-4n**5n)/3n-BigInt(m-4);
  ck(F.naiveG>=G,'shared G upper');
  if(m>=6)ck(F.naiveG>G,'strict shared subgate reuse');
  ck(F.clauses.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),'proper CNF');
  ck(new Set(F.gates.map(g=>g.out)).size===G,'unique paid identities');
  const polarity=Array.from({length:V+1},()=>new Set());
  F.clauses.forEach(c=>c.forEach(l=>polarity[Math.abs(l)].add(Math.sign(l))));
  ck(polarity.slice(1).every(t=>t.size===2),'all variables both signs');
  ck(sat(F,assign(F,0,0)),'canonical shared witness');
  let zeros=new Uint8Array(V+1),ones=new Uint8Array(V+1);ones.fill(1);
  ck(!sat(F,zeros)&&!sat(F,ones),'all trivial assignments fail');
  ck(recognize(src,m)===m,'canonical recognizer');
  ck(recognize(src+' ',m)===null,'padding rejected');
  ck(recognize(src.replace('p cnf','x cnf'),m)===null,'malformed rejected');
  const sample=m<=6?(1<<(2*m)):64;
  for(let t=0;t<sample;t++){
   const x=m<=6?t&((1<<m)-1):(t*13+7)&((1<<m)-1);
   const z=m<=6?t>>m:(t*17+3)&((1<<m)-1);
   const a=assign(F,x,z);ck(sat(F,a),'all scale gates witness');
   for(const c of F.scales){
    const mask=(1<<c.j)-1,[u,v]=forward(x&mask,z&mask,c.j);
    ck(c.U.every((id,i)=>a[id]===bit(u,i)),'U relation');
    ck(c.V.every((id,i)=>a[id]===bit(v,i)),'V relation');
    const [xx,zz]=inverse(u,v,c.j);
    ck(xx===(x&mask)&&zz===(z&mask),'inverse relation');
   }
  }
  for(const c of F.scales)if(c.j<=7){
   const seen=new Set();let j=c.j;
   for(let x=0;x<(1<<j);x++)for(let z=0;z<(1<<j);z++){
    const [u,v]=forward(x,z,j), val=u|(v<<j);
    ck(!seen.has(val),'permutation injective');seen.add(val);
    const [xx,zz]=inverse(u,v,j);ck(xx===x&&zz===z,'inverse total');
   }
   ck(seen.size===(1<<(2*j)),'rank exact');
  }
  const good=assign(F,0,0);
  const rerouted=new Uint8Array(V+1);
  for(let i=1;i<=V;i++)rerouted[V+1-i]=good[i]^(i%3===0?1:0);
  let C=F.clauses.map(c=>c.map(l=>(l>0?1:-1)*(Math.abs(l)%3===0?-1:1)*(V+1-Math.abs(l)))).reverse();
  C=C.concat(C.slice(0,8));
  ck(C.every(c=>holds(c,rerouted)),'signed renamed reordered duplicated witness');
  const state={done:new Set(),active:false,halt:true,view:false};
  function p(){return [0n,0n,state.active?0n:S,BigInt(!state.active),BigInt(G-state.done.size),0n,BigInt(state.halt)]}
  const wt=[0n,0n,0n,1n,1n,0n,1n];
  const dot=v=>v.reduce((s,a,i)=>s+a*wt[i],0n);
  const initial=p(); ck(dot(initial)===BigInt(G+2),'exact primal initial');
  state.view=true;ck(p().every((v,i)=>v===initial[i]),'zero VIEW closure');
  state.view=false;ck(p().every((v,i)=>v===initial[i]),'zero SCC');
  for(const g of F.gates){
   const before=p();ck(!state.done.has(g.out),'identity only once');
   state.done.add(g.out);const d=before.map((v,i)=>v-p()[i]);
   ck(d[4]===1n&&d.every((v,i)=>i===4||v===0n),'CHECK delta');
   ck(dot(d)===1n,'CHECK tariff');
  }
  ck(state.done.size===G,'all gate AND obligations retained');
  const before=p();state.active=true;const delta=before.map((v,i)=>v-p()[i]);
  ck(delta[2]===S&&delta[3]===1n&&delta.every((v,i)=>(i===2||i===3)||v===0n),
    'one true nonterminal ACTIVATE simultaneous multiscale discharge');
  ck(dot(delta)===1n&&state.halt,'ACTIVATE price1 before HALT');
  ck(S>1n,'uniform positive rank tariff overdischarges');
  const prev=p();state.halt=false;const d=prev.map((v,i)=>v-p()[i]);
  ck(d[6]===1n&&dot(d)===1n&&p().every(v=>v===0n),'HALT and terminal');
  ck(BigInt(G+2)===dot(initial),'matching G+2 charged steps');
  tariffs.push({m,G,scaleRanks:F.scales.map(c=>({j:c.j,rank:'4^'+c.j})),
   rankSum:S.toString(),rows:[
    {rule:'VIEW/NOP',cost:0,delta:['0','0','0','0','0','0','0']},
    {rule:'CHECK_ID',cost:1,delta:['0','0','0','0','1','0','0']},
    {rule:'ACTIVATE_NONTERMINAL',cost:1,delta:['0','0',S.toString(),'1','0','0','0']},
    {rule:'HALT',cost:1,delta:['0','0','0','0','0','0','1']}
   ],exactCone:['lambda_GAMMA<=1','('+S.toString()+')lambda_SEP+lambda_FUS<=1','lambda_MACHINE<=1','lambda>=0'],
   optimalInitial:G+2,weights:['0','0','0','1','1','0','1']});
  rows.push({m,variables:V,clauses:F.clauses.length,distinctGates:G,
   noSharingUpper:F.naiveG,encodedBytes:src.length,scaleCount:F.scales.length,
   scaleRanks:F.scales.map(c=>'4^'+c.j),totalRankMinusOne:S.toString(),
   exactRecordWork:G+2});
 }
 return {id:'TMR2-MULTISCALE105',checks,failures:0,rows,tariffs,scope:'COMPUTATIONAL finite; symbolic proof restricted to authenticated shared-gate record calculus',PvsNP:'OPEN'};
}
if(typeof module!=='undefined' && require.main===module)console.log(JSON.stringify(audit(),null,2));

'use strict';
// LSPV-1 341 fixed-model strict signed BPHP3 -> unary PHP source derivations.
// Pure JS, no packages. Charges one per two-input definition and RES node.
// This is a PREFIX CERTIFICATE, NOT a completed PHP refutation.
function check(n) {
 if(n<4 || (n&(n-1))!==0)throw Error('holes must be power of two >=4');
 const ell=Math.log2(n),m=n+1,M=n*m*(m-1)/2;
 let next=m*ell+1,source=0,rescount=0,gatesCount=0;
 const rows=[],def=new Map(),pref=new Map(),gates=new Map(),coll=new Map(),imp=new Map();
 const key=(i,u)=>i+':'+u, bit=(i,t)=>i*ell+t+1;
 const match=(i,u,t)=>u[t]==='1'?bit(i,t):-bit(i,t);
 const norm=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
 const same=(a,b)=>a.length===b.length && a.every(x=>b.includes(x));
 const add=(cl,kind)=>{let c=norm(cl);if(c.some(x=>c.includes(-x)))throw Error('tautology');let idx=rows.length;rows.push({cl:c,kind});if(kind==='source')source++;if(kind==='res')rescount++;return idx};
 const res=(a,b,p)=>{let A=rows[a].cl,B=rows[b].cl;if(!A.includes(p)||!B.includes(-p))throw Error('bad pivot');return add([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)],'res')};
 const gate=(q,a,b)=>{gatesCount++;return [
 add([-q,a],'def'),add([-q,b],'def'),add([q,-a,-b],'def')]};
 for(let i=0;i<m;i++)for(let d=1;d<=ell;d++)for(let z=0;z<2**d;z++){
  let u=z.toString(2).padStart(d,'0');
  if(d===1)pref.set(key(i,u),match(i,u,0));
  else {let p=pref.get(key(i,u.slice(0,-1))),q=next++;
   pref.set(key(i,u),q);gates.set(key(i,u),gate(q,p,match(i,u,d-1)));
  }
 }
 for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)for(let z=0;z<n;z++){
  const u=z.toString(2).padStart(ell,'0'),w=[];
  for(let h of [i,j])for(let t=0;t<ell;t++)w.push(-match(h,u,t));
  const a=Array.from({length:2*ell-3},()=>next++),frags=[[w[0],w[1],a[0]]];
  for(let r=1;r<a.length;r++)frags.push([-a[r-1],w[r+1],a[r]]);
  frags.push([-a.at(-1),w.at(-2),w.at(-1)]);
  const ids=frags.map(x=>add(x,'source'));let curr=ids[0];
  for(let r=0;r<a.length;r++)curr=res(curr,ids[r+1],a[r]);
  if(!same(rows[curr].cl,w))throw Error('bad original clause');
  coll.set(i+':'+j+':'+z,curr);
 }
 function getImp(i,u,t) {
  const k=key(i,u)+':'+t;if(imp.has(k))return imp.get(k);
  if(u.length<2)throw Error('bad prefix');
  const g=gates.get(key(i,u)),q=pref.get(key(i,u)),v=u.slice(0,-1);
  const idx=t===u.length-1?g[1]:v.length===1?g[0]:res(g[0],getImp(i,v,t),pref.get(key(i,v)));
  if(!same(rows[idx].cl,[-q,match(i,u,t)]))throw Error('bad literal implication');
  imp.set(k,idx);return idx;
 }
 for(let i=0;i<m;i++)for(let z=0;z<n;z++){
  let u=z.toString(2).padStart(ell,'0');for(let t=0;t<ell;t++)getImp(i,u,t);
 }
 let collisionCount=0;
 for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)for(let z=0;z<n;z++){
  let u=z.toString(2).padStart(ell,'0'),curr=coll.get(i+':'+j+':'+z);
  for(let h of [i,j])for(let t=0;t<ell;t++)curr=res(curr,getImp(h,u,t),-match(h,u,t));
  if(!same(rows[curr].cl,[-pref.get(key(i,u)),-pref.get(key(j,u))]))throw Error('bad unary collision');
  collisionCount++;
 }
 function expand(i,u) {
  let d=u.length,a=u+'0',b=u+'1',q=pref.get(key(i,u)),A=pref.get(key(i,a)),B=pref.get(key(i,b));
  const ga=gates.get(key(i,a)),gb=gates.get(key(i,b));
  let curr=res(ga[2],gb[2],bit(i,d));
  if(!same(rows[curr].cl,[-q,A,B]))throw Error('bad split');
  for(let child of [a,b])if(child.length<ell)curr=res(curr,expand(i,child),pref.get(key(i,child)));
  let target=[-q];for(let z=0;z<n;z++){
   let v=z.toString(2).padStart(ell,'0');
   if(v.startsWith(u))target.push(pref.get(key(i,v)));
  }
  if(!same(rows[curr].cl,target))throw Error('bad prefix row');
  return curr;
 }
 for(let i=0;i<m;i++){
  const lo=expand(i,'0'),hi=expand(i,'1'),final=res(lo,hi,bit(i,0));
  const target=Array.from({length:n},(_,z)=>pref.get(key(i,z.toString(2).padStart(ell,'0'))));
  if(!same(rows[final].cl,target))throw Error('bad unary row');
 }
 if(source!==M*(2*ell-2))throw Error('source count');
 if(gatesCount!==m*(2**(ell+1)-4))throw Error('gate count');
 return {holes:n,ell,source_clauses:source,def_nodes:gatesCount,res_nodes:rescount,
         paid_prefix_cost:gatesCount+rescount,unary_rows:m,unary_collisions:collisionCount,
         clause_records:rows.length,full_refutation:false};
}
const results=[check(4),check(8)];
if(typeof console!=='undefined')console.log(JSON.stringify(results,null,2));

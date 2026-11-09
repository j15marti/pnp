/* LSPV-3/528: source-shared, fresh-private-DEF, two-copy reconvergence.
   Declared ER2-OWNER, NOT authenticated historical R_mix341 grammar.
   Runs with the pre-existing, blob-pinned /526 -> /523 -> /524 producers. */
'use strict';
const norm=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
const eq=(a,b)=>JSON.stringify(norm(a))===JSON.stringify(norm(b));
function splice(p){
 const x=p.proof,L=x.lines.map(n=>({...n,clause:[...n.clause]})),
       G=x.defs.map(g=>({...g,facets:[...g.facets]}));
 if(L.length!==237||G.length!==34||p.source_count!==21)throw Error('base count');
 const lit=n=>Math.abs(n)<=12?n:Math.sign(n)*(Math.abs(n)+34),
       ix=i=>i<21?i:237+i-21;
 if(L.slice(0,21).some(n=>n.kind!=='SOURCE')||L.slice(21).some(n=>n.kind==='SOURCE'))throw Error('sources');
 for(const g of x.defs)G.push({...g,id:lit(g.id),a:lit(g.a),b:lit(g.b),owner:g.owner+34,facets:g.facets.map(ix),label:'copy2_'+g.label});
 for(const n of x.lines.slice(21)){
  const t={...n,id:ix(n.id),clause:norm(n.clause.map(lit))};
  if(t.kind==='RES'){t.left=ix(n.left);t.right=ix(n.right);t.pivot=lit(n.pivot)}
  else if(t.kind==='FACET')t.owner+=34;
  else throw Error('unlicensed source');
  if(t.id!==L.length)throw Error('order');L.push(t);
 }
 const res=(a,b,pivot,goal)=>{
   if(!L[a].clause.includes(pivot))[a,b]=[b,a];
   if(!L[a].clause.includes(pivot)||!L[b].clause.includes(-pivot))throw Error('pivot');
   const c=norm([...L[a].clause.filter(i=>i!==pivot),...L[b].clause.filter(i=>i!==-pivot)]);
   if(!eq(c,goal))throw Error('resolvent');
   const id=L.length;L.push({id,kind:'RES',clause:c,left:a,right:b,pivot});return id;
 };
 const joins=[];
 for(const t of p.targets){
   const a=t.input,u=-t.bit,v=lit(u);
   joins.push({k:t.k,bit1:-u,bit2:-v,input:a,
     forward:res(t.positive,ix(t.negative),a,[u,-v]),
     backward:res(ix(t.positive),t.negative,a,[v,-u])});
 }
 return {model:'ER2-OWNER only, historical R_mix341 unverified',lines:L,defs:G,joins};
}
function verify(q){
 const L=q.lines,G=q.defs,c={SOURCE:0,RES:0,FACET:0};
 if(L.length!==459||G.length!==68||q.joins.length!==3)throw Error('size');
 for(let i=0;i<G.length;i++){const g=G[i];if(g.id!==13+i||g.owner!==i||Math.abs(g.a)>=g.id||Math.abs(g.b)>=g.id||Math.abs(g.a)===Math.abs(g.b))throw Error('DEF')}
 for(let i=0;i<L.length;i++){
   const n=L[i];if(n.id!==i||!eq(n.clause,norm(n.clause))||!(n.kind in c))throw Error('node');c[n.kind]++;
   if(n.kind==='SOURCE'){if(i>=21)throw Error('source');}
   if(n.kind==='FACET'){
     const g=G[n.owner],k=g?.facets.indexOf(i);
     if(k<0||!eq(n.clause,[[-g.id,g.a],[-g.id,g.b],[g.id,-g.a,-g.b]][k]))throw Error('facet');
   }
   if(n.kind==='RES'){
     if(n.left<0||n.right<0||n.left>=i||n.right>=i||n.pivot<=0)throw Error('ancestry');
     const a=L[n.left].clause,b=L[n.right].clause;
     if(!a.includes(n.pivot)||!b.includes(-n.pivot)||!eq(n.clause,[...a.filter(x=>x!==n.pivot),...b.filter(x=>x!==-n.pivot)]))throw Error('resolution');
   }
 }
 if(c.SOURCE!==21||c.RES!==234||c.FACET!==204)throw Error('counts');
 const s=new Set(L.slice(0,21).map(n=>n.clause.join(','))),expect=[];
 for(let i=0;i<3;i++)for(let j=0;j<3;j++)for(let k=0;k<3;k++)if((i+j+k)%3!==0)expect.push(norm([-1-i,-4-j,-7-k]).join(','));
 [[1,2,3],[4,5,6],[7,8,9]].forEach(a=>expect.push(a.join(',')));
 if(s.size!==21||expect.some(a=>!s.has(a)))throw Error('foreign source');
 for(const t of q.joins)if(t.input!==10+t.k||!eq(L[t.forward].clause,[-t.bit1,t.bit2])||!eq(L[t.backward].clause,[-t.bit2,t.bit1]))throw Error('join');
 return {source:21,RES:234,FACET:204,DEF:68,paid:302,records:459,join_RES:6};
}
if(require.main===module){
 const {build,check}=require('./lspv3_526_core_zero_splice.cjs');const p=build();check(p);
 const q=splice(p);console.log(JSON.stringify({status:'PASS / RESTRICTED',counts:verify(q)},null,2));
 if(process.argv[2]==='--certificate')require('fs').writeFileSync(process.argv[3]||'lspv3_528_certificate.json',JSON.stringify(q));
}
module.exports={splice,verify};

'use strict';
// LSPV-3/532: strict original 3-CNF, source-authenticated ordinary Resolution.
function make(k) {
 if(!Number.isSafeInteger(k)||k<1||k>200) throw Error('k out of range');
 const B=j=>j, I=j=>k+2+j, X=(e,r)=>3*e+r+1;
 const base=3*(2*k+1), source=[], rules=[], rows=new Map(), clauses=new Map(), pins=new Map();
 const E=v=>k===1?[[0,1],[1,1],[2,1]]:
  v===0?[[B(0),1],[B(1),1],[I(0),1]]:
  v===k-1?[[I(v-1),-1],[B(k),1],[B(k+1),1]]:
  [[I(v-1),-1],[B(v+1),1],[I(v),1]];
 const src=(c,tag)=>{let id=source.length+1;source.push({id,c,tag});return id};
 for(let e=0;e<2*k+1;e++)src([X(e,0),X(e,1),X(e,2)],'ALO');
 for(let v=0;v<k;v++){
  let a=E(v);
  for(let p=0;p<3;p++)for(let q=0;q<3;q++)for(let r=0;r<3;r++){
   if((a[0][1]*p+a[1][1]*q+a[2][1]*r+300)%3===0)continue;
   rows.set(v+':'+p+q+r,src([-X(a[0][0],p),-X(a[1][0],q),-X(a[2][0],r)],'wrong'+v));
  }
 }
 const gadget=[];
 for(let j=0;j<k+2;j++){
  let a=j===k+1?1:0, p=X(B(j),a),u=base+2*j+1,v=u+1;
  gadget.push({j,a,p,u,v,ids:[src([p,u,v],'pin'),src([p,u,-v],'pin'),
    src([p,-u,v],'pin'),src([p,-u,-v],'pin')]});
 }
 if(source.length!==24*k+9)throw Error('source count');
 for(let s of source)clauses.set(s.id,s.c);
 const resolve=(a,b,p,tag)=>{
  let A=clauses.get(a),C=clauses.get(b);
  if(!A||!C||!A.includes(p)||!C.includes(-p))throw Error('pivot '+tag);
  let c=[...new Set([...A.filter(x=>x!==p),...C.filter(x=>x!==-p)])];
  if(c.some(x=>c.includes(-x)))throw Error('tautology');
  let id=source.length+rules.length+1;
  rules.push({id,a,b,p,c,tag});clauses.set(id,c);return id;
 };
 for(let g of gadget){
  let t=resolve(g.ids[0],g.ids[1],g.v,'pin-a');
  let u=resolve(g.ids[2],g.ids[3],g.v,'pin-b');
  let z=resolve(t,u,g.u,'pin-unit');
  if(clauses.get(z).length!==1||clauses.get(z)[0]!==g.p)throw Error('bad pin');
  pins.set(B(g.j),{a:g.a,id:z});
 }
 for(let v=0;v<k-1;v++){
  let a=E(v),g=pins.get(a[0][0]),h=pins.get(a[1][0]);if(!g||!h)throw Error('input');
  let out=[0,1,2].find(t=>(a[0][1]*g.a+a[1][1]*h.a+a[2][1]*t+300)%3===0);
  let bad=[];
  for(let t=0;t<3;t++)if(t!==out){
   let r=rows.get(v+':'+g.a+h.a+t);
   let p=resolve(g.id,r,X(a[0][0],g.a),'bad-left');
   let q=resolve(h.id,p,X(a[1][0],h.a),'bad-right');
   bad.push([t,q]);
  }
  let p=resolve(a[2][0]+1,bad[0][1],X(a[2][0],bad[0][0]),'ALO1');
  let q=resolve(p,bad[1][1],X(a[2][0],bad[1][0]),'ALO2');
  if(clauses.get(q).length!==1||clauses.get(q)[0]!==X(a[2][0],out))throw Error('output');
  pins.set(a[2][0],{a:out,id:q});
 }
 let a=E(k-1),g=a.map(e=>pins.get(e[0]));if(g.some(z=>!z))throw Error('last input');
 let r=rows.get((k-1)+':'+g.map(z=>z.a).join(''));if(!r)throw Error('not UNSAT');
 let p=resolve(g[0].id,r,X(a[0][0],g[0].a),'last0');
 let q=resolve(g[1].id,p,X(a[1][0],g[1].a),'last1');
 let z=resolve(g[2].id,q,X(a[2][0],g[2].a),'FALSE');
 if(clauses.get(z).length||rules.length!==9*k+3)throw Error('final');
 return {k,variables:base+2*(k+2),source,rules,empty:z};
}
if(typeof module!=='undefined'&&require.main===module){
 const k=Number(process.argv[2]||4);
 process.stdout.write(JSON.stringify(make(k)));
}
